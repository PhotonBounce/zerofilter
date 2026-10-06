# engine/produce_episode_8.py
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

IMG_EP8 = r"assets\cover_ep8_1791269731484.jpg"
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
    "id": "2026-10-06-08",
    "date": "2026-10-06",
    "hour": "08:00",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Black Sea Naval Drone Perimeters, Oil Refinery Flaring & Reflexive Control Bluffs",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Russian Black Sea Fleet humiliation, Ukrainian precision strikes on catalytic cracking towers, Prigogine non-equilibrium thermodynamics, and Soviet reflexive control psychological warfare.",
    "seconds": 180,
    "audio": "audio/2026-10-06-08.mp3",
    "thumb": "thumbs/2026-10-06-08.webp",
    "cover_video": "thumbs/2026-10-06-08.mp4",
    "paragraphs": [
        "Welcome to hour eight of ZeroFilter. Let's examine the raw geopolitical ledger with former KGB foreign intelligence analyst Yuri Shvets. Shvets' latest dispatch cuts through the manufactured hysteria surrounding Kremlin red-line rhetoric. While Washington foreign policy elites agonize over mythical escalation risks, Ukrainian naval intelligence has systematically demolished the operational dominance of Russia's Black Sea Fleet. Armed with hundred-thousand-dollar autonomous Magura surface drones, Ukraine forced billion-dollar guided missile frigates and landing ships to flee their home base in Sevastopol and hide in Novorossiysk. As Shvets points out, authoritarian regimes never negotiate out of goodwill—they retreat only when physically humiliated by superior tactical asymmetry.",
        "Now look at the strategic energy infrastructure: precision long-range drone strikes have systematically taken offline over fifteen percent of Russia's primary oil refining capacity, specifically targeting imported vacuum distillation columns and catalytic cracking towers that Russian industry cannot manufacture domestically. Western corporate apologists cried that this would cause global crude oil shocks, but the empirical data proves them completely wrong: refined fuel prices inside Russia skyrocketed, forcing Moscow into nationwide gasoline export bans while global crude prices remained stable. Ukraine is methodically severing the economic fuel lines of the Russian war machine while Western bureaucrats wring their hands.",
        "In physical theory, this dynamic illustrates Ilya Prigogine's Nobel-winning principles of non-equilibrium thermodynamics and dissipative structures. Rigid, centralized authoritarian states are closed thermodynamic systems with zero internal adaptability. When external stress fluxes inject entropy into the system faster than the centralized hierarchy can dissipate it, the entire regime doesn't bend—it fractures into a sudden, chaotic phase transition. Collapse in totalitarian empires is always slow at first, and then instantaneous.",
        "On the engineering front, naval surface drones are now integrating multi-spectral electro-optical terminal guidance with edge-computed visual odometry. Operating entirely independent of satellite GPS constellations, these naval interceptors communicate over secure maritime millimeter-wave mesh nets, dynamically routing around heavy Russian coastal jamming suites with zero human intervention.",
        "This directly counters the Soviet doctrine of reflexive control that Shvets spent his intelligence career analyzing. Reflexive control is the deliberate injection of curated fear narratives into an adversary's media ecosystem to make them voluntarily paralyze their own decision-making. Every time an American politician repeats Kremlin talking points about nuclear escalation, they are executing Moscow's operational playbook for free.",
        "Refuse to let corrupt politicians and compromised media anchors dictate your reality. Verify the empirical facts, reject ideological theater, and recognize that consciousness and moral courage are the true engines of human freedom. Stay analytical, stay defiant, and I'll see you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-08/f01.webp", "caption": "Black Sea fleet naval tracks and drone corridors" },
            { "t": 35, "src": "art/2026-10-06-08/f02.webp", "caption": "Infrared thermal targeting on refinery cracking towers" },
            { "t": 72, "src": "art/2026-10-06-08/f03.webp", "caption": "Prigogine non-equilibrium thermodynamic entropy vectors" },
            { "t": 108, "src": "art/2026-10-06-08/f04.webp", "caption": "Autonomous maritime surface drone visual odometry" },
            { "t": 140, "src": "art/2026-10-06-08/f05.webp", "caption": "Yuri Shvets reflexive control psychological warfare matrix" },
            { "t": 165, "src": "art/2026-10-06-08/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-08 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-08.webp")
    convert_to_webp(IMG_EP8, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-08.mp4")
    generate_looping_video(IMG_EP8, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-08")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP8, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP8, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP8, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP8, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-08.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 8...")
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
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-08"]
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
