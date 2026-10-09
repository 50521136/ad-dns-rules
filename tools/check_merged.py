#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""校验 dist/ 里的合并产物。CI 用它做门禁，退出码非 0 即失败。

检查项
------
1. 语法：每一行必须是 `||domain^` 或 `@@||domain^`（可选 $修饰符）
2. 归属：block 文件里不得出现 @@ 规则；allow 文件里必须全是 @@ 规则
3. 重复：同一文件内不得有重复条目
4. 自建规则必须生效：allow 产物里不得有任何条目（自身或父域）
   覆盖 blacklist.txt 里的域名 —— 这是整个流水线的核心保证
5. 自建白名单必须保留：whitelist.txt 的每条都要出现在 allow 产物里
6. 体积与条数报告

用法: python3 tools/check_merged.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RULE_RE = re.compile(r"^(@@)?\|\|([a-z0-9][a-z0-9._-]*)\^(\$[a-z0-9_,.=~-]+)?$")
DOMAIN_RE = re.compile(
    r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$"
)


def load(path: Path) -> tuple[set[str], set[str], list[str], set[str]]:
    """返回 (拦截域名, 放行域名, 错误列表, 全部规则原文)"""
    block: set[str] = set()
    allow: set[str] = set()
    errors: list[str] = []
    if not path.exists():
        errors.append(f"缺少产物文件: {path.relative_to(ROOT)}")
        return block, allow, errors, set()

    seen: set[str] = set()
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("!"):
            continue
        m = RULE_RE.match(line)
        if not m:
            errors.append(f"{path.name}:{lineno} 语法错误: {line[:60]}")
            continue
        dom = m.group(2)
        if not DOMAIN_RE.match(dom):
            errors.append(f"{path.name}:{lineno} 域名非法: {dom}")
            continue
        # 去重口径与 merge.py 一致：完整规则（含 $修饰符）算一条
        # ||x^ 和 ||x^$third-party 是两条不同规则，不视为重复
        if line in seen:
            errors.append(f"{path.name}:{lineno} 重复: {line[:60]}")
        seen.add(line)
        (allow if m.group(1) else block).add(dom)
    return block, allow, errors, seen


def parents(domain: str) -> set[str]:
    parts = domain.split(".")
    return {".".join(parts[i:]) for i in range(1, len(parts))}


def main() -> int:
    ok = True
    bl, bl_allow, bl_err, bl_lines = load(ROOT / "dist" / "block-merged.txt")
    al_plain, al_allow, al_err, al_lines = load(ROOT / "dist" / "allow-merged.txt")

    print(f"dist/block-merged.txt  拦截 {len(bl):7d} 条 | 内嵌放行 {len(bl_allow)} 条")
    print(f"dist/allow-merged.txt  放行 {len(al_allow):7d} 条 | 内嵌拦截 {len(al_plain)} 条")

    if bl_allow:
        ok = False
        print(f"  ! block 产物里不该有 @@ 规则，发现 {len(bl_allow)} 条")
    if al_plain:
        ok = False
        print(f"  ! allow 产物里不该有不带 @@ 的拦截规则，发现 {len(al_plain)} 条: "
              f"{sorted(al_plain)[:8]}")

    for name, errs in (("block-merged.txt", bl_err), ("allow-merged.txt", al_err)):
        if errs:
            ok = False
            print(f"\n[{name}] 问题 {len(errs)} 项，前 20 条:")
            for e in errs[:20]:
                print("  ", e)

    # ---- 核心保证 ----
    self_bl, _, self_bl_err, _ = load(ROOT / "blacklist.txt")
    if self_bl_err:
        ok = False
        print(f"\n[blacklist.txt] 解析失败: {self_bl_err[:3]}")
    self_wl_plain, self_wl, _, _ = load(ROOT / "whitelist.txt")

    covered: dict[str, list[str]] = {}
    for d in sorted(self_bl):
        hit = al_allow & ({d} | parents(d))
        if hit:
            covered[d] = sorted(hit)
    print(f"\n自建黑名单 {len(self_bl)} 条 —— 被 allow 产物覆盖的: {len(covered)} 个")
    if covered:
        ok = False
        print("  ! 以下自建黑名单规则会被合并白名单作废，必须修 merge.py 的策略：")
        for d, c in list(covered.items())[:30]:
            print(f"    {d:40s} 被 {c} 覆盖")
    else:
        print("  ✓ 全部生效")

    missing = self_wl - al_allow
    print(f"自建白名单 {len(self_wl)} 条 —— 在 allow 产物里缺失的: {len(missing)} 条")
    if missing:
        ok = False
        print(f"  ! 缺失: {sorted(missing)[:20]}")

    short = sorted(d for d in al_allow if d.count(".") == 1)
    print(f"\nallow 产物里两段整域放行: {len(short)} 条")
    for d in short[:20]:
        print(f"    {d}")
    if len(short) > 20:
        print(f"    …（还有 {len(short) - 20} 条，见 dist/report.md）")

    # 冗余的 $修饰符变体（同域已有无修饰版本时，非 $important 的变体是多余的）
    plain = {ln for ln in bl_lines if "$" not in ln}
    redundant = {ln for ln in bl_lines
                 if "$" in ln and "$important" not in ln and ln.split("$", 1)[0] in plain}
    print(f"\nblock 产物里冗余的 $修饰符变体: {len(redundant)} 条（同域已有无修饰版本，不影响功能）")

    print("\n" + ("通过 ✓" if ok else "存在问题 ✗"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
