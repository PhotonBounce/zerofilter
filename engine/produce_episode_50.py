# engine/produce_episode_50.py
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

IMG_EP50 = os.path.join(THUMBS_DIR, "2026-10-08-02.webp")
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
    "id": "2026-10-08-02",
    "hour": "02:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Taiwan Strait Undersea Acoustic Hydrophone Barriers, SOSUS Line Arrays & Soviet Submarine Tracking Doctrine",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Taiwan Strait undersea acoustic hydrophone barriers, SOSUS line arrays and beamforming triangulation, and Yuri Shvets's insider analysis of Soviet Pacific Fleet submarine tracking doctrine and cable sabotage operations.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero two hundred hours. In the shallow, treacherous waters of the Taiwan Strait and the Luzon Chokepoint, modern maritime warfare is being determined beneath the surface. Deep-sea fiber-optic hydrophone networks, anchored directly into the continental shelf, form an acoustic tripwire designed to eliminate undersea stealth. Derived from the Cold War Sound Surveillance System, these fixed passive line arrays leverage beamforming signal processing algorithms to detect, classify, and track the low-frequency acoustic signatures and propeller cavitation of submerged attack submarines across hundreds of nautical miles.",
        "The Taiwan Strait presents an acoustic nightmare of tidal clutter, thermal stratification, and dense commercial merchant traffic. To penetrate this ambient noise floor, modern anti-submarine warfare integrates seabed line arrays with autonomous uncrewed underwater vehicles and low-frequency active dipping sonars deployed from maritime patrol aircraft. When an undersea target crosses the hydrophone baseline, time-difference-of-arrival triangulation calculates the target’s course, speed, and depth, feeding real-time targeting coordinates into coastal anti-ship missile batteries and smart sea-mine corridors deployed across the first island chain.",
        "This acoustic barrier architecture reflects the operational doctrines forged during the Cold War’s undersea confrontation. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet naval strategy was perpetually paralyzed by the US Navy’s SOSUS chokeholds across the GIUK Gap and Pacific approaches. The Soviet Pacific Fleet based in Petropavlovsk and Vladivostok could not transit into open ocean without their acoustic profiles being instantly logged, triangulated, and shadowed by Western hunter-killer submarines.",
        "According to Shvets, the KGB’s First Chief Directorate and Soviet naval intelligence expended colossal resources attempting to blind, sever, or deceive these acoustic arrays. Soviet spy ships disguised as oceanographic research trawlers systematically surveyed Western cable routes, while specialized Directorate S sabotage divers practiced underwater cable tapping and demolition. Shvets reveals that Soviet defectors and Western espionage rings—most notably the John Walker spy ring—provided Moscow with deciphered communication keys and acoustic tracking telemetry that exposed just how vulnerable Soviet nuclear submarines were to Western seabed arrays.",
        "Today, Beijing faces the identical hydrophone containment perimeter that constrained the Soviet Navy four decades ago. In response, Chinese naval intelligence is actively deploying seabed surveillance networks and underwater glider swarms while executing gray-zone dredging operations near undersea fiber-optic nodes. But acoustic physics remains unforgiving: in the narrow waters of the Western Pacific, any submarine entering the littoral zone is tracked from the moment its reactor coolant pumps cycle. The undersea balance of power is written in raw acoustic decibels.",
        "Monitor the hydrophone baselines, decode the low-frequency acoustic telemetry, and audit the seabed chokepoints. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="taiwan_sosus")
    img.save(IMG_EP50, "WEBP", quality=92)
    print(f"Saved: {IMG_EP50}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP50, output_mp4, duration=10)
    
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
        IMG_EP50,
        IMG_REX,
        IMG_EP50,
        IMG_STUDIO,
        IMG_EP50,
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
