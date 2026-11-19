---
name: call-mining
description: Mine sales or customer call transcripts in inputs/calls/ for objections, triggers, buyer phrases and disqualifiers, each with a quote and its source. Use on Day 1 before building the Brain.
---

Full method: `docs/capture/call-mining.md` in this repo. Summary:

1. Read every transcript in the folder you are given.
2. Extract, as separate lists:
   - **Buyer phrases:** the exact words the buyer used for the problem and the category. Keep them verbatim, typos included.
   - **Objections:** what made them hesitate.
   - **Triggers:** what happened that made them look now.
   - **Disqualifiers:** signs they are not a fit.
   - **Proof they asked for:** numbers, logos, comparisons.
3. Every item gets a quote and `source: <file>, <timestamp or line>`. No quote, no item. List anything you inferred without a quote under "needs a human".
4. Write the result to `inputs/mined.md`, grouped by list, with the most repeated items first.

Do not summarize in your own words where the buyer's words exist. The buyer's phrasing is the point.

If a list has nothing in the transcripts, write "None found". Never fill a list to make it look complete. A rep's claim (for example a pilot result) goes under "Proof they asked for" only if the buyer asked for it. Otherwise it goes in `brain/CONTEXT.md` as a fact sourced to the call.
