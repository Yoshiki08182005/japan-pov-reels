# japan-pov-reels

Daily Instagram Reels system: **first-person POV 3D shorts that teach English speakers how everyday Japan actually works** — one counter-intuitive rule per episode (cash tray, ticket machine, manner mode…), grounded in realistic daily-life scenes: retail, food, transit, conversation, events.

It reuses the Three.js engine and production pipeline of the sister project [moshimo-reels](https://github.com/Yoshiki08182005/moshimo-reels) (@moshimo.simulation), with a new format layer on top. The reference for the format is @thejapanlogic's POV reels — same camera grammar and structure, rendered in real 3D instead of flat illustration.

## The format (see FORMAT.md for the full spec + checklist)

~40–50s vertical (1080×1920), first-person throughout — the protagonist is only two 3D hands with mustard sleeves at the bottom of the frame.

1. **Cold open (0–3s):** the POV hand does the WRONG thing; the staff character reacts with a Japanese speech bubble + JP voice clip. The black title label `POV: your first ___ in Japan` is on screen from second 0.
2. **First narration line = the rule itself** (no greeting). Calm English TTS (edge-tts, en-US-AriaNeural).
3. **"THE RIGHT WAY" banner** → the scene redone correctly.
4. **Explainer card:** black card, big orange LED-style object name (CASH TRAY) + one line of logic. A 0.5s beat of silence lands right before it.
5. **Payoff:** staff smiles, 「ありがとうございます！」 bubble, change returns on the tray; then a detail beat, a quotable **punchline** (exception / absurd-but-true), and the **"Follow for more" pill**.

View-count rules baked into the format (from the sister account's 28-day data — full checklist in FORMAT.md): 38–48s total; payoff by ~55% of runtime; a visual change every 2–3s; telops ≤7 words at 88px in a fixed lower-third slot; an SFX cue on every beat; caption line 1 is a two-choice question; hashtags proofread letter by letter.

## Layout

| Path | What |
|---|---|
| `FORMAT.md` | Format spec learned from the reference account + the production checklist |
| `TOPICS.md` | The 17-topic bank (retail → food → transit → conversation → events) |
| `engine/` | The app (copied from moshimo-3d; `engine/engine/core.js` + `kit*.js` are the original engine, untouched) |
| `engine/engine/pov.js` | **New:** the POV overlay runner — title label, speech bubbles, banner, explainer card, telops, follow pill |
| `engine/engine/kitpov.js` | **New:** konbini scene (counter, blue cash tray, register screen ¥550, drink fridge, shelves, clerk in green/white) + the POV hands rig |
| `engine/episodes/ep01_konbini_tray.*` | Episode 1 (model episode): `.js` shots, `.script.json`, `.voice.json`, `_voice/` narration, `_jp/` staff clips, `_sfx/` register beep + room tone |
| `engine/topics.json` | Production queue (17 topics, slug/scene/rule/narration/title) |
| `tools/publish.py` | Instagram posting, **triple-gated** (see below) |
| `tools/fetch_sfx.py` | Downloads the SFX library files from their source (never committed) |
| `.github/prompts/daily.md` | The daily production prompt (Claude Code) |
| `.github/workflows/daily.yml` | Daily 07:00 JST run: produce → (gated) publish → save → notify |

## Run it locally

```bash
pip install playwright pillow edge-tts && python -m playwright install chromium
cd engine && npm ci
python ../tools/fetch_sfx.py          # SFX audio files (license: no redistribution)
python voice.py ep01_konbini_tray     # (re)generate narration — needs a direct internet connection
python render.py ep01_konbini_tray stills 0.8 7.4 13.5 21.5 37.5   # proof frames -> out/ep01_konbini_tray/sheet.jpg
python render.py ep01_konbini_tray full                             # full video -> out/ep01_konbini_tray/final.mp4
```

## Status / what remains

- ✅ Engine, format layer, konbini scene, episode 1 shots/timing, topics queue, workflow, gated publisher.
- ⚠️ **Episode 1's voice files are placeholder timing** (silent MP3s + estimated durations, marked in `ep01_konbini_tray.voice.json`): this build machine's egress proxy blocks the Edge TTS websocket, so real narration could not be synthesized here. Run `python voice.py ep01_konbini_tray` once on any direct connection (the GitHub Actions `render-only` mode does exactly this) to get the real voice + timings before a full render. The JP staff clips in `ep01_konbini_tray_jp/` are likewise silent placeholders.
- ⛔ **No Instagram account yet — nothing can be posted.** Creating the account needs the user (email/SMS verification code is theirs to enter). Publishing is disabled by default and cannot hit the wrong account:
  1. Create the Instagram account (user, with their verification code) and switch it to a professional account.
  2. Create/select a Meta app at developers.facebook.com, add the Instagram Graph API, connect the account, and mint a long-lived system-user token with `instagram_content_publish`.
  3. In THIS repo only: set variable `IG_USER_ID`, secret `IG_ACCESS_TOKEN`, variable `JAPAN_POV_USERNAME` (the new account's username), and finally variable `JAPAN_POV_PUBLISH=true`. `tools/publish.py` re-verifies the token's username against `JAPAN_POV_USERNAME` before uploading, and the moshimo-reels credentials are never read here.
  4. Set secret `CLAUDE_CODE_OAUTH_TOKEN` for the production step, and optionally variable `NOTIFY_ISSUE` (issue number for run reports).
