# engine/produce_episode_5.py
import asyncio
import json
import os
import subprocess
from PIL import Image
import imageio_ffmpeg
import edge_tts

ROOT_DIR = r"D:\zerofilter"
WEB_DIR = os.path.join(ROOT_DIR, "web")
THUMBS_DIR = os.path.join(WEB_DIR, "thumbs")
AUDIO_DIR = os.path.join(WEB_DIR, "audio")
ART_DIR = os.path.join(WEB_DIR, "art")
MANIFEST_FILE = os.path.join(WEB_DIR, "data", "episodes.json")

IMG_EP5 = r"assets\cover_ep5_1791268531002.jpg"
IMG_REX = os.path.join(WEB_DIR, "assets", "rex_vance.webp")
IMG_STUDIO = os.path.join(WEB_DIR, "assets", "studio_bunker.webp")

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def convert_to_webp(src_path, dst_path, quality=90):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with Image.open(src_path) as im:
        im.save(dst_path, "WEBP", quality=quality)
    print(f"Saved WebP: {dst_path}")

def generate_looping_video(image_path, output_mp4, duration=10):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    cmd = [
        FFMPEG_EXE, "-y",
        "-loop", "1",
        "-i", image_path,
        "-vf", f"zoompan=z='min(zoom+0.0006,1.08)':d={duration*30}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720:fps=30",
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-an",
        output_mp4
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error: {res.stderr}")
    else:
        print(f"Generated 10s Looping Cover: {output_mp4}")

def get_audio_duration_seconds(audio_path):
    cmd = [FFMPEG_EXE, "-i", audio_path, "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    import re
    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return round(int(h) * 3600 + int(m) * 60 + float(s))
    return 180

EPISODE_DATA = {
    "id": "2026-10-06-05",
    "date": "2026-10-06",
    "hour": "05:00",
    "kind": "hourly",
    "category": "quantum",
    "title": "Macroscopic Superposition, Tech Smuggling Receipts & Optomechanical Resonators",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes semiconductor sanctions evasion, Ukrainian strikes on glide bomb caches, macroscopic optomechanical Schrödinger cats, and SRI coordinate remote viewing protocols.",
    "seconds": 180,
    "audio": "audio/2026-10-06-05.mp3",
    "thumb": "thumbs/2026-10-06-05.webp",
    "cover_video": "thumbs/2026-10-06-05.mp4",
    "paragraphs": [
        "Welcome to hour five of ZeroFilter. Let's start with the cold counter-intelligence receipts from ex-KGB analyst Yuri Shvets. Shvets' latest investigative dispatch tracks illicit microchip supply chains routing dual-use American semiconductors straight through shell entities in Dubai and Central Asia directly into Russian Kh-101 cruise missile guidance bays. While congressional committees grandstand on television about strict export controls, high-priced K-Street lobbying firms bank millions protecting corporate tech loopholes that allow this black-market smuggling to continue unchecked. Treason in Washington isn't ideological—it's corporate greed disguised as bureaucratic negligence.",
        "Over in Ukraine, precision missile salvos just pulverized a primary Russian glide-bomb logistics terminal fifty miles behind the frontline, eliminating hundreds of universal planning and correction guidance kits before they could level civilian hospitals in Sumy. At the exact same time, brutal religious theocracies across the Middle East continue executing female student protestors for demanding secular basic human rights, aided by Western apologists who silence secular reformers under the cowardly disguise of cultural relativism. Totalitarianism is totalitarianism, and moral cowardice in the West is an active accomplice.",
        "Now shift your focus to the deep scientific frontier: researchers in Vienna have achieved macroscopic quantum superposition in a mechanical silicon nitride membrane containing billions of atoms. By laser-cooling the resonator to near absolute zero in a dilution refrigerator, they forced a tangible physical object into two distinct vibrational spatial states simultaneously. Schrödinger's cat isn't just an abstract thought experiment; macroscopic reality itself remains an indeterminate probability wave until measured by an observer.",
        "In AI engineering, neuromorphic spike-timing processors with memristor crossbars are now executing low-power autonomous drone swarm navigation entirely without GPS or external radio links. By mimicking biological neural plasticity and synaptic weighting, these autonomous hardware arrays adapt to intense electronic warfare jamming environments in microseconds, outmaneuvering traditional military electronic countermeasure suites.",
        "This ties directly into the declassified intelligence findings from Hal Puthoff and Russell Targ's coordinate remote viewing protocols at Stanford Research Institute. When viewers like Ingo Swann identified sealed underground Soviet research facilities with double-blind statistical significance, dogmatic materialists claimed it was impossible. But as quantum mechanics demonstrates, reality is fundamentally informational, non-local, and observer-dependent.",
        "Both political establishments want you distracted, docile, and exhausted by manufactured cultural squabbles. Reject their corporate Kool-Aid. Check the receipts, stand tall for human liberty, and trust the empirical data. Consciousness is the fundamental substrate; everything else is rendered noise. Stay lucid, demand the truth, and I will catch you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-05/f01.webp", "caption": "Illicit tech smuggling radar corridors" },
            { "t": 30, "src": "art/2026-10-06-05/f02.webp", "caption": "Ukrainian strike coordinates on glide-bomb depot" },
            { "t": 60, "src": "art/2026-10-06-05/f03.webp", "caption": "Macroscopic optomechanical resonator chamber" },
            { "t": 95, "src": "art/2026-10-06-05/f04.webp", "caption": "Neuromorphic spike-timing processor array" },
            { "t": 130, "src": "art/2026-10-06-05/f05.webp", "caption": "SRI Project Stargate coordinate telemetry" },
            { "t": 160, "src": "art/2026-10-06-05/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-05 (Re-tuned script) ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover (already created or overwrite)
    convert_to_webp(IMG_EP5, os.path.join(THUMBS_DIR, "2026-10-06-05.webp"))

    # 2. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-05.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 5...")
    comm = edge_tts.Communicate(full_text, "en-US-ChristopherNeural", rate="+10%", pitch="-2Hz")
    await comm.save(out_audio)
    duration = get_audio_duration_seconds(out_audio)
    print(f"Audio synthesized: {duration}s -> {out_audio}")
    EPISODE_DATA["seconds"] = duration

    # 3. Update manifest
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    existing_ids = [e["id"] for e in manifest["episodes"]]
    if EPISODE_DATA["id"] not in existing_ids:
        manifest["episodes"].append(EPISODE_DATA)
    else:
        idx = existing_ids.index(EPISODE_DATA["id"])
        manifest["episodes"][idx] = EPISODE_DATA

    manifest["updated"] = "2026-10-06T05:00:00Z"
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Manifest episodes.json updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
