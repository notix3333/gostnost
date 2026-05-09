#!/usr/bin/env python3
"""Combined lightweight GOST/university-guide check for student reports."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PLACEHOLDER_RE = re.compile(r"\[[А-ЯЁA-Z0-9 _-]+\]")
FIGURE_CAPTION_RE = re.compile(r"Рисунок\s+([А-ЯA-Z]?\d+)\s+[–-]\s+\S", re.IGNORECASE)
FIGURE_MENTION_RE = re.compile(r"Рисунк[аеуом]\s+([А-ЯA-Z]?\d+)", re.IGNORECASE)
TABLE_TITLE_RE = re.compile(r"Таблица\s+([А-ЯA-Z]?\d+)\s+[–-]\s+\S", re.IGNORECASE)
TABLE_MENTION_RE = re.compile(r"Таблиц[аеуы]\s+([А-ЯA-Z]?\d+)", re.IGNORECASE)
BIB_SECTION_RE = re.compile(
    r"СПИСОК\s+(ИСПОЛЬЗОВАННЫХ|ИСПОЛЬЗУЕМЫХ)\s+ИСТОЧНИКОВ|СПИСОК\s+ЛИТЕРАТУРЫ",
    re.IGNORECASE,
)
SOURCE_ENTRY_RE = re.compile(r"^\s*(\[\d+\]|\d+[\).])\s+\S", re.MULTILINE)
CITATION_RE = re.compile(r"\[(\d+)\]")


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
    return "\n".join(paragraphs), media_count, b"srcRect" in xml


def read_text(path: Path) -> tuple[str, int, bool]:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    return path.read_text(encoding="utf-8", errors="ignore"), 0, False


def found(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE | re.MULTILINE) is not None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: check_gost_requirements.py path/to/report.docx|md|txt")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text, media_count, has_crop_tag = read_text(path)
    issues: list[tuple[str, str]] = []

    required = [
        ("critical", "Title page hint not detected", r"(министерство|университет|кафедра|выполнил|проверил)"),
        ("format", "`СОДЕРЖАНИЕ` not detected", r"\bСОДЕРЖАНИЕ\b"),
        ("critical", "Goal of work not detected", r"(целью работы является|цель работы|целью данной работы)"),
        ("critical", "Conclusion not detected", r"\bЗАКЛЮЧЕНИЕ\b|таким образом|в результате выполнения работы"),
    ]
    for category, message, pattern in required:
        if not found(pattern, text):
            issues.append((category, message))

    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        issues.append(("clarify", "Unresolved placeholders: " + ", ".join(placeholders)))

    figure_captions = FIGURE_CAPTION_RE.findall(text)
    figure_mentions = FIGURE_MENTION_RE.findall(text)
    if media_count and not figure_captions:
        issues.append(("format", f"{media_count} embedded image(s) detected, but no figure captions found"))
    for number in sorted(set(figure_captions)):
        if number not in set(figure_mentions) or figure_mentions.count(number) < 2:
            issues.append(("format", f"Figure {number} may lack a separate text reference"))
    if has_crop_tag:
        issues.append(("critical", "DOCX crop tag detected; verify screenshots are not cropped"))

    table_titles = TABLE_TITLE_RE.findall(text)
    table_mentions = TABLE_MENTION_RE.findall(text)
    for number in sorted(set(table_titles)):
        if number not in set(table_mentions) or table_mentions.count(number) < 2:
            issues.append(("format", f"Table {number} may lack a separate text reference"))

    has_bib = BIB_SECTION_RE.search(text) is not None
    source_entries = SOURCE_ENTRY_RE.findall(text)
    citations = CITATION_RE.findall(text)
    if has_bib and not source_entries:
        issues.append(("gost", "Bibliography section exists, but numbered source entries were not detected"))
    if source_entries and not citations:
        issues.append(("gost", "Numbered sources exist, but in-text square-bracket citations were not detected"))

    if re.search(r"\b(я думаю|мне кажется|в общем|короче|получилось нормально)\b", text, re.IGNORECASE):
        issues.append(("style", "Conversational phrasing detected"))

    print("COMBINED GOST/GUIDE CHECK")
    print(f"- Embedded images: {media_count}")
    print(f"- Figure captions: {len(figure_captions)}")
    print(f"- Table titles: {len(table_titles)}")
    print(f"- Source-like entries: {len(source_entries)}")
    print(f"- In-text citations: {len(citations)}")

    if not issues:
        print("- OK")
        print("Readiness score: 100")
        return 0

    by_category: dict[str, list[str]] = {}
    for category, message in issues:
        by_category.setdefault(category, []).append(message)
    for category in ["critical", "format", "gost", "style", "clarify"]:
        messages = by_category.get(category, [])
        if messages:
            print(f"{category.upper()}:")
            for message in messages:
                print(f"- {message}")

    score = max(0, 100 - 15 * len(by_category.get("critical", [])) - 8 * len(issues))
    print(f"Readiness score: {score}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
