// pov.js — "Japan POV" format layer on top of core.js (moshimo engine is untouched).
// First-person reels for English speakers learning how Japan works (see ../FORMAT.md):
//   - protagonist = two 3D hands + mustard sleeves at the bottom of the frame (rig lives in kitpov.js)
//   - black rounded title label at the top from second 0: "POV: your first ___ in Japan"
//   - cold open: the WRONG way + a Japanese speech bubble from the staff character
//   - "THE RIGHT WAY" coloured banner, then the scene redone correctly
//   - explainer card: black card, big orange LED-style object name + one-line logic
//   - payoff: staff smile + Japanese thanks bubble, then a calm English close + "Follow for more" pill
// EP contract (built with narrate() from _common.js, same as the pop style):
//   runPov({ title, shots, narr, voice, cues, music, scenes, followText })
//   shot extras: bubbles: [{t, end, text, x, y}]  (t/end = seconds inside the shot, x/y = px centre of the bubble)
//                banner:  {t, end, text, color}  (full-width band across the middle)
//                card:    {big, sub}             (explainer card covers the whole shot)
//                follow:  true                   (show the follow pill in this shot, from 0.8s in)
import { THREE, W, H, clamp, ease, lerp, renderer, applyCam, GOTH } from './core.js';

const out = document.getElementById('out');
const ctx = out.getContext('2d');
const ORANGE = '#ff9d2e', INK = '#14161c';
const outBack = (t) => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const EN = (s) => `700 ${s}px "Arial","Helvetica Neue","Noto Sans CJK JP",sans-serif`;
const ENB = (s) => `900 ${s}px "Arial Black","Arial","Noto Sans CJK JP",sans-serif`;

function fitFont(str, maxW, size, fn) {
  ctx.font = fn(size);
  while (ctx.measureText(str).width > maxW && size > 16) { size -= 2; ctx.font = fn(size); }
  return fn(size);
}
function rrect(x, y, w, h, r) {
  ctx.beginPath(); ctx.roundRect(x, y, w, h, r);
}
// top-of-frame label, present from second 0 for the whole video
function titleLabel(text) {
  const f = fitFont(text, 880, 47, ENB);
  ctx.font = f;
  const w = ctx.measureText(text).width + 64, h = 84, x = (W - w) / 2, y = 268;
  ctx.save();
  ctx.shadowColor = 'rgba(0,0,0,0.45)'; ctx.shadowBlur = 14; ctx.shadowOffsetY = 4;
  ctx.fillStyle = 'rgba(12,12,14,0.94)'; rrect(x, y, w, h, 42); ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.fillStyle = '#ffffff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(text, W / 2, y + h / 2 + 3);
  ctx.restore();
}
// white speech bubble with a tail pointing down-left (toward the staff member)
function bubble(b, lt) {
  const t = lt - b.t, dur = (b.end ?? b.t + 2.2) - b.t;
  if (t < 0 || t > dur) return;
  const sc = t < 0.25 ? 0.4 + 0.6 * outBack(clamp(t / 0.25)) : 1;
  const a = clamp((dur - t) / 0.2);
  const f = GOTH(52);
  ctx.font = f;
  const w = ctx.measureText(b.text).width + 56, h = 96;
  ctx.save(); ctx.globalAlpha = a; ctx.translate(b.x, b.y); ctx.scale(sc, sc);
  ctx.shadowColor = 'rgba(0,0,0,0.35)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
  ctx.fillStyle = '#ffffff'; rrect(-w / 2, -h / 2, w, h, 30); ctx.fill();
  ctx.beginPath(); ctx.moveTo(-w / 2 + 34, h / 2 - 6); ctx.lineTo(-w / 2 + 78, h / 2 - 6); ctx.lineTo(-w / 2 + 44, h / 2 + 34); ctx.closePath(); ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.fillStyle = INK; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(b.text, 0, 4);
  ctx.restore();
}
// coloured band across the middle: "THE RIGHT WAY"
function banner(bn, lt) {
  const t = lt - bn.t, dur = (bn.end ?? bn.t + 1.8) - bn.t;
  if (t < 0 || t > dur) return;
  const a = clamp(t / 0.18) * clamp((dur - t) / 0.2);
  const slide = (1 - ease(clamp(t / 0.3))) * -W;
  ctx.save(); ctx.globalAlpha = a;
  ctx.fillStyle = bn.color || '#1faa59'; ctx.fillRect(slide, 838, W, 168);
  ctx.fillStyle = '#ffffff'; ctx.font = ENB(92); ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(bn.text, W / 2 + slide, 838 + 88);
  ctx.restore();
}
// explainer card: black frame, big orange LED-style object name, one line of logic under it
function explainer(card, lt, dur) {
  const a = clamp(lt / 0.3) * clamp((dur - lt) / 0.3);
  ctx.save(); ctx.globalAlpha = a;
  ctx.fillStyle = '#050505'; ctx.fillRect(0, 0, W, H);
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.shadowColor = ORANGE; ctx.shadowBlur = 42;
  ctx.fillStyle = ORANGE; ctx.font = fitFont(card.big, 940, 150, ENB);
  ctx.fillText(card.big, W / 2, 830);
  ctx.fillText(card.big, W / 2, 830); // second pass = stronger LED glow
  ctx.shadowBlur = 0;
  ctx.fillStyle = '#f5f5f5'; ctx.font = fitFont(card.sub, 880, 44, EN);
  // wrap the logic line to at most 2 lines
  const words = card.sub.split(' '), lines = [''];
  for (const wd of words) {
    const cand = lines[lines.length - 1] ? lines[lines.length - 1] + ' ' + wd : wd;
    if (ctx.measureText(cand).width > 880 && lines[lines.length - 1]) lines.push(wd); else lines[lines.length - 1] = cand;
  }
  lines.slice(0, 2).forEach((ln, i) => ctx.fillText(ln, W / 2, 960 + i * 58));
  ctx.restore();
}
// narration caption = the main telop. FORMAT rules: one idea per telop, <= ~7 English words on screen,
// >= 64px at 1080 wide (we use 88), lower-third ABOVE the hands (baseline y=1300), never over the key
// prop or the staff face, white bold + ink outline, same slot in every episode.
const TELOP_Y = 1300, TELOP_SIZE = 88;
function caption(EP, gt) {
  const n = (EP.narr || []).find(k => gt >= k.t0 - 0.03 && gt < k.t1 + 0.18);
  if (!n) return;
  let c = n.chunks[0]; for (const k of n.chunks) if (gt >= k.t - 0.03) c = k;
  const parts = c.text.split(/(\[[^\]]*\])/).filter(Boolean).map(p => p[0] === '[' ? [p.slice(1, -1), ORANGE] : [p, '#ffffff']);
  let size = TELOP_SIZE;
  ctx.font = ENB(size);
  let tw = parts.reduce((s, p) => s + ctx.measureText(p[0]).width, 0);
  if (tw > 900) { size = Math.floor(size * 900 / tw); ctx.font = ENB(size); tw = parts.reduce((s, p) => s + ctx.measureText(p[0]).width, 0); }
  const t = gt - c.t, sc = t < 0.14 ? 0.85 + 0.15 * outBack(clamp(t / 0.14)) : 1;
  ctx.save(); ctx.translate(500, TELOP_Y); ctx.scale(sc, sc); ctx.textAlign = 'left'; ctx.textBaseline = 'alphabetic'; ctx.lineJoin = 'round';
  ctx.lineWidth = size * 0.22; ctx.strokeStyle = INK;
  let x = -tw / 2; for (const p of parts) { ctx.strokeText(p[0], x, 0); x += ctx.measureText(p[0]).width; }
  x = -tw / 2; for (const p of parts) { ctx.fillStyle = p[1]; ctx.fillText(p[0], x, 0); x += ctx.measureText(p[0]).width; }
  ctx.restore();
}
function followPill(text, lt) {
  const t = lt - 0.8; if (t < 0) return;
  const sc = t < 0.3 ? 0.5 + 0.5 * outBack(clamp(t / 0.3)) : 1;
  ctx.font = EN(46);
  const w = ctx.measureText(text).width + 84, h = 92;
  ctx.save(); ctx.translate(W / 2, 1478); ctx.scale(sc, sc);
  ctx.shadowColor = 'rgba(0,0,0,0.4)'; ctx.shadowBlur = 12; ctx.shadowOffsetY = 4;
  ctx.fillStyle = ORANGE; rrect(-w / 2, -h / 2, w, h, h / 2); ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.fillStyle = '#16181d'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, 3);
  ctx.restore();
}

export function runPov(EP) {
  const DURATION = EP.shots[EP.shots.length - 1].e;
  let SC = null;
  function overlay(shot, lt, gt) {
    if (shot.card) { explainer(shot.card, lt, shot.e - shot.s); return; } // the card replaces the scene view
    const g = ctx.createLinearGradient(0, 0, 0, 460);
    g.addColorStop(0, 'rgba(0,0,0,0.30)'); g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.fillRect(0, 0, W, 460);
    caption(EP, gt);
    for (const b of shot.bubbles || []) bubble(b, lt);
    if (shot.banner) banner(shot.banner, lt);
    if (shot.follow) followPill(EP.followText || 'Follow for more', lt);
    titleLabel(EP.title);
  }
  function renderAt(gt, clean = false) {
    gt = Math.min(gt, DURATION - 1e-3);
    const shot = EP.shots.find(s => gt >= s.s && gt < s.e);
    const lt = gt - shot.s;
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    const S = SC[shot.sc];
    if (shot.fn) S[shot.fn](lt, gt, shot); else S.update(lt, gt, shot);
    if (shot.cam) applyCam(S.camera, shot.cam, lt, shot.e - shot.s);
    renderer.render(S.scene, S.camera);
    ctx.imageSmoothingEnabled = true; ctx.imageSmoothingQuality = 'high';
    ctx.drawImage(renderer.domElement, 0, 0, W, H);
    if (!clean) overlay(shot, lt, gt);
    let fade = Math.max(1 - clamp(lt / 0.22), 1 - clamp((DURATION - gt) / 0.35));
    if (shot.s === 0) fade = Math.max(1 - clamp(gt / 0.3), 1 - clamp((DURATION - gt) / 0.35));
    if (fade > 0) { ctx.fillStyle = `rgba(0,0,0,${fade})`; ctx.fillRect(0, 0, W, H); }
  }
  (async () => {
    await Promise.all([
      document.fonts.load(GOTH(52), 'いや、ありがとうございます！トレイ'),
      document.fonts.load(ENB(60), 'POV: your first konbini in Japan'),
      document.fonts.load(EN(46), 'Follow for more'),
    ]);
    SC = {};
    for (const [k, fn] of Object.entries(EP.scenes)) SC[k] = fn();
    for (const s of EP.shots) renderAt(s.s + 0.5);
    const gl = renderer.getContext(); const ext = gl.getExtension('WEBGL_debug_renderer_info');
    window.GPU = ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : 'unknown';
    window.META = { duration: DURATION, cues: EP.cues || [], T_B: 0, music: EP.music || {}, voice: EP.voice || [] };
    window.frameAt = (t, q = 0.95, clean = false) => { renderAt(t, clean); return out.toDataURL('image/jpeg', q); };
    window.READY = true;
    const qs = new URLSearchParams(location.search);
    if (qs.has('t')) renderAt(parseFloat(qs.get('t')));
  })().catch(e => { window.ERR = String(e && e.stack || e); console.error(e); });
}
