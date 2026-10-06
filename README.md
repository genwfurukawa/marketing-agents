# Marketing Agents

**The open subset of the system [SuperMarketers](https://www.supermarketers.ai) installs, runs and hands over.**

Most AI marketing work starts from an empty prompt. Someone describes the company
again, pastes in a few links, and hopes. The output comes back generic because the
input was.

This repo is the other approach, in the open: a shared memory every agent reads from
before it makes anything, a voice pulled out of your own best writing, and gates that
check the work before a human ever sees it.

Same models everyone else is using. Different input.

## The picture is the codebase

Five stages, one shared Brain. Every directory here is a piece of it.

```
CAPTURE -> BUILD -> APPROVE -> SHIP -> IMPROVE
                                          |
                    (what you learn feeds back into CAPTURE and BUILD)
```

| Stage | Clock | What it does |
|---|---|---|
| **CAPTURE** | Continuous, ranked weekly | Expertise and signals become source-linked knowledge and a ranked queue. The judgment stage. |
| **BUILD** | Daily | Queue items become drafts. Volume happens here. |
| **APPROVE** | Per artifact | Gates that stop bad output, then one human decision |
| **SHIP** | Daily | Publish and distribute, which are not the same act |
| **IMPROVE** | Weekly + monthly | Not a report, an input. It rewrites what CAPTURE ranks next. |

The agents live in `.claude/`, where Claude Code can find them. `brain/`, `loops/`,
`gates/` and `ports/` are the map: what each agent is for, which stage it belongs to,
and how much of the work it actually takes off you. [`MAP.md`](MAP.md) is the index.

**The Brain is not a stage.** It is the substrate every stage reads from before it
does anything. If it is wrong, everything downstream is confidently wrong. That is
why `brain/` comes first in this repo and why the capture guides live there.

**APPROVE is its own stage, not a step inside BUILD.** Three reasons. It makes the
trust boundary visible, so you can see exactly where judgment sits. It enforces
maker is not checker: the agent that built the output never declares it done. And it
is the one place a human is required, which is what makes the rest safe to automate.

> A human marketing team runs one loop per quarter. An agentic system runs this one
> continuously, at five different speeds at once. That mismatch, not the tooling, is
> what changes the output.

## Four things, and all of them are yours

| | What it is | Where |
|---|---|---|
| **The Brain** | The memory the system reads from | `brain/` |
| **The Voice** | How you sound, extracted from your own best work | `brain/BRAND.md` |
| **The Gates** | Source, fabrication, voice, structure, fit, risk. Checked before anyone reads it. | `gates/` |
| **The Ledger** | What shipped, what it replaced, what it produced | `ledger/` |

Nothing here phones home, runs on our platform, or expires. Clone it and it is yours.

## Start here

```bash
git clone https://github.com/genwfurukawa/marketing-agents.git
cd marketing-agents
```

Open it in [Claude Code](https://claude.com/claude-code), then work through
`brain/` first. Building the Brain before you generate anything is the whole point.
Skipping to `loops/` gets you the same generic output you already have.

## The Autonomy Ladder

Every agent in this repo is tagged L1 to L4, because "AI agent" on its own tells you
nothing about who is still doing the work.

| Level | Name | What it means | Human role |
|---|---|---|---|
| **L1** | Suggests | Surfaces options, ranks, flags. Decides nothing. | Decides everything |
| **L2** | Drafts | Produces the artifact. Never publishes. | Edits and ships |
| **L3** | Ships with approval | Publishes on a click. Human is a gate, not an editor. | Approves |
| **L4** | Autonomous | Runs unattended inside defined bounds. | Audits the log |

**Two thirds of marketing work is suggest or draft.** Most vendors imply L4. See
[`AUTONOMY.md`](AUTONOMY.md) for every agent scored, with the method, so you can
check it rather than take our word for it.

## What is not here

The orchestration layer that runs these on a schedule, picks the next move and drives
it to the APPROVE gate. The review layer above the gates. Those are what SuperMarketers
runs for clients, and keeping them out is deliberate rather than coy: this repo is
useful on its own and does not depend on them.

Also not here, on purpose: any scraper. Extraction is commodity and it will get your
account restricted. The judgment on top of the data is the only part worth owning, so
that is the part we publish. See `loops/sm-demand/`.

## Where does it break for you?

Capture, Build, Approve, Ship, or Improve. Tell us which and we will tell you what we would do
first: [supermarketers.ai](https://www.supermarketers.ai)

## License

[MIT](LICENSE). Use it, fork it, run it for your own brand or your clients.

Built by [Gen Furukawa](https://www.linkedin.com/in/genfurukawa) at SuperMarketers.
Operators, not an agency.
