# engine/produce_episode_54.py
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

IMG_EP54 = os.path.join(THUMBS_DIR, "2026-10-08-06.webp")
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
    "id": "2026-10-08-06",
    "hour": "06:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Barents Sea Nuclear Submarine Bastion Doctrine, SOSUS Trench Baffles & Soviet Northern Fleet Deterrence",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the Barents Sea under-ice nuclear submarine bastion doctrine, abyssal trench acoustic shadow zones and thermal stratification baffles, and Yuri Shvets's insider analysis of Soviet Northern Fleet strategic deterrence deployment and GUGI deep-sea seabed sabotage.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero six hundred hours. Beneath the frozen polar ice caps of the Barents Sea and the Kola Peninsula, the Russian Federation maintains the ultimate sanctuary for its strategic second-strike nuclear capability: the naval bastion. Designed to shield ballistic missile submarines from Western attack submarines, the bastion doctrine relies on heavily defended littoral sea space enclosed by layered coastal missile batteries, anti-submarine aircraft, and minefields. Under the permanent acoustic shelter of the marginal ice zone, Russian submarines exploit underwater bathymetric trenches and severe thermal stratification to evade Western acoustic detection.",
        "The physics of Arctic underwater acoustics creates an asymmetric defensive sanctuary. Deep underwater canyons and glacial ridges act as natural sound baffles, trapping acoustic emissions within shadow zones where passive sonar arrays cannot penetrate. Surface ice grinding and calving generate extreme ambient noise floors that mask the low-frequency mechanical signatures of nuclear propulsion reactors. Simultaneously, Western anti-submarine forces attempting to penetrate the Barents perimeter face an acoustic gauntlet of seabed acoustic sensors, bottom-moored magnetic anomaly detectors, and ice-penetrating synthetic aperture radars deployed from Russian maritime patrol platforms.",
        "This Arctic fortress strategy has direct operational ancestry in the Soviet Navy’s Cold War posture. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet naval leadership recognized after the Cuban Missile Crisis that their diesel and early nuclear submarines could never survive an open-ocean transit through NATO’s SOSUS lines in the North Atlantic. Under Admiral Sergey Gorshkov, the Soviet Navy completely reoriented its strategic nuclear fleet toward the bastion concept, locking its Delta and Typhoon-class submarines safely inside the Barents and Okhotsk seas.",
        "According to Shvets, the KGB’s First Chief Directorate was tasked with ensuring the absolute survivability of these Arctic bastions against Western covert penetration. Soviet naval counter-intelligence monitored Western hydrophone research stations in Norway and Svalbard, while specialized deep-sea units—the precursors to today’s Main Directorate of Deep-Sea Research—mapped the polar seabed to install covert nuclear-powered sonar beacons and underwater communication cables. Shvets emphasizes that the Kremlin viewed the Barents bastion as the guarantor of regime survival, making any Western encroachment an existential red line.",
        "Today, as melting polar ice opens commercial transit lanes and naval access corridors, the Barents Sea is re-emerging as the central flashpoint of global deterrence. Modern NATO maritime forces and autonomous undersea drones are probing deeper into the Arctic perimeter, challenging Moscow’s proprietary control over its northern bastion. But the geopolitical stakes remain chillingly unaltered: beneath hundreds of meters of polar ice, the nuclear balance of power hinges on the quiet navigation of abyssal trenches.",
        "Probe the polar bathymetry, monitor the Arctic shadow zones, and audit the deep-sea bastion doctrines. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="barents_bastion")
    img.save(IMG_EP54, "WEBP", quality=92)
    print(f"Saved: {IMG_EP54}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP54, output_mp4, duration=10)
    
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
        IMG_EP54,
        IMG_REX,
        IMG_EP54,
        IMG_STUDIO,
        IMG_EP54,
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
