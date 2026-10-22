import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import {
  CumulativeChart,
  LoopChart,
  PolicyBars,
  PriceChart,
  SimpleBars,
  SplitBars,
  WeekPriceChart,
  WeekSocChart,
} from "@/components/charts";
import data from "@/data/dashboard.json";
import {
  captureBenchmarks,
  competitors,
  fleet,
  judging,
  pitchArithmetic,
  pitfalls,
  revenueIndex,
  revenueMixSep26,
  workflowSteps,
} from "@/data/research";

type Eval = { score: number; ci95?: number[]; pct_of_oracle: number | null; cycles: number; days?: number; error: string | null };
type Results = Record<string, Record<"train" | "val" | "test", Eval>> | null;

const NAMES: Record<string, string> = {
  do_nothing: "Do nothing",
  fixed_schedule: "Fixed schedule",
  seed: "Seed policy",
  champion: "Champion",
  oracle: "Perfect foresight",
};

function Tile({ label, value, sub }: { label: string; value: string; sub?: string }) {
  return (
    <Card className="gap-1 py-4">
      <CardHeader className="pb-0">
        <CardDescription className="text-xs">{label}</CardDescription>
      </CardHeader>
      <CardContent>
        <div className="num text-4xl font-semibold">{value}</div>
        {sub ? <div className="text-xs text-muted-foreground mt-1">{sub}</div> : null}
      </CardContent>
    </Card>
  );
}

function Section({ title, kicker, children }: { title: string; kicker: string; children: React.ReactNode }) {
  return (
    <section className="space-y-4">
      <div>
        <div className="text-sm text-muted-foreground">{kicker}</div>
        <h2 className="text-2xl font-semibold tracking-tight">{title}</h2>
      </div>
      {children}
    </section>
  );
}

export default function Home() {
  const te = data.train_eval as Record<string, Eval>;
  const results = data.results as Results;
  const loop = data.loop;
  const kept = loop.filter((r) => r.kept && r.iter > 0);
  const champion = te.champion;
  const seed = te.seed;
  const last = loop[loop.length - 1];

  const policyRows = [
    ...["do_nothing", "fixed_schedule", "seed", "champion"].map((k) => ({ name: NAMES[k], score: te[k].score, pct: te[k].pct_of_oracle })),
    { name: NAMES.oracle, score: data.oracle_train_per_day, pct: 100 },
  ];

  const splitRows = results
    ? [
        ...["fixed_schedule", "seed", "champion"].map((k) => ({ name: NAMES[k], train: results[k].train.score, val: results[k].val.score, test: results[k].test.score })),
        { name: NAMES.oracle, train: data.splits.train.oracle_per_day, val: data.splits.val.oracle_per_day, test: data.splits.test.oracle_per_day },
      ]
    : null;

  const ideaCounts = kept.length;
  const gapToOracle = (data.oracle_train_per_day - champion.score).toFixed(1);

  return (
    <main className="mx-auto max-w-7xl px-6 py-12 space-y-14 [&_td]:whitespace-normal [&_th]:whitespace-normal [&_td]:align-top">
      <header className="hero-in space-y-6">
        <div className="flex items-baseline justify-between gap-6">
          <div className="text-sm font-medium">Moonfire</div>
          <div className="text-sm text-muted-foreground">{last.iter} experiments · {ideaCounts} kept</div>
        </div>
        <h1 className="hero-claim font-semibold">Battery dispatch that improves itself.</h1>
        <p className="max-w-[52ch] text-base text-muted-foreground">
          An agent rewrites one trading rule. A sealed simulator scores it on a year of real GB prices. Only rules that win on
          unseen months are promoted.
        </p>
        <div className="flex flex-wrap items-end gap-x-10 gap-y-4 pt-2">
          <div>
            <div className="text-sm text-muted-foreground">Seed rule, train</div>
            <div className="num text-5xl font-semibold text-muted-foreground">£{seed.score}</div>
          </div>
          <div className="pb-3 text-3xl text-muted-foreground">→</div>
          <div>
            <div className="text-sm text-muted-foreground">After the loop, train £/MW/day</div>
            <div className="num text-6xl font-semibold text-primary">£{champion.score}</div>
          </div>
          <div>
            <div className="text-sm text-muted-foreground">Held-out test</div>
            <div className="num text-5xl font-semibold">{results ? `£${results.champion.test.score}` : "pending"}</div>
            <div className="text-sm text-muted-foreground">{results ? `${results.champion.test.pct_of_oracle}% of perfect foresight` : "gate not yet run"}</div>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <Tile label="Of perfect foresight, train" value={`${champion.pct_of_oracle}%`} sub={`seed ${seed.pct_of_oracle}%`} />
        <Tile label="Uplift vs seed" value={`+${(100 * (champion.score / seed.score - 1)).toFixed(0)}%`} sub={`+£${(champion.score - seed.score).toFixed(1)} per MW-day`} />
        <Tile label="Battery cycles over train" value={`${champion.cycles}`} sub={`seed ${seed.cycles}; wear is charged inside the simulator`} />
        <Tile label="Confidence interval, train" value={`£${champion.ci95?.[0]} to £${champion.ci95?.[1]}`} sub="95% bootstrap over days" />
      </div>

      <dl className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-x-8 gap-y-3 border-y border-border py-4 text-sm">
        <div><dt className="text-muted-foreground">Data</dt><dd>Elexon BMRS, APX market index, half-hourly</dd></div>
        <div><dt className="text-muted-foreground">Window</dt><dd className="num">{data.splits.train.range[0]} to {data.splits.test.range[1]}</dd></div>
        <div><dt className="text-muted-foreground">Splits, by time</dt><dd className="num">train {data.splits.train.days} d · val {data.splits.val.days} d · test {data.splits.test.days} d</dd></div>
        <div><dt className="text-muted-foreground">Asset</dt><dd className="num">{data.spec.power_mw} MW / {data.spec.capacity_mwh} MWh, {Math.round(data.spec.efficiency * 100)}% round trip, £{data.spec.degradation_gbp_per_mwh}/MWh wear</dd></div>
        <div><dt className="text-muted-foreground">Policy sees</dt><dd>past prices only; no forecast, no current price</dd></div>
        <div><dt className="text-muted-foreground">Generated</dt><dd className="num">{data.generated_at.replace("T", " ")} from loop_log.md, evaluate.py, gate.py</dd></div>
      </dl>

      <Section kicker="Research loop" title="Train score by iteration">
        <div className="grid lg:grid-cols-3 gap-4">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Attempts and best kept</CardTitle>
              <CardDescription>Gap to perfect foresight: £{gapToOracle}/MW/day</CardDescription>
            </CardHeader>
            <CardContent>
              <LoopChart data={loop} oracle={data.oracle_train_per_day} seed={seed.score} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Ideas the loop kept</CardTitle>
              <CardDescription>Largest gains first</CardDescription>
            </CardHeader>
            <CardContent className="max-h-80 overflow-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>#</TableHead>
                    <TableHead>Idea</TableHead>
                    <TableHead className="text-right">Gain</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {[...kept]
                    .sort((a, b) => (b.gain ?? 0) - (a.gain ?? 0))
                    .map((r) => (
                      <TableRow key={r.iter}>
                        <TableCell className="text-muted-foreground">{r.iter}</TableCell>
                        <TableCell>{r.idea}</TableCell>
                        <TableCell className="text-right tabular-nums">+{r.gain?.toFixed(2)}</TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </Section>

      <Section kicker="Evaluation" title="Policies vs perfect foresight">
        <div className="grid lg:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Train split, £/MW/day</CardTitle>
              <CardDescription>Oracle is exact DP, same losses and wear</CardDescription>
            </CardHeader>
            <CardContent>
              <PolicyBars rows={policyRows} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Train, val, test</CardTitle>
              <CardDescription>{splitRows ? "Val gates, test read once" : "Waiting for gate"}</CardDescription>
            </CardHeader>
            <CardContent>
              {splitRows ? (
                <SplitBars rows={splitRows} />
              ) : (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Split</TableHead>
                      <TableHead>Window</TableHead>
                      <TableHead className="text-right">Days</TableHead>
                      <TableHead className="text-right">Mean £/MWh</TableHead>
                      <TableHead className="text-right">Neg. periods</TableHead>
                      <TableHead className="text-right">Oracle £/day</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {(["train", "val", "test"] as const).map((s) => (
                      <TableRow key={s}>
                        <TableCell>{s}</TableCell>
                        <TableCell className="text-muted-foreground">{data.splits[s].range.join(" to ")}</TableCell>
                        <TableCell className="text-right tabular-nums">{data.splits[s].days}</TableCell>
                        <TableCell className="text-right tabular-nums">{data.splits[s].mean_price}</TableCell>
                        <TableCell className="text-right tabular-nums">{data.splits[s].negative_periods}</TableCell>
                        <TableCell className="text-right tabular-nums">{data.splits[s].oracle_per_day}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              )}
            </CardContent>
          </Card>
        </div>
        {results ? (
          <Card>
            <CardHeader>
              <CardTitle>Gate results</CardTitle>
              
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Policy</TableHead>
                    <TableHead className="text-right">Train</TableHead>
                    <TableHead className="text-right">Val</TableHead>
                    <TableHead className="text-right">Test</TableHead>
                    <TableHead className="text-right">Test 95% CI</TableHead>
                    <TableHead className="text-right">Test % of oracle</TableHead>
                    <TableHead className="text-right">Test cycles</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {Object.entries(results).map(([k, r]) => (
                    <TableRow key={k}>
                      <TableCell>{NAMES[k] ?? k}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.train.score}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.val.score}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.test.score}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.test.ci95?.join(" to ")}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.test.pct_of_oracle}</TableCell>
                      <TableCell className="text-right tabular-nums">{r.test.cycles}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        ) : null}
      </Section>

      <Section kicker="Behaviour" title="Champion behaviour">
        <div className="grid lg:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Cumulative revenue, train</CardTitle>
              <CardDescription>Champion vs seed</CardDescription>
            </CardHeader>
            <CardContent>
              <CumulativeChart data={data.daily} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>One week of dispatch</CardTitle>
              <CardDescription>Last train week, from {data.week[0].date}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-2">
              <WeekPriceChart data={data.week} />
              <WeekSocChart data={data.week} />
            </CardContent>
          </Card>
        </div>
        <div className="grid lg:grid-cols-3 gap-4">
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>GB prices</CardTitle>
              <CardDescription>Daily mean and range, val and test shaded</CardDescription>
            </CardHeader>
            <CardContent>
              <PriceChart data={data.price_days} splits={data.splits} />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Champion rule</CardTitle>
              <CardDescription>Evolve block</CardDescription>
            </CardHeader>
            <CardContent>
              <pre className="text-[11px] leading-snug overflow-auto max-h-96 font-mono whitespace-pre">{data.evolve_block}</pre>
            </CardContent>
          </Card>
        </div>
      </Section>

      <Section kicker="Market" title="GB market">
        <div className="grid lg:grid-cols-3 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>BESS revenue, £k/MW/year</CardTitle>
              <CardDescription>Modo GB index</CardDescription>
            </CardHeader>
            <CardContent>
              <SimpleBars data={revenueIndex} xKey="month" yKey="gbp_k" label="£k/MW/yr" unit="£k" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Sep 2026 revenue mix, £k/MW/yr</CardTitle>
              <CardDescription>Wholesale is 69%</CardDescription>
            </CardHeader>
            <CardContent>
              <SimpleBars data={revenueMixSep26} xKey="stream" yKey="gbp_k" label="£k/MW/yr" unit="£k" horizontal />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>GB fleet, GW</CardTitle>
              <CardDescription>2029 Modo, 2030 NESO range</CardDescription>
            </CardHeader>
            <CardContent>
              <SimpleBars data={fleet} xKey="label" yKey="gw" label="GW" unit=" GW" />
            </CardContent>
          </Card>
        </div>
        <div className="grid lg:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Percent of perfect foresight</CardTitle>
              <CardDescription>Published figures use forecasts; ours does not</CardDescription>
            </CardHeader>
            <CardContent>
              <SimpleBars data={[...captureBenchmarks, { label: "Our champion, train (no forecast)", pct: champion.pct_of_oracle ?? 0, source: "this repo" }]} xKey="label" yKey="pct" label="% of perfect" unit="%" horizontal height="h-72" />
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Pitch arithmetic</CardTitle>
              <CardDescription>Estimates</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableBody>
                  {pitchArithmetic.map((r) => (
                    <TableRow key={r.label}>
                      <TableCell>{r.label}</TableCell>
                      <TableCell className="tabular-nums">{r.value}</TableCell>
                      <TableCell className="text-muted-foreground text-xs">{r.basis}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </Section>

      <Section kicker="Competition" title="Competitors">
        <Card>
          <CardHeader>
            <CardTitle>No published percent-of-perfect, no automated loop</CardTitle>
            <CardDescription>Vendor claims</CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead>Commercial model</TableHead>
                  <TableHead>Dispatch approach</TableHead>
                  <TableHead>Uplift claim</TableHead>
                  <TableHead>Continuous improvement</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {competitors.map((c) => (
                  <TableRow key={c.name}>
                    <TableCell className="whitespace-nowrap">{c.name}</TableCell>
                    <TableCell>{c.model}</TableCell>
                    <TableCell>{c.approach}</TableCell>
                    <TableCell>{c.claim}</TableCell>
                    <TableCell>{c.loop}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </Section>

      <Section kicker="Adoption" title="Adoption">
        <div className="grid lg:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Quant workflow</CardTitle>
              <CardDescription>From job ads</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableBody>
                  {workflowSteps.map((s) => (
                    <TableRow key={s.step}>
                      <TableCell>{s.step}</TableCell>
                      <TableCell className="text-right">
                        <Badge variant={s.automated ? "default" : "outline"}>{s.automated ? "automated by the loop" : "human"}</Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Pitfalls and design answers</CardTitle>
              
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Pitfall</TableHead>
                    <TableHead>In this evaluator</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {pitfalls.map((p) => (
                    <TableRow key={p.pitfall}>
                      <TableCell>{p.pitfall}</TableCell>
                      <TableCell>{p.design}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
        <div className="grid lg:grid-cols-2 gap-4">
          <Card>
            <CardHeader>
              <CardTitle>Simulator spec</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableBody>
                  <TableRow><TableCell>Power / capacity</TableCell><TableCell className="tabular-nums">{data.spec.power_mw} MW / {data.spec.capacity_mwh} MWh</TableCell></TableRow>
                  <TableRow><TableCell>Round-trip efficiency</TableCell><TableCell className="tabular-nums">{data.spec.efficiency * 100}%</TableCell></TableRow>
                  <TableRow><TableCell>Degradation cost</TableCell><TableCell className="tabular-nums">£{data.spec.degradation_gbp_per_mwh}/MWh moved</TableCell></TableRow>
                  <TableRow><TableCell>Step</TableCell><TableCell>half-hour settlement period, APX market index</TableCell></TableRow>
                  <TableRow><TableCell>Policy sees</TableCell><TableCell>strictly past prices, SoC, period, weekday</TableCell></TableRow>
                  <TableRow><TableCell>Scores zero</TableCell><TableCell>crash, timeout, non-math import, literal date, non-finite power</TableCell></TableRow>
                  <TableRow><TableCell>Not modelled yet</TableCell><TableCell>EV plug-in windows, departure targets, ancillary services, BM, intraday</TableCell></TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>Judging criteria</CardTitle>
              <CardDescription>Equal weights</CardDescription>
            </CardHeader>
            <CardContent>
              <Table>
                <TableBody>
                  {judging.map((j) => (
                    <TableRow key={j.criterion}>
                      <TableCell>{j.criterion}</TableCell>
                      <TableCell className="text-right tabular-nums">{j.weight}%</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </div>
      </Section>
    </main>
  );
}
