#!/usr/bin/env python3
"""Safe, rerunnable improvement to existing eMarkaz Hadith search and homepage.

Run at repository root. Does not touch PDF files, Python generators or index JSON.
Changes only the existing search HTML and (if present) homepage Hadith banner.
"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path.cwd()
SEARCH = ROOT / 'emarkaz-books/e-courses/hadith/hadith-search.html'
HOME = ROOT / 'index.html'
MARK = 'EMARKAZ_SEARCH_READABILITY_V2'
HM = 'EMARKAZ_HADITH_DYNAMIC_STATS_V2'

CSS = '''
/* EMARKAZ_SEARCH_READABILITY_V2 */
.result{display:flex;flex-direction:column;gap:8px;min-height:188px}
.result .meta{line-height:1.8;overflow-wrap:anywhere;color:#b9d4e0}
.result h3{margin:0;font-size:clamp(18px,1.7vw,21px);line-height:1.7;unicode-bidi:plaintext;overflow-wrap:anywhere}
.result h3[dir="ltr"]{text-align:left;font-family:Arial,Helvetica,sans-serif}
.result h3[dir="rtl"]{text-align:right;font-family:Arial,"Noto Naskh Arabic","Noto Nastaliq Urdu",sans-serif}
.result .actions{margin-top:auto;padding-top:6px}
.result .btn{display:inline-flex;align-items:center;justify-content:center;min-height:41px}
.result:focus-within{outline:2px solid #6ce2bd;outline-offset:2px}
#volume,#collection{font-family:Arial,"Noto Naskh Arabic",sans-serif}
@media(max-width:760px){.result{min-height:0}.result h3{font-size:19px}}
'''

# Avoid assumptions about the index format, use the actual entries already loaded by existing JS.
VOLUME_OLD = "function updateVolumes(){const previous=vol.value;vol.replaceChildren();addOption(vol,'','تمام جلدیں');const v=new Set(entries.filter(e=>!col.value||e.collection===col.value).map(e=>e.volume).filter(Boolean));[...v].sort((a,b)=>Number(a)-Number(b)).forEach(x=>addOption(vol,x,'جلد '+x));if(v.has(previous))vol.value=previous}"
VOLUME_NEW = """function updateVolumes(){
 const previous=vol.value;vol.replaceChildren();addOption(vol,'','تمام جلدیں');
 const counts=new Map();for(const e of entries){if(col.value&&e.collection!==col.value)continue;if(!e.volume)continue;counts.set(e.volume,(counts.get(e.volume)||0)+1)}
 [...counts.keys()].sort((a,b)=>Number(a)-Number(b)).forEach(x=>addOption(vol,x,'جلد '+String(x).padStart(2,'0')+' — '+counts.get(x)+' PDFs'));
 if(counts.has(previous))vol.value=previous;
}"""
CARD_OLD = "const card=el('article','result');card.append(el('div','meta',item.collectionName+(item.volume?' · جلد '+item.volume:'')));card.append(el('h3','',item.title));"
CARD_NEW = """const card=el('article','result');
 const meta=el('div','meta',item.collectionName+(item.volume?' · جلد '+String(item.volume).padStart(2,'0'):''));card.append(meta);
 const heading=el('h3','',item.title);
 // When the title starts with Arabic/Urdu it reads RTL; Latin titles read LTR.
 const first=String(item.title||'').trim().charAt(0);
 heading.setAttribute('dir',/[\\u0600-\\u06FF]/.test(first)?'rtl':'ltr');
 card.append(heading);"""
STATUS_OLD = "status.textContent=count.toLocaleString()+' PDFs found · '+collections.length+' collections indexed';"
STATUS_NEW = "status.textContent=count.toLocaleString()+' PDFs found · '+collections.length+' collections indexed';" # No behavioral change.

HOMESCRIPT = r'''<script id="EMARKAZ_HADITH_DYNAMIC_STATS_V2">
(function () {
  const target = document.getElementById('hadith-search-live-stats');
  if (!target) return;
  fetch('emarkaz-books/e-courses/hadith/hadith-search-index.json', {cache:'no-store'})
    .then(function(response){if(!response.ok)throw new Error('index unavailable');return response.json();})
    .then(function(data){
      const n=(Array.isArray(data.entries)?data.entries.length:0);
      const c=(Array.isArray(data.collections)?data.collections.length:0);
      if(n&&c)target.textContent=c+' مجموعے · '+n.toLocaleString()+' PDFs searchable';
    }).catch(function(){target.textContent='مختلف کتبِ حدیث کی تلاش';});
})();
</script>'''


def fail(msg):
    raise SystemExit('ERROR: '+msg)


def replace_once(s, old, new, label):
    if s.count(old) != 1:
        fail(f'Unexpected {label} structure ({s.count(old)} matches). No changes saved.')
    return s.replace(old, new, 1)


def transform_search(s):
    if MARK in s:
        return s, False
    if not all(token in s for token in [VOLUME_OLD, CARD_OLD, '</style>']):
        fail('Search HTML differs from expected version. No files updated. Share current hadith-search.html.')
    s = replace_once(s, VOLUME_OLD, VOLUME_NEW, 'volume selector')
    s = replace_once(s, CARD_OLD, CARD_NEW, 'result cards')
    pos = s.lower().find('</style>')
    s = s[:pos] + CSS + '\n' + s[pos:]
    return s, True


def transform_home(s):
    if HM in s:
        return s, False
    if 'id="hadith-search-home"' not in s:
        print('Notice: No existing Hadith homepage banner found. Homepage left unchanged.')
        return s, False
    match = re.search(r'(<section\b[^>]*\bid="hadith-search-home"[\s\S]*?</section>)', s)
    if not match:
        fail('Hadith homepage section incomplete. No files updated.')
    section = match.group(1)
    if 'hadith-search-live-stats' in section:
        return s, False
    # Insert dynamic stats below existing description, keep all existing text/links.
    needle = '</p>'
    at = section.find(needle)
    if at < 0:
        fail('Homepage banner has no paragraph. No files updated.')
    at += len(needle)
    section = section[:at] + '\n        <p id="hadith-search-live-stats" style="color:#a5f3fc;font-size:15px;margin:8px 0 18px;">مختلف کتبِ حدیث کی تلاش</p>' + section[at:]
    result = s[:match.start()] + section + s[match.end():]
    # Script is explicitly scoped to the homepage banner, injected near end of body.
    if '</body>' not in result.lower():
        fail('Homepage lacks closing body tag. No files updated.')
    result = re.sub(r'</body>', HOMESCRIPT+'\n</body>', result, count=1, flags=re.I)
    return result, True


def main():
    if not SEARCH.is_file() or not HOME.is_file():
        fail('Run from the eMarkaz repository root; hadith-search.html and index.html must exist.')
    status = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, check=True).stdout
    other = [line for line in status.splitlines() if not line.endswith('improve_emarkaz_hadith_search.py')]
    if other:
        fail('Working tree has other changes. Review/commit or stash before running:\n'+'\n'.join(other))
    original_search=SEARCH.read_text(encoding='utf-8')
    original_home=HOME.read_text(encoding='utf-8')
    new_search, change_search=transform_search(original_search)
    new_home, change_home=transform_home(original_home)
    if change_search: SEARCH.write_text(new_search, encoding='utf-8')
    if change_home: HOME.write_text(new_home, encoding='utf-8')
    print('Search page:', 'improved' if change_search else 'already updated')
    print('Homepage banner:', 'dynamic stats added' if change_home else 'unchanged')
    print('No PDFs, search index JSON or generator modified.')
    print('Next: git diff --check && git diff --stat && git status')

if __name__ == '__main__':
    main()
