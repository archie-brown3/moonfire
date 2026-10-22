"use client";

import {
  Area,
  Bar,
  BarChart,
  CartesianGrid,
  ComposedChart,
  LabelList,
  Line,
  LineChart,
  ReferenceArea,
  ReferenceLine,
  Scatter,
  XAxis,
  YAxis,
} from "recharts";
import {
  type ChartConfig,
  ChartContainer,
  ChartLegend,
  ChartLegendContent,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";

// Validated categorical palette (dataviz reference instance): blue, orange, aqua, yellow.
const C = {
  champion: { light: "#2a78d6", dark: "#3987e5" },
  seed: { light: "#eb6834", dark: "#d95926" },
  oracle: { light: "#1baf7a", dark: "#199e70" },
  fixed: { light: "#eda100", dark: "#c98500" },
  neutral: { light: "#8a8984", dark: "#9a998f" },
  band: { light: "#cde2fb", dark: "#184f95" },
};

const money = (v: number) => `£${v.toLocaleString("en-GB", { maximumFractionDigits: 1 })}`;

type LoopRow = { iter: number; idea: string; score: number; kept: boolean; best: number };

export function LoopChart({ data }: { data: LoopRow[] }) {
  const config = {
    score: { label: "Attempt (train £/MW/day)", theme: C.neutral },
    best: { label: "Best kept", theme: C.champion },
  } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-72 w-full aspect-auto">
      <ComposedChart data={data} margin={{ left: 0, right: 12, top: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis hide dataKey="iter" tickLine={false} axisLine={false} tickMargin={8} />
        <YAxis tickLine={false} axisLine={false} width={36} />
        <ChartTooltip
          content={
            <ChartTooltipContent
              labelFormatter={(_, p) => {
                const r = p?.[0]?.payload as LoopRow | undefined;
                return r ? `#${r.iter} ${r.idea}${r.kept ? " (kept)" : ""}` : "";
              }}
            />
          }
        />
        <ChartLegend content={<ChartLegendContent />} />
        <Line type="linear" dataKey="score" stroke="var(--color-score)" strokeWidth={1} dot={false} isAnimationActive={false} />
        <Line
          type="stepAfter"
          dataKey="best"
          stroke="var(--color-best)"
          strokeWidth={2}
          isAnimationActive={false}
          dot={(p: { cx?: number; cy?: number; payload?: LoopRow; index?: number }) =>
            p.payload?.kept ? <circle key={p.index} cx={p.cx} cy={p.cy} r={4} fill="var(--color-best)" stroke="var(--background)" strokeWidth={2} /> : <g key={p.index} />
          }
        />
      </ComposedChart>
    </ChartContainer>
  );
}

export function PolicyBars({ rows }: { rows: { name: string; score: number; pct: number | null }[] }) {
  const config = { score: { label: "Train £/MW/day", theme: C.champion } } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-56 w-full aspect-auto">
      <BarChart data={rows} layout="vertical" margin={{ left: 8, right: 48 }}>
        <CartesianGrid horizontal={false} />
        <XAxis hide type="number" tickLine={false} axisLine={false} />
        <YAxis type="category" dataKey="name" tickLine={false} axisLine={false} width={110} />
        <ChartTooltip content={<ChartTooltipContent formatter={(v) => money(Number(v))} />} />
        <Bar dataKey="score" fill="var(--color-score)" radius={0} barSize={18} isAnimationActive={false}>
          <LabelList dataKey="score" position="right" formatter={(v) => money(Number(v))} className="fill-foreground" fontSize={11} />
        </Bar>
      </BarChart>
    </ChartContainer>
  );
}

export function SplitBars({ rows }: { rows: { name: string; train: number; val: number; test: number }[] }) {
  const config = {
    train: { label: "Train", theme: C.neutral },
    val: { label: "Val", theme: C.fixed },
    test: { label: "Test (held out)", theme: C.champion },
  } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-64 w-full aspect-auto">
      <BarChart data={rows} margin={{ left: 0, right: 8 }} barGap={2}>
        <CartesianGrid vertical={false} />
        <XAxis hide dataKey="name" tickLine={false} axisLine={false} />
        <YAxis tickLine={false} axisLine={false} width={40} />
        <ChartTooltip content={<ChartTooltipContent formatter={(v, n) => `${n}: ${money(Number(v))}`} />} />
        <ChartLegend content={<ChartLegendContent />} />
        <Bar dataKey="train" fill="var(--color-train)" radius={0} isAnimationActive={false} />
        <Bar dataKey="val" fill="var(--color-val)" radius={0} isAnimationActive={false} />
        <Bar dataKey="test" fill="var(--color-test)" radius={0} isAnimationActive={false} />
      </BarChart>
    </ChartContainer>
  );
}

type PriceDay = { date: string; split: string; mean: number; min: number; max: number; spread: number };

export function PriceChart({ data, splits }: { data: PriceDay[]; splits: Record<string, { range: string[] }> }) {
  const rows = data.map((d) => ({ ...d, range: [d.min, d.max] }));
  const config = {
    range: { label: "Daily min to max", theme: C.band },
    mean: { label: "Daily mean £/MWh", theme: C.champion },
  } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-72 w-full aspect-auto">
      <ComposedChart data={rows} margin={{ left: 0, right: 12, top: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis hide dataKey="date" tickLine={false} axisLine={false} tickMargin={8} minTickGap={48} tickFormatter={(d: string) => d.slice(0, 7)} />
        <YAxis tickLine={false} axisLine={false} width={44} />
        <ReferenceArea x1={splits.val.range[0]} x2={splits.val.range[1]} fill="var(--color-mean)" fillOpacity={0.06} label={{ value: "val", position: "insideTop", fontSize: 11 }} />
        <ReferenceArea x1={splits.test.range[0]} x2={splits.test.range[1]} fill="var(--color-mean)" fillOpacity={0.12} label={{ value: "test", position: "insideTop", fontSize: 11 }} />
        <ReferenceLine y={0} stroke="var(--border)" />
        <ChartTooltip
          content={
            <ChartTooltipContent
              formatter={(v, n) => (Array.isArray(v) ? `range: ${v[0]} to ${v[1]} £/MWh` : `${n}: ${v} £/MWh`)}
              labelFormatter={(_, p) => {
                const r = p?.[0]?.payload as PriceDay | undefined;
                return r ? `${r.date} (${r.split})` : "";
              }}
            />
          }
        />
        <ChartLegend content={<ChartLegendContent />} />
        <Area dataKey="range" stroke="none" fill="var(--color-range)" fillOpacity={0.6} isAnimationActive={false} />
        <Line type="monotone" dataKey="mean" stroke="var(--color-mean)" strokeWidth={1.5} dot={false} isAnimationActive={false} />
      </ComposedChart>
    </ChartContainer>
  );
}

export function CumulativeChart({ data }: { data: { date: string; champion_cum: number; seed_cum: number }[] }) {
  const config = {
    champion_cum: { label: "Champion", theme: C.champion },
    seed_cum: { label: "Seed", theme: C.seed },
  } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-64 w-full aspect-auto">
      <LineChart data={data} margin={{ left: 0, right: 12, top: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis hide dataKey="date" tickLine={false} axisLine={false} tickMargin={8} minTickGap={48} tickFormatter={(d: string) => d.slice(0, 7)} />
        <YAxis tickLine={false} axisLine={false} width={48} tickFormatter={(v: number) => `£${(v / 1000).toFixed(0)}k`} />
        <ChartTooltip content={<ChartTooltipContent formatter={(v, n) => `${n}: ${money(Number(v))}`} />} />
        <ChartLegend content={<ChartLegendContent />} />
        <Line type="monotone" dataKey="champion_cum" stroke="var(--color-champion_cum)" strokeWidth={2} dot={false} isAnimationActive={false} />
        <Line type="monotone" dataKey="seed_cum" stroke="var(--color-seed_cum)" strokeWidth={2} dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartContainer>
  );
}

type WeekRow = { h: number; date: string; period: number; price: number; champion_soc: number; seed_soc: number; champion_action: number; seed_action: number };

export function WeekPriceChart({ data }: { data: WeekRow[] }) {
  const charges = data.filter((r) => r.champion_action < 0).map((r) => ({ h: r.h, charge: r.price }));
  const sells = data.filter((r) => r.champion_action > 0).map((r) => ({ h: r.h, sell: r.price }));
  const config = {
    price: { label: "APX price £/MWh", theme: C.neutral },
    charge: { label: "Champion charges", theme: C.oracle },
    sell: { label: "Champion discharges", theme: C.seed },
  } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-64 w-full aspect-auto">
      <ComposedChart data={data} margin={{ left: 0, right: 12, top: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis hide dataKey="h" type="number" domain={[0, 168]} ticks={[0, 24, 48, 72, 96, 120, 144, 168]} tickLine={false} axisLine={false} tickFormatter={(h: number) => `${h}h`} />
        <YAxis tickLine={false} axisLine={false} width={44} />
        <ReferenceLine y={0} stroke="var(--border)" />
        <ChartTooltip content={<ChartTooltipContent labelFormatter={(h) => `hour ${h}`} />} />
        <ChartLegend content={<ChartLegendContent />} />
        <Line type="linear" dataKey="price" stroke="var(--color-price)" strokeWidth={1} dot={false} isAnimationActive={false} />
        <Scatter data={charges} dataKey="charge" name="charge" fill="var(--color-charge)" isAnimationActive={false} shape={(p: { cx?: number; cy?: number }) => <circle cx={p.cx} cy={p.cy} r={4} fill="var(--color-charge)" stroke="var(--background)" strokeWidth={1.5} />} />
        <Scatter data={sells} dataKey="sell" name="sell" fill="var(--color-sell)" isAnimationActive={false} shape={(p: { cx?: number; cy?: number }) => <circle cx={p.cx} cy={p.cy} r={4} fill="var(--color-sell)" stroke="var(--background)" strokeWidth={1.5} />} />
      </ComposedChart>
    </ChartContainer>
  );
}

export function WeekSocChart({ data }: { data: WeekRow[] }) {
  const config = {
    champion_soc: { label: "Champion SoC (MWh)", theme: C.champion },
    seed_soc: { label: "Seed SoC (MWh)", theme: C.seed },
  } satisfies ChartConfig;
  return (
    <ChartContainer config={config} className="h-44 w-full aspect-auto">
      <LineChart data={data} margin={{ left: 0, right: 12, top: 8 }}>
        <CartesianGrid vertical={false} />
        <XAxis hide dataKey="h" type="number" domain={[0, 168]} ticks={[0, 24, 48, 72, 96, 120, 144, 168]} tickLine={false} axisLine={false} tickFormatter={(h: number) => `${h}h`} />
        <YAxis domain={[0, 2]} ticks={[0, 1, 2]} tickLine={false} axisLine={false} width={44} />
        <ChartTooltip content={<ChartTooltipContent labelFormatter={(h) => `hour ${h}`} />} />
        <ChartLegend content={<ChartLegendContent />} />
        <Line type="stepAfter" dataKey="champion_soc" stroke="var(--color-champion_soc)" strokeWidth={2} dot={false} isAnimationActive={false} />
        <Line type="stepAfter" dataKey="seed_soc" stroke="var(--color-seed_soc)" strokeWidth={1.5} dot={false} isAnimationActive={false} />
      </LineChart>
    </ChartContainer>
  );
}

export function SimpleBars({
  data,
  xKey,
  yKey,
  label,
  unit,
  horizontal = false,
  height = "h-56",
}: {
  data: Record<string, string | number>[];
  xKey: string;
  yKey: string;
  label: string;
  unit?: string;
  horizontal?: boolean;
  height?: string;
}) {
  const config = { [yKey]: { label, theme: C.champion } } satisfies ChartConfig;
  const fmt = (v: number) => `${unit === "£k" ? "£" : ""}${v}${unit && unit !== "£k" ? unit : unit === "£k" ? "k" : ""}`;
  return (
    <ChartContainer config={config} className={`${height} w-full aspect-auto`}>
      <BarChart data={data} layout={horizontal ? "vertical" : "horizontal"} margin={horizontal ? { left: 8, right: 40 } : { left: 0, right: 8, top: 24 }}>
        <CartesianGrid vertical={horizontal} horizontal={!horizontal} />
        {horizontal ? (
          <>
            <XAxis hide type="number" tickLine={false} axisLine={false} />
            <YAxis type="category" dataKey={xKey} tickLine={false} axisLine={false} width={170} />
          </>
        ) : (
          <>
            <XAxis hide dataKey={xKey} tickLine={false} axisLine={false} interval={0} fontSize={11} />
            <YAxis tickLine={false} axisLine={false} width={40} />
          </>
        )}
        <ReferenceLine {...(horizontal ? { x: 0 } : { y: 0 })} stroke="var(--border)" />
        <ChartTooltip content={<ChartTooltipContent formatter={(v) => fmt(Number(v))} />} />
        <Bar dataKey={yKey} fill={`var(--color-${yKey})`} radius={0} barSize={horizontal ? 14 : 28} isAnimationActive={false}>
          <LabelList dataKey={yKey} position={horizontal ? "right" : "top"} formatter={(v) => fmt(Number(v))} className="fill-foreground" fontSize={11} />
        </Bar>
      </BarChart>
    </ChartContainer>
  );
}
