#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""拉取 sources.json 里的所有订阅源，归一化语法、合并去重、按策略裁剪，
输出 dist/block-merged.txt + dist/allow-merged.txt + dist/report.md + dist/conflicts.txt

设计要点
--------
1. 语法归一化（把各家五花八门的写法统一成 AGH DNS 规则）：
     hosts   `0.0.0.0 domain` / `127.0.0.1 domain` / 任意 IP + 域名  → `||domain^`
     裸域名  `domain`                                              → `||domain^`
     无 ^ 的  `||domain`                                            → `||domain^`
     去 BOM / 去行内注释 / 统一小写
2. allow 源里的规则一律当作放行（与 AGH 对 whitelist_filters 的处理一致），
   统一输出成 `@@||domain^`。这样 234 那份裸 `||domain^` 的白名单也能正确转换，
   并且转换后可以订阅到**普通 filters 槽位**，从而变成可被 $important 覆盖的。
3. 自建黑名单优先：blacklist.txt 里每个域名 D，都会把 allow 列表里的
   `D` 自身和 `D` 的所有父域条目剔除 —— 保证自建规则一定生效。
4. 同域冲突（既拦又放）默认保留 allow 侧（尊重防误杀），完整清单写进 conflicts.txt。
5. 输出排序 + 稳定格式，让 git diff 尽量小。

用法: python3 tools/merge.py [--sources sources.json] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 去掉尾部 | 之后，匹配 `||domain` / `||domain^` / `||domain^$mod`
RULE_RE = re.compile(r"^\|\|([a-z0-9][a-z0-9._-]*?)\^?(\$[a-z0-9_,.=~-]+)?$")
# 任意 IPv4/IPv6 + 域名（hosts 格式）
HOSTS_RE = re.compile(
    r"^(?:\d{1,3}(?:\.\d{1,3}){3}|[0-9a-f]{0,4}(?::[0-9a-f]{0,4}){2,})\s+(\S+)$",
    re.I,
)
BARE_DOMAIN_RE = re.compile(
    r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$"
)
# 通配符 / 正则：AGH 的 DNS 层对它们行为不可控，单独计数
WILDCARD_RE = re.compile(r"[*?]")
COMMENT_RE = re.compile(r"^\s*(?:!|#|＃|;|\[|\\)")
UA = "ad-dns-rules-merge/1.0 (+https://github.com/50521136/ad-dns-rules)"


def log(msg: str) -> None:
    print(msg, flush=True)


def fetch(url: str, retries: int = 3) -> str:
    """下载文本，带重试。支持 file: 前缀读本地。"""
    if url.startswith("file:"):
        p = ROOT / url[len("file:"):]
        if not p.exists():
            raise FileNotFoundError(f"本地源不存在: {p}")
        return p.read_text(encoding="utf-8", errors="replace")

    last: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception as e:  # noqa: BLE001
            last = e
            if attempt < retries:
                time.sleep(3 * attempt)
    raise RuntimeError(f"下载失败 {url}: {last}")


def labels(domain: str) -> int:
    return domain.count(".") + 1


def parents(domain: str) -> list[str]:
    """example.a.b.com → [a.b.com, b.com, com]（不含自身）"""
    parts = domain.split(".")
    return [".".join(parts[i:]) for i in range(1, len(parts))]


def parse_source(text: str) -> tuple[dict[str, int], list[str], list[str], list[str]]:
    """把一份列表拆成 (统计, 归一化规则, 通配符样本, 丢弃样本)。

    归一化后的规则形如 `||domain^` 或 `||domain^$mod`，不含 @@ 前缀。
    """
    stats = {"lines": 0, "comment": 0, "empty": 0, "hosts": 0,
             "bare": 0, "ok": 0, "wildcard": 0, "dropped": 0}
    rules: list[str] = []
    wild: list[str] = []
    dropped: list[str] = []

    for raw in text.splitlines():
        stats["lines"] += 1
        t = raw.lstrip("\ufeff").strip()
        if not t:
            stats["empty"] += 1
            continue
        if COMMENT_RE.match(t):
            stats["comment"] += 1
            continue
        # 行内注释（hosts / adblock 都可能出现）
        for sep in (" #", " !", "\t#"):
            if sep in t:
                t = t.split(sep, 1)[0].strip()
        if not t:
            stats["comment"] += 1
            continue

        t = t.lower()
        body = t[2:] if t.startswith("@@") else t
        body = body.rstrip("|").strip()

        dom: str | None = None

        m = HOSTS_RE.match(body)
        if m:
            cand = m.group(1).rstrip(".")
            if BARE_DOMAIN_RE.match(cand):
                dom = cand
                stats["hosts"] += 1
        if dom is None:
            m = RULE_RE.match(body)
            if m and BARE_DOMAIN_RE.match(m.group(1).rstrip(".")):
                dom = m.group(1).rstrip(".")
                stats["ok"] += 1
        if dom is None:
            # 通配符 / 正则 / 裸域名
            if WILDCARD_RE.search(body) or body.startswith("/"):
                stats["wildcard"] += 1
                if len(wild) < 30:
                    wild.append(t)
                continue
            if BARE_DOMAIN_RE.match(body):
                dom = body
                stats["bare"] += 1
        if dom is None:
            stats["dropped"] += 1
            if len(dropped) < 30:
                dropped.append(t)
            continue

        # 保留 $ 修饰符（block 侧才有意义；allow 侧调用方会剥掉）
        mod = ""
        mm = RULE_RE.match(body)
        if mm and mm.group(2):
            mod = mm.group(2)
        rules.append(f"||{dom}^{mod}")

    return stats, rules, wild, dropped


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sources", default="sources.json")
    ap.add_argument("--dry-run", action="store_true", help="只跑不写文件")
    args = ap.parse_args()

    cfg = json.loads((ROOT / args.sources).read_text(encoding="utf-8"))
    policy = cfg.get("policy", {})
    out_cfg = cfg.get("output", {})

    report: list[str] = ["# 合并报告", ""]
    rows: list[tuple[str, str, dict, int]] = []
    notes: list[str] = []

    def collect(kind: str) -> tuple[set[str], set[str]]:
        all_rules: set[str] = set()
        self_domains: set[str] = set()
        for src in cfg.get(kind, []):
            name = src.get("name", "?")
            if not src.get("enabled", True):
                log(f"  [跳过] {kind}/{name} (enabled=false)")
                continue
            try:
                text = fetch(src["url"])
            except Exception as e:  # noqa: BLE001
                log(f"  [失败] {kind}/{name}: {e}")
                notes.append(f"- ⚠️ **{kind}/{name}** 下载失败：`{e}`")
                continue

            stats, rules, wild, dropped = parse_source(text)
            uniq = set(rules)
            all_rules |= uniq
            rows.append((kind, name, stats, len(uniq)))
            if src.get("self"):
                self_domains |= {r[2:].rstrip("^").split("$")[0] for r in uniq}
            log(f"  [ok]   {kind}/{name:12s} 行={stats['lines']:7d} 有效={stats['ok']:7d} "
                f"hosts={stats['hosts']:6d} 裸域名={stats['bare']:6d} "
                f"去重后={len(uniq):7d} 通配符={stats['wildcard']:5d} 丢弃={stats['dropped']:5d}")
            if stats["wildcard"]:
                notes.append(
                    f"- `{kind}/{name}` 有 {stats['wildcard']} 条含通配符/正则的规则被跳过，"
                    f"样例：{', '.join(f'`{w[:36]}`' for w in wild[:4])}"
                )
            if stats["dropped"]:
                notes.append(
                    f"- `{kind}/{name}` 有 {stats['dropped']} 条无法解析被丢弃，"
                    f"样例：{', '.join(f'`{d[:36]}`' for d in dropped[:4])}"
                )
        return all_rules, self_domains

    log("=== 拉取黑名单源 ===")
    block_rules, self_block = collect("block")
    log(f"  黑名单合并去重后: {len(block_rules)} 条")

    log("=== 拉取白名单源 ===")
    allow_raw, _ = collect("allow")
    allow_domains: set[str] = set()
    for r in allow_raw:
        m = RULE_RE.match(r)
        if m:
            allow_domains.add(m.group(1))
    log(f"  白名单合并去重后: {len(allow_domains)} 条")

    # ---------- 策略 ----------
    removed_by_self: dict[str, list[str]] = {}
    if policy.get("self_block_wins", True) and self_block:
        for d in sorted(self_block):
            for v in sorted(allow_domains & ({d} | set(parents(d)))):
                removed_by_self.setdefault(v, []).append(d)
        allow_domains -= set(removed_by_self)
        log(f"  自建黑名单优先: 从 allow 剔除 {len(removed_by_self)} 条覆盖条目")

    max_labels = policy.get("strip_allow_max_labels")
    removed_short: set[str] = set()
    if isinstance(max_labels, int):
        removed_short = {d for d in allow_domains if labels(d) <= max_labels}
        allow_domains -= removed_short
        log(f"  剔除 <= {max_labels} 段整域放行: {len(removed_short)} 条")

    block_domains = {r[2:].rstrip("^").split("$")[0] for r in block_rules}
    conflict = sorted(block_domains & allow_domains)

    block_out = sorted(block_rules)
    prefix = out_cfg.get("allow_prefix", "@@")
    allow_out = sorted(f"{prefix}||{d}^" for d in allow_domains)

    # ---------- 报告 ----------
    report += ["", "## 各源贡献", "",
               "| 类型 | 源 | 原始行 | 有效 | 其中 hosts | 其中裸域名 | 去重后 | 通配符跳过 | 丢弃 |",
               "|---|---|---|---|---|---|---|---|---|"]
    for kind, name, s, uniq in rows:
        report.append(
            f"| {kind} | {name} | {s['lines']} | {s['ok']} | {s['hosts']} | {s['bare']} | "
            f"{uniq} | {s['wildcard']} | {s['dropped']} |"
        )

    report += ["", "## 结果", "",
               f"- 黑名单输出：**{len(block_out)}** 条",
               f"- 白名单输出：**{len(allow_out)}** 条（已统一 `{prefix}||domain^` 语法）",
               f"- 自建黑名单域名：**{len(self_block)}** 个",
               f"- 因自建黑名单优先而剔除的放行条目：**{len(removed_by_self)}** 条",
               f"- 同域既拦又放（保留放行侧）：**{len(conflict)}** 条"]
    if removed_short:
        report.append(f"- 因整域放行策略剔除：**{len(removed_short)}** 条")

    if notes:
        report += ["", "## 解析备注", ""] + notes

    if removed_by_self:
        report += ["", "## 被剔除的放行条目（因为覆盖了你的自建黑名单）", "",
                   "| 被剔除的放行 | 它覆盖的自建黑名单域名 |", "|---|---|"]
        for v in sorted(removed_by_self):
            report.append(f"| `{v}` | {', '.join(sorted(set(removed_by_self[v])))} |")

    short_n = policy.get("report_short_allow", 2)
    if isinstance(short_n, int) and short_n > 0:
        shorts = sorted(d for d in allow_domains if labels(d) <= short_n)
        report += ["", f"## 剩余整域放行（段数 <= {short_n}，建议人工复核）", ""]
        if shorts:
            report.append(f"共 {len(shorts)} 条：")
            report.append("")
            report += [f"- `{d}`" for d in shorts[:200]]
            if len(shorts) > 200:
                report.append(f"- …（还有 {len(shorts) - 200} 条）")
        else:
            report.append("无。")

    report += ["", "## 同域冲突", "",
               f"共 {len(conflict)} 条：这些域名在合并黑名单里要拦、在合并白名单里要放，"
               f"AGH 里例外优先，所以**实际不会拦**。",
               "",
               "想把其中某几个恢复拦截：把它们加进 `blacklist.txt`，"
               "下次跑流水线会自动剔除白名单侧对应条目。",
               f"完整清单见 `dist/conflicts.txt`。"]
    if conflict:
        report += [""] + [f"- `{d}`" for d in conflict[:150]]
        if len(conflict) > 150:
            report.append(f"- …（还有 {len(conflict) - 150} 条，见 conflicts.txt）")

    if args.dry_run:
        log("\n[dry-run] 不写文件。")
        log("\n".join(report[:60]))
        return 0

    out_block = ROOT / out_cfg.get("block", "dist/block-merged.txt")
    out_allow = ROOT / out_cfg.get("allow", "dist/allow-merged.txt")
    out_report = ROOT / out_cfg.get("report", "dist/report.md")
    out_conflict = out_report.parent / "conflicts.txt"
    for p in (out_block, out_allow, out_report, out_conflict):
        p.parent.mkdir(parents=True, exist_ok=True)

    stamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    def write_rules(path: Path, title: str, rules: list[str]) -> None:
        with path.open("w", encoding="utf-8", newline="\n") as f:
            f.write(f"! Title: {title}\n! Rules: {len(rules)}\n")
            f.write(f"! Generated: {stamp}\n")
            f.write("! Repo: https://github.com/50521136/ad-dns-rules\n!\n")
            for r in rules:
                f.write(r + "\n")

    write_rules(out_block, "ad-dns-rules 合并黑名单", block_out)
    write_rules(out_allow, "ad-dns-rules 合并白名单（@@ 例外，可订阅到普通过滤器槽位）", allow_out)
    out_report.write_text("\n".join(report) + "\n", encoding="utf-8")
    out_conflict.write_text("\n".join(conflict) + "\n", encoding="utf-8")

    log("")
    log("已写出:")
    log(f"  {out_block.relative_to(ROOT)}  {out_block.stat().st_size/1024/1024:.1f} MB  {len(block_out)} 条")
    log(f"  {out_allow.relative_to(ROOT)}  {out_allow.stat().st_size/1024:.1f} KB  {len(allow_out)} 条")
    log(f"  {out_report.relative_to(ROOT)}")
    log(f"  {out_conflict.relative_to(ROOT)}  {len(conflict)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
