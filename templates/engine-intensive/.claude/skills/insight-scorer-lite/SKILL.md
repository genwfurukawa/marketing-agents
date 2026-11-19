---
name: insight-scorer-lite
description: Rank the mined items in inputs/mined.md and turn the top 3 into Insight Objects in inputs/insights.md. Files-only version of insight-scorer and insight-object-builder (no Notion). Use on Day 1 and in the weekly routine.
---

Score each mined item from 1 to 5 on four things, and add them up (20 maximum):

- **Evidence:** how many different buyers say it, in their own words. Rep and vendor lines don't count here. 1 buyer quote = 2, 2 = 3, 3 = 4, 4+ = 5.
- **Pain:** does the buyer attach cost, time or risk to it?
- **Fit:** does it match `brain/ICP.md`?
- **Proof:** does any file in `brain/` hold a sourced fact that answers it? With no proof, cap the score at 10.

Break ties on Evidence, then Pain.

Write the ranked list to the top of `inputs/insights.md`, with one line on why each item scored what it did. Then build an Insight Object for each of the top 3:

```
## Insight [N]: <one-line claim>
- evidence: "<quote>" source: <file, timestamp> (+ more)
- audience: <who, from ICP.md>
- angle: <the point of view we take>
- channel fit: linkedin | email | page, and why
- brain ids: <src: ids the writers may use>
```

Never invent an evidence quote. An item with no quote is not an insight.
