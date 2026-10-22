import type { Metadata } from "next";
import replay from "@/data/replay.json";
import { SERIES } from "@/lib/series";

export const metadata: Metadata = { title: "Biggest jumps" };

type Jump = {
  iter: number;
  idea: string;
  before: number;
  after: number;
  gain: number;
  headline: string;
};

const money = (v: number) => `£${v.toFixed(2)}`;

export default function JumpsPage() {
  const jumps = replay.jumps as Jump[];
  const rows = replay.rows;
  const tried = rows.length - 1;
  const top = jumps.reduce((s, j) => s + j.gain, 0);
  const max = jumps[0].gain;

  // Kept ideas that raised the best score, the same rule the replay's blue line follows.
  let best = rows[0].score;
  let steps = 0;
  for (const r of rows.slice(1)) {
    if (r.kept && r.score > best) {
      best = r.score;
      steps++;
    }
  }

  return (
    <main className={`mx-auto w-full max-w-7xl space-y-8 px-6 py-10 ${SERIES}`}>
      <div className="max-w-3xl space-y-2">
        <h1 className="text-2xl tracking-tight">
          Five ideas made most of the gain
        </h1>
        <p className="text-sm text-muted-foreground">
          The search tried {tried} ideas. {steps} of them raised the best score,
          from {money(replay.seed)} to {money(replay.best)} per MW per day.
          These five added {money(top)} of the {money(replay.total_gain)}.
        </p>
      </div>

      <ol className="max-w-5xl divide-y divide-border">
        {jumps.map((j) => (
          <li
            key={j.iter}
            className="grid grid-cols-[7rem_1fr] items-baseline gap-x-6 gap-y-3 py-6 md:grid-cols-[8rem_1fr_14rem]"
          >
            <div className="text-3xl tabular-nums">+{money(j.gain)}</div>
            <div className="space-y-1">
              <p className="text-lg leading-snug text-balance">{j.headline}</p>
              <p className="text-xs tabular-nums text-muted-foreground">
                Idea {j.iter}, {money(j.before)} to {money(j.after)}
              </p>
            </div>
            <div className="col-span-2 self-center md:col-span-1">
              <div
                className="h-2"
                style={{
                  width: `${(100 * j.gain) / max}%`,
                  background: "var(--best)",
                }}
              />
            </div>
          </li>
        ))}
      </ol>

      <p className="text-sm text-muted-foreground">
        The other {steps - jumps.length} steps added{" "}
        {money(replay.total_gain - top)} between them.
      </p>
    </main>
  );
}
