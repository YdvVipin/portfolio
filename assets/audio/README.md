Audio assets and TTS instructions

Structure:
- assets/audio/ssml/*.ssml  -> SSML scripts for each demo (ready for ElevenLabs or other TTS providers)
- assets/audio/voice/*.wav  -> Place generated voice WAVs here, named exactly: <demo-key>.wav
  - playwright-bdd-framework.wav
  - ai-enabled-qa.wav
  - multi-agent-orchestration.wav
- assets/audio/music/        -> Optional background music files (e.g. background.mp3)

How to generate voice WAVs (ElevenLabs example):
1) Use ElevenLabs studio or API to create a WAV from SSML. Example (pseudo):
   - Upload SSML content or synthesize via API with voice selection
   - Export 44.1kHz 16-bit WAV, mono or stereo
2) Name the files exactly and place them in assets/audio/voice/

Local TTS (e.g., tts-cli) example:
- tts --ssml assets/audio/ssml/playwright-bdd-framework.ssml --out assets/audio/voice/playwright-bdd-framework.wav

Mixing and running the pipeline:
- If you have ffmpeg locally: from MLProjects/Portfolio run:
  bash ./scripts/process-demo-videos.sh --crf 23 --music assets/audio/music/background.mp3 --voice-dir assets/audio/voice --duck-music
- To skip subtitles: add --no-subs

Notes:
- Adjust music volume and ducking as needed; ducking uses ffmpeg sidechaincompress which may need tuning depending on voice/music dynamics.
- If you want me to create voice WAVs via a TTS provider, provide API access or generate locally and upload the files.
