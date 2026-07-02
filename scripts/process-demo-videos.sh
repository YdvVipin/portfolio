#!/usr/bin/env bash
set -euo pipefail

# process-demo-videos.sh
# Enhanced processing pipeline:
# - Rasterize poster SVGs to PNG
# - Create intro/outro clips
# - Ensure input videos have audio
# - Concatenate intro + original + outro
# - Burn subtitles (optional)
# - Mix voiceover + background music (optional)
# - Output optimized MP4s to assets/videos/processed

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ASSETS="$ROOT/assets"
POSTERS_DIR="$ASSETS/posters"
VIDEOS_DIR="$ASSETS/videos"
SUBS_DIR="$ASSETS/subs"
VOICE_DIR="$ASSETS/audio/voice"
MUSIC_FILE=""
OUT_DIR="$VIDEOS_DIR/processed"
TMP_DIR="$ROOT/.tmp_video_work"

mkdir -p "$OUT_DIR" "$TMP_DIR" "$VOICE_DIR"

CRF=23
BURN_SUBS=1
INTRO_SEC=3
OUTRO_SEC=4
SCALE=1280:720
DUCK_MUSIC=0

while [[ ${#@} -gt 0 ]]; do
  case "$1" in
    --no-subs) BURN_SUBS=0; shift ;;
    --crf) CRF="$2"; shift 2 ;;
    --crf=*) CRF="${1#*=}"; shift ;;
    --intro) INTRO_SEC="$2"; shift 2 ;;
    --outro) OUTRO_SEC="$2"; shift 2 ;;
    --music) MUSIC_FILE="$2"; shift 2 ;;
    --duck-music) DUCK_MUSIC=1; shift ;;
    --voice-dir) VOICE_DIR="$2"; shift 2 ;;
    --help) echo "Usage: $0 [--no-subs] [--crf N] [--music music.mp3] [--voice-dir path] [--duck-music]"; exit 0 ;;
    *) shift ;;
  esac
done

# Demos list: base name => poster svg name, srt name
declare -A POSTS
POSTS[playwright-bdd-framework]="playwright-bdd-framework-poster.svg|playwright-bdd-framework-demo.srt"
POSTS[ai-enabled-qa]="ai-enabled-qa-poster.svg|ai-enabled-qa-demo.srt"
POSTS[multi-agent-orchestration]="multi-agent-orchestration-poster.svg|multi-agent-orchestration-demo.srt"

# Check dependencies
command -v ffmpeg >/dev/null 2>&1 || { echo "ffmpeg not found in PATH. Install ffmpeg and retry."; exit 1; }
command -v ffprobe >/dev/null 2>&1 || { echo "ffprobe not found in PATH. Install ffmpeg (includes ffprobe) and retry."; exit 1; }

# Helper: ensure a file has an audio track; if not, create a temp with silent audio
ensure_audio() {
  local infile="$1"
  local outfile="$2"
  if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$infile" | grep -q .; then
    ffmpeg -y -i "$infile" -c:v libx264 -c:a aac -b:a 128k -pix_fmt yuv420p -movflags +faststart "$outfile"
  else
    ffmpeg -y -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i "$infile" -shortest -c:v libx264 -c:a aac -b:a 128k -pix_fmt yuv420p -movflags +faststart "$outfile"
  fi
}

# Mix voice + music into a single audio track. Produces output at $3 (final file)
mix_voice_and_music() {
  local base_video="$1"   # input video path
  local voice_file="$2"   # voice .wav (optional)
  local music_file="$3"   # music .mp3 (optional)
  local out_file="$4"     # output path
  local tmp_audio="$TMP_DIR/tmp_mixed_audio.aac"

  # If no voice and no music, just copy
  if [[ -z "$voice_file" && -z "$music_file" ]]; then
    cp "$base_video" "$out_file"
    return 0
  fi

  # If voice only: replace audio stream
  if [[ -n "$voice_file" && -z "$music_file" ]]; then
    ffmpeg -y -i "$base_video" -i "$voice_file" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest "$out_file"
    return 0
  fi

  # If music only: mix music at low volume
  if [[ -z "$voice_file" && -n "$music_file" ]]; then
    ffmpeg -y -i "$base_video" -i "$music_file" -filter_complex "[1:a]volume=0.18[m];[0:a][m]amix=inputs=2:weights=1 0.3:dropout_transition=2[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest "$out_file"
    return 0
  fi

  # Both voice + music: either duck music while voice present or simple mix
  if [[ "$DUCK_MUSIC" -eq 1 ]]; then
    # Simple ducking: reduce music volume when voice present using sidechain-like approach
    # Note: this is a pragmatic approach and may need tuning per file
    ffmpeg -y -i "$base_video" -i "$voice_file" -i "$music_file" -filter_complex \
      "[2:a]volume=0.6[m];[1:a]aresample=44100[voice];[m][voice]sidechaincompress=threshold=0.1:ratio=10[mc];[0:a][mc]amix=inputs=2:weights=1 1:duration=shortest[aout]" \
      -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest "$out_file"
  else
    # Simple mix with music lowered
    ffmpeg -y -i "$base_video" -i "$voice_file" -i "$music_file" -filter_complex "[2:a]volume=0.18[m];[1:a]volume=1.0[voice];[voice][m]amix=inputs=2:weights=1 0.3:dropout_transition=2[aout]" -map 0:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -shortest "$out_file"
  fi
}

# Process each demo
for key in "${!POSTS[@]}"; do
  IFS='|' read -r poster_svg srt_file <<< "${POSTS[$key]}"
  echo "\n--- Processing: $key ---"

  POSTER_SVG="$POSTERS_DIR/$poster_svg"
  POSTER_PNG="$TMP_DIR/${poster_svg%.svg}.png"
  INPUT_VIDEO="$VIDEOS_DIR/$key-demo.mp4"
  SRT_PATH="$SUBS_DIR/$srt_file"
  TMP_INTRO="$TMP_DIR/${key}_intro.mp4"
  TMP_OUTRO="$TMP_DIR/${key}_outro.mp4"
  TMP_INPUT_WITH_AUDIO="$TMP_DIR/${key}_input_with_audio.mp4"
  CONCATED="$TMP_DIR/${key}_concat.mp4"
  FINAL_OUT="$OUT_DIR/${key}-final.mp4"
  FINAL_OUT_SUBS="$OUT_DIR/${key}-final-subs.mp4"
  FINAL_WITH_VOICE="$OUT_DIR/${key}-final-voice.mp4"

  # Verify poster exists
  if [[ ! -f "$POSTER_SVG" ]]; then
    echo "Poster SVG not found: $POSTER_SVG — skipping $key"
    continue
  fi

  # Convert SVG -> PNG (try imagemagick convert, fallback to ffmpeg raster)
  if command -v convert >/dev/null 2>&1; then
    echo "Converting SVG to PNG via ImageMagick convert: $POSTER_SVG -> $POSTER_PNG"
    convert -density 150 "$POSTER_SVG" -resize ${SCALE%%:*}x${SCALE##*:} "$POSTER_PNG"
  else
    echo "ImageMagick not found, using ffmpeg to rasterize SVG"
    ffmpeg -y -i "$POSTER_SVG" -vf "scale=${SCALE}" -frames:v 1 "$POSTER_PNG"
  fi

  # Create intro/outro clips with silent audio
  echo "Creating intro ($INTRO_SEC s) and outro ($OUTRO_SEC s)"
  ffmpeg -y -loop 1 -i "$POSTER_PNG" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -c:v libx264 -t $INTRO_SEC -pix_fmt yuv420p -c:a aac -b:a 128k -shortest "$TMP_INTRO"
  ffmpeg -y -loop 1 -i "$POSTER_PNG" -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -c:v libx264 -t $OUTRO_SEC -pix_fmt yuv420p -c:a aac -b:a 128k -shortest "$TMP_OUTRO"

  # Verify input video
  if [[ ! -f "$INPUT_VIDEO" ]]; then
    echo "Input demo video not found: $INPUT_VIDEO — skipping $key"
    continue
  fi

  # Ensure input has an audio track (creates TMP_INPUT_WITH_AUDIO)
  echo "Ensuring input video has audio (or adding silent audio)"
  ensure_audio "$INPUT_VIDEO" "$TMP_INPUT_WITH_AUDIO"

  # Concat intro + input + outro using filter_complex concat
  echo "Concatenating intro + input + outro"
  ffmpeg -y -i "$TMP_INTRO" -i "$TMP_INPUT_WITH_AUDIO" -i "$TMP_OUTRO" -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" -c:v libx264 -crf $CRF -preset medium -c:a aac -b:a 128k -movflags +faststart "$CONCATED"

  # Optimize final (re-encode to target settings)
  echo "Optimizing output -> $FINAL_OUT"
  ffmpeg -y -i "$CONCATED" -c:v libx264 -crf $CRF -preset medium -c:a aac -b:a 128k -movflags +faststart "$FINAL_OUT"

  # Burn subtitles if requested and SRT exists
  if [[ $BURN_SUBS -eq 1 && -f "$SRT_PATH" ]]; then
    echo "Burning subtitles from $SRT_PATH -> $FINAL_OUT_SUBS"
    ffmpeg -y -i "$FINAL_OUT" -vf "subtitles=${SRT_PATH//:/\\:}:force_style='FontName=DejaVu Sans,FontSize=20,PrimaryColour=&H00FFFFFF&'" -c:a copy "$FINAL_OUT_SUBS"
  else
    echo "Skipping subtitle burn (either disabled or SRT not found)"
  fi

  # If voice file exists for this demo, mix voice + optional music
  VOICE_FILE_CANDIDATE="$VOICE_DIR/${key}.wav"
  if [[ -f "$VOICE_FILE_CANDIDATE" || -n "$MUSIC_FILE" ]]; then
    # choose base input: with subs if created, otherwise final
    BASE_IN="$FINAL_OUT"
    if [[ -f "$FINAL_OUT_SUBS" ]]; then BASE_IN="$FINAL_OUT_SUBS"; fi

    echo "Mixing voice/music for $key (voice: ${VOICE_FILE_CANDIDATE}, music: ${MUSIC_FILE:-none})"
    mix_voice_and_music "$BASE_IN" "${VOICE_FILE_CANDIDATE}" "$MUSIC_FILE" "$FINAL_WITH_VOICE"
    echo "Final with voice: $FINAL_WITH_VOICE"
  fi

  echo "Finished $key -> outputs in $OUT_DIR"

done

# Cleanup note
echo "\nAll done. Processed videos are in: $OUT_DIR"
echo "Temporary files are under: $TMP_DIR (you can delete when happy)"

echo "Example run to process everything (from MLProjects/Portfolio):"
echo "  bash ./scripts/process-demo-videos.sh --crf 23 --music assets/audio/music/background.mp3 --voice-dir assets/audio/voice --duck-music"

echo "To skip subtitles: --no-subs"

exit 0
