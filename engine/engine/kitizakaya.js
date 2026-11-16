// kitizakaya: first-person izakaya scenes for the 3D-method prototype of ep03 (otoshi).
// Same contract as kitpov.js: buildIzakaya() / buildIzakayaExterior() -> { scene, camera, api, update(lt, gt, shot) }
//   shot: { show: ['otoshi', 'beer'], act(lt, api, gt, shot) }
//   api:  { server (toyGuy, indigo + apron + hachimaki), cook, guests, P (props), hands {L, R, sticksR},
//           frozenNow (set by act: while true the ambient clock stops — guests/cook hold their pose —
//           but steam, noren and lantern flicker keep moving on the real clock) }
// Everything is animated in-engine: steam sprites rise continuously, noren panels sway, lantern
// emissive + point lights flicker, background guests eat/drink/chat on the ambient clock, the cook
// works the grill. The freeze gag = characters frozen (ambient clock stopped + act holds the server)
// while the environment keeps moving.
import { THREE, V, lerp, clamp, canvasTex, cam, basic, applyCam } from './core.js';
import { toyGuy, sph, caps, rbox, cyl, M } from './kit6.js';

const MUSTARD = '#d9a441', SKIN = '#ffd3ad';
const shd = (m) => { m.castShadow = m.receiveShadow = true; return m; };
const box = (parent, w, h, d, m, x, y, z) => { const o = shd(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), typeof m === 'string' ? M(m) : m)); o.position.set(x, y, z); parent.add(o); return o; };

// ---- POV hand rig (same protagonist as kitpov: mustard sleeves) ----
function makeHand(side) {
  const g = new THREE.Group();
  const sl = cyl(0.045, 0.056, 0.115, MUSTARD, 0, -0.045, 0.035, g); sl.rotation.x = 2.75;
  sph(0.056, MUSTARD, 0, -0.098, 0.057, g, 1, 0.75, 1);
  const cuff = cyl(0.055, 0.06, 0.045, '#f5f2ea', 0, -0.022, 0.005, g); cuff.rotation.x = 2.75;
  sph(0.088, SKIN, 0, 0, -0.03, g, 1.05, 0.55, 1.25);
  for (let i = 0; i < 4; i++) {
    const f = caps(0.021, 0.05, SKIN, (i - 1.5) * 0.042, -0.028, -0.125, g);
    f.rotation.x = Math.PI / 2.6;
  }
  const th = caps(0.024, 0.045, SKIN, side * -0.085, -0.01, -0.07, g); th.rotation.z = side * 0.7; th.rotation.x = 0.5;
  return g;
}

// ---- steam: soft sprites rising in a loop; runs on the REAL clock (never freezes) ----
const steamTex = () => canvasTex(128, 128, (g) => {
  const gr = g.createRadialGradient(64, 64, 4, 64, 64, 62);
  gr.addColorStop(0, 'rgba(255,255,255,0.85)'); gr.addColorStop(0.55, 'rgba(255,255,255,0.32)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = gr; g.fillRect(0, 0, 128, 128);
});
let STEAM_TEX = null;
function makeSteam(parent, x, y, z, { n = 5, rise = 0.5, spread = 0.05, size = 0.16, speed = 0.16 } = {}) {
  if (!STEAM_TEX) STEAM_TEX = steamTex();
  const grp = new THREE.Group(); grp.position.set(x, y, z); parent.add(grp);
  const sprites = [];
  for (let i = 0; i < n; i++) {
    const m = new THREE.SpriteMaterial({ map: STEAM_TEX, transparent: true, opacity: 0, depthWrite: false });
    const s = new THREE.Sprite(m); s.userData = { ph: i / n, sp: speed * (0.8 + (i % 3) * 0.2), rise, spread, size, seed: i * 1.7 };
    grp.add(s); sprites.push(s);
  }
  return { grp, sprites };
}
function tickSteam(sys, gt) {
  for (const s of sys.sprites) {
    const u = s.userData, f = (gt * u.sp + u.ph) % 1;
    s.position.set(Math.sin(gt * 0.9 + u.seed) * u.spread * f, f * u.rise, Math.cos(gt * 0.7 + u.seed) * u.spread * f * 0.6);
    const sc = u.size * (0.6 + f * 1.1); s.scale.set(sc, sc, 1);
    s.material.opacity = Math.sin(f * Math.PI) * 0.34;
  }
}

// ---- red paper lantern (chochin) with flickering emissive body ----
function makeLantern(parent, x, y, z, r = 0.17) {
  const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g);
  const mat = new THREE.MeshStandardMaterial({ color: '#d8362f', roughness: 0.6, emissive: '#ff7a30', emissiveIntensity: 1.2 });
  const body = shd(new THREE.Mesh(new THREE.SphereGeometry(r, 24, 18), mat)); body.scale.set(1, 0.84, 1); g.add(body);
  cyl(r * 0.42, r * 0.42, 0.035, '#1c1c20', 0, r * 0.86, 0, g);
  cyl(r * 0.42, r * 0.42, 0.035, '#1c1c20', 0, -r * 0.86, 0, g);
  for (const yy of [-0.35, 0, 0.35]) { const t = new THREE.Mesh(new THREE.TorusGeometry(r * 0.99, 0.006, 6, 32), M('#a8231e')); t.rotation.x = Math.PI / 2; t.position.y = yy * r; t.scale.set(1, 1, 0.84); g.add(t); }
  cyl(0.008, 0.008, 0.5, '#1c1c20', 0, r + 0.28, 0, g); // hanging cord
  return { grp: g, mat };
}

// ---- noren curtain: panels hinged at the rod, swaying on the real clock ----
function makeNoren(parent, x, y, z, { w = 0.46, h = 0.78, n = 3, rotY = 0 } = {}) {
  const g = new THREE.Group(); g.position.set(x, y, z); g.rotation.y = rotY; parent.add(g);
  cyl(0.02, 0.02, w * n + 0.3, '#4a3220', 0, 0.02, 0, g).rotation.z = Math.PI / 2;
  const tex = canvasTex(256, 340, (c) => {
    c.fillStyle = '#2e3d66'; c.fillRect(0, 0, 256, 340);
    c.fillStyle = '#f5f2ea'; c.beginPath(); c.arc(128, 128, 62, 0, Math.PI * 2); c.fill();
    c.fillStyle = '#2e3d66'; c.beginPath(); c.arc(128, 128, 44, 0, Math.PI * 2); c.fill();
    c.fillStyle = '#f5f2ea'; c.fillRect(112, 236, 32, 62);
  });
  const panels = [];
  for (let i = 0; i < n; i++) {
    const geo = new THREE.PlaneGeometry(w - 0.03, h); geo.translate(0, -h / 2, 0);
    const p = new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ map: tex, side: THREE.DoubleSide, roughness: 0.9 }));
    p.position.set((i - (n - 1) / 2) * w, 0, 0); p.castShadow = true; g.add(p); panels.push(p);
  }
  return { grp: g, panels };
}
function tickNoren(nr, gt, amp = 1) {
  nr.panels.forEach((p, i) => { p.rotation.x = (Math.sin(gt * 1.35 + i * 0.8) * 0.075 + Math.sin(gt * 2.2 + i * 1.7) * 0.028) * amp; });
}

export function buildIzakaya() {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#241610');
  scene.fog = new THREE.Fog(0x241610, 12, 26);
  const hemi = new THREE.HemisphereLight(0xffe2b8, 0x4a3220, 1.15); scene.add(hemi);
  const key = new THREE.DirectionalLight(0xffd9a8, 2.0); key.position.set(2.5, 5.5, 4.5); key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024); Object.assign(key.shadow.camera, { left: -6, right: 6, top: 6, bottom: -6, near: 0.5, far: 25 });
  key.shadow.bias = -0.0004; scene.add(key);
  const fill = new THREE.DirectionalLight(0xffc9a0, 0.4); fill.position.set(-4, 3, 2); scene.add(fill);
  const G = () => new THREE.Group();

  // ---- room ----
  const floorTex = canvasTex(512, 512, (g) => {
    g.fillStyle = '#5d4128'; g.fillRect(0, 0, 512, 512);
    for (let i = 0; i < 8; i++) { g.fillStyle = i % 2 ? '#63462c' : '#573d26'; g.fillRect(0, i * 64, 512, 62); }
    g.fillStyle = 'rgba(0,0,0,0.25)'; for (let i = 0; i < 40; i++) g.fillRect(Math.random() * 512, Math.random() * 512, 30 + Math.random() * 60, 2);
  });
  floorTex.wrapS = floorTex.wrapT = THREE.RepeatWrapping; floorTex.repeat.set(3, 3);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(16, 16), new THREE.MeshStandardMaterial({ map: floorTex, roughness: 0.9 }));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const wallM = M('#6e4b2c', 0.92);
  const back = new THREE.Mesh(new THREE.PlaneGeometry(13, 4.4), wallM); back.position.set(0, 2.2, -3.2); back.receiveShadow = true; scene.add(back);
  const left = new THREE.Mesh(new THREE.PlaneGeometry(10, 4.4), M('#63452a', 0.92)); left.rotation.y = Math.PI / 2; left.position.set(-3.6, 2.2, 0); left.receiveShadow = true; scene.add(left);
  for (const bx of [-2.4, 0, 2.4]) box(scene, 0.18, 0.24, 7, '#3d2817', bx, 3.05, -0.6); // ceiling beams
  // menu strips on the back wall
  const menuTex = canvasTex(1024, 220, (g) => {
    g.fillStyle = '#54381f'; g.fillRect(0, 0, 1024, 220);
    const cols = ['#f5efdd', '#f5efdd', '#e8b4a0', '#f5efdd', '#f5efdd', '#f2d492', '#f5efdd'];
    for (let i = 0; i < 7; i++) {
      g.fillStyle = cols[i]; g.fillRect(28 + i * 140, 18, 104, 184);
      g.fillStyle = '#2b2b30'; for (let j = 0; j < 4; j++) g.fillRect(66 + i * 140, 38 + j * 34, 28, 20);
      g.fillStyle = '#b03024'; g.fillRect(66 + i * 140, 176, 28, 12);
    }
  });
  const menu = new THREE.Mesh(new THREE.PlaneGeometry(3.4, 0.73), new THREE.MeshStandardMaterial({ map: menuTex, roughness: 0.85 }));
  menu.position.set(-0.7, 2.35, -3.17); scene.add(menu);
  // sake bottles on a back shelf (right of the menu)
  box(scene, 1.5, 0.05, 0.3, '#4a3220', 1.95, 1.98, -3.05);
  const bottleCols = ['#2f5d3a', '#3a3f4c', '#6b4a2a', '#274b63', '#59332b'];
  for (let i = 0; i < 5; i++) {
    const b = G(); b.position.set(1.42 + i * 0.27, 2.0, -3.05); scene.add(b);
    cyl(0.055, 0.06, 0.3, bottleCols[i], 0, 0.15, 0, b); cyl(0.02, 0.035, 0.12, bottleCols[i], 0, 0.36, 0, b);
    rbox(0.07, 0.12, 0.005, 0.002, '#f5efdd', 0, 0.16, 0.058, b);
  }

  // ---- counter (POV sits on the near side; top y = 0.94) ----
  box(scene, 4.4, 0.86, 0.55, '#7a5230', 0, 0.43, -0.62);
  box(scene, 4.5, 0.07, 0.68, '#9a6b3f', 0, 0.905, -0.62);
  box(scene, 4.4, 0.1, 0.03, '#54381f', 0, 0.55, -0.33);
  for (const sx of [-1.5, 0, 1.5]) { const st = cyl(0.16, 0.16, 0.05, '#8a2f27', sx, 0.62, 0.35, scene); st.castShadow = true; cyl(0.03, 0.03, 0.6, '#4a3220', sx, 0.3, 0.35, scene); } // stools on the POV side

  // ---- noren doorway, back-left ----
  box(scene, 1.7, 0.14, 0.12, '#3d2817', -2.45, 2.62, -3.14);
  const dark = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 2.6), basic('#120a06')); dark.position.set(-2.45, 1.3, -3.18); scene.add(dark);
  const norenIn = makeNoren(scene, -2.45, 2.55, -3.08, { w: 0.52, h: 0.85, n: 3 });

  // ---- lanterns ----
  const lan1 = makeLantern(scene, -1.25, 2.32, -1.5);
  const lan2 = makeLantern(scene, 1.05, 2.38, -1.95, 0.19);
  const lan3 = makeLantern(scene, 0.1, 2.45, -0.75, 0.15);
  const pl1 = new THREE.PointLight(0xffa050, 14, 7, 1.8); pl1.position.set(-1.25, 2.25, -1.4); scene.add(pl1);
  const pl2 = new THREE.PointLight(0xffa050, 16, 8, 1.8); pl2.position.set(1.05, 2.3, -1.8); scene.add(pl2);

  // ---- grill + cook, back-right ----
  const grill = G(); grill.position.set(1.62, 0, -2.35); scene.add(grill);
  box(grill, 1.25, 0.78, 0.62, '#2b2b30', 0, 0.39, 0);
  box(grill, 1.3, 0.05, 0.66, '#17171b', 0, 0.8, 0);
  for (let i = 0; i < 4; i++) {
    const sk = G(); sk.position.set(-0.42 + i * 0.27, 0.86, 0); sk.rotation.z = 0.5; grill.add(sk);
    cyl(0.008, 0.008, 0.42, '#c98f4a', 0, 0, 0, sk);
    for (let j = 0; j < 3; j++) rbox(0.075, 0.06, 0.075, 0.02, i % 2 ? '#c96f3a' : '#7fae4c', 0, 0.08 + j * 0.085, 0, sk);
  }
  const grillGlow = box(grill, 1.1, 0.02, 0.5, basic('#ff6a22'), 0, 0.83, 0); grillGlow.castShadow = false;
  const steamGrill = makeSteam(scene, 1.62, 0.95, -2.3, { n: 7, rise: 0.85, spread: 0.3, size: 0.3, speed: 0.13 });
  const cook = toyGuy({ top: '#3a3f4c', pants: '#2a2f3a', hair: '#1c1c20', skin: '#e6b892', seed: 0.35 });
  cook.position.set(1.62, 0, -3.0); cook.rotation.y = 0.12; scene.add(cook);
  sph(0.3, '#f5f2ea', 0, 1.78, 0, cook.userData.body, 1, 0.42, 1); // cook's cap

  // ---- server: indigo top, white apron, hachimaki ----
  const server = toyGuy({ top: '#2e3d66', pants: '#33415c', hair: '#2a1d16', skin: '#f1c9a5', pocket: '#f5f2ea', bun: true, seed: 0.85 });
  server.position.set(0.15, 0, -1.42); scene.add(server);
  rbox(0.38, 0.5, 0.03, 0.02, '#f5f2ea', 0, 0.7, 0.245, server.userData.body); // apron
  cyl(0.435, 0.435, 0.1, '#f5f2ea', 0, 0.17, 0, server.userData.head); // hachimaki band

  // ---- background guests at a side table, back-left ----
  const gTable = G(); gTable.position.set(-1.85, 0, -2.15); scene.add(gTable);
  box(gTable, 1.15, 0.05, 0.8, '#8a5f36', 0, 0.64, 0);
  for (const [x, z] of [[-0.5, -0.32], [0.5, -0.32], [-0.5, 0.32], [0.5, 0.32]]) cyl(0.03, 0.03, 0.62, '#4a3220', x, 0.31, z, gTable);
  const gDish1 = G(); gDish1.position.set(-0.25, 0.665, 0.05); gTable.add(gDish1);
  cyl(0.11, 0.08, 0.045, '#e8e2d2', 0, 0.02, 0, gDish1); sph(0.07, '#c96f3a', 0, 0.05, 0, gDish1, 1, 0.5, 1);
  const gDish2 = G(); gDish2.position.set(0.28, 0.665, -0.08); gTable.add(gDish2);
  cyl(0.11, 0.08, 0.045, '#37414c', 0, 0.02, 0, gDish2); sph(0.07, '#7fae4c', 0, 0.05, 0, gDish2, 1, 0.5, 1);
  for (const [x, z] of [[0.02, 0.22], [-0.42, -0.2]]) { const m = G(); m.position.set(x, 0.665, z); gTable.add(m); cyl(0.045, 0.038, 0.13, M('#cfe0c8', 0.3), 0, 0.065, 0, m); cyl(0.046, 0.046, 0.03, '#f5f2ea', 0, 0.125, 0, m); }
  const steamG1 = makeSteam(gTable, -0.25, 0.72, 0.05, { n: 3, rise: 0.3, spread: 0.03, size: 0.1, speed: 0.2 });
  const steamG2 = makeSteam(gTable, 0.28, 0.72, -0.08, { n: 3, rise: 0.3, spread: 0.03, size: 0.1, speed: 0.17 });
  const guest1 = toyGuy({ top: '#3a5a8a', pants: '#2a2f3a', hair: '#23262f', skin: '#e6b892', seed: 0.5 });
  guest1.position.set(-2.32, -0.44, -2.15); guest1.rotation.y = 1.25; scene.add(guest1);
  const guest2 = toyGuy({ top: '#8a3b3b', pants: '#33415c', hair: '#3b2a20', skin: '#f1c9a5', bun: true, seed: 0.15 });
  guest2.position.set(-1.38, -0.44, -2.2); guest2.rotation.y = -1.85; scene.add(guest2);
  for (const [x, z] of [[-2.32, -1.8], [-1.38, -1.85]]) box(scene, 0.42, 0.08, 0.42, '#8a2f27', x, 0.42, z);

  // ---- props ----
  const P = {}, reg = (name, o) => { scene.add(o); o.userData.home = [o.position.clone(), o.rotation.clone(), o.scale.clone()]; P[name] = o; return o; };
  const otoshi = G(); // the otoshi: little dish on a wooden mini-tray, steam included
  rbox(0.3, 0.02, 0.22, 0.008, '#8a5f36', 0, 0.01, 0, otoshi);
  cyl(0.085, 0.06, 0.05, '#e8e2d2', 0, 0.045, 0, otoshi);
  sph(0.062, '#c96f3a', -0.015, 0.075, 0, otoshi, 1, 0.55, 1);
  sph(0.035, '#7fae4c', 0.045, 0.08, 0.03, otoshi, 1, 0.5, 1);
  sph(0.028, '#f2c27a', 0.03, 0.085, -0.035, otoshi, 1, 0.5, 1);
  otoshi.position.set(0.12, 0.94, -0.78); reg('otoshi', otoshi);
  const steamDish = makeSteam(otoshi, 0, 0.1, 0, { n: 4, rise: 0.34, spread: 0.035, size: 0.11, speed: 0.22 });
  const beer = G(); // a draft beer mug
  cyl(0.055, 0.048, 0.17, M('#e8a33d', 0.25), 0, 0.085, 0, beer);
  cyl(0.056, 0.056, 0.035, '#fdf6e3', 0, 0.175, 0, beer);
  const handle = new THREE.Mesh(new THREE.TorusGeometry(0.045, 0.011, 8, 20), M('#e8a33d', 0.25)); handle.position.set(0.065, 0.09, 0); shd(handle); beer.add(handle);
  beer.position.set(0.62, 0.94, -0.82); reg('beer', beer);

  // ---- POV hands ----
  const camera = cam(58); scene.add(camera);
  const handL = makeHand(-1), handR = makeHand(1); camera.add(handL, handR);
  const sticksR = G(); { const s1 = caps(0.007, 0.17, '#c98f4a', -0.02, 0.03, -0.12, sticksR); s1.rotation.x = Math.PI / 2.15; const s2 = caps(0.007, 0.17, '#c98f4a', 0.022, 0.03, -0.12, sticksR); s2.rotation.x = Math.PI / 2.15; handR.add(sticksR); }
  const REST = { L: [V(-0.17, -0.3, -0.5), new THREE.Euler(-0.3, 0.15, 0.1)], R: [V(0.17, -0.3, -0.5), new THREE.Euler(-0.3, -0.15, -0.1)] };
  const hands = { L: handL, R: handR, sticksR, REST };
  const pv = new THREE.Vector3();
  const api = {
    scene, server, cook, guests: [guest1, guest2], P, hands, camera,
    frozenNow: false, cookCheer: 0,
    screen(v) { pv.copy(v).project(camera); return [(pv.x * 0.5 + 0.5) * 1080, (-pv.y * 0.5 + 0.5) * 1920]; },
  };

  // ambient clock: advances only while not frozen (guests/cook hold their pose in the freeze),
  // while steam / noren / lanterns always run on the real clock.
  let amb = 0, prevGt = 0;
  function tickFx(gt) {
    if (!api.frozenNow) amb += Math.max(0, Math.min(0.1, gt - prevGt));
    prevGt = gt;
    tickSteam(steamGrill, gt); tickSteam(steamDish, gt); tickSteam(steamG1, gt); tickSteam(steamG2, gt);
    tickNoren(norenIn, gt);
    const fl = 1.15 + Math.sin(gt * 11) * 0.1 + Math.sin(gt * 23 + 1.3) * 0.07 + Math.sin(gt * 5.1) * 0.06;
    lan1.mat.emissiveIntensity = fl; lan2.mat.emissiveIntensity = fl * 1.05; lan3.mat.emissiveIntensity = fl * 0.95;
    pl1.intensity = 13 + Math.sin(gt * 13 + 0.5) * 2.2; pl2.intensity = 15 + Math.sin(gt * 12 + 2.1) * 2.4;
    grillGlow.material = basic(Math.sin(gt * 9) > -0.4 ? '#ff6a22' : '#e85a1a');
    // cook works the grill: right arm sweeps the skewers; cheer = both arms up (shout reaction)
    const c = cook.userData, sweep = Math.sin(amb * 1.7) * 0.25;
    if (api.cookCheer > 0.05) { c.arm('R', 2.9, 0.5, 0.3); c.arm('L', 2.7, 0.5, 0.3); cook.position.y = Math.abs(Math.sin(gt * 7)) * 0.03 * api.cookCheer; }
    else { c.reach('R', V(1.35 + sweep * 0.2, 1.0, -2.35)); c.arm('L', 0.3, 0.3, 0.5); cook.position.y = 0; }
    c.face({ lid: 0.18, look: [0, -0.25], mouth: api.cookCheer > 0.05 ? 'o' : 'flat', open: 0.7 });
    cook.userData.tick(amb);
    // guests: one drinks in a slow loop, the other chats/nods; both freeze with the ambient clock
    const g1 = guest1.userData, g2 = guest2.userData;
    const drink = Math.max(0, Math.sin(amb * 0.55)) ** 3;
    g1.arm('R', 0.5 + drink * 1.5, 0.35, 0.4 + drink * 0.9); g1.arm('L', 0.35, 0.3, 0.5);
    g1.head.rotation.x = drink * 0.32; g1.face({ lid: 0.22, look: [0.3, 0], mouth: 'smile' });
    guest1.userData.tick(amb + 2.0);
    g2.arm('R', 0.4, 0.3, 0.6); g2.arm('L', 0.45 + Math.sin(amb * 2.1) * 0.12, 0.3, 0.5);
    g2.head.rotation.z = Math.sin(amb * 2.1) * 0.05; g2.head.rotation.x = Math.max(0, Math.sin(amb * 1.05)) * 0.1;
    g2.face({ lid: 0.28, look: [-0.3, 0], mouth: Math.sin(amb * 2.1) > 0.6 ? 'o' : 'smile', open: 0.6 });
    guest2.userData.tick(amb + 4.0);
  }

  return {
    scene, camera, api,
    update(lt, gt, shot) {
      for (const p of Object.values(P)) {
        p.visible = false; if (p.parent !== scene) scene.add(p);
        const [a, b, c] = p.userData.home; p.position.copy(a); p.rotation.copy(b); p.scale.copy(c);
      }
      for (const n of shot.show || []) P[n].visible = true;
      server.userData.reset(); server.position.set(0.15, 0, -1.42); server.rotation.set(0, 0, 0); server.scale.setScalar(1);
      for (const s of ['L', 'R']) { hands[s].position.copy(REST[s][0]); hands[s].rotation.copy(REST[s][1]); }
      sticksR.visible = false;
      tickFx(gt);
      if (shot.cam) { applyCam(camera, shot.cam, lt, shot.e - shot.s); camera.updateMatrixWorld(true); }
      if (shot.act) shot.act(lt, api, gt, shot);
      server.userData.tick(gt);
    },
  };
}

export function buildIzakayaExterior() {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#1c2733');
  scene.fog = new THREE.Fog(0x1c2733, 10, 24);
  const hemi = new THREE.HemisphereLight(0x8fa8c8, 0x2a2118, 0.75); scene.add(hemi);
  const moon = new THREE.DirectionalLight(0xbcd2ff, 0.7); moon.position.set(-3, 6, 4); moon.castShadow = true;
  moon.shadow.mapSize.set(1024, 1024); Object.assign(moon.shadow.camera, { left: -7, right: 7, top: 7, bottom: -7, near: 0.5, far: 30 });
  moon.shadow.bias = -0.0004; scene.add(moon);
  const G = () => new THREE.Group();

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(24, 16), M('#2e3138', 0.95));
  ground.rotation.x = -Math.PI / 2; ground.position.z = 2; ground.receiveShadow = true; scene.add(ground);
  // neighbouring dark facades
  box(scene, 3.4, 4.6, 0.4, '#232a35', -3.6, 2.3, -2.9);
  box(scene, 3.4, 4.2, 0.4, '#272430', 3.7, 2.1, -2.9);
  // the shop front
  box(scene, 4.0, 3.4, 0.5, '#6e4b2c', 0, 1.7, -2.75);
  box(scene, 4.3, 0.28, 0.7, '#3d2817', 0, 3.5, -2.7);
  box(scene, 4.3, 0.18, 0.7, '#3d2817', 0, 0.35, -2.7);
  // glowing window with interior silhouettes
  const win = box(scene, 1.7, 1.5, 0.06, basic('#ffb36b'), -1.0, 1.75, -2.48); win.castShadow = false;
  box(scene, 0.07, 1.5, 0.08, '#3d2817', -1.0, 1.75, -2.46);
  box(scene, 1.7, 0.07, 0.08, '#3d2817', -1.0, 1.75, -2.46);
  box(scene, 0.5, 0.85, 0.05, '#7a4a20', -1.25, 1.45, -2.44);
  box(scene, 0.42, 0.7, 0.05, '#8a5a28', -0.72, 1.38, -2.44);
  // entrance + noren + lantern
  box(scene, 1.15, 2.5, 0.1, '#17100b', 1.15, 1.25, -2.52);
  const norenOut = makeNoren(scene, 1.15, 2.42, -2.42, { w: 0.4, h: 0.72, n: 3 });
  const lanOut = makeLantern(scene, 2.15, 2.35, -2.3, 0.2);
  const plOut = new THREE.PointLight(0xffa050, 18, 8, 1.8); plOut.position.set(2.15, 2.3, -2.1); scene.add(plOut);
  // vertical sign board
  const signTex = canvasTex(128, 512, (g) => {
    g.fillStyle = '#f5efdd'; g.fillRect(0, 0, 128, 512);
    g.fillStyle = '#2b2b30'; for (let j = 0; j < 4; j++) g.fillRect(34, 40 + j * 112, 60, 74);
    g.fillStyle = '#b03024'; g.fillRect(34, 452, 60, 30);
  });
  const sign = new THREE.Mesh(new THREE.BoxGeometry(0.34, 1.7, 0.08), new THREE.MeshStandardMaterial({ map: signTex, roughness: 0.7 }));
  sign.position.set(-2.15, 2.0, -2.45); shd(sign); scene.add(sign);
  // steam from a side vent
  const vent = G(); vent.position.set(-2.9, 0, -2.2); scene.add(vent);
  cyl(0.09, 0.09, 1.5, '#4a4f57', 0, 0.75, 0, vent);
  const steamVent = makeSteam(scene, -2.9, 1.6, -2.2, { n: 6, rise: 1.1, spread: 0.12, size: 0.3, speed: 0.15 });
  // passer-by
  const walker = toyGuy({ top: '#4f6b4a', pants: '#2a2f3a', hair: '#1c1c20', skin: '#e6b892', seed: 0.6 });
  scene.add(walker);

  const camera = cam(58);
  const api = { scene, walker, camera, frozenNow: false, cookCheer: 0, screen(v) { const pv = v.clone().project(camera); return [(pv.x * 0.5 + 0.5) * 1080, (-pv.y * 0.5 + 0.5) * 1920]; } };
  return {
    scene, camera, api,
    update(lt, gt, shot) {
      tickSteam(steamVent, gt);
      tickNoren(norenOut, gt, 1.5);
      lanOut.mat.emissiveIntensity = 1.2 + Math.sin(gt * 10 + 1) * 0.12 + Math.sin(gt * 27) * 0.06;
      plOut.intensity = 17 + Math.sin(gt * 12.5) * 2.4;
      // the passer-by crosses the front of the shop on a loop, arms swinging, slight bob
      const span = 8.4, x = -4.2 + ((gt * 0.62) % span);
      walker.position.set(x, Math.abs(Math.sin(gt * 4.4)) * 0.035, -1.55);
      walker.rotation.y = Math.PI / 2 - 0.12;
      const sw = Math.sin(gt * 4.4) * 0.4;
      walker.userData.arm('L', 0.3 + sw * 0.5, 0.25, 0.25); walker.userData.arm('R', 0.3 - sw * 0.5, 0.25, 0.25);
      walker.userData.face({ lid: 0.15, look: [0.2, 0], mouth: 'flat' });
      walker.userData.tick(gt);
      if (shot.cam) { applyCam(camera, shot.cam, lt, shot.e - shot.s); camera.updateMatrixWorld(true); }
      if (shot.act) shot.act(lt, api, gt, shot);
    },
  };
}
export { V, lerp, clamp };
