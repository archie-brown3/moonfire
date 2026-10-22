"""Build results/replay.html: a deterministic, interactive replay of loop_log.md.

Every row of the log becomes one frame. Kept ideas step the best-so-far line up and swap in the
policy.py that the loop committed for that score (from `git log --grep=loop:`), so the rule can be
watched evolving next to the chart. Pure function of the log and the git history; no randomness.

    uv run python plot_replay.py            # writes results/replay.html and dashboard/data/replay.json
"""

import difflib
import json
import re
import subprocess

LOG = "loop_log.md"
OUT = "results/replay.html"
DASH_OUT = "dashboard/data/replay.json"
ORACLE_PER_DAY = 64.95  # perfect-foresight LP on the train split, £/MW/day (evaluate.py: oracle / days)
TOP_JUMPS = 5
# Plain-English headline per big jump, written from that iteration's policy.py diff.
JUMP_NOTES = {
    3: "Compare each price with the last week, not the last two days",
    8: "Buy only in the usually cheaper half of the day, sell only in the dearer half",
    12: "Work out the usual day from the last 3 days instead of 7",
    34: "Average the last two half-hours, so one spike can't trigger a trade",
    17: "Always charge when the price goes negative",
}


def biggest_jumps(rows: list[dict]) -> list[dict]:
    best, jumps = rows[0]["score"], []
    for r in rows[1:]:
        if r["kept"] and r["score"] > best:
            jumps.append({"iter": r["iter"], "idea": r["idea"], "before": best, "after": r["score"],
                          "gain": round(r["score"] - best, 2),
                          "headline": JUMP_NOTES.get(r["iter"], r["idea"])})
            best = r["score"]
    return sorted(jumps, key=lambda j: -j["gain"])[:TOP_JUMPS]


def evolve_block(src: str) -> list[str]:
    lines = src.splitlines()
    a = next(i for i, l in enumerate(lines) if "EVOLVE-BLOCK-START" in l)
    b = next(i for i, l in enumerate(lines) if "EVOLVE-BLOCK-END" in l)
    return lines[a + 1:b]


def loop_commits() -> list[tuple[float, str]]:
    out = subprocess.run(["git", "log", "--reverse", "--format=%h %s", "--grep=loop:"],
                         capture_output=True, text=True, check=True).stdout
    commits = []
    for line in out.splitlines():
        m = re.search(r"score=([\d.]+)", line)
        if m:
            commits.append((float(m.group(1)), line.split()[0]))
    return commits


def parse_log() -> list[dict]:
    rows = []
    for line in open(LOG):
        m = re.match(r"\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*([\d.]+)\s*\|\s*(.*?)\s*\|", line)
        if m:
            rows.append({"iter": int(m[1]), "idea": m[2], "score": float(m[3]),
                         "kept": m[4].startswith("yes") or m[4] == "baseline"})
    return rows


def main() -> None:
    rows = parse_log()
    commits = loop_commits()
    seed = evolve_block(open("seed_policy.py").read())
    programs = [seed]          # programs[k] = code after the k-th kept idea
    code_at = [0]              # per row, index into programs
    ci = 0
    for r in rows[1:]:
        if r["kept"]:
            while ci < len(commits) and abs(commits[ci][0] - r["score"]) > 0.005:
                ci += 1
            if ci < len(commits):
                src = subprocess.run(["git", "show", f"{commits[ci][1]}:policy.py"],
                                     capture_output=True, text=True, check=True).stdout
                programs.append(evolve_block(src))
                ci += 1
            else:
                programs.append(programs[-1])
        code_at.append(len(programs) - 1)

    # Per program: lines with a flag for "new in this version" (vs the previous program).
    versions = []
    for k, prog in enumerate(programs):
        prev = programs[k - 1] if k else []
        flags = []
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, prev, prog).get_opcodes():
            flags.extend([tag != "equal"] * (j2 - j1))
        versions.append([[l, f] for l, f in zip(prog, flags)])

    data = {"rows": rows, "code_at": code_at, "versions": versions, "oracle": ORACLE_PER_DAY}
    html = TEMPLATE.replace("__DATA__", json.dumps(data))
    open(OUT, "w").write(html)
    best = max(r["score"] for r in rows if r["kept"])
    dash = {**data, "seed": rows[0]["score"], "best": best, "total_gain": round(best - rows[0]["score"], 2),
            "jumps": biggest_jumps(rows)}
    with open(DASH_OUT, "w") as f:
        json.dump(dash, f, indent=1)
    kept = sum(r["kept"] for r in rows) - 1
    print(f"{OUT}, {DASH_OUT}: {len(rows) - 1} ideas, {kept} kept, {len(programs)} program versions")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Battery rule replay</title>
<style>
:root {
  --bg: #fafafa; --ink: #18181b; --ink-2: #52525b; --ink-3: #a1a1aa; --line: #e4e4e7;
  --accent: #0f766e; --accent-soft: #ccfbf1; --reject: #71717a; --code-bg: #f4f4f5;
  --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  --sans: -apple-system, "Helvetica Neue", Helvetica, Arial, sans-serif;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #111113; --ink: #f4f4f5; --ink-2: #a1a1aa; --ink-3: #71717a; --line: #27272a;
    --accent: #14b8a6; --accent-soft: #134e4a; --reject: #71717a; --code-bg: #18181b;
  }
}
:root[data-theme="dark"] {
  --bg: #111113; --ink: #f4f4f5; --ink-2: #a1a1aa; --ink-3: #71717a; --line: #27272a;
  --accent: #14b8a6; --accent-soft: #134e4a; --reject: #71717a; --code-bg: #18181b;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 15px/1.5 var(--sans); }
main { max-width: 1120px; margin: 0 auto; padding: 32px 16px 48px; }
h1 { font-size: 24px; font-weight: 600; margin: 0 0 4px; letter-spacing: -0.01em; }
.lede { color: var(--ink-2); margin: 0 0 24px; max-width: 64ch; }
.stats { display: grid; grid-template-columns: repeat(3, auto); gap: 32px; justify-content: start; margin-bottom: 20px; }
.stats div span { display: block; }
.stats .n { font: 600 28px/1.1 var(--mono); font-variant-numeric: tabular-nums; }
.stats .l { color: var(--ink-2); font-size: 13px; }
.grid { display: grid; grid-template-columns: 3fr 2fr; gap: 24px; align-items: start; }
@media (max-width: 800px) { .grid { grid-template-columns: 1fr; } .stats { gap: 20px; } }
svg { width: 100%; height: auto; display: block; }
.axis text { fill: var(--ink-3); font: 11px var(--mono); }
.axis line, .grid-line { stroke: var(--line); stroke-width: 1; }
.oracle { stroke: var(--ink-3); stroke-width: 1; stroke-dasharray: 4 4; }
.oracle-label { fill: var(--ink-2); font: 11px var(--sans); }
.best { fill: none; stroke: var(--accent); stroke-width: 2; stroke-linejoin: round; }
.dot { stroke: var(--bg); stroke-width: 2; }
.dot.rej { fill: var(--bg); stroke: var(--reject); stroke-width: 1.5; }
.dot.keep { fill: var(--accent); }
.dot.now { r: 6; }
.caption { min-height: 48px; margin: 12px 0 8px; display: flex; gap: 12px; align-items: baseline; }
.caption .it { font: 600 13px var(--mono); color: var(--ink-3); }
.caption .idea { font-size: 16px; }
.caption .verdict { font: 600 12px var(--mono); padding: 2px 8px; border-radius: 4px; }
.verdict.keep { background: var(--accent-soft); color: var(--accent); }
.verdict.rej { color: var(--ink-2); border: 1px solid var(--line); }
.controls { display: flex; gap: 12px; align-items: center; margin-top: 8px; flex-wrap: wrap; }
button, select { font: 14px var(--sans); color: var(--ink); background: var(--bg); border: 1px solid var(--ink); border-radius: 4px; padding: 6px 14px; cursor: pointer; }
button:active { transform: translateY(1px); }
input[type=range] { flex: 1; min-width: 160px; accent-color: var(--accent); }
.hint { color: var(--ink-3); font-size: 12px; }
pre { margin: 0; background: var(--code-bg); border-radius: 4px; padding: 12px 0; font: 12px/1.5 var(--mono); overflow-x: auto; }
pre div { padding: 0 12px; white-space: pre; }
pre div.new { background: var(--accent-soft); }
.code-title { font-size: 13px; color: var(--ink-2); margin: 0 0 8px; display: flex; justify-content: space-between; }
.tip { position: fixed; pointer-events: none; background: var(--ink); color: var(--bg); font: 12px var(--sans); padding: 6px 8px; border-radius: 4px; display: none; max-width: 280px; }
@media (prefers-reduced-motion: no-preference) { .best, .dot { transition: all 120ms linear; } }
</style>
</head>
<body>
<main>
  <h1>How the battery rule was found</h1>
  <p class="lede">Each dot is one idea the search agent tried on the training months. The line only moves when an idea beat the best so far. The code on the right is the rule at that point.</p>
  <div class="stats">
    <div><span class="n" id="s-tried">0</span><span class="l">ideas tried</span></div>
    <div><span class="n" id="s-kept">0</span><span class="l">kept</span></div>
    <div><span class="n" id="s-score">0.00</span><span class="l">£ per MW per day, train</span></div>
  </div>
  <div class="grid">
    <section>
      <svg id="chart" viewBox="0 0 660 340" role="img" aria-label="Best training score by iteration"></svg>
      <div class="caption"><span class="it" id="c-iter"></span><span class="idea" id="c-idea"></span><span class="verdict" id="c-verdict"></span></div>
      <div class="controls">
        <button id="play">Play</button>
        <input type="range" id="scrub" min="0" value="0" aria-label="Iteration">
        <select id="speed" aria-label="Speed"><option value="250">1x</option><option value="120" selected>2x</option><option value="50">5x</option></select>
        <span class="hint">space plays, arrows step</span>
      </div>
    </section>
    <section>
      <p class="code-title"><span>policy.py, the part the loop may edit</span><span id="c-ver"></span></p>
      <pre id="code"></pre>
    </section>
  </div>
</main>
<div class="tip" id="tip"></div>
<script>
const D = __DATA__;
const rows = D.rows, N = rows.length - 1;
const W = 660, H = 340, L = 44, R = 16, T = 16, B = 32;
const ymax = Math.ceil(D.oracle / 10) * 10;
const x = i => L + (W - L - R) * i / N;
const y = v => T + (H - T - B) * (1 - v / ymax);
const svg = document.getElementById('chart');
const ns = 'http://www.w3.org/2000/svg';
const el = (t, a) => { const e = document.createElementNS(ns, t); for (const k in a) e.setAttribute(k, a[k]); return e; };

// axes
const ax = el('g', {class: 'axis'});
for (let v = 0; v <= ymax; v += 10) {
  ax.appendChild(el('line', {x1: L, x2: W - R, y1: y(v), y2: y(v), class: 'grid-line'}));
  const t = el('text', {x: L - 6, y: y(v) + 4, 'text-anchor': 'end'}); t.textContent = v; ax.appendChild(t);
}
for (let i = 0; i <= N; i += 50) {
  const t = el('text', {x: x(i), y: H - 10, 'text-anchor': 'middle'}); t.textContent = i; ax.appendChild(t);
}
const xl = el('text', {x: W - R, y: H - 10, 'text-anchor': 'end'}); xl.textContent = 'iteration'; ax.appendChild(xl);
svg.appendChild(ax);
svg.appendChild(el('line', {x1: L, x2: W - R, y1: y(D.oracle), y2: y(D.oracle), class: 'oracle'}));
const ol = el('text', {x: L + 4, y: y(D.oracle) - 5, class: 'oracle-label'}); ol.textContent = 'perfect foresight ' + D.oracle.toFixed(2); svg.appendChild(ol);
const dots = el('g', {}); svg.appendChild(dots);
const best = el('path', {class: 'best'}); svg.appendChild(best);

const tip = document.getElementById('tip');
const dotEls = rows.map((r, i) => {
  const c = el('circle', {cx: x(i), cy: y(r.score), r: 3.5, class: 'dot ' + (r.kept ? 'keep' : 'rej')});
  c.style.display = 'none';
  c.addEventListener('mousemove', e => { tip.style.display = 'block'; tip.style.left = (e.clientX + 12) + 'px'; tip.style.top = (e.clientY + 12) + 'px';
    tip.textContent = `#${r.iter} ${r.idea}: ${r.score.toFixed(2)} ${r.kept ? '(kept)' : '(rejected)'}`; });
  c.addEventListener('mouseleave', () => tip.style.display = 'none');
  c.addEventListener('click', () => { stop(); show(i); });
  dots.appendChild(c); return c;
});

const code = document.getElementById('code');
let shownVer = -1;
function renderCode(v) {
  if (v === shownVer) return; shownVer = v;
  code.innerHTML = '';
  for (const [line, isNew] of D.versions[v]) { const d = document.createElement('div'); if (isNew && v > 0) d.className = 'new'; d.textContent = line || ' '; code.appendChild(d); }
  document.getElementById('c-ver').textContent = v === 0 ? 'seed' : `version ${v} of ${D.versions.length - 1}`;
}

let cur = 0;
function show(i) {
  cur = i;
  let b = 0, path = '', kept = 0;
  for (let k = 0; k <= i; k++) {
    if (rows[k].score > b || k === 0) b = rows[k].score;
    if (rows[k].kept && k > 0) kept++;
    path += (k ? ' H' + x(k) + ' V' + y(b) : 'M' + x(0) + ' ' + y(b));
    dotEls[k].style.display = '';
    dotEls[k].classList.toggle('now', k === i);
  }
  for (let k = i + 1; k <= N; k++) dotEls[k].style.display = 'none';
  best.setAttribute('d', path);
  const r = rows[i];
  document.getElementById('s-tried').textContent = i;
  document.getElementById('s-kept').textContent = kept;
  document.getElementById('s-score').textContent = b.toFixed(2);
  document.getElementById('c-iter').textContent = i === 0 ? 'seed' : '#' + r.iter;
  document.getElementById('c-idea').textContent = r.idea;
  const v = document.getElementById('c-verdict');
  v.textContent = i === 0 ? 'baseline' : (r.kept ? 'kept' : 'rejected');
  v.className = 'verdict ' + (r.kept ? 'keep' : 'rej');
  scrub.value = i;
  renderCode(D.code_at[i]);
}

const scrub = document.getElementById('scrub'); scrub.max = N;
const playBtn = document.getElementById('play');
const speed = document.getElementById('speed');
let timer = null;
function tick() { if (cur >= N) return stop(); show(cur + 1); }
function play() { if (cur >= N) show(0); playBtn.textContent = 'Pause'; timer = setInterval(tick, +speed.value); }
function stop() { clearInterval(timer); timer = null; playBtn.textContent = cur >= N ? 'Replay' : 'Play'; }
playBtn.onclick = () => timer ? stop() : play();
speed.onchange = () => { if (timer) { clearInterval(timer); timer = setInterval(tick, +speed.value); } };
scrub.oninput = () => { stop(); show(+scrub.value); };
document.addEventListener('keydown', e => {
  if (e.code === 'Space') { e.preventDefault(); timer ? stop() : play(); }
  if (e.code === 'ArrowRight') { stop(); show(Math.min(N, cur + 1)); }
  if (e.code === 'ArrowLeft') { stop(); show(Math.max(0, cur - 1)); }
});
show(0);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
