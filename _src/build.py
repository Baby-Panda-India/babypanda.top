"""Generate the static pages for babypanda.top.

Run from the repo root:  python _src/build.py
Writes index.html, treks/index.html, treks/<slug>.html and 404.html.
Jekyll (GitHub Pages) ignores this _src folder.
"""
import html
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(__file__))
from treks import TREKS, IG  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://babypanda.top"
THADAM = "https://thadam.babypanda.top"
PHONES = [("+91 86674 49954", "+918667449954")]
RANGES = ["Sahyadris", "Eastern Ghats", "Palani Hills"]

e = html.escape


def fmt_date(iso):
    if not iso:
        return ""
    d = date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%B %Y')}"


def slug_range(r):
    return r.lower().replace(" ", "-")


# ---------- art: layered ridgelines, one palette per hue ----------
PALETTES = {
    "leaf": ("#dfe9cc", "#9fbb6c", "#638d24", "#3a5812", "#22340a"),
    "water": ("#d6e7ee", "#8fbccb", "#4f8ea3", "#2b6274", "#173a46"),
    "rock": ("#efe2cf", "#c9a77f", "#9e7751", "#604c38", "#33281c"),
    "fort": ("#ece6dc", "#b8a993", "#857560", "#56493a", "#2c251c"),
}


def ridge_art(t, idx, cls="art"):
    sky, a, b, c, d = PALETTES[t["hue"]]
    s = (idx * 37) % 23  # small per-trek variation
    p1 = f"M0 {150+s} C 80 {110+s} 140 {130-s} 210 {100+s} S 330 {70+s} 400 {105-s} V300 H0Z"
    p2 = f"M0 {190-s} C 60 {160} 120 {175+s} 190 {150} S 320 {140-s} 400 {165} V300 H0Z"
    p3 = f"M0 {230} C 90 {205+s} 150 {225} 230 {205-s} S 350 {215} 400 {200+s} V300 H0Z"
    p4 = f"M0 {262} C 100 {250} 170 {268-s//2} 260 {255} S 360 {262} 400 {252} V300 H0Z"
    accent = ""
    if t["kind"] in ("Waterfall", "Rock pool"):
        accent = "".join(f'<path d="M{222+s+k*7} {100+s} q{3-k} 70 {-2+k} 150" stroke="#fff" stroke-opacity="{.75-k*.2:.2f}" stroke-width="{4-k}" fill="none" stroke-linecap="round"/>' for k in range(3))
    elif t["kind"] == "Hill fort":
        accent = '<path d="M170 96h60v-12h8v12h12v-16h8v16h12v30h-100z" fill="' + c + '"/>'
    elif t["kind"] in ("Twin pinnacles", "Peak"):
        accent = f'<path d="M150 150 L176 58 L196 150Z M206 150 L230 70 L252 150Z" fill="{b}"/>'
    elif t["kind"] == "Caves":
        accent = f'<path d="M168 190 q32 -46 64 0Z" fill="{d}"/><path d="M240 196 q18 -26 36 0Z" fill="{d}"/>'
    elif t["kind"] == "Plateau":
        accent = f'<path d="M90 140 L140 92 H290 L330 140Z" fill="{b}"/>'
    elif t["kind"] == "Ridge traverse":
        accent = f'<path d="M30 170 Q80 120 120 150 T210 120 T300 135 T380 105" fill="none" stroke="#fff" stroke-opacity=".75" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>'
    sun = f'<circle cx="{318-s*2}" cy="{58+s}" r="22" fill="#fff" fill-opacity=".55"/>'
    return (
        f'<svg class="{cls}" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false">'
        f'<rect width="400" height="300" fill="{sky}"/><g data-depth="0.2">{sun}</g>'
        f'<g data-depth="0.4"><path d="{p1}" fill="{a}"/>{accent}</g><g data-depth="0.65"><path d="{p2}" fill="{b}"/></g>'
        f'<g data-depth="0.85"><path d="{p3}" fill="{c}"/></g><g data-depth="1"><path d="{p4}" fill="{d}" transform="translate(0 2) scale(1 1.02)"/></g></svg>'
    )


# ---------- shared chrome ----------
def head(title, desc, path, depth):
    up = "../" * depth
    canonical = SITE + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#f5f3ee" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14120f" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/assets/img/group-1100.jpg">
<link rel="icon" href="{up}favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="{up}assets/img/apple-touch-icon.png">
<link rel="stylesheet" href="{up}assets/css/site.css">
<script src="{up}assets/js/site.js" defer></script>
</head>
"""


def nav(depth, current=""):
    up = "../" * depth
    home = up or "./"

    def cur(name):
        return ' aria-current="page"' if current == name else ""

    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="nav" data-nav>
  <div class="nav-inner">
    <a class="brand" href="{home}" aria-label="Baby Panda Treks, home">
      <img src="{up}assets/img/panda.png" alt="" width="34" height="34">
      <span>Baby Panda <b>Treks</b></span>
    </a>
    <nav aria-label="Main">
      <a href="{up}treks/"{cur('treks')}>Treks</a>
      <a href="{home}#thadam">Thadam</a>
      <a class="nav-cta" href="{home}#join">Join a trek</a>
    </nav>
  </div>
</header>
"""


def footer(depth):
    up = "../" * depth
    home = up or "./"
    phones = "".join(f'<li><a href="tel:{t}">{d}</a></li>' for d, t in PHONES)
    return f"""<footer class="foot">
  <div class="wrap foot-grid">
    <div>
      <a class="brand" href="{home}"><img src="{up}assets/img/panda.png" alt="" width="34" height="34"><span>Baby Panda <b>Treks</b></span></a>
      <p class="muted">Small-group treks to forts, falls and peaks across the Sahyadris, the Eastern Ghats and the Palani Hills.</p>
    </div>
    <div>
      <h2 class="foot-h">Explore</h2>
      <ul><li><a href="{up}treks/">Trek journal</a></li><li><a href="{home}#thadam">Thadam app</a></li><li><a href="{home}#join">Join a trek</a></li></ul>
    </div>
    <div>
      <h2 class="foot-h">Contact</h2>
      <ul>{phones}<li><a href="{IG}" rel="noopener">Instagram @babypanda.top</a></li></ul>
    </div>
  </div>
  <div class="wrap foot-base muted"><span>© {date.today().year} Baby Panda Treks</span><span>Trek safe. Leave no trace.</span></div>
</footer>
</body>
</html>
"""


def card(t, idx, depth):
    up = "../" * depth
    when = fmt_date(t["date"])
    state = t["place"].split(", ")[-1]
    spec = [e(t["kind"]), e(state)]
    if when:
        spec.insert(0, f'<time datetime="{t["date"]}">{when}</time>')
    spec_html = '<span class="dot" aria-hidden="true">·</span>'.join(f"<span>{s}</span>" for s in spec)
    return f"""<li class="card" data-range="{slug_range(t['range'])}">
  <a href="{up}treks/{t['slug']}.html">
    <div class="card-art">{ridge_art(t, idx)}<span class="chip">{e(t['range'])}</span></div>
    <div class="card-body">
      <p class="spec">{spec_html}</p>
      <h3>{e(t['name'])}</h3>
      <p class="card-sum">{e(t['summary'])}</p>
      <span class="more">Read the story <span aria-hidden="true">→</span></span>
    </div>
  </a>
</li>"""


def journal(depth, heading_tag="h2", intro=True, limit=None):
    counts = {r: sum(1 for t in TREKS if t["range"] == r) for r in RANGES}
    seg = '<button type="button" role="tab" aria-selected="true" data-filter="all">All <span>{}</span></button>'.format(len(TREKS))
    seg += "".join(
        f'<button type="button" role="tab" aria-selected="false" data-filter="{slug_range(r)}">{e(r)} <span>{counts[r]}</span></button>'
        for r in RANGES
    )
    cards = "\n".join(card(t, i, depth) for i, t in enumerate(TREKS))
    more = (
        f'<div class="more-row" data-more-row><a class="btn btn-quiet more-btn" href="{"../" * depth}treks/" data-more>'
        f'<span data-more-label>See all {len(TREKS)} treks</span> <span class="more-chev" aria-hidden="true"></span></a></div>'
        if limit else ""
    )
    lead = (
        f'<p class="lead">All {len(TREKS)} Baby Panda Treks so far, newest first, from our first monsoon trek in the Sahyadris to the shola forests of Kodaikanal.</p>'
        if intro else ""
    )
    return f"""<section class="section" id="treks" aria-labelledby="treks-h">
  <div class="wrap">
    <div class="section-head">
      <{heading_tag} id="treks-h" class="h-section">The trek journal</{heading_tag}>
      {lead}
    </div>
    <div class="seg" role="tablist" aria-label="Filter treks by mountain range" data-seg>
      <span class="seg-pill" aria-hidden="true"></span>{seg}
    </div>
    <ul class="grid" data-grid{f' data-limit="{limit}"' if limit else ""}>
{cards}
    </ul>
    {more}
  </div>
</section>
"""


def map_section(depth):
    import json
    up = "../" * depth
    pts = [
        {"name": t["name"], "url": f"{up}treks/{t['slug']}.html", "lat": t["at"][0], "lon": t["at"][1], "kind": t["kind"]}
        for t in TREKS if t.get("at")
    ]
    legend = "".join(
        f'<li><a href="{up}treks/{t["slug"]}.html">{e(t["name"])}</a><span>{e(t["place"].split(", ")[-1])}</span></li>'
        for t in TREKS
    )
    return f"""<section class="section map-sec" id="map" aria-labelledby="map-h">
  <div class="wrap">
    <div class="section-head"><h2 id="map-h" class="h-section">Where we've walked</h2>
    <p class="lead">From the Sahyadri forts around Mumbai and Pune to the Andhra waterfalls near Chennai and the shola forests of Kodaikanal. Pins are approximate; a few treks aren't pinned yet.</p></div>
    <div class="map-wrap">
      <div class="map" data-map data-points='{e(json.dumps(pts))}' role="img" aria-label="Map of India with pins at each trek location"></div>
      <ul class="map-list">{legend}</ul>
    </div>
  </div>
</section>
"""


def profile_graphic():
    import json
    prof = json.load(open(os.path.join(os.path.dirname(__file__), "velliangiri_profile.json")))
    W, H, PAD = 1000, 260, 0
    xs = [p[0] for p in prof["pts"]]
    x1, y0, y1 = max(xs), prof["minEle"] - 60, prof["maxEle"] + 40
    def X(v): return round(PAD + v / x1 * (W - 2 * PAD), 1)
    def Y(v): return round(H - (v - y0) / (y1 - y0) * (H - 20), 1)
    line = "M" + " L".join(f"{X(a)} {Y(b)}" for a, b in prof["pts"])
    area = line + f" L{X(x1)} {H} L{X(0)} {H}Z"
    data = e(json.dumps({"pts": prof["pts"], "y0": y0, "y1": y1, "H": H}))
    return f"""<figure class="profile" data-profile="{data}">
      <figcaption class="profile-head">
        <span><span class="eyebrow light">Real Thadam data</span><b class="profile-title">Velliangiri Hills, {prof['km']} km one way</b></span>
        <span class="readout" aria-hidden="true"><b data-p-km>0.00</b> km <span class="sep">·</span> <b data-p-ele>{prof['minEle']}</b> m</span>
      </figcaption>
      <div class="profile-plot">
        <svg viewBox="0 0 {W} {H}" preserveAspectRatio="none" role="img" aria-label="Elevation profile rising from {prof['minEle']} m to {prof['maxEle']:,} m over {prof['km']} km" focusable="false">
          <defs><linearGradient id="pf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fbb6c" stop-opacity=".5"/><stop offset="1" stop-color="#9fbb6c" stop-opacity="0"/></linearGradient>
          <clipPath id="pclip"><rect data-p-clip x="0" y="0" width="0" height="{H}"/></clipPath></defs>
          <path d="{area}" fill="url(#pf)" clip-path="url(#pclip)"/>
          <path d="{line}" fill="none" stroke="rgba(242,246,234,.22)" stroke-width="2" vector-effect="non-scaling-stroke"/>
          <path d="{line}" fill="none" stroke="#c4d99a" stroke-width="3" vector-effect="non-scaling-stroke" clip-path="url(#pclip)"/>
        </svg>
        <span class="p-cursor" data-p-cursor aria-hidden="true"></span>
        <span class="p-dot" data-p-dot aria-hidden="true"></span>
      </div>
      <div class="profile-foot"><span>Start · {prof['minEle']} m</span><span>{prof['gain']:,} m of climbing, out and back</span><span>Summit · {prof['maxEle']:,} m</span></div>
    </figure>"""


def thadam_section(depth):
    up = "../" * depth
    feats = [
        ("Verified trail cards", "True distance, total climb, time by fitness level and the steepest stretch, computed from real route and elevation data."),
        ("Works with no signal", "Download a trail pack before you lose network. Map, route and your position keep working on the trail."),
        ("Off-route alerts", "If you stray more than 40 m from the path, your phone buzzes and shows the way back."),
        ("Check in, check out", "Tell the trail office you've started. If you're overdue, someone knows. Safety features are always free."),
    ]
    items = "".join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in feats)
    return f"""<section class="thadam" id="thadam" aria-labelledby="thadam-h">
  <div class="wrap thadam-grid">
    <div class="thadam-copy">
      <p class="eyebrow light"><img src="{up}assets/img/thadam-icon.svg" alt="" width="28" height="28"> Our app · தடம்</p>
      <h2 id="thadam-h" class="h-section">Thadam: a trail companion for when the signal drops.</h2>
      <p class="lead">On our treks we kept running into two problems: trail information that was wrong or missing, and no help once the network disappeared. Thadam is our answer, starting with Tamil Nadu's forest and temple trails.</p>
      <ul class="feats">{items}</ul>
      <div class="actions">
        <a class="btn btn-light" href="{THADAM}">Get the Android app</a>
        <span class="note">Android app · Preview build · Tamil, English and 11 more languages</span>
      </div>
    </div>
    <div class="phones" aria-label="Thadam screenshots" data-phones>
      <figure class="phone p1"><img src="{up}assets/img/thadam-home.jpg" alt="Thadam home screen listing Tamil Nadu trails" width="375" height="812" loading="lazy"></figure>
      <figure class="phone p2"><img src="{up}assets/img/thadam-trail.jpg" alt="Velliangiri Hills trail card with 3D map, 10.57 km distance and 1480 m climb" width="375" height="812" loading="lazy"></figure>
      <figure class="phone p3"><img src="{up}assets/img/thadam-guide.jpg" alt="Thadam on-trail guide screen" width="375" height="812" loading="lazy"></figure>
    </div>
  </div>
  <div class="wrap">{profile_graphic()}</div>
</section>
"""


def join_section():
    phones = " or ".join(f'<a href="tel:{t}">{d}</a>' for d, t in PHONES)
    return f"""<section class="section" id="join" aria-labelledby="join-h">
  <div class="wrap">
    <div class="section-head">
      <h2 id="join-h" class="h-section">Join the next trek</h2>
      <p class="lead">We announce every trip on Instagram first. Small groups, pickup points shared with each trip, and no experience needed for most trails.</p>
    </div>
    <ol class="steps">
      <li><span class="n">1</span><h3>Follow along</h3><p>New treks, dates and pickup points go up on <a href="{IG}" rel="noopener">@babypanda.top</a>.</p></li>
      <li><span class="n">2</span><h3>Register</h3><p>Use the registration link in our Instagram bio. We'll confirm your spot and send the details.</p></li>
      <li><span class="n">3</span><h3>Show up ready</h3><p>Good shoes, water, a rain layer. Each trek post here says what else to pack.</p></li>
    </ol>
    <div class="contact">
      <a class="btn" href="{IG}" rel="noopener">Follow on Instagram</a>
      <p class="muted">Questions? Call {phones}, or message us on Instagram.</p>
    </div>
  </div>
</section>
"""


TRAIL = "M150 900 C 260 820 330 800 420 760 S 600 700 680 640 S 820 560 900 520 S 1010 470 1050 420"


def hero_section():
    import random
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.randint(0, 1440)}" cy="{rnd.randint(0, 430)}" r="{rnd.choice((0.8, 1, 1.2, 1.6))}" fill="#fff" opacity="{rnd.uniform(.35, .9):.2f}"/>'
        for _ in range(70)
    )
    rot_names = {"katraj-to-sinhagad": "the K2S ridge"}
    places = [rot_names.get(t["slug"], t["name"]) for t in TREKS]
    first = e(places[0])
    ticker_items = "".join(
        f'<li><a href="treks/{t["slug"]}.html">{e(t["name"])}</a></li>' for t in sorted(TREKS, key=lambda t: t["num"])
    )
    import json
    return f"""<section class="hero" aria-labelledby="hero-h" data-hero>
  <div class="hero-stage">
    <svg class="scene" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
      <defs>
        <linearGradient id="sky-day" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a2a10"/><stop offset=".42" stop-color="#3b5320"/><stop offset=".7" stop-color="#a08a52"/><stop offset="1" stop-color="#f0d6a8"/></linearGradient>
        <linearGradient id="sky-night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#04070a"/><stop offset=".6" stop-color="#0d1610"/><stop offset="1" stop-color="#26301c"/></linearGradient>
        <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff3dc" stop-opacity=".95"/><stop offset=".3" stop-color="#f5d9a6" stop-opacity=".45"/><stop offset="1" stop-color="#e8cca2" stop-opacity="0"/></radialGradient>
        <filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="18"/></filter>
        <clipPath id="panda-clip"><circle r="17"/></clipPath>
        <mask id="trail-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="1440" height="900"><path data-trail-draw d="{TRAIL}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round"/></mask>
      </defs>
      <rect width="1440" height="900" fill="url(#sky-day)"/>
      <rect width="1440" height="900" fill="url(#sky-night)" data-night/>
      <g data-stars>{stars}</g>
      <g data-depth="0.08"><g data-sun><circle cx="1060" cy="360" r="300" fill="url(#glow)"/><circle cx="1060" cy="360" r="50" fill="#fff3dc"/></g></g>
      <g data-depth="0.18"><path d="M0 520 C 140 470 240 500 360 455 S 560 400 700 430 S 940 350 1060 395 S 1300 360 1440 400 V900 H0Z" fill="#6f7a43" opacity=".6"/></g>
      <g data-depth="0.3"><g class="mist"><ellipse cx="420" cy="520" rx="380" ry="36" fill="#f5e9d6" opacity=".22" filter="url(#soft)"/><ellipse cx="1180" cy="470" rx="320" ry="30" fill="#f5e9d6" opacity=".18" filter="url(#soft)"/></g></g>
      <g data-depth="0.38"><path d="M0 610 C 120 560 210 580 320 540 S 520 470 640 500 S 820 430 920 470 S 1000 410 1050 420 C 1120 450 1230 470 1320 450 S 1420 470 1440 480 V900 H0Z" fill="#3d5420"/>
        <path d="{TRAIL}" fill="none" stroke="#f5e9d6" stroke-width="3.5" stroke-dasharray="2 12" stroke-linecap="round" mask="url(#trail-mask)"/>
        <g data-trail-flag transform="translate(1050 420)" opacity="0"><path d="M0 0 V-50" stroke="#f5e9d6" stroke-width="3" stroke-linecap="round"/><path d="M0 -50 L32 -39 L0 -28Z" fill="#9fbb6c"/></g>
        <g data-trail-walker transform="translate(150 900)"><circle data-trail-halo r="26" fill="#fff" opacity=".2"/><circle r="20" fill="#fff"/><image href="assets/img/panda.png" x="-17" y="-17" width="34" height="34" clip-path="url(#panda-clip)" preserveAspectRatio="xMidYMid slice"/></g></g>
      <g data-depth="0.6"><path d="M0 700 C 160 650 280 690 420 660 S 640 610 780 650 S 1000 600 1140 640 S 1340 610 1440 630 V900 H0Z" fill="#26391a"/></g>
      <g data-depth="0.85"><path d="M0 790 C 180 750 330 790 520 770 S 820 730 1000 765 S 1300 740 1440 760 V900 H0Z" fill="#162310"/></g>
      <g data-depth="1"><path d="M0 850 C 220 830 420 860 660 845 S 1100 830 1440 845 V900 H0Z" fill="#0b1206"/></g>
    </svg>
    <div class="hero-copy wrap">
      <p class="eyebrow light rise" style="--i:0"><span class="dot-live" aria-hidden="true"></span> Baby Panda Treks · {len(TREKS)} treks and counting</p>
      <h1 id="hero-h" class="display"><span class="w"><span style="--i:1">Weekends,</span></span> <span class="w"><span style="--i:2">on</span></span> <span class="w"><span style="--i:3">foot.</span></span></h1>
      <p class="hero-rot rise" style="--i:4">We've walked to <span class="rot" data-rot='{e(json.dumps(places))}'><span class="rot-word">{first}</span></span></p>
      <p class="hero-sub rise" style="--i:5">Small-group treks to forts, waterfalls and peaks across the Sahyadris, the Eastern Ghats and the Palani Hills.</p>
      <div class="actions rise" style="--i:6">
        <a class="btn btn-light" href="#treks">Read the trek journal</a>
        <a class="btn btn-glass" href="#join">Join the next trek</a>
      </div>
    </div>
    <nav class="ticker rise" style="--i:7" aria-label="All treks">
      <ul class="ticker-track">{ticker_items}</ul>
      <ul class="ticker-track" aria-hidden="true">{ticker_items.replace('<a ', '<a tabindex="-1" ')}</ul>
    </nav>
  </div>
</section>
"""


# ---------- pages ----------
def page_home():
    n = len(TREKS)
    out = head(
        "Baby Panda Treks",
        f"{len(TREKS)} small-group treks so far to forts, waterfalls and peaks across Maharashtra, Tamil Nadu and Andhra Pradesh, plus Thadam, our offline trail companion.",
        "/", 0,
    )
    out += '<body class="home">\n' + nav(0)
    out += f"""<main id="main">
{hero_section()}
<section class="crew" id="crew" aria-labelledby="crew-h" data-crew>
  <div class="crew-stick">
    <figure class="crew-photo" data-crew-photo>
      <picture>
        <source media="(max-width: 700px)" srcset="assets/img/silhouette-1100.jpg">
        <img class="crew-img" src="assets/img/silhouette-1920.jpg" alt="The Baby Panda crew seen from behind in silhouette, arms raised, on a misty Sahyadri fort" width="1920" height="964" loading="lazy" data-crew-img>
      </picture>
      <span class="crew-warm" aria-hidden="true"></span>
      <span class="crew-word" aria-hidden="true" data-crew-word>THE CREW · THE CREW</span>
    </figure>
    <div class="crew-copy wrap">
      <p class="eyebrow light" data-crew-in style="--d:0">The crew</p>
      <h2 id="crew-h" class="crew-h" data-crew-in style="--d:1">{n} summits. Same arms in the air.</h2>
      <p class="crew-p" data-crew-in style="--d:2">Wet shoes, misty forts, and a group that's grown with every trek. There's room for you on the next one.</p>
      <div class="actions" data-crew-in style="--d:3"><a class="btn btn-light" href="#join">Join the next trek</a><a class="btn btn-glass" href="#treks">See where we've been</a></div>
    </div>
  </div>
</section>
<section class="stats wrap" aria-label="At a glance">
  <div><b data-count="{n}">{n}</b><span>treks so far</span></div>
  <div><b data-count="3">3</b><span>states</span></div>
  <div><b data-count="3">3</b><span>mountain ranges</span></div>
  <div><b data-count="1">1</b><span>app in the making</span></div>
</section>
"""
    out += journal(0, limit=6) + map_section(0) + thadam_section(0) + join_section() + faq_section() + "</main>\n" + footer(0)
    return out


FAQS = [
    ("Do I need trekking experience?",
     "Not for most of our trails. Each trek post describes the terrain, so you can judge whether it suits you. If you're unsure, call or message us before registering."),
    ("How do I sign up?",
     "Every trip is announced on our Instagram, @babypanda.top, with the date, pickup points and a registration link in the bio. We confirm your spot after you register."),
    ("What should I carry?",
     "Shoes with good grip, at least two litres of water, a rain layer and a small snack. Waterfall and canyon treks need a change of clothes. Each trek post lists what else to pack."),
    ("What happens if it rains heavily?",
     "Streams and canyons can rise quickly. If a crossing or a stretch looks unsafe on the day, we turn back. No view is worth the risk."),
    ("Is Thadam free?",
     "Thadam is a free Android app, in preview, that you can download from thadam.babypanda.top. Its safety features — offline maps, off-route alerts and check-in — will always be free."),
]


def faq_section():
    items = "".join(
        f'<details><summary>{e(q)}<span class="chev" aria-hidden="true"></span></summary><p>{e(a)}</p></details>'
        for q, a in FAQS
    )
    return f"""<section class="section faq" id="faq" aria-labelledby="faq-h">
  <div class="wrap faq-grid">
    <div class="section-head"><h2 id="faq-h" class="h-section">First trek with us?</h2><p class="lead">The questions people ask most before signing up.</p></div>
    <div class="faq-list">{items}</div>
  </div>
</section>
"""


def page_treks():
    out = head(
        "Trek journal · Baby Panda Treks",
        "Every Baby Panda trek so far: Sahyadri forts and canyons, Andhra waterfalls and Kodaikanal forest trails.",
        "/treks/", 1,
    )
    out += '<body class="list">\n' + nav(1, "treks")
    out += '<main id="main" class="pad-top">' + journal(1, "h1") + "</main>\n" + footer(1)
    return out


def page_trek(i):
    t = TREKS[i]
    when = fmt_date(t["date"])
    prev_t = TREKS[i - 1] if i > 0 else None
    next_t = TREKS[i + 1] if i + 1 < len(TREKS) else None
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in t["facts"])
    body = "".join(f"<p>{e(p)}</p>" for p in t["body"])
    links = "".join(
        f'<a class="btn{" btn-quiet" if j else ""}" href="{u}" rel="noopener">{e(label)} <span aria-hidden="true">↗</span></a>'
        for j, (label, u) in enumerate(t["links"])
    )
    meta = [e(t["kind"]), e(t["range"])]
    if when:
        meta.insert(0, f'<time datetime="{t["date"]}">{when}</time>')
    pn = '<nav class="pn wrap" aria-label="More treks">'
    pn += (f'<a class="pn-prev" href="{prev_t["slug"]}.html"><span>Newer</span>{e(prev_t["name"])}</a>' if prev_t else "<span></span>")
    pn += (f'<a class="pn-next" href="{next_t["slug"]}.html"><span>Older</span>{e(next_t["name"])}</a>' if next_t else "<span></span>")
    pn += "</nav>"
    words = sum(len(p.split()) for p in t["body"]) + len(t["summary"].split())
    mins = max(1, round(words / 200))
    meta.append(f"{mins} min read")
    water = t["kind"] in ("Waterfall", "Rock pool", "Canyon")
    byg = [
        "Tell someone at home where you're going and when you expect to be back.",
        "Carry at least two litres of water and something salty to eat.",
        "Wear shoes with real grip; wet rock and laterite are slippery.",
        "Pack out everything you carry in. Leave no trace.",
    ]
    if water:
        byg.insert(1, "Water levels change fast after rain. If a crossing looks wrong, turn back.")
    if t["range"] == "Sahyadris":
        byg.insert(1, "Monsoon trails are beautiful and slippery. Start early and finish before dark.")
    byg_html = "".join(f"<li>{e(x)}</li>" for x in byg)
    tn = "Tamil Nadu" in t["place"]
    plug = (
        f'<aside class="plug"><img src="../assets/img/thadam-icon.svg" alt="" width="44" height="44"><div><h2>Trekking in {"Tamil Nadu" if tn else "the hills"}?</h2>'
        f'<p>Thadam gives you honest trail data and keeps working with no signal.</p><a href="{THADAM}">Get the Android app ↗</a></div></aside>'
    )
    out = head(f"{t['name']} · Baby Panda Treks", t["summary"], f"/treks/{t['slug']}.html", 1)
    out += '<body class="post">\n<div class="progress" aria-hidden="true"><span data-progress></span></div>\n' + nav(1, "treks")
    out += f"""<main id="main">
<article>
  <header class="post-hero" data-post-hero>
    {ridge_art(t, i, "art post-art")}
    <div class="wrap post-title">
      <a class="back" href="./">← All treks</a>
      <p class="eyebrow">{" · ".join(meta)}</p>
      <h1 class="display">{e(t['name'])}</h1>
      <p class="post-place">{e(t['place'])}</p>
    </div>
  </header>
  <div class="wrap post-grid">
    <div class="prose">
      <p class="lead">{e(t['summary'])}</p>
      {body}
      <div class="actions">{links}</div>
    </div>
    <aside class="facts" aria-label="Trek facts">
      <h2>At a glance</h2>
      <dl>{facts}</dl>
    </aside>
  </div>
  <div class="wrap byg-wrap">
    <section class="byg" aria-labelledby="byg-h"><h2 id="byg-h">Before you go</h2><ul>{byg_html}</ul></section>
    {plug}
  </div>
</article>
{pn}
</main>
"""
    out += footer(1)
    return out


def page_404():
    out = head("Off trail · Baby Panda Treks", "This page doesn't exist.", "/404.html", 0)
    out = out.replace('href="favicon.ico"', 'href="/favicon.ico"').replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    out += '<body class="nf">\n' + nav(0).replace('href="./"', 'href="/"').replace('href="treks/', 'href="/treks/').replace('src="assets/', 'src="/assets/').replace('href="./#', 'href="/#')
    out += """<main id="main" class="nf-main wrap">
  <p class="eyebrow">404</p>
  <h1 class="display">You've wandered off the trail.</h1>
  <p class="lead">This page doesn't exist. Head back and pick a trek.</p>
  <div class="actions"><a class="btn" href="/treks/">See all treks</a><a class="btn btn-quiet" href="/">Home</a></div>
</main>
"""
    out += footer(0).replace('href="./"', 'href="/"').replace('href="treks/', 'href="/treks/').replace('src="assets/', 'src="/assets/').replace('href="./#', 'href="/#')
    return out


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    print("wrote", rel)


if __name__ == "__main__":
    write("index.html", page_home())
    write("treks/index.html", page_treks())
    for i in range(len(TREKS)):
        write(f"treks/{TREKS[i]['slug']}.html", page_trek(i))
    write("404.html", page_404())
