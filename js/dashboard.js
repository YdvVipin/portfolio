/* ═══════════════════════════════════════════════════
   Quality Dashboard — renders data/qa-metrics.json
   (written by scripts/qa-metrics.mjs in CI)
   ═══════════════════════════════════════════════════ */

(function () {
  const DATA_URL = (document.body.dataset.basePath || '') + 'data/qa-metrics.json';
  const MAX_RUNS = 30;
  const LH = [
    { key: 'performance', label: 'Performance', cls: 's1' },
    { key: 'accessibility', label: 'Accessibility', cls: 's2' },
    { key: 'best-practices', label: 'Best Practices', cls: 's3' },
    { key: 'seo', label: 'SEO', cls: 's4' },
  ];
  const SVG_NS = 'http://www.w3.org/2000/svg';
  const root = document.getElementById('qa-dash');
  if (!root) return;

  // ─── Helpers ─────────────────────────────────────
  const esc = s => String(s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const fmtDate = iso => new Date(iso).toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
  const fmtDateTime = iso => new Date(iso).toLocaleString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  const fmtDuration = ms => ms >= 60000 ? `${Math.floor(ms / 60000)}m ${Math.round((ms % 60000) / 1000)}s` : `${Math.round(ms / 1000)}s`;
  const passRate = t => (t.passed + t.failed) ? Math.round((t.passed / (t.passed + t.failed)) * 1000) / 10 : 0;

  function el(tag, attrs = {}, parent) {
    const node = document.createElementNS(SVG_NS, tag);
    for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
    if (parent) parent.appendChild(node);
    return node;
  }

  function showXLabel(i, n, every) {
    return i === n - 1 || (i % every === 0 && n - 1 - i >= every);
  }

  function niceMax(v) {
    if (v <= 10) return 10;
    const step = Math.pow(10, Math.floor(Math.log10(v)));
    return Math.ceil(v / step) * step;
  }

  // ─── Tooltip (one per chart) ─────────────────────
  function makeTooltip(frame) {
    const tip = document.createElement('div');
    tip.className = 'kc-viz__tip';
    tip.setAttribute('role', 'status');
    tip.hidden = true;
    frame.appendChild(tip);
    return {
      show(html, x, y) {
        tip.innerHTML = html;
        tip.hidden = false;
        const fw = frame.clientWidth, tw = tip.offsetWidth;
        tip.style.left = Math.max(4, Math.min(fw - tw - 4, x - tw / 2)) + 'px';
        tip.style.top = Math.max(4, y - tip.offsetHeight - 12) + 'px';
      },
      hide() { tip.hidden = true; },
    };
  }

  // ─── Chart: test results per run (stacked bars) ──
  function renderTestsChart(frame, runs) {
    frame.querySelectorAll('svg, .kc-viz__tip').forEach(n => n.remove());
    const W = frame.clientWidth || 600, H = 240;
    const m = { t: 12, r: 12, b: 28, l: 40 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const yMax = niceMax(Math.max(...runs.map(r => r.tests.passed + r.tests.failed)));
    const y = v => m.t + ih - (v / yMax) * ih;
    const band = iw / runs.length;
    const bw = Math.max(4, Math.min(28, band * 0.6));

    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img', 'aria-labelledby': 'tests-chart-title' });
    el('title', {}, svg).textContent = 'Passed and failed tests per CI run';

    for (let i = 0; i <= 4; i++) {
      const v = (yMax / 4) * i, yy = y(v);
      el('line', { x1: m.l, x2: W - m.r, y1: yy, y2: yy, class: i ? 'kc-viz__grid' : 'kc-viz__axis' }, svg);
      el('text', { x: m.l - 8, y: yy + 4, 'text-anchor': 'end', class: 'kc-viz__tick' }, svg).textContent = Math.round(v);
    }

    const labelEvery = Math.ceil(runs.length / Math.max(1, Math.floor(iw / 64)));
    const tip = makeTooltip(frame);

    runs.forEach((r, i) => {
      const cx = m.l + band * i + band / 2, x = cx - bw / 2;
      const { passed, failed } = r.tests;
      const g = el('g', {}, svg);
      // Stacked from the baseline: passed, 2px surface gap, then failed. Rounded top on the top-most segment only.
      const pTop = y(passed);
      if (passed) el('path', { d: barPath(x, pTop, bw, y(0) - pTop, !failed), class: 'kc-viz__bar kc-viz__bar--good' }, g);
      if (failed) {
        const fTop = y(passed + failed);
        el('path', { d: barPath(x, fTop, bw, Math.max(1, pTop - fTop - (passed ? 2 : 0)), true), class: 'kc-viz__bar kc-viz__bar--bad' }, g);
      }
      if (showXLabel(i, runs.length, labelEvery)) {
        el('text', { x: cx, y: H - 8, 'text-anchor': 'middle', class: 'kc-viz__tick' }, svg).textContent = fmtDate(r.date);
      }
      const hit = el('rect', { x: m.l + band * i, y: m.t, width: band, height: ih, class: 'kc-viz__hit', tabindex: 0, role: 'img',
        'aria-label': `${fmtDate(r.date)}: ${passed} passed, ${failed} failed` }, svg);
      const show = () => {
        g.classList.add('is-active');
        tip.show(`<strong>${esc(fmtDateTime(r.date))}</strong>${r.commit ? ` · <code>${esc(r.commit)}</code>` : ''}
          <div><span class="kc-viz__key kc-viz__key--good"></span>Passed <b>${passed}</b></div>
          <div><span class="kc-viz__key kc-viz__key--bad"></span>Failed <b>${failed}</b></div>
          <div class="kc-viz__muted">Flaky ${r.tests.flaky} · ${fmtDuration(r.tests.durationMs)}</div>`, cx, pTop);
      };
      const hide = () => { g.classList.remove('is-active'); tip.hide(); };
      hit.addEventListener('mouseenter', show); hit.addEventListener('focus', show);
      hit.addEventListener('mouseleave', hide); hit.addEventListener('blur', hide);
    });
    frame.prepend(svg);
  }

  function barPath(x, y, w, h, roundTop) {
    const r = roundTop ? Math.min(4, w / 2, h) : 0;
    return `M${x},${y + h}V${y + r}${r ? `Q${x},${y} ${x + r},${y}` : ''}H${x + w - r}${r ? `Q${x + w},${y} ${x + w},${y + r}` : ''}V${y + h}Z`;
  }

  // ─── Chart: Lighthouse scores over time (lines) ──
  function renderLighthouseChart(frame, runs) {
    frame.querySelectorAll('svg, .kc-viz__tip').forEach(n => n.remove());
    const W = frame.clientWidth || 600, H = 240;
    const m = { t: 14, r: 108, b: 28, l: 40 };
    const iw = W - m.l - m.r, ih = H - m.t - m.b;
    const all = runs.flatMap(r => LH.map(c => r.lighthouse[c.key]));
    const yMin = Math.max(0, Math.min(50, Math.floor((Math.min(...all) - 5) / 25) * 25));
    const y = v => m.t + ih - ((v - yMin) / (100 - yMin)) * ih;
    const x = i => runs.length === 1 ? m.l + iw / 2 : m.l + (iw / (runs.length - 1)) * i;

    const svg = el('svg', { viewBox: `0 0 ${W} ${H}`, width: W, height: H, role: 'img' });
    el('title', {}, svg).textContent = 'Lighthouse category scores per CI run';

    const step = 100 - yMin <= 50 ? 10 : 25;
    for (let v = yMin; v <= 100; v += step) {
      const yy = y(v), i = v - yMin;
      el('line', { x1: m.l, x2: m.l + iw, y1: yy, y2: yy, class: i ? 'kc-viz__grid' : 'kc-viz__axis' }, svg);
      el('text', { x: m.l - 8, y: yy + 4, 'text-anchor': 'end', class: 'kc-viz__tick' }, svg).textContent = Math.round(v);
    }
    const labelEvery = Math.ceil(runs.length / Math.max(1, Math.floor(iw / 64)));
    runs.forEach((r, i) => {
      if (showXLabel(i, runs.length, labelEvery)) {
        el('text', { x: x(i), y: H - 8, 'text-anchor': 'middle', class: 'kc-viz__tick' }, svg).textContent = fmtDate(r.date);
      }
    });

    LH.forEach(c => {
      const pts = runs.map((r, i) => [x(i), y(r.lighthouse[c.key])]);
      if (pts.length > 1) el('path', { d: 'M' + pts.map(p => p.join(',')).join('L'), class: `kc-viz__line kc-viz__line--${c.cls}` }, svg);
      const last = pts[pts.length - 1];
      el('circle', { cx: last[0], cy: last[1], r: 4, class: `kc-viz__dot kc-viz__dot--${c.cls}` }, svg);
    });

    // Direct labels at the line ends, nudged apart so they never collide.
    const lastRun = runs[runs.length - 1];
    const labels = LH.map(c => ({ c, v: lastRun.lighthouse[c.key], y: y(lastRun.lighthouse[c.key]) })).sort((a, b) => a.y - b.y);
    for (let i = 1; i < labels.length; i++) labels[i].y = Math.max(labels[i].y, labels[i - 1].y + 14);
    const lx = x(runs.length - 1) + 10;
    labels.forEach(l => {
      el('text', { x: lx, y: l.y + 4, class: 'kc-viz__label' }, svg).textContent = `${l.c.label} ${l.v}`;
    });

    // Crosshair + tooltip.
    const cross = el('line', { y1: m.t, y2: m.t + ih, class: 'kc-viz__cross', visibility: 'hidden' }, svg);
    const hit = el('rect', { x: m.l - 8, y: m.t, width: iw + 16, height: ih, class: 'kc-viz__hit', tabindex: 0, role: 'img',
      'aria-label': 'Lighthouse scores by run; use arrow keys to step through runs' }, svg);
    const tip = makeTooltip(frame);
    let active = runs.length - 1;
    const showAt = i => {
      active = i;
      const r = runs[i], cx = x(i);
      cross.setAttribute('x1', cx); cross.setAttribute('x2', cx); cross.setAttribute('visibility', 'visible');
      const rows = LH.map(c => `<div><span class="kc-viz__key kc-viz__key--${c.cls}"></span>${c.label} <b>${r.lighthouse[c.key]}</b></div>`).join('');
      tip.show(`<strong>${esc(fmtDateTime(r.date))}</strong>${r.commit ? ` · <code>${esc(r.commit)}</code>` : ''}${rows}`, cx, m.t + 8);
    };
    const hide = () => { cross.setAttribute('visibility', 'hidden'); tip.hide(); };
    hit.addEventListener('mousemove', e => {
      const box = svg.getBoundingClientRect();
      const px = ((e.clientX - box.left) / box.width) * W;
      const i = runs.length === 1 ? 0 : Math.round(((px - m.l) / iw) * (runs.length - 1));
      showAt(Math.max(0, Math.min(runs.length - 1, i)));
    });
    hit.addEventListener('mouseleave', hide);
    hit.addEventListener('focus', () => showAt(active));
    hit.addEventListener('blur', hide);
    hit.addEventListener('keydown', e => {
      if (e.key === 'ArrowLeft') showAt(Math.max(0, active - 1));
      else if (e.key === 'ArrowRight') showAt(Math.min(runs.length - 1, active + 1));
    });
    frame.prepend(svg);
  }

  // ─── Page sections ───────────────────────────────
  function kpiHTML(latest) {
    const t = latest.tests, lh = latest.lighthouse;
    const ok = t.failed === 0;
    const commit = latest.commit
      ? (latest.runUrl ? `<a href="${esc(latest.runUrl)}" target="_blank" rel="noopener"><code>${esc(latest.commit)}</code></a>` : `<code>${esc(latest.commit)}</code>`)
      : '';
    return `
      <div class="kc-stats kc-dash__kpis">
        <div class="kc-stat">
          <div class="kc-stat__value">${passRate(t)}%</div>
          <div class="kc-stat__label">Pass rate · latest run</div>
          <div class="kc-dash__status kc-dash__status--${ok ? 'good' : 'bad'}">${ok ? '✓ All green' : `✕ ${t.failed} failing`}</div>
        </div>
        <div class="kc-stat">
          <div class="kc-stat__value">${t.passed + t.failed}</div>
          <div class="kc-stat__label">Checks run (${t.passed} passed)</div>
        </div>
        <div class="kc-stat">
          <div class="kc-stat__value">${lh.accessibility}</div>
          <div class="kc-stat__label">Lighthouse accessibility</div>
        </div>
        <div class="kc-stat">
          <div class="kc-stat__value kc-dash__date">${esc(fmtDate(latest.date))}</div>
          <div class="kc-stat__label">Last run ${commit}</div>
        </div>
      </div>`;
  }

  function tableHTML(runs) {
    const rows = runs.slice().reverse().map(r => `
      <tr>
        <td>${esc(fmtDateTime(r.date))}</td>
        <td>${r.runUrl ? `<a href="${esc(r.runUrl)}" target="_blank" rel="noopener"><code>${esc(r.commit || '—')}</code></a>` : `<code>${esc(r.commit || '—')}</code>`}</td>
        <td>${r.tests.passed}</td><td>${r.tests.failed}</td><td>${r.tests.flaky}</td><td>${fmtDuration(r.tests.durationMs)}</td>
        ${LH.map(c => `<td>${r.lighthouse[c.key]}</td>`).join('')}
      </tr>`).join('');
    return `
      <details class="kc-dash__table">
        <summary>View all runs as a table</summary>
        <div class="kc-dash__scroll">
          <table>
            <thead><tr><th>Run</th><th>Commit</th><th>Passed</th><th>Failed</th><th>Flaky</th><th>Duration</th>${LH.map(c => `<th>${c.label}</th>`).join('')}</tr></thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </details>`;
  }

  function renderEmpty() {
    root.innerHTML = `<div class="kc-dash__empty">
      <h2 class="kc-dash__h2">No runs recorded yet</h2>
      <p>Results appear here after the first CI run on <code>main</code>.</p>
    </div>`;
  }

  async function init() {
    let runs;
    try {
      const res = await fetch(DATA_URL, { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      runs = ((await res.json()).runs || []).filter(r => r && r.tests && r.lighthouse).slice(-MAX_RUNS);
    } catch (err) {
      runs = [];
    }
    if (!runs.length) return renderEmpty();

    const latest = runs[runs.length - 1];
    root.innerHTML = `
      ${kpiHTML(latest)}
      <div class="kc-dash__grid">
        <figure class="kc-viz">
          <figcaption>
            <h2 class="kc-dash__h2">Test results per run</h2>
            <div class="kc-viz__legend">
              <span><span class="kc-viz__key kc-viz__key--good"></span>Passed</span>
              <span><span class="kc-viz__key kc-viz__key--bad"></span>Failed</span>
            </div>
          </figcaption>
          <div class="kc-viz__frame" id="tests-chart"></div>
        </figure>
        <figure class="kc-viz">
          <figcaption>
            <h2 class="kc-dash__h2">Lighthouse scores</h2>
            <div class="kc-viz__legend">
              ${LH.map(c => `<span><span class="kc-viz__key kc-viz__key--${c.cls}"></span>${c.label}</span>`).join('')}
            </div>
          </figcaption>
          <div class="kc-viz__frame" id="lh-chart"></div>
        </figure>
      </div>
      ${runs.length < 3 ? `<p class="kc-dash__note">History builds up with every push — ${runs.length} run${runs.length > 1 ? 's' : ''} recorded so far.</p>` : ''}
      ${tableHTML(runs)}`;

    const draw = () => {
      renderTestsChart(document.getElementById('tests-chart'), runs);
      renderLighthouseChart(document.getElementById('lh-chart'), runs);
    };
    draw();
    let raf;
    window.addEventListener('resize', () => { cancelAnimationFrame(raf); raf = requestAnimationFrame(draw); });
  }

  init();
})();
