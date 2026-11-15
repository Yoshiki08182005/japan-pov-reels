"""Assemble the ep02 copy-format episode v3 — THE 1-SECOND RULE.

Same episode as build_2d_v2.py (real-motion i2v beats, voices, karaoke subs,
SE, BGM), rebuilt under the user's hard rule (2026-11-15): NO segment of the
video may look static for more than 1.0 second. Every beat gets real motion,
a cut, a punch-zoom, or graphic animation at intervals of 1 second or less.
A slow push-in over a still does NOT count as motion.

What changed vs v2:
  freeze 0-3s   was a 3s still. Now: 0.70s i2v lead-in (hand slides the bill
                in, scene alive) -> FREEZE SNAP at 0.70s (impact shake, gasp)
                -> freeze still held only 0.75s -> punch-zoom crop on the
                owner+bill (0.75s) -> tighter punch crop on the owner's face
                (0.80s). The freeze still reads as a freeze; nothing is
                static for more than 0.75s.
  machine 3-5s  was a still + stamp. Now an i2v clip (steam drifts in from
                the kitchen, sign glows, noren sways). Stamp slam unchanged.
  ticket ~9-11s was a still. Now an i2v clip: hand lifts the ¥850 ticket,
                paper flutters.
  empty 23-27s  was a 4s still (worst violation). Now an i2v clip (last
                steam wisp fades, owner nods, POV fist taps the counter),
                trimmed to 3.0s; the freed 1.0s went to the waiting beat
                (4.0s -> 5.0s of real cooking motion). Story stays 27.0s.
  cards         karaoke already changed sub-second; now the card art itself
                animates: card1 machine buttons light in sequence, card2
                the ¥850 ticket slides in then pulses, card3 the owner icon
                bobs and the ORDER HERE sign swings. Plus a thin progress
                bar under the narration line on every card.
  endcard       stamp slams in at the start, the ring text rotates slowly
                and continuously, FOLLOW FOR MORE pulses.

  python build_2d_v3.py ep02_ramen_ticket

Needs (all under episodes/):
  <ep>_frames/f1..f9 *.jpg            AI-generated stills
  <ep>_clips/<beat>.mp4               i2v clips (704x1248, 24fps)
  <ep>_art/*.png                      from episodes/<ep>_assets.py
  <ep>.voice.json + <ep>_voice/       EN narration (real TTS, reused)
  <ep>_jp.voice.json + <ep>_jp_voice/ JP shout line
Outputs: out/<ep>/final.mp4 (v3), cover.jpg, sheet.jpg, meta.json
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(os.path.dirname(ROOT), "sfx-library")
FPS = 30
W, H = 1080, 1920
MAX_MB = float(os.environ.get("MOSHIMO_MAX_MB", "9.6"))

EP = sys.argv[1] if len(sys.argv) > 1 else "ep02_ramen_ticket"
EPD = os.path.join(ROOT, "episodes")
FRAMES = os.path.join(EPD, EP + "_frames")
CLIPD = os.path.join(EPD, EP + "_clips")
ART = os.path.join(EPD, EP + "_art")
OUT = os.path.join(ROOT, "out", EP)
ANIM = os.path.join(OUT, "anim")
os.makedirs(ANIM, exist_ok=True)

sys.path.insert(0, EPD)
import ep02_ramen_ticket_assets as A   # font/fit/led_text helpers + palette
ORANGE = A.ORANGE


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        print("CMD FAILED:", " ".join(str(c) for c in cmd)[:300]); print(r.stderr[-1800:]); sys.exit(1)
    return r.stdout


def load_voice(name):
    p = os.path.join(EPD, name + ".voice.json")
    v = json.load(open(p, encoding="utf-8"))
    if "_note" in v:
        print(f"WARNING: {name} uses PLACEHOLDER voice timing (silent). Real render needs voice.py.")
    return v


EN = load_voice(EP)
JP = load_voice(EP + "_jp")
N = {k: v["dur"] for k, v in EN["lines"].items()}
SHOUT_DUR = JP["lines"]["shout"]["dur"]

# ---------------------------------------------------------------- derived freeze assets
def freeze_assets():
    """Punch crops of f1 + the freeze-hold sequence with an impact shake."""
    f1 = Image.open(os.path.join(FRAMES, "f1_freeze.jpg")).convert("RGB")  # 1152x2048
    mid = f1.crop((0, 169, 800, 1591)).resize((W, H), Image.LANCZOS)       # owner + bill
    mid_path = os.path.join(OUT, "f1_crop_mid.jpg"); mid.save(mid_path, quality=92)
    face = f1.crop((25, 106, 575, 1084)).resize((W, H), Image.LANCZOS)     # owner's face
    face_path = os.path.join(OUT, "f1_crop_face.jpg"); face.save(face_path, quality=92)
    hold_dir = os.path.join(ANIM, "freeze_hold"); os.makedirs(hold_dir, exist_ok=True)
    big = f1.resize((1116, 1984), Image.LANCZOS)  # 3.3% margin so the shake never shows an edge
    shakes = [(9, -6), (-7, 5), (4, -3), (-2, 1)]  # decaying impact shake, first ~0.13s
    for i in range(30):
        ox, oy = shakes[i] if i < len(shakes) else (0, 0)
        fr = big.crop((18 + ox, 32 + oy, 18 + ox + W, 32 + oy + H))
        fr.save(os.path.join(hold_dir, f"{i:03d}.png"))
    return mid_path, face_path, hold_dir


# ---------------------------------------------------------------- animated explainer cards
def card_base(title):
    img = Image.new("RGBA", (W, H), (5, 5, 5, 255))
    A.led_text(img, W // 2, 1080, title, 150)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((90, 1736, 990, 1744), 4, fill=(70, 70, 70, 255))  # progress track
    return img


def draw_progress(d, t, dur):
    w = int(900 * min(1.0, max(0.0, t / dur)))
    if w > 8:
        d.rounded_rectangle((90, 1736, 90 + w, 1744), 4, fill=ORANGE + (255,))


def draw_machine_icon(d, lit):
    x0, y0, w, h = 390, 400, 300, 400  # same geometry as assets.icon_machine
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), 22, outline=ORANGE, width=9)
    d.rectangle((x0, y0, x0 + w, y0 + 74), fill=ORANGE)
    for r in range(3):
        for c in range(3):
            bx, by = x0 + 34 + c * 82, y0 + 108 + r * 66
            if r * 3 + c == lit:
                d.rounded_rectangle((bx, by, bx + 58, by + 42), 8, fill=ORANGE)
            else:
                d.rounded_rectangle((bx, by, bx + 58, by + 42), 8, outline=ORANGE, width=6)
    d.rectangle((x0 + 34, y0 + h - 62, x0 + w - 34, y0 + h - 34), outline=ORANGE, width=6)


def ticket_layer():
    tw, th = 470, 300
    lay = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((6, 6, tw - 6, th - 6), 18, outline=ORANGE, width=9)
    for yy in range(24, th - 18, 26):  # perforation
        d.ellipse((22, yy, 32, yy + 10), fill=ORANGE)
        d.ellipse((tw - 32, yy, tw - 22, yy + 10), fill=ORANGE)
    d.text((tw / 2, 64), "ラーメン", font=A.fit("ラーメン", 300, 52, jp=True), fill=ORANGE, anchor="mm")
    d.text((tw / 2, th / 2 + 34), "¥850", font=A.font(110), fill=ORANGE, anchor="mm")
    return lay


def owner_head_layer():
    lay = Image.new("RGBA", (340, 480), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, top = 170, 0  # assets.icon_owner geometry, local coords
    d.ellipse((cx - 105, top, cx + 105, top + 210), outline=ORANGE, width=9)
    d.arc((cx - 105, top + 6, cx + 105, top + 216), start=180, end=360, fill=ORANGE, width=26)  # hachimaki
    d.ellipse((cx - 52, top + 96, cx - 34, top + 114), fill=ORANGE)  # eyes
    d.ellipse((cx + 34, top + 96, cx + 52, top + 114), fill=ORANGE)
    d.arc((cx - 30, top + 116, cx + 30, top + 164), start=20, end=160, fill=ORANGE, width=7)  # smile
    d.arc((cx - 150, top + 268, cx + 150, top + 470), start=180, end=360, fill=ORANGE, width=9)  # shoulders
    return lay


def sign_layer():
    f = A.fit("ORDER HERE", 300, 52)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength("ORDER HERE", font=f))
    lay = Image.new("RGBA", (tw + 60, 88), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle((3, 3, lay.width - 3, lay.height - 3), 14, outline=ORANGE, width=7)
    d.text((lay.width / 2, lay.height / 2), "ORDER HERE", font=f, fill=ORANGE, anchor="mm")
    return lay


def card_seq(idx, title, dur):
    outdir = os.path.join(ANIM, f"card{idx}"); os.makedirs(outdir, exist_ok=True)
    base = card_base(title)
    ticket = ticket_layer() if idx == 2 else None
    head = owner_head_layer() if idx == 3 else None
    sign = sign_layer() if idx == 3 else None
    n = int(round(dur * FPS)) + 2
    for i in range(n):
        t = i / FPS
        fr = base.copy(); d = ImageDraw.Draw(fr)
        if idx == 1:
            draw_machine_icon(d, int(t / 0.33) % 9)  # buttons light up in sequence
        elif idx == 2:
            if t < 0.45:  # slide-in with a tilt, then a steady pulse
                u = t / 0.45; e = 1 - (1 - u) ** 3
                xoff, rot, sc = -580 * (1 - e), -10 * (1 - e), 1.0
            else:
                xoff, rot, sc = 0.0, 0.0, 1 + 0.05 * math.sin(2 * math.pi * (t - 0.45) / 0.8)
            lay = ticket.rotate(rot, resample=Image.BICUBIC, expand=True) if rot else ticket
            if sc != 1.0:
                lay = lay.resize((int(lay.width * sc), int(lay.height * sc)), Image.BICUBIC)
            fr.alpha_composite(lay, (int(540 + xoff - lay.width / 2), int(515 - lay.height / 2)))
        elif idx == 3:
            bob = round(7 * math.sin(2 * math.pi * t / 0.9))  # owner bobs
            fr.alpha_composite(head, (540 - 170, 400 + bob))
            sg = sign.rotate(7 * math.sin(2 * math.pi * t / 1.15), resample=Image.BICUBIC, expand=True)  # sign swings
            fr.alpha_composite(sg, (int(540 - sg.width / 2), int(774 + bob - sg.height / 2)))
        draw_progress(d, t, dur)
        fr.convert("RGB").save(os.path.join(outdir, f"{i:03d}.png"))
    return outdir


# ---------------------------------------------------------------- animated end card
EC_CX, EC_CY, EC_R = 540, 830, 380


def endcard_static():
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    cx, cy, R = EC_CX, EC_CY, EC_R
    d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=ORANGE, width=14)
    d.ellipse((cx - R + 44, cy - R + 44, cx + R - 44, cy + R - 44), outline=ORANGE, width=5)
    d.text((cx, cy - 102), "CASE No.1", font=A.fit("CASE No.1", 400, 52), fill=(245, 245, 245, 255), anchor="mm")
    d.text((cx, cy + 4), "RAMEN", font=A.font(112), fill=(255, 255, 255, 255), anchor="mm")
    d.text((cx, cy + 102), "TICKET", font=A.font(112), fill=(255, 255, 255, 255), anchor="mm")
    d.arc((cx - 70, cy + 158, cx + 70, cy + 252), start=0, end=180, fill=ORANGE, width=9)  # bowl glyph
    d.line((cx - 70, cy + 205, cx + 70, cy + 205), fill=ORANGE, width=9)
    d.line((cx - 28, cy + 142, cx + 40, cy + 186), fill=ORANGE, width=8)
    d.line((cx + 2, cy + 134, cx + 70, cy + 178), fill=ORANGE, width=8)
    return lay


def ring_layer():
    """Full-circle ring text on its own layer so it can rotate continuously."""
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    text = "JAPAN FIRST TIMES ★ JAPAN FIRST TIMES ★ "
    f = A.font(54)
    r = EC_R - 84
    for i, ch in enumerate(text):
        phi = math.radians(i * 360.0 / len(text))
        x, y = EC_CX + r * math.sin(phi), EC_CY - r * math.cos(phi)
        ch_img = Image.new("RGBA", (120, 120), (0, 0, 0, 0))
        cd = ImageDraw.Draw(ch_img)
        cd.text((60, 60), ch, font=f, fill=ORANGE + (255,), anchor="mm")
        ch_img = ch_img.rotate(-math.degrees(phi), resample=Image.BICUBIC, center=(60, 60))
        lay.alpha_composite(ch_img, (int(x - 60), int(y - 60)))
    return lay


def follow_layer():
    f = A.fit("FOLLOW FOR MORE", 620, 60)
    d0 = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    tw = int(d0.textlength("FOLLOW FOR MORE", font=f))
    lay = Image.new("RGBA", (tw + 40, 100), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((lay.width / 2, 50), "FOLLOW FOR MORE", font=f, fill=ORANGE + (255,), anchor="mm")
    return lay


def endcard_seq(dur):
    outdir = os.path.join(ANIM, "endcard"); os.makedirs(outdir, exist_ok=True)
    S, R, F = endcard_static(), ring_layer(), follow_layer()
    n = int(round(dur * FPS)) + 2
    for i in range(n):
        t = i / FPS
        u = min(1.0, t / 0.30)                       # stamp slam: 2.5x -> 1x in 0.30s
        s = 1 + 1.5 * (1 - u) ** 3
        rot = -6 - 10 * (1 - u)                      # settles at the stamp's -6 degrees
        stamp = S.copy()
        stamp.alpha_composite(R.rotate(-14.0 * t, resample=Image.BICUBIC, center=(EC_CX, EC_CY)))  # ring rotates ~14 deg/s, never stops
        if rot:
            stamp = stamp.rotate(rot, resample=Image.BICUBIC, center=(EC_CX, EC_CY))
        if s != 1.0:
            big = stamp.resize((int(W * s), int(H * s)), Image.BICUBIC)
            canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            canvas.alpha_composite(big, (int(EC_CX - EC_CX * s), int(EC_CY - EC_CY * s)))
            stamp = canvas
        frame = Image.new("RGBA", (W, H), (5, 5, 5, 255))
        frame.alpha_composite(stamp)
        if t > 0.35:  # FOLLOW FOR MORE pulses under the stamp
            sc = 1 + 0.07 * math.sin(2 * math.pi * (t - 0.35) / 0.85)
            fw, fh = int(F.width * sc), int(F.height * sc)
            frame.alpha_composite(F.resize((fw, fh), Image.BICUBIC), (540 - fw // 2, 1330 - fh // 2))
        frame.convert("RGB").save(os.path.join(outdir, f"{i:03d}.png"))
    return outdir


# ---------------------------------------------------------------- timeline (COPY_SPEC beat sheet, 1s rule applied)
MID_CROP, FACE_CROP, FREEZE_HOLD = freeze_assets()
# kind: clip (src=(file, in-point)) / seq (src=frame dir) / still (src=path, zoom=(z0, z1))
SEGS = [
    ("freeze_in",   "clip",  ("freeze_in.mp4", 0.0), 0.70, None),        # hand slides the bill in, scene alive
    ("freeze_hold", "seq",   FREEZE_HOLD,            0.75, None),        # FREEZE snap + impact shake, held <=0.75s
    ("freeze_c1",   "still", MID_CROP,               0.75, (1.00, 1.16)),  # punch-zoom: owner + bill
    ("freeze_c2",   "still", FACE_CROP,              0.80, (1.00, 1.10)),  # punch-zoom: owner's frozen face
    ("machine",     "clip",  ("machine.mp4", 1.0),   2.0,  None),        # steam, glowing sign, swaying noren
    ("exterior",    "clip",  ("exterior.mp4", 0.5),  2.0,  None),
    ("insert",      "clip",  ("insert.mp4", 0.3),    2.2,  None),
    ("ticket",      "clip",  ("ticket.mp4", 1.2),    1.8,  None),        # ticket lifts, paper flutters
    ("shout",       "clip",  ("shout.mp4", 0.45),    4.0,  None),        # in-point skips the clip's dead first 0.5s; laugh climax lands just after the shout voice
    ("waiting",     "clip",  ("waiting.mp4", 1.0),   5.0,  None),        # +1s freed by the empty-bowl trim
    ("bowl",        "clip",  ("bowl.mp4", 0.5),      4.0,  None),
    ("empty",       "clip",  ("empty.mp4", 0.3),     3.0,  None),        # steam fades, nod, counter tap
]
card_durs = {}
for lid in ("n1", "n2", "n3"):
    card_durs[lid] = max(3.0, N[lid] + 0.55)
end_dur = max(3.4, N["n4"] + 1.1)
story_end = sum(s[3] for s in SEGS)
total = story_end + sum(card_durs.values()) + end_dur
if total > 44.0:  # clamp: shave card padding first
    over = total - 43.6
    for lid in ("n1", "n2", "n3"):
        cut = min(over, card_durs[lid] - (N[lid] + 0.28))
        if cut > 0:
            card_durs[lid] -= cut; over -= cut
    if over > 0:
        end_dur = max(N["n4"] + 0.5, end_dur - over)
    total = story_end + sum(card_durs.values()) + end_dur
if total < 38.0:
    end_dur += 38.0 - total; total = 38.0
CARD_DIRS = {1: card_seq(1, "THE MACHINE", card_durs["n1"]),
             2: card_seq(2, "TICKET FIRST", card_durs["n2"]),
             3: card_seq(3, "AT COUNTER", card_durs["n3"])}
END_DIR = endcard_seq(end_dur)
SEGS += [("card1", "seq", CARD_DIRS[1], card_durs["n1"], None),
         ("card2", "seq", CARD_DIRS[2], card_durs["n2"], None),
         ("card3", "seq", CARD_DIRS[3], card_durs["n3"], None),
         ("endcard", "seq", END_DIR, end_dur, None)]
STARTS = {}
_t = 0.0
for name, _k, _s, dur, _z in SEGS:
    STARTS[name] = _t; _t += dur
TOTAL = _t
SNAP_T = STARTS["freeze_hold"]
print(f"total {TOTAL:.2f}s  story {story_end:.1f}s  cards " +
      " ".join(f"{k}={v:.2f}" for k, v in card_durs.items()) + f" end={end_dur:.2f}  snap@{SNAP_T:.2f}")


# ---------------------------------------------------------------- animated overlays (PIL sequences)
def stamp_seq(stamp_png, outdir, dur, cx, cy, final_w):
    """slam: scale 3x -> 1x, ease-out cubic over 0.22s, hard stop, then held"""
    os.makedirs(outdir, exist_ok=True)
    st = Image.open(stamp_png).convert("RGBA")
    n = int(round(dur * FPS))
    for i in range(n):
        u = min(1.0, (i / FPS) / 0.22)
        s = 1 + 2 * (1 - u) ** 3
        w = int(final_w * s); h = int(st.height * w / st.width)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        frame.alpha_composite(st.resize((w, h)), (int(cx - w / 2), int(cy - h / 2)))
        frame.save(os.path.join(outdir, f"{i:03d}.png"))
    return outdir


def pop_seq(png, outdir, dur, cx, cy, s0=1.35, back=False):
    """quick pop-in (optional outBack overshoot), then held"""
    os.makedirs(outdir, exist_ok=True)
    im = Image.open(png).convert("RGBA")
    n = int(round(dur * FPS))
    for i in range(n):
        t = i / FPS
        if back:
            u = min(1.0, t / 0.2); c1 = 1.70158; c3 = c1 + 1
            s = 0.5 + 0.5 * (1 + c3 * (u - 1) ** 3 + c1 * (u - 1) ** 2) if u < 1 else 1.0
        else:
            u = min(1.0, t / 0.16); s = s0 + (1 - s0) * (1 - (1 - u) ** 3)
        w = int(im.width * s); h = int(im.height * s)
        frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        frame.alpha_composite(im.resize((w, h)), (int(cx - w / 2), int(cy - h / 2)))
        frame.save(os.path.join(outdir, f"{i:03d}.png"))
    return outdir


SLAM2_T = STARTS["machine"] + 0.35
SLAM7_T = STARTS["bowl"] + 0.6
POP3_T = STARTS["exterior"] + 0.2
BUB_T = STARTS["shout"] + 1.45
SHOUT_T = STARTS["shout"] + 1.5
seq_wrong = stamp_seq(os.path.join(ART, "stamp_wrong.png"), os.path.join(ANIM, "wrong"), STARTS["machine"] + 2.0 - SLAM2_T, 540, 990, 1290)
seq_right = stamp_seq(os.path.join(ART, "stamp_right.png"), os.path.join(ANIM, "right"), STARTS["bowl"] + 4.0 - SLAM7_T, 540, 920, 1240)
seq_pill = pop_seq(os.path.join(ART, "pill_rightway.png"), os.path.join(ANIM, "pill"), 2.0 - 0.2, 540, 880)
bub = Image.open(os.path.join(ART, "bubble_shout.png"))
seq_bub = pop_seq(os.path.join(ART, "bubble_shout.png"), os.path.join(ANIM, "bubble"), STARTS["shout"] + 3.8 - BUB_T, 300 + bub.width // 2, 320 + bub.height // 2, back=True)

# ---------------------------------------------------------------- karaoke subtitles (ASS)
def ass_time(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def word_events():
    """one event per word; words already spoken in orange, the rest white"""
    lines = [("n1", STARTS["card1"]), ("n2", STARTS["card2"]), ("n3", STARTS["card3"]), ("n4", STARTS["endcard"])]
    evs = []
    for lid, start in lines:
        info = EN["lines"][lid]
        words = []  # (start, end, text)
        chunks = info["chunks"]
        for ci, ch in enumerate(chunks):
            ctext = ch["text"].replace("[", "").replace("]", "")
            cstart = start + 0.12 + ch["t"]
            cend = start + 0.12 + (chunks[ci + 1]["t"] if ci + 1 < len(chunks) else info["dur"])
            ws = ctext.split()
            lens = [max(1, len(w)) for w in ws]; tot = sum(lens); acc = 0.0
            for w in ws:
                wlen = max(1, len(w))
                words.append([cstart + (cend - cstart) * acc / tot, cstart + (cend - cstart) * (acc + wlen) / tot, w])
                acc += wlen
        # wrap into 2 lines when long
        texts = [w[2] for w in words]
        brk = None
        if sum(len(x) for x in texts) > 34:
            best, acc = 10 ** 9, 0
            for i in range(1, len(texts)):
                a = len(" ".join(texts[:i])); b = len(" ".join(texts[i:]))
                if abs(a - b) < best:
                    best, brk = abs(a - b), i
        for wi, (ws_, we_, _w) in enumerate(words):
            parts = []
            for j, (_s, _e, wtxt) in enumerate(words):
                if j == brk:
                    parts.append("\\N")
                elif j > 0:
                    parts.append(" ")
                col = r"{\c&H2E9DFF&}" if j <= wi else r"{\c&HFFFFFF&}"
                parts.append(col + wtxt.replace("{", "").replace("}", ""))
            evs.append((ws_, max(we_, ws_ + 0.05), "".join(parts)))
    return evs


ass_path = os.path.join(OUT, "subs.ass")
hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: K,Noto Sans CJK JP,63,&HFFFFFF,&HFFFFFF,&H14161C,&H000000,1,0,0,0,100,100,0,0,1,7,0,2,60,60,250,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
with open(ass_path, "w", encoding="utf-8") as f:
    f.write(hdr)
    for s, e, txt in word_events():
        f.write(f"Dialogue: 0,{ass_time(s)},{ass_time(e)},K,,0,0,0,,{txt}\n")
print("subs written")

# ---------------------------------------------------------------- synthesized episode SFX
def synth_sfx():
    beep_hi = os.path.join(OUT, "beep_hi.wav"); beep_lo = os.path.join(OUT, "beep_lo.wav")
    prt = os.path.join(OUT, "print.wav"); siz = os.path.join(OUT, "sizzle.wav")
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=1319:duration=0.09", "-af", "afade=t=in:st=0:d=0.01,afade=t=out:st=0.05:d=0.04", beep_hi])
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "sine=frequency=988:duration=0.1", "-af", "afade=t=in:st=0:d=0.01,afade=t=out:st=0.06:d=0.04", beep_lo])
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anoisesrc=color=white:duration=0.65",
         "-af", "bandpass=f=2600:width_type=h:w=900,tremolo=f=28:d=0.75,afade=t=in:st=0:d=0.05,afade=t=out:st=0.5:d=0.15,volume=0.6", prt])
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anoisesrc=color=white:duration=5.2",
         "-af", "highpass=f=3200,tremolo=f=6:d=0.45,volume=0.5", siz])
    return beep_hi, beep_lo, prt, siz


BEEP_HI, BEEP_LO, PRINT, SIZZLE = synth_sfx()
lib = json.load(open(os.path.join(SFX, "sfx.json"), encoding="utf-8"))["sfx"]


def libf(key):
    return os.path.join(SFX, lib[key]["file"])


# ---------------------------------------------------------------- video pass
inputs, filt = [], []
for name, kind, src, dur, zoom in SEGS:
    if kind == "clip":
        cfile, cin = src
        inputs += ["-ss", f"{cin:.2f}", "-t", f"{dur + 0.3:.2f}", "-i", os.path.join(CLIPD, cfile)]
    elif kind == "seq":
        inputs += ["-framerate", str(FPS), "-i", os.path.join(src, "%03d.png")]
    else:
        inputs += ["-loop", "1", "-t", f"{dur + 0.3:.2f}", "-i", src]
for off, seq in [(SLAM2_T, seq_wrong), (SLAM7_T, seq_right), (POP3_T, seq_pill), (BUB_T, seq_bub)]:
    inputs += ["-itsoffset", f"{off:.3f}", "-framerate", str(FPS), "-i", os.path.join(seq, "%03d.png")]
inputs += ["-loop", "1", "-t", f"{TOTAL:.2f}", "-i", os.path.join(ART, "pill_title.png")]
n_seg = len(SEGS)
for i, (name, kind, src, dur, zoom) in enumerate(SEGS):
    n = int(round(dur * FPS))
    if kind in ("clip", "seq"):
        filt.append(f"[{i}:v]scale={W}:{H}:flags=lanczos,fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[s{i}]")
    elif zoom is None or zoom[0] == zoom[1]:
        filt.append(f"[{i}:v]scale={W}:{H}:flags=lanczos,fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[s{i}]")
    else:
        z0, z1 = zoom
        filt.append(f"[{i}:v]scale=2304:4096:flags=lanczos,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[s{i}]")
filt.append("".join(f"[s{i}]" for i in range(n_seg)) + f"concat=n={n_seg}:v=1:a=0[base]")
cur = "base"
for j, idx in enumerate(range(n_seg, n_seg + 4)):
    filt.append(f"[{cur}][{idx}:v]overlay=0:0:eof_action=pass:shortest=0[o{j}]")
    cur = f"o{j}"
title_i = n_seg + 4
filt.append(f"[{cur}][{title_i}:v]overlay=(W-w)/2:238:eof_action=pass:enable='between(t,0,{story_end:.2f})'[ot]")
filt.append(f"[ot]subtitles={ass_path}:fontsdir=/usr/share/fonts[vs]")
raw = os.path.join(OUT, "raw.mp4")
run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filt),
     "-map", "[vs]", "-t", f"{TOTAL:.3f}", "-c:v", "libx264", "-preset", "fast", "-crf", "12", "-pix_fmt", "yuv420p", raw])
print("raw video done")

# ---------------------------------------------------------------- audio pass
bgm = os.path.join(OUT, "bgm.wav")
run([sys.executable, os.path.join(ROOT, "bgm_pop.py"), bgm, f"{TOTAL:.2f}", f"{STARTS['card1']:.2f}", f"{TOTAL - 4:.2f}"])
ainputs = ["-i", bgm]
afilt = ["[0:a]volume=-16dB[b0]"]
labels = ["[b0]"]
cues = []  # (t, path, gain_db, trim_s or None)
for lid, segname in [("n1", "card1"), ("n2", "card2"), ("n3", "card3"), ("n4", "endcard")]:
    cues.append((STARTS[segname] + 0.12, os.path.join(EPD, EN["lines"][lid]["file"]), 4, None))
cues.append((SHOUT_T, os.path.join(EPD, JP["lines"]["shout"]["file"]), 7, None))
cues += [
    (SNAP_T - 0.02, libf("shock"), -8, 1.1),              # gasp lands ON the freeze snap
    (STARTS["freeze_c1"], libf("whoosh_switch2"), -14, None),  # punch-zoom whoosh
    (SLAM2_T, libf("impact_don"), -4, None),              # WRONG WAY slam
    (STARTS["exterior"] + 0.05, libf("whoosh_switch2"), -12, None),
    (STARTS["insert"] + 0.45, BEEP_LO, -6, None),         # bill accepted
    (STARTS["insert"] + 1.55, BEEP_HI, -6, None),         # button press
    (STARTS["insert"] + 2.75, PRINT, -7, None),           # ticket printing (spans into ticket shot)
    (STARTS["shout"] + 0.8, libf("whoosh_slide"), -15, None),
    (STARTS["waiting"], SIZZLE, -30, 5.0),                # cooking, under the wait
    (STARTS["bowl"] + 0.05, libf("impact_don"), -17, 0.5),  # bowl set down (soft)
    (SLAM7_T, libf("impact_don"), -4, None),              # RIGHT WAY slam
    (SLAM7_T + 0.05, libf("sparkle"), -10, None),         # success tone
    (STARTS["empty"] + 0.25, libf("end_tirin"), -12, None),  # satisfied
    (STARTS["card1"], libf("text_tin"), -16, None),
    (STARTS["card2"], libf("text_tin"), -16, None),
    (STARTS["card3"], libf("text_tin"), -16, None),
    (STARTS["endcard"] + 0.1, libf("sparkle"), -13, None),
]
for j, (t, path, gain, trim) in enumerate(cues):
    ainputs += ["-i", path]
    tr = f"atrim=0:{trim},afade=t=out:st={max(0, trim - 0.25)}:d=0.25," if trim else ""
    ms = int(t * 1000)
    afilt.append(f"[{j + 1}:a]aformat=sample_rates=44100:channel_layouts=stereo,{tr}volume={gain}dB,adelay={ms}|{ms}[c{j}]")
    labels.append(f"[c{j}]")
afilt.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=44100[a]")
audio = os.path.join(OUT, "audio.m4a")
run(["ffmpeg", "-y", "-loglevel", "error", *ainputs, "-filter_complex", ";".join(afilt),
     "-map", "[a]", "-t", f"{TOTAL:.3f}", "-c:a", "aac", "-b:a", "128k", audio])
print("audio done")

# ---------------------------------------------------------------- final encode (mirrors render.py)
vbit = int(min(8000, (MAX_MB * 8 * 1000 / TOTAL) - 140))
final = os.path.join(OUT, "final.mp4"); log = os.path.join(OUT, "x264")
base = ["-c:v", "libx264", "-preset", "veryslow", "-tune", "animation", "-b:v", f"{vbit}k", "-pix_fmt", "yuv420p", "-passlogfile", log]
run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, *base, "-pass", "1", "-an", "-f", "mp4", os.devnull])
run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-i", audio, *base, "-pass", "2", "-profile:v", "high",
     "-movflags", "+faststart", "-c:a", "copy", "-shortest", final])
print(f"final {final} {os.path.getsize(final) / 1e6:.2f}MB video {vbit}kbps")
run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", raw, "-frames:v", "1", "-q:v", "2", os.path.join(OUT, "cover.jpg")])

# contact sheet from the finished video (segment midpoints)
from PIL import Image as PILImage
ims = []
for name, kind, src, dur, zoom in SEGS:
    t = STARTS[name] + dur / 2
    p = os.path.join(OUT, f"chk_{name}.jpg")
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-q:v", "3", p])
    ims.append(PILImage.open(p).resize((270, 480)))
cols = 6; rows = (len(ims) + cols - 1) // cols
sheet = PILImage.new("RGB", (270 * cols, 480 * rows))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
sheet.save(os.path.join(OUT, "sheet.jpg"), quality=88)
meta = {"ep": EP, "version": "v3-1s-rule", "duration": round(TOTAL, 2), "starts": {k: round(v, 2) for k, v in STARTS.items()},
        "motion_beats": ["freeze_in", "machine", "exterior", "insert", "ticket", "shout", "waiting", "bowl", "empty"],
        "freeze_snap_at": round(SNAP_T, 2), "freeze_hold_s": 0.75,
        "shout_at": round(SHOUT_T, 2), "slam_wrong_at": round(SLAM2_T, 2), "slam_right_at": round(SLAM7_T, 2)}
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print("sheet + meta done", meta)
