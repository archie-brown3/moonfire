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
      <Replay data={replay as unknown as ReplayData} />
    </main>
  );
}
