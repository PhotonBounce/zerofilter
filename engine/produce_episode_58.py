# engine/produce_episode_58.py
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

IMG_EP58 = os.path.join(THUMBS_DIR, "2026-10-08-10.webp")
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
    "id": "2026-10-08-10",
    "hour": "10:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Undersea Autonomous Drone Swarms, GIUK Gap Acoustic Barriers & Soviet Titanium-Hull Submarines",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates autonomous undersea drone swarm barrier networks across the Greenland-Iceland-United Kingdom Gap, seabed hydrophone line array upgrades, and Yuri Shvets's insider analysis of Soviet titanium-hull deep-diving submarine doctrines and Alfa-class acoustic evasion.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is ten hundred hours. Across the treacherous North Atlantic waters separating Greenland, Iceland, and the United Kingdom—the legendary GIUK Gap—the naval battle for acoustic dominance has entered the robotic era. Historically monitored by fixed seabed hydrophone arrays operating under the U.S. Navy’s Sound Surveillance System, NATO is now deploying autonomous undersea drone swarms to enforce an impenetrable acoustic curtain. Long-endurance extra-large uncrewed underwater vehicles, equipped with active low-frequency dipping sonars and towed synthetic aperture arrays, patrol the choke point continuously, coordinating via acoustic modems and surface satellite gateway buoys.",
        "The strategic objective is total containment of Russian Northern Fleet nuclear submarines attempting to slip out from the Barents Sea into open Atlantic patrol lanes. Traditional crewed attack submarines are prohibitively expensive and scarce, forcing Western planners to shift toward distributed robotic attrition. Autonomous drone swarms operate in coordinated packs, using bistatic acoustic processing where one drone acts as an active acoustic illuminator while dozens of silent slave drones detect target reflections. This distributed architecture strips away the acoustic stealth of modern Russian nuclear submarines, turning the GIUK Gap into a persistent gauntlet of persistent tracking.",
        "This underwater perimeter war directly inherits the doctrinal obsessions of the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has extensively analyzed, the Soviet naval command regarded the GIUK Gap as NATO’s acoustic choke-collar around the throat of the Soviet submarine fleet. To smash through NATO’s SOSUS line without acoustic detection, Soviet design bureaus embarked on the most extreme metallurgical gamble in naval history: constructing deep-diving submarines from solid titanium.",
        "According to Shvets, the resulting Alfa, Mike, and Sierra-class nuclear submarines utilized non-magnetic titanium alloys and liquid-metal-cooled nuclear reactors to achieve crushing depths beyond one thousand meters and speeds exceeding forty knots. Soviet naval intelligence calculated that diving far beneath the North Atlantic sound channel would allow these high-speed titanium predators to outrun Western homing torpedoes and penetrate the GIUK Gap before NATO command could react. Shvets emphasizes that while Soviet titanium metallurgy achieved unmatched physical performance, the astronomical manufacturing costs and maintenance bottlenecks ultimately crippled the Soviet naval budget.",
        "Today, as Russian submarines reassert aggressive Atlantic patrol patterns, the acoustic struggle has come full circle. Moscow no longer has the industrial capital to build titanium deep-divers, relying instead on hybrid seabed sabotage and ultra-quiet Yasen-class cruise missile platforms. But NATO’s answer is not more expensive hulls—it is an autonomous undersea drone swarm that never sleeps, never surfaces, and listens to every acoustic frequency.",
        "Map the GIUK bathymetry, audit the undersea drone swarms, and expose the naval choke points. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="giuk_gap")
    img.save(IMG_EP58, "WEBP", quality=92)
    print(f"Saved: {IMG_EP58}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP58, output_mp4, duration=10)
    
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
        IMG_EP58,
        IMG_REX,
        IMG_EP58,
        IMG_STUDIO,
        IMG_EP58,
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
