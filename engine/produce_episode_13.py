# engine/produce_episode_13.py
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

IMG_EP13 = r"assets\cover_ep13_1791271233545.jpg"
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
    "id": "2026-10-06-13",
    "date": "2026-10-06",
    "hour": "13:00",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Vacuum Fluctuations, Casimir Micro-Thrusters & Orbital Surveillance",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Russian Cosmos co-orbital satellite stalkers, Ukrainian proliferated LEO radar meshes, the dynamical Casimir effect zero-point physics, and propellant-less micro-propulsion.",
    "seconds": 180,
    "audio": "audio/2026-10-06-13.mp3",
    "thumb": "thumbs/2026-10-06-13.webp",
    "cover_video": "thumbs/2026-10-06-13.mp4",
    "paragraphs": [
        "Welcome to hour thirteen of ZeroFilter. Let's look up to the high frontier of orbital warfare with former KGB foreign counter-intelligence analyst Yuri Shvets. Shvets' latest intelligence brief examines Moscow's deployment of Cosmos-2576, a covert co-orbital inspector satellite maneuvering within striking distance of American classified optical reconnaissance platforms in low Earth orbit. While Pentagon defense contractors rake in hundreds of millions developing multi-billion-dollar exquisite satellite systems, Russian and Chinese space forces have fielded ground-based laser dazzling suites capable of blinding optical sensors for a tiny fraction of the cost. Once again, Washington's defense monopolies prioritize bloated corporate billings over resilient survivability.",
        "Now observe how asymmetric distributed architecture solved this vulnerability on the Ukrainian front: by utilizing proliferated low Earth orbit satellite meshes like ICEYE synthetic aperture radar and commercial optical swarms, Ukrainian artillery commanders receive uninterrupted sub-meter radar imaging straight through cloud cover and smoke screens. Russia can blind or jam one satellite, but they cannot blind thousands of autonomous nodes operating in a self-healing mesh. Distributed resilience destroys centralized authoritarian targeting doctrine every single time.",
        "In fundamental physics, this brings us to one of the most astonishing truths in quantum mechanics: the dynamical Casimir effect. Classical physics taught that the vacuum of space is cold, empty nothingness. Quantum field theory proves the absolute opposite: the quantum vacuum is a turbulent, boiling ocean of zero-point fluctuations, bursting with virtual particle-antiparticle pairs that appear and annihilate in femtoseconds. By vibrating a conductive boundary at relativistic velocities, physicists have experimentally extracted real, observable photons directly from the vacuum. The void is not empty; it is an inexhaustible sea of latent energy.",
        "In applied aerospace engineering, researchers are fabricating asymmetric Casimir micro-cavities using silicon-carbide metamaterials. By engineering spatial gradients in vacuum fluctuation density, these propellant-less micro-thrusters generate continuous nanoscale station-keeping propulsion for deep-space micro-satellites, completely bypassing the physical weight limits of liquid chemical rocket fuels.",
        "This shatters the reductionist materialist delusion that you are an isolated speck in a dead, meaningless void. There is no empty space. Every cubic centimeter of the cosmos is teeming with infinite computational and thermodynamic potential. Consciousness is the fundamental field that observes, measures, and brings this infinite ground state into physical form.",
        "Don't let legacy gatekeepers trap your mind in obsolete nineteenth-century mechanical dogmas. Follow the mathematics, demand real accountability from our defense establishment, and remember that reality is boundless energy waiting for conscious direction. Stay sharp, remain free, and I'll catch you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-13/f01.webp", "caption": "Russian Cosmos-2576 co-orbital inspector satellite track" },
            { "t": 35, "src": "art/2026-10-06-13/f02.webp", "caption": "Proliferated LEO synthetic aperture radar constellation" },
            { "t": 72, "src": "art/2026-10-06-13/f03.webp", "caption": "Dynamical Casimir effect vacuum cavity test chamber" },
            { "t": 110, "src": "art/2026-10-06-13/f04.webp", "caption": "Silicon-carbide asymmetric metamaterial micro-thruster" },
            { "t": 142, "src": "art/2026-10-06-13/f05.webp", "caption": "Quantum zero-point energy density tensor mapping" },
            { "t": 165, "src": "art/2026-10-06-13/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-13 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-13.webp")
    convert_to_webp(IMG_EP13, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-13.mp4")
    generate_looping_video(IMG_EP13, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-13")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP13, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP13, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP13, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP13, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-13.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 13...")
    communicate = edge_tts.Communicate(
        text=full_text,
        voice="en-US-ChristopherNeural",
        rate="+10%",
        pitch="-2Hz"
    )
    await communicate.save(out_audio)
    actual_duration = get_audio_duration_seconds(out_audio)
    print(f"Audio synthesized: {actual_duration}s -> {out_audio}")
    EPISODE_DATA["seconds"] = actual_duration

    # 4. Manifest Update
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_list = manifest.get("episodes", manifest)
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-13"]
    manifest_list.insert(0, EPISODE_DATA)

    if isinstance(manifest, dict) and "episodes" in manifest:
        manifest["episodes"] = manifest_list
        data_to_write = manifest
    else:
        data_to_write = manifest_list

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_write, f, indent=2)

    print("Manifest episodes.json updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
