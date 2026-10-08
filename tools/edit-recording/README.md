# edit-recording

A Claude Code skill that edits a raw recording into a publishable video, using free tools
that run on your own machine. It replaces the parts of Descript most people actually use:
cutting a video by editing its transcript, removing retakes and long pauses, and adding
captions.

You record (OBS, Loom, a phone, anything that makes a video file), then tell Claude Code
"edit my latest recording." It will:

1. Transcribe the recording locally with Whisper, with a timestamp on every word.
2. Read the transcript and list every retake, false start and "scratch that" to cut,
   keeping the last complete take of each sentence.
3. Show you a cut list with every removed phrase struck through, and wait for your approval.
4. Render a fast preview with ffmpeg, re-transcribe it, and check that nothing it meant to
   cut survived and nothing it meant to keep got clipped.
5. Optionally add word-by-word captions, a lower third, a logo and an end card with
   HyperFrames, generated from your brand settings, and refuse to render if anything is
   off-brand.
6. Render a final master with the audio set to -14 LUFS for YouTube and LinkedIn.

Loop stage: SHIP. Autonomy Ladder: **L2 (Drafts)**. It drafts the cut and checks it, and a
human approves the cut list and watches the preview before anything is final.

The transcript decides **what** gets said and the audio decides **where** to cut. Whisper's
word timestamps can drift by seconds, so every cut lands in a measured silence or the quietest
moment between two words, never on a raw Whisper timestamp.

## What you need

| Tool | Why | Install (macOS) |
|---|---|---|
| [Claude Code](https://docs.claude.com/en/docs/claude-code) | Runs the skill: reads the transcript, decides the cuts, runs everything else | See the Claude Code docs |
| [ffmpeg](https://ffmpeg.org) | Cuts, audio cleanup, loudness, rendering | `brew install ffmpeg` |
| [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | Local speech-to-text with word timestamps | `brew install whisper-cpp` |
| A Whisper model | The speech recognition weights (about 1.5 GB) | see below |
| Python 3 + PyYAML | The scripts (standard library only, plus PyYAML for brand configs) | `python3 -m pip install pyyaml` |
| Node.js 22+ | Only for captions and overlays ([HyperFrames](https://hyperframes.heygen.com)) | `brew install node` |

Download the Whisper model once:

```bash
mkdir -p ~/.cache/hyperframes/whisper/models
curl -L -o ~/.cache/hyperframes/whisper/models/ggml-medium.en.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-medium.en.bin
```

For non-English recordings, download `ggml-medium.bin` instead and pass
`--model <path> --language <code>` to `transcribe`.

## Install the skill

```bash
git clone https://github.com/genwfurukawa/marketing-agents.git
mkdir -p ~/.claude/skills
cp -R marketing-agents/tools/edit-recording ~/.claude/skills/edit-recording
```

Then in Claude Code, run `/edit-recording` or just ask it to edit a recording.

## Try the brand layer

`examples/acme-brand/config.yaml` is a complete demo brand (palette, color roles, fonts,
logos, caption and end-card rules). Check it:

```bash
python3 ~/.claude/skills/edit-recording/scripts/brand.py check \
  ~/.claude/skills/edit-recording/examples/acme-brand/config.yaml
```

To use your own brand, copy that file next to your own assets and replace the values. If you
have a website stylesheet, set `source_css` and the check will fail whenever the config
drifts from the site.

## Use the scripts without Claude Code

Everything mechanical is a plain command, so you can run it by hand or from another agent:

```bash
E=scripts/edit.py; B=scripts/brand.py
python3 $E transcribe raw.mp4 --out transcript.json --vocab "Acme, Jane Doe"
# write removals.json from transcript.txt: [{"from": "w12", "to": "w40", "reason": "retake"}]
python3 $E plan transcript.json --video raw.mp4 --removals removals.json --out-dir .
python3 $E render raw.mp4 keep.json preview.mp4 --preview
python3 $E render raw.mp4 keep.json cut.mp4 --height 1440

npx hyperframes init branded --non-interactive
python3 $B install examples/acme-brand/config.yaml branded
python3 $B compose branded --video cut.mp4 --transcript transcript.cut.json --name "Jane Doe"
python3 $B lint branded && (cd branded && npx hyperframes render --output final.mp4)
```

`SKILL.md` documents every stage, flag and failure mode in detail.

## What it can't do

- It can't hear delivery. It knows you said a sentence twice, not which take sounded better.
  When two complete takes differ only in tone, it asks.
- It can't feel pacing. You watch the preview once and give notes with timestamps.
- Filler removal is conservative on purpose. An "um" that runs straight into the next word
  is left in and listed, because cutting it would clip a real word.
- No Studio Sound-style audio repair, eye-contact correction or voice cloning. Light noise
  reduction is built in (`--denoise`).
- One source file per edit. Sync and mux multi-camera or separate audio first.

## License

MIT, like the rest of this repository. The demo brand ships the Inter typeface under the SIL
Open Font License (`examples/acme-brand/fonts/Inter-OFL.txt`).
