#!/usr/bin/env python3
"""Check bibliography section and basic source numbering."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


SECTION_RE = re.compile(
    r"СПИСОК\s+(ИСПОЛЬЗОВАННЫХ|ИСПОЛЬЗУЕМЫХ)\s+ИСТОЧНИКОВ|СПИСОК\s+ЛИТЕРАТУРЫ",
    re.IGNORECASE,
)
SOURCE_ENTRY_RE = re.compile(r"^\s*(\[\d+\]|\d+[\).])\s+\S", re.MULTILINE)
CITATION_RE = re.compile(r"\[(\d+)\]")


def read_text(path: Path) -> str:
    if path.suffix.lower() == ".docx":
        with zipfile.ZipFile(path) as docx:
            xml = docx.read("word/document.xml")
        root = ET.fromstring(xml)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs = []
        for p in root.findall(".//w:p", ns):
            text = "".join(t.text or "" for t in p.findall(".//w:t", ns)).strip()
            if text:
                paragraphs.append(text)
        return "\n".join(paragraphs)
    return path.read_text(encoding="utf-8", errors="ignore")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: check_bibliography.py path/to/report.docx|md|txt")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text = read_text(path)
    warnings = []

    if not SECTION_RE.search(text):
        warnings.append("Bibliography section was not detected.")

    entries = SOURCE_ENTRY_RE.findall(text)
    citations = CITATION_RE.findall(text)
    if SECTION_RE.search(text) and not entries:
        warnings.append("Bibliography section exists, but numbered source entries were not detected.")
    if entries and not citations:
        warnings.append("Numbered sources exist, but in-text square-bracket citations were not detected.")

    print("BIBLIOGRAPHY CHECK")
    print(f"- Numbered source-like entries detected: {len(entries)}")
    print(f"- In-text square-bracket citations detected: {len(citations)}")

    if warnings:
        for warning in warnings:
            print(f"- WARNING: {warning}")
        return 1

    print("- OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
