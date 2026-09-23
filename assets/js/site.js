/* 青溪里里長辦公室 — 互動與動態 */
(function () {
  'use strict';

  var doc = document;
  var html = doc.documentElement;
  var anim = html.classList.contains('anim');
  window.QX_READY = true;
  var finePointer = false;
  try { finePointer = window.matchMedia('(pointer: fine)').matches; } catch (e) {}
  var $ = function (s, c) { return (c || doc).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || doc).querySelectorAll(s)); };
  var clamp = function (v, a, b) { return Math.max(a, Math.min(b, v)); };
  var ease = function (x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  var headerH = function () { var h = $('.site-header'); return h ? h.offsetHeight : 64; };

  /* ── 寬螢幕才啟用的釘住場景 ── */
  var isWide = function () { return anim && window.innerWidth >= 900; };
  html.classList.toggle('wide', isWide());

  /* ── 開場印章 ── */
  var intro = $('.intro');
  if (intro) {
    var endIntro = function (skip) {
      intro.classList.add('gone');
      if (skip) { html.classList.add('nointro'); }
    };
    if (html.classList.contains('nointro') || !anim) {
      endIntro(false);
    } else {
      window.setTimeout(function () { endIntro(false); }, 2350);
      intro.addEventListener('click', function () { endIntro(true); });
    }
  }

  /* ── 手機選單 ── */
  var menuBtn = $('.menu-btn');
  var menu = $('.mobile-menu');
  if (menuBtn && menu) {
    var setMenu = function (open) {
      html.classList.toggle('menu-open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
      menuBtn.setAttribute('aria-label', open ? '關閉選單' : '開啟選單');
      menu.setAttribute('aria-hidden', open ? 'false' : 'true');
      if (open) { menu.removeAttribute('inert'); } else { menu.setAttribute('inert', ''); }
    };
    setMenu(false);
    menuBtn.addEventListener('click', function () { setMenu(!html.classList.contains('menu-open')); });
    $$('a', menu).forEach(function (a) { a.addEventListener('click', function () { setMenu(false); }); });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && html.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth >= 900) { setMenu(false); } });
  }

  /* ── 捲動顯現 ── */
  if (anim && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    $$('.rv').forEach(function (el) { io.observe(el); });
  } else {
    $$('.rv').forEach(function (el) { el.classList.add('in'); });
  }

  /* ── 篩選按鈕（公告、里務進度） ── */
  $$('[data-filter-group]').forEach(function (group) {
    var chips = $$('[data-filter]', group);
    var target = $(group.getAttribute('data-filter-group'));
    if (!target) { return; }
    var items = $$('[data-cat]', target);
    var empty = $('[data-filter-empty]', target.parentNode);
    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        var f = chip.getAttribute('data-filter');
        chips.forEach(function (c) { c.setAttribute('aria-pressed', c === chip ? 'true' : 'false'); });
        var shown = 0;
        items.forEach(function (it) {
          var ok = f === 'all' || (' ' + it.getAttribute('data-cat') + ' ').indexOf(' ' + f + ' ') > -1;
          it.hidden = !ok;
          if (ok) { shown += 1; it.classList.add('in'); }
        });
        if (empty) { empty.hidden = shown > 0; }
      });
    });
  });

  /* ── 活動照片左右鍵（沒有釘住時使用） ── */
  var hs = $('.hs');
  $$('[data-slide]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (hs) { hs.scrollBy({ left: parseInt(b.getAttribute('data-slide'), 10) * 424, behavior: 'smooth' }); }
    });
  });

  /* ── 主視覺墨流 ── */
  var hero = $('.hero');
  var cv = $('.flow-cv');
  var flow = null;
  if (hero && cv && cv.getContext) {
    flow = {
      ctx: null, w: 0, h: 0, ps: [], on: true,
      mouse: { x: -9999, y: -9999 },
      cols: ['rgba(224,144,106,0.62)', 'rgba(224,144,106,0.3)', 'rgba(242,237,227,0.42)', 'rgba(242,237,227,0.2)'],
      size: function () {
        var w = hero.clientWidth, h = hero.clientHeight;
        var dpr = Math.min(window.devicePixelRatio || 1, 2);
        cv.width = Math.round(w * dpr);
        cv.height = Math.round(h * dpr);
        this.w = w; this.h = h;
        this.ctx = cv.getContext('2d');
        this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
        this.ctx.fillStyle = '#1C1815';
        this.ctx.fillRect(0, 0, w, h);
        var n = Math.round(clamp(w * (w < 900 ? 0.4 : 0.55), 120, 900));
        this.ps = [];
        for (var i = 0; i < n; i++) {
          var r = Math.random();
          this.ps.push({
            x: Math.random() * w,
            lane: Math.floor(Math.random() * 5),
            off: (Math.random() - 0.5) * 2,
            sp: 0.5 + Math.random() * 1.3,
            g: r < 0.375 ? 0 : r < 0.75 ? 1 : r < 0.875 ? 2 : 3,
            px: null, py: null
          });
        }
      },
      step: function (t) {
        var ctx = this.ctx;
        if (!ctx) { return; }
        var w = this.w, h = this.h, time = t * 0.001;
        var narrow = w < 900;
        ctx.fillStyle = 'rgba(28,24,21,0.085)';
        ctx.fillRect(0, 0, w, h);
        ctx.lineWidth = 1.15;
        ctx.lineCap = 'round';
        var mx = this.mouse.x, my = this.mouse.y;
        for (var g = 0; g < 4; g++) {
          ctx.strokeStyle = this.cols[g];
          ctx.beginPath();
          for (var i = 0; i < this.ps.length; i++) {
            var p = this.ps[i];
            if (p.g !== g) { continue; }
            var base = h * ((narrow ? 0.66 : 0.56) + p.lane * (narrow ? 0.05 : 0.07));
            var amp = (narrow ? 22 : 38) + p.lane * (narrow ? 5 : 8);
            var y = base + Math.sin(p.x * 0.0042 + time * 0.55 + p.lane * 1.7) * amp +
              Math.sin(p.x * 0.011 - time * 0.9 + p.lane) * 10 + p.off * 16;
            var dx = p.x - mx, dy = y - my, d2 = dx * dx + dy * dy;
            if (d2 < 25600) { y += (dy >= 0 ? 1 : -1) * (1 - Math.sqrt(d2) / 160) * 70; }
            if (p.px !== null) { ctx.moveTo(p.px, p.py); ctx.lineTo(p.x, y); }
            p.px = p.x; p.py = y;
            p.x += p.sp * 1.5;
            if (p.x > w + 20) { p.x = -20; p.px = null; }
          }
          ctx.stroke();
        }
      }
    };
    flow.size();
    if (!anim) {
      for (var k = 0; k < 170; k++) { flow.step(k * 16); }
    } else if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) { flow.on = es[0].isIntersecting; }).observe(hero);
    }
  }

  if (!anim) { return; }

  /* ── 以下都是動態效果 ── */
  var progEl = $('.prog');
  var qTrack = $('.q-track'), qStage = $('.q-stage'), qc = $$('.qc'), qCap = $('.q-cap'), qLit = -1;
  var mTrack = $('.m-track'), mStage = $('.m-stage'), mGrid = $('.m-grid'), mPh = $$('.m-ph'), mCap = $('.m-cap');
  var aTrack = $('.a-track'), aStage = $('.a-stage'), aBar = $('.a-bar');
  var mqWrap = $('.mq-wrap');
  var px = $$('.px');
  var wide = isWide();
  var mStart = 3, mEnd = 1, aShift = 0;
  var tx = 0, ty = 0, mx = 0, my = 0, skew = 0, lastY = null;
  var dirty = true;

  function pg(track, stage) {
    if (!track || !stage) { return 0; }
    var r = track.getBoundingClientRect();
    var total = r.height - stage.offsetHeight;
    if (total <= 0) { return 0; }
    return clamp((headerH() - r.top) / total, 0, 1);
  }

  function clearPins() {
    if (mGrid) { mGrid.style.transform = ''; }
    mPh.forEach(function (el) { el.style.opacity = ''; });
    if (mCap) { mCap.style.opacity = ''; }
    if (hs) { hs.style.transform = ''; }
    if (aTrack) { aTrack.style.height = ''; }
  }

  function measure() {
    wide = isWide();
    html.classList.toggle('wide', wide);
    if (!wide) { clearPins(); return; }
    if (aTrack && aStage && hs) {
      hs.style.transform = '';
      aShift = Math.max(0, hs.scrollWidth - aStage.clientWidth + 40);
      aTrack.style.height = (aStage.offsetHeight + aShift) + 'px';
    }
    if (mStage) {
      var sw = mStage.clientWidth, sh = mStage.clientHeight;
      mEnd = Math.min(1, (sh - 110) / 700, (sw - 80) / 1060);
      mStart = Math.min(sw / 344, sh / 224) * 0.9;
    }
  }

  function update() {
    var y = window.pageYOffset || html.scrollTop;
    var vh = window.innerHeight;
    if (progEl) {
      var den = html.scrollHeight - vh;
      progEl.style.transform = 'scaleX(' + (den > 0 ? clamp(y / den, 0, 1) : 0).toFixed(4) + ')';
    }
    if (qc.length) {
      var qp = pg(qTrack, qStage);
      var n = Math.round(Math.min(1, qp * 1.3) * qc.length);
      if (n !== qLit) {
        for (var i = 0; i < qc.length; i++) { qc[i].classList.toggle('on', i < n); }
        qLit = n;
      }
      if (qCap) { qCap.style.opacity = qp > 0.8 ? '1' : '0'; }
    }
    if (wide && mGrid) {
      var mp = pg(mTrack, mStage);
      var s = mStart + (mEnd - mStart) * ease(Math.min(1, mp * 1.3));
      mGrid.style.transform = 'translate(-50%, -50%) scale(' + s.toFixed(4) + ')';
      for (var j = 0; j < mPh.length; j++) {
        mPh[j].style.opacity = clamp((mp - 0.1 - j * 0.035) / 0.34, 0, 1).toFixed(3);
      }
      if (mCap) { mCap.style.opacity = mp > 0.82 ? '1' : '0'; }
    }
    if (wide && hs && aShift) {
      var ap = pg(aTrack, aStage);
      hs.style.transform = 'translate3d(' + (-ap * aShift).toFixed(1) + 'px,0,0)';
      if (aBar) { aBar.style.transform = 'scaleX(' + ap.toFixed(4) + ')'; }
    }
  }

  function frame(t) {
    var i;
    mx += (tx - mx) * 0.06;
    my += (ty - my) * 0.06;
    for (i = 0; i < px.length; i++) {
      var d = parseFloat(px[i].getAttribute('data-d')) || 10;
      px[i].style.transform = 'translate3d(' + (mx * d).toFixed(2) + 'px,' + (my * d).toFixed(2) + 'px,0)';
    }
    if (flow && flow.on) { flow.step(t); }
    var y = window.pageYOffset || html.scrollTop;
    if (lastY === null) { lastY = y; }
    skew += (clamp((y - lastY) * 0.3, -9, 9) - skew) * 0.12;
    lastY = y;
    if (mqWrap) { mqWrap.style.transform = 'skewX(' + (-skew).toFixed(2) + 'deg)'; }
    if (dirty) { dirty = false; update(); }
    window.requestAnimationFrame(frame);
  }

  measure();
  update();
  window.addEventListener('scroll', function () { dirty = true; }, { passive: true });
  var rz;
  window.addEventListener('resize', function () {
    window.clearTimeout(rz);
    rz = window.setTimeout(function () { if (flow) { flow.size(); } measure(); dirty = true; }, 150);
  });
  window.addEventListener('load', function () { measure(); dirty = true; });
  window.requestAnimationFrame(frame);

  /* ── 滑鼠：景深、傾斜光澤、磁吸按鈕 ── */
  if (!finePointer) { return; }
  var tiltEl = null, magEl = null;
  function resetTilt() {
    if (tiltEl) {
      tiltEl.style.transition = 'transform .7s cubic-bezier(.16,.84,.24,1)';
      tiltEl.style.transform = '';
      tiltEl = null;
    }
  }
  function resetMag() { if (magEl) { magEl.style.transform = ''; magEl = null; } }
  doc.addEventListener('mousemove', function (e) {
    tx = (e.clientX / window.innerWidth - 0.5) * 2;
    ty = (e.clientY / Math.min(window.innerHeight, 1000) - 0.5) * 2;
    if (flow) {
      var r = hero.getBoundingClientRect();
      flow.mouse.x = e.clientX - r.left;
      flow.mouse.y = e.clientY - r.top;
    }
    var t = e.target && e.target.closest ? e.target : null;
    var tl = t ? t.closest('.tilt') : null;
    if (tl !== tiltEl) { resetTilt(); tiltEl = tl; }
    if (tl) {
      var b = tl.getBoundingClientRect();
      var x = (e.clientX - b.left) / b.width, yy = (e.clientY - b.top) / b.height;
      tl.style.transition = 'transform .25s ease-out';
      tl.style.transform = 'perspective(1100px) rotateX(' + ((0.5 - yy) * 7).toFixed(2) + 'deg) rotateY(' + ((x - 0.5) * 9).toFixed(2) + 'deg)';
      tl.style.setProperty('--gx', (x * 100).toFixed(1) + '%');
      tl.style.setProperty('--gy', (yy * 100).toFixed(1) + '%');
    }
    var mg = t ? t.closest('.mag') : null;
    if (mg !== magEl) { resetMag(); magEl = mg; }
    if (mg) {
      var m = mg.getBoundingClientRect();
      mg.style.transform = 'translate(' + ((e.clientX - m.left - m.width / 2) * 0.22).toFixed(1) + 'px,' +
        ((e.clientY - m.top - m.height / 2) * 0.3).toFixed(1) + 'px) scale(1.04)';
    }
  });
  html.addEventListener('mouseleave', function () {
    tx = 0; ty = 0;
    if (flow) { flow.mouse.x = -9999; }
    resetTilt(); resetMag();
  });
})();
