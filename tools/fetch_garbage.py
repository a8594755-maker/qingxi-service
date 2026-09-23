# -*- coding: utf-8 -*-
"""從桃園市垃圾清運路線即時查詢系統（route.tyoem.gov.tw）撈出中壢區所有路線，
列出清運點備註含「青溪里」的點。用法：python tools/fetch_garbage.py [里名]

官方網站不允許 iframe、也沒開 CORS，所以只能像這樣從伺服器端查詢：
先開首頁拿 session cookie 與隱藏欄位 random_form，再 POST 到 dataManagerAgentWeb.jsp。
"""
import http.cookiejar
import json
import re
import sys
import urllib.parse
import urllib.request

BASE = 'https://route.tyoem.gov.tw'
TOWN = 'lagi2-004'  # 中壢區
VILLAGE = sys.argv[1] if len(sys.argv) > 1 else '青溪里'
DAYS = '日一二三四五六'  # run_type 第 i 碼 = JS getDay()，週日為 0

jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
op.addheaders = [('User-Agent', 'Mozilla/5.0')]
home = op.open(BASE + '/', timeout=30).read().decode('utf-8', 'replace')
tag = re.search(r'<[^>]*id="random_form"[^>]*>', home)
rf = re.search(r'value="([^"]*)"', tag.group(0)).group(1) if tag else ''


def post(**params):
    body = urllib.parse.urlencode(dict(random_form=rf, **params)).encode()
    return json.loads(op.open(BASE + '/web/dataManagerAgentWeb.jsp', body, timeout=30).read().decode('utf-8'))


routes = post(dcfid='lagifQueryRouteByTown', gid=TOWN).get('result') or []
print('中壢區路線數：%d' % len(routes))
found = 0
for r in routes:
    # 用「班表」查詢：固定帶 memo（含里名）；即時查詢 lagifRealtimeRouteDetailByRoute 在收運結束後常不帶 memo
    pts = post(dcfid='lagifQueryTimeTableDetailByRoute', routing_id=r['routing_id']).get('result') or []
    hits = [p for p in pts if VILLAGE in (p.get('memo') or '')]
    if not hits:
        continue
    rt = r.get('run_type') or ''
    days = '、'.join(DAYS[i] for i, c in enumerate(rt) if c != '0') or '（未標示）'
    recycle = '、'.join(DAYS[i] for i, c in enumerate(rt) if c == '2')
    print('\n== %s %s（%s）收運：週%s；資收日：%s' % (r.get('routing_name', ''), r.get('routing_id'), rt, days, recycle or '同車'))
    for p in hits:
        found += 1
        print('  %s  %s  (%s, %s)  %s' % (p.get('arrive_time'), p.get('poi_name'), p.get('lat'), p.get('lng'), p.get('show_memo') or ''))
print('\n共 %d 個「%s」清運點。大樓的社區專車點沒有標示里別，需另外判斷。' % (found, VILLAGE))
