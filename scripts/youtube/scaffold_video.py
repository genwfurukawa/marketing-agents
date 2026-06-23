#!/usr/bin/env python3
"""
YouTube video folder scaffolder.

Creates the standardized folder structure for a new video:
    {client_root}/workflows/youtube/videos/{video-slug}/
        input/
            DROP_FILES_HERE.md
        output/
            .gitkeep

Usage:
    python scripts/youtube/scaffold_video.py \
        --client acme \
        --slug "ai-agents-marketing-2026"

    # Or let the script generate a slug from a title:
    python scripts/youtube/scaffold_video.py \
        --client acme \
        --title "How I replaced my marketing team with AI agents"
"""

import argparse
import json
import re
import sys
from pathlib import Path


def slugify(title: str) -> str:
    """
    Convert a video title to a URL-safe folder slug.

    Rules:
    - Lowercase
    - Replace spaces and special chars with hyphens
    - Collapse multiple hyphens
    - Strip leading/trailing hyphens
    - Max 60 chars

    Args:
        title: Human-readable video title

    Returns:
        URL-safe slug string
    """
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug[:60]


def find_workspace_root() -> Path:
    """Find workspace root by looking for CLAUDE.md marker."""
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "CLAUDE.md").exists():
            return parent
    raise RuntimeError("Cannot find workspace root - CLAUDE.md not found")


def find_client_root(client_slug: str, workspace_root: Path) -> Path:
    """
    Resolve client root path from clients_registry.json.

    Falls back to ../clients/{client_slug}/ if not in registry.

    Args:
        client_slug: Client name (e.g. 'acme')
        workspace_root: Path to the ops repo root

    Returns:
        Resolved absolute Path to client root

    Raises:
        FileNotFoundError: If client path does not exist on disk
    """
    registry_path = workspace_root / "clients_registry.json"

    if registry_path.exists():
        with open(registry_path) as f:
            registry = json.load(f)

        clients = registry.get("clients", {})
        if client_slug in clients:
            client_path = Path(clients[client_slug].get("path", ""))
            if not client_path.is_absolute():
                client_path = (workspace_root / client_path).resolve()
            if client_path.exists():
                return client_path

    # Fallback: default path
    default_base = workspace_root.parent / "clients" / client_slug
    if default_base.exists():
        return default_base

    raise FileNotFoundError(
        f"Client '{client_slug}' not found. Checked:\n"
        f"  - clients_registry.json\n"
        f"  - {default_base}"
    )


def scaffold_video(client_root: Path, video_slug: str) -> Path:
    """
    Create the video folder structure.

    Creates:
        {client_root}/workflows/youtube/videos/{video_slug}/
            input/
                DROP_FILES_HERE.md
            output/
                .gitkeep

    Args:
        client_root: Resolved client workspace root path
        video_slug: URL-safe slug for this video

    Returns:
        Path to the created video folder

    Raises:
        FileExistsError: If the video folder already exists
    """
    video_dir = client_root / "workflows" / "youtube" / "videos" / video_slug
    input_dir = video_dir / "input"
    output_dir = video_dir / "output"

    if video_dir.exists():
        raise FileExistsError(
            f"Video folder already exists: {video_dir}\n"
            f"Drop your files into {input_dir}/ and run: /youtube publish {video_slug}"
        )

    input_dir.mkdir(parents=True)
    output_dir.mkdir(parents=True)

    # Write instructions file
    drop_files_content = f"""# Drop Your Files Here

Before running the YouTube publish agent, paste these files into this folder:

| File | Source | Required |
|------|--------|----------|
| `transcript.txt` | Descript: Export > Plain Text | Yes |
| `transcript.srt` | Descript: Export > SRT Captions | Yes |
| `video.mp4` | Your edited video file | Optional (for future upload) |

## How to Export from Descript

1. Open your project in Descript
2. File > Export
3. Export "Transcript" as Plain Text -> save as `transcript.txt`
4. Export "Captions" as SRT -> save as `transcript.srt`

## After Dropping Files

Run the publish agent:

```
/youtube publish {video_slug}
```

Or via Python directly:

```bash
python scripts/run_agent.py \\
    --agent youtube_publish \\
    --client {{client}} \\
    --input input/agent_input.json \\
    --output output/metadata.json
```

The agent will generate everything into the `output/` subfolder:
- `metadata.json` - All structured metadata (titles, tags, chapters, etc.)
- `thumbnail_prompt.json` - Nano Banana image prompt
- `thumbnail.png` - Generated YouTube thumbnail (16:9, 2K)
- `description.txt` - Ready to paste into YouTube Studio
- `pinned_comment.md` - First comment to post after upload
- `captions_en.srt` - Subtitles file for YouTube
"""
    (input_dir / "DROP_FILES_HERE.md").write_text(drop_files_content)
    (output_dir / ".gitkeep").touch()

    return video_dir


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new YouTube video folder")
    parser.add_argument("--client", required=True, help="Client slug (e.g. acme)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--slug", help="URL-safe folder slug")
    group.add_argument("--title", help="Video title (will be slugified)")

    args = parser.parse_args()

    video_slug = args.slug if args.slug else slugify(args.title)

    workspace_root = find_workspace_root()
    client_root = find_client_root(args.client, workspace_root)

    try:
        video_dir = scaffold_video(client_root, video_slug)
        print(f"Created video folder: {video_dir}")
        print(f"\nNext steps:")
        print(f"  1. Drop transcript.txt and transcript.srt into: {video_dir / 'input'}/")
        print(f"  2. Run: /youtube publish {video_slug}")
    except FileExistsError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
