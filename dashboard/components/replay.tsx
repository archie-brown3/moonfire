"use client";

import { useEffect, useState } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { SERIES } from "@/lib/series";

export type ReplayRow = {
  iter: number;
  idea: string;
  score: number;
  kept: boolean;
};
export type ReplayData = {
  rows: ReplayRow[];
  code_at: number[];
  versions: [string, boolean][][];
  oracle: number;
};

const W = 720;
const H = 300;
const L = 44;
const R = 12;
const T = 14;
const B = 28;
const SPEEDS = [
  { label: "1x", ms: 250 },
  { label: "2x", ms: 120 },
  { label: "5x", ms: 50 },
];

function Stat({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <div className="text-3xl tabular-nums">{value}</div>
      <div className="text-xs text-muted-foreground">{label}</div>
    </div>
  );
}

export function Replay({ data }: { data: ReplayData }) {
  const { rows, code_at, versions, oracle } = data;
  const n = rows.length - 1;
  const [cur, setCur] = useState(0);
  const [playing, setPlaying] = useState(false);
  const [ms, setMs] = useState(120);

  useEffect(() => {
    if (!playing) return;
    const id = setInterval(() => setCur((c) => Math.min(n, c + 1)), ms);
    return () => clearInterval(id);
  }, [playing, ms, n]);

  useEffect(() => {
    if (playing && cur >= n) setPlaying(false);
  }, [playing, cur, n]);

  const toggle = () => {
    if (!playing && cur >= n) setCur(0);
    setPlaying(!playing);
  };
  const step = (d: number) => {
    setPlaying(false);
    setCur((c) => Math.max(0, Math.min(n, c + d)));
  };

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.target as HTMLElement).closest("button, input, select, textarea"))
        return;
      if (e.code === "Space") {
        e.preventDefault();
        toggle();
      } else if (e.code === "ArrowRight") step(1);
      else if (e.code === "ArrowLeft") step(-1);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  });

  const ymax = Math.ceil(oracle / 10) * 10;
  const x = (i: number) => L + ((W - L - R) * i) / n;
  const y = (v: number) => T + (H - T - B) * (1 - v / ymax);

  let best = rows[0].score;
  let kept = 0;
  let path = `M${x(0)} ${y(best)}`;
  for (let k = 1; k <= cur; k++) {
    const r = rows[k];
    if (r.kept) kept++;
    if (r.kept && r.score > best) best = r.score;
    path += ` H${x(k)} V${y(best)}`;
  }

  const row = rows[cur];
  const version = code_at[cur];
  const verdict = cur === 0 ? "starting rule" : row.kept ? "kept" : "rejected";

  return (
    <div className={`space-y-6 ${SERIES}`}>
      <div className="flex flex-wrap gap-x-12 gap-y-4">
        <Stat label="Ideas tried" value={String(cur)} />
        <Stat label="Kept" value={String(kept)} />
        <Stat
          label="Best so far, £ per MW per day"
          value={`£${best.toFixed(2)}`}
        />
      </div>

      <div className="grid items-start gap-4 lg:grid-cols-5">
        <Card className="lg:col-span-3">
          <CardContent className="space-y-4">
            <svg
              viewBox={`0 0 ${W} ${H}`}
              className="h-auto w-full"
              role="img"
              aria-label="Training score of each idea, with the best kept score so far"
            >
              {[0, 20, 40, 60].map((v) => (
                <g key={v}>
                  <line
                    x1={L}
                    x2={W - R}
                    y1={y(v)}
                    y2={y(v)}
                    className="stroke-border"
                  />
                  <text
                    x={L - 8}
                    y={y(v) + 4}
                    textAnchor="end"
                    className="fill-muted-foreground text-[11px]"
                  >
                    £{v}
                  </text>
                </g>
              ))}
              {[0, 50, 100, 150, 200].map((i) => (
                <text
                  key={i}
                  x={x(i)}
                  y={H - 8}
                  textAnchor="middle"
                  className="fill-muted-foreground text-[11px]"
                >
                  {i}
                </text>
              ))}
              <text
                x={W - R}
                y={H - 8}
                textAnchor="end"
                className="fill-muted-foreground text-[11px]"
              >
                idea
              </text>
              <line
                x1={L}
                x2={W - R}
                y1={y(oracle)}
                y2={y(oracle)}
                stroke="var(--oracle)"
                strokeDasharray="4 4"
              />
              <text
                x={L + 4}
                y={y(oracle) - 6}
                className="fill-muted-foreground text-[11px]"
              >
                Perfect foresight £{oracle.toFixed(2)}
              </text>
              {rows.slice(0, cur + 1).map((r, k) => (
                <g key={r.iter}>
                  <title>{`Idea ${r.iter}: ${r.idea}. £${r.score.toFixed(2)}, ${r.kept ? "kept" : "rejected"}`}</title>
                  <circle cx={x(k)} cy={y(r.score)} r={7} fill="transparent" />
                  {r.kept ? (
                    <circle
                      cx={x(k)}
                      cy={y(r.score)}
                      r={4}
                      fill="var(--best)"
                      className="stroke-background"
                      strokeWidth={2}
                    />
                  ) : (
                    <circle
                      cx={x(k)}
                      cy={y(r.score)}
                      r={3}
                      fill="none"
                      stroke="var(--attempt)"
                      strokeWidth={1.5}
                    />
                  )}
                </g>
              ))}
              <path
                d={path}
                fill="none"
                stroke="var(--best)"
                strokeWidth={2}
                strokeLinejoin="round"
              />
              <circle
                cx={x(cur)}
                cy={y(row.score)}
                r={8}
                fill="none"
                className="stroke-foreground"
                strokeWidth={1.5}
              />
            </svg>

            <p className="min-h-10 text-sm">
              <span className="tabular-nums text-muted-foreground">
                {cur === 0 ? "Seed" : `#${row.iter}`}
              </span>{" "}
              {row.idea}{" "}
              <span
                className={row.kept ? "font-medium" : "text-muted-foreground"}
              >
                ({verdict})
              </span>
            </p>

            <div className="flex flex-wrap items-center gap-3">
              <button
                type="button"
                onClick={toggle}
                className="h-9 min-w-24 border border-foreground px-4 text-sm transition-colors hover:bg-foreground hover:text-background focus-visible:outline-2 focus-visible:outline-offset-2"
              >
                {playing ? "Pause" : cur >= n ? "Replay" : "Play"}
              </button>
              <input
                type="range"
                min={0}
                max={n}
                value={cur}
                onChange={(e) => {
                  setPlaying(false);
                  setCur(Number(e.target.value));
                }}
                aria-label="Idea number"
                className="min-w-40 flex-1"
                style={{ accentColor: "var(--best)" }}
              />
              <select
                value={ms}
                onChange={(e) => setMs(Number(e.target.value))}
                aria-label="Playback speed"
                className="h-9 border border-border bg-background px-2 text-sm"
              >
                {SPEEDS.map((s) => (
                  <option key={s.ms} value={s.ms}>
                    {s.label}
                  </option>
                ))}
              </select>
              <span className="text-xs text-muted-foreground">
                Space plays, arrows step
              </span>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle>The rule at this point</CardTitle>
            <CardDescription>
              {version === 0
                ? "The seed rule the search started from."
                : `Version ${version} of ${versions.length - 1}. Highlighted lines changed in this version.`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <pre className="overflow-x-auto text-xs leading-5">
              {versions[version].map(([line, changed], i) => (
                <div
                  // biome-ignore lint/suspicious/noArrayIndexKey: lines are positional
                  key={i}
                  className="px-2 whitespace-pre"
                  style={
                    changed && version > 0
                      ? {
                          background:
                            "color-mix(in oklab, var(--best) 14%, transparent)",
                        }
                      : undefined
                  }
                >
                  {line || " "}
                </div>
              ))}
            </pre>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
