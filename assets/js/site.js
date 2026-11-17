/* Baby Panda Treks: motion and progressive enhancement.
   Everything here is optional; the pages are complete without it.
   Motion uses one tiny spring engine (damping ratio + response, Apple-style),
   so every animation starts from the current value and can be interrupted. */
(() => {
  const doc = document.documentElement;
  const reduceMQ = matchMedia('(prefers-reduced-motion: reduce)');
  let reduce = reduceMQ.matches;
  reduceMQ.addEventListener?.('change', (e) => { reduce = e.matches; });
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

  /* ---------- spring engine ---------- */
  // damping 1 = no overshoot; response = seconds to (mostly) settle.
  class Spring {
    constructor(value = 0, { damping = 1, response = 0.4 } = {}) {
      this.value = value; this.target = value; this.velocity = 0;
      this.set(damping, response);
    }
    set(damping, response) {
      this.k = Math.pow((2 * Math.PI) / response, 2);
      this.c = (4 * Math.PI * damping) / response;
    }
    to(t) { this.target = t; wake(); return this; }
    jump(v) { this.value = this.target = v; this.velocity = 0; return this; }
    step(dt) {
      const f = -this.k * (this.value - this.target) - this.c * this.velocity;
      this.velocity += f * dt;
      this.value += this.velocity * dt;
    }
    get settled() { return Math.abs(this.velocity) < 0.001 && Math.abs(this.value - this.target) < 0.001; }
  }
  const springs = new Set();
  const renderers = new Set();
  let running = false, last = 0;
  const spring = (v, o) => { const s = new Spring(v, o); springs.add(s); return s; };
  function wake() { if (!running) { running = true; last = performance.now(); requestAnimationFrame(tick); } }
  function tick(now) {
    let dt = Math.min(0.064, (now - last) / 1000); last = now;
    const n = Math.ceil(dt / 0.008); dt /= n; // sub-steps keep stiff springs stable
    let busy = false;
    for (const s of springs) {
      if (s.settled) { s.value = s.target; s.velocity = 0; continue; }
      for (let i = 0; i < n; i++) s.step(dt);
      busy = true;
    }
    for (const r of renderers) r();
    if (busy) requestAnimationFrame(tick); else running = false;
  }
  // Scroll-linked work runs on the frame clock, not the scroll event.
  const scrollJobs = new Set();
  let scrollQueued = false;
  const onScrollFrame = () => { scrollQueued = false; for (const j of scrollJobs) j(); };
  const queueScroll = () => { if (!scrollQueued) { scrollQueued = true; requestAnimationFrame(onScrollFrame); } };
  addEventListener('scroll', queueScroll, { passive: true });
  addEventListener('resize', queueScroll);
  // 0 when el's top hits the bottom of the viewport, 1 when its bottom hits the top
  const progressThrough = (el) => {
    const r = el.getBoundingClientRect();
    return clamp((innerHeight - r.top) / (innerHeight + r.height), 0, 1);
  };

  /* ---------- nav material ---------- */
  const nav = document.querySelector('[data-nav]');
  if (nav) {
    const hero = document.querySelector('[data-hero]');
    const job = () => {
      const over = hero ? hero.getBoundingClientRect().bottom > 64 : false;
      nav.classList.toggle('scrolled', scrollY > 8);
      nav.classList.toggle('on-dark', over);
    };
    scrollJobs.add(job); job();
  }

  /* ---------- hero: parallax ridges + a trail that draws itself ---------- */
  const hero = document.querySelector('[data-hero]');
  if (hero) {
    const layers = [...hero.querySelectorAll('.scene [data-depth]')].map((g) => ({ g, d: +g.dataset.depth }));
    const px = spring(0, { damping: 1, response: 0.9 });
    const py = spring(0, { damping: 1, response: 0.9 });
    let scrollShift = 0;
    const render = () => {
      for (const { g, d } of layers) {
        g.setAttribute('transform', `translate(${(px.value * d * 28).toFixed(2)} ${(py.value * d * 14 + scrollShift * (1 - d) * -0.35).toFixed(2)})`);
      }
    };
    renderers.add(render);
    if (!reduce && finePointer) {
      hero.addEventListener('pointermove', (e) => {
        const r = hero.getBoundingClientRect();
        px.to(((e.clientX - r.left) / r.width - 0.5) * -2);
        py.to(((e.clientY - r.top) / r.height - 0.5) * -2);
      });
      hero.addEventListener('pointerleave', () => { px.to(0); py.to(0); });
    }
    if (!reduce) {
      scrollJobs.add(() => {
        const r = hero.getBoundingClientRect();
        if (r.bottom < 0) return;
        scrollShift = clamp(-r.top, 0, r.height);
        render();
      });
    }

    // Sunrise: the sun climbs from behind the ridge, night fades, stars go out.
    const sun = hero.querySelector('[data-sun]');
    const night = hero.querySelector('[data-night]');
    const stars = hero.querySelector('[data-stars]');
    const rise = spring(reduce ? 1 : 0, { damping: 1, response: 3.2 });
    renderers.add(() => {
      const r = clamp(rise.value, 0, 1);
      sun.setAttribute('transform', `translate(0 ${(260 * (1 - r)).toFixed(1)})`);
      night.setAttribute('opacity', (1 - r * 0.97).toFixed(3));
      stars.setAttribute('opacity', clamp(1 - r * 1.4, 0, 1).toFixed(3));
    });

    // Trail: the mask path draws, the panda rides the leading edge, the flag is planted at the summit.
    const draw = hero.querySelector('[data-trail-draw]');
    const walker = hero.querySelector('[data-trail-walker]');
    const flag = hero.querySelector('[data-trail-flag]');
    if (draw && walker) {
      const L = draw.getTotalLength();
      draw.style.strokeDasharray = `${L} ${L}`;
      const prog = spring(reduce ? 1 : 0, { damping: 1, response: reduce ? 0.01 : 3.4 });
      const flagS = spring(reduce ? 1 : 0, { damping: 0.7, response: 0.5 }); // a little bounce: the flag is planted
      let planted = reduce;
      renderers.add(() => {
        const p = clamp(prog.value, 0, 1);
        draw.style.strokeDashoffset = (L * (1 - p)).toFixed(1);
        const pt = draw.getPointAtLength(L * p);
        // bob a little as it walks
        const bob = Math.sin(p * 60) * 2.2 * (1 - p * p);
        walker.setAttribute('transform', `translate(${pt.x.toFixed(1)} ${(pt.y - 22 + bob).toFixed(1)})`);
        if (p > 0.985 && !planted) { planted = true; flagS.to(1); }
        const f = flagS.value;
        flag.setAttribute('opacity', clamp(f, 0, 1).toFixed(2));
        flag.setAttribute('transform', `translate(1050 420) scale(${clamp(f, 0, 1.3).toFixed(3)})`);
      });
      if (!reduce) {
        setTimeout(() => rise.to(1), 250);
        setTimeout(() => prog.to(1), 1300);
      }
    }

    // "We've walked to …": cycle through every place we've been.
    const rot = hero.querySelector('[data-rot]');
    if (rot && !reduce) {
      const names = JSON.parse(rot.dataset.rot);
      let i = 0;
      const w = spring(rot.offsetWidth, { damping: 1, response: 0.45 });
      renderers.add(() => { rot.style.width = w.value.toFixed(1) + 'px'; });
      const measure = (el) => { el.style.position = 'absolute'; const x = el.offsetWidth; el.style.position = ''; return x; };
      let paused = false;
      rot.closest('.hero-rot').addEventListener('pointerenter', () => { paused = true; });
      rot.closest('.hero-rot').addEventListener('pointerleave', () => { paused = false; });
      setInterval(() => {
        if (paused || document.hidden) return;
        i = (i + 1) % names.length;
        const old = rot.querySelector('.rot-word:not(.out)');
        const nu = document.createElement('span');
        nu.className = 'rot-word in';
        nu.textContent = names[i];
        rot.append(nu);
        w.to(measure(nu));
        requestAnimationFrame(() => { nu.classList.remove('in'); old.classList.add('out'); });
        setTimeout(() => old.remove(), 700);
      }, 2600);
    }
    if (!reduce) doc.classList.add('motion');
  }

  /* ---------- crew: pinned scene; scroll lifts the fog, pulls the camera back, tells the story ---------- */
  const crew = document.querySelector('[data-crew]');
  if (crew && !reduce) {
    const stick = crew.querySelector('.crew-stick');
    const world = crew.querySelector('[data-crew-world]');
    const fogs = [...crew.querySelectorAll('[data-fog]')].map((el) => ({ el, k: +el.dataset.fog }));
    const beats = [...crew.querySelectorAll('[data-beat]')];
    const steps = [...crew.querySelectorAll('[data-step]')];
    const smooth = (a, b, x) => { const t = clamp((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); };
    // Scroll progress is smoothed by a critically damped spring so wheel steps glide.
    const prog = spring(0, { damping: 1, response: 0.35 });
    // Mist drifts toward the pointer: independent X and Y springs.
    const mx = spring(0, { damping: 1, response: 1.2 });
    const my = spring(0, { damping: 1, response: 1.2 });
    // Beat windows: [fade in start, fully in, fade out start, gone]
    const W = [[0.0, 0.04, 0.2, 0.27], [0.27, 0.33, 0.47, 0.53], [0.53, 0.59, 0.7, 0.76], [0.8, 0.88, 2, 2]];
    renderers.add(() => {
      const p = clamp(prog.value, 0, 1);
      const clear = smooth(0.05, 0.78, p);             // fog lifting
      world.style.setProperty('--z', (1.35 - 0.35 * smooth(0, 0.85, p)).toFixed(4));
      world.style.setProperty('--blur', (1 - smooth(0.12, 0.7, p)).toFixed(3));
      world.style.setProperty('--bright', (0.55 + 0.45 * smooth(0.3, 0.85, p)).toFixed(3));
      stick.style.setProperty('--light', smooth(0.45, 0.9, p).toFixed(3));
      fogs.forEach(({ el, k }, i) => {
        const spread = clear * 38 * Math.sign(k) * (1 + i * 0.25);   // fog parts to the sides
        el.style.transform = `translate3d(${(spread + mx.value * k * 3).toFixed(2)}vw, ${(my.value * k * 1.5 - clear * 6).toFixed(2)}vh, 0)`;
        el.style.opacity = (1 - clear * 0.96).toFixed(3);
      });
      beats.forEach((el, i) => {
        const [a0, a1, b0, b1] = W[i];
        const o = smooth(a0, a1, p) * (1 - smooth(b0, b1, p));
        el.style.opacity = o.toFixed(3);
        el.style.transform = `translateY(${((1 - smooth(a0, a1, p)) * 24 - smooth(b0, b1, p) * 24).toFixed(1)}px)`;
        el.style.pointerEvents = o > 0.5 ? 'auto' : 'none';
        el.setAttribute('aria-hidden', o > 0.5 ? 'false' : 'true');
      });
      const active = W.reduce((acc, w, i) => (p >= w[0] ? i : acc), 0);
      steps.forEach((li, i) => li.classList.toggle('on', i === active));
    });
    const job = () => {
      const r = crew.getBoundingClientRect();
      const span = r.height - innerHeight;
      prog.to(clamp(-r.top / Math.max(1, span), 0, 1));
    };
    scrollJobs.add(job); job();
    prog.jump(prog.target); wake();
    if (finePointer) {
      stick.addEventListener('pointermove', (e) => {
        mx.to((e.clientX / innerWidth - 0.5) * 2);
        my.to((e.clientY / innerHeight - 0.5) * 2);
      });
      stick.addEventListener('pointerleave', () => { mx.to(0); my.to(0); });
    }
  } else if (crew) {
    crew.querySelectorAll('[data-beat]').forEach((el) => { el.style.opacity = 1; });
  }

  /* ---------- reveal on scroll (only things below the fold, so nothing flashes) ---------- */
  const io = 'IntersectionObserver' in window && !reduce
    ? new IntersectionObserver((entries) => {
        for (const en of entries) if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
      }, { rootMargin: '0px 0px -10% 0px' })
    : null;
  if (io) {
    doc.classList.add('js');
    let row = 0, lastTop = null;
    document.querySelectorAll('.card, .steps li, .faq details, .feats li, .map-wrap, .section-head, .profile, .stats div').forEach((el) => {
      const top = el.getBoundingClientRect().top;
      if (top <= innerHeight) return;
      row = top === lastTop ? row + 1 : 0; lastTop = top;
      el.style.setProperty('--stagger', `${Math.min(row, 4) * 70}ms`);
      el.classList.add('reveal'); io.observe(el);
    });
  }

  /* ---------- stats: count up with a spring when they arrive ---------- */
  const counts = [...document.querySelectorAll('[data-count]')];
  if (counts.length && 'IntersectionObserver' in window && !reduce) {
    const cio = new IntersectionObserver((ents) => {
      ents.forEach((en) => {
        if (!en.isIntersecting) return;
        cio.unobserve(en.target);
        const el = en.target, end = +el.dataset.count;
        const s = spring(0, { damping: 1, response: 1.1 });
        const r = () => { el.textContent = Math.round(s.value); };
        renderers.add(r); s.to(end);
      });
    }, { threshold: 0.6 });
    counts.forEach((el) => { el.textContent = '0'; cio.observe(el); });
  }

  /* ---------- trek cards: tilt toward the pointer, ridges shift in depth ---------- */
  if (finePointer && !reduce) {
    document.querySelectorAll('.card > a').forEach((a) => {
      const rx = spring(0, { damping: 1, response: 0.45 });
      const ry = spring(0, { damping: 1, response: 0.45 });
      const lift = spring(0, { damping: 1, response: 0.35 });
      const groups = [...a.querySelectorAll('.card-art [data-depth]')].map((g) => ({ g, d: +g.dataset.depth }));
      a.classList.add('tilt');
      const render = () => {
        if (lift.settled && Math.abs(lift.value) < 0.001 && rx.settled && ry.settled && !a.matches(':hover')) {
          a.style.transform = ''; return;
        }
        a.style.transform = `perspective(900px) translateY(${(-6 * lift.value).toFixed(2)}px) rotateX(${rx.value.toFixed(3)}deg) rotateY(${ry.value.toFixed(3)}deg)`;
        a.style.boxShadow = lift.value > 0.01 ? `0 2px 4px rgba(31,27,22,${(.08 * lift.value).toFixed(3)}), 0 ${(8 + 14 * lift.value).toFixed(1)}px ${(24 + 20 * lift.value).toFixed(1)}px rgba(31,27,22,${(.08 + .08 * lift.value).toFixed(3)})` : '';
        for (const { g, d } of groups) g.setAttribute('transform', `translate(${(ry.value * d * 1.6).toFixed(2)} ${(-rx.value * d * 1.2).toFixed(2)})`);
      };
      renderers.add(render);
      a.addEventListener('pointerenter', () => lift.to(1));
      a.addEventListener('pointermove', (e) => {
        const r = a.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5;
        const y = (e.clientY - r.top) / r.height - 0.5;
        ry.to(x * 7); rx.to(-y * 6); // independent X and Y springs
      });
      a.addEventListener('pointerleave', () => { rx.to(0); ry.to(0); lift.to(0); });
      a.addEventListener('pointerdown', () => lift.to(0.4)); // press feedback on pointer-down
      a.addEventListener('pointerup', () => lift.to(1));
    });
  }

  /* ---------- segmented filter: the pill is a spring, so rapid taps redirect it mid-flight ---------- */
  const seg = document.querySelector('[data-seg]');
  const grid = document.querySelector('[data-grid]');
  if (seg && grid) {
    const pill = seg.querySelector('.seg-pill');
    const buttons = [...seg.querySelectorAll('button')];
    const sx = spring(0, { damping: 1, response: 0.35 });
    const sw = spring(0, { damping: 1, response: 0.35 });
    renderers.add(() => { pill.style.width = sw.value + 'px'; pill.style.transform = `translateX(${sx.value}px)`; });
    const place = (btn, instant) => {
      if (instant || reduce) { sx.jump(btn.offsetLeft); sw.jump(btn.offsetWidth); wake(); }
      else { sx.to(btn.offsetLeft); sw.to(btn.offsetWidth); }
    };
    let current = buttons.find((b) => b.getAttribute('aria-selected') === 'true');
    // Home page shows the first N of each filter; "View more" opens the rest in place.
    const limit = +grid.dataset.limit || Infinity;
    const moreRow = grid.parentElement.querySelector('[data-more-row]');
    const moreBtn = moreRow?.querySelector('[data-more]');
    const moreLabel = moreRow?.querySelector('[data-more-label]');
    const expanded = {};
    const rangeName = (f) => buttons.find((b) => b.dataset.filter === f).firstChild.textContent.trim();
    const apply = (animate) => {
      const f = current.dataset.filter;
      const open = !!expanded[f];
      let match = 0, k = 0;
      grid.querySelectorAll('.card').forEach((c) => {
        const inRange = f === 'all' || c.dataset.range === f;
        const show = inRange && (open || match < limit);
        if (inRange) match++;
        if (show && c.hidden) {
          c.hidden = false;
          if (animate && !reduce) { c.classList.remove('in', 'pop'); c.style.setProperty('--stagger', `${Math.min(k, 6) * 45}ms`); void c.offsetWidth; c.classList.add('pop'); }
        } else if (!show) c.hidden = true;
        if (show) { c.classList.add('in'); k++; }
      });
      if (moreRow) {
        const extra = match - limit;
        moreRow.hidden = extra <= 0;
        if (extra > 0) {
          moreBtn.setAttribute('aria-expanded', String(open));
          moreLabel.textContent = open ? 'Show fewer' : (f === 'all' ? `View ${extra} more treks` : `View ${extra} more in the ${rangeName(f)}`);
          moreBtn.setAttribute('href', moreBtn.getAttribute('href').split('#')[0] + (f === 'all' ? '' : '#' + f));
        }
      }
    };
    if (moreBtn) {
      moreBtn.setAttribute('role', 'button');
      moreBtn.addEventListener('click', (e) => {
        e.preventDefault();
        const f = current.dataset.filter;
        expanded[f] = !expanded[f];
        apply(true);
        // Collapsing: bring the button back into view so the page doesn't jump away from it
        if (!expanded[f]) moreRow.scrollIntoView({ block: 'nearest', behavior: reduce ? 'auto' : 'smooth' });
      });
    }
    const select = (btn, focus) => {
      if (btn === current) return;
      current = btn;
      buttons.forEach((b) => { b.setAttribute('aria-selected', String(b === btn)); b.tabIndex = b === btn ? 0 : -1; });
      place(btn);
      if (focus) btn.focus();
      apply(true);
    };
    // /treks/#sahyadris opens on that range (the home page's no-JS "View more" link lands here)
    const fromHash = buttons.find((b) => b.dataset.filter === location.hash.slice(1));
    if (fromHash && fromHash !== current) {
      current = fromHash;
      buttons.forEach((b) => { b.setAttribute('aria-selected', String(b === fromHash)); b.tabIndex = b === fromHash ? 0 : -1; });
    }
    apply(false);
    buttons.forEach((b) => {
      b.addEventListener('pointerdown', (e) => { if (e.button === 0) select(b); }); // respond on press
      b.addEventListener('click', () => select(b));
    });
    seg.addEventListener('keydown', (e) => {
      const i = buttons.indexOf(current);
      const d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
      if (d) { e.preventDefault(); select(buttons[(i + d + buttons.length) % buttons.length], true); }
    });
    const init = () => place(current, true);
    init();
    addEventListener('resize', init);
    document.fonts?.ready.then(init);
  }

  /* ---------- Thadam: phones fan out as the section scrolls in ---------- */
  const phones = document.querySelector('[data-phones]');
  if (phones && !reduce) {
    const [p1, p2, p3] = phones.querySelectorAll('.phone');
    const job = () => {
      const p = clamp((progressThrough(phones) - 0.12) / 0.4, 0, 1);
      const e = 1 - Math.pow(1 - p, 3);
      phones.style.setProperty('--fan', e.toFixed(4));
    };
    scrollJobs.add(job); job();
  }

  /* ---------- Thadam: elevation profile scrubs with scroll ---------- */
  const prof = document.querySelector('[data-profile]');
  if (prof) {
    const data = JSON.parse(prof.dataset.profile);
    const pts = data.pts, total = pts[pts.length - 1][0];
    const clip = prof.querySelector('[data-p-clip]');
    const dot = prof.querySelector('[data-p-dot]');
    const cur = prof.querySelector('[data-p-cursor]');
    const km = prof.querySelector('[data-p-km]');
    const ele = prof.querySelector('[data-p-ele]');
    const plot = prof.querySelector('.profile-plot');
    const s = spring(0, { damping: 1, response: 0.5 }); // smooths scroll jitter, still tracks closely
    const eleAt = (d) => {
      let i = 1; while (i < pts.length - 1 && pts[i][0] < d) i++;
      const [a0, e0] = pts[i - 1], [a1, e1] = pts[i];
      return e0 + (e1 - e0) * ((d - a0) / Math.max(1, a1 - a0));
    };
    renderers.add(() => {
      const p = clamp(s.value, 0, 1);
      const d = p * total, el = eleAt(d);
      clip.setAttribute('width', (p * 1000).toFixed(1));
      const w = plot.clientWidth, h = plot.clientHeight;
      const y = (1 - (el - data.y0) / (data.y1 - data.y0) * ((data.H - 20) / data.H)) * h;
      dot.style.transform = `translate(${(p * w).toFixed(1)}px, ${y.toFixed(1)}px)`;
      cur.style.transform = `translateX(${(p * w).toFixed(1)}px)`;
      km.textContent = (d / 1000).toFixed(2);
      ele.textContent = Math.round(el).toLocaleString('en-IN');
    });
    if (reduce) { s.jump(1); wake(); }
    else {
      const job = () => s.to(clamp((progressThrough(prof) - 0.18) / 0.5, 0, 1));
      scrollJobs.add(job); job();
    }
  }

  /* ---------- trek post: parallax header + reading progress ---------- */
  const postHero = document.querySelector('[data-post-hero]');
  if (postHero && !reduce) {
    const groups = [...postHero.querySelectorAll('[data-depth]')].map((g) => ({ g, d: +g.dataset.depth }));
    const title = postHero.querySelector('.post-title');
    scrollJobs.add(() => {
      const y = scrollY;
      if (y > postHero.offsetHeight + 200) return;
      for (const { g, d } of groups) g.setAttribute('transform', `translate(0 ${(y * (1 - d) * 0.18).toFixed(2)})`);
      title.style.transform = `translateY(${(y * 0.25).toFixed(1)}px)`;
      title.style.opacity = clamp(1 - y / (postHero.offsetHeight * 0.8), 0, 1).toFixed(3);
    });
  }
  const bar = document.querySelector('[data-progress]');
  if (bar) {
    const art = document.querySelector('article');
    scrollJobs.add(() => {
      const r = art.getBoundingClientRect();
      const p = clamp(-r.top / Math.max(1, r.height - innerHeight), 0, 1);
      bar.style.transform = `scaleX(${p.toFixed(4)})`;
    });
  }

  /* ---------- map: MapLibre + OpenFreeMap, loaded only when the map nears the screen ---------- */
  const mapEl = document.querySelector('[data-map]');
  if (mapEl) {
    const VER = '4.7.1';
    const load = () => new Promise((res, rej) => {
      const css = document.createElement('link');
      css.rel = 'stylesheet'; css.href = `https://unpkg.com/maplibre-gl@${VER}/dist/maplibre-gl.css`;
      document.head.append(css);
      const sc = document.createElement('script');
      sc.src = `https://unpkg.com/maplibre-gl@${VER}/dist/maplibre-gl.js`;
      sc.onload = res; sc.onerror = rej; document.head.append(sc);
    });
    const draw = () => {
      const pts = JSON.parse(mapEl.dataset.points);
      const dark = matchMedia('(prefers-color-scheme: dark)').matches && doc.dataset.theme !== 'light';
      const map = new maplibregl.Map({
        container: mapEl,
        style: `https://tiles.openfreemap.org/styles/${dark ? 'dark' : 'positron'}`,
        bounds: [[72.6, 9.6], [80.6, 21.6]], fitBoundsOptions: { padding: 40 },
        cooperativeGestures: true, attributionControl: { compact: true },
      });
      map.addControl(new maplibregl.NavigationControl({ showCompass: false }), 'top-right');
      const pinByName = {};
      map.once('load', () => {
        pts.forEach((p, i) => {
          const el = document.createElement('button');
          el.type = 'button'; el.className = 'map-pin'; el.setAttribute('aria-label', p.name);
          const dotEl = document.createElement('span');
          dotEl.style.setProperty('--d', `${i * 110}ms`);
          el.append(dotEl);
          const a = document.createElement('a'); a.href = p.url; a.textContent = p.name + ' →';
          pinByName[p.name] = el;
          new maplibregl.Marker({ element: el }).setLngLat([p.lon, p.lat])
            .setPopup(new maplibregl.Popup({ offset: 14, closeButton: false }).setDOMContent(a)).addTo(map);
        });
      });
      // Hovering the list lights up its pin
      mapEl.parentElement.querySelectorAll('.map-list li').forEach((li) => {
        const name = li.querySelector('a').textContent;
        li.addEventListener('pointerenter', () => pinByName[name]?.classList.add('hot'));
        li.addEventListener('pointerleave', () => pinByName[name]?.classList.remove('hot'));
      });
    };
    const fail = () => { mapEl.innerHTML = '<p class="map-fallback">The map couldn\'t load. The list beside it has every trek.</p>'; };
    const go = () => load().then(draw).catch(fail);
    if ('IntersectionObserver' in window) {
      const mio = new IntersectionObserver((en) => { if (en[0].isIntersecting) { mio.disconnect(); go(); } }, { rootMargin: '400px' });
      mio.observe(mapEl);
    } else go();
  }

  queueScroll();
})();
