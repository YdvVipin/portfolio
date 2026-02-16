"""Assemble frames and audio into final MP4 video using moviepy."""

from pathlib import Path
from PIL import Image
import numpy as np
from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    VideoClip,
)

from frames_gen import (
    generate_image_frame,
    generate_code_frame,
    apply_zoom_effect,
    apply_pan_effect,
)


FPS = 24
RESOLUTION = (1280, 720)


def _frame_to_array(frame: Image.Image) -> np.ndarray:
    """Convert PIL Image to numpy array for moviepy."""
    return np.array(frame.convert("RGB"))


def _create_slide_clip(
    slide_config: dict,
    audio_path: str,
    base_dir: str,
) -> VideoClip:
    """Create a video clip for a single slide with effects."""

    # Get audio duration
    audio = AudioFileClip(audio_path)
    duration = audio.duration + 0.5  # Add 0.5s padding

    # Generate base frame
    if "image" in slide_config:
        img_path = str(Path(base_dir) / slide_config["image"])
        title = slide_config.get("title")
        base_frame = generate_image_frame(img_path, title, RESOLUTION)
    elif "code_snippet" in slide_config:
        filename = slide_config.get("filename", "code.py")
        base_frame = generate_code_frame(
            slide_config["code_snippet"], filename, RESOLUTION
        )
    else:
        # Blank frame with text
        base_frame = Image.new("RGB", RESOLUTION, (10, 10, 15))

    effect = slide_config.get("effect", "fade")
    base_array = _frame_to_array(base_frame)

    # Apply effect
    if effect in ("zoom_in", "zoom_out"):
        zoom_in = effect == "zoom_in"
        clip = ImageClip(base_array).with_duration(duration)
        if zoom_in:
            clip = clip.resized(lambda t: 1 + 0.15 * (t / duration))
        else:
            clip = clip.resized(lambda t: 1.15 - 0.15 * (t / duration))

    elif effect in ("pan_left", "pan_right"):
        total_frames = int(duration * FPS)
        direction = "left" if effect == "pan_left" else "right"
        frames_cache = []
        for i in range(total_frames):
            progress = i / max(total_frames - 1, 1)
            f = apply_pan_effect(base_frame, progress, direction)
            frames_cache.append(_frame_to_array(f))

        def make_frame_pan(t):
            idx = min(int(t * FPS), len(frames_cache) - 1)
            return frames_cache[idx]

        clip = VideoClip(make_frame_pan, duration=duration)

    else:  # fade, typewriter, or default
        clip = ImageClip(base_array).with_duration(duration)

    # Attach audio
    clip = clip.with_audio(audio)

    return clip


def assemble_video(
    slides: list[dict],
    audio_paths: list[str],
    output_path: str,
    base_dir: str,
    crossfade: float = 0.5,
) -> Path:
    """Assemble all slides into a single MP4 video.

    Args:
        slides: List of slide config dicts from YAML.
        audio_paths: List of audio file paths, one per slide.
        output_path: Where to save the final MP4.
        base_dir: Base directory for resolving relative image paths.
        crossfade: Seconds of crossfade between slides.

    Returns:
        Path to the output video.
    """
    clips = []
    for slide, audio_path in zip(slides, audio_paths):
        clip = _create_slide_clip(slide, audio_path, base_dir)
        clips.append(clip)

    # Concatenate with crossfade
    if len(clips) > 1:
        final = concatenate_videoclips(clips, method="compose", padding=-crossfade)
    else:
        final = clips[0]

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    final.write_videofile(
        str(output),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        logger="bar",
    )

    print(f"  [Video] Output: {output}")
    return output
