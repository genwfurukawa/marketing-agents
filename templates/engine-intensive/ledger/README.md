# Ledger

One row per thing that shipped, plus one visibility row per engine each week. Leave a cell empty rather than estimating it. Log the day it happens: SuperMarketers' own 30-day ledger has hours on only 4 of its 11 rows, because the rest weren't logged at the time.

| Column | Meaning |
|---|---|
| `type` | `shipped` or `visibility` |
| `minutes` | Your hands-on time, start to approve |
| `cost_usd` | From `total_cost_usd` in the run's JSON |
| `named_or_cited` | For visibility rows: answers naming or citing you, out of answers asked, e.g. `2/60` |
| `source_ids` | The `src:` ids the piece used |
