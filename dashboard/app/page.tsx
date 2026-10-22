import Link from "next/link";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Table, TableBody, TableCell, TableRow } from "@/components/ui/table";
import { PriceChart, SimpleBars } from "@/components/charts";
import data from "@/data/dashboard.json";
import { captureBenchmarks, fleet, pitchArithmetic, revenueIndex, revenueMixSep26 } from "@/data/research";
import { trainEval } from "@/lib/results";

function Section({ title, kicker, children }: { title: string; kicker: string; children: React.ReactNode }) {
  return (
    <section className="space-y-4">
      <div>
        <div className="text-xs uppercase tracking-wide text-muted-foreground">{kicker}</div>
        <h2 className="text-xl">{title}</h2>
      </div>
      {children}
    </section>
  );
}

export default function Home() {
  const champion = trainEval.champion;

  return (
    <main className="mx-auto max-w-7xl px-6 py-10 space-y-12 [&_td]:whitespace-normal [&_th]:whitespace-normal [&_td]:align-top">
      <header className="max-w-[65ch] space-y-4">
        <h1 className="text-3xl tracking-tight text-balance">A battery&apos;s earnings come down to one rule</h1>
        <div className="space-y-4 text-base leading-relaxed">
          <ul className="list-disc space-y-2 pl-5">
            <li>
              Britain has 8.5 GW of grid batteries and needs 23 to 27 GW by 2030. Every half hour, a rule decides whether each one charges,
              discharges or waits.
            </li>
            <li>That rule sets the earnings. In September 2026 the average two-hour battery earned £104k per MW a year; the best earned £148k.</li>
            <li>
              Quants improve the rule by hand today. We automate that: each new rule is scored against perfect foresight and kept only if it also
              wins on months the search never saw.
            </li>
          </ul>
          <p>
            <Link href="/replay" className="underline underline-offset-4 hover:text-muted-foreground">
              Watch the search improve the rule
            </Link>
          </p>
        </div>
        <p className="text-xs text-muted-foreground">Sources: Modo Energy (fleet, revenue index, September 2026); NESO (2030 need).</p>
      </header>

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
        <Card>
          <CardHeader>
            <CardTitle>GB prices, Oct 2025 to Oct 2026</CardTitle>
            <CardDescription>Daily mean and range. Validation and test months shaded.</CardDescription>
          </CardHeader>
          <CardContent>
            <PriceChart data={data.price_days} splits={data.splits} />
          </CardContent>
        </Card>
      </Section>
    </main>
  );
}
