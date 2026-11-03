#!/usr/bin/env python3
"""One-time, safe integration with your EXISTING generate_file_pages.py.

Run from repository root: python install_hadith_search_hook.py
Creates a .git/local-backups copy. Does not overwrite generator internals.
"""
from pathlib import Path
import ast
import shutil

root = Path(__file__).resolve().parent
target = root / 'generate_file_pages.py'
search_script = root / 'build_hadith_search.py'
if not target.is_file() or not search_script.is_file():
    raise SystemExit('Run from repository root, with generator and search script in the root.')
src = target.read_text(encoding='utf-8')
needle = '    # EMARKAZ_HADITH_SEARCH_AUTO_BUILD_V1\n    from build_hadith_search import main as build_hadith_search_main\n    build_hadith_search_main()\n'
if 'EMARKAZ_HADITH_SEARCH_AUTO_BUILD_V1' in src:
    print('Already installed. Nothing changed.')
else:
    # Insert into main(), after the existing generation pass, before the module guard.
    guard = 'if __name__ == "__main__":'
    if guard not in src or 'def main():' not in src or src.count(guard) != 1:
        raise SystemExit('Generator layout was not recognized. No changes made.')
    idx = src.index(guard)
    before = src[:idx].rstrip('\n')
    after = src[idx:]
    modified = before + '\n' + needle + '\n' + after
    ast.parse(modified)
    backup_dir = root / '.git' / 'local-backups'
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / 'generate_file_pages_before_hadith_search.py'
    shutil.copy2(target, backup)
    target.write_text(modified, encoding='utf-8')
    print(f'Installed generator hook. Backup: {backup.relative_to(root)}')
print('Next: python generate_file_pages.py')
