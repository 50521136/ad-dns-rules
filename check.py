#!/usr/bin/env python3
"""校验 blacklist.txt / whitelist.txt 的规则语法、重复与冲突。

用法: python3 check.py
退出码 0 = 通过，1 = 有问题（CI 用这个判断）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RULE_RE = re.compile(r"^(@@)?\|\|([a-z0-9][a-z0-9.-]*)\^(\$[a-z0-9_,.=~-]+)?$")
DOMAIN_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?(\.[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?)+$")


def load(path: Path):
    """返回 (拦截规则, 白名单规则, 错误列表, 注释掉的候选数)。"""
    block, allow, errors, commented = [], [], [], 0
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if line.startswith("!"):
            # 形如 !||domain^ 的是被注释掉的可选规则，统计一下
            if re.match(r"^!(@@)?\|\|", line):
                commented += 1
            continue
        m = RULE_RE.match(line)
        if not m:
            errors.append(f"{path.name}:{lineno} 语法错误: {line}")
            continue
        dom = m.group(2).lower()
        if not DOMAIN_RE.match(dom):
            errors.append(f"{path.name}:{lineno} 域名非法: {dom}")
            continue
        (allow if m.group(1) else block).append(dom)
    return block, allow, errors, commented


def dups(items):
    seen, out = set(), []
    for i in items:
        if i in seen and i not in out:
            out.append(i)
        seen.add(i)
    return out


def main() -> int:
    bl_path, wl_path = ROOT / "blacklist.txt", ROOT / "whitelist.txt"
    if not bl_path.exists() or not wl_path.exists():
        print("缺少 blacklist.txt 或 whitelist.txt")
        return 1

    bl, bl_allow, bl_err, bl_cmt = load(bl_path)
    wl_plain, wl_allow, wl_err, wl_cmt = load(wl_path)

    ok = True
    print(f"blacklist.txt  拦截 {len(bl):3d} 条 | 内嵌放行 {len(bl_allow):2d} 条 | 注释候选 {bl_cmt:2d} 条")
    print(f"whitelist.txt  放行 {len(wl_allow):3d} 条 | 注释候选 {wl_cmt:2d} 条")
    if wl_plain:
        ok = False
        print(f"  ! whitelist.txt 里出现了 {len(wl_plain)} 条不带 @@ 的拦截规则，白名单文件只应放 @@ 规则: {', '.join(wl_plain)}")

    for name, errs in (("blacklist.txt", bl_err), ("whitelist.txt", wl_err)):
        if errs:
            ok = False
            print(f"\n[{name}] 语法问题:")
            for e in errs:
                print("  ", e)

    for name, d in (("blacklist.txt", dups(bl)), ("whitelist.txt", dups(wl_allow))):
        if d:
            ok = False
            print(f"\n[{name}] 重复条目: {', '.join(d)}")

    allow_all = set(wl_allow) | set(bl_allow)
    conflict = sorted(set(bl) & allow_all)
    if conflict:
        ok = False
        print(f"\n拦截与白名单冲突（同一域名同时被拦又放行）: {', '.join(conflict)}")

    # 白名单父域会覆盖黑名单子域（例外规则优先级更高），这是必须拦下的错误
    bl_set = set(bl)
    for a in sorted(bl_set):
        for b in sorted(allow_all):
            if a.endswith("." + b):
                ok = False
                print(f"  ! 冲突: 黑名单 {a} 被白名单父域 {b} 覆盖，该广告域会失效")

    print("\n" + ("通过 ✓" if ok else "存在问题 ✗"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
