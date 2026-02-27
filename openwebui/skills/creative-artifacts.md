---
name: creative-artifacts
description: Build rich, polished, interactive HTML and React artifacts with exceptional visual quality and creative ambition. Use this skill for any request involving an interactive web component, mini-application, game, tool, calculator, simulator, generative art piece, animated visualization, creative UI, dashboard widget, or any deliverable that lives in the browser and benefits from interactivity, animation, or a distinct visual identity. Trigger on requests like "build me a…", "create an interactive…", "make a…tool/game/component/app/widget/demo", or any prompt where the output should feel designed and alive rather than static. The default bar is high: artifacts from this skill should surprise and delight — not just function correctly. Always ask "what would make this feel polished and memorable?" before writing a single line.
---

# Creative Artifacts Skill — React & HTML

This skill is about building browser artifacts that are **both functional and beautiful**. The technical foundations (CDN imports, rendering patterns) matter, but design quality and creative ambition matter just as much.

---

## Step 1 — Choose the Right Format

| Use HTML + vanilla JS | Use React (.jsx) |
|---|---|
| Generative art, canvas animations, WebGL | Component-heavy UIs, multi-state apps |
| Single interaction / single view | Tabbed interfaces, multi-step flows |
| Pure CSS visual effects | Dynamic lists, filtered data, forms |
| Performance-critical rendering loops | Anything needing `useState` / `useEffect` |
| No UI state to manage | Reusable, composable widgets |

**When in doubt: React.** Its component model and state management make complexity tractable. Use HTML when you need raw `<canvas>` control, WebGL, or a single self-contained animation with no state.

---

## Step 2 — Available Libraries (React artifacts)

All imports come from CDN — no bundler, no `package.json`. Use exactly these import paths:

```jsx
// Core React (always available, no import needed in .jsx artifacts)
import { useState, useEffect, useRef, useCallback, useMemo, useReducer } from "react";

// UI icons (~260 icons, lightweight)
import { Search, Star, Heart, ArrowRight, ChevronDown, X, Menu,
         Check, AlertCircle, Loader2, Play, Pause, RotateCcw } from "lucide-react";

// Charts (works alongside Recharts, not D3)
import { LineChart, BarChart, AreaChart, RadarChart, PieChart,
         Line, Bar, Area, Radar, Pie, Cell,
         XAxis, YAxis, CartesianGrid, Tooltip, Legend,
         ResponsiveContainer } from "recharts";

// shadcn/ui components (inform user when used — requires their setup)
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Progress } from "@/components/ui/progress";
import { Slider } from "@/components/ui/slider";
import { Switch } from "@/components/ui/switch";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";

// D3 (full library — use for custom data viz inside React)
import * as d3 from "d3";

// Math engine
import * as math from "mathjs";

// Utilities
import _ from "lodash";

// Animation / music (advanced)
import * as Tone from "tone";
import * as THREE from "three";      // r128 — no OrbitControls, no CapsuleGeometry
```

**NEVER use localStorage, sessionStorage, or any browser storage APIs in artifacts** — they are not supported. Store all state in React state (`useState`, `useReducer`) or JavaScript variables.

---

## Step 3 — Available Libraries (HTML artifacts)

For plain HTML files, load libraries from CDN in `<script>` tags:

```html
<!-- D3.js — data visualization, SVG manipulation -->
<script src="https://cdn.jsdelivr.net/npm/d3@7"></script>

<!-- Three.js r128 — 3D WebGL rendering -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<!-- Tone.js — audio synthesis and scheduling -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/tone/14.8.49/Tone.js"></script>

<!-- Anime.js — timeline-based DOM animations -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>

<!-- GSAP — professional-grade animation -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>

<!-- p5.js — creative coding, generative art -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>

<!-- Chart.js — standard charts -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>

<!-- Plotly.js — interactive scientific charts -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.2/plotly-basic.min.js"></script>

<!-- Vis Network / Timeline — (see dedicated skills) -->
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script src="https://unpkg.com/vis-timeline@latest/standalone/umd/vis-timeline-graph2d.min.js"></script>
<link  href="https://unpkg.com/vis-timeline@latest/styles/vis-timeline-graph2d.min.css" rel="stylesheet"/>

<!-- Mermaid — diagrams from text -->
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>

<!-- MathJax — LaTeX rendering -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-chtml.min.js"></script>

<!-- Prism.js — code syntax highlighting -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet"/>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
```

---

## Step 4 — React Artifact Shell

```jsx
import { useState, useEffect, useRef } from "react";

// Tailwind is available via pre-compiled core utilities — use class names directly
// ONLY use core Tailwind classes (no JIT, no custom values like `w-[372px]`)

export default function MyArtifact() {
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-2xl bg-gray-900 rounded-2xl p-8 shadow-2xl">
        <h1 className="text-2xl font-bold text-white mb-2">Title</h1>
        <p className="text-gray-400 text-sm mb-6">Subtitle</p>

        {/* Content */}
        <button
          onClick={() => setCount(c => c + 1)}
          className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 rounded-lg font-medium transition-colors"
        >
          Count: {count}
        </button>
      </div>
    </div>
  );
}
```

**Tailwind constraints in artifacts:**
- Only pre-compiled core classes work — no arbitrary values like `w-[372px]`
- Use `style={{}}` for pixel-perfect custom dimensions
- Core classes: all standard `p-`, `m-`, `text-`, `bg-`, `border-`, `flex`, `grid`, `rounded-`, `shadow-`, `opacity-`, `transition-` classes work

---

## Step 5 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Artifact</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      min-height: 100vh;
    }
    /* Layout, typography, animation — all inline here */
  </style>
</head>
<body>
  <!-- Markup -->

  <!-- Libraries LAST, before your script -->
  <script src="...CDN..."></script>
  <script>
    // App code
  </script>
</body>
</html>
```

---

## Step 6 — Design System (use consistently across all artifacts)

### Color palette
```css
/* Dark theme (default) */
--bg-deep:      #0f1117   /* page background */
--bg-surface:   #1a1d27   /* card / panel */
--bg-elevated:  #1e2130   /* tooltip, dropdown */
--border:       rgba(255,255,255,0.08)
--text-primary: #f1f5f9
--text-muted:   #94a3b8
--text-faint:   #475569

/* Accent palette */
--indigo:  #6366f1   --indigo-light: #818cf8
--violet:  #8b5cf6   --pink:         #ec4899
--red:     #f43f5e   --orange:       #f97316
--amber:   #eab308   --green:        #22c55e
--teal:    #14b8a6   --cyan:         #06b6d4
--blue:    #3b82f6
```

### Typography scale
```css
--text-xs:   0.75rem / 1.1  /* captions, labels */
--text-sm:   0.875rem / 1.4 /* body small */
--text-base: 1rem / 1.5     /* body */
--text-lg:   1.125rem / 1.5 /* subheadings */
--text-xl:   1.25rem / 1.4  /* headings */
--text-2xl:  1.5rem / 1.3   /* display */
--text-3xl:  1.875rem / 1.2 /* hero */

font-weight: 400 (body) / 500 (medium) / 600 (semibold) / 700 (bold)
```

### Elevation / depth
```css
/* Cards */    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
/* Modals */   box-shadow: 0 16px 64px rgba(0,0,0,0.6);
/* Floating */ box-shadow: 0 2px 8px rgba(0,0,0,0.3);
/* Glows */    box-shadow: 0 0 24px rgba(99,102,241,0.3);
```

### Motion
```css
/* Micro-interactions */
transition: all 0.15s ease;

/* Entrances */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(12px); }
  to   { opacity: 1; transform: translateY(0); }
}
animation: fadeUp 0.3s ease forwards;

/* Pulse / breathing */
@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: 0.7; transform: scale(0.97); }
}
```

---

## Step 7 — Creative Patterns & Ideas by Category

### 🎨 Generative Art (HTML + Canvas / p5.js)

Think beyond static shapes. Ask: what would make this *alive*?

```javascript
// Perlin noise flow field
const ctx = canvas.getContext('2d');
let t = 0;
function draw() {
  ctx.fillStyle = 'rgba(15,17,23,0.05)'; // trail fade
  ctx.fillRect(0, 0, W, H);
  for (const p of particles) {
    const angle = noise(p.x * 0.003, p.y * 0.003, t) * Math.PI * 4;
    p.x += Math.cos(angle) * 1.5;
    p.y += Math.sin(angle) * 1.5;
    ctx.beginPath();
    ctx.arc(p.x, p.y, 1.2, 0, Math.PI * 2);
    ctx.fillStyle = `hsl(${(angle / Math.PI) * 60 + 220}, 80%, 70%)`;
    ctx.fill();
    if (p.x < 0 || p.x > W || p.y < 0 || p.y > H) resetParticle(p);
  }
  t += 0.003;
  requestAnimationFrame(draw);
}
```

**Generative art ideas to suggest or implement unprompted when relevant:**
- Particle systems with attraction/repulsion forces
- Lissajous curves evolving over time
- Reaction-diffusion systems (Turing patterns)
- Cellular automata (Game of Life, Langton's Ant)
- Truchet tiles, Penrose tiling
- Voronoi diagrams with animated seeds
- Fractal trees that grow in real time
- Wave interference patterns

### 🎮 Mini Games (HTML or React)

```javascript
// Game loop pattern
let state = { score: 0, lives: 3, running: true };
let lastTime = 0;

function gameLoop(timestamp) {
  const dt = (timestamp - lastTime) / 1000; // delta in seconds
  lastTime = timestamp;
  if (state.running) {
    update(dt);
    render();
    requestAnimationFrame(gameLoop);
  }
}
requestAnimationFrame(gameLoop);

// Input handling
const keys = {};
window.addEventListener('keydown', e => { keys[e.key] = true; e.preventDefault(); });
window.addEventListener('keyup',   e => { keys[e.key] = false; });
```

**Game ideas**: Snake, Tetris, breakout/Arkanoid, memory match, typing speed test, reaction timer, platformer physics demo, flocking simulation (boids), particle physics sandbox.

### 📊 Interactive Dashboards (React + Recharts)

```jsx
import { useState } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1e2130', border: '1px solid rgba(255,255,255,0.1)', borderRadius: 8, padding: '8px 14px' }}>
      <p style={{ color: '#94a3b8', fontSize: 12, marginBottom: 4 }}>{label}</p>
      {payload.map(p => (
        <p key={p.name} style={{ color: p.color, fontSize: 14, fontWeight: 600 }}>
          {p.name}: {p.value.toLocaleString()}
        </p>
      ))}
    </div>
  );
};

// Usage inside a chart
<ResponsiveContainer width="100%" height={300}>
  <AreaChart data={data}>
    <defs>
      <linearGradient id="grad1" x1="0" y1="0" x2="0" y2="1">
        <stop offset="5%"  stopColor="#6366f1" stopOpacity={0.3}/>
        <stop offset="95%" stopColor="#6366f1" stopOpacity={0}/>
      </linearGradient>
    </defs>
    <XAxis dataKey="month" stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} />
    <YAxis stroke="#475569" tick={{ fill: '#94a3b8', fontSize: 12 }} />
    <Tooltip content={<CustomTooltip />} />
    <Area type="monotone" dataKey="value" stroke="#6366f1" fill="url(#grad1)" strokeWidth={2} />
  </AreaChart>
</ResponsiveContainer>
```

### 🔧 Tools & Calculators (React)

Design principles:
- Input → live computation → output (no submit button needed)
- Use `useMemo` for expensive recalculations
- Show intermediate steps when educational
- Copy-to-clipboard button on outputs
- Keyboard shortcuts for power users

```jsx
// Live calculation pattern
const result = useMemo(() => {
  if (!input || isNaN(+input)) return null;
  return compute(+input);
}, [input]);

// Copy to clipboard
const [copied, setCopied] = useState(false);
const copy = async (text) => {
  await navigator.clipboard.writeText(text);
  setCopied(true);
  setTimeout(() => setCopied(false), 1500);
};
```

### ✨ Micro-interactions & Animations

```jsx
// Stagger children on mount
const items = ['a', 'b', 'c'];
return (
  <div>
    {items.map((item, i) => (
      <div
        key={item}
        style={{
          animation: `fadeUp 0.3s ease ${i * 0.06}s both`,
        }}
      >
        {item}
      </div>
    ))}
  </div>
);

// Number counter animation
function useCounter(target, duration = 1000) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    let start = null;
    const step = (ts) => {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      setValue(Math.floor(progress * target));
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [target, duration]);
  return value;
}

// Spring-like hover scale (CSS only)
// className="transition-transform duration-150 hover:scale-105 active:scale-95"
```

### 🌐 3D Scenes (Three.js)

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
  const scene    = new THREE.Scene();
  const camera   = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setSize(innerWidth, innerHeight);
  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  document.body.appendChild(renderer.domElement);

  // Lights
  scene.add(new THREE.AmbientLight(0xffffff, 0.4));
  const dir = new THREE.DirectionalLight(0xffffff, 1);
  dir.position.set(5, 10, 5);
  scene.add(dir);

  // Geometry
  const geo  = new THREE.IcosahedronGeometry(1, 0);
  const mat  = new THREE.MeshStandardMaterial({ color: 0x6366f1, metalness: 0.3, roughness: 0.4, wireframe: false });
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);
  camera.position.z = 3;

  // Animate
  function animate() {
    requestAnimationFrame(animate);
    mesh.rotation.x += 0.005;
    mesh.rotation.y += 0.008;
    renderer.render(scene, camera);
  }
  animate();

  // Responsive
  window.addEventListener('resize', () => {
    camera.aspect = innerWidth / innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(innerWidth, innerHeight);
  });
</script>
```

**Note:** Three.js r128 — do NOT use `THREE.CapsuleGeometry` (added in r142). Use `CylinderGeometry`, `SphereGeometry`, or lathe geometry instead.

---

## Step 8 — Polish Checklist

Every artifact before shipping:

**Functionality**
- [ ] All interactive elements respond correctly
- [ ] No console errors
- [ ] Edge cases handled (empty state, zero values, out-of-range inputs)
- [ ] Loading states shown when async

**Design**
- [ ] Consistent color palette (use the design system tokens)
- [ ] Typography hierarchy is clear (title > body > caption)
- [ ] Sufficient contrast for text (≥ 4.5:1 for body, ≥ 3:1 for large text)
- [ ] Hover and active states on all interactive elements
- [ ] Spacing is consistent (8px grid: 4, 8, 12, 16, 24, 32, 48, 64)
- [ ] No raw `<form>` tags — use `onClick`/`onChange` handlers instead
- [ ] Responsive (doesn't overflow or break on narrow viewports)

**Delight**
- [ ] At least one meaningful animation or transition
- [ ] Micro-feedback on interactions (button press, copy confirm, etc.)
- [ ] The artifact has a clear purpose that is immediately obvious
- [ ] There is something in the design that would make the user pause and notice

---

## Step 9 — Complete Example: Interactive Particle Physics

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Particle Gravity</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { background: #0f1117; overflow: hidden; font-family: 'Segoe UI', sans-serif; }
    canvas { display: block; }
    #ui {
      position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
      background: rgba(26,29,39,0.85); backdrop-filter: blur(12px);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 12px; padding: 12px 20px;
      display: flex; gap: 16px; align-items: center;
      color: #94a3b8; font-size: 13px;
    }
    .stat { display: flex; flex-direction: column; align-items: center; gap: 2px; }
    .stat-val { color: #f1f5f9; font-size: 18px; font-weight: 600; font-variant-numeric: tabular-nums; }
    kbd {
      background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
      border-radius: 4px; padding: 2px 6px; font-size: 11px; color: #e2e8f0;
    }
  </style>
</head>
<body>
  <div id="ui">
    <div class="stat"><span class="stat-val" id="count">0</span><span>particles</span></div>
    <div class="stat"><span class="stat-val" id="fps">60</span><span>fps</span></div>
    <span style="color:#475569">|</span>
    <span>Click to attract &nbsp; <kbd>Space</kbd> burst &nbsp; <kbd>R</kbd> reset</span>
  </div>
  <canvas id="c"></canvas>
  <script>
    const canvas = document.getElementById('c');
    const ctx = canvas.getContext('2d');
    let W, H;

    const resize = () => { W = canvas.width = innerWidth; H = canvas.height = innerHeight; };
    resize();
    window.addEventListener('resize', resize);

    const mouse = { x: W / 2, y: H / 2, down: false };
    canvas.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
    canvas.addEventListener('mousedown', () => { mouse.down = true; });
    canvas.addEventListener('mouseup',   () => { mouse.down = false; });

    const COLORS = ['#6366f1','#8b5cf6','#ec4899','#f43f5e','#f97316','#06b6d4'];
    const particles = [];

    function spawn(x, y, vx = 0, vy = 0) {
      particles.push({
        x: x ?? Math.random() * W,
        y: y ?? Math.random() * H,
        vx: vx + (Math.random() - 0.5) * 4,
        vy: vy + (Math.random() - 0.5) * 4,
        r:  Math.random() * 2.5 + 1,
        color: COLORS[Math.floor(Math.random() * COLORS.length)],
        alpha: 1,
        life: 1,
      });
    }

    for (let i = 0; i < 120; i++) spawn();

    window.addEventListener('keydown', e => {
      if (e.code === 'Space') {
        e.preventDefault();
        for (let i = 0; i < 40; i++) {
          const angle = (i / 40) * Math.PI * 2;
          spawn(W / 2, H / 2, Math.cos(angle) * 6, Math.sin(angle) * 6);
        }
      }
      if (e.code === 'KeyR') particles.length = 0, setTimeout(() => { for (let i = 0; i < 120; i++) spawn(); }, 50);
    });

    let lastT = 0, frameCount = 0, fps = 60;

    function frame(t) {
      requestAnimationFrame(frame);
      const dt = Math.min((t - lastT) / 16, 3);
      lastT = t;
      frameCount++;
      if (frameCount % 30 === 0) {
        fps = Math.round(1000 / ((t - lastT + 16) / 2));
        document.getElementById('count').textContent = particles.length;
        document.getElementById('fps').textContent   = fps;
      }

      ctx.fillStyle = 'rgba(15,17,23,0.18)';
      ctx.fillRect(0, 0, W, H);

      for (let i = particles.length - 1; i >= 0; i--) {
        const p = particles[i];

        if (mouse.down) {
          const dx = mouse.x - p.x, dy = mouse.y - p.y;
          const dist = Math.sqrt(dx * dx + dy * dy) + 1;
          const force = Math.min(300 / (dist * dist), 0.8);
          p.vx += (dx / dist) * force * dt;
          p.vy += (dy / dist) * force * dt;
        }

        // Gravity well at center (gentle)
        const cx = W / 2 - p.x, cy = H / 2 - p.y;
        const cd = Math.sqrt(cx * cx + cy * cy) + 1;
        p.vx += (cx / cd) * 0.04 * dt;
        p.vy += (cy / cd) * 0.04 * dt;

        // Damping
        p.vx *= 0.992;
        p.vy *= 0.992;

        p.x += p.vx * dt;
        p.y += p.vy * dt;

        // Bounce off edges
        if (p.x < 0 || p.x > W) p.vx *= -0.7;
        if (p.y < 0 || p.y > H) p.vy *= -0.7;
        p.x = Math.max(0, Math.min(W, p.x));
        p.y = Math.max(0, Math.min(H, p.y));

        const speed = Math.sqrt(p.vx * p.vx + p.vy * p.vy);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r + speed * 0.15, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = 0.85;
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    }
    requestAnimationFrame(frame);
  </script>
</body>
</html>
```

---

## Creative Mandate

**The default output from this skill should be surprising.** When the request is open-ended or leaves room for creative interpretation:

- Choose a visual direction, don't default to the most generic version
- Add an animation that wasn't explicitly asked for if it elevates the result
- Pick a color treatment — don't use browser defaults
- Include micro-interactions: hover effects, transitions, feedback
- If you're building a tool, make the output feel designed, not printed
- If you're building art, make it move and breathe

The question to ask before finalizing: *"Would I be proud to show this to someone?"*
