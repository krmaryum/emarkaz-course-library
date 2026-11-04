#!/usr/bin/env python3
"""Add Bukhari-style auto-open Collection Reader to all Hadith collections.

The existing generate_file_pages.py embeds a reader automatically when a
collection contains README.md. This helper only creates MISSING README files.
Existing READMEs and all PDFs are never modified.

Run at the emarkaz-course-library repository root:
    python setup_all_hadith_collection_readers.py --dry-run
    python setup_all_hadith_collection_readers.py
    python generate_file_pages.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path
from urllib.parse import quote

HADITH_REL = Path('emarkaz-books/e-courses/hadith')
NAMES = {
    'Sahih-Bukhari-Al-Bushra': 'صحیح البخاری — طبع البشری',
    'Sahih_Muslim': 'صحیح مسلم',
    'JAMI_AL_TIRMIZI_BUSHRA': 'جامع الترمذی — طبع البشری',
    'kitab ul Hadith': 'کتاب الحدیث',
}


def sortkey(value: str):
    return [int(x) if x.isdigit() else x.casefold() for x in re.split(r'(\d+)', value)]


def urlpath(path: Path) -> str:
    return '/'.join(quote(p, safe='') for p in path.parts)


def safe_cell(value: str) -> str:
    return value.replace('|', r'\|').replace('\n', ' ').strip()


def volume_label(folder: Path) -> str:
    m = re.search(r'(?:volume|vol)[ _-]*0*(\d+)', folder.name, re.I)
    return f'جلد {int(m.group(1)):02d}' if m else folder.name.replace('_', ' ')


def make_readme(collection: Path, pdfs: list[Path], folders: list[Path]) -> str:
    label = NAMES.get(collection.name, collection.name.replace('_', ' ').replace('-', ' '))
    lines = [
        f'# {label}', '',
        '## مجموعے کا تعارف', '',
        f'اس مجموعے میں **{len(pdfs)} PDF فائلیں** دستیاب ہیں۔ ذیل میں موجود جلدوں یا ذیلی فولڈرز اور PDF فائلوں کی فہرست دی گئی ہے۔',
        '',
        '> **اہم نوٹ:** فہرست موجودہ فائلوں کے ناموں اور فولڈر ساخت سے تیار کی گئی ہے۔ یہ اصل کتاب/باب کی نمبرنگ، صفحات یا اشاعتی تفصیلات کی آزادانہ تصدیق نہیں ہے۔',
        '', '## جلدوں اور فولڈرز کی فہرست', '',
    ]
    if folders:
        lines += ['| جلد / فولڈر | PDF فائلیں | کھولیں |', '| --- | ---: | --- |']
        for folder in folders:
            subtotal = sum(1 for p in pdfs if folder in p.parents)
            lines.append(f'| {safe_cell(volume_label(folder))} | {subtotal} | [فولڈر کھولیں]({urlpath(folder.relative_to(collection))}/) |')
    else:
        lines.append('اس مجموعے میں الگ جلدوں کے فولڈرز موجود نہیں ہیں۔')
    lines += ['', '## تمام دستیاب PDF فائلیں', '',
              '| نمبر | فائل / عنوان | PDF کھولیں |', '| ---: | --- | --- |']
    for n, pdf in enumerate(pdfs, start=1):
        title = safe_cell(pdf.stem.replace('_', ' ').replace('-', ' '))
        link = urlpath(pdf.relative_to(collection))
        lines.append(f'| {n} | {title} | [PDF]({link}) |')
    lines += ['', '## حدیث کی کتابیں تلاش کریں', '',
              '[تلاشِ کتب حدیث — تمام مجموعے](../hadith-search.html)', '',
              'یہ تلاش دستیاب PDF عنوانات اور فائل ناموں پر مبنی ہے؛ اسکین شدہ PDF صفحات کے اندر مکمل متن کی تلاش نہیں۔', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Show planned files, do not write anything')
    args = parser.parse_args()
    root = Path.cwd()
    hadith = root / HADITH_REL
    if not (root / 'generate_file_pages.py').is_file() or not hadith.is_dir():
        parser.error('Run from the emarkaz-course-library repository root.')
    collections = sorted((p for p in hadith.iterdir() if p.is_dir() and not p.name.startswith('.')),
                         key=lambda p: sortkey(p.name))
    created = skipped = empty = 0
    for collection in collections:
        pdfs = sorted((p for p in collection.rglob('*') if p.is_file() and p.suffix.lower() == '.pdf'),
                      key=lambda p: sortkey(p.relative_to(collection).as_posix()))
        readme = collection / 'README.md'
        if readme.exists():
            print(f'KEEP existing README: {readme.relative_to(root)}')
            skipped += 1
            continue
        if not pdfs:
            print(f'SKIP (no PDFs): {collection.relative_to(root)}')
            empty += 1
            continue
        folders = sorted((p for p in collection.iterdir() if p.is_dir() and not p.name.startswith('.')),
                         key=lambda p: sortkey(p.name))
        content = make_readme(collection, pdfs, folders)
        print(f'{"WOULD CREATE" if args.dry_run else "CREATED"}: {readme.relative_to(root)} ({len(pdfs)} PDFs)')
        if not args.dry_run:
            # Exclusive create: refuse overwrite even in a race.
            with readme.open('x', encoding='utf-8', newline='\n') as f:
                f.write(content)
        created += 1
    print(f'\nSummary: {created} new README(s), {skipped} existing preserved, {empty} without PDFs.')
    if not args.dry_run:
        print('NEXT: python generate_file_pages.py')
        print('Review: git status && git diff --stat')


if __name__ == '__main__':
    main()
