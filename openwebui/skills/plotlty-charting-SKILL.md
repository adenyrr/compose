---
name: charting
description: Create polished, interactive data charts using Plotly.js or Chart.js, delivered as self-contained HTML artifacts. Use this skill for quantitative data visualization: bar charts, line charts, pie/donut charts, scatter plots, radar charts, bubble charts, histograms, box plots, violin plots, heatmaps, financial charts (candlestick/OHLC), 3D surfaces, subplots, and mixed charts. Trigger on requests to visualize metrics, compare values, show distributions, display trends, build dashboards, or plot any dataset — even without explicit mention of Chart.js or Plotly. Do NOT use this skill for: network/node-edge graphs (→ vis-network skill), timelines or Gantt charts (→ vis-timeline skill), or bespoke/pixel-perfect SVG visualizations with custom layouts (→ d3-charting skill).
---

# Charting Skill — Plotly.js & Chart.js

This skill guides the creation of polished, interactive **data charts** as single-file HTML artifacts. Both libraries are purpose-built for quantitative visualization: they excel at turning datasets into readable, interactive charts with minimal code.

---

## Step 1 — Route to the Right Skill First

Before choosing between Chart.js and Plotly, verify this is the right skill to use:

| What is needed | Skill to use |
|---|---|
| Data charts: bars, lines, pie, scatter, histograms, heatmaps, box plots, financial… | **This skill** (charting) |
| Nodes and edges, relationship graphs, network topology, org charts | **vis-network** |
| Events on a time axis, Gantt charts, project roadmaps, chronologies | **vis-timeline** |
| Bespoke SVG layout, force simulation, geo projections, custom animations, pixel-perfect control | **d3-charting** |

If the request is genuinely a data chart, continue below.

---

## Step 2 — Choose Between Chart.js and Plotly.js

| Criterion | Chart.js | Plotly.js |
|---|---|---|
| Chart types | Bar, line, pie, doughnut, radar, polarArea, scatter, bubble, mixed | All of Chart.js + box, violin, histogram, heatmap, contour, 3D surface/scatter, candlestick, OHLC, funnel, waterfall, treemap, sankey |
| Interactivity | Tooltips, hover, legend toggle | Full: zoom, pan, lasso select, range slider, dropdown/button controls, animated transitions |
| Data volume | ≤ 100 000 points | 100 000+ points → `scattergl` / `heatmapgl` (WebGL) |
| Bundle weight | ~200 KB | ~3.5 MB full / ~1 MB basic |
| Scientific / statistical | Basic | Full: error bars, log axes, ECDF, regression annotations |
| API style | Options object, imperative updates | Declarative JSON traces + layout |

**Rule of thumb:** standard charts for dashboards or presentations → **Chart.js**. Scientific, statistical, financial, 3D, or deeply interactive → **Plotly.js**.

---

## Step 3 — CDN Setup

### Chart.js
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
```
Optional plugin (data labels):
```html
<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
```

### Plotly.js
```html
<!-- Basic bundle (~1 MB) — all standard 2D charts, no 3D/maps/WebGL -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.2/plotly-basic.min.js"></script>

<!-- Full bundle (~3.5 MB) — needed for 3D, geo maps, scattergl/heatmapgl -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.2/plotly.min.js"></script>
```
Default to the **basic bundle** — it loads 3× faster and covers the vast majority of use cases.

---

## Step 4 — HTML Artifact Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Chart Title</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
      background: #0f1117;
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 24px;
    }
    .card {
      width: 100%;
      max-width: 900px;
      background: #1a1d27;
      border-radius: 16px;
      padding: 32px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    }
    h1 { font-size: 1.4rem; font-weight: 600; color: #f1f5f9; margin-bottom: 6px; }
    p.sub { font-size: 0.875rem; color: #94a3b8; margin-bottom: 24px; }

    /* Chart.js — canvas needs explicit max-width; height via aspectRatio option */
    canvas { max-width: 100%; }
    /* Plotly — div needs explicit height */
    #plotly-chart { width: 100%; height: 480px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Chart Title</h1>
    <p class="sub">Brief description or data source</p>

    <!-- Chart.js -->
    <canvas id="myChart"></canvas>

    <!-- Plotly.js (swap in instead of canvas above) -->
    <!-- <div id="plotly-chart"></div> -->
  </div>

  <script src="...CDN..."></script>
  <script>
    // Chart code here — after CDN and DOM are ready
  </script>
</body>
</html>
```

**Theming tokens (dark theme — default):**

| Token | Value |
|---|---|
| Page background | `#0f1117` |
| Card background | `#1a1d27` |
| Grid lines | `rgba(255,255,255,0.06)` |
| Axis text / labels | `#94a3b8` |
| Title | `#f1f5f9` |
| Subtitle | `#64748b` |

Light theme: page `#f8fafc`, card `#ffffff`, grid `rgba(0,0,0,0.08)`, text `#475569`.

---

## Step 5 — Chart.js Patterns

### Minimal setup
```javascript
Chart.defaults.color       = '#94a3b8';
Chart.defaults.borderColor = 'rgba(255,255,255,0.08)';
Chart.defaults.font.family = "'Inter', 'Segoe UI', sans-serif";
Chart.defaults.font.size   = 13;

const chart = new Chart(document.getElementById('myChart').getContext('2d'), {
  type: 'bar', // 'line'|'pie'|'doughnut'|'radar'|'polarArea'|'scatter'|'bubble'
  data: {
    labels: ['Jan', 'Feb', 'Mar'],
    datasets: [{
      label:           'Revenue',
      data:            [120, 190, 150],
      backgroundColor: 'rgba(99,102,241,0.8)',
      borderColor:     'rgb(99,102,241)',
      borderWidth:     2,
      borderRadius:    6,       // rounded bars
    }]
  },
  options: {
    responsive:          true,
    aspectRatio:         2,     // width/height; increase for wider charts
    animation:           { duration: 700, easing: 'easeOutQuart' },
    plugins: {
      legend:  { position: 'top' },
      tooltip: { mode: 'index', intersect: false },
    },
    scales: {           // omit entirely for pie / doughnut / radar
      x: { grid: { color: 'rgba(255,255,255,0.05)' } },
      y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
    },
  },
});
```

### Color palettes
```javascript
const VIVID = ['#6366f1','#8b5cf6','#ec4899','#f43f5e','#f97316','#eab308','#22c55e','#06b6d4'];
const SOFT  = ['rgba(99,102,241,0.8)','rgba(139,92,246,0.8)','rgba(236,72,153,0.8)','rgba(34,197,94,0.8)'];
const MONO  = ['#1e3a8a','#1d4ed8','#3b82f6','#60a5fa','#93c5fd','#bfdbfe'];
```

### Line chart with area fill
```javascript
{
  borderColor:     '#6366f1',
  backgroundColor: 'rgba(99,102,241,0.12)',
  fill:            true,
  tension:         0.4,         // 0 = straight; 0.4 = smooth curve
  pointRadius:     4,
  pointHoverRadius:7,
}
```

### Mixed chart (bar + line on dual axes)
```javascript
datasets: [
  { type: 'bar',  label: 'Volume', data: [...], yAxisID: 'y'  },
  { type: 'line', label: 'Price',  data: [...], yAxisID: 'y1', tension: 0.3 },
]
// scales: { y: { position: 'left' }, y1: { position: 'right', grid: { drawOnChartArea: false } } }
```

### Staggered entry animation
```javascript
// In options
animation: {
  delay: (context) => context.dataIndex * 60,
  duration: 600,
  easing: 'easeOutQuart',
}
```

### Doughnut with center text (no plugin)
```javascript
plugins: [{
  id: 'centerText',
  afterDraw(chart) {
    const { ctx, chartArea: { width, height } } = chart;
    ctx.save();
    ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = 'bold 28px Inter'; ctx.fillStyle = '#f1f5f9';
    ctx.fillText('72%', width / 2, height / 2);
    ctx.restore();
  }
}]
```

---

## Step 6 — Plotly.js Patterns

### Minimal setup
```javascript
Plotly.newPlot(
  'plotly-chart',
  [trace],   // array of trace objects
  layout,
  { responsive: true, displayModeBar: false, displaylogo: false }
);
```

### Dark theme layout (reuse across charts)
```javascript
const LAYOUT = {
  paper_bgcolor: 'rgba(0,0,0,0)',
  plot_bgcolor:  'rgba(0,0,0,0)',
  font:          { family: 'Segoe UI, sans-serif', color: '#94a3b8', size: 13 },
  margin:        { l: 55, r: 20, t: 40, b: 50 },
  xaxis:         { gridcolor: 'rgba(255,255,255,0.06)', zeroline: false },
  yaxis:         { gridcolor: 'rgba(255,255,255,0.06)', zeroline: false },
  legend:        { orientation: 'h', y: 1.08, x: 0.5, xanchor: 'center', font: { color: '#e2e8f0' } },
  hovermode:     'x unified',
};
```

### Trace types reference
```javascript
// Scatter / Line
{ type: 'scatter', mode: 'lines',           x, y }  // line
{ type: 'scatter', mode: 'markers',         x, y }  // scatter
{ type: 'scatter', mode: 'lines+markers',   x, y }  // both
{ type: 'scatter', fill: 'tozeroy', fillcolor: 'rgba(99,102,241,0.12)', x, y }  // area

// Bar
{ type: 'bar', x, y }
{ type: 'bar', orientation: 'h', x: values, y: labels }  // horizontal

// Pie / Donut
{ type: 'pie', labels, values, hole: 0.4 }   // hole: 0 = pie, 0.4+ = donut

// Statistical
{ type: 'histogram', x, nbinsx: 30 }
{ type: 'box',       y,  boxmean: 'sd', jitter: 0.3 }
{ type: 'violin',    y,  box: { visible: true }, meanline: { visible: true } }

// Heatmap (matrix)
{ type: 'heatmap',  z: matrix2d, colorscale: 'Viridis' }

// Financial
{ type: 'candlestick', x: dates, open, high, low, close }
{ type: 'ohlc',        x: dates, open, high, low, close }

// 3D (full bundle required)
{ type: 'surface',    z: matrix2d, colorscale: 'Plasma' }
{ type: 'scatter3d',  mode: 'markers', x, y, z }

// Aggregation charts
{ type: 'funnel',   y: stages, x: values }
{ type: 'waterfall',x: categories, y: deltas, measure: ['relative','relative','total'] }
{ type: 'treemap',  labels, parents, values }
{ type: 'sankey',   node: { label }, link: { source, target, value } }
```

### Built-in colorscales
`'Viridis'` `'Plasma'` `'Inferno'` `'Magma'` `'Cividis'` `'Blues'` `'Reds'` `'RdBu'` `'Spectral'` `'Portland'` `'Jet'`

### Subplots
```javascript
layout.grid = { rows: 2, columns: 2, pattern: 'independent' };
trace1.xaxis = 'x';  trace1.yaxis = 'y';   // cell (1,1)
trace2.xaxis = 'x2'; trace2.yaxis = 'y2';  // cell (1,2)
```

### Annotations and reference lines
```javascript
layout.annotations = [{
  x: 'Feb', y: 190, text: 'Peak',
  showarrow: true, arrowhead: 2,
  font: { color: '#f1f5f9' }, arrowcolor: '#6366f1',
}];
layout.shapes = [{
  type: 'line', x0: 'Jan', x1: 'Mar', y0: 160, y1: 160,
  line: { color: '#f43f5e', dash: 'dash', width: 1.5 },
}];
```

### Live updates
```javascript
Plotly.update('plotly-chart', { 'marker.color': [newColors] }, {}, [0]); // trace 0
Plotly.relayout('plotly-chart', { 'title.text': 'New Title' });
Plotly.addTraces('plotly-chart', newTrace);
Plotly.deleteTraces('plotly-chart', [1]);
Plotly.animate('plotly-chart',
  { data: [{ y: newY }] },
  { transition: { duration: 500, easing: 'cubic-in-out' }, frame: { duration: 500 } }
);
```

---

## Step 7 — Design & Polish Checklist

- [ ] `responsive: true` (both libraries) — chart resizes with its container
- [ ] No hardcoded pixel widths on the chart element
- [ ] Rounded bar corners: `borderRadius: 6` (Chart.js) / `marker.line` styling (Plotly)
- [ ] Smooth curves: `tension: 0.4` (Chart.js) / `line.shape: 'spline'` (Plotly)
- [ ] Meaningful tooltip: `mode: 'index'` (Chart.js) / `hovermode: 'x unified'` (Plotly)
- [ ] Legend placed clearly: top for ≤4 series, right for more
- [ ] No chart junk: hide unnecessary grid lines, tick marks, axis spines
- [ ] `aria-label` on `<canvas>` or wrapping `<div>` for accessibility
- [ ] Color contrast ≥ 3:1 against background

---

## Step 8 — Complete Examples

### Chart.js — Multi-Series Bar Chart

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Revenue by Quarter</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 820px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p { font-size: 0.85rem; color: #64748b; margin-bottom: 24px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Revenue by Quarter</h1>
    <p>Fiscal year 2024 — All regions combined</p>
    <canvas id="chart"></canvas>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
  <script>
    Chart.defaults.color       = '#94a3b8';
    Chart.defaults.borderColor = 'rgba(255,255,255,0.07)';
    Chart.defaults.font.family = 'Segoe UI, sans-serif';

    new Chart(document.getElementById('chart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: ['Q1', 'Q2', 'Q3', 'Q4'],
        datasets: [
          { label: 'North', data: [420, 580, 510, 690], backgroundColor: 'rgba(99,102,241,0.85)',  borderRadius: 6 },
          { label: 'South', data: [310, 420, 390, 510], backgroundColor: 'rgba(139,92,246,0.85)', borderRadius: 6 },
        ]
      },
      options: {
        responsive:  true,
        aspectRatio: 2,
        animation:   { duration: 800, easing: 'easeOutQuart' },
        plugins:     { legend: { position: 'top' }, tooltip: { mode: 'index' } },
        scales: {
          x: { grid: { display: false } },
          y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' } },
        },
      },
    });
  </script>
</body>
</html>
```

### Plotly.js — Area Line Chart with Unified Hover

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Performance Trends</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f1117; color: #e2e8f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; padding: 24px; }
    .card { background: #1a1d27; border-radius: 16px; padding: 32px; width: 100%; max-width: 900px; box-shadow: 0 8px 40px rgba(0,0,0,0.5); }
    h1 { font-size: 1.2rem; font-weight: 600; color: #f1f5f9; margin-bottom: 4px; }
    p { font-size: 0.85rem; color: #64748b; margin-bottom: 20px; }
    #chart { width: 100%; height: 450px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Performance Trends</h1>
    <p>Monthly KPIs — hover to explore</p>
    <div id="chart"></div>
  </div>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.2/plotly-basic.min.js"></script>
  <script>
    const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    const mkTrace = (name, data, color) => ({
      x: months, y: data, name,
      type: 'scatter', mode: 'lines+markers',
      line:      { color, width: 2.5, shape: 'spline' },
      marker:    { color, size: 6 },
      fill:      'tozeroy',
      fillcolor: color.replace(')', ', 0.08)').replace('rgb', 'rgba'),
    });

    Plotly.newPlot('chart', [
      mkTrace('Revenue',  [42,55,48,70,65,80,75,90,88,95,102,115], 'rgb(99,102,241)'),
      mkTrace('Expenses', [30,35,32,40,38,45,42,50,48,52,55,60],   'rgb(236,72,153)'),
    ], {
      paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)',
      font:    { family: 'Segoe UI, sans-serif', color: '#94a3b8', size: 13 },
      margin:  { l: 55, r: 20, t: 20, b: 45 },
      legend:  { orientation: 'h', y: 1.08, x: 0.5, xanchor: 'center', font: { color: '#e2e8f0' } },
      xaxis:   { gridcolor: 'rgba(255,255,255,0.06)', zeroline: false },
      yaxis:   { gridcolor: 'rgba(255,255,255,0.06)', zeroline: false, tickprefix: '$' },
      hovermode: 'x unified',
    }, { responsive: true, displayModeBar: false });
  </script>
</body>
</html>
```

---

## Common Mistakes to Avoid

- **Chart.js** — `maintainAspectRatio: false` with a CSS-fixed height but no `aspectRatio` option: use `aspectRatio` in options instead, or pair `maintainAspectRatio: false` with an explicit CSS height on the canvas wrapper
- **Chart.js** — manual `Chart.register()` not needed with the UMD build; all components auto-register
- **Plotly** — `paper_bgcolor: 'transparent'` without explicit `font.color` → text inherits and disappears
- **Plotly** — loading the 3.5 MB full bundle when `plotly-basic.min.js` is sufficient
- **Both** — running chart code before the CDN `<script>` tag has loaded; always place chart code in a `<script>` after the CDN tag, at the end of `<body>`
- **Both** — hardcoding pixel widths on the chart element; always use `responsive: true` and percentage-based container widths
