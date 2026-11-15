"""Programmatic art for ep02_ramen_ticket (2D copy-format episode).

Generates into episodes/ep02_ramen_ticket_art/:
  stamp_wrong.png / stamp_right.png  - verdict stamps (transparent, rotated -12deg)
  pill_title.png                     - black title pill (top of frame, from second 0)
  pill_rightway.png                  - green "THE RIGHT WAY" pill
  bubble_shout.png                   - JP speech bubble for the owner's shout
  card1.png / card2.png / card3.png  - black explainer cards, orange LED text + icon
  endcard.png                        - circular stamp end card (Japan First Times)

usage: python ep02_ramen_ticket_assets.py
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "ep02_ramen_ticket_art")
os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1920
ORANGE = (255, 157, 46)
INK = (20, 22, 28)
RED = (214, 40, 40)
GREEN = (26, 168, 84)


def font(size, jp=False):
    cands = (["/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"] if jp else
             ["/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
              "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
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
def stamp(text, color, path):
    f = font(150)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f))
    w, h = tw + 130, 250
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (10, 10, w - 10, h - 10), 26, outline=color + (255,), width=16)
    rrect(d, (34, 34, w - 34, h - 34), 16, outline=color + (255,), width=5)
    d.text((w / 2, h / 2 + 4), text, font=f, fill=color + (255,), anchor="mm")
    # ink distress: erase sparse speckles so it reads as a rubber stamp
    rnd = random.Random(7)
    px = img.load()
    for _ in range(2600):
        x, y = rnd.randrange(w), rnd.randrange(h)
        r, g, b, a = px[x, y]
        if a > 40:
            px[x, y] = (r, g, b, int(a * rnd.uniform(0.25, 0.8)))
    img = img.rotate(-12, resample=Image.BICUBIC, expand=True)
    img.save(path)
    print("stamp", path, img.size)


# ---------------------------------------------------------------- pills & bubble
def pill_title():
    text = "POV: your first ramen shop in Japan"
    f = fit(text, 950, 58)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f))
    w, h = tw + 72, 108
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (2, 2, w - 2, h - 2), 54, fill=(10, 10, 12, 242))
    d.text((w / 2, h / 2 + 2), text, font=f, fill=(255, 255, 255, 255), anchor="mm")
    img.save(os.path.join(OUT, "pill_title.png")); print("pill_title", img.size)


def pill_rightway():
    text = "THE RIGHT WAY"
    f = font(84)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f))
    w, h = tw + 110, 148
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (2, 2, w - 2, h - 2), 74, fill=GREEN + (255,))
    d.text((w / 2, h / 2 + 3), text, font=f, fill=(255, 255, 255, 255), anchor="mm")
    img.save(os.path.join(OUT, "pill_rightway.png")); print("pill_rightway", img.size)


def bubble_shout():
    text = "はい、ラーメン一丁！"
    f = fit(text, 800, 68, jp=True)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength(text, font=f))
    w, h = tw + 84, 150
    img = Image.new("RGBA", (w, h + 46), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    rrect(d, (2, 2, w - 2, h - 2), 34, fill=(255, 255, 255, 255))
    d.polygon([(70, h - 8), (128, h - 8), (82, h + 42)], fill=(255, 255, 255, 255))
    d.text((w / 2, h / 2 + 2), text, font=f, fill=INK + (255,), anchor="mm")
    img.save(os.path.join(OUT, "bubble_shout.png")); print("bubble_shout", img.size)


# ---------------------------------------------------------------- explainer cards
def card_base():
    return Image.new("RGBA", (W, H), (5, 5, 5, 255))


def icon_machine(d, cx, top):
    w, h = 300, 400
    x0, y0 = cx - w // 2, top
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 22, outline=ORANGE, width=9)
    d.rectangle((x0, y0, x0 + w, y0 + 74), fill=ORANGE)
    for r in range(3):
        for c in range(3):
            bx, by = x0 + 34 + c * 82, y0 + 108 + r * 66
            d.rounded_rectangle((bx, by, bx + 58, by + 42), 8, outline=ORANGE, width=6)
    d.rectangle((x0 + 34, y0 + h - 62, x0 + w - 34, y0 + h - 34), outline=ORANGE, width=6)


def icon_ticket(d, cx, top):
    w, h = 400, 230
    x0, y0 = cx - w // 2, top
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 18, outline=ORANGE, width=9)
    for yy in range(y0 + 18, y0 + h - 10, 26):  # perforation
        d.ellipse((x0 + 16, yy, x0 + 26, yy + 10), fill=ORANGE)
        d.ellipse((x0 + w - 26, yy, x0 + w - 16, yy + 10), fill=ORANGE)
    f = font(96)
    d.text((cx, y0 + h / 2), "¥850", font=f, fill=ORANGE, anchor="mm")


def icon_owner(d, cx, top):
    d.ellipse((cx - 105, top, cx + 105, top + 210), outline=ORANGE, width=9)
    d.arc((cx - 105, top + 6, cx + 105, top + 216), start=180, end=360, fill=ORANGE, width=26)  # hachimaki band
    d.arc((cx - 150, top + 268, cx + 150, top + 470), start=180, end=360, fill=ORANGE, width=9)  # shoulders
    f = fit("ORDER HERE", 300, 52)
    tw = int(ImageDraw.Draw(Image.new("RGBA", (8, 8))).textlength("ORDER HERE", font=f))
    d.rounded_rectangle((cx - tw // 2 - 30, top + 330, cx + tw // 2 + 30, top + 418), 14, outline=ORANGE, width=7)
    d.text((cx, top + 374), "ORDER HERE", font=f, fill=ORANGE, anchor="mm")


def card(name, big, icon):
    img = card_base()
    d = ImageDraw.Draw(img)
    icon(d, W // 2, 400)
    led_text(img, W // 2, 1080, big, 150)
    img.convert("RGB").save(os.path.join(OUT, name), quality=92)
    print(name)


# ---------------------------------------------------------------- end stamp card
def arc_text(img, cx, cy, radius, text, f, color, span_deg):
    """Text along the TOP arc, reading left to right (verified mode-A geometry).
    Position: (cx + r*sin(phi), cy - r*cos(phi)), phi = clockwise-from-top angle;
    each glyph is rotated by -phi (PIL rotate appears clockwise-positive on screen)."""
    n = len(text)
    for i, ch in enumerate(text):
        t = i / max(1, n - 1)
        phi = math.radians(-span_deg + 2 * span_deg * t)
        x, y = cx + radius * math.sin(phi), cy - radius * math.cos(phi)
        ch_img = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
        cd = ImageDraw.Draw(ch_img)
        cd.text((65, 65), ch, font=f, fill=color + (255,), anchor="mm")
        ch_img = ch_img.rotate(-math.degrees(phi), resample=Image.BICUBIC, center=(65, 65))
        img.alpha_composite(ch_img, (int(x - 65), int(y - 65)))


def arc_text_bottom(img, cx, cy, radius, text, f, color, span_deg):
    """Text along the BOTTOM arc, reading left to right, heads toward the centre.
    Position: (cx + r*sin(phi), cy + r*cos(phi)); glyph PIL rotation = +phi degrees."""
    n = len(text)
    for i, ch in enumerate(text):
        t = i / max(1, n - 1)
        phi = math.radians(-span_deg + 2 * span_deg * t)
        x, y = cx + radius * math.sin(phi), cy + radius * math.cos(phi)
        ch_img = Image.new("RGBA", (130, 130), (0, 0, 0, 0))
        cd = ImageDraw.Draw(ch_img)
        cd.text((65, 65), ch, font=f, fill=color + (255,), anchor="mm")
        ch_img = ch_img.rotate(math.degrees(phi), resample=Image.BICUBIC, center=(65, 65))
        img.alpha_composite(ch_img, (int(x - 65), int(y - 65)))


def endcard():
    img = card_base()
    cx, cy, R = W // 2, 900, 400
    stamp_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(stamp_img)
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=ORANGE, width=14)
    d.ellipse((cx - R + 44, cy - R + 44, cx + R - 44, cy + R - 44), outline=ORANGE, width=5)
    arc_text(stamp_img, cx, cy, R - 88, "JAPAN FIRST TIMES", font(64), ORANGE, 62)
    arc_text_bottom(stamp_img, cx, cy, R - 88, "FOLLOW FOR MORE", font(58), ORANGE, 56)
    d = ImageDraw.Draw(stamp_img)
    d.text((cx, cy - 108), "CASE No.1", font=fit("CASE No.1", 420, 54), fill=(245, 245, 245, 255), anchor="mm")
    d.text((cx, cy + 6), "RAMEN", font=font(118), fill=(255, 255, 255, 255), anchor="mm")
    d.text((cx, cy + 108), "TICKET", font=font(118), fill=(255, 255, 255, 255), anchor="mm")
    # small bowl glyph under the title
    d.arc((cx - 74, cy + 168, cx + 74, cy + 268), start=0, end=180, fill=ORANGE, width=9)
    d.line((cx - 74, cy + 218, cx + 74, cy + 218), fill=ORANGE, width=9)
    d.line((cx - 30, cy + 150, cx + 44, cy + 196), fill=ORANGE, width=8)
    d.line((cx + 2, cy + 142, cx + 76, cy + 188), fill=ORANGE, width=8)
    stamp_img = stamp_img.rotate(-6, resample=Image.BICUBIC, center=(cx, cy))
    img.alpha_composite(stamp_img)
    img.convert("RGB").save(os.path.join(OUT, "endcard.png"), quality=92)
    print("endcard")


if __name__ == "__main__":
    stamp("WRONG WAY", RED, os.path.join(OUT, "stamp_wrong.png"))
    stamp("RIGHT WAY", GREEN, os.path.join(OUT, "stamp_right.png"))
    pill_title(); pill_rightway(); bubble_shout()
    card("card1.png", "THE MACHINE", icon_machine)
    card("card2.png", "TICKET FIRST", icon_ticket)
    card("card3.png", "AT COUNTER", icon_owner)
    endcard()
