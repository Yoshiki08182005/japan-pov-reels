"""Standard programmatic art for 2D copy-format episodes (the approved v4 format).

Parameterized version of episodes/ep02_ramen_ticket_assets.py: the text-bearing
art (title pill, verdict stamps, JP speech bubble) is generated from the
episode spec's "art" block, so any episode gets the same look without a
per-episode assets script. Also hosts the shared helpers (font / fit /
led_text / palette) that build_2d_std.py imports.

build_art(outdir, cfg) writes:
  stamp_wrong.png / stamp_right.png  verdict stamps (transparent, rotated -12deg)
  pill_title.png                     black title pill (top of frame, from second 0)
  pill_rightway.png                  green "THE RIGHT WAY" pill
  bubble_shout.png                   JP speech bubble for the staff shout line

cfg: {"title": "POV: your first ... in Japan", "bubble": "はい、…！",
      "bubble_en": "Yes, ...! (EN translation shown under the JP line)",
      "stamp_wrong": "WRONG WAY", "stamp_right": "RIGHT WAY"}
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1080, 1920
ORANGE = (255, 157, 46)
INK = (20, 22, 28)
RED = (214, 40, 40)
GREEN = (26, 168, 84)


def font(size, jp=False):
    cands = (["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"] if jp else
             ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
              "/usr/share/fonts/opentype/noto/NotoSansCJKjp-Bold.otf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"])
    for p in cands:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def fit(text, max_w, size, jp=False):
    d = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    while size > 18 and d.textlength(text, font=font(size, jp)) > max_w:
        size -= 3
    return font(size, jp)


def rrect(d, box, r, **kw):
    d.rounded_rectangle(box, radius=r, **kw)


def led_text(img, cx, cy, text, size):
    """orange LED-style text: blurred glow passes + sharp core (mirrors pov.js)"""
    f = fit(text, 960, size)
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.text((cx, cy), text, font=f, fill=ORANGE + (255,), anchor="mm")
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(16)))
    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(5)))
    d = ImageDraw.Draw(img)
    d.text((cx, cy), text, font=f, fill=(255, 176, 84, 255), anchor="mm")


# ---------------------------------------------------------------- stamps
def _stamp(text, color, path):
    f = font(150)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f))
    w, h = tw + 130, 250
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (10, 10, w - 10, h - 10), 26, outline=color + (255,), width=16)
    rrect(d, (34, 34, w - 34, h - 34), 16, outline=color + (255,), width=5)
    d.text((w / 2, h / 2 + 4), text, font=f, fill=color + (255,), anchor="mm")
    rnd = random.Random(7)  # ink distress: sparse speckles -> rubber stamp feel
    px = img.load()
    for _ in range(2600):
        x, y = rnd.randrange(w), rnd.randrange(h)
        r, g, b, a = px[x, y]
        if a > 40:
            px[x, y] = (r, g, b, int(a * rnd.uniform(0.25, 0.8)))
    img = img.rotate(-12, resample=Image.BICUBIC, expand=True)
    img.save(path)
    print("stamp", path, img.size)


def _pill(text, fill_rgba, fnt, path, pad_x=72, height=108, radius=54):
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=fnt))
    w, h = tw + pad_x, height
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (2, 2, w - 2, h - 2), radius, fill=fill_rgba)
    d.text((w / 2, h / 2 + 2), text, font=fnt, fill=(255, 255, 255, 255), anchor="mm")
    img.save(path)
    print("pill", path, img.size)


def _bubble(text, path, en=None):
    """JP speech bubble. 2026-11-24 dialogue rule: when a Japanese character
    speaks, the bubble shows the JP line on top with its EN translation
    directly underneath (smaller, muted). Pass the translation as `en`."""
    lines = text.split("\n")
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    if len(lines) == 1 and not en:
        f = fit(text, 800, 68, jp=True)
        d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
        tw = int(d0.textlength(text, font=f))
        w, h = tw + 84, 150
        img = Image.new("RGBA", (w, h + 46), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        rrect(d, (2, 2, w - 2, h - 2), 34, fill=(255, 255, 255, 255))
        d.polygon([(70, h - 8), (128, h - 8), (82, h + 42)], fill=(255, 255, 255, 255))
        d.text((w / 2, h / 2 + 2), text, font=f, fill=INK + (255,), anchor="mm")
        img.save(path)
        print("bubble", path, img.size)
        return
    # multi-line: fit the widest JP line to 300px so the bubble fits the
    # free space right of the speaker (frame is 1080 wide)
    size = 60
    while size > 18 and max(d0.textlength(s, font=font(size, jp=True)) for s in lines) > 300:
        size -= 3
    f = font(size, jp=True)
    jp_w = max(int(d0.textlength(s, font=f)) for s in lines)
    lh = f.size + 12
    # EN translation line(s): smaller latin font, fit to 420px, muted ink
    en_lines = en.split("\n") if en else []
    fe, en_w, en_lh = None, 0, 0
    if en_lines:
        esize = max(18, int(size * 0.62))
        fe = font(esize)
        while esize > 16 and max(d0.textlength(s, font=fe) for s in en_lines) > 420:
            esize -= 2
            fe = font(esize)
        en_w = max(int(d0.textlength(s, font=fe)) for s in en_lines)
        en_lh = fe.size + 10
    w = max(jp_w, en_w) + 72
    h = lh * len(lines) + (10 + en_lh * len(en_lines) if en_lines else 0) + 44
    img = Image.new("RGBA", (w, h + 46), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (2, 2, w - 2, h - 2), 34, fill=(255, 255, 255, 255))
    d.polygon([(70, h - 8), (128, h - 8), (82, h + 42)], fill=(255, 255, 255, 255))
    y = h / 2 - (len(lines) - 1) * lh / 2 - (en_lh * len(en_lines) + 10) / 2 if en_lines else h / 2 - (len(lines) - 1) * lh / 2
    for s in lines:
        d.text((w / 2, y + 2), s, font=f, fill=INK + (255,), anchor="mm")
        y += lh
    if en_lines:
        y += 10
        for s in en_lines:
            d.text((w / 2, y + 2), s, font=fe, fill=(90, 90, 108, 255), anchor="mm")
            y += en_lh
    img.save(path)
    print("bubble", path, img.size)


def build_art(outdir, cfg):
    os.makedirs(outdir, exist_ok=True)
    _stamp(cfg.get("stamp_wrong", "WRONG WAY"), RED, os.path.join(outdir, "stamp_wrong.png"))
    _stamp(cfg.get("stamp_right", "RIGHT WAY"), GREEN, os.path.join(outdir, "stamp_right.png"))
    _pill(cfg["title"], (10, 10, 12, 242), fit(cfg["title"], 950, 58), os.path.join(outdir, "pill_title.png"))
    _pill("THE RIGHT WAY", GREEN + (255,), font(84), os.path.join(outdir, "pill_rightway.png"), pad_x=110, height=148, radius=74)
    _bubble(cfg["bubble"], os.path.join(outdir, "bubble_shout.png"), cfg.get("bubble_en"))
    return outdir
