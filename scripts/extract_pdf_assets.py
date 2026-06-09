#!/usr/bin/env python3
"""Render PDF pages to PNG assets for lecture teaching notes.

The script prefers PyMuPDF (`fitz`) and writes page images to:
outputs/<lecture_name>/assets/
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "lecture"


def parse_pages(page_spec: str | None, page_count: int) -> list[int]:
    if not page_spec:
        return list(range(page_count))

    pages: set[int] = set()
    for part in page_spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start_text, end_text = part.split("-", 1)
            start = int(start_text)
            end = int(end_text)
            if start > end:
                start, end = end, start
            pages.update(range(start - 1, end))
        else:
            pages.add(int(part) - 1)

    return [p for p in sorted(pages) if 0 <= p < page_count]


def render_pdf(pdf_path: Path, output_root: Path, lecture_name: str | None, dpi: int, pages: str | None) -> Path:
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit(
            "PyMuPDF is required to render PDF assets. Install it with: pip install pymupdf"
        ) from exc

    pdf_path = pdf_path.resolve()
    if not pdf_path.exists():
        raise SystemExit(f"PDF not found: {pdf_path}")

    lecture_slug = slugify(lecture_name or pdf_path.stem)
    asset_dir = output_root / lecture_slug / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)

    doc = fitz.open(pdf_path)
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    selected_pages = parse_pages(pages, doc.page_count)

    for page_index in selected_pages:
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        image_path = asset_dir / f"page_{page_index + 1:03d}.png"
        pix.save(image_path)

    manifest = asset_dir / "manifest.txt"
    manifest.write_text(
        "\n".join(f"page_{page_index + 1:03d}.png" for page_index in selected_pages) + "\n",
        encoding="utf-8",
    )
    return asset_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Render lecture slide PDF pages into PNG assets.")
    parser.add_argument("pdf", type=Path, help="Path to the lecture slides PDF.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("outputs"),
        help="Root output directory. Default: outputs",
    )
    parser.add_argument(
        "--lecture-name",
        default=None,
        help="Lecture output folder name. Defaults to the PDF filename stem.",
    )
    parser.add_argument("--dpi", type=int, default=180, help="Render DPI. Default: 180")
    parser.add_argument(
        "--pages",
        default=None,
        help="1-based page selection such as '1,3,5-8'. Default: all pages.",
    )
    args = parser.parse_args()

    asset_dir = render_pdf(args.pdf, args.output_root, args.lecture_name, args.dpi, args.pages)
    print(asset_dir)


if __name__ == "__main__":
    main()

