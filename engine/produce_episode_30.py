# engine/produce_episode_30.py
import asyncio
import json
import os
import subprocess
from PIL import Image
import imageio_ffmpeg
import edge_tts
from generate_procedural_cover import generate_cover

ROOT_DIR = r"D:\zerofilter"
WEB_DIR = os.path.join(ROOT_DIR, "web")
THUMBS_DIR = os.path.join(WEB_DIR, "thumbs")
AUDIO_DIR = os.path.join(WEB_DIR, "audio")
ART_DIR = os.path.join(WEB_DIR, "art")
MANIFEST_FILE = os.path.join(WEB_DIR, "data", "episodes.json")

IMG_EP30 = os.path.join(THUMBS_DIR, "2026-10-07-06.webp")
IMG_REX = os.path.join(WEB_DIR, "assets", "rex_vance.webp")
IMG_STUDIO = os.path.join(WEB_DIR, "assets", "studio_bunker.webp")

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

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
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Generated 10s Looping Cover: {output_mp4}")

def create_art_frames(ep_id, src_art_paths):
    target_dir = os.path.join(ART_DIR, ep_id)
    os.makedirs(target_dir, exist_ok=True)
    frame_names = ["f01.webp", "f02.webp", "f03.webp", "f04.webp", "f05.webp", "f06.webp"]
    for src, fname in zip(src_art_paths, frame_names):
        dst = os.path.join(target_dir, fname)
        with Image.open(src) as im:
            im.save(dst, "WEBP", quality=90)
        print(f"Saved WebP: {dst}")
    print(f"Created 6 art frames in {target_dir}")

async def synthesize_rex_vance(text, output_mp3):
    os.makedirs(os.path.dirname(output_mp3), exist_ok=True)
    communicate = edge_tts.Communicate(text, "en-US-ChristopherNeural", rate="+10%", pitch="-2Hz")
    await communicate.save(output_mp3)

def get_audio_duration(file_path):
    cmd = [
        FFMPEG_EXE, "-i", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            total_sec = int(h) * 3600 + int(m) * 60 + float(s)
            return round(total_sec)
    return 180

EPISODE_DATA = {
    "id": "2026-10-07-06",
    "hour": "06:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Undersea Cable Sabotage, GUGI Seabed Warfare & Abyssal SIGINT Interception",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates vulnerabilities in transoceanic submarine fiber-optic cables, Russian Main Directorate of Deep-Sea Research (GUGI) special-mission submersibles, and Yuri Shvets's insider analysis of Kremlin seabed sabotage doctrines.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero six hundred hours. Ninety-seven percent of global internet communications, interbank financial transfers exceeding ten trillion dollars daily, and classified diplomatic traffic do not travel through satellites; they pulse through microscopic glass fibers encased in steel armor resting silently on the abyssal ocean floor. A single coordinated severance of key transoceanic choke points—in the English Channel, the Luzon Strait, or the Red Sea—would plunge modern financial markets and military command architectures into immediate paralysis.",
        "As Washington counter-intelligence insider and former KGB Major Yuri Shvets has frequently highlighted, Russian naval doctrine has prioritized asymmetric seabed warfare for over four decades. Operating under the secretive Main Directorate of Deep-Sea Research, known by its Russian acronym GUGI, Moscow commands specialized nuclear auxiliary mother submarines like the Belgorod and deep-diving titanium submersibles like the Losharik. These vessels operate at depths exceeding three thousand meters, designed specifically to tap, manipulate, or physically sever transatlantic undersea infrastructure during geopolitical escalations.",
        "The strategic advantage of seabed warfare lies in its profound attribution deficit. When an underwater fiber cable is cut on an abyssal continental shelf miles beneath turbulent international waters, distinguishing between commercial trawler anchor drag, seismic subsea landslides, and covert military sabotage can take weeks of underwater acoustic forensics. By the time allied naval hydrophones and remotely operated vehicles inspect the physical crimp or clean shear, the adversary's special-mission oceanographic vessel has already returned to Murmansk under sovereign immunity.",
        "Furthermore, GUGI's operational mandate extends far beyond blunt kinetic sabotage to covert signals intelligence interception. Western intelligence agencies pioneered seabed cable tapping in the 1970s with Operation Ivy Bells in the Sea of Okhotsk. Today, Russian intelligence deploys non-intrusive inductive sensors clamped directly around fiber repeaters, harvesting unencrypted packet telemetry directly from the physical layer before it ever reaches landing stations or cryptographic decryptors.",
        "Countering this abyssal vulnerability requires transforming our maritime security posture from reactive repair to continuous autonomous seabed defense. Allied nations must deploy persistent acoustic sensor arrays, autonomous unmanned underwater patrol gliders equipped with active sonar, and enforce international naval exclusion zones around critical landing conduits. In the 21st century, defending sovereignty requires securing the dark ocean floor with the same mathematical rigor we apply to orbital satellites and terrestrial borders.",
        "Audit the abyssal trenches, monitor the acoustic cavitation of covert submersibles, and never assume that deep water guarantees security. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="undersea_cable")
    img.save(IMG_EP30, "WEBP", quality=92)
    print(f"Saved: {IMG_EP30}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP30, output_mp4, duration=10)
    
    # 3. Audio Synthesis (Rex Vance Baritone)
    print("[3/5] Synthesizing audio via edge-tts (ChristopherNeural)...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    
    actual_duration = get_audio_duration(audio_path)
    print(f"Audio synthesized: {audio_path} ({actual_duration}s)")
    EPISODE_DATA["seconds"] = actual_duration
    
    # 4. Synchronized Art Frames
    print("[4/5] Creating 6 synchronized art frames...")
    art_sources = [
        IMG_EP30,
        IMG_REX,
        IMG_EP30,
        IMG_STUDIO,
        IMG_EP30,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = actual_duration / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
    EPISODE_DATA["thumb"] = f"thumbs/{EPISODE_DATA['id']}.webp"
    EPISODE_DATA["audio"] = f"audio/{EPISODE_DATA['id']}.mp3"
    EPISODE_DATA["cover_video"] = f"thumbs/{EPISODE_DATA['id']}.mp4"
    
    # 5. Manifest Registration
    print("[5/5] Updating manifest web/data/episodes.json...")
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Prepend new episode so newest is first
    existing = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
    manifest["episodes"] = [EPISODE_DATA] + existing
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"[+] Successfully produced Episode {EPISODE_DATA['id']} ({actual_duration}s)!")

if __name__ == "__main__":
    asyncio.run(main())
