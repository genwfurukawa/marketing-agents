#!/usr/bin/env python3
"""
Generate images from structured JSON prompt files.

Each JSON file follows the image_prompt schema and produces one image.
Supports batch generation from a directory of JSON files.

Usage:
    # Single file
    python scripts/image/generate_from_json.py --input prompts/hero.json --output-dir output/images/

    # Batch (all JSON files in a directory)
    python scripts/image/generate_from_json.py --input prompts/ --output-dir output/images/

    # With client brand overrides
    python scripts/image/generate_from_json.py --input prompts/ --output-dir output/images/ --client acme
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.image.brand_image_generator import (
    BrandImageGenerator,
    BRAND,
    LINKEDIN_PRESETS,
    _build_brand_prompt,
)
from scripts.image.gemini_image_client import GeminiImageClient


def load_prompt(json_path: Path) -> dict:
    """Load and validate an image prompt JSON file."""
    with open(json_path, "r") as f:
        data = json.load(f)

    # Required fields
    if "prompt" not in data:
        raise ValueError(f"Missing required field 'prompt' in {json_path}")
    if "output_filename" not in data:
        raise ValueError(f"Missing required field 'output_filename' in {json_path}")

    return data


def build_full_prompt(data: dict) -> str:
    """
    Assemble the full generation prompt from JSON fields.

    Combines: style + brand guidelines + layout + core prompt + negative prompt
    """
    parts = []

    # Style direction
    style = data.get("style", "")
    if style:
        parts.append(f"STYLE: {style}")

    # Core prompt
    parts.append(data["prompt"])

    # Layout instructions (for text-heavy images)
    layout = data.get("layout")
    if layout:
        parts.append("\nTEXT LAYOUT:")
        if layout.get("headline"):
            parts.append(f'HEADLINE: "{layout["headline"]}"')
        if layout.get("subheadline"):
            parts.append(f'SUBHEADLINE: "{layout["subheadline"]}"')
        if layout.get("stat"):
            parts.append(f'KEY STAT: Display "{layout["stat"]}" prominently')
        if layout.get("body_text"):
            parts.append(f'BODY TEXT: "{layout["body_text"]}"')
        if layout.get("cta"):
            parts.append(f'CTA: "{layout["cta"]}"')

        logo_pos = layout.get("logo_position", "bottom-right")
        if logo_pos != "none":
            wordmark = layout.get("wordmark_text") or os.environ.get("VISIBILITY_OPS_WORDMARK")
            if wordmark:
                parts.append(f'\nPlace small "{wordmark}" wordmark in {logo_pos}')

        parts.append("\nIMPORTANT: Render all text accurately and legibly. Text content is the most important element.")

    # Negative prompt
    negative = data.get("negative_prompt")
    if negative:
        parts.append(f"\nAVOID: {negative}")

    raw_prompt = "\n".join(parts)

    # Brand wrapping
    brand_mode = data.get("brand", "client")
    preset_name = data.get("preset", "single_image")

    if brand_mode == "client":
        # Client brand injection happens at the BrandImageGenerator level
        return _build_brand_prompt(raw_prompt)
    else:
        # No brand wrapping - raw prompt
        return raw_prompt


def resolve_settings(data: dict) -> dict:
    """Extract generation settings from the JSON, with preset defaults."""
    preset_name = data.get("preset", "single_image")
    preset = LINKEDIN_PRESETS.get(preset_name, LINKEDIN_PRESETS["single_image"])

    return {
        "model": data.get("model", "flash-preview"),
        "aspect_ratio": data.get("aspect_ratio", preset.get("aspect_ratio", "1:1")),
        "resolution": data.get("resolution", "2K"),
        "reference_images": data.get("reference_images"),
    }


def generate_image(
    data: dict,
    output_dir: Path,
    client_name: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> dict:
    """
    Generate a single image from a prompt JSON dict.

    Args:
        data: Parsed image prompt JSON
        output_dir: Directory to save the output image
        client_name: Optional client for brand overrides
        logger: Logger instance

    Returns:
        dict with generation results
    """
    logger = logger or logging.getLogger(__name__)

    # Build prompt
    full_prompt = build_full_prompt(data)

    # Resolve settings
    settings = resolve_settings(data)

    # Output path
    output_path = output_dir / data["output_filename"]

    logger.info(
        f"Generating: {data['output_filename']} "
        f"(model={settings['model']}, ratio={settings['aspect_ratio']}, res={settings['resolution']})"
    )

    # Use BrandImageGenerator if client specified, else raw client
    if client_name and data.get("brand") == "client":
        generator = BrandImageGenerator(
            model=settings["model"],
            client_name=client_name,
            logger=logger,
        )
        result = generator.image_client.generate(
            prompt=full_prompt,
            output_path=output_path,
            aspect_ratio=settings["aspect_ratio"],
            resolution=settings["resolution"],
            reference_images=settings.get("reference_images"),
        )
    else:
        client = GeminiImageClient(
            model=settings["model"],
            logger=logger,
        )
        result = client.generate(
            prompt=full_prompt,
            output_path=output_path,
            aspect_ratio=settings["aspect_ratio"],
            resolution=settings["resolution"],
            reference_images=settings.get("reference_images"),
        )

    # Add metadata to result
    result["source_json"] = data.get("metadata", {})
    result["output_filename"] = data["output_filename"]

    return result


def generate_batch(
    input_dir: Path,
    output_dir: Path,
    client_name: Optional[str] = None,
    logger: Optional[logging.Logger] = None,
) -> list:
    """
    Generate images from all JSON files in a directory.

    Args:
        input_dir: Directory containing image prompt JSON files
        output_dir: Directory to save output images
        client_name: Optional client for brand overrides
        logger: Logger instance

    Returns:
        List of result dicts
    """
    logger = logger or logging.getLogger(__name__)

    json_files = sorted(input_dir.glob("*.json"))
    if not json_files:
        logger.warning(f"No JSON files found in {input_dir}")
        return []

    logger.info(f"Found {len(json_files)} image prompts in {input_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for json_file in json_files:
        try:
            data = load_prompt(json_file)
            result = generate_image(data, output_dir, client_name, logger)
            result["source_file"] = str(json_file)
            results.append(result)
            logger.info(f"OK: {json_file.name} -> {data['output_filename']}")
        except Exception as e:
            logger.error(f"FAIL: {json_file.name} - {e}")
            results.append({
                "source_file": str(json_file),
                "error": str(e),
            })

    # Summary
    ok = sum(1 for r in results if "error" not in r)
    fail = sum(1 for r in results if "error" in r)
    logger.info(f"Batch complete: {ok} succeeded, {fail} failed out of {len(json_files)}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Generate images from structured JSON prompt files"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to a single JSON file or directory of JSON files",
    )
    parser.add_argument(
        "--output-dir", "-o",
        required=True,
        help="Directory to save generated images",
    )
    parser.add_argument(
        "--client", "-c",
        help="Client slug for brand overrides",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print assembled prompts without generating images",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("image_generator")

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.dry_run:
        # Dry run - just show assembled prompts
        files = [input_path] if input_path.is_file() else sorted(input_path.glob("*.json"))
        for f in files:
            data = load_prompt(f)
            prompt = build_full_prompt(data)
            settings = resolve_settings(data)
            print(f"\n{'='*60}")
            print(f"FILE: {f.name}")
            print(f"OUTPUT: {data['output_filename']}")
            print(f"MODEL: {settings['model']} | RATIO: {settings['aspect_ratio']} | RES: {settings['resolution']}")
            print(f"{'='*60}")
            print(prompt)
            print()
        return

    if input_path.is_file():
        # Single file
        data = load_prompt(input_path)
        result = generate_image(data, output_dir, args.client, logger)
        if result.get("image_path"):
            print(f"Image saved: {result['image_path']}")
        else:
            print(f"Error: {result.get('error', 'Unknown error')}")
    elif input_path.is_dir():
        # Batch
        results = generate_batch(input_path, output_dir, args.client, logger)
        for r in results:
            if "error" in r:
                print(f"FAIL: {r['source_file']} - {r['error']}")
            else:
                print(f"OK: {r.get('image_path', r.get('output_filename'))}")
    else:
        print(f"Error: {input_path} is not a file or directory")
        sys.exit(1)


if __name__ == "__main__":
    main()