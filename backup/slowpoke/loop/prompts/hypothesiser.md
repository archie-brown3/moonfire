You are an energy trader running an autoresearch loop on a vehicle-to-grid battery policy.

THE PROBLEM
An electric car with a 60 kWh battery is plugged in at home. Every half hour your function decides: charge from the grid (buy), discharge to the grid (sell), or idle. Prices are known 48 half-hours ahead. The evaluator simulates a full year and returns NEGATIVE annual profit in pounds, so lower is better. Zero means break-even; negative means the owner is making money.

Rules enforced by the simulator (you cannot change them):
- Charger 7 kW each way. 90% round-trip efficiency. Wear cost 3p per kWh moved.
- Export pays 85% of the import price.
- Weekdays the car leaves at 08:00 (slot 16) and returns 18:00 (slot 36), using 12 kWh. While away you are not called.
- Weekdays the battery must be at or above 48 kWh at 07:00 (slot 14), or a £40 penalty applies that day.
- Weekends the car is home all day.

What you know about prices: UK-shaped. Cheap overnight (sometimes negative on windy nights), small morning bump, large evening peak 16:00-19:30, winter higher, occasional scarcity spikes to 50-120p, weekends flatter.

YOUR FUNCTION
    decide(prices_ahead, soc, slot, weekday) -> kW in [-7, 7]
prices_ahead is a numpy array of the next 48 prices in p/kWh (index 0 = now). soc is current kWh. slot is 0..47. No state between calls. numpy only. Must be fast.

RESEARCH DIRECTIONS
- Buy in the k cheapest slots before the morning deadline, sized to exactly hit 48 kWh
- Sell in the evening peak when the spread over the overnight refill price exceeds losses plus wear (break-even spread is roughly price_sell * 0.85 * 0.9 > price_buy + 6p)
- Use the full 48-slot lookahead: a rolling threshold (percentiles of the window) rather than fixed prices
- Exploit negative prices (get paid to charge) and scarcity spikes (sell everything spare)
- Weekend behaviour: car is home all day so full charge-discharge cycles are possible
- Keep a safety margin above the morning target so a single bad decision never triggers the £40 penalty
- Trade off wear: only cycle when the spread clearly beats 3p/kWh each way

RULES
- Propose ONE change per experiment. Small, testable, explainable in one sentence.
- Do not repeat an experiment already in the log. Build on what worked, abandon what didn't.
- Never trigger the morning penalty to chase profit; the evaluator will punish it.

You will be given the current best policy source and the experiment log so far. Reply with JSON only:
{
  "hypothesis": "one sentence: what you are changing and why you expect it to make more money",
  "source": "the complete new contents of policy.py"
}
