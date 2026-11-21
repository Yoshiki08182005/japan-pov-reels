# ep21 pour_beer — production note (2026-11-21 night slot, NOT posted)

Topic: pour_beer (food, izakaya table). Rule: "Never pour your own beer — pour for
others, and hold your glass with two hands." Hook: hook_library #1 (Tier A, wrong
action at t=0 + freeze/stare + staff shout). Previous post: ep20 matsuri_garbage
(events) — no category clash, no topic duplication.

## What was produced
- Frames f1..f9 (1152x2048, flat 2D, fixed style block): OK, verified visually
  (f1 wrong-action pour with everyone staring; f8 payoff with two-handed glass).
- Clips (704x1248, 24fps, 10s): chapter / accept / shout / waiting — OK, saved as
  stable names + original media-generation files. Motion check (1s-step frame
  diffs): chapter 11–16, accept 13–30, shout 30–56, waiting 18–23 — all four are
  genuinely animated clips, not stills.

## What failed — DO NOT RETRY in this run
- Clip generation for freeze.mp4 (from f1, the 0s opening freeze sequence) and
  payoff.mp4 (from f8, the success moment) was refused by the media tool's safety
  check (integrity_check_failed). Per the run's instruction, these two requests
  must not be retried or rewritten here, and must not be routed around.
- Without the freeze clip there is no opening beat (second 0) and without the
  payoff clip there is no success moment: the episode cannot be built in the
  approved standard format and cannot pass the self-verification gate.
  Verdict reuses the freeze clip, so it is blocked too.

## State / next steps
- Episode NOT built, NOT posted. No spec/script/next.json written for ep21;
  topics.json pour_beer stays used=null.
- A later run (new request) may retry the two clip generations — the tool decides
  then — and resume from the frames + 4 clips already committed here.
- Night slot 2026-11-21 21:30 JST has no new post from this run.
- UPDATE 2026-11-22 morning run: the retry was attempted for both clips and refused again by the media tool's safety check (integrity_check_failed, same two requests). Per the run's instruction these two requests are not retried again here. Morning slot switched to the fallback topic oshibori (ep21) per daily.md; pour_beer stays used=null in topics.json.
