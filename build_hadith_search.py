#!/usr/bin/env python3
"""Build eMarkaz Hadith Search index from repository PDFs.

Run from repository root: python build_hadith_search.py
No PDF is opened or modified. Automatically discovers all first-level
collections inside emarkaz-books/e-courses/hadith/.
"""
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent
HADITH = ROOT / 'emarkaz-books' / 'e-courses' / 'hadith'
OUT = HADITH / 'hadith-search-index.json'
PAGE_NAME = 'hadith-search.html'
MARK = '<!-- EMARKAZ_HADITH_SEARCH_BUTTON_V1 -->'
COLLECTION_NAMES = {
    'JAMI_AL_TIRMIZI_BUSHRA': {'ur': 'جامع الترمذی — طبع البشری', 'en': 'Jami al-Tirmidhi Al-Bushra'},
    'Sahih-Bukhari-Al-Bushra': {'ur': 'صحیح البخاری — طبع البشری', 'en': 'Sahih Bukhari Al-Bushra'},
    'Sahih_Muslim': {'ur': 'صحیح مسلم', 'en': 'Sahih Muslim'},
}
SKIP_DIRS = {'.git', '.github', '__pycache__', '.venv', 'node_modules'}


def natural_key(text):
    return [int(a) if a.isdigit() else a.casefold() for a in re.split(r'(\d+)', text)]


def pretty_name(raw):
    return re.sub(r'[_-]+', ' ', raw).strip()


def volume_label(relparts):
    for p in relparts:
        match = re.search(r'(?:volume|vol)[_\s-]*0*(\d+)(?!\d)', p, re.I)
        if match:
            return f'{int(match.group(1)):02d}'
    return ''


def build():
    if not HADITH.is_dir():
        raise SystemExit(f'Cannot find Hadith folder: {HADITH}. Run this in your repository.')
    collections = []
    entries = []
    for collection in sorted(HADITH.iterdir(), key=lambda p: natural_key(p.name)):
        if not collection.is_dir() or collection.name.startswith('.') or collection.name in SKIP_DIRS:
            continue
        pdfs = sorted((p for p in collection.rglob('*') if p.is_file() and p.suffix.lower() == '.pdf'
                       and not any(s in SKIP_DIRS or s.startswith('.') for s in p.relative_to(collection).parts[:-1])),
                      key=lambda p: natural_key(p.relative_to(collection).as_posix()))
        if not pdfs:
            continue
        name = COLLECTION_NAMES.get(collection.name, {'ur': pretty_name(collection.name), 'en': pretty_name(collection.name)})
        collection_key = collection.name
        counts = {}
        for pdf in pdfs:
            rel = pdf.relative_to(collection)
            vol = volume_label(rel.parts[:-1])
            counts[vol or 'Other'] = counts.get(vol or 'Other', 0) + 1
            # URL paths are encoded per segment; source files remain untouched.
            url = '/'.join(quote(x, safe='') for x in pdf.relative_to(ROOT).parts)
            title = pretty_name(pdf.stem)
            entries.append({
                'collection': collection_key,
                'collectionName': name['ur'],
                'collectionEnglish': name['en'],
                'volume': vol,
                'title': title,
                'filename': pdf.name,
                'url': '/' + url,  # root-relative URL for GitHub Pages custom domain
            })
        collections.append({
            'id': collection_key, 'name': name['ur'], 'english': name['en'],
            'count': len(pdfs), 'volumes': sorted(counts.keys(), key=natural_key),
            'url': '/' + '/'.join(quote(x, safe='') for x in collection.relative_to(ROOT).parts) + '/',
        })
    data = {'schemaVersion': 1, 'collections': collections, 'entries': entries}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Search index: {len(entries)} PDFs across {len(collections)} collections -> {OUT.relative_to(ROOT)}')
    return collections


def add_buttons(collections):
    """Add a search button to currently generated pages, safely and idempotently."""
    targets = [(HADITH / 'index.html', None)]
    targets += [(HADITH / c['id'] / 'index.html', c['id']) for c in collections]
    for page, chosen in targets:
        if not page.is_file():
            print(f'Skipped search button, page missing: {page.relative_to(ROOT)}')
            continue
        html = page.read_text(encoding='utf-8')
        if MARK in html:
            continue
        target_url = ('../' if chosen else '') + PAGE_NAME
        if chosen:
            target_url += '?collection=' + quote(chosen, safe='')
        section = f'''\n    {MARK}\n    <section class="reader-section" style="margin:24px 0;padding:22px;border-radius:20px;background:#0b1c2a;color:#f8fafc;">
      <h2 style="color:#d2fff0;font-size:24px;margin:0 0 14px;">🔎 تلاشِ کتب حدیث / Hadith Search</h2>
      <p style="margin:0 0 14px;color:#dbeafe;">کتاب یا باب تلاش کریں — اردو، رومن اردو یا انگریزی میں</p>
      <a class="btn open" style="display:inline-block;background:#10b981;color:#06111f;padding:12px 20px;border-radius:12px;" href="{escape(target_url, quote=True)}">کتاب تلاش کریں / Search PDFs →</a>
    </section>\n'''
        anchor = '    <section class="hero">'
        if anchor not in html:
            print(f'Skipped search button, hero not found: {page.relative_to(ROOT)}')
            continue
        html = html.replace(anchor, section + anchor, 1)
        page.write_text(html, encoding='utf-8')
        print(f'Search button added: {page.relative_to(ROOT)}')


def main():
    collections = build()
    add_buttons(collections)


if __name__ == '__main__':
    main()
