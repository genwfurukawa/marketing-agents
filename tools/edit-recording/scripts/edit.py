#!/usr/bin/env python3
"""Transcript-driven rough cut for a single-camera recording (OBS, Loom, phone).

Subcommands:
  transcribe  video -> transcript.json (word-level, chunked at pauses so timings stay tight)
  plan    transcript.json [+ removals.json] -> keep.json, cuts.md, transcript.cut.json
  render  keep.json + source video -> cut video (audio cleaned + loudness-normalized)

Stdlib only. Needs ffmpeg/ffprobe and whisper-cli (whisper.cpp) on PATH.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_PROMPT = ""
# Whisper drops disfluencies unless prompted with them, but the prompt also makes it invent
# fillers in silence. So fillers come from a second pass and are kept only where they align
# between two words the clean pass agrees on.
FILLER_PROMPT = "Um, so, uh, I was like, um, you know, uh, I mean, hmm."
HALLUCINATIONS = {"you", "thankyou", "thanks", "bye", "thanksforwatching", "okay"}
FILLERS = re.compile(r"^(um+|uh+|uhm+|umm+|erm+|er|ah+|hmm+|mm+|eh)$", re.I)


def norm(text):
    return re.sub(r"[^\w']", "", text).lower()


def probe(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=index,codec_type,r_frame_rate,width,height:format=duration",
         "-of", "json", str(path)],
        check=True, capture_output=True, text=True).stdout
    info = json.loads(out)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    audio = [s for s in info["streams"] if s["codec_type"] == "audio"]
    num, den = video["r_frame_rate"].split("/")
    return {
        "duration": float(info["format"]["duration"]),
        "fps": round(float(num) / float(den), 3),
        "width": video["width"], "height": video["height"],
        "audio_tracks": len(audio),
    }


def load_removals(path, words):
    """removals.json: [{"from": "w12", "to": "w40", "reason": "retake"}]
    or [{"start": 61.2, "end": 75.0, "reason": "..."}]. Returns (start, end, reason)."""
    if not path:
        return []
    by_id = {w["id"]: w for w in words}
    out = []
    for r in json.loads(Path(path).read_text()):
        if "from" in r:
            a, b = by_id[r["from"]], by_id[r.get("to", r["from"])]
            out.append((a["start"], b["end"], r.get("reason", "manual")))
        else:
            out.append((float(r["start"]), float(r["end"]), r.get("reason", "manual")))
    return out


def fmt(t):
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def speech_map(video, audio_track=0, win=0.02):
    """Energy VAD from ffmpeg astats. Returns (speech_runs, silence_runs) in seconds.
    Threshold adapts to the recording: floor (10th pct) + 30% of the floor->loud range."""
    n = int(16000 * win)
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
         "-map", f"0:a:{audio_track}", "-af",
         f"pan=mono|c0=0.5*c0+0.5*c1,aresample=16000,asetnsamples=n={n}:p=0,astats=metadata=1:reset=1,"
         "ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-",
         "-f", "null", "-"], check=True, capture_output=True, text=True).stdout
    db = []
    for line in out.splitlines():
        if line.startswith("lavfi."):
            v = line.split("=", 1)[1]
            db.append(-120.0 if "inf" in v else float(v))
    # smooth over ~100ms (power domain) so single noisy frames don't flip state
    pw = [10 ** (d / 10) for d in db]
    k = 5
    sm = []
    for i in range(len(pw)):
        lo, hi = max(0, i - k // 2), min(len(pw), i + k // 2 + 1)
        sm.append(10 * __import__("math").log10(max(sum(pw[lo:hi]) / (hi - lo), 1e-12)))
    srt = sorted(sm)
    floor, loud = srt[len(srt) // 5], srt[int(len(srt) * 0.95)]
    rng = max(loud - floor, 12.0)
    hi_thr, lo_thr = floor + 0.4 * rng, floor + 0.2 * rng
    thr = hi_thr
    runs, cur = [], None
    for i, d in enumerate(sm):  # hysteresis: enter above hi_thr, leave below lo_thr
        if cur is None and d > hi_thr:
            cur = [i * win, (i + 1) * win]
        elif cur is not None and d > lo_thr:
            cur[1] = (i + 1) * win
        elif cur is not None:
            runs.append(cur); cur = None
    if cur:
        runs.append(cur)
    merged = []
    for r in runs:  # bridge consonant dips
        if merged and r[0] - merged[-1][1] < 0.12:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    speech = [r for r in merged if r[1] - r[0] >= 0.15]  # drop clicks and bumps
    # hysteresis misses soft onsets ("It's" starting on a breathy vowel) and trailing
    # consonants; grow each run outward while raw frames stay clearly above the floor
    edge_thr, reach = floor + 4.0, int(0.3 / win)

    def grow(i, step):
        # walk outward; tolerate up to 2 quiet frames (40ms) between onset bursts
        best, quiet = i, 0
        for n in range(1, reach + 1):
            j = i + step * n
            if j < 0 or j >= len(db):
                break
            if db[j] > edge_thr:
                best, quiet = j, 0
            else:
                quiet += 1
                if quiet > 2:
                    break
        return best

    for r in speech:
        r[0] = grow(int(r[0] / win), -1) * win
        r[1] = (grow(int(r[1] / win) - 1, 1) + 1) * win
    for a_, b_ in zip(speech, speech[1:]):
        a_[1] = min(a_[1], b_[0])
    total = len(db) * win
    silence, t = [], 0.0
    for s, e in speech:
        if s > t:
            silence.append([t, s])
        t = e
    if t < total:
        silence.append([t, total])
    levels = {"floor_db": round(floor, 1), "loud_db": round(loud, 1), "threshold_db": round(hi_thr, 1),
              "frames": db, "win": win}
    return speech, silence, levels


def transcribe(args):
    """Whisper over one long file spreads word timings across pauses (seconds of drift).
    Instead: split at pauses from the energy VAD, transcribe each chunk in one
    whisper-cli run (model loads once), and offset words back to source time."""
    import shutil
    import tempfile
    model = Path(args.model).expanduser()
    if not model.exists():
        sys.exit(f"missing whisper model {model}; run `npx hyperframes transcribe <any.wav> "
                 f"--model medium.en` once to download it, or pass --model")
    speech, _, levels = speech_map(args.video, args.audio_track)
    db, win = levels.pop("frames"), levels.pop("win")

    def split_long(s, e):
        # whisper.cpp timestamps run off the end of long chunks; split at the quietest frame
        if e - s <= args.max_chunk:
            return [[s, e]]
        lo, hi = int((s + 1.0) / win), int((e - 1.0) / win)
        i = min(range(lo, hi), key=lambda j: db[j])
        return split_long(s, i * win) + split_long((i + 1) * win, e)

    chunks = []
    for s0, e0 in speech:
        for s, e in split_long(s0, e0):
            if chunks and s - chunks[-1][1] < args.split_gap and e - chunks[-1][0] <= args.max_chunk:
                chunks[-1][1] = e
            else:
                chunks.append([s, e])
    tmp = Path(tempfile.mkdtemp(prefix="er-chunks-"))
    files = []
    for i, (s, e) in enumerate(chunks):
        f = tmp / f"c{i:04d}.wav"
        a = max(0.0, s - 0.1)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{a:.3f}", "-to", f"{e + 0.15:.3f}",
                        "-i", str(args.video), "-map", f"0:a:{args.audio_track}", "-ac", "1",
                        "-ar", "16000", "-af", "adelay=300:all=1,apad=pad_dur=0.5", str(f)], check=True)
        files.append((f, a - 0.3, s, e))  # 300ms of leading silence shifts whisper's zero
    print(f"{len(chunks)} speech chunks, levels {levels}; transcribing with {model.name}", file=sys.stderr)
    prompt = " ".join(x for x in (args.prompt, args.vocab) if x)

    def run_whisper(targets, with_prompt):
        cmd = ["whisper-cli", "-m", str(model), "-l", args.language, "-ml", "1", "-sow", "-oj", "-np"]
        if with_prompt and prompt:
            cmd += ["--prompt", prompt]
        for f, *_ in targets:
            cmd += ["-f", str(f)]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def read_chunk(ci):
        f, offset, s, e = files[ci]
        data = json.loads(Path(f"{f}.json").read_text())
        chunk_words, in_tag = [], False
        for seg in data["transcription"]:
            text = seg["text"].strip()
            if text.startswith(("[", "(")):
                in_tag = True
            if in_tag or not text:  # [BLANK_AUDIO], (lips smacking), (music)
                in_tag = in_tag and not text.endswith(("]", ")"))
                continue
            ws = seg["offsets"]["from"] / 1000 + offset
            we = seg["offsets"]["to"] / 1000 + offset
            if norm(text) == "" and chunk_words:  # bare punctuation: glue onto previous word
                chunk_words[-1]["text"] += text
                continue
            chunk_words.append({"text": text, "start": ws, "end": max(we, ws + 0.02), "chunk": ci})
        # whisper starts early / runs late within a chunk: rescale the chunk's words into the
        # measured speech span instead of clamping (clamping piles words onto the boundary)
        if chunk_words:
            rs, re_ = chunk_words[0]["start"], chunk_words[-1]["end"]
            ns, ne = max(rs, s), min(re_, e)
            k = (ne - ns) / (re_ - rs) if re_ > rs else 1.0
            for w in chunk_words:
                w["start"] = ns + (w["start"] - rs) * k
                w["end"] = ns + (w["end"] - rs) * k
            spread_stacked(chunk_words)
        return chunk_words

    def squash(ws):
        return "".join(norm(w["text"]) for w in ws)

    run_whisper(files, with_prompt=True)
    per_chunk = [read_chunk(ci) for ci in range(len(files))]
    # on unclear audio whisper echoes its prompt back ("n8n, Make.com, Relevance AI.");
    # redo those chunks without the prompt
    pnorm = re.sub(r"[^\w']", "", prompt).lower()
    echoes = [ci for ci, ws in enumerate(per_chunk) if pnorm and len(squash(ws)) > 3 and squash(ws) in pnorm]
    if echoes:
        print(f"{len(echoes)} chunks echoed the prompt; re-transcribing them without it", file=sys.stderr)
        run_whisper([files[ci] for ci in echoes], with_prompt=False)
        for ci in echoes:
            per_chunk[ci] = read_chunk(ci)
    if args.fillers:
        import difflib
        print("filler pass", file=sys.stderr)
        for f, *_ in files:
            Path(f"{f}.json").rename(f"{f}.clean.json")
        saved_prompt = prompt
        prompt = " ".join(x for x in (FILLER_PROMPT, args.vocab) if x)
        run_whisper(files, with_prompt=True)
        prompt = saved_prompt
        added = 0
        for ci, clean in enumerate(per_chunk):
            noisy = read_chunk(ci)
            a = [norm(w["text"]) for w in clean]
            b = [norm(w["text"]) for w in noisy]
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
                if op != "insert" or j2 >= len(b) or not 0 < i1 < len(a):
                    continue  # only fillers strictly between two agreed words
                if not all(FILLERS.match(x) for x in b[j1:j2]):
                    continue
                for w in noisy[j1:j2]:
                    if not 0.08 <= w["end"] - w["start"] <= 1.2:
                        continue
                    prev, nxt = clean[i1 - 1], clean[i1]
                    w["start"], w["end"] = max(w["start"], prev["start"] + 0.05), min(w["end"], nxt["end"] - 0.05)
                    if w["end"] - w["start"] < 0.08:
                        continue
                    prev["end"] = min(prev["end"], w["start"])
                    nxt["start"] = max(nxt["start"], w["end"])
                    w["text"] = w["text"].strip(",. ").lower() + ","
                    clean.append(w)
                    added += 1
            clean.sort(key=lambda w: w["start"])
        print(f"filler pass added {added} um/uh", file=sys.stderr)
    words = []
    for ws in per_chunk:
        # whisper's stock hallucinations on noise: a lone "you" / "thank you" chunk
        if squash(ws) in HALLUCINATIONS:
            continue
        words += ws
    for i, w in enumerate(words):
        w["id"] = f"w{i}"
    out = Path(args.out)
    out.write_text(json.dumps([{"id": w["id"], "text": w["text"], "start": w["start"], "end": w["end"]}
                               for w in words], indent=1))
    # plain-text view for reading: one line per chunk with timestamps and word ids
    lines, cur = [], None
    for w in words:
        if w["chunk"] != cur:
            cur = w["chunk"]
            lines.append(f"\n[{fmt(w['start'])}] ({w['id']}) ")
        lines[-1] += w["text"] + " "
    out.with_suffix(".txt").write_text("".join(lines).strip() + "\n")
    shutil.rmtree(tmp)
    print(f"wrote {out} ({len(words)} words) and {out.with_suffix('.txt')}")


def spread_stacked(ws):
    """whisper sometimes emits a run of zero-length words followed by one word that owns the
    whole span ("set this up with a custom n8n workflow." -> 7 words at 106.47, last ends 109.1).
    Spread each such run across its span, weighted by word length."""
    i = 0
    while i < len(ws):
        j = i
        while j + 1 < len(ws) and ws[j]["end"] - ws[j]["start"] < 0.05:
            j += 1
        if j > i:
            a, b = ws[i]["start"], ws[j]["end"]
            lens = [max(len(norm(w["text"])), 1) for w in ws[i:j + 1]]
            t = a
            for w, n in zip(ws[i:j + 1], lens):
                w["start"] = t
                t += (b - a) * n / sum(lens)
                w["end"] = t
        i = j + 1
    for w in ws:
        w["start"], w["end"] = round(w["start"], 3), round(w["end"], 3)


def subtract(intervals, cuts):
    out = []
    for s, e in intervals:
        pieces = [[s, e]]
        for cs, ce in cuts:
            nxt = []
            for ps, pe in pieces:
                if ce <= ps or cs >= pe:
                    nxt.append([ps, pe]); continue
                if cs > ps:
                    nxt.append([ps, cs])
                if ce < pe:
                    nxt.append([ce, pe])
            pieces = nxt
        out.extend(pieces)
    return out


def snap(lo, hi, silence, vad, side, pad, strict=False):
    """Place a cut edge inside [lo, hi], the gap between a kept word and the removed word
    next to it (widened a little for whisper's timing error), where it can't slice a syllable.
    1. A silence overlapping the gap: cut inside it, `pad` away from the speech we keep.
       side='start' (removal begins) -> just after the preceding kept speech ends;
       side='end' (removal ends) -> just before the following kept speech begins.
    2. Words run together (no silence): the quietest 20ms frame in the gap.
    With strict=True (fillers), return None unless that frame is actually quiet; the
    caller then leaves the word in rather than risk clipping a neighbour."""
    for s, e in silence:
        if e < lo or s > hi:
            continue
        edge = min(s + pad, e) if side == "start" else max(e - pad, s)
        return min(max(edge, lo), hi)
    db, win = vad["frames"], vad["win"]
    js = range(max(0, int(lo / win)), min(len(db), int(hi / win) + 1))
    if not js:
        return None if strict else (lo + hi) / 2
    i = min(js, key=lambda j: db[j])
    if strict and db[i] > vad["quiet"]:
        return None
    return (i + 0.5) * win


def plan(args):
    words = json.loads(Path(args.transcript).read_text())
    for i, w in enumerate(words):
        w.setdefault("id", f"w{i}")
    words = [w for w in words if norm(w["text"])]  # drop ♪, punctuation-only tokens
    info = probe(args.video)
    duration = info["duration"]
    speech, silence, levels = speech_map(args.video, args.audio_track)
    frames = levels.pop("frames"), levels.pop("win")
    removals = load_removals(args.removals, words)

    def removed_reason(w):
        mid = (w["start"] + w["end"]) / 2
        for s, e, why in removals:
            if s <= mid <= e:
                return why
        if not args.keep_fillers and FILLERS.match(norm(w["text"])):
            return "filler"
        return None

    for w in words:
        w["_cut"] = removed_reason(w)

    # contiguous removed-word spans
    spans, cur = [], None
    for i, w in enumerate(words):
        if w["_cut"]:
            if cur and cur["reason"] == w["_cut"] and cur["last"] == i - 1:
                cur["last"] = i
            else:
                cur = {"reason": w["_cut"], "first": i, "last": i}
                spans.append(cur)
        else:
            cur = None
    pad, tol = args.pad, args.tolerance
    vad = {"frames": frames[0], "win": frames[1],
           "quiet": levels["floor_db"] + 0.25 * (levels["loud_db"] - levels["floor_db"])}
    # pauses: shrink every silence longer than max_pause down to keep_pause
    half = args.keep_pause / 2
    pause_cuts = [[s + half, e - half] for s, e in silence if e - s > args.max_pause]

    def skip(sp, why):
        sp["skip"] = why
        for w in words[sp["first"]:sp["last"] + 1]:
            w["_cut"] = None

    def coverage(w):
        span = max(w["end"] - w["start"], 1e-3)
        return sum(max(0.0, min(w["end"], k["end"]) - max(w["start"], k["start"])) for k in keep) / span

    # build, check coverage, revert filler cuts that clip a neighbour or don't remove the
    # filler (whisper timing is ~±0.1s and an "uh" is 0.1-0.3s), rebuild
    for _ in range(4):
        cut_ranges = []
        for sp in spans:
            if sp.get("skip"):
                continue
            a, b = words[sp["first"]], words[sp["last"]]
            prev_end = words[sp["first"] - 1]["end"] if sp["first"] > 0 else a["start"]
            next_start = words[sp["last"] + 1]["start"] if sp["last"] + 1 < len(words) else b["end"]
            strict = sp["reason"] == "filler"
            s = snap(min(prev_end, a["start"]) - tol, a["start"] + tol, silence, vad, "start", pad, strict)
            e = snap(b["end"] - tol, max(next_start, b["end"]) + tol, silence, vad, "end", pad, strict)
            if s is None or e is None or e - s < 0.06:
                skip(sp, "no clean edge to cut on")
                continue
            sp["range"] = (s, e)
            cut_ranges.append([s, e])
        kept_speech = subtract(speech, cut_ranges)
        if not kept_speech:
            sys.exit("nothing left to keep")
        lo = max(0.0, kept_speech[0][0] - args.head)
        hi = min(duration, kept_speech[-1][1] + args.tail)
        segs = [x for x in sorted(subtract([[lo, hi]], cut_ranges + pause_cuts)) if x[1] - x[0] >= 0.1]
        keep, out_t = [], 0.0
        for s, e in segs:
            keep.append({"start": round(s, 3), "end": round(e, 3), "out": round(out_t, 3)})
            out_t += e - s
        new_dur = out_t
        # exact check, no re-transcription noise: kept words must survive, removed words must not
        clipped = [w for w in words if not w["_cut"] and coverage(w) < 0.85]
        leaked = [w for w in words if w["_cut"] and coverage(w) > 0.15]
        bad_ids = {w["id"] for w in clipped + leaked}
        bad = [sp for sp in spans if not sp.get("skip") and sp["reason"] == "filler"
               and any(words[i]["id"] in bad_ids
                       for i in range(max(0, sp["first"] - 1), min(len(words), sp["last"] + 2)))]
        if not bad:
            break
        for sp in bad:
            skip(sp, "cut would clip a neighbouring word")
    uncuttable = [sp for sp in spans if sp.get("skip")]
    spans = [sp for sp in spans if not sp.get("skip")]

    # remap kept words onto the new timeline (for captions); whisper times are
    # approximate, so map by midpoint and clamp to the segment it lands in
    cut_words = []
    for w in words:
        if w["_cut"]:
            continue
        mid = (w["start"] + w["end"]) / 2
        k = next((k for k in keep if k["start"] <= mid <= k["end"]), None)
        if k is None:
            continue
        off = k["out"] - k["start"]
        cut_words.append({"id": w["id"], "text": w["text"],
                          "start": round(max(w["start"], k["start"]) + off, 3),
                          "end": round(min(w["end"], k["end"]) + off, 3)})

    # speech with no transcribed word nearby: likely an um/uh whisper dropped, a cough, a click
    unworded = []
    for s, e in subtract(speech, cut_ranges):
        if not 0.12 <= e - s <= 1.5:
            continue
        if any(w["start"] - 0.15 < e and w["end"] + 0.15 > s for w in words if not w["_cut"]):
            continue
        unworded.append([round(s, 2), round(e, 2)])

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "keep.json").write_text(json.dumps(
        {"source": str(args.video), "source_duration": duration, "cut_duration": round(new_dur, 3),
         "levels": levels, "segments": keep}, indent=1))
    (out / "transcript.cut.json").write_text(json.dumps(cut_words, indent=1))

    tally = {}
    for sp in spans:
        tally[sp["reason"]] = tally.get(sp["reason"], 0) + 1
    paused = sum(e - s for s, e in pause_cuts)
    lines = ["# Cut list\n",
             f"Source {fmt(duration)} -> cut {fmt(new_dur)} "
             f"({100 * (1 - new_dur / duration):.0f}% removed, {len(keep)} segments)\n",
             "Removed: " + (", ".join(f"{n} {r}" for r, n in sorted(tally.items())) or "no speech")
             + f"; {len(pause_cuts)} pauses over {args.max_pause}s shrunk to {args.keep_pause}s "
             f"({paused:.1f}s total)\n",
             f"Audio levels: floor {levels['floor_db']} dB, speech {levels['loud_db']} dB, "
             f"VAD threshold {levels['threshold_db']} dB\n",
             "## Removed speech\n"]
    for sp in spans:
        s, e = sp["range"]
        before = " ".join(x["text"] for x in words[max(0, sp["first"] - 6):sp["first"]])
        after = " ".join(x["text"] for x in words[sp["last"] + 1:sp["last"] + 7])
        cut = " ".join(x["text"] for x in words[sp["first"]:sp["last"] + 1])
        lines.append(f"- **{fmt(s)}–{fmt(e)}** [{sp['reason']}] …{before} ~~{cut}~~ {after}…")
    lines.append("\n## Coverage check\n")
    lines.append(f"{len(clipped)} kept words clipped, {len(leaked)} removed words leaking through.")
    for w in clipped:
        lines.append(f"- clipped: {w['id']} \"{w['text']}\" at {fmt(w['start'])} ({coverage(w):.0%} kept)")
    for w in leaked:
        lines.append(f"- leaked: {w['id']} \"{w['text']}\" at {fmt(w['start'])} ({coverage(w):.0%} kept)")
    if uncuttable:
        lines.append("\n## Left in (reverted automatically; review if they bother you)\n")
        for sp in uncuttable:
            a, b = words[sp["first"]], words[sp["last"]]
            ctx = " ".join(x["text"] for x in words[max(0, sp["first"] - 4):sp["last"] + 5])
            lines.append(f"- {fmt(a['start'])} [{sp['reason']}: {sp['skip']}] "
                         f"{' '.join(x['text'] for x in words[sp['first']:sp['last'] + 1])} …{ctx}…")
    if unworded:
        lines.append("\n## Sounds with no transcribed word (kept; check for dropped um/uh)\n")
        lines += [f"- {fmt(s)}–{fmt(e)}" for s, e in unworded]
    (out / "cuts.md").write_text("\n".join(lines) + "\n")
    print(f"{fmt(duration)} -> {fmt(new_dur)}, {len(keep)} segments, {tally or 'no speech removed'}, "
          f"{len(pause_cuts)} pauses shrunk, {len(unworded)} unworded sounds, "
          f"{len(clipped)} clipped / {len(leaked)} leaked words, {len(uncuttable)} left in; "
          f"wrote {out}/keep.json, cuts.md, transcript.cut.json")


def render(args):
    keep = json.loads(Path(args.keep).read_text())["segments"]
    info = probe(args.video)
    a_in = f"0:a:{args.audio_track}"
    fade = 0.012
    parts, labels = [], []
    for i, k in enumerate(keep):
        d = k["end"] - k["start"]
        parts.append(f"[0:v]trim=start={k['start']}:end={k['end']},setpts=PTS-STARTPTS[v{i}]")
        parts.append(f"[{a_in}]atrim=start={k['start']}:end={k['end']},asetpts=PTS-STARTPTS,"
                     f"afade=t=in:d={fade},afade=t=out:st={max(0, d - fade):.3f}:d={fade}[a{i}]")
        labels.append(f"[v{i}][a{i}]")
    vchain = "null"
    if args.preview:
        vchain = "scale=-2:720"
    elif args.height and args.height != info["height"]:
        vchain = f"scale=-2:{args.height}:flags=lanczos"
    achain = ["highpass=f=80"]
    if args.denoise:
        achain.append("afftdn=nf=-25")
    achain.append("loudnorm=I=-14:TP=-1.5:LRA=11")
    parts.append("".join(labels) + f"concat=n={len(keep)}:v=1:a=1[vc][ac]")
    parts.append(f"[vc]{vchain}[vout]")
    parts.append(f"[ac]{','.join(achain)},aresample=48000[aout]")

    graph = Path(args.out).with_suffix(".filtergraph.txt")
    graph.write_text(";\n".join(parts))
    venc = (["-c:v", "libx264", "-preset", "ultrafast", "-crf", "28"] if args.preview
            else ["-c:v", "libx264", "-preset", "medium", "-crf", str(args.crf)])
    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-stats",
           "-i", str(args.video), "-/filter_complex", str(graph),
           "-map", "[vout]", "-map", "[aout]", *venc,
           "-r", str(info["fps"]), "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(args.out)]
    subprocess.run(cmd, check=True)

    # single-pass loudnorm undershoots on dynamic speech (-16 for a -14 target);
    # measure the result and redo only the audio with linear two-pass normalization
    meas = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(args.out), "-map", "0:a",
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = json.loads(meas[meas.rindex("{"):meas.rindex("}") + 1])
    if abs(float(m["input_i"]) + 14) > 0.5:
        tmp = Path(args.out).with_suffix(".norm.mp4")
        ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
              f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
              f"offset={m['target_offset']}:linear=true,aresample=48000")
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", str(args.out),
                        "-map", "0:v", "-map", "0:a", "-c:v", "copy", "-af", ln,
                        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(tmp)], check=True)
        tmp.replace(args.out)
    graph.unlink(missing_ok=True)
    print(f"wrote {args.out} ({len(keep)} segments)")


def levels(args):
    """Print the 20ms energy frames around a time, to check whether a cut sits in a gap."""
    _, _, lv = speech_map(args.video, args.audio_track)
    db, win = lv["frames"], lv["win"]
    lo, hi = max(0, int((args.at - args.span) / win)), min(len(db), int((args.at + args.span) / win))
    print(f"floor {lv['floor_db']} dB, speech {lv['loud_db']} dB, threshold {lv['threshold_db']} dB")
    for i in range(lo, hi):
        bar = "#" * max(0, int((db[i] - lv["floor_db"] + 6) / 2))
        print(f"{i * win:8.2f} {db[i]:6.1f} {bar}{'  <-- t' if abs(i * win - args.at) < win / 2 else ''}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    tr = sub.add_parser("transcribe")
    tr.add_argument("video")
    tr.add_argument("--out", default="transcript.json")
    tr.add_argument("--audio-track", type=int, default=0)
    tr.add_argument("--model", default="~/.cache/hyperframes/whisper/models/ggml-medium.en.bin")
    tr.add_argument("--language", default="en", help="use a non-.en model for other languages")
    tr.add_argument("--prompt", default=DEFAULT_PROMPT,
                    help="whisper initial prompt: spells names right and coaxes it to keep ums")
    tr.add_argument("--vocab", default="", help="extra names/terms appended to the prompt")
    tr.add_argument("--no-fillers", dest="fillers", action="store_false",
                    help="skip the second whisper pass that finds um/uh (halves transcribe time)")
    tr.add_argument("--split-gap", type=float, default=0.35, help="pause that starts a new chunk")
    tr.add_argument("--max-chunk", type=float, default=6.0)

    pl = sub.add_parser("plan")
    pl.add_argument("transcript")
    pl.add_argument("--video", required=True, help="source recording")
    pl.add_argument("--audio-track", type=int, default=0, help="OBS multi-track: which audio stream")
    pl.add_argument("--removals", help="removals.json written after reading the transcript")
    pl.add_argument("--out-dir", default=".")
    pl.add_argument("--pad", type=float, default=0.08, help="seconds kept inside the silence at a hard cut")
    pl.add_argument("--max-pause", type=float, default=0.45, help="pauses longer than this get shrunk")
    pl.add_argument("--keep-pause", type=float, default=0.25, help="what a long pause shrinks to")
    pl.add_argument("--tolerance", type=float, default=0.08,
                    help="how far a cut edge may stray past whisper's word boundary")
    pl.add_argument("--head", type=float, default=0.3)
    pl.add_argument("--tail", type=float, default=0.6)
    pl.add_argument("--keep-fillers", action="store_true")

    rn = sub.add_parser("render")
    rn.add_argument("video")
    rn.add_argument("keep")
    rn.add_argument("out")
    rn.add_argument("--audio-track", type=int, default=0, help="OBS multi-track: which audio stream")
    rn.add_argument("--denoise", action="store_true")
    rn.add_argument("--preview", action="store_true", help="fast 720p review render")
    rn.add_argument("--height", type=int, help="output height, e.g. 1440")
    rn.add_argument("--crf", type=int, default=18)

    lv = sub.add_parser("levels")
    lv.add_argument("video")
    lv.add_argument("--at", type=float, required=True, help="source time in seconds")
    lv.add_argument("--span", type=float, default=0.5)
    lv.add_argument("--audio-track", type=int, default=0)

    args = p.parse_args()
    {"transcribe": transcribe, "plan": plan, "render": render, "levels": levels}[args.cmd](args)


if __name__ == "__main__":
    main()
