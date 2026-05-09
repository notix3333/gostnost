# gostnost

`gostnost` helps create, edit, format, rewrite, and check Russian student practical, laboratory, and course reports according to GOST, the attached university guide, and a protected Word title page template.

## Installation

Place the `gostnost` folder into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R gostnost "${CODEX_HOME:-$HOME/.codex}/skills/gostnost"
```

Example request through `$skill-installer` after publishing the skill to a GitHub repository:

```text
Use $skill-installer to install https://github.com/<owner>/<repo>/tree/main/gostnost
```

Restart Codex after installation so the skill is discovered.

## Usage

Ask Codex to create, format, fill, rewrite, or check a student report. Mention GOST, the university guide, the title page, a practical work, laboratory work, or course work to trigger the skill.

Examples:

- `Оформи отчет по практической работе по ГОСТ и методичке.`
- `Проверь этот DOCX перед сдачей.`
- `Заполни титульный лист, не меняя его оформление.`
- `Перепиши вывод академическим стилем от лица студента.`

## Replaceable Files

You can replace these files for another university or department:

- `assets/title-page-template.docx` - protected title page template.
- `assets/report-template.docx` - body skeleton template.
- `references/university-report-guide.md` - university or department guide summary.
- `references/title-page-rules.md` - rules for the specific title page.
- `references/report-structure-rules.md` - report section requirements.

## Adding A New Title Page

Replace `assets/title-page-template.docx` with the new title page. Then update `references/title-page-rules.md` with the exact variable fields. Do not mark a field as fillable unless it is clearly intended for editing.

## Adding Report Examples

Add examples only after removing personal data. Store examples as local assets or references only if they directly improve report creation or checking. Do not add unnecessary samples.

## Running Checks

```bash
python3 scripts/check_report_structure.py path/to/report.docx
python3 scripts/check_images.py path/to/report.docx
python3 scripts/check_bibliography.py path/to/report.docx
python3 scripts/check_gost_requirements.py path/to/report.docx
```

The scripts use only Python standard library modules and support basic checks for `.docx`, `.md`, and `.txt` files.

## Limitations

- Scripts perform structural and textual checks, not full Word layout validation.
- Automated checks cannot prove that every screenshot is visually readable.
- DOCX crop detection is limited to detectable OOXML crop tags.
- Bibliography checks are basic and do not fully validate every GOST bibliographic field.
- The skill must ask questions when title-page fields or report requirements are ambiguous.

## Security And Personal Data

Before publishing or sharing this skill, remove student full names, groups, internal university data, teacher personal data, assignment variants, and any private information from example reports, screenshots, and templates. Keep only materials you are allowed to reuse.
