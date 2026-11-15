"""Motion audit for the 1-second rule.

Samples a finished video every 0.5s, computes the mean absolute frame
difference between consecutive samples (270x480 grayscale), and checks:
  - every consecutive 0.5s pair changed visibly (a pair at/below the static
    threshold means two samples landed inside one static hold), and
  - every sliding 1.0s window contains real change (max pair diff inside
    the window well above the static threshold).
Also writes a proof strip: frame pairs 1.0s apart at the beats that were
static holds in v2 (freeze / machine / ticket / empty bowl / cards / end).

  python motion_audit.py <video.mp4> <report.txt> <strip.jpg> [meta.json]

Metrics per pair: (1) whole-frame mean abs diff; (2) strong-change fraction
(% of pixels with |diff| > 25) — catches small-area graphic animation such
as a lighting button or a karaoke word highlight, which a whole-frame mean
dilutes; (3) tile-max (max mean diff over a 6x6 tile grid) — catches local
motion such as steam or a nod. A pair counts as CHANGED when any metric
clears its bar: mean >= 1.5, strong-frac >= 0.25%, or tile-max >= 4.0.
Calibration: a re-encoded truly-static pair measures mean ~0.1-0.6,
strong-frac ~0.005%, tile-max ~1.4; the v2 static cards (karaoke only)
measured strong-frac 0.12-0.20%.
"""
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

VIDEO, REPORT, STRIP = sys.argv[1], sys.argv[2], sys.argv[3]
META = sys.argv[4] if len(sys.argv) > 4 else None
SW, SH = 270, 480
MEAN_BAR, FRAC_BAR, TILE_BAR = 1.5, 0.25, 4.0

dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", VIDEO], capture_output=True, text=True).stdout.strip())
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", VIDEO, "-vf",
                      f"fps=2,scale={SW}:{SH},format=gray", "-f", "rawvideo", "-"],
                     capture_output=True).stdout
n = len(raw) // (SW * SH)
frames = np.frombuffer(raw[:n * SW * SH], dtype=np.uint8).reshape(n, SH, SW).astype(np.float32)
times = [i * 0.5 for i in range(n)]


def pair_metrics(i):
    d = np.abs(frames[i + 1] - frames[i])
    tiles = [d[y * 80:(y + 1) * 80, x * 45:(x + 1) * 45].mean() for y in range(6) for x in range(6)]
    return float(d.mean()), float((d > 25).mean() * 100), float(max(tiles))


mets = [pair_metrics(i) for i in range(n - 1)]
changed = [m >= MEAN_BAR or f >= FRAC_BAR or t >= TILE_BAR for m, f, t in mets]
diffs = [m[0] for m in mets]

# sliding 1.0s windows: a window [t, t+1.0] spans pairs (t->t+0.5) and (t+0.5->t+1.0);
# it is static only if BOTH pairs are unchanged.
static_wins = [(times[i], mets[i], mets[i + 1]) for i in range(len(mets) - 1)
               if not changed[i] and not changed[i + 1]]
worst_win = min(range(len(mets) - 1), key=lambda i: max(diffs[i], diffs[i + 1]))
min_pair_i = int(np.argmin(diffs))

starts = {}
if META:
    starts = json.load(open(META)).get("starts", {})

lines = []
lines.append(f"MOTION AUDIT — {VIDEO}")
lines.append(f"duration {dur:.2f}s | samples every 0.5s: {n} frames, {len(mets)} consecutive pairs")
lines.append(f"metrics per pair: mean abs diff | strong-change % (pixels |diff|>25) | tile-max (6x6 grid)")
lines.append(f"a pair is CHANGED if mean >= {MEAN_BAR} or strong >= {FRAC_BAR}% or tile-max >= {TILE_BAR}")
lines.append("")
lines.append(f"min pair mean diff: {diffs[min_pair_i]:.2f} at {times[min_pair_i]:.1f}s -> {times[min_pair_i] + 0.5:.1f}s "
             f"(strong {mets[min_pair_i][1]:.3f}%, tile-max {mets[min_pair_i][2]:.1f})")
lines.append(f"median pair mean diff: {float(np.median(diffs)):.2f}")
lines.append(f"worst 1.0s window (by best pair inside): starts {times[worst_win]:.1f}s, "
             f"max pair mean {max(diffs[worst_win], diffs[worst_win + 1]):.2f}")
flagged = [(times[i], mets[i]) for i in range(len(mets)) if not changed[i]]
lines.append(f"pairs with no metric over the bar: {len(flagged)}")
for t, (m, f, tl) in flagged:
    lines.append(f"  NEAR-STATIC pair {t:.1f}s -> {t + 0.5:.1f}s  mean {m:.2f} strong {f:.3f}% tile-max {tl:.1f}")
lines.append(f"static 1.0s windows (both pairs unchanged): {len(static_wins)}")
for t, a, b in static_wins:
    lines.append(f"  STATIC WINDOW {t:.1f}s -> {t + 1.0:.1f}s")
lines.append("")
lines.append("all pairs (t -> t+0.5s): mean / strong% / tile-max")
for i, (m, f, tl) in enumerate(mets):
    lines.append(f"  {times[i]:5.1f}s  {m:7.2f}  {f:6.3f}%  {tl:6.1f}" + ("" if changed[i] else "   <-- near-static"))
verdict = "PASS" if not static_wins else "FAIL"
lines.append("")
lines.append(f"VERDICT: {verdict} — no 1s window is static" if verdict == "PASS"
             else f"VERDICT: {verdict} — static 1s windows listed above")
open(REPORT, "w").write("\n".join(lines) + "\n")
print("\n".join(lines[:14]))

# ---- proof strip: pairs 1.0s apart at the formerly-static beats
spots = []
if starts:
    spots = [("freeze", starts.get("freeze_in", 0) + 0.15),
             ("machine", starts.get("machine", 3) + 0.6),
             ("ticket", starts.get("ticket", 9) + 0.3),
             ("empty", starts.get("empty", 23) + 0.4),
             ("card1", starts.get("card1", 27) + 0.8),
             ("endcard", starts.get("endcard", 36) + 1.2)]
else:
    spots = [("t0", 0.15), ("t10", 10.0), ("t20", 20.0)]
tiles = []
for label, t in spots:
    pair = []
    for tt in (t, t + 1.0):
        p = f"/tmp/audit_{label}_{tt:.1f}.jpg"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{tt:.2f}", "-i", VIDEO,
                        "-frames:v", "1", "-q:v", "3", p], check=True)
        pair.append(Image.open(p).resize((270, 480)))
    idx = min(int(t * 2), len(diffs) - 1)
    d = ImageDraw.Draw(pair[0])
    d.rectangle((0, 452, 270, 480), fill=(0, 0, 0))
    d.text((6, 458), f"{label} {t:.1f}s vs {t + 1.0:.1f}s", fill=(255, 255, 0))
    tiles += pair
cols = 4
rows = (len(tiles) + cols - 1) // cols
strip = Image.new("RGB", (270 * cols, 480 * rows))
for i, im in enumerate(tiles):
    strip.paste(im, ((i % cols) * 270, (i // cols) * 480))
strip.save(STRIP, quality=88)
print("strip ->", STRIP)
