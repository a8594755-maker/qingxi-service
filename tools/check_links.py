# -*- coding: utf-8 -*-
"""檢查六個頁面裡所有對外連結是否打得開。用法（在專案根目錄）：python tools/check_links.py

政府網站偶爾很慢或擋程式，這裡失敗的網址要再用瀏覽器實際開一次確認，不要直接刪。
"""
import glob
import html
import os
import re
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('fonts.googleapis.com', 'fonts.gstatic.com')

urls = set()
for f in glob.glob(os.path.join(ROOT, '*.html')):
    for u in re.findall(r'href="(https?://[^"]+)"', open(f, encoding='utf-8').read()):
        if not any(s in u for s in SKIP):
            urls.add(html.unescape(u))

bad = []
for u in sorted(urls):
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        code = urllib.request.urlopen(req, timeout=30).status
    except Exception as e:  # noqa: BLE001
        code = getattr(e, 'code', None) or type(e).__name__
    ok = isinstance(code, int) and code < 400
    print('%s  %s' % ('OK ' if ok else 'BAD', u) + ('' if ok else '  (%s)' % code))
    if not ok:
        bad.append(u)
print('\n%d 個連結，%d 個需要用瀏覽器再確認' % (len(urls), len(bad)))
