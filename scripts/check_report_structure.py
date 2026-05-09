#!/usr/bin/env python3
"""Check a Russian student report for basic required sections."""

from __future__ import annotations

import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


PLACEHOLDER_RE = re.compile(r"\[[А-ЯЁA-Z0-9 _-]+\]")


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


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE | re.MULTILINE) is not None


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: check_report_structure.py path/to/report.docx|md|txt")
        return 2

    path = Path(argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}")
        return 2

    text = read_text(path)
    checks = [
        ("title_page_hint", r"(министерство|университет|кафедра|выполнил|проверил)"),
        ("content", r"\bСОДЕРЖАНИЕ\b"),
        ("goal", r"(целью работы является|цель работы|целью данной работы)"),
        ("tasks", r"(задач[аи]|были решены следующие задачи)"),
        ("conclusion", r"\bЗАКЛЮЧЕНИЕ\b|таким образом|в результате выполнения работы"),
        ("bibliography", r"СПИСОК (ИСПОЛЬЗОВАННЫХ|ИСПОЛЬЗУЕМЫХ) ИСТОЧНИКОВ|ЛИТЕРАТУР"),
    ]

    warnings = []
    for name, pattern in checks:
        if not has(pattern, text):
            warnings.append(f"Missing or not detected: {name}")

    placeholders = sorted(set(PLACEHOLDER_RE.findall(text)))
    if placeholders:
        warnings.append("Unresolved placeholders: " + ", ".join(placeholders))

    if warnings:
        print("STRUCTURE CHECK: WARNINGS")
        for warning in warnings:
            print(f"- {warning}")
        return 1

    print("STRUCTURE CHECK: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
