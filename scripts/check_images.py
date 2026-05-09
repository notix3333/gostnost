#!/usr/bin/env python3
"""Check figure and screenshot mentions in a Russian student report."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


FIGURE_CAPTION_RE = re.compile(r"Рисунок\s+([А-ЯA-Z]?\d+)\s+[–-]\s+\S", re.IGNORECASE)
FIGURE_MENTION_RE = re.compile(r"Рисунк[аеуом]\s+([А-ЯA-Z]?\d+)", re.IGNORECASE)


def read_docx(path: Path) -> tuple[str, int, bool]:
    with zipfile.ZipFile(path) as docx:
        names = docx.namelist()
        xml = docx.read("word/document.xml")
        media_count = sum(1 for name in names if name.startswith("word/media/"))
    root = ET.fromstring(xml)
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    paragraphs = []
    for p in root.findall(".//w:p", ns):
        text = "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()
        if text:
            paragraphs.append(text)
    has_crop_tag = b"srcRect" in xml
    return "\n".join(paragraphs), media_count, has_crop_tag


def read_text(path: Path) -> tuple[str, int, bool]:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore"), 0, False


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: check_images.py path/to/report.docx|md|txt")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text, media_count, has_crop_tag = read_text(path)
    captions = FIGURE_CAPTION_RE.findall(text)
    mentions = FIGURE_MENTION_RE.findall(text)
    caption_set = set(captions)
    mention_set = set(mentions)

    warnings = []
    if media_count and not captions:
        warnings.append(f"Detected {media_count} embedded image(s), but no figure captions were found.")
    if captions and not mentions:
        warnings.append("Figure captions exist, but text references to figures were not detected.")
    for number in sorted(caption_set):
        if number not in mention_set or mentions.count(number) < 2:
            warnings.append(f"Figure {number} may lack a separate text reference before/near the caption.")
    if re.search(r"скриншот|снимок экрана", text, re.IGNORECASE) and not captions:
        warnings.append("Screenshot is mentioned, but a figure caption was not detected.")
    if has_crop_tag:
        warnings.append("DOCX crop tag detected. Verify that screenshots are not cropped.")

    print("IMAGE CHECK")
    print("- Screenshots must not be cropped, stretched, or edited with loss of content.")
    print("- Preserve original proportions and readability; move large screenshots to a new page or appendix.")
    if media_count:
        print(f"- Embedded images detected: {media_count}")
    print(f"- Figure captions detected: {len(captions)}")

    if warnings:
        for warning in warnings:
            print(f"- WARNING: {warning}")
        return 1

    print("- OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
