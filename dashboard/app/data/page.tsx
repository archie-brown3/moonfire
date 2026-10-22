import type { Metadata } from "next";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import data from "@/data/dashboard.json";

export const metadata: Metadata = { title: "The data" };

// From data/prices.csv as written by fetch_prices.py: one day past the test window, outside every split.
const FILE_ROWS = 18192;
const FILE_LAST = "2026-10-15";

type Split = {
  days: number;
  periods: number;
  mean_price: number;
  negative_periods: number;
  oracle_per_day: number;
  range: string[];
};

const SPLITS: {
  key: "train" | "val" | "test";
  name: string;
  reader: string;
}[] = [
  {
    key: "train",
    name: "Train",
    reader: "The search, for every idea",
  },
  {
    key: "val",
    name: "Validation",
    reader: "gate.py, to promote a rule",
  },
  {
    key: "test",
    name: "Test",
    reader: "gate.py, once, to report",
  },
];

const date = (iso: string) =>
  new Date(`${iso}T00:00:00Z`).toLocaleDateString("en-GB", {
    day: "numeric",
    month: "short",
    year: "numeric",
    timeZone: "UTC",
  });

const num = (v: number) => v.toLocaleString("en-GB");

function Section({
  title,
  lede,
  children,
}: {
  title: string;
  lede: React.ReactNode;
  children?: React.ReactNode;
}) {
  return (
    <section className="space-y-4">
      <div className="max-w-3xl space-y-2">
        <h2 className="text-xl tracking-tight">{title}</h2>
        <div className="space-y-2 text-sm leading-relaxed text-muted-foreground">
          {lede}
        </div>
      </div>
      {children}
    </section>
  );
}

function File({ children }: { children: React.ReactNode }) {
  return (
    <code className="bg-muted px-1.5 py-0.5 text-xs text-foreground">
      {children}
    </code>
  );
}

export default function DataPage() {
  const splits = data.splits as Record<string, Split>;
  const spec = data.spec;
  const first = splits.train.range[0];
  const lastUsed = splits.test.range[1];
  const usedDays = SPLITS.reduce((s, x) => s + splits[x.key].days, 0);
  const usedPeriods = SPLITS.reduce((s, x) => s + splits[x.key].periods, 0);
  const ceilingRise = splits.test.oracle_per_day / splits.train.oracle_per_day;
  const eachWay = Math.sqrt(spec.efficiency) * 100;

  const steps: { text: string; file: string }[] = [
    {
      text: "Ask the API for prices seven days at a time, because it caps each request at seven days. Where two pages overlap, the same half-hour is kept once.",
      file: "fetch_prices.py",
    },
    {
      text: "Keep one exchange, APX. The API also returns N2EX, a second exchange with little traded volume, so we drop it.",
      file: "fetch_prices.py",
    },
    {
      text: "Drop the first and last day of the download, which arrive incomplete. Clock-change days stay as they are: 26 Oct 2025 has 50 half-hours and 29 Mar 2026 has 46.",
      file: "fetch_prices.py",
    },
    {
      text: "Fill the 12 half-hours where nothing traded with a straight line between the nearest traded prices either side, so the simulator never meets a gap.",
      file: "fetch_prices.py",
    },
    {
      text: "Write data/prices.csv, one row per half-hour: start time, settlement date, period number, price in £/MWh and traded volume.",
      file: "fetch_prices.py",
    },
    {
      text: "Load only the rows whose date falls inside the requested split, and add the day of the week.",
      file: "battery.py",
    },
    {
      text: "Replay those rows one half-hour at a time. At each step the rule returns how hard to charge or discharge, and the simulator applies the limits and books the cash.",
      file: "battery.py",
    },
  ];

  return (
    <main className="mx-auto w-full max-w-7xl space-y-12 px-6 py-10">
      <div className="max-w-3xl space-y-2">
        <h1 className="text-2xl tracking-tight">
          A year of half-hourly British power prices
        </h1>
        <p className="text-sm leading-relaxed text-muted-foreground">
          Every score on this dashboard comes from replaying real GB market
          prices, one per half-hour, from {date(first)} to {date(lastUsed)}. The
          search learns on the first eight months only, and its rule is judged
          on the months after, which it never sees.
        </p>
      </div>

      <Section
        title="Where it comes from"
        lede={
          <>
            <p>
              Britain&apos;s electricity market settles every day in 48
              half-hours. Elexon publishes a market index price for each one:
              the price power traded at on the exchange in that half-hour, in
              pounds per megawatt-hour. Its BMRS API is open, with no account or
              key.
            </p>
            <p>
              We keep the APX exchange&apos;s series. The download holds{" "}
              <span className="tabular-nums text-foreground">
                {num(FILE_ROWS)}
              </span>{" "}
              half-hours from {date(first)} to {date(FILE_LAST)}; the splits
              below use{" "}
              <span className="tabular-nums text-foreground">
                {num(usedPeriods)}
              </span>{" "}
              of them, {usedDays} days, and leave the last day unused.
            </p>
          </>
        }
      >
        <p className="max-w-3xl overflow-x-auto text-xs text-muted-foreground">
          <code className="whitespace-nowrap">
            data.elexon.co.uk/bmrs/api/v1/balancing/pricing/market-index?from=…&amp;to=…
          </code>
        </p>
      </Section>

      <Section
        title="How it is processed"
        lede={
          <p>
            Five steps run once to build the price file. The last two run every
            time a rule is scored.
          </p>
        }
      >
        <ol className="max-w-5xl divide-y divide-border border-y border-border">
          {steps.map((s, i) => (
            <li
              key={s.text}
              className="grid grid-cols-[2rem_1fr] gap-x-4 gap-y-2 py-4 md:grid-cols-[2rem_1fr_10rem]"
            >
              <span className="text-sm tabular-nums text-muted-foreground">
                {i + 1}
              </span>
              <p className="text-sm leading-relaxed">{s.text}</p>
              <div className="col-start-2 md:col-start-3 md:text-right">
                <File>{s.file}</File>
              </div>
            </li>
          ))}
        </ol>
      </Section>

      <Section
        title="How it is split"
        lede={
          <>
            <p>
              The year is cut into three windows by date, never mixing days
              between them, so a rule is always tested on prices that come after
              the ones it learned from. That is also how it would run for real.
            </p>
            <p>
              Prices rose through the year. The most a battery could have earned
              with perfect foresight is{" "}
              <span className="tabular-nums text-foreground">
                {ceilingRise.toFixed(1)}×
              </span>{" "}
              higher on test than on train, which is why we report £ per MW per
              day and percentage of that ceiling side by side.
            </p>
          </>
        }
      >
        <Card className="max-w-5xl py-0">
          <Table>
            <TableHeader>
              <TableRow className="hover:bg-transparent">
                <TableHead className="pl-4">Split</TableHead>
                <TableHead>Window</TableHead>
                <TableHead className="text-right">Days</TableHead>
                <TableHead className="text-right">Mean £/MWh</TableHead>
                <TableHead className="h-auto w-28 py-2 text-right whitespace-normal">
                  Negative half-hours
                </TableHead>
                <TableHead className="h-auto w-28 py-2 text-right whitespace-normal">
                  Perfect foresight £/MW/day
                </TableHead>
                <TableHead className="pr-4">Read by</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {SPLITS.map(({ key, name, reader }) => {
                const s = splits[key];
                return (
                  <TableRow key={key} className="hover:bg-transparent">
                    <TableCell className="py-3 pl-4">{name}</TableCell>
                    <TableCell className="tabular-nums">
                      {date(s.range[0])} to {date(s.range[1])}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {s.days}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {s.mean_price.toFixed(1)}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {s.negative_periods}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {s.oracle_per_day.toFixed(1)}
                    </TableCell>
                    <TableCell className="pr-4 text-muted-foreground">
                      {reader}
                    </TableCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
        </Card>
        <p className="max-w-3xl text-xs leading-relaxed text-muted-foreground">
          A negative price means the battery is paid to charge. Perfect
          foresight is the most any rule could earn if it knew every future
          price, worked out exactly by <File>battery.py</File>.
        </p>
      </Section>

      <Section
        title="What the simulator assumes"
        lede={
          <p>
            The rule is called once per half-hour with the prices before that
            half-hour, the battery&apos;s charge, the period number and the day
            of the week. It never sees the current price, which is only known
            after the half-hour settles, or anything later.
          </p>
        }
      >
        <div className="grid max-w-5xl gap-4 lg:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>The battery</CardTitle>
              <CardDescription>
                Fixed in battery.py. The search cannot change it.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <dl className="divide-y divide-border text-sm">
                {[
                  ["Power", `${spec.power_mw} MW`],
                  [
                    "Energy",
                    `${spec.capacity_mwh} MWh, so 2 hours at full power`,
                  ],
                  [
                    "Round trip",
                    `${Math.round(spec.efficiency * 100)}%, about ${eachWay.toFixed(1)}% each way`,
                  ],
                  [
                    "Wear",
                    `£${spec.degradation_gbp_per_mwh} per MWh moved, in or out`,
                  ],
                  ["Start", "Half full at the start of each window"],
                ].map(([k, v]) => (
                  <div
                    key={k}
                    className="grid grid-cols-[6.5rem_1fr] gap-4 py-2"
                  >
                    <dt className="text-muted-foreground">{k}</dt>
                    <dd className="tabular-nums">{v}</dd>
                  </div>
                ))}
              </dl>
              <p className="mt-4 text-xs leading-relaxed text-muted-foreground">
                The rule only asks for an amount. The simulator caps it at the
                power rating and at what the battery can hold or give, then
                books the cash, the losses and the wear.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader>
              <CardTitle>What it leaves out</CardTitle>
              <CardDescription>
                Each of these would change the £ figures.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="divide-y divide-border text-sm leading-relaxed">
                <li className="py-2">
                  No forecasts. Real operators use forecast feeds; the rule here
                  has only past prices.
                </li>
                <li className="py-2">
                  One market. It trades the market index only, not the day-ahead
                  auction, frequency response or the Balancing Mechanism, so the
                  £ here is a floor.
                </li>
                <li className="py-2">
                  No market impact. At 1 MW we assume the battery&apos;s own
                  trades do not move the price.
                </li>
                <li className="py-2">
                  Flat wear cost. Real ageing depends on how the battery is
                  cycled; a richer model would slot into battery.py.
                </li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </Section>
    </main>
  );
}
