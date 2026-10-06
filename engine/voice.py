# engine/voice.py — Rex Vance Voice Synthesis Engine for ZeroFilter
import asyncio
import json
import os
import sys
import edge_tts

DEFAULT_VOICE = "en-US-ChristopherNeural"
DEFAULT_RATE = "+10%"
DEFAULT_PITCH = "-2Hz"

async def synthesize_episode_audio(paragraphs, output_path, voice=DEFAULT_VOICE, rate=DEFAULT_RATE, pitch=DEFAULT_PITCH):
    """Synthesizes the complete 6-paragraph script into audio using Rex Vance's profile."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    full_text = "\n\n".join(paragraphs)
    
    communicate = edge_tts.Communicate(
        text=full_text,
        voice=voice,
        rate=rate,
        pitch=pitch
    )
    await communicate.save(output_path)
    print(f"Synthesized: {output_path}")

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
    await synthesize_episode_audio(ep["paragraphs"], out_audio)

if __name__ == "__main__":
    asyncio.run(main())
