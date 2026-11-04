#!/usr/bin/env python3
"""Safely register Jami al-Tirmidhi Al-Bushra in eMarkaz Hadith Library.

Run from the root of a checked-out emarkaz-course-library repository.
No PDFs are opened, changed, copied or deleted.
"""
from pathlib import Path
from urllib.parse import quote
import re

ROOT = Path.cwd()
HADITH = ROOT / 'emarkaz-books' / 'e-courses' / 'hadith'
COLLECTION = HADITH / 'JAMI_AL_TIRMIZI_BUSHRA'
BUILDER = ROOT / 'build_hadith_search.py'
README = COLLECTION / 'README.md'
KEY = "'JAMI_AL_TIRMIZI_BUSHRA': {'ur': 'جامع الترمذی — طبع البشری', 'en': 'Jami al-Tirmidhi Al-Bushra'},"

def natural(text):
    return [int(n) if n.isdigit() else n.casefold() for n in re.split(r'(\d+)', text)]

def encode_relative(p):
    return '/'.join(quote(part, safe='') for part in p.parts)

def main():
    if not COLLECTION.is_dir() or not BUILDER.is_file():
        raise SystemExit('ERROR: Run from emarkaz-course-library root with build_hadith_search.py and JAMI_AL_TIRMIZI_BUSHRA folder present.')
    folders = sorted((p for p in COLLECTION.iterdir() if p.is_dir() and not p.name.startswith('.')), key=lambda p: natural(p.name))
    pdfs = sorted(COLLECTION.rglob('*.pdf'), key=lambda p: natural(p.relative_to(COLLECTION).as_posix()))
    nums = set()
    for folder in folders:
        m = re.search(r'(?:Volume|Vol)[_-]*0*(\d+)', folder.name, re.I)
        if m:
            nums.add(int(m.group(1)))
    print('Found volume folders:', len(folders), '| Volume numbers:', sorted(nums), '| PDFs:', len(pdfs))
    if nums != {1,2,3,4,5} or len(pdfs) == 0:
        raise SystemExit('ERROR: Expected volumes 01–05 and at least one PDF. No files updated; review local folders first.')

    code = BUILDER.read_text(encoding='utf-8')
    if "'JAMI_AL_TIRMIZI_BUSHRA':" not in code:
        match = re.search(r'^COLLECTION_NAMES\s*=\s*\{', code, flags=re.M)
        if not match:
            raise SystemExit('ERROR: COLLECTION_NAMES block not found in search builder; no changes made.')
        pos = match.end()
        code = code[:pos] + '\n    ' + KEY + code[pos:]
        BUILDER.write_text(code, encoding='utf-8')
        print('Added proper Urdu/English Tirmidhi name to search builder.')
    else:
        print('Tirmidhi name already exists in builder; unchanged.')

    if README.exists():
        print('Existing README preserved:', README.relative_to(ROOT))
    else:
        lines = [
            '# جامع الترمذی — طبع البشری', '',
            '## مجموعے کا تعارف', '',
            'جامع الترمذی — طبع البشری کے اس مجموعے میں پانچ جلدوں کی PDF فائلیں موضوعاتی فہرست کے ساتھ پیش کی گئی ہیں۔',
            'فائلوں کے عنوانات اور ترتیب اصل موجودہ فائل ناموں سے حاصل کی گئی ہے؛ یہ ناشر کی مستند کتاب/باب نمبرنگ یا مطبوعہ صفحات کی تصدیق نہیں ہے۔',
            '', '## جلدوں کی فہرست', '',
            '| جلد | الگ PDF فائلیں | فولڈر کھولیں |', '| --- | ---: | --- |'
        ]
        for folder in folders:
            files = sorted(folder.rglob('*.pdf'), key=lambda p: natural(p.relative_to(folder).as_posix()))
            match = re.search(r'(?:Volume|Vol)[_-]*0*(\d+)', folder.name, re.I)
            vol = f'{int(match.group(1)):02d}' if match else folder.name
            lines.append(f'| جلد {vol} | {len(files)} | [فولڈر کھولیں]({encode_relative(folder.relative_to(COLLECTION))}/) |')
        lines += ['', '## تمام دستیاب PDF فائلوں کی فہرست', '',
                  'یہ فہرست اپ لوڈ شدہ PDF فائل ناموں سے تیار کی گئی ہے۔ لنکس اسی مجموعے کے فولڈرز میں کھلتے ہیں۔', '']
        for folder in folders:
            match = re.search(r'(?:Volume|Vol)[_-]*0*(\d+)', folder.name, re.I)
            vol = f'{int(match.group(1)):02d}' if match else folder.name
            lines += [f'### جلد {vol}', '', '| نمبر | فائل / عنوان | PDF |', '| ---: | --- | --- |']
            files = sorted(folder.rglob('*.pdf'), key=lambda p: natural(p.relative_to(folder).as_posix()))
            for number, pdf in enumerate(files, 1):
                title = pdf.stem.replace('_', ' ').replace('|', '\\|')
                url = encode_relative(pdf.relative_to(COLLECTION))
                lines.append(f'| {number} | {title} | [PDF کھولیں](<{url}>) |')
            lines.append('')
        lines += ['## تلاش', '',
                  '[تلاشِ کتب حدیث — تمام مجموعے](../hadith-search.html)', '',
                  '> نوٹ: یہ تلاش فائل ناموں اور دستیاب عنوانات کی بنیاد پر ہے؛ اسکین شدہ صفحات کے اندر مکمل متن کی تلاش نہیں۔', '']
        README.write_text('\n'.join(lines), encoding='utf-8')
        print('Created Urdu README with links:', README.relative_to(ROOT))
    print('\nNEXT: python generate_file_pages.py')
    print('Check output: search index should show 3 collections and include Tirmidhi PDFs.')

if __name__ == '__main__':
    main()
