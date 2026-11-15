"""Assemble the ep02 copy-format episode WITH REAL MOTION (v2). Same beat sheet,
timeline, voices, karaoke subs, SE and BGM as build_2d.py (v1 stills version),
but the living beats are image-to-video clips generated from the v1 frames:
steam, cooking, eating, hands moving. The freeze stays a still — that contrast
is the gag. Stamps / jump cut / LED cards / end card stay graphic elements.

  python build_2d_v2.py ep02_ramen_ticket

Needs (all under episodes/):
  <ep>_frames/f1..f9 *.jpg          AI-generated stills (see COPY_SPEC art spec)
  <ep>_clips/<beat>.mp4             i2v clips for CLIP_SEGS beats (704x1248, 24fps)
  <ep>_art/*.png                    from episodes/<ep>_assets.py (stamps, pills, cards)
  <ep>.voice.json + <ep>_voice/     EN narration (real TTS files, reused from v1)
  <ep>_jp.voice.json + <ep>_jp_voice/  JP shout line
Outputs: out/<ep>/final.mp4, cover.jpg, sheet.jpg, meta.json
"""
import json, math, os, subprocess, sys
from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.abspath(__file__))
SFX = os.path.join(os.path.dirname(ROOT), "sfx-library")
FPS = 30
W, H = 1080, 1920
MAX_MB = float(os.environ.get("MOSHIMO_MAX_MB", 9.6))

EP = sys.argv[1] if len(sys.argv) > 1 else "ep02_ramen_ticket"
EPD = os.path.join(ROOT, "episodes")
FRAMES = os.path.join(EPD, EP + "_frames")
CLIPD = os.path.join(EPD, EP + "_clips")
ART = os.path.join(EPD, EP + "_art")
OUT = os.path.join(ROOT, "out", EP)
ANIM = os.path.join(OUT, "anim")
os.makedirs(ANIM, exist_ok=True)


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

# ---------------------------------------------------------------- timeline (COPY_SPEC beat sheet)
# name, image, dur, zoom0, zoom1
SEGS = [
    ("freeze",   "f1_freeze.jpg",   3.0, 1.00, 1.05),
    ("machine",  "f2_machine.jpg",  2.0, 1.00, 1.03),
    ("exterior", "f3_exterior.jpg", 2.0, 1.00, 1.03),
    ("insert",   "f4_insert.jpg",   2.2, 1.00, 1.04),
    ("ticket",   "f5_ticket.jpg",   1.8, 1.00, 1.03),
    ("shout",    "f6_shout.jpg",    4.0, 1.00, 1.02),
    ("waiting",  "f7_waiting.jpg",  4.0, 1.00, 1.02),
    ("bowl",     "f8_bowl.jpg",     4.0, 1.00, 1.03),
    ("empty",    "f9_empty.jpg",    4.0, 1.02, 1.02),   # jump cut: same scale, held
]
# beats replaced by generated motion clips: name -> (clip file, source in-point s)
# freeze / machine / ticket / empty stay stills on purpose (gag + punctuation);
# cards and endcard are graphics.
CLIP_SEGS = {
    "exterior": ("exterior.mp4", 0.5),   # lantern sways, noren flutters
    "insert":   ("insert.mp4",   0.3),   # hand feeds the same ¥1000 bill into NOTES
    "shout":    ("shout.mp4",    0.0),   # owner takes ticket, bobs, shouts
    "waiting":  ("waiting.mp4",  1.0),   # ladle stirring, steam, customer slurping
    "bowl":     ("bowl.mp4",     0.5),   # steam rises, chopsticks lift noodles
}
card_durs = {}
for lid, art in [("n1", "card1.png"), ("n2", "card2.png"), ("n3", "card3.png")]:
    card_durs[lid] = max(3.0, N[lid] + 0.55)
end_dur = max(3.4, N["n4"] + 1.1)
story_end = sum(s[2] for s in SEGS)
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
SEGS += [("card1", "card1.png", card_durs["n1"], 1.0, 1.0),
         ("card2", "card2.png", card_durs["n2"], 1.0, 1.0),
         ("card3", "card3.png", card_durs["n3"], 1.0, 1.0),
         ("endcard", "endcard.png", end_dur, 1.0, 1.0)]
STARTS = {}
_t = 0.0
for name, *_rest in SEGS:
    STARTS[name] = _t; _t += dict((s[0], s[2]) for s in SEGS)[name]
TOTAL = _t
print(f"total {TOTAL:.2f}s  story {story_end:.1f}s  cards " +
      " ".join(f"{k}={v:.2f}" for k, v in card_durs.items()) + f" end={end_dur:.2f}")

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
    run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anoisesrc=color=white:duration=4.0",
         "-af", "highpass=f=3200,tremolo=f=6:d=0.45,volume=0.5", siz])
    return beep_hi, beep_lo, prt, siz


BEEP_HI, BEEP_LO, PRINT, SIZZLE = synth_sfx()
lib = json.load(open(os.path.join(SFX, "sfx.json"), encoding="utf-8"))["sfx"]


def libf(key):
    return os.path.join(SFX, lib[key]["file"])


# ---------------------------------------------------------------- video pass
inputs, filt = [], []
for name, img, dur, z0, z1 in SEGS:
    if name in CLIP_SEGS:
        cfile, cin = CLIP_SEGS[name]
        inputs += ["-ss", f"{cin:.2f}", "-t", f"{dur + 0.3:.2f}", "-i", os.path.join(CLIPD, cfile)]
    else:
        path = os.path.join(ART, img) if img.startswith(("card", "endcard")) else os.path.join(FRAMES, img)
        inputs += ["-loop", "1", "-t", f"{dur + 0.3:.2f}", "-i", path]
for off, seq in [(SLAM2_T, seq_wrong), (SLAM7_T, seq_right), (POP3_T, seq_pill), (BUB_T, seq_bub)]:
    inputs += ["-itsoffset", f"{off:.3f}", "-framerate", str(FPS), "-i", os.path.join(seq, "%03d.png")]
inputs += ["-loop", "1", "-t", f"{TOTAL:.2f}", "-i", os.path.join(ART, "pill_title.png")]
n_still = len(SEGS)
for i, (name, img, dur, z0, z1) in enumerate(SEGS):
    n = int(round(dur * FPS))
    if name in CLIP_SEGS:
        filt.append(f"[{i}:v]scale={W}:{H}:flags=lanczos,fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[s{i}]")
    elif z0 == z1:
        filt.append(f"[{i}:v]scale={W}:{H}:flags=lanczos,fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[s{i}]")
    else:
        filt.append(f"[{i}:v]scale=2304:4096:flags=lanczos,zoompan=z='{z0}+({z1}-{z0})*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W}x{H}:fps={FPS},trim=end_frame={n},setpts=PTS-STARTPTS,format=yuv420p[s{i}]")
filt.append("".join(f"[s{i}]" for i in range(n_still)) + f"concat=n={n_still}:v=1:a=0[base]")
cur = "base"
for j, idx in enumerate(range(n_still, n_still + 4)):
    filt.append(f"[{cur}][{idx}:v]overlay=0:0:eof_action=pass:shortest=0[o{j}]")
    cur = f"o{j}"
title_i = n_still + 4
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
    (0.12, libf("shock"), -8, 1.1),                       # gasp at the freeze
    (SLAM2_T, libf("impact_don"), -4, None),              # WRONG WAY slam
    (STARTS["exterior"] + 0.05, libf("whoosh_switch2"), -12, None),
    (STARTS["insert"] + 0.45, BEEP_LO, -6, None),         # bill accepted
    (STARTS["insert"] + 1.55, BEEP_HI, -6, None),         # button press
    (STARTS["insert"] + 2.75, PRINT, -7, None),           # ticket printing (spans into ticket shot)
    (STARTS["shout"] + 0.8, libf("whoosh_slide"), -15, None),
    (STARTS["waiting"], SIZZLE, -30, 4.0),                # cooking, under the wait
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
for name, img, dur, z0, z1 in SEGS:
    t = STARTS[name] + dur / 2
    p = os.path.join(OUT, f"chk_{name}.jpg")
    run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", final, "-frames:v", "1", "-q:v", "3", p])
    ims.append(PILImage.open(p).resize((270, 480)))
cols = 6; rows = (len(ims) + cols - 1) // cols
sheet = PILImage.new("RGB", (270 * cols, 480 * rows))
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * 270, (i // cols) * 480))
sheet.save(os.path.join(OUT, "sheet.jpg"), quality=88)
meta = {"ep": EP, "version": "v2-motion", "duration": round(TOTAL, 2), "starts": {k: round(v, 2) for k, v in STARTS.items()},
        "motion_beats": {k: v[0] for k, v in CLIP_SEGS.items()},
        "shout_at": round(SHOUT_T, 2), "slam_wrong_at": round(SLAM2_T, 2), "slam_right_at": round(SLAM7_T, 2)}
json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print("sheet + meta done", meta)
