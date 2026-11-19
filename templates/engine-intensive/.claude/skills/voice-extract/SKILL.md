---
name: voice-extract
description: Derive 6 to 10 voice rules from the writing samples in inputs/writing/, and split them into grep tests and model-checked rules. Use on Day 1.
---

Full method: `docs/capture/voice-extract.md` in this repo. Summary:

1. Read every sample. Note what the best ones do repeatedly: sentence length, how they open, how they use numbers, what they never say.
2. Write 6 to 10 rules. Each rule must quote one line from a sample that shows it (`source: <file>`).
3. Put the rules a grep can check (banned words and phrases, punctuation) in `voice/banned.txt`, one phrase per line.
4. Put the rest in `voice/rules.md`, each with a pass example and a fail example.
