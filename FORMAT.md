# Format spec — learned from @thejapanlogic (Japan Logic), analyzed 2026-11-15

Reference reels: konbini cash tray (DfscVEHAQWs, 3.4k likes), ramen ticket machine (DfvjjmogNRP, 16.6k likes). Audio length ~46s.

## What the reference actually is
- NOT live action. Flat 2D illustration / pop-art animation, AI-generated (Instagram labels it AI content).
- **Our differentiator: same format and camera grammar, rendered in real 3D** (Three.js engine from moshimo-reels).

## Camera grammar (to reproduce)
- First-person POV the whole way. The protagonist is never seen except **two hands + mustard-color sleeves at the bottom of the frame**.
- Slow push-in / walking drift between beats; mostly locked-off cuts per beat.
- Counter scenes are framed over-the-counter at the staff member (eye level).

## Structure (every episode, ~40-50s)
1. **Cold open — the WRONG way (0-3s).** POV hand does the intuitive-but-wrong thing (hands cash directly to the clerk). Staff reacts with a short Japanese line in a speech bubble (「いや、いや、いや…」 / 「先に食券を！」).
2. **Title label** top of frame from second 0: black rounded label, bold white text: `POV: your first ___ in Japan`.
3. **"THE RIGHT WAY" banner** (colored band across the middle) — redo the scene correctly.
4. **Explainer card**: black background, orange LED-style big text naming the object (CASH TRAY / THE MACHINE), small caption under it. The one-line logic: why it exists.
5. **Correct-way payoff**: staff smiles, Japanese thanks (「ありがとうございます！」), POV enjoys the result (eats the ramen).
6. **Close (narration)**: rule restated + exception ("No tray? Only a machine? Feed the machine.") + sign-off line + "Follow for more."

## Audio
- Calm, clear English narration (TTS), flat delivery. No prominent BGM.
- Japanese staff lines as speech bubbles + short JP voice clips.

## Caption template (from the account's posts)
```
POV: your first ___ in Japan. <counter-intuitive rule in one sentence>. <emoji>

<2-3 sentences: the logic + the exception.>

<question to the viewer> 👇

#japantravel #japantrip #firsttimeinjapan <topic tag> #japantips
```

## What performs (their last ~33 posts)
- POV first-timer rules dominate their top posts: ramen ticket 16.6k, night-out tout warning 3.7k, konbini tray 3.4k, tax-free news 2.0k.
- Non-POV "saw the viral X?" follow-ups and niche rules sit at 16-200 likes. **Stick to POV first-timer rules about daily-life scenes.**

## Production checklist — view-count rules (every episode, no exceptions)

Proven on the sister account @moshimo.simulation (28-day Instagram data, 2026-11-15: median watch ~17s of ~66s videos; 99% of views from non-followers; comments near zero until the caption carried a question). Encoded in `engine/engine/pov.js`, `engine/episodes/ep01_konbini_tray.js` (the model episode) and `.github/prompts/daily.md`.

### Length & structure
- [ ] Total length **38–48s** (reference format is ~46s; moshimo cut 58–68s → 38–50s for the same reason).
- [ ] The payoff — correct-way success **and** the one-line logic — lands by **~55% of runtime at the latest** (moshimo's twist at 60–70% never reached most viewers; it was moved to ~50%).
- [ ] After the payoff, keep feeding new information (origin detail, exception, payoff shot) so nobody leaves at the answer.
- [ ] The scene section ends with **one quotable punchline** (the exception or absurd-but-true detail, e.g. "No tray? Only a machine? Feed the machine.") with the success SFX + a slight camera push-in — **then** the follow pill. Never end on the explanation.
- [ ] Follow pill in the final shot ("Follow for more first times in Japan").

### Hook
- [ ] Frame 0 already shows the situation **and** the title label. No intro, no logo.
- [ ] The WRONG action starts within the **first 1 second** (hand already moving at t=0).
- [ ] The first narration line **is the counter-intuitive rule itself** — not a greeting, not scene-setting.

### Pacing （間の長さ）
- [ ] No dead air: a visual change, camera move, bubble or new telop at least every **2–3 seconds**.
- [ ] Cuts land on narration phrase boundaries (one shot = one or two narration lines).
- [ ] The only deliberate silence is **0.3–0.5s right before the explainer card / punchline** (ep01 uses `pre: 0.5` on the card shot).
- [ ] Narration sentences are short; line gaps in the voice timing stay at the pipeline default (0.2s) — no long pauses between lines.

### Telops (burned into `pov.js` — do not improvise per episode)
- [ ] One idea per telop, **max ~7 English words** on screen at once (plus the JP speech bubble).
- [ ] Main telop (narration caption): **88px** at 1080 wide (rule: ≥64px), white bold + ink outline, baseline **y=1300** — lower-third, above the hands.
- [ ] Title label: black rounded label, top of frame (y≈268), present from second 0 to the end.
- [ ] Telops never cover the key prop (tray / ticket machine) or the staff member's face.
- [ ] Same positions in every episode — viewers learn the layout.

### Sound (moshimo SFX cue system; every beat gets a cue)
- [ ] Whoosh on scene changes / hand moves (`whoosh_swing`, `whoosh_switch1/2`, `whoosh_slide`).
- [ ] Impact/pop on the wrong-way moment (`impact_don` at the cold-open punch).
- [ ] Register "pi" beep + coin/cash sounds at payment (`beep.mp3` episode file, `coin_toss`).
- [ ] Sparkle/success on the correct-way payoff and on the punchline (`sparkle`, `text_pa`).
- [ ] `text_tin` tick as each telop line appears.
- [ ] Low room tone under the whole video (`roomtone.mp3` episode file at −34dB); JP staff voice clips timed to their bubbles.
- [ ] No silent stretch over ~2s except the deliberate pre-card beat.

### Caption (posted text)
- [ ] Line 1 carries a **two-choice question** (this is what finally produced comments on the sister account).
- [ ] Hashtags checked letter by letter — a typo'd hashtag once shipped on the sister account and is a standing embarrassment. Fixed set: `#japantravel #japantrip #firsttimeinjapan #japantips` + one topic tag.
