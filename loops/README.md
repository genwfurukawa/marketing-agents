# LOOPS

One loop per discipline. Each runs all five stages on its own clock, and all of them
read from the same Brain.

| Loop | Clock | What it owns |
|---|---|---|
| `sm-content` | Daily build, weekly capture | Briefs, drafts, publication |
| `sm-aeo` | Weekly capture, continuous improve | Getting cited by AI engines |
| `sm-social` | Daily | Owned distribution and the signal it returns |
| `sm-demand` | Weekly | Turning attention into named, scored people |

**Why separate loops rather than one big pipeline.** They run at different speeds.
Content builds daily and captures weekly. AEO improves continuously and ships in
batches. Forcing them onto one clock means the fastest one waits for the slowest.

**Why they share the Brain.** Four loops reading four different versions of who the
buyer is produces four flavours of off target work. One substrate, four speeds.

Each loop directory holds its agents in stage subdirectories. See
[`../AUTONOMY.md`](../AUTONOMY.md) for what each one does and how much of the work
it actually takes off you.
