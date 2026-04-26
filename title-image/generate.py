#!/usr/bin/env python3
"""Generate the title image via Gemini 2.5 Flash Image (nano-banana).

Reads the prompt from prompt.md (or a file passed as argv[1]), POSTs to the
Gemini API, saves the resulting PNG to renders/render-<timestamp>.png.

Requires one of these env vars:
  GEMINI_API_KEY  (preferred)
  GOOGLE_API_KEY
  GOOGLE_GENERATIVE_AI_API_KEY

Optional override:
  GEMINI_IMAGE_MODEL  (default: gemini-2.5-flash-image-preview)

Stdlib only — no pip install needed.
"""

from __future__ import annotations

import base64
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

DEFAULT_MODEL = "gemini-3-pro-image-preview"  # Nano Banana Pro — premium tier
DEFAULT_ASPECT = "16:9"
DEFAULT_SIZE = "4K"  # max quality; alternatives: "1K", "2K"
HERE = Path(__file__).resolve().parent
RENDERS = HERE / "renders"


def get_api_key() -> str:
    for var in ("GEMINI_API_KEY", "GOOGLE_API_KEY", "GOOGLE_GENERATIVE_AI_API_KEY"):
        value = os.environ.get(var)
        if value:
            return value
    sys.exit(
        "ERROR: no API key in environment. "
        "Set GEMINI_API_KEY (or GOOGLE_API_KEY)."
    )


def read_prompt(path: Path) -> str:
    """Extract the prompt body from a markdown file.

    Convention: the prompt is the content of the first fenced code block.
    If no fenced block exists, the whole file is treated as the prompt.
    """
    text = path.read_text(encoding="utf-8")
    if "```" not in text:
        return text.strip()
    # Split on the fence; parts[1] is the first block body (with optional lang tag).
    parts = text.split("```")
    if len(parts) < 3:
        sys.exit(f"ERROR: unbalanced code fence in {path}")
    block = parts[1]
    # Drop a leading language tag if present (e.g. ```text\n...).
    first_line, _, rest = block.partition("\n")
    if first_line.strip() and len(first_line.strip()) < 20 and " " not in first_line.strip():
        return rest.rstrip()
    return block.rstrip()


def call_api(prompt: str, api_key: str, model: str,
             aspect: str, size: str) -> bytes:
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"{model}:generateContent?key={api_key}"
    )
    payload = json.dumps(
        {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {
                    "aspectRatio": aspect,
                    "imageSize": size,
                },
            },
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            data = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        sys.exit(f"HTTP {exc.code} from Gemini API:\n{body}")
    except urllib.error.URLError as exc:
        sys.exit(f"Network error: {exc.reason}")

    for candidate in data.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            inline = part.get("inlineData") or part.get("inline_data")
            if inline and "data" in inline:
                return base64.b64decode(inline["data"])

    sys.exit(
        "ERROR: API returned no image data.\n"
        f"Full response:\n{json.dumps(data, indent=2)}"
    )


def main() -> None:
    prompt_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "prompt.md"
    if not prompt_path.is_absolute():
        prompt_path = HERE / prompt_path
    if not prompt_path.exists():
        sys.exit(f"ERROR: prompt file not found: {prompt_path}")

    api_key = get_api_key()
    model = os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_MODEL)
    aspect = os.environ.get("GEMINI_IMAGE_ASPECT", DEFAULT_ASPECT)
    size = os.environ.get("GEMINI_IMAGE_SIZE", DEFAULT_SIZE)
    prompt = read_prompt(prompt_path)
    if not prompt:
        sys.exit(f"ERROR: empty prompt in {prompt_path}")

    print(f"Model:  {model}")
    print(f"Config: {aspect} @ {size}")
    print(f"Prompt: {prompt_path.name} ({len(prompt)} chars)")
    print("Calling Gemini API...", flush=True)

    image_bytes = call_api(prompt, api_key, model, aspect, size)

    RENDERS.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = RENDERS / f"render-{stamp}.png"
    out_path.write_bytes(image_bytes)
    print(f"Saved:  {out_path.relative_to(HERE)} ({len(image_bytes):,} bytes)")


if __name__ == "__main__":
    main()
