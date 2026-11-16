// ep03 (3D-method prototype): POV — your first izakaya in Japan. Rule: the little dish you never
// ordered is the otoshi — the table charge, served as a snack. Punchline: "Rent for your chair.
// Served as a snack."
// Same beat sheet, narration script (s1-s9 + n1-n4) and JP shout as the 2D ep03 — rendered with the
// real-3D engine (kitizakaya.js) for the side-by-side method comparison. Everything moves from
// second 0: steam, noren, lantern flicker, background guests, the cook. The freeze gag freezes the
// CHARACTERS (server's pose held by act, guests/cook held by the stopped ambient clock) while the
// environment keeps moving.
import { runPov } from '../engine/pov.js';
import { buildIzakaya, buildIzakayaExterior, V, lerp, clamp } from '../engine/kitizakaya.js';
import { narrate } from './_common.js';

const voice = await (await fetch(new URL('./ep03_izakaya_otoshi.voice.json', import.meta.url))).json();
const K = (t, a, b) => clamp((t - a) / (b - a));
const e = (x) => { x = clamp(x); return x * x * (3 - 2 * x); };
const TONE = 'ep01_konbini_tray_sfx/roomtone.mp3';
const SHOUT = 'ep03_izakaya_otoshi_jp_voice/shout.mp3';
const DISH_FAR = -0.78, DISH_SENT_BACK = -0.68, DISH_MINE = -0.38; // dish z positions on the counter

const plan = [
  // 1) cold open (0-~3s): the otoshi lands uninvited — the server slides it in front of you; the POV
  //    hand pushes it straight back. FREEZE: server + whole room stop mid-motion; steam, noren and
  //    lanterns keep moving. No narration (the silence is the setup).
  { sc: 'iz', say: [], pre: 0, hold: 3.1, show: ['otoshi'],
    cam: { p0: [0, 1.27, 1.22], p1: [0, 1.25, 1.06], l0: [0.05, 1.02, -0.8] },
    sfx: [[0.28, 'whoosh_slide', -16], [1.02, 'whoosh_swing', -14], [1.5, 'shock', -8]],
    act(lt, s) {
      const h = s.hands, sv = s.server.userData, d = s.P.otoshi;
      s.frozenNow = lt >= 1.5; s.cookCheer = 0;
      const slide = e(K(lt, 0.25, 0.8)), push = e(K(lt, 1.0, 1.45));
      d.position.z = lerp(DISH_FAR, -0.4, slide) - push * 0.28;
      if (lt < 1.0) { sv.reach('R', V(0.12, 1.0, -0.62)); sv.arm('L', 0.2, 0.3, 0.4); sv.face({ lid: 0.15, look: [0, -0.25], mouth: 'smile' }); }
      else { sv.arm('R', 1.25, 0.5, 0.45); sv.arm('L', 0.9, 0.45, 0.5); sv.face({ lid: 0.02, brow: -0.7, look: [0, 0.05], mouth: 'o', open: 0.9 }); }
      const ext = e(K(lt, 0.95, 1.4));
      h.R.position.set(lerp(0.17, 0.1, ext), lerp(-0.3, -0.17, ext), lerp(-0.5, -0.64, ext));
      h.R.rotation.set(-0.35, -0.1, -0.05);
    } },
  // 2) verdict: s1 + s2 over the held freeze, WRONG WAY banner; then the room unfreezes — the server
  //    shakes her head and points down at the dish: it stays.
  { sc: 'iz', say: ['s1', 's2'], pre: 0.1, hold: 0.5, show: ['otoshi'],
    cam: { p0: [0, 1.25, 1.06], p1: [0.02, 1.24, 0.9], l0: [0.1, 1.06, -1.0] },
    banner: { t: 0.05, end: 1.75, text: 'WRONG WAY', color: '#d23b2e' },
    sfx: [[0.05, 'impact_don', -6], [0.12, 'text_pa', -12]],
    act(lt, s) {
      const h = s.hands, sv = s.server.userData, d = s.P.otoshi;
      s.frozenNow = lt < 1.15; s.cookCheer = 0;
      d.position.z = DISH_SENT_BACK;
      if (lt < 1.15) { sv.arm('R', 1.25, 0.5, 0.45); sv.arm('L', 0.9, 0.45, 0.5); sv.face({ lid: 0.02, brow: -0.7, look: [0, 0.05], mouth: 'o', open: 0.9 }); }
      else {
        const shake = Math.sin(K(lt, 1.15, 2.3) * Math.PI * 2.2) * 0.1 * (1 - K(lt, 1.9, 2.4));
        sv.head.rotation.y = shake;
        sv.reach('R', V(0.12, 1.02, -0.6)); sv.arm('L', 0.2, 0.3, 0.4);
        sv.face({ lid: 0.1, brow: -0.45, look: [0, -0.3], mouth: 'flat' });
      }
      const back = e(K(lt, 1.15, 1.75));
      h.R.position.set(lerp(0.1, 0.17, back), lerp(-0.17, -0.3, back), lerp(-0.64, -0.5, back));
      h.R.rotation.set(-0.32, -0.12, -0.08);
    } },
  // 3) chapter: the shop from outside at night — noren swaying, lantern flickering, steam from the
  //    vent, a passer-by crossing. s3: "That dish? Otoshi."
  { sc: 'ex', say: ['s3'], pre: 0.35, hold: 0.6,
    cam: { p0: [-0.55, 1.52, 2.35], p1: [0.15, 1.46, 1.65], l0: [0.1, 1.35, -2.4] },
    sfx: [[0.05, 'whoosh_switch2', -16], [0.42, 'text_tin', -14]],
    act(lt, s) { s.frozenNow = false; } },
  // 4) accept: THE RIGHT WAY banner; the POV hand pulls the dish back and keeps it. s4.
  { sc: 'iz', say: ['s4'], pre: 0.1, hold: 0.8, show: ['otoshi'],
    cam: { p0: [0.02, 1.24, 0.9], p1: [0, 1.25, 1.02], l0: [0.05, 1.02, -0.8] },
    banner: { t: 0.05, end: 1.5, text: 'THE RIGHT WAY', color: '#1faa59' },
    sfx: [[0.05, 'text_pa', -10], [0.38, 'whoosh_slide', -15]],
    act(lt, s) {
      const h = s.hands, sv = s.server.userData, d = s.P.otoshi;
      s.frozenNow = false; s.cookCheer = 0;
      const pull = e(K(lt, 0.35, 0.95));
      d.position.z = lerp(DISH_SENT_BACK, DISH_MINE, pull);
      const reach = e(K(lt, 0.15, 0.4)), off = e(K(lt, 1.05, 1.5));
      h.R.position.set(lerp(0.17, 0.1, reach) + off * 0.07, lerp(-0.3, -0.2, reach) + off * 0.08, lerp(-0.5, -0.6, reach) + off * 0.12);
      h.R.rotation.set(-0.35, -0.08, -0.05);
      sv.body.rotation.x = Math.sin(K(lt, 0.55, 1.35) * Math.PI) * 0.13; // a small bow
      sv.arm('R', 0.25, 0.3, 0.45); sv.arm('L', 0.25, 0.3, 0.45);
      sv.face({ lid: 0.28, brow: 0.25, look: [0, -0.2], mouth: 'smile' });
    } },
  // 5) order: POV points up at the menu board; the server grins and turns to the kitchen. s5 + s6.
  { sc: 'iz', say: ['s5', 's6'], pre: 0.1, hold: 0.3, show: ['otoshi'],
    cam: { p0: [0, 1.25, 1.02], p1: [-0.06, 1.27, 1.0], l0: [-0.15, 1.12, -1.1] },
    sfx: [[0.1, 'text_tin', -14], [0.14, 'whoosh_swing', -15]],
    act(lt, s, gt, sh) {
      const h = s.hands, sv = s.server.userData, d = s.P.otoshi;
      s.frozenNow = false; s.cookCheer = 0;
      d.position.z = DISH_MINE;
      const up = e(K(lt, 0.2, 0.6)), down = e(K(lt, (sh.lt.s6 ?? 2.2) + 0.3, (sh.lt.s6 ?? 2.2) + 0.9));
      h.L.position.set(lerp(-0.17, -0.24, up) + down * 0.05, lerp(-0.3, 0.0, up) - down * 0.22, lerp(-0.5, -0.52, up) + down * 0.04);
      h.L.rotation.set(-0.85, 0.2, 0.1);
      const turn = e(K(lt, (sh.lt.s6 ?? 2.2) + 0.15, (sh.lt.s6 ?? 2.2) + 0.85));
      s.server.rotation.y = -0.85 * turn;
      sv.head.rotation.x = -0.14 * (1 - turn);
      sv.arm('R', 0.3, 0.3, 0.4); sv.arm('L', 0.3, 0.3, 0.4);
      sv.face({ lid: 0.32, brow: 0.3, look: [-0.25, 0.25], mouth: 'smile' });
    } },
  // 6) the shout: silence, then the server cups a hand and calls the order to the kitchen —
  //    「はい、生ビール一丁！」 — and the cook throws both arms up in answer.
  { sc: 'iz', say: [], pre: 0.3, hold: 2.3, show: ['otoshi'],
    cam: { p0: [0.05, 1.26, 1.05], p1: [0.28, 1.28, 0.92], l0: [0.55, 1.12, -1.5] },
    bubbles: [{ t: 0.35, end: 2.25, text: 'はい、生ビール一丁！', x: 615, y: 520 }],
    sfx: [[0.3, 'whoosh_swing', -14]],
    act(lt, s) {
      const sv = s.server.userData, d = s.P.otoshi;
      s.frozenNow = false;
      s.cookCheer = (lt > 0.5 && lt < 2.05) ? Math.sin(K(lt, 0.5, 2.05) * Math.PI) : 0;
      d.position.z = DISH_MINE;
      s.server.rotation.y = -0.85;
      sv.arm('R', 2.25, 0.55, 2.1); sv.arm('L', 0.3, 0.3, 0.4); // hand cupped to the mouth
      sv.head.rotation.x = -0.13;
      sv.face(lt < 0.35 ? { lid: 0.3, brow: 0.3, mouth: 'smile' } : { lid: 0.12, brow: 0.2, look: [0.4, 0.1], mouth: 'o', open: 1 });
    } },
  // 7) the wait: camera drifts toward the grill — the cook works the skewers, steam pours, the
  //    guests eat and chat. The POV hand taps the counter, then settles. s7.
  { sc: 'iz', say: ['s7'], pre: 0.1, hold: 2.4, show: ['otoshi'],
    cam: { p0: [0.28, 1.28, 0.92], p1: [0.55, 1.3, 1.02], l0: [1.25, 1.05, -2.1] },
    sfx: [[0.05, 'text_tin', -14]],
    act(lt, s) {
      const h = s.hands, d = s.P.otoshi;
      s.frozenNow = false; s.cookCheer = 0;
      d.position.z = DISH_MINE;
      if (lt < 1.3) h.R.position.y = -0.3 + Math.abs(Math.sin(lt * 9)) * 0.012; // impatient tap
    } },
  // 8) payoff: the beer arrives, slid across the counter; chopsticks dip into the otoshi. s8.
  { sc: 'iz', say: ['s8'], pre: 0.1, hold: 1.7, show: ['otoshi', 'beer'],
    cam: { p0: [0.4, 1.29, 1.0], p1: [0.12, 1.24, 0.9], l0: [0.15, 1.0, -0.6] },
    sfx: [[0.25, 'whoosh_slide', -15], [1.05, 'sparkle', -10], [1.12, 'text_pa', -11]],
    act(lt, s) {
      const h = s.hands, sv = s.server.userData, d = s.P.otoshi, b = s.P.beer;
      s.frozenNow = false; s.cookCheer = 0;
      d.position.z = DISH_MINE;
      const slide = e(K(lt, 0.2, 0.9));
      b.position.set(lerp(0.62, 0.38, slide), 0.94, lerp(-0.82, -0.35, slide));
      if (lt < 1.0) { sv.reach('R', V(0.5, 1.0, -0.6)); sv.reach('L', V(0.3, 1.0, -0.62)); }
      else { sv.arm('R', 0.25, 0.3, 0.45); sv.arm('L', 0.25, 0.3, 0.45); sv.body.rotation.x = Math.sin(K(lt, 1.15, 1.8) * Math.PI) * 0.12; }
      sv.face({ lid: 0.3, brow: 0.3, look: [0, -0.2], mouth: 'smile' });
      h.sticksR.visible = lt >= 0.9;
      const dip = Math.sin(K(lt, 1.0, 1.65) * Math.PI);
      h.R.position.set(0.1, -0.19 - dip * 0.035, -0.58); h.R.rotation.set(-0.42, -0.08, -0.05);
      d.rotation.x = dip * 0.12;
    } },
  // 9) the punchline, push-in on dish + beer; the server gives a thumbs-up behind the counter. s9.
  { sc: 'iz', say: ['s9'], pre: 0.1, hold: 1.3, show: ['otoshi', 'beer'],
    cam: { p0: [0.12, 1.24, 0.9], p1: [0.05, 1.2, 0.6], l0: [0.1, 0.98, -0.5] },
    sfx: [[0.02, 'sparkle', -10], [0.3, 'end_tirin', -11]],
    act(lt, s) {
      const h = s.hands, sv = s.server.userData, d = s.P.otoshi, b = s.P.beer;
      s.frozenNow = false; s.cookCheer = 0;
      d.position.z = DISH_MINE; b.position.set(0.38, 0.94, -0.35);
      h.sticksR.visible = true;
      h.R.position.set(0.1, -0.19, -0.58); h.R.rotation.set(-0.42, -0.08, -0.05);
      sv.arm('R', 2.75, 0.35, 0.2); sv.hand('R', 'gu'); sv.arm('L', 0.25, 0.3, 0.45); // thumbs-up
      sv.face({ lid: 0.35, brow: 0.4, look: [0, 0], mouth: 'smile' });
    } },
  // 10-12) explainer cards (programmatic, as in the standard format): n1 / n2 / n3.
  { sc: 'iz', say: ['n1'], pre: 0.5, show: ['otoshi'],
    card: { big: 'THE OTOSHI', sub: 'It lands before you order anything.' },
    sfx: [[0.52, 'text_tin', -13]],
    act(lt, s) { s.frozenNow = false; s.cookCheer = 0; s.server.userData.face({ mouth: 'smile' }); } },
  { sc: 'iz', say: ['n2'], pre: 0.1, show: ['otoshi'],
    card: { big: 'THE CHARGE', sub: "It's the table charge — about ¥400 a head." },
    sfx: [[0.12, 'text_tin', -13]],
    act(lt, s) { s.frozenNow = false; s.cookCheer = 0; s.server.userData.face({ mouth: 'smile' }); } },
  { sc: 'iz', say: ['n3'], pre: 0.1, show: ['otoshi'],
    card: { big: 'JUST ASK', sub: "Don't want it? Ask before it lands." },
    sfx: [[0.12, 'text_tin', -13]],
    act(lt, s) { s.frozenNow = false; s.cookCheer = 0; s.server.userData.face({ mouth: 'smile' }); } },
  // 13) close: follow pill, the server waves goodbye over the counter. n4.
  { sc: 'iz', say: ['n4'], pre: 0.1, follow: true, show: ['otoshi', 'beer'],
    cam: { p0: [0.05, 1.21, 0.72], p1: [0, 1.26, 1.18], l0: [0.05, 1.05, -1.0] },
    sfx: [[0.05, 'end_kira', -12]],
    act(lt, s) {
      const sv = s.server.userData, d = s.P.otoshi, b = s.P.beer;
      s.frozenNow = false; s.cookCheer = 0;
      d.position.z = DISH_MINE; b.position.set(0.38, 0.94, -0.35);
      const w = Math.sin(lt * 7) * 0.15;
      sv.arm('R', 2.7, 0.4 + w, 0.25); sv.arm('L', 0.2, 0.3, 0.4);
      sv.face({ lid: 0.3, look: [0, 0], mouth: 'smile' });
    } },
];

const T = narrate(voice, plan, { gap: 0.2, tail: 2.0 });
const at = (id) => T.narr.find(n => n.id === id).t0;
const DUR = T.shots[T.shots.length - 1].e;
T.cues.push([0, TONE, -34, DUR]);                          // low room tone under the whole video
T.cues.push([T.shots[5].s + 0.35, SHOUT, -5]);             // はい、生ビール一丁！

runPov({
  title: 'POV: your first izakaya in Japan',
  followText: 'Follow for more first times in Japan',
  shots: T.shots, narr: T.narr, voice: T.voice, cues: T.cues,
  music: { style: 'pop', twist: at('s9'), cta: at('n4') },
  scenes: { iz: () => buildIzakaya(), ex: () => buildIzakayaExterior() },
});
