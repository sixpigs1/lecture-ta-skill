#!/usr/bin/env python3
"""Build standalone Chinese HTML lecture notes from structured content.

Usage:
python scripts/build_html.py note.json --template templates/lecture_note_template.html --output outputs/lecture03/index.html

Formula text is rendered as MathJax LaTeX. Pass formulas either with explicit
delimiters (`\\(...\\)` or `\\[...\\]`) or as raw LaTeX; raw formula strings are
wrapped in display math automatically.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_TEMPLATE = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{{ title }}</title>
  <script>
    window.MathJax = {
      tex: {
        inlineMath: [['\\\\(', '\\\\)']],
        displayMath: [['\\\\[', '\\\\]']],
        processEscapes: true,
        processEnvironments: true
      },
      options: {
        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
      }
    };
  </script>
  <script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; line-height: 1.68; color: #1f2933; }
    .layout { display: grid; grid-template-columns: 240px minmax(0, 1fr); gap: 32px; max-width: 1180px; margin: 0 auto; padding: 32px 24px; }
    .toc { position: sticky; top: 24px; align-self: start; border-right: 1px solid #d9e2ec; padding-right: 18px; }
    main { max-width: 900px; }
    h1, h2, h3 { color: #102a43; line-height: 1.25; }
    h2 { border-bottom: 1px solid #d9e2ec; padding-bottom: 8px; margin-top: 36px; }
    img { max-width: 100%; border: 1px solid #d9e2ec; border-radius: 8px; }
    figcaption { color: #5f6b7a; font-size: 0.92rem; }
    .formula, pre { overflow-x: auto; background: #f3f6f9; border-radius: 8px; padding: 14px 16px; }
    .formula { border-left: 4px solid #1d4ed8; white-space: normal; }
    .knowledge-map, .takeaway, .proof { background: #f8fafc; border: 1px solid #d9e2ec; border-radius: 8px; padding: 16px 18px; }
    .terms { border-collapse: collapse; width: 100%; margin: 16px 0; }
    .terms th, .terms td { border: 1px solid #d9e2ec; padding: 8px 10px; text-align: left; vertical-align: top; }
    .terms th { background: #f8fafc; }
    @media (max-width: 820px) { .layout { display: block; padding: 20px 16px; } .toc { position: static; border: 1px solid #d9e2ec; border-radius: 8px; margin-bottom: 24px; padding: 12px 14px; } }
  </style>
</head>
<body>
  <div class="layout">
    <nav class="toc"><strong>目录</strong><ol>{{ toc }}</ol></nav>
    <main><header><h1>{{ title }}</h1><p>{{ subtitle }}</p></header>{{ content }}</main>
  </div>
</body>
</html>
"""


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "section"


def html_escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def paragraphize(text: str) -> str:
    paragraphs = [p.strip() for p in str(text).split("\n\n") if p.strip()]
    return "\n".join(f"<p>{html_escape(p)}</p>" for p in paragraphs)


def ensure_math_delimiters(value: Any, display: bool = True) -> str:
    text = str(value).strip()
    if not text:
        return ""
    if text.startswith(("\\[", "\\(", "$$")):
        return text
    if display:
        return "\\[\n" + text + "\n\\]"
    return "\\(" + text + "\\)"


def render_formula(value: Any, display: bool = True) -> str:
    formula = ensure_math_delimiters(value, display=display)
    return f'<div class="formula">{html_escape(formula)}</div>'


def render_image(image: dict[str, Any]) -> str:
    src = html_escape(image.get("src", ""))
    alt = html_escape(image.get("alt", "课程图示"))
    caption = html_escape(image.get("caption", ""))
    caption_html = f"<figcaption>{caption}</figcaption>" if caption else ""
    return f'<figure><img src="{src}" alt="{alt}">{caption_html}</figure>'


def render_terms(terms: list[dict[str, Any]]) -> str:
    if not terms:
        return ""
    rows = [
        f"<tr><td><strong>{html_escape(item.get('term', ''))}</strong></td><td>{html_escape(item.get('explanation', ''))}</td></tr>"
        for item in terms
    ]
    return '<table class="terms"><thead><tr><th>概念 / Term</th><th>解释</th></tr></thead><tbody>' + "\n".join(rows) + "</tbody></table>"


def render_proof(proof: dict[str, Any]) -> str:
    title = html_escape(proof.get("title", "理论证明 / 推导"))
    text = proof.get("text", "")
    content = str(text) if str(text).lstrip().startswith("<") else paragraphize(str(text))
    return f'<div class="proof"><h3>{title}</h3>{content}</div>'


def render_block(block: dict[str, Any]) -> str:
    block_type = str(block.get("type", "paragraph"))
    if block_type == "paragraph":
        return paragraphize(str(block.get("text", "")))
    if block_type == "html":
        return str(block.get("html", ""))
    if block_type == "image":
        return render_image(block)
    if block_type == "formula":
        return render_formula(block.get("text", ""), display=bool(block.get("display", True)))
    if block_type == "code":
        return f"<pre><code>{html_escape(block.get('text', ''))}</code></pre>"
    if block_type == "terms":
        return render_terms(block.get("items", []))
    if block_type == "proof":
        return render_proof(block)
    return paragraphize(str(block.get("text", "")))


def render_section(section: dict[str, Any]) -> str:
    title = str(section.get("title", "Untitled Section"))
    section_id = str(section.get("id") or slugify(title))
    kind = str(section.get("kind", "normal"))
    classes = "section"
    if kind == "knowledge-map":
        classes += " knowledge-map"
    if kind == "takeaway":
        classes += " takeaway"

    pieces: list[str] = [f'<section id="{html_escape(section_id)}" class="{classes}">', f"<h2>{html_escape(title)}</h2>"]

    content = section.get("content", "")
    if content:
        if isinstance(content, list):
            pieces.extend(f"<p>{html_escape(item)}</p>" for item in content)
        elif str(content).lstrip().startswith("<"):
            pieces.append(str(content))
        else:
            pieces.append(paragraphize(str(content)))

    pieces.append(render_terms(section.get("terms", [])))

    for block in section.get("blocks", []):
        pieces.append(render_block(block))

    for formula in section.get("formulas", []):
        pieces.append(render_formula(formula))

    for proof in section.get("proofs", []):
        pieces.append(render_proof(proof))

    for image in section.get("images", []):
        pieces.append(render_image(image))

    pieces.append("</section>")
    return "\n".join(piece for piece in pieces if piece)


def build_html(note: dict[str, Any], template_text: str) -> str:
    title = str(note.get("title", "课程学习笔记"))
    subtitle = str(note.get("subtitle", "基于课程 slides 生成的中文助教式学习笔记。"))
    sections = note.get("sections", [])

    toc_items = []
    rendered_sections = []
    for section in sections:
        section_title = str(section.get("title", "Untitled Section"))
        section_id = str(section.get("id") or slugify(section_title))
        section["id"] = section_id
        toc_items.append(f'<li><a href="#{html_escape(section_id)}">{html_escape(section_title)}</a></li>')
        rendered_sections.append(render_section(section))

    return (
        template_text.replace("{{ title }}", html_escape(title))
        .replace("{{ subtitle }}", html_escape(subtitle))
        .replace("{{ toc }}", "\n".join(toc_items))
        .replace("{{ content }}", "\n".join(rendered_sections))
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Build an HTML lecture teaching note from JSON data.")
    parser.add_argument("input_json", type=Path, help="JSON file describing the lecture note.")
    parser.add_argument("--template", type=Path, default=None, help="HTML template path.")
    parser.add_argument("--output", type=Path, required=True, help="Output HTML path, usually outputs/<lecture>/index.html.")
    args = parser.parse_args()

    note = json.loads(args.input_json.read_text(encoding="utf-8"))
    template_text = args.template.read_text(encoding="utf-8") if args.template else DEFAULT_TEMPLATE
    html_text = build_html(note, template_text)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_text, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
