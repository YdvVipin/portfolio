"""OpenAI TTS narration generator."""

import os
from pathlib import Path
from openai import OpenAI


def generate_narration(
    text: str,
    output_path: str,
    voice: str = "nova",
    model: str = "tts-1",
) -> Path:
    """Generate speech audio from text using OpenAI TTS API.

    Args:
        text: The narration script text.
        output_path: Where to save the MP3 file.
        voice: OpenAI voice name (alloy, echo, fable, onyx, nova, shimmer).
        model: TTS model (tts-1 or tts-1-hd).

    Returns:
        Path to the generated audio file.
    """
    client = OpenAI()  # Uses OPENAI_API_KEY env var

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text,
    )

    response.stream_to_file(str(output))
    print(f"  [TTS] Generated: {output}")
    return output
