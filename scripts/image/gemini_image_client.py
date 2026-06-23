#!/usr/bin/env python3
"""
Gemini Image Generation Client (Nano Banana).

Thin wrapper around Google's Gemini image generation API with:
- Retry with exponential backoff
- Model selection (Flash, Flash Preview, Pro Preview)
- Aspect ratio and resolution control
- Multi-turn conversation support for iterative editing
- File-based output management
"""

import base64
import logging
import os
import time
from io import BytesIO
from pathlib import Path
from typing import Optional, List, Union

# Version
__version__ = "1.0.0"


class GeminiImageClient:
    """
    Low-level client for Gemini image generation.

    Supports text-to-image, image editing, and multi-turn conversations.

    Models:
        - gemini-2.5-flash-image: Speed/volume (Nano Banana)
        - gemini-3.1-flash-image-preview: Best all-around (Nano Banana 2)
        - gemini-3-pro-image-preview: Professional assets (Nano Banana Pro)
    """

    # Model aliases for convenience
    MODELS = {
        "flash": "gemini-2.5-flash-image",
        "flash-preview": "gemini-3.1-flash-image-preview",
        "pro": "gemini-3-pro-image-preview",
    }

    # Valid aspect ratios
    ASPECT_RATIOS = [
        "1:1", "1:4", "1:8", "2:3", "3:2", "3:4",
        "4:1", "4:3", "4:5", "5:4", "8:1", "9:16", "16:9", "21:9",
    ]

    # Valid resolutions
    RESOLUTIONS = ["512px", "1K", "2K", "4K"]

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "flash-preview",
        max_retries: int = 3,
        logger: Optional[logging.Logger] = None,
    ):
        """
        Initialize Gemini image client.

        Args:
            api_key: Google GenAI API key (reads from GOOGLE_GENAI_API_KEY
                     or GOOGLE_API_KEY env if None)
            model: Model name or alias ('flash', 'flash-preview', 'pro')
            max_retries: Maximum retry attempts on failure
            logger: Logger instance
        """
        self.api_key = api_key or os.getenv("GOOGLE_GENAI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No API key provided. Set GOOGLE_GENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        # Resolve model alias
        self.model = self.MODELS.get(model, model)
        self.max_retries = max_retries
        self.logger = logger or logging.getLogger(__name__)

        # Lazy-loaded client
        self._client = None
        self._chat = None

    @property
    def client(self):
        """Lazy-load Google GenAI client."""
        if self._client is None:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
                self.logger.debug(f"Initialized Gemini client with model: {self.model}")
            except ImportError:
                raise ImportError(
                    "google-genai package not installed. "
                    "Install with: pip install google-genai"
                )
        return self._client

    def generate(
        self,
        prompt: str,
        output_path: Optional[Union[str, Path]] = None,
        aspect_ratio: str = "1:1",
        resolution: str = "1K",
        image_only: bool = False,
        reference_images: Optional[List[Union[str, Path]]] = None,
    ) -> dict:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text description of the image to generate
            output_path: Path to save the generated image (optional)
            aspect_ratio: Output aspect ratio (e.g., '1:1', '4:5', '16:9')
            resolution: Output resolution ('512px', '1K', '2K', '4K')
            image_only: If True, only return image (no text)
            reference_images: List of paths to reference images for editing

        Returns:
            dict with keys:
                - image_path: Path to saved image (if output_path provided)
                - image_data: Raw image bytes
                - text: Any text returned alongside the image
                - model: Model used
                - prompt: Original prompt
        """
        from google.genai import types

        # Validate aspect ratio
        if aspect_ratio not in self.ASPECT_RATIOS:
            raise ValueError(
                f"Invalid aspect ratio '{aspect_ratio}'. "
                f"Valid options: {', '.join(self.ASPECT_RATIOS)}"
            )

        # Validate resolution
        if resolution not in self.RESOLUTIONS:
            raise ValueError(
                f"Invalid resolution '{resolution}'. "
                f"Valid options: {', '.join(self.RESOLUTIONS)}"
            )

        # Build contents
        contents = [prompt]

        # Add reference images if provided
        if reference_images:
            from PIL import Image as PILImage
            for img_path in reference_images:
                img = PILImage.open(str(img_path))
                contents.append(img)

        # Build config
        modalities = ["IMAGE"] if image_only else ["TEXT", "IMAGE"]

        # Build image config - image_size may not be available in all SDK versions
        img_config_kwargs = {"aspect_ratio": aspect_ratio}
        try:
            # Try with resolution (newer SDK versions / Gemini 3.x models)
            test_config = types.ImageConfig(aspect_ratio=aspect_ratio, image_size=resolution)
            img_config_kwargs["image_size"] = resolution
        except Exception:
            # Older SDK - skip image_size, use default 1K
            self.logger.debug(f"image_size not supported in this SDK version, using default")

        config = types.GenerateContentConfig(
            response_modalities=modalities,
            image_config=types.ImageConfig(**img_config_kwargs),
        )

        # Retry loop
        last_error = None
        for attempt in range(self.max_retries):
            try:
                self.logger.info(
                    f"Generating image (attempt {attempt + 1}/{self.max_retries}) "
                    f"model={self.model} ratio={aspect_ratio} res={resolution}"
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config,
                )

                # Extract results
                result = {
                    "image_data": None,
                    "image_path": None,
                    "text": None,
                    "model": self.model,
                    "prompt": prompt,
                    "aspect_ratio": aspect_ratio,
                    "resolution": resolution,
                }

                for part in response.parts:
                    if part.text is not None:
                        result["text"] = part.text
                    elif part.inline_data is not None:
                        # Get raw bytes from inline_data
                        raw_bytes = part.inline_data.data
                        mime = part.inline_data.mime_type or "image/png"

                        # Convert to PIL Image for consistent handling
                        from PIL import Image as PILImage
                        pil_image = PILImage.open(BytesIO(raw_bytes))

                        # Save raw bytes
                        buf = BytesIO()
                        pil_image.save(buf, format="PNG")
                        result["image_data"] = buf.getvalue()

                        # Save to file if path provided
                        if output_path:
                            output_path = Path(output_path)
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            pil_image.save(str(output_path), format="PNG")
                            result["image_path"] = str(output_path)
                            self.logger.info(f"Image saved to: {output_path}")

                if result["image_data"] is None:
                    raise RuntimeError(
                        "No image returned in response. "
                        "The model may have returned only text."
                    )

                return result

            except Exception as e:
                last_error = e
                self.logger.warning(f"Attempt {attempt + 1} failed: {e}")

                if attempt < self.max_retries - 1:
                    wait_time = 2 ** attempt
                    self.logger.info(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        self.logger.error(f"All {self.max_retries} attempts failed")
        raise last_error

    def edit(
        self,
        prompt: str,
        image_path: Union[str, Path],
        output_path: Optional[Union[str, Path]] = None,
        aspect_ratio: str = "1:1",
        resolution: str = "1K",
    ) -> dict:
        """
        Edit an existing image with a text prompt.

        Args:
            prompt: Description of the edit to make
            image_path: Path to the image to edit
            output_path: Path to save the edited image
            aspect_ratio: Output aspect ratio
            resolution: Output resolution

        Returns:
            Same dict format as generate()
        """
        return self.generate(
            prompt=prompt,
            output_path=output_path,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            reference_images=[image_path],
        )

    def start_chat(self) -> None:
        """
        Start a multi-turn chat session for iterative image editing.

        Use send_message() after starting a chat to iterate on images.
        """
        from google.genai import types

        self._chat = self.client.chats.create(
            model=self.model,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )
        self.logger.info("Started multi-turn image chat session")

    def send_message(
        self,
        message: str,
        output_path: Optional[Union[str, Path]] = None,
        aspect_ratio: Optional[str] = None,
        resolution: Optional[str] = None,
    ) -> dict:
        """
        Send a message in an active chat session.

        Args:
            message: Text prompt for the next iteration
            output_path: Path to save the resulting image
            aspect_ratio: Override aspect ratio for this message
            resolution: Override resolution for this message

        Returns:
            Same dict format as generate()
        """
        if self._chat is None:
            raise RuntimeError("No active chat session. Call start_chat() first.")

        from google.genai import types

        # Build config overrides
        kwargs = {}
        if aspect_ratio or resolution:
            img_config = {}
            if aspect_ratio:
                img_config["aspect_ratio"] = aspect_ratio
            if resolution:
                img_config["image_size"] = resolution
            kwargs["config"] = types.GenerateContentConfig(
                image_config=types.ImageConfig(**img_config),
            )

        response = self._chat.send_message(message, **kwargs)

        result = {
            "image_data": None,
            "image_path": None,
            "text": None,
            "model": self.model,
            "prompt": message,
        }

        for part in response.parts:
            if part.text is not None:
                result["text"] = part.text
            elif part.inline_data is not None:
                image = part.as_image()
                buf = BytesIO()
                image.save(buf, format="PNG")
                result["image_data"] = buf.getvalue()

                if output_path:
                    output_path = Path(output_path)
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    image.save(str(output_path))
                    result["image_path"] = str(output_path)

        return result

    def end_chat(self) -> None:
        """End the current chat session."""
        self._chat = None
        self.logger.info("Ended multi-turn image chat session")
