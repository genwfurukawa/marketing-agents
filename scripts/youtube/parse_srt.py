#!/usr/bin/env python3
"""
SRT parser for YouTube chapter extraction.

Parses Descript SRT export format into a flat list of caption cues.
Also provides chapter candidate extraction with configurable gap thresholds.

Usage (standalone):
    python scripts/youtube/parse_srt.py transcript.srt --min-gap 90

Usage (as module):
    from scripts.youtube.parse_srt import parse_srt, extract_chapter_candidates
"""

import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class SRTCue:
    index: int
    start_seconds: float
    end_seconds: float
    text: str


def timecode_to_seconds(tc: str) -> float:
    """
    Convert SRT timecode 'HH:MM:SS,mmm' to float seconds.

    Args:
        tc: Timecode string like '00:01:23,456'

    Returns:
        Total seconds as float
    """
    tc = tc.replace(",", ".")
    parts = tc.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = float(parts[2])
    return hours * 3600 + minutes * 60 + seconds


def seconds_to_display(seconds: float) -> str:
    """
    Convert seconds to YouTube chapter display format.

    Under 1 hour: 'M:SS' or 'MM:SS'
    Over 1 hour:  'H:MM:SS'

    Args:
        seconds: Total seconds

    Returns:
        Display string like '1:45' or '1:23:45'
    """
    total = int(seconds)
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


def parse_srt(srt_path: Path) -> List[SRTCue]:
    """
    Parse an SRT or VTT file into a list of SRTCue objects.

    Handles both SRT and WebVTT formats (Descript, Zoom, etc.):
        SRT: 00:00:00,000 --> 00:00:04,500
        VTT: 00:00:00.000 --> 00:00:04.500

    Also strips speaker prefixes (e.g., "Speaker Name: text").

    Args:
        srt_path: Path to .srt or .vtt file

    Returns:
        List of SRTCue objects, sorted by start time

    Raises:
        FileNotFoundError: If srt_path does not exist
        ValueError: If file is not valid SRT format
    """
    srt_path = Path(srt_path)
    if not srt_path.exists():
        raise FileNotFoundError(f"SRT file not found: {srt_path}")

    # Read with UTF-8 BOM handling
    content = srt_path.read_text(encoding="utf-8-sig")

    # Normalize line endings
    content = content.replace("\r\n", "\n").replace("\r", "\n")

    # Split into blocks
    blocks = re.split(r"\n\n+", content.strip())

    cues = []
    timecode_pattern = re.compile(
        r"(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})"
    )

    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 2:
            continue

        # Find the timecode line (may be line 1 or line 2)
        tc_match = None
        tc_line_idx = -1
        for i, line in enumerate(lines):
            tc_match = timecode_pattern.search(line)
            if tc_match:
                tc_line_idx = i
                break

        if not tc_match:
            continue

        # Index is everything before the timecode line (usually just "1", "2", etc.)
        try:
            index = int(lines[0].strip()) if tc_line_idx > 0 else len(cues) + 1
        except ValueError:
            index = len(cues) + 1

        start_seconds = timecode_to_seconds(tc_match.group(1))
        end_seconds = timecode_to_seconds(tc_match.group(2))

        # Text is everything after the timecode line
        text_lines = lines[tc_line_idx + 1:]
        text = " ".join(text_lines).strip()

        # Strip HTML tags Descript sometimes adds
        text = re.sub(r"<[^>]+>", "", text)

        # Strip speaker prefix from VTT/Zoom format (e.g., "Speaker Name: text")
        text = re.sub(r"^[A-Za-z\s]+:\s*", "", text)

        if text:
            cues.append(SRTCue(
                index=index,
                start_seconds=start_seconds,
                end_seconds=end_seconds,
                text=text,
            ))

    if len(cues) < 3:
        raise ValueError(
            f"Only {len(cues)} cues found in {srt_path}. "
            "Expected at least 3. Is this a valid SRT file?"
        )

    cues.sort(key=lambda c: c.start_seconds)
    return cues


def extract_chapter_candidates(
    cues: List[SRTCue],
    min_gap_seconds: int = 90,
) -> List[dict]:
    """
    Extract chapter candidate timestamps from SRT cues.

    Strategy: Take the start of the first cue (always 0:00), then walk
    forward and emit a new candidate only when we are at least min_gap_seconds
    past the last emitted candidate. Each candidate includes surrounding text
    context so Claude can name the chapter.

    Args:
        cues: Parsed SRT cues from parse_srt()
        min_gap_seconds: Minimum seconds between chapter candidates (default 90)

    Returns:
        List of dicts: [{"timecode": "0:00", "timecode_seconds": 0, "text_context": "..."}]

    Raises:
        ValueError: If cues is empty
    """
    if not cues:
        raise ValueError("Cannot extract chapters from empty cue list")

    candidates = []
    last_emitted = -min_gap_seconds  # Ensures first cue is always emitted

    for i, cue in enumerate(cues):
        if cue.start_seconds - last_emitted >= min_gap_seconds:
            # Gather text context: this cue + next 2 cues
            context_cues = cues[i:i + 3]
            text_context = " ".join(c.text for c in context_cues)

            candidates.append({
                "timecode": seconds_to_display(cue.start_seconds),
                "timecode_seconds": int(cue.start_seconds),
                "text_context": text_context[:300],  # Cap at 300 chars
            })
            last_emitted = cue.start_seconds

    # Ensure first chapter is always 0:00
    if candidates and candidates[0]["timecode_seconds"] != 0:
        first_context = " ".join(c.text for c in cues[:3])
        candidates.insert(0, {
            "timecode": "0:00",
            "timecode_seconds": 0,
            "text_context": first_context[:300],
        })

    return candidates


def get_transcript_text(cues: List[SRTCue]) -> str:
    """
    Join all SRT cue text into a single clean transcript string.

    Args:
        cues: Parsed SRT cues

    Returns:
        Full transcript as a single string with spaces between cues
    """
    return " ".join(cue.text.strip() for cue in cues)


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Parse SRT file and extract chapter candidates")
    parser.add_argument("srt_file", type=Path, help="Path to SRT file")
    parser.add_argument("--min-gap", type=int, default=90, help="Minimum gap between chapters in seconds")
    parser.add_argument("--format", choices=["chapters", "full", "text"], default="chapters",
                        help="Output format: chapters (default), full (all cues), text (plain transcript)")
    args = parser.parse_args()

    cues = parse_srt(args.srt_file)

    if args.format == "text":
        print(get_transcript_text(cues))
    elif args.format == "full":
        for cue in cues:
            print(f"[{seconds_to_display(cue.start_seconds)}] {cue.text}")
    else:
        candidates = extract_chapter_candidates(cues, min_gap_seconds=args.min_gap)
        print(json.dumps(candidates, indent=2))
        print(f"\n{len(candidates)} chapter candidates extracted from {len(cues)} cues")
