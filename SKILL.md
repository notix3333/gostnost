---
name: gostnost
description: Use this skill to create, format, rewrite, and check Russian student reports according to GOST, university guidelines, and a fixed Word title page template.
---

# Gostnost

Use this skill for Russian student practical, laboratory, and course reports when the user asks to create, edit, format, rewrite, or check a report according to GOST, a university or department guide, and a fixed Word title page template.

## Use Cases

- Create a laboratory work report.
- Create a practical work report.
- Create a course work report.
- Format a report according to GOST and the attached university guide.
- Check a report before submission.
- Fill a report according to the attached guide.
- Fill the title page without changing its structure or visual formatting.
- Format figures, screenshots, tables, formulas, appendices, and bibliography.
- Rewrite text in formal academic Russian from the student's perspective.

## Source Priority

Apply requirements in this order:

1. Direct user requirements.
2. Teacher requirements.
3. Attached university or department guide.
4. Fixed title page template.
5. GOST as the baseline formatting standard.
6. General academic writing rules.

If GOST and the guide conflict, explicitly report the conflict. Prefer teacher, department, or guide requirements unless the user asks otherwise.

## Required References

- Read `references/university-report-guide.md` before creating or checking a report.
- Read `references/title-page-rules.md` before filling or discussing the title page.
- Read `references/report-structure-rules.md` before creating the report structure.
- Use `references/formatting-checklist.md` for final checks.
- Use `references/common-mistakes.md` when reporting issues.
- Use `assets/placeholders.md` when data is missing.
- Use `assets/title-page-template.docx` as the protected title page template.
- Use `assets/report-template.docx` only as a body skeleton; do not treat it as a replacement for the protected title page.

## Title Page Rule

The title page is a protected template. Do not structurally or visually change it. Do not redraw, rewrite, reformat, or improve it. Fill only clearly variable fields, such as student full name, group, discipline, topic, teacher, city, year, variant, dates, and other explicitly fillable fields. If a variable field is not obvious, ask the user before editing.

## Screenshot Rule

Do not crop screenshots. Do not change screenshot proportions, remove content, or alter the screenshot in a way that loses information. Insert screenshots fully, preserving proportions, readability, caption, and a text reference. If a screenshot is too large, scale it proportionally, move it to the next page, or propose placing it in an appendix.

## Internet Rule

Do not download GOST texts, images, libraries, templates, examples, or external materials from the internet unless the user directly asks for it. Work with the user's attached files and local skill materials.

## Questions Rule

Ask clarifying questions when data is missing or ambiguous. This is mandatory when any of the following is unknown and needed for the task: work type, topic, discipline, university, department, student full name, group, teacher, variant, required volume, report structure, source data, whether a bibliography is required, whether screenshots must be inserted, and final file format.

Do not invent missing data. Use square-bracket placeholders instead.

## Creating A Report

1. Determine the work type: practical, laboratory, course work, or another student report.
2. Read the university guide and relevant reference files.
3. Use GOST as the baseline standard.
4. Use the title page as an immutable template.
5. Collect missing data or insert placeholders.
6. Create the report structure according to the guide and the assignment.
7. Write in formal academic Russian from the student's perspective.
8. Format figures, screenshots, tables, formulas, appendices, and sources.
9. Check the report against `references/formatting-checklist.md`.
10. Return the final file, corrected text, or a precise list of required fixes.

## Checking A Report

Check:

- Required sections.
- Compliance with the guide structure.
- Title page formatting and protected-template handling.
- Academic student voice.
- Section numbering.
- Figure and screenshot formatting.
- Table formatting.
- Formula formatting.
- References to figures and tables in text.
- Bibliography and in-text source references.
- Match between goal and conclusion.
- Absence of conversational style.
- Absence of invented data.
- Absence of cropped screenshots.

For automated checks, run scripts from `scripts/`:

```bash
python3 scripts/check_report_structure.py path/to/report.docx
python3 scripts/check_images.py path/to/report.docx
python3 scripts/check_bibliography.py path/to/report.docx
python3 scripts/check_gost_requirements.py path/to/report.docx
```

## Review Output Format

Return review results in this structure:

1. Critical errors.
2. Formatting errors.
3. GOST or guide errors.
4. Style notes.
5. Questions for the user.
6. Corrected fragments.
7. Final readiness score from 0 to 100.

## Writing Style

Use formal academic Russian. Write from the perspective of the student who completed the practical, laboratory, or course work. Avoid conversational phrasing, excessive complexity, invented results, and the phrase "мы считаем" unless the guide requires it.

Prefer formulations such as:

- "Целью работы является..."
- "В ходе выполнения работы были решены следующие задачи..."
- "В практической части выполнено..."
- "В результате выполнения работы получены..."
- "Таким образом, поставленная цель была достигнута..."

## Placeholders

Use these placeholders when data is missing:

- `[ФИО СТУДЕНТА]`
- `[ГРУППА]`
- `[ДИСЦИПЛИНА]`
- `[ТЕМА РАБОТЫ]`
- `[ТИП РАБОТЫ]`
- `[ФИО ПРЕПОДАВАТЕЛЯ]`
- `[КАФЕДРА]`
- `[ВУЗ]`
- `[ГОРОД]`
- `[ГОД]`
- `[ВАРИАНТ]`
- `[ДОБАВИТЬ СКРИНШОТ]`
- `[ДОБАВИТЬ РАСЧЕТЫ]`
- `[ДОБАВИТЬ ВЫВОД]`

## Prohibitions

Do not:

- Change the title page without permission.
- Change title page visual formatting.
- Crop screenshots.
- Download unnecessary files.
- Install unnecessary dependencies.
- Invent missing data.
- Ignore the guide.
- Ignore GOST.
- Delete report sections without explanation.
- Shorten the report unless the user asks.
- Write from the teacher's, organization's, or abstract author's perspective.
- Leave a checked report without a checklist-based result.
