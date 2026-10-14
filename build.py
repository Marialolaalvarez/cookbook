"""Build recipes.js from the Markdown files in recipes/.

Run from this folder:  python3 build.py
Files starting with _ (like _TEMPLATE.md) are skipped.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "recipes"
OUT = ROOT / "recipes.js"

LIST_FIELDS = {"tags"}
NUMBER_FIELDS = {"time", "servings", "score"}


def parse_front_matter(text):
    if not text.startswith("---"):
        return {}, text
    _, fm, body = text.split("---", 2)
    meta = {}
    for line in fm.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        if key in LIST_FIELDS:
            meta[key] = [v.strip() for v in value.split(",") if v.strip()]
        elif key in NUMBER_FIELDS:
            try:
                meta[key] = float(value) if "." in value else int(value)
            except ValueError:
                meta[key] = None
        else:
            meta[key] = value
    return meta, body


def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*(.+?)\*", r"<em>\1</em>", s)
    s = re.sub(r"\[(.+?)\]\((https?://[^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    return s


def markdown_to_html(md):
    out, list_tag, para = [], None, []

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            para.clear()

    def close_list():
        nonlocal list_tag
        if list_tag:
            out.append(f"</{list_tag}>")
            list_tag = None

    for raw in md.splitlines():
        line = raw.strip()
        ul = re.match(r"^[-*] (.+)", line)
        ol = re.match(r"^\d+[.)] (.+)", line)
        if not line:
            flush_para(); close_list()
        elif line.startswith("#"):
            flush_para(); close_list()
            out.append("<h3>" + inline(line.lstrip("#").strip()) + "</h3>")
        elif ul or ol:
            flush_para()
            tag = "ul" if ul else "ol"
            if list_tag != tag:
                close_list(); out.append(f"<{tag}>"); list_tag = tag
            out.append("<li>" + inline((ul or ol).group(1)) + "</li>")
        else:
            close_list(); para.append(line)
    flush_para(); close_list()
    return "\n".join(out)


def main():
    recipes = []
    for path in sorted(SRC.glob("*.md")):
        if path.name.startswith("_"):
            continue
        meta, body = parse_front_matter(path.read_text(encoding="utf-8"))
        meta["id"] = path.stem
        meta.setdefault("title", path.stem.replace("-", " ").title())
        meta["html"] = markdown_to_html(body)
        recipes.append(meta)
    OUT.write_text("window.RECIPES = " + json.dumps(recipes, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
    print(f"Built {len(recipes)} recipes -> {OUT.name}")


if __name__ == "__main__":
    main()
