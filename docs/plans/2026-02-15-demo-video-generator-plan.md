# Demo Video Generator — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a Python pipeline that generates AI-narrated demo videos for portfolio projects and embed them with a custom video player.

**Architecture:** A CLI tool reads YAML configs per project, calls OpenAI TTS API for narration audio, generates animated slide frames with Pillow, and assembles final MP4s with moviepy. Videos are embedded in existing project detail pages via a custom dark-themed HTML5 video player.

**Tech Stack:** Python 3.10+, OpenAI TTS API, moviepy, Pillow, pyyaml, ffmpeg

**Design doc:** `docs/plans/2026-02-15-demo-video-generator-design.md`

---

### Task 1: Project Scaffolding & Dependencies

**Files:**
- Create: `tools/demo-generator/requirements.txt`
- Create: `tools/demo-generator/.gitignore`
- Create: `tools/demo-generator/configs/` (empty dir with .gitkeep)
- Modify: `.gitignore` (root — add video assets)

**Step 1: Create directory structure**

```bash
mkdir -p tools/demo-generator/{configs,narrations,frames,screenshots}
```

**Step 2: Create requirements.txt**

```
# tools/demo-generator/requirements.txt
moviepy>=2.0.0
openai>=1.0.0
Pillow>=10.0.0
pyyaml>=6.0
playwright>=1.40.0
```

**Step 3: Create .gitignore for generated artifacts**

```
# tools/demo-generator/.gitignore
narrations/
frames/
screenshots/
*.mp3
*.mp4
__pycache__/
```

**Step 4: Add video assets to root .gitignore**

Append to the existing `.gitignore`:
```
# Generated demo videos (too large for git)
assets/videos/*.mp4
```

**Step 5: Create Python virtual env and install**

```bash
cd tools/demo-generator
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Step 6: Commit**

```bash
git add tools/demo-generator/requirements.txt tools/demo-generator/.gitignore .gitignore
git commit -m "feat: scaffold demo video generator tool"
```

---

### Task 2: TTS Narration Module

**Files:**
- Create: `tools/demo-generator/tts.py`

**Step 1: Create the TTS module**

This module takes a text string and voice name, calls OpenAI TTS API, saves MP3.

```python
# tools/demo-generator/tts.py
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
```

**Step 2: Quick manual test**

```bash
cd tools/demo-generator
source .venv/bin/activate
export OPENAI_API_KEY="sk-..."
python3 -c "
from tts import generate_narration
generate_narration('Hello, this is a test narration.', 'narrations/test.mp3')
"
# Expected: narrations/test.mp3 created, playable audio
```

**Step 3: Commit**

```bash
git add tools/demo-generator/tts.py
git commit -m "feat: add TTS narration module using OpenAI API"
```

---

### Task 3: Slide Frame Generator (Pillow)

**Files:**
- Create: `tools/demo-generator/frames_gen.py`

**Step 1: Create the frame generator module**

Handles two slide types: image-based slides and code snippet slides. Applies visual effects.

```python
# tools/demo-generator/frames_gen.py
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

    # Add subtle rounded border effect
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
```

**Step 2: Quick manual test**

```bash
python3 -c "
from frames_gen import generate_code_frame, generate_image_frame
# Test code frame
frame = generate_code_frame('def hello():\n    print(\"Hello World\")\n\nhello()', 'test.py')
frame.save('frames/test_code.png')
print('Code frame saved')
"
# Expected: frames/test_code.png — dark terminal-style code display
```

**Step 3: Commit**

```bash
git add tools/demo-generator/frames_gen.py
git commit -m "feat: add Pillow frame generator for image and code slides"
```

---

### Task 4: Video Assembly Module (moviepy)

**Files:**
- Create: `tools/demo-generator/assembler.py`

**Step 1: Create the video assembler**

Takes generated frames + audio and produces final MP4.

```python
# tools/demo-generator/assembler.py
"""Assemble frames and audio into final MP4 video using moviepy."""

from pathlib import Path
from PIL import Image
import numpy as np
from moviepy import (
    ImageClip,
    AudioFileClip,
    CompositeVideoClip,
    concatenate_videoclips,
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
) -> CompositeVideoClip:
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

    # Apply effect by generating frames
    if effect in ("zoom_in", "zoom_out"):
        zoom_in = effect == "zoom_in"

        def make_frame(t):
            progress = t / duration
            frame = apply_zoom_effect(base_frame, progress, zoom_in=zoom_in)
            return _frame_to_array(frame)

        clip = ImageClip(_frame_to_array(base_frame)).with_duration(duration)
        clip = clip.transform(
            lambda get_frame, t: make_frame(t),
            apply_to="mask" if False else [],
        )
        # Simpler approach: use static frame with moviepy resize effect
        clip = ImageClip(_frame_to_array(base_frame)).with_duration(duration)
        if zoom_in:
            clip = clip.resized(lambda t: 1 + 0.15 * (t / duration))
        else:
            clip = clip.resized(lambda t: 1.15 - 0.15 * (t / duration))

    elif effect in ("pan_left", "pan_right"):
        total_frames = int(duration * FPS)
        frames = []
        direction = "left" if effect == "pan_left" else "right"
        for i in range(total_frames):
            progress = i / max(total_frames - 1, 1)
            f = apply_pan_effect(base_frame, progress, direction)
            frames.append(_frame_to_array(f))

        def make_frame_pan(t):
            idx = min(int(t * FPS), len(frames) - 1)
            return frames[idx]

        clip = ImageClip(_frame_to_array(base_frame)).with_duration(duration)
        # Use pre-rendered frames
        from moviepy import VideoClip
        clip = VideoClip(make_frame_pan, duration=duration)

    elif effect == "typewriter" and "code_snippet" in slide_config:
        # For typewriter, we just use the full code frame (animation is complex)
        # Future enhancement: render progressive code reveal
        clip = ImageClip(_frame_to_array(base_frame)).with_duration(duration)

    else:  # fade or default
        clip = ImageClip(_frame_to_array(base_frame)).with_duration(duration)

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
```

**Step 2: Commit**

```bash
git add tools/demo-generator/assembler.py
git commit -m "feat: add moviepy video assembler with zoom/pan effects"
```

---

### Task 5: Main CLI Entry Point

**Files:**
- Create: `tools/demo-generator/generate.py`

**Step 1: Create the main CLI**

Orchestrates the full pipeline: read config → TTS → frames → assemble.

```python
#!/usr/bin/env python3
# tools/demo-generator/generate.py
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
            # Generate minimal audio
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
```

**Step 2: Commit**

```bash
git add tools/demo-generator/generate.py
git commit -m "feat: add main CLI for demo video generation pipeline"
```

---

### Task 6: First Project Config (QA AI Enabler)

**Files:**
- Create: `tools/demo-generator/configs/ai-enabled-qa.yaml`

**Step 1: Write the YAML config with narration scripts**

Note: Image paths reference screenshots that will be captured in Task 8. For now, use existing project page visuals.

```yaml
# tools/demo-generator/configs/ai-enabled-qa.yaml
project: ai-enabled-qa
title: "QA Automation AI Enabler"
voice: "nova"
resolution: [1280, 720]

slides:
  - code_snippet: |
      # QA Automation AI Enabler
      # 50,000+ Lines of Code
      # 72 FastAPI Endpoints
      # 18 Specialized AI Agents
      # Built with: React + FastAPI + AI/ML
    filename: "project-overview.py"
    narration: >
      Meet QA Automation AI Enabler — my flagship project.
      Over fifty thousand lines of code, seventy-two FastAPI endpoints,
      and eighteen specialized AI agents working together
      to automate the entire QA lifecycle.
    effect: "fade"

  - code_snippet: |
      # Architecture: 3-Layer Pipeline

      Layer 1: Browser Recorder (Chrome Extension)
        → Captures user interactions in real-time

      Layer 2: Deterministic Parser (FastAPI)
        → Converts raw events to structured actions

      Layer 3: AI Code Generator (Multi-LLM)
        → Generates production-ready Playwright tests
    filename: "architecture.md"
    narration: >
      The architecture follows a three-layer pipeline.
      First, a Chrome extension records browser interactions.
      Then, a deterministic parser structures raw events into actions.
      Finally, a multi-LLM AI layer generates production-ready
      Playwright test scripts with self-healing locators.
    effect: "fade"

  - code_snippet: |
      @app.post("/api/generate-tests")
      async def generate_tests(spec: TestSpec):
          """Generate Playwright tests from recorded actions."""
          agent = TestGeneratorAgent(
              model="gpt-4",
              strategy="deterministic_first"
          )
          result = await agent.run(spec)
          return {"tests": result.code, "confidence": result.score}

      @app.post("/api/self-heal")
      async def self_heal(broken: BrokenLocator):
          """AI-powered locator self-healing."""
          healer = SelfHealingAgent()
          return await healer.fix(broken)
    filename: "api/endpoints.py"
    narration: >
      Here's a glimpse at the API layer. Each endpoint triggers
      a specialized AI agent. The test generator uses a
      deterministic-first strategy — AI only kicks in when
      rule-based generation isn't confident enough.
      The self-healing agent automatically fixes broken locators
      when the UI changes.
    effect: "typewriter"

  - code_snippet: |
      class AgentOrchestrator:
          """Coordinates 18 specialized AI agents."""

          agents = {
              "test_generator": TestGeneratorAgent,
              "locator_healer": SelfHealingAgent,
              "assertion_builder": AssertionAgent,
              "data_factory": TestDataAgent,
              "report_analyzer": ReportAnalysisAgent,
              "code_reviewer": CodeReviewAgent,
              # ... 12 more specialized agents
          }

          async def run_pipeline(self, task: QATask):
              plan = await self.planner.create_plan(task)
              for step in plan.steps:
                  agent = self.agents[step.agent_type]()
                  result = await agent.execute(step)
                  await self.memory.store(result)
    filename: "agents/orchestrator.py"
    narration: >
      The heart of the system is the Agent Orchestrator.
      Eighteen specialized agents — from test generation
      to self-healing locators to intelligent report analysis.
      Each agent has a focused responsibility, and the orchestrator
      coordinates them through a planning pipeline with shared memory.
    effect: "zoom_in"

  - code_snippet: |
      # React Dashboard
      # ┌─────────────────────────────────────┐
      # │  QA AI Enabler         [Settings]   │
      # ├─────────┬───────────────────────────┤
      # │ Record  │  Generated Tests     [▶]  │
      # │ History │  ─────────────────────     │
      # │         │  test_login.spec.ts        │
      # │ Agents  │  test_checkout.spec.ts     │
      # │ Status  │  test_search.spec.ts       │
      # │         │                             │
      # │ Reports │  Coverage: 94.2%           │
      # └─────────┴───────────────────────────┘
    filename: "dashboard-layout.txt"
    narration: >
      The React dashboard brings it all together.
      Record browser sessions, view generated test scripts,
      monitor agent status in real-time, and track test coverage.
      Everything is designed for QA engineers who want
      AI-powered automation without the complexity.
    effect: "fade"

  - code_snippet: |
      # Built with AI-Assisted Development
      # Using Agentic AI throughout the process

      # This project demonstrates:
      #   ✓ Full-stack AI integration (React + FastAPI)
      #   ✓ Multi-agent orchestration (18 agents)
      #   ✓ Production-ready API design (72 endpoints)
      #   ✓ Self-healing test automation
      #   ✓ AI-assisted development workflow

      # github.com/YdvVipin
    filename: "README.md"
    narration: >
      QA Automation AI Enabler was built using AI-assisted
      development with agentic AI throughout the process.
      It represents the intersection of QA engineering expertise
      and modern AI — exactly where testing is headed.
      Check out the full source code on GitHub.
    effect: "zoom_out"
```

**Step 2: Commit**

```bash
git add tools/demo-generator/configs/ai-enabled-qa.yaml
git commit -m "feat: add QA AI Enabler demo config with narration scripts"
```

---

### Task 7: Configs for Tier-1 Projects (Multi-Agent & Playwright)

**Files:**
- Create: `tools/demo-generator/configs/multi-agent-orchestration.yaml`
- Create: `tools/demo-generator/configs/playwright-bdd-framework.yaml`

**Step 1: Create Multi-Agent Orchestration config**

```yaml
# tools/demo-generator/configs/multi-agent-orchestration.yaml
project: multi-agent-orchestration
title: "Multi-Agent Orchestration System"
voice: "nova"
resolution: [1280, 720]

slides:
  - code_snippet: |
      # Multi-Agent Orchestration System
      # 5 Specialized AI Agents
      # 5 MCP (Model Context Protocol) Servers
      # Built with: CrewAI + LangChain + MCP
    filename: "project-overview.py"
    narration: >
      This is my Multi-Agent Orchestration System.
      Five specialized AI agents coordinated through
      five MCP servers, built on CrewAI and LangChain.
      It demonstrates how multiple AI agents can collaborate
      on complex tasks autonomously.
    effect: "fade"

  - code_snippet: |
      # Agent Architecture

      Agent 1: Research Agent
        → Gathers and synthesizes information
        → Tools: Web search, document parsing

      Agent 2: Analysis Agent
        → Processes and evaluates data
        → Tools: Data analysis, pattern matching

      Agent 3: Code Agent
        → Generates and reviews code
        → Tools: Code execution, linting

      Agent 4: QA Agent
        → Tests and validates outputs
        → Tools: Test runner, assertion engine

      Agent 5: Orchestrator Agent
        → Plans and delegates to other agents
        → Tools: Task planner, memory store
    filename: "agents/README.md"
    narration: >
      Five agents, each with a clear specialty.
      Research, Analysis, Code Generation, QA Validation,
      and an Orchestrator that plans and delegates.
      Each agent has its own toolset and communicates
      through the Model Context Protocol.
    effect: "zoom_in"

  - code_snippet: |
      from crewai import Agent, Task, Crew
      from langchain.tools import Tool

      research_agent = Agent(
          role="Research Specialist",
          goal="Gather comprehensive information",
          tools=[web_search, doc_parser],
          llm=ChatOpenAI(model="gpt-4")
      )

      crew = Crew(
          agents=[research, analysis, coder, qa, orchestrator],
          tasks=task_pipeline,
          process=Process.hierarchical,
          manager_llm=ChatOpenAI(model="gpt-4")
      )

      result = crew.kickoff()
    filename: "orchestration/crew.py"
    narration: >
      The implementation uses CrewAI's hierarchical process.
      A manager LLM coordinates the crew, delegating tasks
      based on each agent's specialization.
      LangChain provides the tool integrations and
      chain-of-thought reasoning capabilities.
    effect: "typewriter"

  - code_snippet: |
      # MCP Server Architecture

      Server 1: File System Server
        → Read/write project files

      Server 2: Database Server
        → Query and store structured data

      Server 3: API Server
        → External API integrations

      Server 4: Code Execution Server
        → Sandboxed code runner

      Server 5: Memory Server
        → Shared context and state
    filename: "mcp/servers.md"
    narration: >
      Five MCP servers provide the infrastructure layer.
      File system access, database operations, external APIs,
      sandboxed code execution, and a shared memory server.
      This separation of concerns makes the system
      modular and secure.
    effect: "pan_left"

  - code_snippet: |
      # Built with AI-Assisted Development
      # Using Agentic AI (CrewAI + LangChain)

      # Key Achievements:
      #   ✓ 5 autonomous AI agents
      #   ✓ 5 MCP protocol servers
      #   ✓ Hierarchical task delegation
      #   ✓ Shared memory and context
      #   ✓ Production-ready architecture

      # github.com/YdvVipin
    filename: "README.md"
    narration: >
      This project showcases production-grade multi-agent
      architecture. Five agents working together through
      the Model Context Protocol — this is the future
      of AI-powered software engineering.
    effect: "zoom_out"
```

**Step 2: Create Playwright BDD Framework config**

```yaml
# tools/demo-generator/configs/playwright-bdd-framework.yaml
project: playwright-bdd-framework
title: "Playwright BDD Framework"
voice: "nova"
resolution: [1280, 720]

slides:
  - code_snippet: |
      # Playwright BDD Framework
      # TypeScript + Cucumber BDD
      # 3 AI Agents for Smart Testing
      # 9-Tier Intelligent Locator System
    filename: "project-overview.ts"
    narration: >
      The Playwright BDD Framework combines TypeScript,
      Cucumber BDD, and three AI agents
      with a nine-tier intelligent locator system.
      It's designed for enterprise-grade test automation.
    effect: "fade"

  - code_snippet: |
      // 9-Tier Locator Strategy

      Tier 1: data-testid (most reliable)
      Tier 2: aria-label / role
      Tier 3: CSS unique ID
      Tier 4: Text content match
      Tier 5: CSS class combination
      Tier 6: XPath relative
      Tier 7: Visual proximity
      Tier 8: AI pattern match
      Tier 9: AI fallback generation

      // Each tier has a confidence score
      // System tries Tier 1 first, falls through
    filename: "locators/strategy.ts"
    narration: >
      The nine-tier locator system is the framework's secret weapon.
      Starting from the most reliable data-testid attributes,
      falling through to ARIA labels, CSS selectors,
      text matching, and finally AI-powered pattern matching.
      Each tier has a confidence score — the system always
      picks the most reliable locator available.
    effect: "zoom_in"

  - code_snippet: |
      // Cucumber BDD Feature
      Feature: User Authentication

        Scenario: Successful login
          Given I am on the login page
          When I enter valid credentials
            | email    | test@example.com |
            | password | SecurePass123    |
          And I click the login button
          Then I should see the dashboard
          And the welcome message shows my name

      // Step Definition (TypeScript)
      Given('I am on the login page', async () => {
        await page.goto('/login');
        await locator.find('login-form').waitFor();
      });
    filename: "features/auth.feature"
    narration: >
      BDD scenarios written in plain English, backed by
      TypeScript step definitions. The framework integrates
      the intelligent locator system directly into step definitions.
      QA engineers write human-readable tests,
      and the AI handles the element-finding complexity.
    effect: "typewriter"

  - code_snippet: |
      // AI Agent Architecture

      Agent 1: Locator Intelligence Agent
        → Analyzes DOM, selects optimal locator tier
        → Self-heals broken locators automatically

      Agent 2: Test Data Agent
        → Generates context-aware test data
        → Handles edge cases and boundary values

      Agent 3: Report Analysis Agent
        → Analyzes test failures
        → Suggests fixes and identifies flaky tests
    filename: "agents/index.ts"
    narration: >
      Three AI agents enhance the framework.
      A Locator Intelligence agent that selects and heals locators.
      A Test Data agent that generates smart test data.
      And a Report Analysis agent that identifies flaky tests
      and suggests targeted fixes.
    effect: "pan_right"

  - code_snippet: |
      # Built with AI-Assisted Development

      # Key Features:
      #   ✓ TypeScript + Cucumber BDD
      #   ✓ 9-tier intelligent locator system
      #   ✓ 3 specialized AI agents
      #   ✓ Self-healing test locators
      #   ✓ AI-powered failure analysis

      # github.com/YdvVipin
    filename: "README.md"
    narration: >
      The Playwright BDD Framework proves that AI and traditional
      testing frameworks can work together beautifully.
      Nine tiers of locator intelligence, three AI agents,
      and enterprise-ready BDD — built with AI-assisted development.
    effect: "zoom_out"
```

**Step 3: Commit**

```bash
git add tools/demo-generator/configs/multi-agent-orchestration.yaml tools/demo-generator/configs/playwright-bdd-framework.yaml
git commit -m "feat: add Tier-1 project demo configs (multi-agent, playwright)"
```

---

### Task 8: Screenshot Capture Utility

**Files:**
- Create: `tools/demo-generator/capture.py`

**Step 1: Create capture script**

Uses Playwright to capture screenshots from existing project detail pages (they already have architecture diagrams and visuals in HTML).

```python
#!/usr/bin/env python3
# tools/demo-generator/capture.py
"""Capture screenshots from project detail pages using Playwright.

Usage:
    python capture.py --project ai-enabled-qa --url http://localhost:52305
    python capture.py --project ai-enabled-qa --file ../../projects/ai-enabled-qa/index.html
"""

import argparse
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


SCREENSHOTS_DIR = Path(__file__).parent / "screenshots"


async def capture_project_page(
    project_name: str,
    url: str,
    sections: list[str] | None = None,
) -> list[Path]:
    """Capture screenshots from a project's detail page.

    Args:
        project_name: Name for the output directory.
        url: URL of the project page.
        sections: CSS selectors for sections to capture. If None, captures full page.
    """
    output_dir = SCREENSHOTS_DIR / project_name
    output_dir.mkdir(parents=True, exist_ok=True)

    captured = []

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})

        await page.goto(url, wait_until="networkidle")
        await page.wait_for_timeout(1000)  # Let animations settle

        if sections:
            for i, selector in enumerate(sections):
                try:
                    element = page.locator(selector).first
                    await element.wait_for(timeout=5000)
                    path = output_dir / f"{i+1:02d}-{selector.replace('.', '').replace('#', '')[:30]}.png"
                    await element.screenshot(path=str(path))
                    captured.append(path)
                    print(f"  [Capture] {path.name}")
                except Exception as e:
                    print(f"  [Skip] {selector}: {e}")
        else:
            # Full page screenshot
            path = output_dir / "01-full-page.png"
            await page.screenshot(path=str(path), full_page=True)
            captured.append(path)
            print(f"  [Capture] {path.name}")

            # Also capture viewport
            path = output_dir / "02-hero.png"
            await page.screenshot(path=str(path))
            captured.append(path)
            print(f"  [Capture] {path.name}")

        await browser.close()

    return captured


def main():
    parser = argparse.ArgumentParser(description="Capture project screenshots")
    parser.add_argument("--project", required=True, help="Project name")
    parser.add_argument("--url", help="URL to capture")
    parser.add_argument("--file", help="Local HTML file path")
    parser.add_argument("--sections", nargs="*", help="CSS selectors to capture")
    args = parser.parse_args()

    url = args.url
    if args.file:
        url = f"file://{Path(args.file).resolve()}"

    if not url:
        print("Error: Provide --url or --file")
        return

    asyncio.run(capture_project_page(args.project, url, args.sections))


if __name__ == "__main__":
    main()
```

**Step 2: Commit**

```bash
git add tools/demo-generator/capture.py
git commit -m "feat: add Playwright screenshot capture utility"
```

---

### Task 9: Custom Video Player (CSS)

**Files:**
- Modify: `css/style.css` — append video player styles

**Step 1: Add video player CSS to the portfolio stylesheet**

Append the following to the end of `css/style.css` (before any resume-specific styles):

```css
/* ─── Demo Video Player ───────────────────────── */
.kc-video {
  position: relative;
  margin-bottom: 48px;
  border-radius: var(--kc-radius);
  overflow: hidden;
  background: #0a0a0f;
  border: 1px solid rgba(99, 102, 241, 0.12);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.kc-video video {
  width: 100%;
  display: block;
  border-radius: var(--kc-radius);
}

.kc-video__poster {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(10, 10, 15, 0.95), rgba(17, 17, 25, 0.9));
  cursor: pointer;
  transition: opacity 0.4s ease;
  z-index: 2;
}

.kc-video__poster.hidden {
  opacity: 0;
  pointer-events: none;
}

.kc-video__play-btn {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #8b5cf6, #ec4899);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 24px rgba(99, 102, 241, 0.4);
}

.kc-video__poster:hover .kc-video__play-btn {
  transform: scale(1.1);
  box-shadow: 0 6px 32px rgba(99, 102, 241, 0.6);
}

.kc-video__play-btn svg {
  width: 32px;
  height: 32px;
  fill: white;
  margin-left: 4px;
}

.kc-video__poster-text {
  position: absolute;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 0.85rem;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.7);
  letter-spacing: 0.05em;
}

.kc-video__badge {
  position: absolute;
  top: 16px;
  left: 16px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  background: rgba(99, 102, 241, 0.15);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.25);
  backdrop-filter: blur(8px);
  z-index: 3;
}

/* Controls bar */
.kc-video__controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12px 16px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.8));
  display: flex;
  align-items: center;
  gap: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 4;
}

.kc-video:hover .kc-video__controls {
  opacity: 1;
}

.kc-video__controls button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}

.kc-video__progress {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 2px;
  cursor: pointer;
  position: relative;
}

.kc-video__progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #6366f1, #ec4899);
  border-radius: 2px;
  width: 0%;
  transition: width 0.1s linear;
}

.kc-video__time {
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  color: rgba(255, 255, 255, 0.7);
  min-width: 80px;
  text-align: right;
}

/* Demo badge on project cards (projects.html) */
.kc-card__demo-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 10px;
  border-radius: 100px;
  font-size: 0.7rem;
  font-weight: 700;
  background: rgba(99, 102, 241, 0.2);
  color: #818cf8;
  border: 1px solid rgba(99, 102, 241, 0.3);
  z-index: 2;
}

/* Fallback when no video exists */
.kc-video--coming-soon {
  padding: 60px 24px;
  text-align: center;
  background: linear-gradient(135deg, rgba(10, 10, 15, 0.95), rgba(17, 17, 25, 0.9));
  border: 1px dashed rgba(99, 102, 241, 0.2);
}

.kc-video--coming-soon p {
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.9rem;
}
```

**Step 2: Commit**

```bash
git add css/style.css
git commit -m "feat: add custom dark-themed video player CSS"
```

---

### Task 10: Video Player JavaScript

**Files:**
- Modify: `js/script.js` — add video player initialization

**Step 1: Add video player JS**

Append to `js/script.js`, add `initVideoPlayers()` call in the DOMContentLoaded listener, and add the function:

```javascript
// ─── Video Player ─────────────────────────────────
function initVideoPlayers() {
  document.querySelectorAll('.kc-video').forEach(container => {
    const video = container.querySelector('video');
    const poster = container.querySelector('.kc-video__poster');
    const playPauseBtn = container.querySelector('.kc-video__play-pause');
    const progress = container.querySelector('.kc-video__progress');
    const progressBar = container.querySelector('.kc-video__progress-bar');
    const timeDisplay = container.querySelector('.kc-video__time');

    if (!video) return;

    // Click poster to play (lazy load)
    if (poster) {
      poster.addEventListener('click', () => {
        const src = video.dataset.src;
        if (src && !video.src) {
          video.src = src;
          video.load();
        }
        video.play();
        poster.classList.add('hidden');
      });
    }

    // Play/Pause toggle
    if (playPauseBtn) {
      playPauseBtn.addEventListener('click', () => {
        if (video.paused) {
          video.play();
          if (poster) poster.classList.add('hidden');
        } else {
          video.pause();
        }
      });
    }

    // Progress bar update
    video.addEventListener('timeupdate', () => {
      if (video.duration) {
        const pct = (video.currentTime / video.duration) * 100;
        if (progressBar) progressBar.style.width = pct + '%';
        if (timeDisplay) {
          const cur = formatTime(video.currentTime);
          const dur = formatTime(video.duration);
          timeDisplay.textContent = cur + ' / ' + dur;
        }
      }
    });

    // Click progress bar to seek
    if (progress) {
      progress.addEventListener('click', (e) => {
        const rect = progress.getBoundingClientRect();
        const pct = (e.clientX - rect.left) / rect.width;
        video.currentTime = pct * video.duration;
      });
    }

    // Reset on end
    video.addEventListener('ended', () => {
      if (poster) poster.classList.remove('hidden');
      if (progressBar) progressBar.style.width = '0%';
    });
  });
}

function formatTime(seconds) {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return m + ':' + (s < 10 ? '0' : '') + s;
}
```

Also add `initVideoPlayers();` to the DOMContentLoaded event listener.

**Step 2: Commit**

```bash
git add js/script.js
git commit -m "feat: add video player JS with lazy loading and custom controls"
```

---

### Task 11: Embed Video Player in QA AI Enabler Project Page

**Files:**
- Modify: `projects/ai-enabled-qa/index.html` — add video player after hero section

**Step 1: Add video player HTML**

Insert after the closing `</section>` of the hero section (after line ~198) and before the stats bar:

```html
<!-- Demo Video -->
<section class="section" id="demo">
  <div class="container">
    <div class="section-label">Project Demo</div>
    <h2 class="section-title">Watch It In Action</h2>
    <div class="kc-video">
      <div class="kc-video__badge">AI-Generated Demo</div>
      <video data-src="../../assets/videos/ai-enabled-qa-demo.mp4" preload="none"></video>
      <div class="kc-video__poster">
        <div class="kc-video__play-btn">
          <svg viewBox="0 0 24 24"><polygon points="5,3 19,12 5,21"/></svg>
        </div>
        <div class="kc-video__poster-text">Click to play demo</div>
      </div>
      <div class="kc-video__controls">
        <button class="kc-video__play-pause" aria-label="Play/Pause">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="white"><polygon points="5,3 19,12 5,21"/></svg>
        </button>
        <div class="kc-video__progress">
          <div class="kc-video__progress-bar"></div>
        </div>
        <span class="kc-video__time">0:00 / 0:00</span>
      </div>
    </div>
  </div>
</section>
```

**Step 2: Add the video player CSS inline** (since project pages use inline styles, not the main stylesheet)

Add the video player CSS rules inside the existing `<style>` block in the project page.

**Step 3: Add the video player JS inline**

Add the `initVideoPlayers()` function and call it in the project page's inline script.

**Step 4: Commit**

```bash
git add projects/ai-enabled-qa/index.html
git commit -m "feat: embed demo video player in QA AI Enabler project page"
```

---

### Task 12: Embed in Multi-Agent & Playwright Pages

**Files:**
- Modify: `projects/multi-agent-orchestration/index.html`
- Modify: `projects/playwright-bdd-framework/index.html`

Same pattern as Task 11 — add video player HTML + inline CSS/JS after each page's hero section.

**Step 1: Add video player to Multi-Agent page**

Same HTML structure, change `data-src` to `../../assets/videos/multi-agent-orchestration-demo.mp4`.

**Step 2: Add video player to Playwright BDD page**

Same HTML structure, change `data-src` to `../../assets/videos/playwright-bdd-framework-demo.mp4`.

**Step 3: Commit**

```bash
git add projects/multi-agent-orchestration/index.html projects/playwright-bdd-framework/index.html
git commit -m "feat: embed demo video players in multi-agent and playwright pages"
```

---

### Task 13: Generate Demo Videos (Run Pipeline)

**Step 1: Set OpenAI API key**

```bash
export OPENAI_API_KEY="your-key-here"
```

**Step 2: Create assets/videos directory**

```bash
mkdir -p assets/videos
```

**Step 3: Generate QA AI Enabler demo**

```bash
cd tools/demo-generator
source .venv/bin/activate
python generate.py --project ai-enabled-qa
```

Expected: `assets/videos/ai-enabled-qa-demo.mp4` created (~15-20MB, ~2 min)

**Step 4: Generate Multi-Agent demo**

```bash
python generate.py --project multi-agent-orchestration
```

**Step 5: Generate Playwright BDD demo**

```bash
python generate.py --project playwright-bdd-framework
```

**Step 6: Verify all videos play correctly**

Open each MP4 in browser or media player. Check audio narration is clear and slides display correctly.

---

### Task 14: Test Full Integration

**Step 1: Start local dev server**

```bash
cd /Users/vipinyadav/Desktop/MLProjects/Portfolio
python3 -m http.server 52305
```

**Step 2: Verify video players work**

Open in browser:
- `http://localhost:52305/projects/ai-enabled-qa/` — click play, verify video loads and plays
- `http://localhost:52305/projects/multi-agent-orchestration/`
- `http://localhost:52305/projects/playwright-bdd-framework/`

Check: poster shows, click plays, controls work, audio is audible.

**Step 3: Test on mobile viewport**

Resize browser to 375px width, verify video player is responsive.

**Step 4: Commit any fixes**

```bash
git add -A
git commit -m "fix: video player integration polish"
```

---

### Task 15: Final Commit & Push

**Step 1: Review all changes**

```bash
git status
git log --oneline -10
```

**Step 2: Push to GitHub**

```bash
git push origin main
```

**Step 3: Verify GitHub Pages deployment**

Check `https://ydvvipin.github.io/portfolio/` loads correctly. Note: video files are gitignored, so demos won't play on GitHub Pages unless videos are committed or hosted elsewhere. Consider uploading videos to a CDN or committing them if under 25MB each.
