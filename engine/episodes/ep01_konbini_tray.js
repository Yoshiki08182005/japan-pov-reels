// ep01: POV — your first konbini in Japan. Rule: cash goes on the little tray, not in the clerk's hand.
// Format rules applied (see FORMAT.md checklist): total 38-48s; wrong action starts at t=0; first narration
// line IS the rule; payoff (correct way + logic) lands by ~50%; a visual change at least every 2-3s;
// 0.35s of silence right before the explainer card; every beat has an SFX cue; the episode ends with the
// quotable punchline ("No tray? Only a machine? Feed the machine.") + push-in, THEN the follow pill.
import { runPov } from '../engine/pov.js';
import { buildKonbini, V, lerp, clamp } from '../engine/kitpov.js';
import { narrate } from './_common.js';

const voice = await (await fetch(new URL('./ep01_konbini_tray.voice.json', import.meta.url))).json();
const K = (t, a, b) => clamp((t - a) / (b - a));
const e = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const SHOW = ['tray', 'register', 'tea', 'onigiri'];
const BEEP = 'ep01_konbini_tray_sfx/beep.mp3', TONE = 'ep01_konbini_tray_sfx/roomtone.mp3';
const IYA = 'ep01_konbini_tray_jp/iya.mp3', ARIGATO = 'ep01_konbini_tray_jp/arigato.mp3';

const plan = [
  // 1) cold open (0-~2s): the WRONG way, already moving at frame 0. Hand offers cash straight to the clerk;
  //    she waves both hands and shakes her head. JP bubble + JP voice. No narration yet.
  { sc: 'kb', say: [], pre: 0, hold: 2.6, show: SHOW,
    cam: { p0: [0, 1.52, 1.68], p1: [0, 1.5, 1.57], l0: [0, 1.22, -0.7] },
    bubbles: [{ t: 0.45, end: 2.05, text: 'いや、いや、いや…', x: 660, y: 545 }],
    sfx: [[0.02, 'whoosh_swing', -13], [0.06, 'impact_don', -9]],
    act(lt, s) {
      const h = s.hands, c = s.clerk.userData, ext = e(K(lt, 0, 0.45)), back = e(K(lt, 1.5, 2.05));
      h.gripR.visible = true;
      h.R.position.set(lerp(0.155, 0.02, ext) - back * 0.05, lerp(-0.28, -0.13, ext) + back * 0.1, lerp(-0.52, -0.78, ext) + back * 0.22);
      h.R.rotation.set(-0.38, -0.1, -0.05);
      const wave = lt > 0.45 && lt < 1.7 ? Math.sin(lt * 16) * 0.18 : 0;
      c.arm('L', 1.5, 0.55, 0.5 + wave); c.arm('R', 1.5, 0.55, 0.5 - wave);
      c.head.rotation.y = lt > 0.45 && lt < 1.7 ? Math.sin(lt * 9) * 0.09 : 0;
      c.face({ lid: 0.05, brow: -0.7, look: [0, -0.2], mouth: 'o', open: 0.8 });
    } },
  // 2) the rule (first narration line = the counter-intuitive rule itself). Clerk points down at the tray.
  { sc: 'kb', say: ['rule'], show: SHOW,
    cam: { p0: [0, 1.5, 1.57], p1: [0, 1.49, 1.45], l0: [0, 1.2, -0.6] },
    sfx: [[0.02, 'whoosh_switch1', -16], [0.08, 'text_tin', -14]],
    act(lt, s) {
      const h = s.hands, c = s.clerk.userData, down = e(K(lt, 0.2, 0.9));
      h.gripR.visible = true;
      h.R.position.set(lerp(0.1, 0.13, down), lerp(-0.19, -0.26, down), lerp(-0.62, -0.55, down));
      h.R.rotation.set(-0.32, -0.12, -0.08);
      c.reach('R', V(-0.18, 1.08, -0.35)); c.arm('L', 0.15, 0.25, 0.3);
      c.head.rotation.x = 0.14 * Math.sin(K(lt, 0.9, 1.7) * Math.PI); // one nod
      c.face({ lid: 0.12, brow: 0.2, look: [0, -0.3], mouth: 'smile' });
    } },
  // 3) THE RIGHT WAY: banner, hand lowers and puts the cash ON the tray (coin sound on contact).
  { sc: 'kb', say: ['right'], hold: 1.0, show: SHOW,
    cam: { p0: [0, 1.49, 1.45], p1: [0, 1.47, 1.31], l0: [-0.08, 1.06, -0.25] },
    banner: { t: 0.05, end: 1.55, text: 'THE RIGHT WAY', color: '#1faa59' },
    sfx: [[0.05, 'text_pa', -10], [0.1, 'whoosh_swing', -12], [1.32, 'coin_toss', -11]],
    act(lt, s) {
      const h = s.hands, c = s.clerk.userData, put = e(K(lt, 0.55, 1.3)), up = e(K(lt, 1.5, 2.0));
      h.gripR.visible = lt < 1.32; s.cashOnTray.visible = lt >= 1.32;
      h.R.position.set(lerp(0.13, -0.05, put) + up * 0.1, lerp(-0.26, -0.31, put) + up * 0.06, lerp(-0.55, -0.76, put) + up * 0.2);
      h.R.rotation.set(-0.35, -0.05, -0.05);
      c.reach('R', V(-0.18, 1.08, -0.35)); c.arm('L', 0.15, 0.25, 0.3);
      c.head.rotation.x = lt > 1.4 ? 0.12 * Math.sin(K(lt, 1.4, 2.0) * Math.PI) : 0;
      c.face({ lid: 0.15, brow: 0.2, look: [0, -0.35], mouth: 'smile' });
    } },
  // 4) explainer card (black, orange LED). pre: 0.5 = the deliberate beat of silence before the punchline card.
  { sc: 'kb', say: ['card'], pre: 0.5, show: SHOW,
    cam: { p0: [0, 1.47, 1.31], p1: [0, 1.47, 1.29], l0: [-0.08, 1.06, -0.25] },
    card: { big: 'CASH TRAY', sub: 'Your change comes back on the same tray.' },
    sfx: [[0.52, 'text_tin', -13]],
    act(lt, s) { s.cashOnTray.visible = true; s.clerk.userData.face({ mouth: 'smile' }); } },
  // 5) payoff: clerk slides the tray to herself, register beeps, tray returns with change + receipt,
  //    she smiles and bows — bubble + JP voice: ありがとうございます！ POV hand picks up the receipt.
  { sc: 'kb', say: ['takes', 'thanks'], hold: 1.6, show: SHOW,
    cam: { p0: [0, 1.47, 1.31], p1: [0, 1.48, 1.4], l0: [0, 1.26, -0.85] },
    sfx: [[0.35, 'whoosh_slide', -14], [2.55, 'sparkle', -11], [4.55, 'text_tin', -14]],
    act(lt, s, gt, sh) {
      const h = s.hands, c = s.clerk.userData, tray = s.P.tray, th = sh.lt.thanks ?? 3.4;
      const away = e(K(lt, 0.4, 1.4)), back = e(K(lt, 2.6, 3.6));
      tray.position.z = -0.12 - away * 0.38 + back * 0.38;
      s.cashOnTray.visible = lt < 1.45; s.changeOnTray.visible = lt >= 2.6 && lt < 5.15;
      c.reach('R', V(-0.1, 1.05, -0.55)); c.reach('L', V(-0.3, 1.05, -0.55));
      const bow = lt > th + 0.25 ? Math.sin(K(lt, th + 0.25, th + 1.1) * Math.PI) * 0.16 : 0;
      c.body.rotation.x = bow;
      c.face(lt < th ? { lid: 0.15, look: [0, -0.3], mouth: 'flat' } : { lid: 0.3, brow: 0.3, look: [0, 0], mouth: 'smile' });
      const grab = e(K(lt, 4.6, 5.15)), off = e(K(lt, 5.15, 5.9));
      h.receiptR.visible = lt >= 5.15;
      h.R.position.set(lerp(0.155, -0.04, grab) + off * 0.14, -0.28 - grab * 0.04 + off * 0.03, lerp(-0.52, -0.74, grab) + off * 0.24);
      h.R.rotation.set(-0.32, -0.08, -0.06);
    } },
  // 6) keep feeding information after the payoff: the origin detail, camera drifts toward the fridge,
  //    POV is already holding the tea — the result is enjoyed, not just explained.
  { sc: 'kb', say: ['detail'], hold: 0.8, show: ['tray', 'register', 'onigiri'],
    cam: { p0: [0, 1.48, 1.4], p1: [0.42, 1.5, 1.58], l0: [0.1, 1.22, -0.8], l1: [1.4, 1.1, -1.3] },
    sfx: [[0.05, 'text_tin', -14], [0.1, 'whoosh_switch2', -16]],
    act(lt, s) {
      const h = s.hands, c = s.clerk.userData, up = e(K(lt, 0.3, 1.1));
      h.teaL.visible = true; h.receiptR.visible = true;
      h.L.position.set(lerp(-0.155, -0.1, up), lerp(-0.28, -0.17, up), lerp(-0.52, -0.55, up));
      h.L.rotation.set(-0.5, 0.1, 0.05);
      c.arm('L', 0.2, 0.3, 0.4); c.arm('R', 0.2, 0.3, 0.4);
      c.face({ lid: 0.25, look: [0.2, 0], mouth: 'smile' });
    } },
  // 7) the ochi: one quotable twist line, success SFX, slight push-in. Then (next shot) the follow pill.
  { sc: 'kb', say: ['punch'], hold: 1.4, show: SHOW,
    cam: { p0: [0.3, 1.5, 1.55], p1: [0.02, 1.48, 1.18], l0: [0.05, 1.22, -0.7] },
    sfx: [[0.02, 'sparkle', -10], [0.06, 'text_pa', -10]],
    act(lt, s) {
      const h = s.hands, c = s.clerk.userData;
      h.teaL.visible = true; h.receiptR.visible = true;
      h.L.position.set(-0.1, -0.16, -0.55); h.L.rotation.set(-0.5, 0.1, 0.05);
      c.head.rotation.z = 0.07; c.arm('R', 1.9, 0.35, 0.9); c.arm('L', 0.2, 0.3, 0.4); // one hand up, cheerful
      c.face({ lid: 0.35, brow: 0.4, look: [0, 0], mouth: 'smile' });
    } },
  // 8) close: follow pill (drawn by the overlay), clerk waves goodbye.
  { sc: 'kb', say: ['close'], follow: true, show: SHOW,
    cam: { p0: [0.02, 1.48, 1.18], p1: [0, 1.5, 1.44], l0: [0, 1.22, -0.75] },
    sfx: [[0.05, 'end_kira', -12]],
    act(lt, s) {
      const h = s.hands, c = s.clerk.userData;
      h.teaL.visible = true; h.receiptR.visible = true;
      h.L.position.set(-0.1, -0.16, -0.55); h.L.rotation.set(-0.5, 0.1, 0.05);
      const w = Math.sin(lt * 7) * 0.15;
      c.arm('R', 2.7, 0.4 + w, 0.25); c.arm('L', 0.2, 0.3, 0.4);
      c.face({ lid: 0.3, look: [0, 0], mouth: 'smile' });
    } },
];

const T = narrate(voice, plan, { gap: 0.2, tail: 2.0 });
const at = (id) => T.narr.find(n => n.id === id).t0;
const payoff = T.shots[4], DUR = T.shots[T.shots.length - 1].e;
// timed to the actual voice: thanks bubble + JP voice start with the "thanks" line; register beep as the tray is taken
payoff.bubbles = [{ t: payoff.lt.thanks + 0.1, end: payoff.lt.thanks + 2.3, text: 'ありがとうございます！', x: 655, y: 540 }];
T.cues.push([0, TONE, -34, DUR]);                                        // low room tone under the whole video
T.cues.push([T.shots[0].s + 0.45, IYA, -6]);                             // いや、いや、いや…
T.cues.push([payoff.s + 1.5, BEEP, -8]);                                 // register "pi" as the clerk takes the tray
T.cues.push([payoff.s + payoff.lt.thanks + 0.1, ARIGATO, -6]);          // ありがとうございます！

runPov({
  title: 'POV: your first konbini in Japan',
  followText: 'Follow for more first times in Japan',
  shots: T.shots, narr: T.narr, voice: T.voice, cues: T.cues,
  music: { style: 'pop', twist: at('punch'), cta: at('close') },
  scenes: { kb: () => buildKonbini() },
});
