# engine/produce_episode_62.py
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

IMG_EP62 = os.path.join(THUMBS_DIR, "2026-10-08-14.webp")
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
    "id": "2026-10-08-14",
    "hour": "14:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Strait of Malacca Maritime Drone Blockades, Subsea Acoustic Hydrophone Gates & Soviet Indian Ocean Task Force",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates maritime autonomous surface and undersea drone blockades across the Strait of Malacca, seabed hydrophone acoustic tripwire gates, and Yuri Shvets's insider analysis of Soviet 8th Operational Squadron doctrine in the Indian Ocean.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is fourteen hundred hours. The Strait of Malacca is the ultimate global maritime choke point, funneling nearly a quarter of all seaborne trade and over eighty percent of East Asia's crude oil imports through a passage barely 1.5 nautical miles wide at Phillips Channel. In the emerging calculus of distributed naval warfare, this vital economic artery is being transformed into an asymmetric kill zone dominated by autonomous surface vessels, loitering munition swarms, and subsea acoustic tripwires designed to sever commercial transit lines instantly.",
        "The tactical architecture relies on persistent seabed acoustic hydrophone gates coupled with autonomous underwater patrol vehicles. Low-frequency passive sonar arrays anchored along the continental shelf establish continuous acoustic tomography, detecting cavitation profiles, propeller signatures, and magnetic displacement of passing hulls. When an unauthorized target crosses the acoustic tripwire, high-endurance autonomous surface drones armed with directed-energy jammers, electronic spoofers, and loitering kinetic torpedoes deploy in coordinated wolfpacks to close the strait, choking commercial shipping without requiring a single capital warship.",
        "This choke point interdiction strategy mirrors Soviet naval operational doctrine during peak Cold War confrontations. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively detailed, Soviet military theorists recognized choke point dominance as their premier asymmetric weapon. During the 1970s and 1980s, the Soviet Navy's 8th Operational Squadron maintained a continuous combat patrol across the Indian Ocean and Malacca approaches, tasked with choking Western energy routes and isolating regional maritime allies in the event of global conflict.",
        "According to Shvets, Soviet intelligence stations across Southeast Asia systematically mapped commercial shipping schedules, hydrographic channels, and subsea bathymetry. The KGB's maritime operational desks coordinated with Soviet naval intelligence to pre-position passive acoustic listening buoys, covert oceanographic tenders, and clandestine surveillance assets. Shvets underscores that while the Kremlin relied on diesel-electric submarines and missile cruisers to threaten commercial shipping lanes, today's distributed autonomous swarms achieve total maritime blockade capability at a tiny fraction of the procurement cost.",
        "Today, the commercial fragility of the Malacca Strait remains a critical geopolitical flashpoint. As naval superpowers invest hundreds of billions into aircraft carrier strike groups and nuclear-powered destroyers, low-cost autonomous drone blockades prove that whoever controls the narrow shallows and acoustic tripwires controls the global economy. Modern maritime supremacy is no longer defined by massive fleet tonnage, but by the relentless precision of autonomous swarms.",
        "Audit the hydrophone acoustic gates, track the autonomous drone vectors, and verify the choke points. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="malacca_blockade")
    img.save(IMG_EP62, "WEBP", quality=92)
    print(f"Saved: {IMG_EP62}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP62, output_mp4, duration=10)
    
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
        IMG_EP62,
        IMG_REX,
        IMG_EP62,
        IMG_STUDIO,
        IMG_EP62,
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
