#!/usr/bin/env python3
"""Demo video generator CLI.

Usage:
    python generate.py --project ai-enabled-qa
    python generate.py --project all
    python generate.py --list
"""

import argparse
import sys
from pathlib import Path

import yaml

from tts import generate_narration
from assembler import assemble_video


CONFIGS_DIR = Path(__file__).parent / "configs"
NARRATIONS_DIR = Path(__file__).parent / "narrations"
PORTFOLIO_ROOT = Path(__file__).parent.parent.parent
OUTPUT_DIR = PORTFOLIO_ROOT / "assets" / "videos"


def load_config(project_name: str) -> dict:
    """Load a project's YAML configuration."""
    config_path = CONFIGS_DIR / f"{project_name}.yaml"
    if not config_path.exists():
        print(f"Error: Config not found: {config_path}")
        sys.exit(1)

    with open(config_path) as f:
        return yaml.safe_load(f)


def list_configs() -> list[str]:
    """List all available project configs."""
    return sorted(p.stem for p in CONFIGS_DIR.glob("*.yaml"))


def generate_project_demo(project_name: str) -> Path:
    """Generate a demo video for a single project."""
    print(f"\n{'='*60}")
    print(f"  Generating demo: {project_name}")
    print(f"{'='*60}\n")

    config = load_config(project_name)
    voice = config.get("voice", "nova")
    slides = config["slides"]
    base_dir = str(Path(__file__).parent)

    # Step 1: Generate TTS audio for each slide
    print("[1/3] Generating narration audio...")
    audio_paths = []
    for i, slide in enumerate(slides):
        narration_text = slide.get("narration", "")
        if not narration_text:
            # Create silent placeholder
            audio_path = NARRATIONS_DIR / project_name / f"slide_{i:02d}_silent.mp3"
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            generate_narration(".", str(audio_path), voice=voice)
        else:
            audio_path = NARRATIONS_DIR / project_name / f"slide_{i:02d}.mp3"
            audio_path.parent.mkdir(parents=True, exist_ok=True)
            generate_narration(narration_text, str(audio_path), voice=voice)
        audio_paths.append(str(audio_path))

    # Step 2: Assemble video
    print("\n[2/3] Assembling video...")
    output_path = OUTPUT_DIR / f"{project_name}-demo.mp4"

    result = assemble_video(
        slides=slides,
        audio_paths=audio_paths,
        output_path=str(output_path),
        base_dir=base_dir,
    )

    # Step 3: Report
    size_mb = result.stat().st_size / (1024 * 1024)
    print(f"\n[3/3] Done! Output: {result}")
    print(f"  Size: {size_mb:.1f} MB")

    return result


def main():
    parser = argparse.ArgumentParser(description="Generate AI-narrated demo videos")
    parser.add_argument("--project", help="Project name or 'all'")
    parser.add_argument("--list", action="store_true", help="List available configs")
    args = parser.parse_args()

    if args.list:
        configs = list_configs()
        if not configs:
            print("No configs found. Add YAML files to tools/demo-generator/configs/")
        else:
            print("Available projects:")
            for name in configs:
                print(f"  - {name}")
        return

    if not args.project:
        parser.print_help()
        return

    if args.project == "all":
        for name in list_configs():
            generate_project_demo(name)
    else:
        generate_project_demo(args.project)


if __name__ == "__main__":
    main()
