"""Placeholder voice for local assembly tests (mirrors ep01's placeholder approach).

Real voices come from voice.py (edge-tts) in GitHub Actions; this VM cannot reach
the TTS service. Writes silent mp3s with estimated durations + episodes/<ep>.voice.json
so build_2d.py can be exercised end-to-end. voice.py overwrites everything when run.

usage: python placeholder_voice.py EP [EP_JP ...]
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PUNCT = re.compile(r"[\s、。！？!?「」『』（）()・…,.\-ー〜~：:]")


def norm(s):
    return PUNCT.sub("", s)


def estimate(text):
    n = len(norm(text))
    return max(0.9, n / 13.5 + 0.25)


def make(ep):
    sc = json.load(open(os.path.join(ROOT, "episodes", ep + ".script.json"), encoding="utf-8"))
    vdir = os.path.join(ROOT, "episodes", ep + "_voice"); os.makedirs(vdir, exist_ok=True)
    res = {"_note": "PLACEHOLDER TIMING (silent audio, estimated durations). Regenerate with voice.py before any real render.",
           "voice": sc["voice"], "rate": sc.get("rate", "+0%"), "lines": {}}
    for ln in sc["lines"]:
        chunks = [c for c in ln["text"].split("|") if c]
        plain = [c.replace("[", "").replace("]", "") for c in chunks]
        dur = estimate("".join(plain))
        path = os.path.join(vdir, ln["id"] + ".mp3")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
                        "-t", f"{dur:.2f}", "-c:a", "libmp3lame", "-b:a", "128k", path], check=True)
        lens = [max(1, len(norm(c))) for c in plain]; total = sum(lens); acc = 0; ts = []
        for L in lens:
            ts.append(round(dur * acc / total, 3)); acc += L
        res["lines"][ln["id"]] = {"file": f"{ep}_voice/{ln['id']}.mp3", "dur": round(dur, 3),
                                  "chunks": [{"t": t, "text": c} for t, c in zip(ts, chunks)]}
        print(f"{ep} {ln['id']:8s} {dur:5.2f}s (placeholder)")
    json.dump(res, open(os.path.join(ROOT, "episodes", ep + ".voice.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    for ep in sys.argv[1:]:
        make(ep)
