// kitpov: first-person konbini scene for the "Japan POV" format (see pov.js / FORMAT.md).
// buildKonbini() -> { scene, camera, api, update(lt, gt, shot) } — same contract as kit6's buildToyStage.
//   shot: { show: ['tray', ...props], act(lt, api, gt, shot) }
//   api:  { clerk (toyGuy, green/white uniform), P (props by name), hands: {L, R, gripR, teaL}, clerkFace helpers via clerk.userData }
// The POV hands rig is parented to the camera: two hands + mustard sleeves at the bottom of the frame.
//   hands.L / hands.R are groups in CAMERA space (x right, y up, -z forward); act() sets their position/rotation
//   every frame (update() resets them to the rest pose first). hands.gripR = cash held in the right hand,
//   hands.receiptR = receipt in the right hand, hands.teaL = bottled tea in the left hand (all hidden by default).
import { THREE, V, lerp, clamp, canvasTex, cam, basic, applyCam } from './core.js';
import { toyGuy, sph, caps, rbox, cyl, M } from './kit6.js';

const MUSTARD = '#d9a441', SKIN = '#ffd3ad';
const shd = (m) => { m.castShadow = m.receiveShadow = true; return m; };

function makeHand(side) { // side: -1 = left, +1 = right (camera space)
  const g = new THREE.Group();
  // sleeve: mustard forearm running from the wrist DOWN and back toward the camera's lower edge
  // (axis tilted 2.2 rad so the elbow end drops below the palm instead of pointing a disc at the lens)
  const sl = cyl(0.045, 0.056, 0.115, MUSTARD, 0, -0.045, 0.035, g); sl.rotation.x = 2.75;
  sph(0.056, MUSTARD, 0, -0.098, 0.057, g, 1, 0.75, 1); // rounded elbow cap (no open tube end)
  const cuff = cyl(0.055, 0.06, 0.045, '#f5f2ea', 0, -0.022, 0.005, g); cuff.rotation.x = 2.75;
  // palm: flattened sphere; fingers: 4 curled capsules at the front; thumb on the inner side
  sph(0.088, SKIN, 0, 0, -0.03, g, 1.05, 0.55, 1.25);
  for (let i = 0; i < 4; i++) {
    const f = caps(0.021, 0.05, SKIN, (i - 1.5) * 0.042, -0.028, -0.125, g);
    f.rotation.x = Math.PI / 2.6;
  }
  const th = caps(0.024, 0.045, SKIN, side * -0.085, -0.01, -0.07, g); th.rotation.z = side * 0.7; th.rotation.x = 0.5;
  return g;
}
function makeBill() { // a 1000-yen-ish bill, held flat
  const g = new THREE.Group();
  rbox(0.155, 0.004, 0.076, 0.002, '#8aa88a', 0, 0, 0, g);
  rbox(0.13, 0.005, 0.055, 0.002, '#cfe0c8', 0, 0.001, 0, g);
  sph(0.02, '#8aa88a', 0, 0.004, 0, g, 1, 0.25, 1);
  return g;
}
function makeCoin(col = '#c9a227') { return cyl(0.026, 0.026, 0.006, M(col, 0.3), 0, 0, 0, new THREE.Group()); }
function makeTea() { // bottled green tea
  const g = new THREE.Group();
  cyl(0.042, 0.045, 0.21, M('#7fae4c', 0.25), 0, 0, 0, g);
  cyl(0.043, 0.043, 0.07, '#f5f2ea', 0, 0.01, 0, g);
  cyl(0.02, 0.03, 0.05, M('#7fae4c', 0.25), 0, 0.125, 0, g);
  cyl(0.021, 0.021, 0.025, '#3f7a2e', 0, 0.155, 0, g);
  return g;
}

export function buildKonbini() {
  const scene = new THREE.Scene(); scene.background = new THREE.Color('#f2ede2');
  scene.fog = new THREE.Fog(0xf2ede2, 14, 30);
  const hemi = new THREE.HemisphereLight(0xffffff, 0xd8cfbc, 1.55); scene.add(hemi);
  const key = new THREE.DirectionalLight(0xffffff, 2.1); key.position.set(2.5, 5.5, 4.5); key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048); Object.assign(key.shadow.camera, { left: -5, right: 5, top: 5, bottom: -5, near: 0.5, far: 25 });
  key.shadow.bias = -0.0004; scene.add(key);
  const fill = new THREE.DirectionalLight(0xdceaff, 0.55); fill.position.set(-4, 3, 2); scene.add(fill);
  const G = () => new THREE.Group();
  const box = (w, h, d, m, x, y, z, parent = scene) => { const o = shd(new THREE.Mesh(new THREE.BoxGeometry(w, h, d), typeof m === 'string' ? M(m) : m)); o.position.set(x, y, z); parent.add(o); return o; };

  // ---- static set dressing ----
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(30, 30), M('#dfe3e6', 0.9));
  floor.rotation.x = -Math.PI / 2; floor.receiveShadow = true; scene.add(floor);
  const wallTex = canvasTex(1024, 256, (g) => {
    g.fillStyle = '#f7f2e4'; g.fillRect(0, 0, 1024, 256);
    g.fillStyle = '#1faa59'; g.fillRect(0, 150, 1024, 26);
    g.fillStyle = '#ff7a1a'; g.fillRect(0, 182, 1024, 10);
    g.fillStyle = '#2b6cb0'; g.fillRect(0, 198, 1024, 10);
    g.fillStyle = '#22303c'; g.font = '900 44px Arial'; g.textAlign = 'center';
    g.fillText('M A R T · 24h', 512, 92);
    g.fillStyle = '#b9c4c9'; for (let i = 0; i < 12; i++) g.fillRect(28 + i * 84, 112, 52, 22);
  });
  const wall = new THREE.Mesh(new THREE.PlaneGeometry(11, 2.75), new THREE.MeshStandardMaterial({ map: wallTex, roughness: 0.9 }));
  wall.position.set(0, 1.85, -2.9); wall.receiveShadow = true; scene.add(wall);
  box(11, 0.5, 0.1, '#e8e2d2', 0, 3.45, -2.9); // pelmet above the wall sign
  for (const x of [-1.6, 1.6]) { const p = box(2.6, 0.06, 0.5, basic('#fff6da'), x, 3.1, -0.6); p.castShadow = false; } // ceiling light panels
  // counter: body + light top slab, front edge at z = 0.05
  box(3.6, 0.9, 0.8, '#3d7a8c', 0, 0.45, -0.35);
  box(3.7, 0.07, 0.9, '#f6f1e7', 0, 0.945, -0.35);
  box(3.6, 0.16, 0.02, '#1faa59', 0, 0.78, 0.06);
  // drink fridge (right, behind the counter line): glass door + colourful cans
  {
    const f = G(); f.position.set(2.45, 0, -1.7); f.rotation.y = -0.38; scene.add(f);
    box(1.15, 2.05, 0.72, '#cfd8dc', 0, 1.02, 0, f);
    const glass = new THREE.Mesh(new THREE.PlaneGeometry(0.95, 1.8), new THREE.MeshStandardMaterial({ color: '#bfe6f5', transparent: true, opacity: 0.35, roughness: 0.15 }));
    glass.position.set(0, 1.05, 0.37); f.add(glass);
    const cols = ['#e2463c', '#2b6cb0', '#f2b705', '#3fae5b', '#ff7a1a', '#7a4fd0'];
    for (let s = 0; s < 3; s++) for (let i = 0; i < 5; i++) {
      const c = cyl(0.045, 0.045, 0.13, cols[(s * 5 + i) % 6], -0.38 + i * 0.19, 0.55 + s * 0.5, 0.18, f); c.castShadow = false;
    }
  }
  // shelves (left): 3 boards of colourful packages
  {
    const s = G(); s.position.set(-2.5, 0, -1.5); s.rotation.y = 0.38; scene.add(s);
    box(0.08, 2.0, 0.5, '#8a6f4d', -0.65, 1.0, 0, s); box(0.08, 2.0, 0.5, '#8a6f4d', 0.65, 1.0, 0, s);
    const cols = ['#ff8a65', '#ffd23a', '#7bd88f', '#5aa9ff', '#ff7eb6', '#ffffff'];
    for (let b = 0; b < 3; b++) {
      box(1.4, 0.05, 0.5, '#a8875e', 0, 0.45 + b * 0.55, 0, s);
      for (let i = 0; i < 5; i++) box(0.2, 0.3, 0.3, cols[(b * 5 + i) % 6], -0.52 + i * 0.26, 0.63 + b * 0.55, 0, s);
    }
  }
  // hanging sign over the counter
  {
    const t = canvasTex(512, 128, (g) => { g.fillStyle = '#22303c'; g.fillRect(0, 0, 512, 128); g.fillStyle = '#ffffff'; g.font = '900 62px Arial'; g.textAlign = 'center'; g.fillText('REGISTER', 256, 84); });
    const s = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.33, 0.05), new THREE.MeshStandardMaterial({ map: t, roughness: 0.7 }));
    s.position.set(0, 2.78, -1.7); scene.add(s);
  }

  // ---- props (reset + hidden each frame unless listed in shot.show) ----
  const P = {}, reg = (name, o) => { scene.add(o); o.userData.home = [o.position.clone(), o.rotation.clone(), o.scale.clone()]; P[name] = o; return o; };
  // cash tray: blue, on the counter. cashOnTray / changeOnTray are children so the tray carries them when it slides.
  const tray = G(); tray.position.set(-0.18, 0.985, -0.12); scene.add(tray);
  rbox(0.36, 0.025, 0.26, 0.008, '#2563eb', 0, 0, 0, tray);
  rbox(0.36, 0.045, 0.02, 0.008, '#2563eb', 0, 0.012, -0.12, tray); rbox(0.36, 0.045, 0.02, 0.008, '#2563eb', 0, 0.012, 0.12, tray);
  rbox(0.02, 0.045, 0.26, 0.008, '#2563eb', -0.17, 0.012, 0, tray); rbox(0.02, 0.045, 0.26, 0.008, '#2563eb', 0.17, 0.012, 0, tray);
  tray.userData.home = [tray.position.clone(), tray.rotation.clone(), tray.scale.clone()];
  P.tray = tray;
  const cashOnTray = G(); { const b = makeBill(); b.position.set(-0.04, 0.022, 0); b.rotation.y = 0.25; cashOnTray.add(b);
    const c1 = makeCoin(); c1.position.set(0.09, 0.02, 0.05); cashOnTray.add(c1); const c2 = makeCoin('#b8bdc4'); c2.position.set(0.12, 0.02, -0.04); cashOnTray.add(c2); tray.add(cashOnTray); }
  const changeOnTray = G(); { const c1 = makeCoin(); c1.position.set(-0.08, 0.02, 0.04); changeOnTray.add(c1);
    const c2 = makeCoin('#c9a227'); c2.position.set(-0.03, 0.02, -0.05); changeOnTray.add(c2); const c3 = makeCoin('#b8bdc4'); c3.position.set(0.02, 0.02, 0.05); changeOnTray.add(c3);
    rbox(0.09, 0.004, 0.15, 0.002, '#ffffff', 0.1, 0.02, 0, changeOnTray).rotation.y = -0.2; tray.add(changeOnTray); }
  // register: base + tilted screen showing the total
  {
    const r = G(); r.position.set(0.78, 0.98, -0.55); r.rotation.y = -0.22; scene.add(r);
    rbox(0.42, 0.16, 0.4, 0.03, '#37414c', 0, 0.08, 0, r);
    const scrTex = canvasTex(256, 160, (g) => { g.fillStyle = '#0d1f16'; g.fillRect(0, 0, 256, 160); g.fillStyle = '#7dff9a'; g.font = '700 34px monospace'; g.fillText('TOTAL', 18, 55); g.font = '900 52px monospace'; g.fillText('¥550', 18, 125); });
    const scr = new THREE.Mesh(new THREE.PlaneGeometry(0.4, 0.25), new THREE.MeshStandardMaterial({ map: scrTex, roughness: 0.4 }));
    scr.position.set(0, 0.32, 0.1); scr.rotation.x = -0.28; r.add(scr);
    rbox(0.44, 0.3, 0.03, 0.02, '#37414c', 0, 0.3, 0.06, r).rotation.x = -0.28;
    r.userData.home = [r.position.clone(), r.rotation.clone(), r.scale.clone()]; P.register = r;
  }
  // bottled tea + an onigiri on the counter (the things you are buying)
  const tea = makeTea(); tea.position.set(0.34, 1.09, -0.28); reg('tea', tea);
  { const o = G(); o.position.set(-0.85, 0.98, -0.3); scene.add(o);
    sph(0.09, '#ffffff', 0, 0.045, 0, o, 1.1, 0.62, 0.8); rbox(0.1, 0.07, 0.02, 0.01, '#20301f', 0, 0.04, 0.055, o);
    o.userData.home = [o.position.clone(), o.rotation.clone(), o.scale.clone()]; P.onigiri = o; }

  // ---- clerk: toyGuy in a green/white uniform, behind the counter ----
  const clerk = toyGuy({ top: '#1faa59', pants: '#33415c', hair: '#2a2a2e', skin: '#f1c9a5', pocket: '#ffffff', seed: 0.7 });
  clerk.position.set(0.05, 0, -1.18); scene.add(clerk);
  rbox(0.36, 0.46, 0.03, 0.02, '#ffffff', 0, 0.72, 0.245, clerk.userData.body); // apron panel
  rbox(0.11, 0.06, 0.012, 0.01, '#ffd23a', 0.14, 1.0, 0.26, clerk.userData.body); // name tag

  // ---- POV hands rig (child of the camera) ----
  const camera = cam(58);
  scene.add(camera);
  const handL = makeHand(-1), handR = makeHand(1);
  camera.add(handL, handR);
  const gripR = G(); { const b = makeBill(); b.rotation.x = -0.15; gripR.add(b); const c = makeCoin(); c.position.set(0.05, 0.012, 0.03); gripR.add(c); gripR.position.set(0, 0.045, -0.06); handR.add(gripR); }
  const receiptR = rbox(0.09, 0.004, 0.15, 0.002, '#ffffff', 0, 0.045, -0.06, handR); receiptR.rotation.x = -0.15;
  const teaL = makeTea(); teaL.rotation.x = 0.5; teaL.position.set(0, 0.02, -0.1); handL.add(teaL);
  const REST = { L: [V(-0.155, -0.28, -0.52), new THREE.Euler(-0.3, 0.15, 0.1)], R: [V(0.155, -0.28, -0.52), new THREE.Euler(-0.3, -0.15, -0.1)] };
  const hands = { L: handL, R: handR, gripR, receiptR, teaL, REST };
  const pv = new THREE.Vector3();
  const api = { scene, clerk, P, hands, cashOnTray, changeOnTray, camera, screen(v) { pv.copy(v).project(camera); return [(pv.x * 0.5 + 0.5) * 1080, (-pv.y * 0.5 + 0.5) * 1920]; } };

  return {
    scene, camera, api,
    update(lt, gt, shot) {
      for (const p of Object.values(P)) {
        p.visible = false; if (p.parent !== scene && p !== tray) scene.add(p);
        const [a, b, c] = p.userData.home; p.position.copy(a); p.rotation.copy(b); p.scale.copy(c);
      }
      cashOnTray.visible = false; changeOnTray.visible = false;
      for (const n of shot.show || []) P[n].visible = true;
      clerk.userData.reset(); clerk.position.set(0.05, 0, -1.18); clerk.rotation.set(0, 0, 0); clerk.scale.setScalar(1);
      for (const s of ['L', 'R']) { hands[s].position.copy(REST[s][0]); hands[s].rotation.copy(REST[s][1]); }
      gripR.visible = false; receiptR.visible = false; teaL.visible = false;
      if (shot.cam) { applyCam(camera, shot.cam, lt, shot.e - shot.s); camera.updateMatrixWorld(true); }
      if (shot.act) shot.act(lt, api, gt, shot);
      clerk.userData.tick(gt);
    },
  };
}
export { V, lerp, clamp };
