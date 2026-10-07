# engine/voice.py — Rex Vance Voice Synthesis Engine for ZeroFilter
#
# Each paragraph is synthesized on its own and the MP3 streams are joined, so
# the start of every paragraph is known exactly. Those starts are written back
# to the manifest as `cues` (seconds) along with the real `seconds`; the player
# uses them for subtitles and story-art timing instead of guessing.
import asyncio
import json
import os
import sys
import edge_tts

DEFAULT_VOICE = "en-US-AvaMultilingualNeural"
DEFAULT_RATE = "+5%"
DEFAULT_PITCH = "-1Hz"
# edge-tts streams audio-24khz-48kbitrate-mono-mp3: constant 48 kbit/s, so
# bytes * 8 / 48000 is the duration (checked against ffprobe on the pilots).
MP3_BYTES_PER_SECOND = 48000 / 8


async def synthesize_paragraph(text, voice, rate, pitch):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    audio = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
    if not audio:
        raise RuntimeError("edge-tts returned no audio for a paragraph")
    return bytes(audio)


async def synthesize_episode_audio(paragraphs, output_path, voice=DEFAULT_VOICE, rate=DEFAULT_RATE, pitch=DEFAULT_PITCH):
    """Synthesizes the 6-paragraph script. Returns (seconds, cues)."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cues, parts, offset = [], [], 0.0
    for idx, text in enumerate(paragraphs):
        print(f"  [TTS] Synthesizing paragraph {idx+1}/{len(paragraphs)} ({len(text.split())} words)...", flush=True)
        audio = await synthesize_paragraph(text, voice, rate, pitch)
        cues.append(round(offset, 2))
        offset += len(audio) / MP3_BYTES_PER_SECOND
        parts.append(audio)
    with open(output_path, "wb") as f:
        for audio in parts:
            f.write(audio)
    print(f"Synthesized: {output_path} ({offset:.1f}s)", flush=True)
    return round(offset, 2), cues


async def main():
    if len(sys.argv) < 3:
        print("Usage: python voice.py <path_to_episodes.json> <episode_id>")
        sys.exit(1)

    manifest_path = sys.argv[1]
    episode_id = sys.argv[2]

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    ep = next((e for e in data["episodes"] if e["id"] == episode_id), None)
    if not ep:
        print(f"Episode {episode_id} not found.")
        sys.exit(1)

    out_audio = os.path.join(os.path.dirname(manifest_path), "..", ep["audio"])
    seconds, cues = await synthesize_episode_audio(ep["paragraphs"], out_audio)
    ep["seconds"] = round(seconds)
    ep["cues"] = cues
    # One story frame per paragraph: pin each frame to its paragraph's start.
    frames = ep.get("art", {}).get("frames", [])
    if len(frames) == len(cues):
        for frame, t in zip(frames, cues):
            frame["t"] = t

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    asyncio.run(main())
