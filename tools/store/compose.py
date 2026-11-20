"""Visuels de store à partir des captures réelles (goldens Flutter).

Usage : python3 compose.py config.json captures_dir sortie_dir
config.json : {
  "bg": [r,g,b], "bg_top": [r,g,b], "accent": [r,g,b], "text": [r,g,b], "frame": [r,g,b],
  "title_font": chemin TTF, "body_font": chemin TTF, "cjk_bold": ..., "cjk_regular": ...,
  "shots": ["3_sim", ...],                         # ordre des captures
  "captions": {"fr": [["titre", "sous-titre"], ...], ...}
}
Produit, pour chaque langue : play/<lang>/N.jpg (1080x1920), apple/<lang>/N.png (1320x2868),
et ipad/<lang>/N.png (2064x2752) si on passe 'ipad' en 4e argument (captures rendues au format tablette).
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

SIZES = {'play': (1080, 1920), 'apple': (1320, 2868), 'ipad': (2064, 2752)}


def fit(d, text, path, size, maxw, minsize=28):
    while True:
        f = ImageFont.truetype(path, size)
        if d.textlength(text, font=f) <= maxw or size <= minsize:
            return f
        size -= 2


def wrap(d, text, font, maxw, ja):
    if d.textlength(text, font=font) <= maxw:
        return [text]
    units = list(text) if ja else text.split(' ')
    sep = '' if ja else ' '
    best = None
    for i in range(1, len(units)):
        a, b = sep.join(units[:i]), sep.join(units[i:])
        if ja and b[0] in '、。）」ー・':
            continue
        m = max(d.textlength(a, font=font), d.textlength(b, font=font))
        if best is None or m < best[0]:
            best = (m, [a, b])
    return best[1]


def compose(cfg, shot_path, title, sub, size, ja):
    W, H = size
    s = W / 1080
    im = Image.new('RGB', (W, H), tuple(cfg['bg']))
    d = ImageDraw.Draw(im)
    top_c, bg = cfg.get('bg_top', cfg['bg']), cfg['bg']
    for y in range(int(H * 0.5)):
        k = max(0.0, 1 - y / (H * 0.5))
        d.line([(0, y), (W, y)], fill=tuple(int(bg[i] + (top_c[i] - bg[i]) * k) for i in range(3)))
    tfp = cfg['cjk_bold'] if ja else cfg['title_font']
    sfp = cfg['cjk_regular'] if ja else cfg['body_font']
    tsize = int((cfg.get('title_size', 74) - (6 if ja else 0)) * s)
    margin = int(60 * s)
    tf = ImageFont.truetype(tfp, tsize)
    lines = wrap(d, title, tf, W - 2 * margin, ja)
    widest = max(lines, key=lambda l: d.textlength(l, font=tf))
    tf = fit(d, widest, tfp, tsize, W - 2 * margin)
    y = int((110 if len(lines) == 2 else 150) * s)
    for l in lines:
        d.text((W / 2, y), l, font=tf, fill=tuple(cfg['accent']), anchor='ma')
        y += tf.size + int(14 * s)
    sf = fit(d, sub, sfp, int(40 * s), W - 2 * margin)
    d.text((W / 2, y + int(14 * s)), sub, font=sf, fill=tuple(cfg['text']), anchor='ma')
    top = y + int(14 * s) + sf.size + int(60 * s)
    sh_img = Image.open(shot_path).convert('RGB')
    sh = H - top + int(120 * s)
    sw = int(sh_img.width * sh / sh_img.height)
    if sw > W - int(150 * s):
        sw = W - int(150 * s)
        sh = int(sh_img.height * sw / sh_img.width)
    sh_img = sh_img.resize((sw, sh), Image.LANCZOS)
    x = (W - sw) // 2
    b, r = int(14 * s), int(54 * s)
    d.rounded_rectangle([x - b, top - b, x + sw + b, top + sh + b], radius=r + b,
                        fill=tuple(cfg.get('bezel', [8, 8, 10])), outline=tuple(cfg['frame']), width=max(2, int(3 * s)))
    mask = Image.new('L', (sw, sh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw, sh], radius=r, fill=255)
    im.paste(sh_img, (x, top), mask)
    return im


def main(cfg_path, shots_dir, out, stores='play,apple'):
    cfg = json.load(open(cfg_path, encoding='utf-8'))
    for lang, caps in cfg['captions'].items():
        ja = lang == 'ja'
        assert len(caps) == len(cfg['shots']), lang
        for i, (shot, (t, sub)) in enumerate(zip(cfg['shots'], caps)):
            src = os.path.join(shots_dir, f'{lang}_{shot}.png')
            for store in stores.split(','):
                size = SIZES[store]
                o = os.path.join(out, store, lang)
                os.makedirs(o, exist_ok=True)
                im = compose(cfg, src, t, sub, size, ja)
                if store == 'play':
                    im.save(os.path.join(o, f'{i + 1}.jpg'), quality=92)
                else:
                    im.save(os.path.join(o, f'{i + 1}.png'), optimize=True)
    print('ok', out)


if __name__ == '__main__':
    main(*sys.argv[1:5])
