# -*- coding: utf-8 -*-
"""產生青溪里網站的六個頁面（index/news/progress/services/life/activities.html）。

用法（在專案根目錄）：python tools/build.py
內容資料都在 tools/content.py；這支檔案只管版型。HTML 是產生出來的，不要直接改 HTML。
"""
import io
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
TEL = 'tel:+886939585611'
PHONE = '0939-585-611'
FB = 'https://www.facebook.com/coco.lee.58'
MAP_URL = 'https://maps.app.goo.gl/wySd4JdQv5F2VPVi7'
MAP_EMBED = ('https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1808!2d121.2079571!3d25.0041417!2m3!1f0!2f0!3f0'
             '!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3468211558ed952b%3A0x336278e5a2bac507!2z6Z2S5rqq6YeM6YeM6L6m5YWs6JmV'
             '!5e0!3m2!1szh-TW!2stw')
EXT = ' target="_blank" rel="noopener noreferrer"'

I_PHONE = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/></svg>'
I_ARR = '<svg class="arr" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
I_EXT = '<svg class="arr" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17L17 7M9 7h8v8"/></svg>'
I_INFO = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>'

EDGE_A = ('M0,0 H1440 V18 C1402,24 1371,14 1330,22 C1287,31 1250,27 1210,19 C1168,11 1131,26 1088,30 C1046,34 1010,22 968,17 '
          'C925,12 892,28 850,33 C806,38 771,27 730,21 C688,15 650,30 606,34 C563,38 530,24 488,18 C446,12 410,26 368,31 '
          'C325,36 290,25 250,20 C207,14 170,29 128,33 C86,37 45,26 0,21 Z')
EDGE_B = ('M0,0 H1440 V22 C1398,30 1360,17 1318,24 C1276,31 1240,36 1196,27 C1152,18 1118,15 1076,25 C1034,35 996,38 954,29 '
          'C912,20 874,14 832,23 C790,32 752,37 710,28 C668,19 632,14 588,24 C544,34 508,36 466,27 C424,18 388,16 346,25 '
          'C304,34 266,36 224,27 C182,18 146,15 104,24 C62,33 30,30 0,26 Z')


def edge(cls, path, dots):
    circles = ''.join('<circle cx="%d" cy="%d" r="%.1f"/>' % d for d in dots)
    return ('<svg class="edge %s" viewBox="0 0 1440 56" preserveAspectRatio="none" aria-hidden="true">'
            '<path d="%s"/>%s</svg>' % (cls, path, circles))


def chars(text, start=0):
    out = []
    for i, ch in enumerate(text):
        out.append('<span class="hc" style="--i: %d;">%s</span>' % (start + i, ch))
    return ''.join(out)


NAV = [('index.html', '首頁', 'home'), ('news.html', '最新公告', 'news'), ('progress.html', '里務進度', 'progress'),
       ('services.html', '服務項目', 'services'), ('life.html', '生活資訊', 'life'), ('activities.html', '活動紀錄', 'activities')]

HEAD_SCRIPT = ("<script>(function(h){h.classList.add('js');var m=false;"
               "try{m=window.matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}"
               "if(!m){h.classList.add('anim');setTimeout(function(){if(!window.QX_READY){h.classList.remove('anim')}},4000)}"
               "%s})(document.documentElement);</script>")
INTRO_FLAG = ("try{if(sessionStorage.getItem('qx-intro')==='1'){h.classList.add('nointro')}"
              "else{sessionStorage.setItem('qx-intro','1')}}catch(e){h.classList.add('nointro')}")


def header(active):
    links = []
    for href, label, key in NAV[1:]:
        cur = ' aria-current="page"' if key == active else ''
        links.append('<a href="%s"%s>%s</a>' % (href, cur, label))
    mob = []
    for href, label, key in NAV:
        cur = ' aria-current="page"' if key == active else ''
        mob.append('<a href="%s"%s>%s%s</a>' % (href, cur, label, I_ARR))
    return ('<header class="site-header">\n<div class="wrap">\n'
            '<a class="brand" href="index.html" aria-label="青溪里里長辦公室 首頁">\n'
            '<span class="seal seal-sm" aria-hidden="true"><span>里</span><span>辦</span><span>青</span><span>溪</span></span>\n'
            '<span class="brand-text" aria-hidden="true"><span class="brand-name">青溪里</span><span class="brand-sub">里長辦公室</span></span>\n'
            '</a>\n'
            '<nav class="main-nav" aria-label="主要導覽">\n' + '\n'.join(links) + '\n'
            '<a class="btn btn-nav" href="index.html#contact">聯絡里長</a>\n</nav>\n'
            '<button class="menu-btn" type="button" aria-expanded="false" aria-controls="mobile-menu" aria-label="開啟選單"><span class="bars" aria-hidden="true"></span></button>\n'
            '</div>\n<span class="prog" aria-hidden="true"></span>\n</header>\n'
            '<div class="mobile-menu" id="mobile-menu" aria-hidden="true" inert>\n'
            '<nav aria-label="手機導覽">\n' + '\n'.join(mob) + '\n</nav>\n'
            '<div class="menu-call"><span>有事，直接找里長</span><a href="%s">%s</a></div>\n</div>\n' % (TEL, PHONE))


MOBILE_CTA = ('<div class="mobile-cta">\n<a class="call" href="%s">%s撥打電話</a>\n'
              '<a class="alt" href="news.html">最新公告</a>\n</div>\n' % (TEL, I_PHONE))

FOOT_TEXT = ('<div class="top"><span>&copy; 2026 青溪里里長辦公處．李詠芳</span><span>本網站僅供里民服務使用，非選舉宣傳用途。</span></div>\n'
             '<span>本網站依個人資料保護法規定，不主動蒐集里民個資。如需反映問題，請透過電話或社群聯繫。</span>\n')

PAGE_FOOT = ('<footer class="page-foot">\n' + edge('edge-paper', EDGE_B, [(520, 46, 2), (1180, 44, 1.7)]) + '\n'
             '<div class="wrap">\n<div class="call"><b>有事，直接找里長。</b><a href="%s">%s</a></div>\n' % (TEL, PHONE)
             + FOOT_TEXT + '</div>\n</footer>\n')


def page(fname, title, desc, active, main, foot=True, intro=''):
    html = ('<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="description" content="%s">\n'
            '<meta name="theme-color" content="#1C1815">\n'
            '<meta property="og:type" content="website">\n<meta property="og:title" content="%s">\n'
            '<meta property="og:description" content="%s">\n'
            '<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+TC:wght@500;700;900&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">\n'
            '<link rel="stylesheet" href="assets/css/site.css">\n%s\n'
            '<script src="assets/js/site.js" defer></script>\n</head>\n<body>\n'
            '<a class="skip" href="#main">跳至主要內容</a>\n'
            % (title, desc, title, desc, HEAD_SCRIPT % (INTRO_FLAG if intro else '')))
    html += intro + header(active) + '<main id="main">\n' + main + '\n</main>\n'
    if foot:
        html += PAGE_FOOT
    html += MOBILE_CTA + '</body>\n</html>\n'
    io.open(os.path.join(OUT, fname), 'w', encoding='utf-8', newline='\n').write(html)
    print(fname, len(html))


def page_hero(eyebrow, lines, lead):
    i, spans = 0, []
    for ln in lines:
        spans.append('<span class="line">' + chars(ln, i) + '</span>')
        i += len(ln) + 1
    return ('<section class="page-hero">\n<div class="wrap">\n'
            '<p class="eyebrow rv">%s</p>\n'
            '<h1><span class="sr-only">%s</span><span aria-hidden="true">%s</span></h1>\n'
            '<svg class="inkline" width="230" height="18" viewBox="0 0 230 18" fill="none" aria-hidden="true">'
            '<path pathLength="1" d="M3 11 C 42 4, 84 15, 126 9 S 198 5, 227 8" stroke="#B4633A" stroke-width="5" stroke-linecap="round"/></svg>\n'
            '<p class="lead rv d2">%s</p>\n</div>\n</section>\n' % (eyebrow, ''.join(lines), ''.join(spans), lead))


def sub_head(eyebrow, h2):
    return ('<div class="sub-head">\n<p class="eyebrow rv">%s</p>\n<h2 class="rv d1">%s</h2>\n</div>\n' % (eyebrow, h2))


from content import ACTS, ACT_FILTERS, HOME_CARDS, PROG, HOME_PROG, NEWS, NEWS_FILTERS, PLACES, FACTS, LINKS, TRASH_POINTS
ACT_BY_ID = {a[0]: a for a in ACTS}

def link_list(cls='link-list'):
    return ('<div class="%s">\n' % cls
            + '\n'.join('<a class="row" href="%s"%s>%s%s</a>' % (u, EXT, t, I_EXT) for t, u in LINKS)
            + '\n</div>')


# ───────────────────────── 首頁 ─────────────────────────
INTRO = ('<div class="intro" aria-hidden="true">\n<div class="ink"></div>\n<div class="seal-ring"></div>\n'
         '<div class="seal seal-big"><span>里</span><span>辦</span><span>青</span><span>溪</span></div>\n</div>\n')

MQ_ITEMS = [('路燈故障', 0), ('長者關懷', 1), ('停水停電通知', 0), ('寒冬送暖', 1), ('道路排水', 0),
            ('節慶活動', 1), ('防災訊息', 0), ('社福轉介', 1), ('急難協助', 0), ('環保志工', 1)]
mq_run = '<span>' + ''.join('<span%s>%s</span>' % (' class="o"' if o else '', t) for t, o in MQ_ITEMS) + '</span>'


def prog_item(mark, label, date, title, text):
    return ('<div class="prog-item row rv">\n<span class="mark %s">%s<span class="date">%s</span></span>\n'
            '<h3>%s</h3>\n<p>%s</p>\n</div>\n' % (mark, label, date, title, text))


def tile_photo(span, img, pos, alt, name, body_cls, body, delay=''):
    return ('<a class="tile tilt %s rv rv-img%s" href="services.html">\n'
            '<img src="%s" alt="%s" loading="lazy" style="object-position: %s;">\n<span class="shade"></span>\n'
            '<span class="t-bottom %s"><span class="t-name">%s</span>%s</span>\n<span class="glare"></span>\n</a>\n'
            % (span, delay, img, alt, pos, body_cls, name, body))


home_cards = ''.join(
    '<a class="card" href="activities.html#%s">\n<div class="ph"><img src="%s" alt="%s" loading="lazy" style="object-position: %s;"></div>\n'
    '<div><span class="meta">%s　%s</span><h3>%s</h3></div>\n</a>\n' % (a[0], a[1], a[6], a[7], a[4], a[3], a[5])
    for a in [ACT_BY_ID[i] for i in HOME_CARDS])

MOSAIC = [('images/elder-outing-2026.jpg', '關懷據點活動大合照', 'center'),
          ('images/yuanxiao-2026.jpg', '元宵節社區 DIY 湯圓', 'center 55%'),
          ('images/qingxi-cup-2025.jpg', '第一屆青溪盃', 'center 45%'),
          ('images/eco-volunteers-2026.jpg', '環保志工日常清掃', 'center 20%'),
          None,
          ('images/festival-2025.jpg', '里民活動現場', 'center 30%'),
          ('images/winter-warmth-2026.jpg', '寒冬送暖', 'center 40%'),
          ('images/community-assembly-2026.jpg', '社區發展協會會員大會', 'center'),
          ('images/softball-celebration-2025.jpg', '慢壘球隊慶功宴', 'center 65%')]
mosaic_cells = ''
for m in MOSAIC:
    if m is None:
        mosaic_cells += ('<div class="m-card"><p>因為有你們，<br>青溪不只是一個地方，<br>而是一個正在發生的<em>「家」</em>。</p></div>\n')
    else:
        mosaic_cells += ('<div class="m-ph"><img src="%s" alt="%s" loading="lazy" style="object-position: %s;"></div>\n' % m)

Q_LINES = [('「有些事情看起來很小，', False), ('但做了之後，', False), ('心裡會很暖。」', True)]
q_html = ''.join('<span class="l">' + ''.join('<span class="qc%s">%s</span>' % (' acc' if acc else '', c) for c in ln) + '</span>'
                 for ln, acc in Q_LINES)

HOME = (
    # 主視覺
    '<section class="hero" id="top">\n'
    '<svg width="0" height="0" style="position: absolute;" aria-hidden="true">'
    '<filter id="stamp"><feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="2" seed="7" result="t"/><feDisplacementMap in="SourceGraphic" in2="t" scale="6"/></filter>'
    '<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>'
    '</svg>\n'
    '<canvas class="flow-cv" aria-hidden="true"></canvas>\n'
    '<svg class="grain" aria-hidden="true"><rect width="100%" height="100%" filter="url(#grain)"/></svg>\n'
    '<div class="wrap hero-inner">\n<div class="hero-copy">\n'
    '<p class="hero-eyebrow fade" style="--dl: 0s;">桃園市中壢區　青溪里</p>\n'
    '<div class="hero-id">\n'
    '<h1 class="hero-name"><span class="role fade" style="--dl: 0.1s;">青溪里 里長</span>'
    '<span class="name" aria-hidden="true">' + chars('李詠芳') + '</span><span class="sr-only">李詠芳</span></h1>\n'
    '<figure class="portrait-m pfade" style="--dl: 0.35s;"><img src="images/chief-portrait.jpg" alt="青溪里里長李詠芳"></figure>\n'
    '</div>\n'
    '<p class="hero-tag fade" style="--dl: 0.55s;">需要幫忙的時候，<em>找得到人。</em></p>\n'
    '<p class="hero-lead fade" style="--dl: 0.75s;">青溪社區發展協會理事長，完成防災士培訓，也當了十幾年的國小故事媽媽志工。里民的大小事，用最快的速度處理。</p>\n'
    '<div class="hero-actions fade" style="--dl: 0.95s;">\n'
    '<a class="btn btn-lg btn-fill mag" href="' + TEL + '">' + I_PHONE + PHONE + '</a>\n'
    '<a class="btn btn-lg btn-ghost" href="#now">看里內最新狀態</a>\n</div>\n</div>\n'
    '<div class="hero-visual" aria-hidden="true">\n'
    '<div class="px" data-d="-10" style="left: 120px; top: 0;"><div class="pfade" style="--dl: 0.3s;"><div class="portrait"><img src="images/chief-portrait.jpg" alt=""></div></div></div>\n'
    '<div class="px" data-d="26" style="left: 0; top: 440px;"><div class="pfade" style="--dl: 0.8s;"><img class="sub-ph float-b" src="images/elder-outing-2026.jpg" alt=""></div></div>\n'
    '<div class="px" data-d="-30" style="left: 62px; top: 36px;"><div class="fade" style="--dl: 1.1s;"><div class="seal seal-mid"><span>里</span><span>辦</span><span>青</span><span>溪</span></div></div></div>\n'
    '</div>\n'
    '<a class="scroll-cue fade" style="--dl: 1.5s;" href="#now"><svg class="cue" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14M6 13l6 6 6-6"/></svg>往下看</a>\n'
    '</div>\n</section>\n'

    # 跑馬燈
    '<div class="marquee" aria-hidden="true"><div class="mq-wrap"><div class="mq">' + mq_run + mq_run + '</div></div></div>\n'

    # 最新狀態
    '<section class="now" id="now">\n' + edge('edge-dark', EDGE_A, [(312, 44, 2.4), (742, 45, 1.5), (930, 49, 2), (1122, 46, 1.8)]) + '\n'
    '<div class="wrap now-grid">\n<div class="now-side">\n'
    '<p class="eyebrow rv">此刻的青溪里</p>\n<h2 class="h-xl rv d1">每件事，<br>辦到哪了。</h2>\n'
    '<p class="lead rv d2">里民反映的問題與里辦推動的工作，依處理狀態公開列出。</p>\n'
    '<div class="stats rv d3">\n'
    '<div class="stat"><b style="color: var(--acc);">' + str(sum(1 for p in PROG if p[0] == 'going')) + '</b><span>持續進行</span></div>\n'
    '<div class="stat"><b>' + str(sum(1 for p in PROG if p[0] == 'done')) + '</b><span>已完成</span></div>\n'
    '<div class="stat"><b style="color: var(--warn);">' + str(sum(1 for p in PROG if p[0] == 'urgent')) + '</b><span>緊急應變・已結案</span></div>\n'
    '</div>\n</div>\n'
    '<div class="now-main">\n<p class="list-head rv">最新公告</p>\n'
    '<a class="notice-link row rv" href="news.html"><span><strong>里辦最新公告</strong>'
    '<small>活動報名、消毒與防災提醒都在這裡。最近一則：' + NEWS[0][4] + '　' + NEWS[0][5] + '</small></span>' + I_ARR + '</a>\n'
    '<p class="list-head gap rv">里務進度</p>\n'
    + ''.join(prog_item(p[1], p[2], p[6], p[3], p[4]) for p in PROG if p[3] in HOME_PROG)
    + '<a class="link-acc ul rv" href="progress.html">查看全部里務進度　→</a>\n'
    '</div>\n</div>\n</section>\n'

    # 服務磚
    '<section class="services" id="services">\n<div class="wrap">\n'
    '<div class="center-head">\n<p class="eyebrow rv">服務項目</p>\n<h2 class="h-xl rv d1">這些事，都可以找里辦。</h2>\n</div>\n'
    '<div class="tiles">\n'
    + tile_photo('s7', 'images/elder-outing-2026.jpg', 'center 40%', '青溪里關懷活動，里長與里民合影', '里民協助', 'row-end',
                 '<span class="t-grid"><span>社福資訊轉介</span><span>長者關懷與寒冬送暖</span><span>急難事件即時協助</span><span>行政流程協助說明</span></span>')
    + '<a class="tile tilt solid clay s5 rv d1" href="services.html">\n<span class="t-name">生活環境</span>\n'
      '<span class="lines"><span>路燈故障通報</span><span>道路／排水／公園問題反映</span><span>環境整潔與髒亂通報</span><span>消毒防疫作業協調</span></span>\n'
      '<span class="glare"></span>\n</a>\n'
    + tile_photo('s5', 'images/qingxi-cup-2025.jpg', 'center 35%', '114 年中壢區第一屆青溪盃', '社區經營', 'col',
                 '<span class="t-list"><span>節慶活動（元宵、中秋、冬至等）</span><span>樂活班、親子活動、手作課程</span><span>青溪盃慢壘球賽</span><span>環保志工招募與出遊</span></span>')
    + '<a class="tile tilt solid ink s7 rv d1" href="services.html">\n'
      '<svg class="deco" viewBox="0 0 720 460" preserveAspectRatio="none" fill="none" stroke="#E0906A" stroke-width="1.5" stroke-linecap="round" aria-hidden="true">'
      '<path d="M-20 120 C 140 60, 260 200, 420 130 S 640 60, 760 140"/><path d="M-20 190 C 160 130, 280 270, 440 200 S 660 130, 760 210"/><path d="M-20 60 C 120 10, 240 140, 400 70 S 620 10, 760 80"/></svg>\n'
      '<span class="t-name rel">防災與公告</span>\n'
      '<span class="lines two"><span>防災訊息與韌性社區推動</span><span>停水停電通知</span><span>政府補助與政策資訊</span><span>火災等緊急事件即時通報</span></span>\n'
      '<span class="glare"></span>\n</a>\n'
    '</div>\n</div>\n</section>\n'

    # 家
    '<section class="mosaic" aria-label="青溪里的日常">\n' + edge('edge-paper2', EDGE_B, [(206, 46, 2), (598, 44, 1.6), (1012, 48, 2.3)]) + '\n'
    '<div class="m-track"><div class="m-stage">\n<div class="m-grid">\n' + mosaic_cells + '</div>\n'
    '<p class="m-cap">——　里長 李詠芳・冬至親子活動</p>\n</div></div>\n</section>\n'

    # 里長的話與簡介
    '<section class="quote" id="about">\n<div class="q-track"><div class="q-stage"><div class="wrap">\n'
    '<p class="eyebrow light">里長的話</p>\n'
    '<blockquote class="q-text"><span class="sr-only">「有些事情看起來很小，但做了之後，心裡會很暖。」</span><span aria-hidden="true">' + q_html + '</span></blockquote>\n'
    '<p class="q-cap">——　里長 李詠芳</p>\n</div></div></div>\n'
    '<div class="wrap bio">\n'
    '<figure class="rv rv-img"><img src="images/winter-solstice-2025.jpg" alt="里長李詠芳於冬至活動中分享青溪 LOGO 設計理念" loading="lazy"></figure>\n'
    '<div class="bio-body">\n<div class="name rv"><p class="eyebrow light">經歷與投入</p><h2 class="h-lg">選上里長的第一件事，<br>是把大門打開。</h2></div>\n'
    '<p class="rv d1">學校空間不足，晨間故事媽媽沒有地方備課，里長就把里辦公處的大門打開給志工使用。服務以「快速回應、主動關心、透明處理」為原則，希望讓每位里民在需要幫助時，都知道可以找到人、找到方法、找到結果。</p>\n'
    '<ul class="rv d2">\n<li>青溪里現任里長、青溪社區發展協會理事長</li>\n<li>台師大 EMBA 進修中</li>\n<li>防災士培訓結業</li>\n'
    '<li>十餘年國小故事媽媽志工經驗</li>\n<li>參與老街溪青埔段水環境公民工作坊</li>\n</ul>\n</div>\n</div>\n'
    + '<div class="wrap facts">\n' + ''.join('<div class="fact rv"><b>%s<small>%s</small></b><span>%s</span></div>\n' % f for f in FACTS) + '</div>\n'
    + '</section>\n'

    # 活動紀錄
    '<section class="acts" id="activities">\n' + edge('edge-dark', EDGE_A, [(412, 45, 2), (866, 47, 1.6), (1260, 44, 2.2)]) + '\n'
    '<div class="a-track"><div class="a-stage">\n<div class="wrap a-head">\n<div>\n'
    '<p class="eyebrow rv">活動紀錄</p>\n<h2 class="h-xl rv d1">最近發生的事。</h2>\n'
    '<a class="link-acc ul rv d2" href="activities.html">看全部活動紀錄　→</a>\n</div>\n'
    '<div class="a-btns">\n'
    '<button class="circle-btn" type="button" data-slide="-1" aria-label="上一則"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg></button>\n'
    '<button class="circle-btn solid" type="button" data-slide="1" aria-label="下一則"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>\n'
    '</div>\n</div>\n'
    '<div class="hs">\n' + home_cards + '</div>\n'
    '<div class="wrap a-barwrap"><div class="track"><div class="a-bar"></div></div></div>\n'
    '</div></div>\n</section>\n'

    # 常用連結
    '<section class="links" id="links">\n<div class="wrap links-grid">\n<div>\n'
    '<p class="eyebrow rv">常用申辦連結</p>\n<h2 class="h-lg rv d1">政府服務，<br>直接前往。</h2>\n'
    '<a class="link-acc ul rv d2" href="life.html">更多生活資訊　→</a>\n</div>\n'
    + link_list('link-list rv d1') + '\n</div>\n</section>\n'

    # 聯絡
    '<section class="contact" id="contact">\n' + edge('edge-paper2', EDGE_B, [(520, 46, 2), (1180, 44, 1.7)]) + '\n'
    '<svg class="grain" aria-hidden="true"><rect width="100%" height="100%" filter="url(#grain)"/></svg>\n'
    '<svg class="deco" viewBox="0 0 1440 700" preserveAspectRatio="none" fill="none" stroke="#E0906A" stroke-width="1.5" stroke-linecap="round" aria-hidden="true">'
    '<path d="M-40 420 C 250 320, 440 540, 740 440 S 1210 320, 1500 460"/><path d="M-40 510 C 270 410, 470 620, 780 520 S 1230 410, 1500 540"/><path d="M-40 600 C 300 500, 500 700, 820 610 S 1250 500, 1500 630"/></svg>\n'
    '<div class="wrap">\n'
    '<p class="eyebrow light rv">找到人、找到方法、找到結果</p>\n'
    '<h2 class="h-xl rv d1">有事，直接找里長。</h2>\n'
    '<a class="fill-t rv" href="' + TEL + '" aria-label="撥打里長電話 ' + PHONE + '">' + PHONE + '</a>\n'
    '<div class="info-grid rv d2">\n'
    '<div><span class="k">里辦公處</span><span class="v">320 桃園市中壢區文昌路225巷28弄19號</span>'
    '<a class="map-link ul" href="' + MAP_URL + '"' + EXT + '>在 Google 地圖中開啟　↗</a></div>\n'
    '<div><span class="k">服務時間</span><span class="v">實際時間請以里辦公處公告為準</span></div>\n'
    '<div><span class="k">社群</span><a class="v ul" href="' + FB + '"' + EXT + '>Facebook：李詠芳　↗</a></div>\n'
    '</div>\n'
    '<div class="map rv"><iframe title="青溪里里辦公處位置" src="' + MAP_EMBED + '" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>\n'
    '<p class="warn-note rv">緊急事件請直接電話聯繫，勿僅透過網路留言。</p>\n'
    '<footer class="site-foot">\n' + FOOT_TEXT + '</footer>\n'
    '</div>\n</section>\n'
)


# ───────────────────────── 最新公告 ─────────────────────────
def news_item(n):
    status, cat, tagcls, tag, date, title, body = n
    badge = {'up': '<span class="tag tag-up">即將舉辦</span>', 'notice': '', 'past': '<span class="done-note">已結束</span>'}[status]
    return ('<article class="news-item rv" data-cat="%s">\n<div>\n<div class="meta"><span class="tag %s">%s</span>%s<span>里辦發布</span></div>\n'
            '<h3>%s</h3>\n<p>%s</p>\n</div>\n<div class="when">%s</div>\n</article>\n' % (cat, tagcls, tag, badge, title, body, date))


def chip_group(target, filters, label, style=''):
    out = '<div class="chips rv" data-filter-group="%s" role="group" aria-label="%s"%s>\n' % (target, label, style)
    for i, (k, t) in enumerate(filters):
        out += '<button class="chip" type="button" data-filter="%s" aria-pressed="%s">%s</button>\n' % (k, 'true' if i == 0 else 'false', t)
    return out + '</div>\n'


def ext_row(src, title, sub, url):
    return ('<a class="row" href="%s"%s><span class="src">%s</span><span><strong>%s</strong><small>%s</small></span>%s</a>\n'
            % (url, EXT, src, title, sub, I_EXT))


NEWS_UP = [n for n in NEWS if n[0] == 'up']
NEWS_REST = [n for n in NEWS if n[0] != 'up']

NEWS_HTML = (
    page_hero('最新公告', ['里內的事，', '先在這裡看到。'],
              '活動報名、消毒與防災提醒、交通改善和里辦說明，都整理在這一頁。最即時的消息，里長也會發在 Facebook 粉絲專頁。')
    + '<section class="page-body">\n<div class="wrap">\n'
    + sub_head('近期', '即將舉辦與進行中')
    + '<div class="up-list">\n' + ''.join(news_item(n) for n in NEWS_UP) + '</div>\n'
    + '<div class="section-gap">\n' + sub_head('全部公告', '里辦公告')
    + chip_group('#news-list', NEWS_FILTERS, '依分類篩選')
    + '<div id="news-list" style="margin-top: 12px;">\n' + ''.join(news_item(n) for n in NEWS_REST) + '</div>\n'
    + '<p class="note-box rv" data-filter-empty hidden style="margin-top: 20px;">' + I_INFO + '<span>這個分類目前沒有公告。</span></p>\n'
    + '<!--\n  新增公告：複製下面這段，貼到 id="news-list" 的最上面，改掉內容即可。\n'
      '  data-cat 可用：event（活動報名）、env（環境衛生）、safety（防災安全）、traffic（交通與設施）\n'
      '  標籤樣式可用：tag-acc、tag-amber、tag-warn、tag-sage、tag-grey\n'
      '<article class="news-item rv" data-cat="event">\n  <div>\n    <div class="meta"><span class="tag tag-acc">活動報名</span><span>里辦發布</span></div>\n'
      '    <h3>公告標題</h3>\n    <p>時間、地點、報名方式。</p>\n  </div>\n  <div class="when">2026/00/00</div>\n</article>\n-->\n'
    + '</div>\n'
    + '<div class="section-gap">\n' + sub_head('停水・停電・政府公告', '政府單位的即時資訊')
    + '<div class="ext-list rv">\n'
    + ext_row('台灣自來水公司', '停水資訊查詢', '用地圖查看目前與預定的停水、降壓範圍。', 'https://web.water.gov.tw/wateroffmap/map')
    + ext_row('台灣電力公司', '停電通報：撥打 1911', '台電 24 小時客服專線，可通報停電或詢問復電時間。', 'tel:1911')
    + ext_row('台灣電力公司', '計畫性工作停電公告', '事先公告的施工停電時間與範圍。', 'https://www.taipower.com.tw/2289/2406/2420/2421/11935/normalPost')
    + ext_row('中壢區公所', '最新消息', '區公所發布的補助、活動與行政公告。', 'https://www.zhongli.tycg.gov.tw/News.aspx?n=5605&sms=10728')
    + '</div>\n'
    + '<div class="panel empty rv" style="margin-top: 28px;">\n<div>\n<h3>追蹤里辦粉絲專頁</h3>\n'
      '<p>「中壢區青溪里里辦公處」會即時發布消毒、防災與活動消息。</p>\n</div>\n'
      '<a class="btn btn-lg btn-ink" href="https://www.facebook.com/profile.php?id=100083187639806"' + EXT + '>前往粉絲專頁　↗</a>\n</div>\n'
    + '</div>\n</div>\n</section>\n'
)


# ───────────────────────── 里務進度 ─────────────────────────
def p_row(p):
    cat, mark, label, title, text, area, when = p
    return ('<article class="p-row row rv" data-cat="%s">\n<span class="mark %s">%s</span>\n'
            '<div><h3>%s</h3><p>%s</p><small>%s</small></div>\n<span class="when">%s</span>\n</article>\n'
            % (cat, mark, label, title, text, area, when))


def tl(label, text):
    return ('<li><span class="dot"><svg width="9" height="9" viewBox="0 0 24 24" fill="none" stroke="#FFFDF8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"/></svg></span>'
            '<b>%s</b><span>%s</span></li>\n' % (label, text))


N_GOING = sum(1 for p in PROG if p[0] == 'going')
N_DONE = sum(1 for p in PROG if p[0] == 'done')
N_URGENT = sum(1 for p in PROG if p[0] == 'urgent')

PROGRESS_HTML = (
    page_hero('里務進度', ['每件事，', '辦到哪了。'],
              '里民反映的問題和里辦推動的工作，依處理狀態公開在這裡：現在進行到哪一步、結果如何，都寫清楚。')
    + '<section class="page-body">\n<div class="wrap">\n'
    '<div class="stats-4">\n'
    '<div class="stat rv"><b style="color: var(--acc);">%d</b><span>持續進行</span></div>\n'
    '<div class="stat rv d1"><b>%d</b><span>已完成</span></div>\n'
    '<div class="stat rv d2"><b style="color: var(--warn);">%d</b><span>緊急應變・已結案</span></div>\n'
    '</div>\n' % (N_GOING, N_DONE, N_URGENT)
    + '<div class="panel case rv">\n<div class="top"><span class="mark mark-going">持續進行・重點項目</span><small>2026/03 起</small></div>\n'
      '<h3>爭取青溪里民活動中心</h3>\n'
      '<p>青溪里一直沒有自己的活動中心。這件事從上任開始推動，已經走到定調階段。</p>\n'
      '<ol class="timeline" style="list-style: none; margin: 0; padding: 0;">\n'
    + tl('發起連署', '上任後第一時間發起連署，讓里民的聲音被看見')
    + tl('向市府表達', '拜會市府，說明青溪里的需求與期待')
    + tl('一樓通過', '今年初會議通過，一樓空間提供里民使用')
    + tl('會勘定調', '3/27 與市府各局處會勘，朝「遊客中心轉型為活動中心示範點」推動')
    + '</ol>\n</div>\n'
    '<div class="section-gap">\n'
    + sub_head('全部項目', '里務一覽')
    + chip_group('#p-list', [('all', '全部'), ('going', '持續進行'), ('done', '已完成'), ('urgent', '緊急應變')], '依狀態篩選')
    + '<div id="p-list" style="margin-top: 20px;">\n' + ''.join(p_row(p) for p in PROG) + '</div>\n</div>\n'
    '<div class="dark-cta rv section-gap">\n<div>\n<h3>有問題要反映？</h3>\n'
    '<p>打電話給里長，說明地點與狀況。里辦會協助處理，或轉給負責的單位並持續追蹤。</p>\n</div>\n'
    '<a class="btn btn-lg btn-fill" href="' + TEL + '">' + I_PHONE + PHONE + '</a>\n</div>\n'
    '</div>\n</section>\n'
)


# ───────────────────────── 服務項目 ─────────────────────────
ICONS = {
    'env': '<path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>',
    'help': '<path d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"/>',
    'com': '<path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>',
    'alert': '<path d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"/>',
}


def svc(icon, title, desc, items):
    rows = ''.join('<div class="tr"><b>%s</b><span>%s</span></div>\n' % it for it in items)
    return ('<section class="svc rv">\n<div class="svc-side">\n'
            '<span class="svc-icon"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg></span>\n'
            '<h2>%s</h2>\n<p>%s</p>\n</div>\n'
            '<div class="svc-table">\n<div class="th"><span>服務內容</span><span>怎麼反映</span></div>\n%s</div>\n</section>\n'
            % (ICONS[icon], title, desc, rows))


SERVICES = (
    page_hero('服務項目', ['這些事，', '都可以找里辦。'],
              '不確定該找誰的時候，先打電話問里長。里辦會幫你確認狀況，說明流程，或轉給負責的單位。')
    + '<section class="page-body">\n<div class="wrap">\n'
    + svc('env', '生活環境', '路燈、道路、排水、公園與環境整潔的問題，里辦受理後會轉給權責單位並持續追蹤。也可以查看區公所的<a class="ul" href="https://www.zhongli.tycg.gov.tw/News_Link.aspx?n=8896&amp;sms=12740"' + EXT + ' style="color: var(--acc); font-weight: 700;">市容查報</a>，或撥 1999 市民專線。',
          [('路燈故障通報', '電話・Facebook'), ('道路／排水／公園問題反映', '電話・Facebook'),
           ('環境整潔與髒亂通報', '電話・Facebook'), ('消毒防疫作業協調', '電話')])
    + svc('help', '里民協助', '社福資訊、長者關懷與急難協助。不確定自己符不符合資格，可以直接問，里辦會協助查詢與轉介。',
          [('社福資訊轉介', '電話・到里辦公處'), ('長者關懷與寒冬送暖', '電話・到里辦公處'),
           ('急難事件即時協助', '直接打電話'), ('行政流程協助說明', '電話・到里辦公處')])
    + svc('com', '社區經營', '節慶活動、課程、球隊與志工招募。想參加或想幫忙，都歡迎直接聯絡里辦。',
          [('節慶活動（元宵、中秋、冬至等）', '看最新公告報名'), ('樂活班、親子活動、手作課程', '看最新公告報名'),
           ('青溪盃慢壘球賽', '電話・Facebook'), ('環保志工招募與出遊', '電話・到里辦公處')])
    + svc('alert', '防災與公告', '防災整備、停水停電通知與緊急事件通報。緊急狀況請直接打電話，不要只留言。',
          [('防災訊息與韌性社區推動', '看最新公告'), ('停水停電通知', '看最新公告'),
           ('政府補助與政策資訊', '看最新公告'), ('火災等緊急事件即時通報', '直接打電話')])
    + '<div class="steps rv">\n<div><p class="eyebrow light" style="font-size: 13px; letter-spacing: .28em;">需要幫忙時</p>'
      '<p class="h" style="margin-top: 8px;">找到人、找到方法、<br>找到結果。</p></div>\n'
      '<div class="s"><span class="n">1</span><span><b>找到人</b><span>來電或透過 Facebook 聯繫里長，快速回應。</span></span></div>\n'
      '<div class="s"><span class="n">2</span><span><b>找到方法</b><span>里辦確認狀況，協助說明流程或轉介權責單位。</span></span></div>\n'
      '<div class="s"><span class="n">3</span><span><b>找到結果</b><span>處理情形公開在里務進度頁，隨時查得到。</span></span></div>\n</div>\n'
    + '</div>\n</section>\n'
)


# ───────────────────────── 生活資訊 ─────────────────────────
def place(title, text, link=''):
    if link == 'MAP':
        link = '<a class="ul" href="' + MAP_URL + '"' + EXT + '>在地圖中開啟　↗</a>\n'
    return '<div class="place rv">\n<h3>%s</h3>\n<p>%s</p>\n%s</div>\n' % (title, text, link)


# ───────── 垃圾車（資料來源：桃園市政府環境管理處垃圾清運路線即時查詢系統，2026/09/23 查詢） ─────────
TRASH_ROWS = ''.join('<div class="tr"><b><span class="stop-no">%s</span>%s</b><span class="t">%s</span></div>\n' % (n, name, t)
                     for n, name, t, la, lo in TRASH_POINTS)
TRASH_JS = '[' + ','.join('[%s,"%s","%s",%.5f,%.5f]' % (n, name, t, la, lo) for n, name, t, la, lo in TRASH_POINTS) + ']'
TRASH_HTML = (
    '<div class="trash rv">\n'
    '<div class="trash-info">\n'
    '<div class="trash-days"><span class="k">一般垃圾</span><b>週一至週六</b><span class="k">資源回收</span><b>週一、二、四、五、六</b><span class="note">週三只收一般垃圾，週日停收</span></div>\n'
    '<div class="svc-table trash-table">\n<div class="th"><span>路三班 第 9 區・清運點</span><span>班表時間</span></div>\n' + TRASH_ROWS + '</div>\n'
    '<p class="trash-note">以上是官方系統標記為「青溪里」的沿街清運點，資源回收與垃圾同一班車收運。大樓社區多由「社區專車」進入社區收運，時間依各社區而定，請洽管委會或用下方系統查詢。</p>\n'
    '<div class="trash-miss"><b>錯過垃圾車？</b><span>中壢區中隊定點收受：華美一路 90 號，週一至週六 07:00–22:00</span></div>\n'
    '<div class="trash-actions">\n'
    '<a class="btn btn-lg btn-ink" href="https://route.tyoem.gov.tw/"' + EXT + '>垃圾車現在在哪　↗</a>\n'
    '<span class="trash-app">手機也可以在 App Store／Google Play 搜尋「桃園垃圾車」</span>\n'
    '</div>\n'
    '<p class="trash-src">資料來源：桃園市政府環境管理處垃圾清運路線即時查詢系統（2026/09/23 查詢）。班表可能調整，實際以官方系統為準；24 小時客服 0800-090-922。</p>\n'
    '</div>\n'
    '<div class="trash-map" id="trash-map" role="img" aria-label="青溪里垃圾車清運點地圖"></div>\n'
    '</div>\n'
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">\n'
    '<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>\n'
    '<script>(function(){var el=document.getElementById("trash-map");if(!el||!window.L)return;'
    'var pts=' + TRASH_JS + ';'
    'var m=L.map(el,{scrollWheelZoom:false,attributionControl:true});'
    'L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png",{maxZoom:19,attribution:"&copy; OpenStreetMap"}).addTo(m);'
    'var line=[];pts.forEach(function(p){line.push([p[3],p[4]]);'
    'L.marker([p[3],p[4]],{icon:L.divIcon({className:"stop-pin",html:"<span>"+p[0]+"</span>",iconSize:[30,30],iconAnchor:[15,15]})})'
    '.addTo(m).bindPopup("<b>"+p[1]+"</b><br>班表時間 "+p[2]+"<br>一般垃圾週一至週六<br>資源回收週三、週日除外");});'
    'L.polyline(line,{color:"#B4633A",weight:3,dashArray:"6 8"}).addTo(m);'
    'var fit=function(){m.invalidateSize();m.fitBounds(line,{padding:[36,36]});};fit();'
    'if(window.ResizeObserver){var w=el.offsetWidth;new ResizeObserver(function(){if(el.offsetWidth!==w){w=el.offsetWidth;fit();}}).observe(el);}'
    '})();</script>\n'
)

LIFE = (
    page_hero('生活資訊', ['住在青溪里，', '你會用到的。'],
              '垃圾車時間、停水停電查詢、里內設施與常用的政府服務，整理在這一頁。')
    + '<section class="page-body">\n<div class="wrap">\n'
    + sub_head('最常被問的', '垃圾車時間與路線')
    + TRASH_HTML
    + '<div class="section-gap">\n' + sub_head('遇到狀況時', '該找誰')
    + '<div class="place-grid">\n'
    + place('青塘園水色異常、泡泡', '發現水色混濁、大量泡泡或可疑排放，請拍照並通報里辦，里辦會通報環保局追查。',
            '<a class="ul" href="' + TEL + '">撥打里辦電話　→</a>\n')
    + place('發現蛇類出沒', '勿靠近草叢，留意孩童與寵物安全，請立即撥打 1999 或通報相關單位處理。',
            '<a class="ul" href="tel:1999">撥打 1999　→</a>\n')
    + place('停水、停電', '停水先查台水停水地圖；停電可撥台電 24 小時專線 1911 通報或詢問。',
            '<a class="ul" href="https://web.water.gov.tw/wateroffmap/map"' + EXT + '>停水地圖　↗</a>\n')
    + place('需要法律諮詢', '中壢區公所免費法律諮詢：每週三、五晚上 6:00–8:30，環北路 380 號 2 樓，免預約、現場排隊。',
            '<a class="ul" href="https://www.zhongli.tycg.gov.tw/News_Content.aspx?n=6381&amp;s=650031"' + EXT + '>區公所說明　↗</a>\n')
    + place('路燈、路樹、公園設施', '可以打電話告訴里長，或查看區公所市容查報，也可以撥 1999 市民專線。',
            '<a class="ul" href="https://www.zhongli.tycg.gov.tw/News_Link.aspx?n=8896&amp;sms=12740"' + EXT + '>區公所市容查報　↗</a>\n')
    + '</div>\n</div>\n'
    + '<div class="section-gap">\n' + sub_head('走出門就會經過', '里內設施與周邊')
    + '<div class="place-grid">\n' + ''.join(place(*p) for p in PLACES) + '</div>\n</div>\n'
    + '<div class="section-gap">\n' + sub_head('交通與申辦', '常用連結') + link_list('link-list small rv') + '\n</div>\n'
    + '</div>\n</section>\n'
)


# ───────────────────────── 活動紀錄 ─────────────────────────
def act(a):
    aid, img, cat, tag, date, title, alt, pos, text = a
    if img:
        ph = '<div class="act-ph"><img src="%s" alt="%s" loading="lazy" style="object-position: %s;"></div>\n' % (img, alt, pos)
        cls = 'act rv'
    else:
        ph = ''
        cls = 'act act-text rv'
    return ('<article class="%s" id="%s" data-cat="%s">\n%s'
            '<div class="act-body">\n<div class="meta"><span class="tag tag-acc">%s</span><time>%s</time></div>\n'
            '<h2>%s</h2>\n<p>%s</p>\n</div>\n</article>\n'
            % (cls, aid, cat, ph, tag, date, title, text))


ACTIVITIES = (
    page_hero('活動紀錄', ['青溪里，', '最近發生的事。'],
              '節慶活動、長者關懷、環保志工、公益講座與社區運動，每一場都是里民一起完成的。')
    + '<section class="page-body">\n<div class="wrap">\n'
    + chip_group('#act-list', ACT_FILTERS, '依類別篩選', ' style="margin-bottom: 64px;"')
    + '<div class="act-list" id="act-list">\n' + ''.join(act(a) for a in ACTS) + '</div>\n'
    + '</div>\n</section>\n'
)


DESC = '桃園市中壢區青溪里里長李詠芳官方服務網站。最新公告、里務進度、服務項目、生活資訊與聯絡方式一站看清楚。'
page('index.html', '青溪里里民服務入口｜里長 李詠芳', DESC, 'home', HOME, foot=False, intro=INTRO)
page('news.html', '最新公告｜青溪里里長辦公室', '青溪里里辦公告、停水停電查詢與政府公告連結。', 'news', NEWS_HTML)
page('progress.html', '里務進度｜青溪里里長辦公室', '青溪里里務與里民反映事項的處理狀態，公開透明。', 'progress', PROGRESS_HTML)
page('services.html', '服務項目｜青溪里里長辦公室', '青溪里里辦公處提供的服務：生活環境、里民協助、社區經營、防災與公告。', 'services', SERVICES)
page('life.html', '生活資訊｜青溪里里長辦公室', '青溪里的垃圾車、停水停電查詢、里內設施與常用政府服務連結。', 'life', LIFE)
page('activities.html', '活動紀錄｜青溪里里長辦公室', '青溪里的節慶活動、長者關懷、環保志工與社區運動紀錄。', 'activities', ACTIVITIES)
