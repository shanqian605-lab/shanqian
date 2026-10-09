#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Transcribe a video/audio file to a timestamped verbatim transcript using faster-whisper.

Usage:
    python transcribe.py <input_file> [--model small] [--language auto] [--out transcript.json]

Notes:
- Decodes audio manually via PyAV (mono 16 kHz float32) instead of faster-whisper's
  decode_audio, because some PyAV versions reject the `metadata_errors` kwarg.
- Accepts .mov/.mp4/.mp3/.wav/.m4a etc. (anything PyAV/FFmpeg can decode).
- Prints timestamped segments to stdout and writes JSON segments to --out.
- On Windows consoles, run with PYTHONIOENCODING=utf-8 to avoid GBK encode errors.
"""
import argparse
import json
import sys

import numpy as np
import av
from av.audio.resampler import AudioResampler


def decode_audio(path: str, target_rate: int = 16000) -> np.ndarray:
    resampler = AudioResampler(format="s16", layout="mono", rate=target_rate)
    chunks = []
    container = av.open(path)
    stream = container.streams.audio[0]
    for frame in container.decode(stream):
        for rframe in resampler.resample(frame):
            chunks.append(rframe.to_ndarray().reshape(-1))
    for rframe in resampler.resample(None):  # flush
        chunks.append(rframe.to_ndarray().reshape(-1))
    container.close()
    if not chunks:
        raise RuntimeError("No audio decoded from input file.")
    return np.concatenate(chunks).astype(np.float32) / 32768.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--model", default="small",
                    help="Whisper model size: tiny/base/small/medium/large-v3 (default: small)")
    ap.add_argument("--language", default=None,
                    help="BCP-47-ish code like es/zh/en/pt; default auto-detect")
    ap.add_argument("--out", default="transcript_raw.json")
    args = ap.parse_args()

    from faster_whisper import WhisperModel

    audio = decode_audio(args.input)
    print(f"audio seconds: {len(audio)/16000:.1f}", flush=True)

    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        audio, beam_size=5, vad_filter=True, language=args.language
    )
    print(f"language={info.language} prob={info.language_probability:.2f}", flush=True)

    out = []
    for seg in segments:
        line = f"[{seg.start:7.2f} - {seg.end:7.2f}] {seg.text.strip()}"
        print(line, flush=True)
        out.append({"start": round(seg.start, 2), "end": round(seg.end, 2),
                    "text": seg.text.strip()})

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump({"language": info.language,
                   "prob": round(info.language_probability, 3),
                   "segments": out}, f, ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
