from pathlib import Path
import re
from urllib.parse import urlsplit

START, END = '<!-- sitenav:auto -->', '<!-- /sitenav:auto -->'
BLOCK = re.compile(re.escape(START) + r'.*?' + re.escape(END) + r'(?:\r?\n)?', re.S)
BODY = re.compile(r'<body\b[^>]*>', re.I)
REDIRECT = re.compile(r'<meta[^>]+http-equiv\s*=\s*["\x27]?refresh', re.I)
SKIP = {'assets', 'queue', 'preview', 's', 'stats', 'nifty', 'tools', 'pagefind'}
BAR = START + """<link rel="stylesheet" href="/assets/reader-navigation.css">
<div class="sr-reader-slot"><nav class="sr-reader-bar" aria-label="Reader navigation">
<a class="sr-reader-back" href="__BACK_PATH__"><span aria-hidden="true">&larr;</span> Back</a>
<a href="/"><span aria-hidden="true">&#8962;</span> Home</a>
<a href="__SEARCH_PATH__"><span aria-hidden="true"><span class="sr-search-icon"></span></span> Search</a>
</nav></div>
<script defer src="/assets/reader-navigation.js"></script>
""" + END + '\n'

def apply(root, main=False):
    search = '/search/'
    count = 0
    for page in sorted(root.rglob('*.html')):
        relative = page.relative_to(root)
        if any(p.startswith('.') or p in SKIP for p in relative.parts[:-1]):
            continue
        with page.open(encoding='utf-8', newline='') as stream:
            original = stream.read()
        if REDIRECT.search(original) or not BODY.search(original):
            continue
        clean = BLOCK.sub('', original)
        parts = relative.parts[:-1]
        parent = '/' + '/'.join(parts[:-1]) + '/' if len(parts) > 1 else '/'
        if len(parts) == 2 and parts[0] == 'health' and re.match(r'^\d{2}-', parts[1]):
            parent = '/health/general/'
        if main and len(parts) == 1 and parts[0] not in {'about','archive','bhakti','gods','health','ortho','search'}:
            parent = '/archive/'
        if not (root / parent.strip('/') / 'index.html').is_file():
            parent = '/'
        block = BAR.replace('__BACK_PATH__', parent).replace('__SEARCH_PATH__', search)
        line_end = '\r\n' if '\r\n' in original else '\n'
        block = block.replace('\n', line_end)
        pos = BODY.search(clean).end()
        new = clean[:pos] + line_end + block + clean[pos:].lstrip('\r\n')
        if new != original:
            with page.open('w', encoding='utf-8', newline='') as stream:
                stream.write(new)
            count += 1
    return count

if __name__ == '__main__':
    print(f'Updated {apply(Path(__file__).resolve().parent.parent)} page(s)')
