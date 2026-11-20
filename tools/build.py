# -*- coding: utf-8 -*-
"""Génère le site brainboiled.com.

    python3 tools/build.py [chemin/vers/flowday-legal]

- Accueil brainboiled en 9 langues (/, /fr/, /de/ …)
- Page d'attente pour chaque appli pas encore publiée (/<appli>/, /<appli>/fr/ …)
- Migration du site FlowDay (dépôt flowday-legal) vers /flowday/, si son chemin est donné
- sitemap.xml

Tout est statique (GitHub Pages). La mise en forme vient de /assets/css/brainboiled.css.
Les pages d'appli « à la main » (comme /flowday/) ne sont pas écrasées : une appli
marquée own_pages=True dans OWN_PAGES n'a pas de page d'attente générée.
"""
import os, re, sys, html
from i18n import LANGS, LANG_NAMES, SITE, CONTACT, HOME, APPS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWN_PAGES = {"flowday"}  # applis qui ont déjà leurs propres pages
URLS = []


def lp(lang):
    """préfixe de langue : '' pour l'anglais, 'fr/' sinon"""
    return "" if lang == "en" else f"{lang}/"


def write(rel, content):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def head(lang, title, desc, canonical_path, alternates, app=None, icon=None, og_image="/assets/brand/og-brainboiled.jpg"):
    """alternates : {lang: chemin} pour les balises hreflang"""
    alt = "\n".join(f'<link rel="alternate" hreflang="{l}" href="{SITE}{p}">' for l, p in alternates.items())
    if "en" in alternates:
        alt += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{alternates["en"]}">'
    if app:
        icons = (f'<link rel="icon" type="image/png" sizes="32x32" href="/assets/apps/{app}-favicon-32.png">\n'
                 f'<link rel="apple-touch-icon" href="/assets/apps/{app}-apple-touch.png">')
        theme = {"flowday": "#123F4E", "diafra": "#16110A", "origins": "#0B0E1C", "morsetree": "#11151E", "ringwise": "#161A20"}[app]
    else:
        icons = ('<link rel="icon" type="image/png" sizes="32x32" href="/assets/icons/favicon-32.png">\n'
                 '<link rel="apple-touch-icon" href="/assets/icons/apple-touch-icon.png">')
        theme = "#041431"
    URLS.append(canonical_path)
    t = html.escape(title, quote=True)
    d = html.escape(desc, quote=True)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{d}">
<meta name="theme-color" content="{theme}">
<link rel="canonical" href="{SITE}{canonical_path}">
{alt}
{icons}
<meta property="og:type" content="website">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}{canonical_path}">
<meta property="og:image" content="{SITE}{og_image}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preload" href="/assets/fonts/urbanist-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/brainboiled.css">
</head>"""


def lang_switch(lang, paths):
    items = []
    for l in LANGS:
        if l not in paths:
            continue
        name = LANG_NAMES[l]
        if l == lang:
            items.append(f'<li><span aria-current="true">{name}</span></li>')
        else:
            items.append(f'<li><a href="{paths[l]}" hreflang="{l}" lang="{l}">{name}</a></li>')
    return (f'<details class="langs"><summary aria-label="{HOME["language"][lang]}">{LANG_NAMES[lang]}</summary>'
            f'<ul>{"".join(items)}</ul></details>')


def topbar(lang, paths, app=None):
    home = f"/{lp(lang)}"
    if app:
        mark = (f'<a class="brandmark" href="{home}"><img src="/assets/brand/brainboiled-symbole.png" alt="" width="32" height="28">'
                f'<span><span class="by">{HOME["an_app_by"][lang]} </span><strong>brainboiled</strong></span></a>')
    else:
        mark = (f'<a class="brandmark" href="{home}"><img src="/assets/brand/brainboiled-logo-horizontal.png" '
                f'alt="brainboiled" width="126" height="32"></a>')
    return f'<div class="topbar"><div class="wrap">{mark}{lang_switch(lang, paths)}</div></div>'


def site_foot(lang, app=None):
    home = f"/{lp(lang)}"
    links = [f'<a href="mailto:{CONTACT}">{HOME["contact"][lang]}</a>']
    return (f'<footer class="site-foot"><div class="wrap">'
            f'<a href="{home}"><img src="/assets/brand/brainboiled-logo-horizontal.png" alt="brainboiled" width="110" height="28"></a>'
            f'<nav>{"".join(links)}</nav><span>© 2026 brainboiled</span></div></footer>')


# ---------------------------------------------------------------- accueil
def build_home():
    paths = {l: f"/{lp(l)}" for l in LANGS}
    for lang in LANGS:
        cards = []
        for a in APPS:
            href = f"/{a['slug']}/{lp(lang)}"
            chip = (f'<span class="chip live">{HOME["available"][lang]}</span>' if a["live"]
                    else f'<span class="chip">{HOME["soon"][lang]}</span>')
            cards.append(f"""
      <a class="app-card" data-app="{a['slug']}" href="{href}">
        <div class="head">
          <img class="icon" src="/assets/apps/{a['slug']}-icon-192.png" alt="" width="64" height="64" loading="lazy">
          <div><h3>{a['name']}</h3><p class="kind">{a['kind'][lang]}</p></div>
        </div>
        <p class="pitch">{a['pitch'][lang]}</p>
        <div class="foot">{chip}<span class="go">{HOME['discover'][lang]}</span></div>
      </a>""")
        values = "".join(f'<div class="value"><h3>{h}</h3><p>{p}</p></div>' for h, p in HOME["values"][lang])
        page = head(lang, HOME["title"][lang], HOME["description"][lang], f"/{lp(lang)}", paths) + f"""
<body data-app="brainboiled">
{topbar(lang, paths)}
<main>
  <header class="hero wrap">
    <img class="logo" src="/assets/brand/brainboiled-logo-empile.png" alt="brainboiled" width="360" height="221">
    <h1>{HOME['tagline'][lang]}</h1>
  </header>
  <section class="section wrap" id="apps">
    <h2 class="section-title">{HOME['apps_title'][lang]}</h2>
    <div class="apps">{''.join(cards)}
    </div>
  </section>
  <section class="section wrap" id="studio">
    <h2 class="section-title">{HOME['studio_title'][lang]}</h2>
    <div class="values">{values}</div>
  </section>
</main>
{site_foot(lang)}
</body>
</html>
"""
        write(f"{lp(lang)}index.html", page)


# ---------------------------------------------------------------- pages d'attente
def build_placeholders():
    for a in APPS:
        if a["slug"] in OWN_PAGES:
            continue
        s = a["slug"]
        paths = {l: f"/{s}/{lp(l)}" for l in LANGS}
        for lang in LANGS:
            title = f"{a['name']} — {a['kind'][lang]}"
            page = head(lang, title, a["pitch"][lang], f"/{s}/{lp(lang)}", paths, app=s) + f"""
<body data-app="{s}" class="app-page">
{topbar(lang, paths, app=s)}
<main class="wrap narrow">
  <header class="app-hero">
    <img class="logo" src="/assets/apps/{s}-icon-192.png" alt="" width="104" height="104">
    <h1>{a['name']}</h1>
    <p class="tagline">{a['kind'][lang]}</p>
    <p class="baseline">{a['pitch'][lang]}</p>
  </header>
  <section>
    <div class="soon-panel">
      <span class="chip">{HOME['soon'][lang]}</span>
      <p style="margin-top:14px">{HOME['soon_long'][lang]}</p>
    </div>
  </section>
  <p style="text-align:center"><a class="back" href="/{lp(lang)}">{HOME['back_home'][lang]}</a></p>
</main>
{site_foot(lang, app=s)}
</body>
</html>
"""
            write(f"{s}/{lp(lang)}index.html", page)


# ---------------------------------------------------------------- migration FlowDay
FD_PAGES = ["", "privacy/", "terms/", "delete-account/"]


def migrate_flowday(src):
    for sub in FD_PAGES:
        paths = {l: f"/flowday/{lp(l)}{sub}" for l in LANGS}
        for lang in LANGS:
            f = os.path.join(src, lp(lang), sub, "index.html")
            raw = open(f, encoding="utf-8").read()
            title = html.unescape(re.search(r"<title>(.*?)</title>", raw, re.S).group(1).strip())
            desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', raw, re.S).group(1))
            body = re.search(r'<div class="wrap">(.*)</div>\s*</body>', raw, re.S).group(1)
            body = body.replace("https://flowdayapp.com/", "/flowday/")
            body = body.replace('<div class="logo">F</div>',
                                '<img class="logo" src="/assets/apps/flowday-icon-192.png" alt="" width="104" height="104">')
            body = body.replace("<header>", '<header class="app-hero">', 1)
            body = body.replace("<footer>", '<footer class="app-foot">', 1)
            legal = sub != ""
            page = head(lang, title, desc, f"/flowday/{lp(lang)}{sub}", paths, app="flowday") + f"""
<body data-app="flowday" class="app-page{' legal' if legal else ''}">
{topbar(lang, paths, app='flowday')}
<main class="wrap{' narrow' if not legal else ''}">{body}</main>
{site_foot(lang, app='flowday')}
</body>
</html>
"""
            write(f"flowday/{lp(lang)}{sub}index.html", page)


def sitemap():
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    xml += [f"  <url><loc>{SITE}{u}</loc></url>" for u in sorted(set(URLS))]
    xml.append("</urlset>\n")
    write("sitemap.xml", "\n".join(xml))


if __name__ == "__main__":
    build_home()
    build_placeholders()
    if len(sys.argv) > 1:
        migrate_flowday(sys.argv[1])
    else:
        # garder les pages FlowDay déjà migrées dans le sitemap
        for sub in FD_PAGES:
            for lang in LANGS:
                URLS.append(f"/flowday/{lp(lang)}{sub}")
    sitemap()
    print(len(set(URLS)), "pages")
