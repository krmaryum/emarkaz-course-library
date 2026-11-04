#!/usr/bin/env python3
"""One-time eMarkaz patch: feature Hadith Search on homepage and move technical guide.

Run from the eMarkaz repository root:
    python add_hadith_search_to_homepage.py

Designed not to replace existing homepage or generator; repeat runs are safe.
"""

from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path.cwd()
HOME = ROOT / "index.html"
GENERATE = ROOT / "generate_file_pages.py"
HADITH = ROOT / "emarkaz-books" / "e-courses" / "hadith"
SEARCH = HADITH / "hadith-search.html"
GUIDE_FROM = HADITH / "HADITH-SEARCH-SETUP.md"
GUIDE_TO = ROOT / "docs" / "HADITH-SEARCH-SETUP.md"
START = "<!-- EMARKAZ_HADITH_SEARCH_HOME_V1 -->"
END = "<!-- /EMARKAZ_HADITH_SEARCH_HOME_V1 -->"

SECTION = f'''  {START}
    <section id="hadith-search-home" class="container" aria-labelledby="hadith-search-heading" style="padding-top:32px;padding-bottom:32px;">
      <div style="background:linear-gradient(135deg,#0b2630,#123b38);border:1px solid rgba(103,232,249,.32);border-radius:24px;padding:clamp(24px,4vw,42px);box-shadow:0 18px 44px rgba(0,0,0,.18);color:#f8fafc;">
        <p class="section-label" style="color:#a5f3fc;margin-bottom:12px;">Hadith Library · Search</p>
        <h2 id="hadith-search-heading" class="section-title" style="color:#fff;margin:0 0 14px;">تلاشِ کتبِ حدیث</h2>
        <p dir="rtl" style="color:#d4e7e8;font-size:17px;line-height:1.9;margin:0 0 20px;">
          صحیح البخاری اور صحیح مسلم کی کتب، ابواب اور موضوعات آسانی سے تلاش کریں۔
          اردو، عربی، رومن اردو اور انگریزی میں تلاش کی سہولت۔
        </p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;">
          <a class="btn btn-primary" href="emarkaz-books/e-courses/hadith/hadith-search.html" style="display:inline-block;background:#67e8f9;color:#06111f;font-weight:800;padding:13px 22px;border-radius:12px;text-decoration:none;">🔎 کتاب تلاش کریں / Search Hadith</a>
          <a class="btn btn-outline" href="emarkaz-books/e-courses/hadith/" style="display:inline-block;background:transparent;border:1px solid rgba(255,255,255,.4);color:#fff;padding:13px 22px;border-radius:12px;text-decoration:none;">📚 مکمل حدیث لائبریری</a>
        </div>
      </div>
    </section>
  {END}
'''


def fail(message):
    print("ERROR:", message, file=sys.stderr)
    raise SystemExit(1)


def main():
    for f in [HOME, GENERATE, SEARCH]:
        if not f.is_file():
            fail(f"Missing required file: {f}. Run this script from the repository root.")
    try:
        result = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                                capture_output=True, text=True, check=True)
    except (OSError, subprocess.CalledProcessError):
        fail("Git status failed. Use Git Bash inside the Git repository.")
    # Allow the newly copied one-time helper script, but stop on unrelated edits.
    pending = [line for line in result.stdout.splitlines()
               if not line.endswith("add_hadith_search_to_homepage.py")]
    if pending:
        fail("You have pre-existing uncommitted changes. Run 'git status' and review them first.\n" + "\n".join(pending))

    html = HOME.read_text(encoding="utf-8")
    match = re.search(r'^\s*<section\b[^>]*\bid\s*=\s*[\"\']general-library[\"\'][^>]*>',
                      html, flags=re.M | re.I)
    if START not in html and not match:
        fail("Could not find homepage General Library section. No files changed.")
    if START in html and END not in html:
        fail("Existing search marker appears incomplete. No files changed.")
    if GUIDE_TO.exists() and GUIDE_FROM.exists():
        fail(f"Both guide locations exist. Resolve duplicates manually: {GUIDE_TO} and {GUIDE_FROM}")

    if GUIDE_FROM.is_file():
        GUIDE_TO.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(GUIDE_FROM), str(GUIDE_TO))
        print(f"Moved technical guide to: {GUIDE_TO.relative_to(ROOT)}")
    elif GUIDE_TO.is_file():
        print("Technical guide already in docs/.")
    else:
        print("Notice: Setup guide wasn't found; skipping guide move.")

    if START not in html:
        html = html[:match.start()] + SECTION + html[match.start():]
        HOME.write_text(html, encoding="utf-8")
        print("Added Hadith Search feature section immediately before General Library.")
    else:
        print("Homepage Hadith Search section already exists; skipping duplicate.")

    print("Regenerating library pages and Hadith search index via existing generator...")
    subprocess.run([sys.executable, str(GENERATE.name)], cwd=ROOT, check=True)
    print("\nDONE. Verify with: git status; git diff --stat")
    print("Expected: homepage modified, guide relocated, Hadith index page updated.")
    print("Only stage reviewed changes before pushing.")

if __name__ == "__main__":
    main()
