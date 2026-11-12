#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ATOOLHUB 工具自动发现脚本
==========================
扫描根目录下的每个子文件夹，自动探测：
  1. 入口 HTML（优先 index.html，其次与文件夹同名的 .html，再取第一个 .html）
  2. 页面 <title>（作为工具名）
  3. 图标（子文件夹下的 favicon.ico / *.png / *.svg，供设置面板展示）

生成 tools.json 工具清单，并把同一份清单注入 ATH.html 的内嵌兜底数据
（__EMBEDDED_TOOLS__ 占位符），保证 file:// 直接打开 ATH.html 也能工作。

对"作者手动配置"（排序 order、是否展示 hidden、名称/描述/类别/emoji 覆盖、手动添加的工具）：
  - 读取上一次生成的 tools.json（如存在），按 id 匹配后合并保留；
  - 若 tools.json 不存在，则尝试从 ATH.html 旧的内嵌清单中继承配置。

用法：
  python3 scan_tools.py            # 扫描并生成 tools.json、更新 ATH.html
  python3 scan_tools.py --dry-run  # 只打印将生成的清单，不写文件
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ATH_HTML = ROOT / "index.html"   # 入口页（原 ATH.html，已改名为 index.html）
TOOLS_JSON = ROOT / "tools.json"
META_JSON = ROOT / "meta.json"   # 作者维护的元数据（标签/emoji/介绍）
EMBED_MARKER = "__EMBEDDED_TOOLS__"

# 跳过这些目录/文件
SKIP_DIRS = {".git", ".workbuddy", "__pycache__", "node_modules", ".idea", ".vscode", "dist", "build"}
SKIP_HTML_NAMES = {"index.html"}  # 仅在候选阶段特殊处理，见 pick_entry

# 页面内的收款码 / 打赏二维码不属于工具图标，扫描时需排除
PAYMENT_IMAGE_KEYWORDS = (
    "alipay", "wechat", "weixin", "wxpay", "qrcode", "qr_code",
    "pay", "donate", "reward", "shoukuan", "收款", "打赏", "赞助",
)


def read_old_manifest() -> dict:
    """读取上一次的清单（tools.json 优先，其次 index.html 内嵌），返回 {id: tool} 便于合并配置。"""
    old = {}
    if TOOLS_JSON.exists():
        try:
            data = json.loads(TOOLS_JSON.read_text(encoding="utf-8"))
            for t in data if isinstance(data, list) else []:
                if isinstance(t, dict) and t.get("id"):
                    old[t["id"]] = t
        except Exception as e:
            print(f"[warn] tools.json 解析失败，忽略旧配置: {e}", file=sys.stderr)
        return old
    # 尝试从 index.html 内嵌清单继承
    if ATH_HTML.exists():
        m = re.search(r'id="%s">\s*(\[.*?\])\s*</script>' % EMBED_MARKER,
                      ATH_HTML.read_text(encoding="utf-8"), re.S)
        if m:
            try:
                data = json.loads(m.group(1))
                for t in data if isinstance(data, list) else []:
                    if isinstance(t, dict) and t.get("id"):
                        old[t["id"]] = t
            except Exception:
                pass
    return old


def read_meta() -> dict:
    """读取作者维护的 meta.json（工具标签/emoji/介绍），返回 {id: meta}。"""
    meta = {}
    if META_JSON.exists():
        try:
            data = json.loads(META_JSON.read_text(encoding="utf-8"))
            for tid, m in (data.items() if isinstance(data, dict) else []):
                if isinstance(m, dict):
                    meta[tid] = m
        except Exception as e:
            print(f"[warn] meta.json 解析失败: {e}", file=sys.stderr)
    return meta


def pick_entry(dir_path: Path) -> Path | None:
    """挑选入口 HTML：index.html > 与文件夹同名.html > 第一个 .html"""
    files = sorted(p for p in dir_path.iterdir() if p.is_file() and p.suffix.lower() == ".html")
    if not files:
        return None
    for f in files:
        if f.name.lower() == "index.html":
            return f
    for f in files:
        if f.stem.lower() == dir_path.name.lower():
            return f
    return files[0]


def extract_title(html_path: Path) -> str:
    """提取 <title> 文本；失败则用文件夹名。"""
    try:
        text = html_path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""
    m = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
    if m:
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        title = html.unescape(title)
        if title:
            return title
    return ""


def is_payment_image(name: str) -> bool:
    """判断是否为收款码 / 打赏二维码类图片（不适合作为工具图标）。"""
    low = name.lower()
    return any(k in low for k in PAYMENT_IMAGE_KEYWORDS)


def pick_icon(dir_path: Path) -> str:
    """挑选图标：favicon.ico > favicon.png > 任意 .png/.jpg/.jpeg/.svg
    跳过收款码/二维码类图片，避免把页面内的打赏图误当成工具图标。"""
    ico = dir_path / "favicon.ico"
    if ico.exists() and not is_payment_image(ico.name):
        return ico.name
    png = dir_path / "favicon.png"
    if png.exists() and not is_payment_image(png.name):
        return png.name
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.svg"):
        cands = sorted(p for p in dir_path.glob(ext) if not is_payment_image(p.name))
        if cands:
            return cands[0].name
    return ""


def scan() -> list[dict]:
    old = read_old_manifest()
    meta = read_meta()   # 作者维护的元数据（标签/emoji/介绍），优先级最高
    tools = []
    used_ids = set()
    for child in sorted(ROOT.iterdir()):
        if not child.is_dir() or child.name.startswith(".") or child.name in SKIP_DIRS:
            continue
        entry = pick_entry(child)
        if entry is None:
            print(f"[skip] {child.name}/ 未找到 HTML 入口", file=sys.stderr)
            continue

        tool_id = child.name
        used_ids.add(tool_id)
        name = extract_title(entry)
        icon = pick_icon(child)
        prev = old.get(tool_id, {})
        m = meta.get(tool_id, {})
        url = f"./{child.name}/{entry.name}"

        tool = {
            "id": tool_id,
            # 名称：meta.json > 旧清单 > <title> > 文件夹名
            "name": m.get("name") or prev.get("name") or name or child.name,
            "url": prev.get("url") or url,
            # 标签/emoji/介绍：meta.json 为唯一来源（作者后台统一维护），旧清单不再作为来源
            "category": m.get("category", ""),
            "desc": m.get("desc", ""),
            "emoji": m.get("emoji", ""),
            "entry": f"./{child.name}/{entry.name}",
            "icon": icon,
            # 排序/隐藏：保留上一次的设置，首次出现时给默认值
            "order": prev.get("order", len(tools)),
            "hidden": prev.get("hidden", False),
        }
        tools.append(tool)
        print(f"[found] {tool_id} -> {entry.name} | {name}")

    # 继承旧清单中已不存在于磁盘的工具（例如手动添加、或临时移走的文件夹），避免配置丢失
    for tid, prev in old.items():
        if tid not in used_ids:
            prev.setdefault("order", len(tools))
            prev.setdefault("hidden", False)
            tools.append(prev)
            print(f"[keep]  {tid} (磁盘上不存在，保留配置)", file=sys.stderr)

    tools.sort(key=lambda t: (t.get("order", 0), t["id"]))
    for i, t in enumerate(tools):
        t["order"] = i
    return tools


def inject_embedded(tools: list[dict]) -> None:
    """把清单注入 index.html 内嵌兜底数据。"""
    if not ATH_HTML.exists():
        print("[error] index.html 不存在", file=sys.stderr)
        sys.exit(1)
    text = ATH_HTML.read_text(encoding="utf-8")
    json_str = json.dumps(tools, ensure_ascii=False, indent=2)
    # 替换为 <script id="__EMBEDDED_TOOLS__" type="application/json">...</script>
    new_block = f'<script id="{EMBED_MARKER}" type="application/json">\n{json_str}\n</script>'
    pattern = re.compile(
        r'<script id="%s" type="application/json">.*?</script>' % EMBED_MARKER,
        re.S,
    )
    if pattern.search(text):
        text = pattern.sub(lambda _: new_block, text, count=1)
    else:
        print(f"[error] index.html 中未找到 {EMBED_MARKER} 占位符，请先添加", file=sys.stderr)
        sys.exit(1)
    ATH_HTML.write_text(text, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="ATOOLHUB 工具自动发现")
    parser.add_argument("--dry-run", action="store_true", help="只打印结果，不写文件")
    args = parser.parse_args()

    tools = scan()
    print(f"\n共发现 {len(tools)} 个工具。")

    if args.dry_run:
        print(json.dumps(tools, ensure_ascii=False, indent=2))
        return

    TOOLS_JSON.write_text(
        json.dumps(tools, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    inject_embedded(tools)
    print(f"已写入 {TOOLS_JSON.name}，并更新 {ATH_HTML.name} 内嵌清单。")


if __name__ == "__main__":
    main()