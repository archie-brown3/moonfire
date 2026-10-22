import type { Metadata } from "next";
import { Replay, type ReplayData } from "@/components/replay";
import replay from "@/data/replay.json";

export const metadata: Metadata = { title: "How it learned" };

export default function ReplayPage() {
  return (
    <main className="mx-auto w-full max-w-7xl space-y-8 px-6 py-10">
      <div className="max-w-3xl space-y-2">
        <h1 className="text-2xl tracking-tight">
          How the search found a better rule
        </h1>
        <p className="text-sm text-muted-foreground">
          Each dot is one idea the search tried on the training months. The blue
          line only moves when an idea beats the best so far. The code on the
          right is the rule at that moment.
        </p>
      </div>
      <section className="max-w-3xl space-y-2 text-sm leading-relaxed">
        <h2 className="text-base">The rule, in plain terms</h2>
        <p>
          The rule tells one grid battery, every half hour, whether to buy power
          (charge), sell it (discharge) or wait, using only the prices it has
          already seen and how full it is:
        </p>
        <ul className="list-disc space-y-1 pl-5">
          <li>
            <strong className="font-medium">Charge</strong> when the price is in
            the cheapest fifth of the past week, or is the lowest expected in
            the next 10 hours, and selling later should cover losses and £20/MWh
            of wear. It holds off if enough cheaper half-hours are coming to
            fill up then. It always charges when the price is negative.
          </li>
          <li>
            <strong className="font-medium">Discharge</strong> when the price is
            in the dearest quarter of the past week, unless enough dearer
            half-hours are expected in the next 4.5 hours to empty the battery
            then.
          </li>
          <li>
            <strong className="font-medium">Wait</strong> otherwise.
          </li>
        </ul>
        <p className="text-muted-foreground">
          To guess the coming hours it averages the same half-hours over the
          past five days. The search started from a simpler rule that compared
          the price with the last two days and nothing else.
        </p>
      </section>
      <Replay data={replay as unknown as ReplayData} />
    </main>
  );
}
