"""Generate video frames from images and code snippets using Pillow."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math


# Default resolution
WIDTH, HEIGHT = 1280, 720
BG_COLOR = (10, 10, 15)        # Dark background matching portfolio
TEXT_COLOR = (228, 228, 239)    # --text equivalent
ACCENT_COLOR = (99, 102, 241)  # --accent equivalent
CODE_BG = (17, 17, 25)         # --bg2 equivalent
MUTED_COLOR = (157, 157, 181)  # --text2 equivalent


def _load_font(size: int, mono: bool = False) -> ImageFont.FreeTypeFont:
    """Load a font, falling back to default if not available."""
    try:
        if mono:
            return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size)
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except (OSError, IOError):
        return ImageFont.load_default()


def generate_image_frame(
    image_path: str,
    title: str | None = None,
    resolution: tuple[int, int] = (WIDTH, HEIGHT),
) -> Image.Image:
    """Create a frame from a screenshot/image, centered with dark background."""
    w, h = resolution
    frame = Image.new("RGB", (w, h), BG_COLOR)

    img = Image.open(image_path).convert("RGB")

    # Scale image to fit within frame with padding
    pad = 40
    max_w, max_h = w - pad * 2, h - pad * 2
    if title:
        max_h -= 60  # Reserve space for title

    ratio = min(max_w / img.width, max_h / img.height)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    img = img.resize(new_size, Image.LANCZOS)

    # Center image
    y_offset = 60 if title else 0
    x = (w - new_size[0]) // 2
    y = (h - new_size[1] + y_offset) // 2
    frame.paste(img, (x, y))

    # Draw title if provided
    if title:
        draw = ImageDraw.Draw(frame)
        font = _load_font(28)
        draw.text((pad, 20), title, fill=TEXT_COLOR, font=font)

    return frame


def generate_code_frame(
    code: str,
    filename: str = "code.py",
    resolution: tuple[int, int] = (WIDTH, HEIGHT),
) -> Image.Image:
    """Create a frame that displays a code snippet in terminal style."""
    w, h = resolution
    frame = Image.new("RGB", (w, h), BG_COLOR)
    draw = ImageDraw.Draw(frame)

    # Code window dimensions
    win_x, win_y = 60, 40
    win_w, win_h = w - 120, h - 80

    # Draw code window background
    draw.rounded_rectangle(
        [win_x, win_y, win_x + win_w, win_y + win_h],
        radius=12,
        fill=CODE_BG,
        outline=(34, 34, 51),
    )

    # Draw title bar
    bar_h = 40
    draw.rounded_rectangle(
        [win_x, win_y, win_x + win_w, win_y + bar_h],
        radius=12,
        fill=(26, 26, 39),
    )
    # Fix bottom corners of title bar
    draw.rectangle(
        [win_x, win_y + bar_h - 12, win_x + win_w, win_y + bar_h],
        fill=(26, 26, 39),
    )

    # Traffic light dots
    for i, color in enumerate([(239, 68, 68), (245, 158, 11), (34, 197, 94)]):
        cx = win_x + 20 + i * 20
        cy = win_y + bar_h // 2
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)

    # Filename
    small_font = _load_font(13, mono=True)
    draw.text((win_x + 90, win_y + 12), filename, fill=MUTED_COLOR, font=small_font)

    # Code text
    code_font = _load_font(16, mono=True)
    code_y = win_y + bar_h + 20
    code_x = win_x + 24

    for i, line in enumerate(code.strip().split("\n")):
        # Line number
        line_num = str(i + 1).rjust(3)
        draw.text((code_x, code_y), line_num, fill=(75, 75, 100), font=code_font)
        # Code content
        draw.text((code_x + 50, code_y), line, fill=TEXT_COLOR, font=code_font)
        code_y += 26
        if code_y > win_y + win_h - 20:
            break

    return frame


def apply_zoom_effect(
    base_frame: Image.Image,
    progress: float,
    zoom_in: bool = True,
    max_zoom: float = 1.15,
) -> Image.Image:
    """Apply zoom effect to a frame. progress is 0.0 to 1.0."""
    w, h = base_frame.size

    if zoom_in:
        scale = 1.0 + (max_zoom - 1.0) * progress
    else:
        scale = max_zoom - (max_zoom - 1.0) * progress

    new_w, new_h = int(w * scale), int(h * scale)
    zoomed = base_frame.resize((new_w, new_h), Image.LANCZOS)

    # Crop center
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    return zoomed.crop((left, top, left + w, top + h))


def apply_pan_effect(
    base_frame: Image.Image,
    progress: float,
    direction: str = "left",
    pan_amount: int = 80,
) -> Image.Image:
    """Apply horizontal pan effect. progress is 0.0 to 1.0."""
    w, h = base_frame.size

    # Scale up slightly so we have room to pan
    scale = 1.1
    new_w, new_h = int(w * scale), int(h * scale)
    scaled = base_frame.resize((new_w, new_h), Image.LANCZOS)

    offset = int(pan_amount * progress)
    if direction == "right":
        offset = pan_amount - offset

    left = (new_w - w) // 2 + offset
    top = (new_h - h) // 2
    return scaled.crop((left, top, left + w, top + h))
