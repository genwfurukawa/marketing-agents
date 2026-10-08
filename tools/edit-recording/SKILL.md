---
name: edit-recording
version: 0.1.0
description: |
  Edit a raw recording (OBS, Loom, phone, Riverside) into a publishable cut without
  Descript: chunked local Whisper transcript with tight word timings, Claude picks retakes
  and false starts from the transcript, audio-based pause shrinking and filler removal,
  ffmpeg render with denoise and -14 LUFS loudness, self-verification by re-transcribing
  the output, then optional word-synced captions and overlays in HyperFrames. Use when
  asked to "edit this recording", "cut my OBS video", "clean up this take", "remove the
  ums and retakes", "rough cut this", or invoked as /edit-recording.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Agent
  - AskUserQuestion
---

# /edit-recording: raw recording in, clean cut out

Text-based editing the way Descript does it, run locally. The transcript decides **what**
gets said; the audio decides **where** to cut. Whisper's word timestamps drift by seconds
over long stretches, so every cut point is snapped to a measured silence or the quietest
20ms frame between words, never placed on a raw Whisper timestamp.

Everything mechanical lives in `scripts/edit.py` (stdlib Python, no installs):

| Step | Command | Output |
|---|---|---|
| transcribe | `edit.py transcribe SRC --out transcript.json` | `transcript.json` (word-level, ids `w0…`) + `transcript.txt` (one line per speech chunk, readable) |
| plan | `edit.py plan transcript.json --video SRC [--removals removals.json] --out-dir .` | `keep.json` (segments), `cuts.md` (review doc), `transcript.cut.json` (words remapped to the cut timeline) |
| render | `edit.py render SRC keep.json OUT.mp4 [--preview] [--denoise] [--height 1440]` | the cut, loudness-normalized to -14 LUFS |
| levels | `edit.py levels SRC --at 141.6 --span 0.3` | 20ms energy frames around a time, to check a cut |

Brand enforcement lives in `scripts/brand.py` (Stage 6). It needs PyYAML (`python3 -m pip install pyyaml`).

| Step | Command | What it does |
|---|---|---|
| check | `brand.py check CONFIG.yaml` | validates the client's `visual_style`; diffs it against `source_css` if set |
| install | `brand.py install CONFIG.yaml PROJECT` | copies fonts and logos into the HyperFrames project; writes `brand/brand.css`, `brand/brand.lock.json`, `DESIGN.md` |
| compose | `brand.py compose PROJECT --video cut.mp4 --transcript transcript.cut.json [--name --title --cta --url]` | writes `index.html` plus `compositions/brand-{captions,lower-third,end-card}.html` |
| lint | `brand.py lint PROJECT` | fails on any color, font or logo file not in the brand lock |

`ffmpeg`, `ffprobe`, `whisper-cli` and `node` must be on PATH in every Bash call. On macOS
with Homebrew, prepend `/opt/homebrew/bin` if the shell doesn't have it. Set the script paths
once (adjust if the skill is installed somewhere else):

```bash
E=~/.claude/skills/edit-recording/scripts/edit.py
B=~/.claude/skills/edit-recording/scripts/brand.py
```

## Stage 0: Intake

- **Source file** (required). Default OBS output is `~/Movies/YYYY-MM-DD HH-MM-SS.mkv|mov`.
  If the user says "my latest recording", take the newest video in `~/Movies`.
  Don't copy the source; reference it by path. Raw files are big.
- **Workspace:** `videos/<YYYY-MM-DD>-<slug>/` in the cwd. All outputs go there.
- `ffprobe` the source. If it has more than one audio stream (OBS multi-track), ask which
  is the mic and pass `--audio-track N` to every command. If the mic and desktop audio are
  on the same track, say so: filler and pause detection will be noisier.
- **Whose brand** (required whenever the video gets captions, a lower third or an end
  card). That means the path to the brand's `config.yaml` with a `visual_style` block
  (`examples/acme-brand/config.yaml` is a working example). Run `brand.py check` on it now, before any editing. If it fails, stop and report what's
  missing (Stage 6 says how to onboard a brand). Never fall back to a default look.
- Ask only what's missing: **target** (YouTube master 1440p / LinkedIn feed / short),
  **captions** (burned-in or none), **how aggressive** (default: cut retakes, false starts,
  ums, and pauses over 0.45s; keep tangents unless the user says otherwise).

## Stage 1: Transcribe

```bash
python3 $E transcribe "$SRC" --out transcript.json --vocab "<product names, company names, guest names>"
```

Uses `~/.cache/hyperframes/whisper/models/ggml-medium.en.bin` by default (the README shows
how to download it once). Non-English:
pass `--model` pointing at a multilingual model (no `.en`) and `--language <code>`.
Speed on an M2 Pro: about 1:45 per 4 minutes of audio with the filler pass, so roughly
25 minutes for an hour of footage. Run long sources with `run_in_background`.
`--no-fillers` halves the time.

How it works, so you can debug it:
- An energy VAD (adaptive to the recording's noise floor) finds speech. Audio is split at
  pauses into chunks of 6s or less, and each chunk is transcribed separately. Whisper over a
  long file drifts by seconds, but per chunk it stays within about 0.1s. Words are then
  rescaled into the measured speech span of their chunk.
- `--vocab` spells names right ("Claude", not "cloud"). When audio is unclear, Whisper
  sometimes echoes the prompt back as speech. Those chunks are detected and redone without it.
- Whisper drops um/uh unless prompted with them, but that prompt also makes it invent
  fillers in silence. So a second pass runs with a filler prompt, and only fillers that
  align *between two words the clean pass agrees on* are kept.

It prints the VAD levels (`floor_db`, `loud_db`, `threshold_db`). Sanity-check them: if
the range between floor and loud is under ~12 dB the mic is buried in noise, so run the
render with `--denoise` and expect more "unworded sounds" in the plan.

**Word ids (`w0`, `w1`…) belong to one transcript.** Re-transcribing renumbers them. If
you re-run `transcribe`, rewrite `removals.json` from the new transcript.

## Stage 2: Decide what to cut (the judgment step)

Read `transcript.txt` end to end. Each line is a speech chunk with its timestamp and the id
of its first word; open `transcript.json` for the exact ids of a span. Write
`removals.json`:

```json
[
  {"from": "w112", "to": "w140", "reason": "retake"},
  {"from": "w301", "to": "w305", "reason": "false start"},
  {"start": 412.0, "end": 431.5, "reason": "off-topic, user asked to drop"}
]
```

What to remove:

- **Retakes.** The same sentence said two or more times. Keep the **last complete** take
  unless an earlier one is clearly more complete. Remove the earlier attempts whole, from
  their first word to their last.
- **Spoken markers.** "scratch that", "let me redo that", "cut", "one more time", a count-in.
  Remove the marker *and* the flubbed attempt before it.
- **False starts.** "So the... so the way this works" → remove "So the...".
- **Mid-sentence restarts** where the speaker abandons a clause and rephrases.

What NOT to remove without asking: tangents, jokes, anything that changes the meaning or
drops a claim, and repeated phrases that are rhetorical ("it's fast, really fast"). When a
span is ambiguous, leave it in and list it for the user in Stage 3.

Filler words (um, uh, erm…) are cut automatically, but conservatively. An "uh" lasts
0.1–0.3s and Whisper's timing is about ±0.1s, so a filler is cut only if there's a quiet
frame on both sides and the cut passes the coverage check. Otherwise it's **left in** and
listed under "Left in" in `cuts.md`. Fillers glued to the next word usually
end up there. That's deliberate: a missed "uh" is better than a clipped word. `plan` also
lists **sounds with no transcribed word**, which are usually a breath, a cough or a
keyboard. These are kept. Add any the user wants gone to `removals.json` as `{start, end}`.

## Stage 3: Plan and approval gate

```bash
python3 $E plan transcript.json --video "$SRC" --removals removals.json --out-dir .
```

`cuts.md` ends with a **coverage check**. It measures how much of every kept word lies
inside the keep segments, and how much of every removed word lies outside them. It must
read `0 kept words clipped, 0 removed words leaking through`. If a retake edge clips or
leaks, widen or narrow that span by one word and re-plan.

Tunables (defaults are right for talking-head): `--max-pause 0.45` (pauses longer than this
get shrunk), `--keep-pause 0.25` (what they shrink to), `--pad 0.08` (silence kept at a hard
cut), `--tolerance 0.08` (how far a cut edge may stray past Whisper's word boundary). For screen recordings where the speaker pauses to let the screen catch up, raise
`--max-pause` to 0.8 and `--keep-pause` to 0.5.

Show the user `cuts.md` in summary: old and new duration, counts by reason, every retake
with its struck-through text, and anything you left in because it was ambiguous. Then ask
with `AskUserQuestion` before rendering the final cut: approve, adjust aggressiveness, or
restore specific spans. This is the step where you replace Descript's timeline, so keep it
readable and don't skip it.

## Stage 4: Preview render and self-verify

```bash
python3 $E render "$SRC" keep.json preview.mp4 --preview      # 720p, ~16s per 4 min
python3 $E transcribe preview.mp4 --out verify.json --no-fillers --vocab "<same vocab>"
```

The coverage check trusts Whisper's word times. This second check trusts the audio, so
both are needed. For **every removed span and every retake boundary**, find the
neighbouring text in `verify.txt` (use `keep.json` `out` times to locate it):

- **A removed phrase that still appears** means a cut edge is wrong. Widen that span in
  `removals.json` by one word.
- **The first or last word next to a cut is missing** ("Desktop. Generating the…" where
  the source said "It's generating…") means a soft onset got clipped. Check the audio:
  `python3 $E levels "$SRC" --at <source seconds> --span 0.3` prints every 20ms frame.
  Speech that starts before the keep segment does is real clipping. Widen the gap in
  `removals.json` or raise `--pad`.
- **A stray word right at a cut** ("Test this is…", "Yes, this is…") is often Whisper
  misreading an abrupt start, not leftover audio. Check with `levels`. If the cut sits in a
  dip near `floor_db`, it's clean. Flag it for the user to listen to rather than "fixing" it.
- Ignore whole-transcript diff noise ("etc" vs "et cetera", "3" vs "three", dropped words
  away from any cut). Whisper isn't deterministic across different audio.

For screen recordings, also pull a frame on each side of every cut
(`ffmpeg -ss <t> -frames:v 1`) at the `out` times in `keep.json`, and check for jarring
jumps such as a dialog vanishing or the cursor teleporting mid-click. A jump cut on a face
is normal. On a screen it can confuse the viewer, so mention any bad ones.

Hand the user `preview.mp4` to watch. You can't judge pacing or delivery by ear. Say that
plainly and ask for timestamped notes ("cut 2:14–2:20", "the jump at 3:05 is too abrupt").
Apply the notes to `removals.json`, re-plan, and re-render the preview.

## Stage 5: Final render

```bash
python3 $E render "$SRC" keep.json cut.mp4 --height 1440 [--denoise]
```

Defaults: x264 CRF 18, AAC 192k, highpass 80 Hz, loudnorm -14 LUFS / -1.5 dBTP (YouTube
and LinkedIn targets). Render measures the result and re-normalizes the audio in a second
linear pass. Expect -14 ± 0.7 LUFS, because the true-peak ceiling can hold dynamic speech
slightly under. Verify with
`ffmpeg -i cut.mp4 -af ebur128=peak=true:framelog=quiet -f null - 2>&1 | grep -E '^\s+(I|Peak):'`.
Render speed: about 30s per 4 minutes at source resolution.
For a noisy room, `--denoise` (afftdn) helps. For heavy noise, suggest running the audio
through Adobe Podcast Enhance (free, browser) and say it's a manual step.

## Stage 6: Branded captions and overlays

Every brand element is generated from the client's `config.yaml` → `visual_style`. Nothing
is styled by hand, and the render doesn't start until the brand lint passes.

```bash
npx hyperframes init <slug> --non-interactive            # empty project in the workspace
python3 $B install "$CONFIG" <slug>                      # fonts, logos, brand.css, lock, DESIGN.md
python3 $B compose <slug> --video cut.mp4 --transcript transcript.cut.json \
    --name "Jane Doe" --title "Founder, Acme Analytics"   # omit --name for no lower third
python3 $B lint <slug>                                   # brand gate: must PASS
(cd <slug> && npx hyperframes lint)                      # framework gate: 0 errors
(cd <slug> && npx hyperframes render --quality draft --output draft.mp4)
```

`compose` writes the logo bug and a host `index.html`, plus one sub-composition each for
captions (word-synced, active word on the brand highlight), the lower third and the end card
(logo, CTA button, URL). `--cta` and `--url` override the config's end card. `--no-captions`
and `--no-end-card` turn those off. Portrait sources get a 1080x1920 canvas automatically.

Two things depend on the footage, so check them per video:
- **Logo contrast.** `--logo-variant auto` (the default) measures brightness under the logo
  bug and uses the on-light logo over bright footage (a white logo vanished on a cream
  screen recording in testing). It prints the choice and the measured luma.
- **Facecam and UI collisions.** Screen recordings with a picture-in-picture facecam need
  `--caption-region 0,0.66` (captions centered in the left two-thirds) or similar. Look at
  the first frames before composing to see where the facecam sits.

**Adding anything beyond the generated elements** (title cards, zooms, callouts): invoke the
`hyperframes` skill. It reads the generated `DESIGN.md`. Style new elements **only** with the
variables in `brand/brand.css` (`var(--brand-accent)`, `var(--font-display)`, `var(--c-<palette name>)`),
and take logos from `brand/logos/`. Then re-run `brand.py lint`. It rejects raw hex, rgb(),
named colors, fonts and logo files outside the brand, and any edited logo file.

**Spot-check the draft** at the lower third (~3s), a few caption moments, and the end card
(`ffmpeg -ss <t> -i draft.mp4 -frames:v 1 f.png`, then Read the PNG). Look at what the lint
can't see: contrast against the footage, captions clear of on-screen UI, logo legibility.

### Onboarding a brand

`visual_style` in the brand's `config.yaml` is the single store for visual brand. If you
also use marketing-agents' `scripts/image/brand_image_generator.py`, it reads the
`colors`/`logos`/`brand_font` keys from the same block, and video reads the rest. Don't create
a separate brand file. To onboard a brand:

1. Get the real assets: logo SVGs (on-dark and on-light), font files (`.woff2`; Google
   Fonts are free to download), and the site's CSS tokens if they have them.
2. Copy `examples/acme-brand/config.yaml` as the schema and fill
   in `palette` (every color, named), `roles` (which palette name plays bg / surface / text /
   accent / highlight / border…), `fonts` (with file paths), `logo_files`, `shape`, `video`.
   Point `source_css` at their stylesheet if you have it, so drift is caught.
3. Set the legacy `colors` keys to palette values (the image generator reads them).
4. `brand.py check` until it PASSes. Draft their `video` rules from their site and get the
   client to sign off once. After that, every video applies the same rules.

## Stage 7: Hand-off

Report the source and cut durations, what was removed by category, anything left in on
purpose, the final file path, and its loudness. Offer the follow-ons that apply: a title,
description and chapters drafted from `transcript.cut.json`, and a `.vtt` caption file
built from the same words for YouTube.

## Recording tips to give the user (once, if they ask how to record for this)

- OBS: record MKV (crash-safe), remux to MP4 after; mic on its own audio track; 48 kHz.
- Flub a line? Pause, say "scratch that", and redo the whole sentence. The marker makes the
  retake unambiguous in the transcript.
- Leave a one-second pause between takes. Cuts land in silence and come out clean.

## Known limits

- Can't hear delivery. Choosing between two complete takes on tone needs the user.
- Mic bleed (music, desktop audio on the mic track) raises the VAD floor, so pauses and
  unworded sounds get detected less reliably.
- Only one source file. For multi-cam or separate audio, sync and mux first.
