---
name: video-transcript
description: Transcribe a local video or audio file into a timestamped verbatim transcript (any language), optionally translate it, and deliver a bilingual transcript document. Use for requests like "总结这个视频的逐字脚本", transcribing creator/KOL videos, interviews, or voice notes. Not for real-time meeting captions or subtitle-file (.srt) authoring.
metadata:
  short-description: Video/audio to verbatim transcript + translation
---

# Video Transcript

Produce a verbatim (逐字) transcript from a local media file, then translate and format it for the user.

## Workflow

1. **Locate the media file** and confirm duration/stream layout:
   ```python
   import av
   c = av.open(path); print(float(c.duration)/1e6); [print(s.type) for s in c.streams]
   ```

2. **Prepare the environment** (one-time per machine):
   - Use the bundled Python runtime from `load_workspace_dependencies` when available.
   - `pip install faster-whisper` — it pulls in PyAV, so **no separate ffmpeg install is needed**.
   - The first run downloads the Whisper model from Hugging Face (network + approval needed; a few hundred MB, cached afterwards).

3. **Transcribe** with `scripts/transcribe.py`:
   ```
   python scripts/transcribe.py <input> [--model small] [--language es] [--out transcript_raw.json]
   ```
   - Default model `small` is a good speed/accuracy tradeoff on CPU. Offer `medium` or `large-v3` when the user wants higher accuracy or the audio is noisy.
   - Language is auto-detected; pass `--language` only when detection is wrong or the user says the language. For Brazil-market content, watch for **Portuguese vs Spanish** misdetection.
   - The script decodes audio itself (16 kHz mono float32) — do NOT call `faster_whisper`'s `decode_audio` with a file path; some PyAV builds reject its `metadata_errors` argument.
   - On Windows, set `PYTHONIOENCODING=utf-8` before running, or non-ASCII transcript text will crash printing with a GBK `UnicodeEncodeError`.

4. **Review and correct** the raw segments before presenting:
   - ASR routinely mangles **brand and product names** (e.g. DJI → "Dejotaí", Mic Mini → "MiG Mini"). Fix them from context and note the corrections to the user.
   - Keep every segment — this is a verbatim transcript, not a summary.

5. **Deliver** a Markdown document in the workspace containing:
   - Header: source file, duration, detected language + confidence, topic.
   - Timestamped segments in `[MM:SS - MM:SS]` form, each with the original text and (when the user works in another language) a translation line.
   - A short bullet summary of content highlights at the end.
   - A caveat that output is machine transcription and details should be checked against the original video.

## Constraints

- Transcription of long files is CPU-bound; roughly real-time or faster with `small`/int8. Warn the user for files longer than ~30 minutes and suggest running in the background.
- Model download and pip install require network access — request escalation with a clear justification if the sandbox blocks them.
- Do not upload the user's media anywhere; all processing is local.
