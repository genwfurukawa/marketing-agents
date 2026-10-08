#!/usr/bin/env python3
"""
Brand-aware image generator.

Wraps GeminiImageClient with brand guidelines, logo reference images,
and LinkedIn-optimized presets. Reads brand colors, fonts, and logo paths
from the active client config (config.yaml + brand assets dir).

Usage:
    # Explicit client config path
    gen = BrandImageGenerator(client_config_path="clients/acme/config.yaml")

    # Or set the env var
    # export CLIENT_CONFIG=clients/acme/config.yaml
    gen = BrandImageGenerator()

The client config supplies:
    visual_style.colors.primary_accent
    visual_style.colors.background
    visual_style.colors.text_primary
    visual_style.colors.text_secondary
    visual_style.brand_font                 # falls back to visual_style.font
    visual_style.logos.{white,yellow,black}   # paths relative to the config dir
    visual_style.brand_prompt_rules           # list of one-line prompt rules

If any of those are missing, the generator falls back to neutral
high-contrast defaults so it never silently produces off-brand output.
"""

import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any, Union, List

import yaml

from scripts.image.gemini_image_client import GeminiImageClient

# Version
__version__ = "2.0.0"


# ----------------------------------------------------------------------------
# Defaults (used when the client config does not supply a value)
# ----------------------------------------------------------------------------

DEFAULT_BRAND = {
    "colors": {
        "primary_accent": "#FFFFFF",
        "background": "#000000",
        "text_primary": "#FFFFFF",
        "text_secondary": "#888888",
    },
    "font": "sans-serif",
    "logos": {},
    "prompt_rules": [
        "High contrast, lots of negative space",
        "No emojis, no clip art, no stock photos",
        "Bold, minimal social media graphic",
    ],
}

# LinkedIn image presets — generic, not brand-specific
LINKEDIN_PRESETS = {
    "single_image":   {"aspect_ratio": "1:1",  "resolution": "1K"},
    "story":          {"aspect_ratio": "9:16", "resolution": "1K"},
    "banner":         {"aspect_ratio": "4:1",  "resolution": "1K"},
    "carousel_slide": {"aspect_ratio": "4:5",  "resolution": "1K"},
}


# ----------------------------------------------------------------------------
# Config loading
# ----------------------------------------------------------------------------

def _find_workspace_root() -> Path:
    """Find workspace root by looking for marker files."""
    current = Path(__file__).resolve()
    markers = ["CLAUDE.md", "MIGRATION_PLAN.md", ".git"]
    for parent in [current] + list(current.parents):
        for marker in markers:
            if (parent / marker).exists():
                return parent
    return Path(__file__).resolve().parent.parent.parent


WORKSPACE_ROOT = _find_workspace_root()


def _resolve_client_config_path(explicit: Optional[Union[str, Path]] = None) -> Optional[Path]:
    """
    Resolve which client config to load, in priority order:
      1. Explicit arg
      2. CLIENT_CONFIG env var
      3. WORKSPACE_ROOT/config.yaml (only useful when called from inside a client repo)
    Returns None if no config is found — caller will use DEFAULT_BRAND.
    """
    candidates: List[Path] = []
    if explicit:
        candidates.append(Path(explicit))
    if os.environ.get("CLIENT_CONFIG"):
        candidates.append(Path(os.environ["CLIENT_CONFIG"]))
    candidates.append(WORKSPACE_ROOT / "config.yaml")

    for cand in candidates:
        if cand.exists():
            return cand.resolve()
    return None


def _load_brand_config(client_config_path: Optional[Path], logger: logging.Logger) -> Dict[str, Any]:
    """
    Load brand values from a client config. Merge with defaults so missing
    keys never blow up downstream.
    """
    if client_config_path is None:
        logger.warning(
            "No client config found. Using neutral defaults. "
            "Pass client_config_path= or set CLIENT_CONFIG to point at a client config.yaml."
        )
        return {**DEFAULT_BRAND, "config_dir": None}

    with open(client_config_path, "r") as f:
        cfg = yaml.safe_load(f) or {}

    visual = cfg.get("visual_style", {}) or {}
    config_dir = client_config_path.parent

    # Colors: support both nested 'colors' dict and flat keys for back-compat.
    colors_from_cfg = visual.get("colors") or {
        "primary_accent": visual.get("primary_color") or visual.get("primary_accent"),
        "background": visual.get("background"),
        "text_primary": visual.get("text_primary"),
        "text_secondary": visual.get("text_secondary"),
    }
    colors = {**DEFAULT_BRAND["colors"]}
    for k, v in colors_from_cfg.items():
        if v:
            colors[k] = v

    # Logos: resolve relative paths against the config dir.
    logos_cfg = visual.get("logos") or {}
    logos = {}
    for variant, rel in logos_cfg.items():
        p = (config_dir / rel).resolve() if not Path(rel).is_absolute() else Path(rel)
        logos[variant] = p

    return {
        "colors": colors,
        # brand_font is the brand typeface; a bare `font` key can belong to another
        # style block (growth's diagram settings use font: hand-drawn)
        "font": visual.get("brand_font") or visual.get("font") or DEFAULT_BRAND["font"],
        "logos": logos,
        "prompt_rules": visual.get("brand_prompt_rules") or DEFAULT_BRAND["prompt_rules"],
        "config_dir": config_dir,
    }


# ----------------------------------------------------------------------------
# Prompt builder
# ----------------------------------------------------------------------------

def build_brand_prompt(content_prompt: str, brand: Dict[str, Any]) -> str:
    """
    Build a concise brand-aware prompt from the client's brand config.
    Keep it short so Gemini focuses on visual impact, not cramming text.
    """
    colors = brand["colors"]
    bg = colors["background"]
    accent = colors["primary_accent"]
    text = colors["text_primary"]
    font = brand["font"]

    rules_lines = [f"- {r}" for r in brand["prompt_rules"]]
    rules_lines.insert(0, f"- Background {bg}, accent {accent}, text {text}")
    rules_lines.insert(1, f"- Clean {font} typography")
    rules_lines.append("- The attached logo image (if any) should appear small in the bottom-right corner")
    rules = "\n".join(rules_lines)

    return f"""Create a bold, minimal social media graphic.

BRAND RULES:
{rules}

{content_prompt}""".strip()


# ----------------------------------------------------------------------------
# Generator
# ----------------------------------------------------------------------------

class BrandImageGenerator:
    """
    Brand-aware image generator. Reads brand values from the active client
    config. The same code base serves any client; only the config changes.
    """

    def __init__(
        self,
        client_config_path: Optional[Union[str, Path]] = None,
        api_key: Optional[str] = None,
        model: str = "flash-preview",
        logger: Optional[logging.Logger] = None,
    ):
        self.logger = logger or logging.getLogger(__name__)

        resolved = _resolve_client_config_path(client_config_path)
        self.brand = _load_brand_config(resolved, self.logger)
        self.client_config_path = resolved

        # Initialize Gemini client
        self.image_client = GeminiImageClient(
            api_key=api_key,
            model=model,
            logger=self.logger,
        )

        # Pick the default logo (white variant on dark backgrounds).
        self.logo_path = self.brand["logos"].get("white")
        if self.logo_path and not Path(self.logo_path).exists():
            self.logger.warning(f"Logo not found at {self.logo_path}")
            self.logo_path = None

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def colors(self) -> Dict[str, str]:
        return dict(self.brand["colors"])

    def font(self) -> str:
        return self.brand["font"]

    def _get_logo_refs(self, background: str = "dark") -> List[Path]:
        """Get logo reference image paths based on background color."""
        if background == "dark":
            logo = self.brand["logos"].get("white")
        elif background == "light":
            logo = self.brand["logos"].get("black")
        else:
            logo = self.brand["logos"].get("yellow")

        if logo and Path(logo).exists():
            return [Path(logo)]
        return []

    def _build_prompt(self, content: str) -> str:
        return build_brand_prompt(content, self.brand)

    # ------------------------------------------------------------------
    # Generation entry points
    # ------------------------------------------------------------------

    def generate_linkedin_image(
        self,
        content: str,
        output_path: Union[str, Path],
        preset: str = "single_image",
        include_logo: bool = True,
    ) -> dict:
        """Generate a brand-aligned LinkedIn image."""
        preset_config = LINKEDIN_PRESETS.get(preset, LINKEDIN_PRESETS["single_image"])
        full_prompt = self._build_prompt(content)
        refs = self._get_logo_refs() if include_logo else []

        self.logger.info(f"Generating LinkedIn {preset} -> {output_path}")

        return self.image_client.generate(
            prompt=full_prompt,
            output_path=output_path,
            aspect_ratio=preset_config["aspect_ratio"],
            resolution=preset_config["resolution"],
            reference_images=refs if refs else None,
        )

    def generate_from_post(
        self,
        post_hook: str,
        post_angle: str,
        key_stat: Optional[str] = None,
        output_path: Optional[Union[str, Path]] = None,
        preset: str = "single_image",
    ) -> dict:
        """Generate an image from LinkedIn post components."""
        parts = [f'Bold headline: "{post_hook}"']
        if key_stat:
            parts.append(f'Feature this stat large: "{key_stat}"')
        parts.append(f"Visual tone: {post_angle}")
        content = "\n".join(parts)

        preset_config = LINKEDIN_PRESETS.get(preset, LINKEDIN_PRESETS["single_image"])
        full_prompt = self._build_prompt(content)
        refs = self._get_logo_refs()

        return self.image_client.generate(
            prompt=full_prompt,
            output_path=output_path,
            aspect_ratio=preset_config["aspect_ratio"],
            resolution=preset_config["resolution"],
            reference_images=refs if refs else None,
        )

    def generate_carousel(
        self,
        slides: list,
        output_dir: Union[str, Path],
        filename_prefix: str = "slide",
    ) -> list:
        """Generate carousel slides with consistent branding."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        self.image_client.start_chat()

        try:
            for i, slide in enumerate(slides):
                content = slide.get("content", "")

                if i == 0:
                    prompt = self._build_prompt(content)
                    prompt += "\n\nThis is slide 1 of a carousel. Establish the visual style."
                else:
                    prompt = (
                        f"Next carousel slide (slide {i + 1}), same visual style.\n\n"
                        f"{content}"
                    )

                output_path = output_dir / f"{filename_prefix}_{i + 1:02d}.png"

                result = self.image_client.send_message(
                    message=prompt,
                    output_path=output_path,
                    aspect_ratio="4:5",
                )
                results.append(result)
                self.logger.info(f"Carousel slide {i + 1}/{len(slides)} done")

        finally:
            self.image_client.end_chat()

        return results


# ----------------------------------------------------------------------------
# Back-compat re-exports
# ----------------------------------------------------------------------------

# Older callers may import `BRAND`, `LINKEDIN_PRESETS`, or `_build_brand_prompt`
# from this module. Preserve those names without the SM-specific values.
BRAND = DEFAULT_BRAND


def _build_brand_prompt(content_prompt: str) -> str:
    """Back-compat shim: builds a prompt using defaults only. Prefer using
    BrandImageGenerator(...)._build_prompt() so client brand values apply."""
    return build_brand_prompt(content_prompt, DEFAULT_BRAND)
