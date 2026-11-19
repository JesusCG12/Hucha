"""Prepara la app web para el APK de Android.

Copia index.html a android/app/src/main/assets quitando lo que solo sirve en la web
(manifest, service worker y descarga directa) y deja las fuentes dentro del APK,
para que se vean igual sin conexión.

Uso: python3 tools/android_assets.py index.html android/app/src/main/assets
"""
import re
import sys
import urllib.request
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding='utf-8')
out = Path(sys.argv[2])
(out / 'fonts').mkdir(parents=True, exist_ok=True)

html = re.sub(r'<!--PWA-->.*?<!--/PWA-->\n', '', src, flags=re.S)
html = re.sub(r'\n\s*/\*PWA-JS\*/.*?/\*/PWA-JS\*/', '', html, flags=re.S)
html = re.sub(r'\n\s*/\*SELFHOST\*/.*?/\*/SELFHOST\*/', '', html, flags=re.S)

link = re.search(r'<link href="(https://fonts\.googleapis\.com/css2[^"]+)" rel="stylesheet">', html)
if link:
    css_url = link.group(1).replace('&amp;', '&')
    try:
        ua = 'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Mobile Safari/537.36'
        css = urllib.request.urlopen(urllib.request.Request(css_url, headers={'User-Agent': ua}), timeout=30).read().decode('utf-8')
        # Solo los alfabetos latinos: con eso basta para el español.
        blocks = re.findall(r'/\* ([a-z-]+) \*/\s*(@font-face \{.*?\})', css, flags=re.S)
        keep = [b for name, b in blocks if name in ('latin', 'latin-ext')] or re.findall(r'@font-face \{.*?\}', css, flags=re.S)
        local_css = []
        for i, block in enumerate(keep):
            url = re.search(r'url\((https://[^)]+)\)', block).group(1)
            name = 'f%d.woff2' % i
            (out / 'fonts' / name).write_bytes(urllib.request.urlopen(url, timeout=30).read())
            local_css.append(block.replace(url, 'fonts/' + name))
        html = html.replace(link.group(0), '<style>\n' + '\n'.join(local_css) + '\n</style>')
        html = re.sub(r'<link rel="preconnect"[^>]*>\n', '', html)
        print('fuentes incluidas:', len(local_css))
    except Exception as e:  # sin fuentes se usan las del sistema
        print('No se han podido descargar las fuentes:', e)

assert 'serviceWorker' not in html and 'manifest.webmanifest' not in html
(out / 'index.html').write_text(html, encoding='utf-8')
print('index.html listo:', len(html), 'bytes')
