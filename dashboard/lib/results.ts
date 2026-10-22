import data from "@/data/dashboard.json";

// Evaluator output shapes and the policy rows the results charts plot. Moved from app/page.tsx.
export type Eval = {
  score: number;
  ci95?: number[];
  pct_of_oracle: number | null;
  cycles: number;
  days?: number;
  error: string | null;
};
type Results = Record<string, Record<"train" | "val" | "test", Eval>> | null;

export const NAMES: Record<string, string> = {
  do_nothing: "Do nothing",
  fixed_schedule: "Fixed schedule",
  seed: "Seed policy",
  champion: "Champion",
  oracle: "Perfect foresight",
};

export const trainEval = data.train_eval as Record<string, Eval>;

export function policyRows() {
  return [
    ...["do_nothing", "fixed_schedule", "seed", "champion"].map((k) => ({
      name: NAMES[k],
      score: trainEval[k].score,
      pct: trainEval[k].pct_of_oracle,
    })),
    { name: NAMES.oracle, score: data.oracle_train_per_day, pct: 100 },
  ];
}

export function splitRows() {
  const results = data.results as Results;
  if (!results) return null;
  return [
    ...["fixed_schedule", "seed", "champion"].map((k) => ({
      name: NAMES[k],
      train: results[k].train.score,
      val: results[k].val.score,
      test: results[k].test.score,
    })),
    {
      name: NAMES.oracle,
      train: data.splits.train.oracle_per_day,
      val: data.splits.val.oracle_per_day,
      test: data.splits.test.oracle_per_day,
    },
  ];
}
