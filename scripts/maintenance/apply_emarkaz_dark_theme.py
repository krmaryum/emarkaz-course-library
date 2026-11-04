#!/usr/bin/env python3
"""Install a consistent dark theme across eMarkaz public pages.

Run from the repository root:
    python apply_emarkaz_dark_theme.py

Safe to re-run. Preserves existing content, generated-page logic,
Hadith search hooks, README previews, and links.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
GEN = ROOT / "generate_file_pages.py"
HOME = ROOT / "index.html"
MARKER = "EMARKAZ_UNIFIED_DARK_V1"
ROOTS = [
    "books", "emarkaz-books", "quran-juzz",
    "Fatawaz", "Molana-Ilyas-Ghuman-db-Books",
]
# Appended last so these overrides win over existing page CSS.
DARK_CSS = r"""
/* EMARKAZ_UNIFIED_DARK_V1 — accessible, consistent dark palette */
:root { color-scheme: dark; --emarkaz-bg:#071421; --emarkaz-panel:#102739;
  --emarkaz-line:#315067; --emarkaz-text:#eff7ff;
  --emarkaz-muted:#c2d3df; --emarkaz-accent:#80edd0; }
body {
  background: linear-gradient(155deg,#071421 0%,#0b2031 55%,#0b282c 100%) !important;
  color:var(--emarkaz-text) !important;
}
header, .top-bar:not(.container), .search-wrap, .hero:not(body > .hero),
.reader-section, .book-card, .folder-card, .toc, .article,
.panel, .result, .card:not(.glass), .note {
  background-color:var(--emarkaz-panel) !important;
  color:var(--emarkaz-text) !important;
  border-color:var(--emarkaz-line) !important;
}
.hero, .search-wrap, .reader-section, .book-card, .folder-card,
.toc, .article, .panel, .result {
  box-shadow:0 16px 40px rgba(0,0,0,.25) !important;
}
h1,h2,h3,h4,h5,h6, .hero h1, .hero h2,
.book-card h3, .folder-card h3, .section-title,
.note-content h1, .note-content h2, .note-content h3, .note-content h4 {
  color:#f8fafc !important;
}
p, li, .english, .reader-meta p, .note-content p,
.subtitle, .search-count, .status, .foot, .meta {
  color:var(--emarkaz-muted) !important;
}
a:not(.btn):not(.back):not(.semester):not(.open):not(.download):not(.folder-link-list a) {
  color:#91e9fa;
}
.search-input, input[type="search"], input[type="text"], select,
textarea {
  background:#091c2b !important;
  color:#fff !important;
  border-color:#426078 !important;
}
input::placeholder,textarea::placeholder { color:#b8cad6 !important; opacity:1; }
.search-label, .file-type, .badge { color:#a5f3fc !important; }
.file-type, .badge {
  background:#153b43 !important; border-color:#326e70 !important;
}
.folder-link-list a {
  background:#123c42 !important; border-color:#3b6c6b !important;
  color:#c4ffeb !important;
}
.no-results { background:#102739 !important; color:#c2d3df !important;
  border-color:#426078 !important; }
.book-card:hover,.folder-card:hover { border-color:#5eead4 !important; }
.note-content th { background:#153947 !important; color:#fff !important; }
.note-content th,.note-content td { border-color:#3c6171 !important; }
.note-content td { color:#e5f2fb !important; }
.note-content a { color:#84e8fa !important; }
.note-content pre { background:#06111f !important; }
.btn.open, .btn-primary, .open { background:#0b8a69 !important; color:#fff !important; }
.btn.download, .download { background:#2456a6 !important; color:#fff !important; }
.back { background:#155546 !important; color:#fff !important; }
.btn-outline { color:#f8fafc !important; border-color:#4a6576 !important; }
@media print {
  :root { color-scheme:light; }
  body { background:#fff !important; color:#111 !important; }
  .book-card,.folder-card,.article,.reader-section,.search-wrap,
  .toc,.panel,.result { background:#fff !important; color:#111 !important; }
  h1,h2,h3,h4,h5,h6,p,li,.note-content p { color:#111 !important; }
}
"""
START = "<!-- " + MARKER + " -->"
END = "<!-- /" + MARKER + " -->"


def fail(msg):
    raise SystemExit("ERROR: " + msg)


def inject_html(path):
    text = path.read_text(encoding="utf-8")
    if START in text:
        return False
    match = re.search(r"</head\s*>", text, flags=re.I)
    if not match:
        print(f"Skipped (no </head>): {path.relative_to(ROOT)}")
        return False
    fragment = f"\n{START}\n<style>\n{DARK_CSS}\n</style>\n{END}\n"
    # Last style in head takes priority over earlier CSS.
    text = text[:match.start()] + fragment + text[match.start():]
    path.write_text(text, encoding="utf-8")
    return True


def patch_generator():
    src = GEN.read_text(encoding="utf-8")
    if MARKER in src:
        print("Generator already includes dark theme.")
        return False
    # Update the *source of truth*: the function called for every generated page.
    pattern = r'(def page_css\(\)\s*(?:->\s*str)?\s*:\s*\n\s*return\s+""")(.*?)("""\s*)'
    m = re.search(pattern, src, flags=re.S)
    if not m:
        fail("Could not find page_css() triple-quoted CSS. Generator unchanged.")
    css = m.group(2)
    replacement = m.group(1) + css + "\n" + DARK_CSS + "\n" + m.group(3)
    src = src[:m.start()] + replacement + src[m.end():]
    GEN.write_text(src, encoding="utf-8")
    print("Updated generator's page_css() to keep future pages dark.")
    return True


def main():
    if not GEN.is_file() or not HOME.is_file():
        fail("Run from C:/Linux/emarkaz-course-library (repo root).")
    try:
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True,
                                text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        fail("Git check failed.")
    # This installer itself may be newly copied into the repository.
    unrelated = [line for line in status.splitlines()
                 if not line.endswith("apply_emarkaz_dark_theme.py")]
    if unrelated:
        fail("Review existing uncommitted changes first:\n" + "\n".join(unrelated))
    patch_generator()
    # Preserve the current generator's search hooks, shared collections and README layout.
    print("Regenerating library pages...")
    subprocess.run([sys.executable, str(GEN.name)], cwd=ROOT, check=True)

    # The homepage and standalone HTML pages (such as the reader and search UI)
    # are not generated by page_css() and need their own dark theme overrides.
    targets = [HOME, ROOT / "markdown-viewer.html"]
    for name in ROOTS:
        folder = ROOT / name
        if folder.is_dir():
            targets += [p for p in folder.rglob("*.html") if p.name != "index.html"]
    changed = 0
    for file in targets:
        if file.is_file() and inject_html(file):
            changed += 1
            print("Styled standalone page:", file.relative_to(ROOT))
    print(f"\nDONE: {changed} standalone pages styled; generated pages styled via generator.")
    print("Review: git status && git diff --stat")


if __name__ == "__main__":
    main()
