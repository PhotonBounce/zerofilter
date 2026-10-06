# engine/produce_episode_40.py
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

IMG_EP40 = os.path.join(THUMBS_DIR, "2026-10-07-16.webp")
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
    "id": "2026-10-07-16",
    "hour": "16:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "corruption",
    "title": "Hypersonic Scramjet Failures, Cost-Plus Coverups & Soviet Aerospace Procurement Fraud",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes Pentagon hypersonic test aborts, thermal plasma blackouts, cost-plus contract padding, and Yuri Shvets's insider revelations regarding Soviet aerospace design bureau falsifications and KGB Third Chief Directorate coverups.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is sixteen hundred hours. Over the past six years, the Department of Defense has poured more than twelve billion dollars into hypersonic glide vehicles and scramjet-powered cruise missile prototypes. Billed as the ultimate asymmetric deterrent against near-peer adversaries, these systems are promised to achieve speeds exceeding Mach 5 with unpredictable maneuverability. Yet behind the classification veils and glossy press releases from prime aerospace contractors, the actual testing record reveals a catastrophic sequence of flight-test aborts, premature booster separations, and persistent telemetry blackouts.",
        "At velocities above Mach 5, friction generates extreme thermal boundary layers exceeding three thousand degrees Fahrenheit, enveloping vehicles in ionized plasma that scrambles satellite guidance and burns through ceramic composites. Rather than resolving these foundational aerodynamic bottlenecks, aerospace primes operating under open-ended cost-plus contracts routinely reclassify catastrophic disintegrations as partial test successes. They lobby congressional defense subcommittees for retroactive metric adjustments and multi-billion-dollar contract extensions, privatizing taxpayer funding while delivering zero deployable inventory.",
        "This institutionalized failure mode is intimately familiar to students of totalitarian defense bureaucracies. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, the Soviet aerospace sector operated under identical corruption. Soviet aviation design bureaus routinely falsified flight-test telemetry, masked severe engine thermal failures, and submitted doctored readiness certifications to the Ministry of Aviation Industry to meet five-year plan production quotas and secure state bonuses.",
        "Shvets reveals that the KGB's Third Chief Directorate—tasked with military counter-intelligence and defense plant surveillance—was thoroughly complicit in the coverup. Rather than arresting dishonest plant directors and chief engineers, KGB officers accepted luxury kickbacks, imported consumer goods, and institutional patronage to bury defect reports. When Soviet frontline regiments received defective aircraft with uncalibrated guidance and cracked structural bulkheads, the state security apparatus simply stamped the dossiers state secrets.",
        "When democratic defense procurement mimics the institutional secrecy and self-dealing of decayed authoritarian empires, national security becomes an illusion. Spending billions on unverified, proprietary hypersonic programs without public testing telemetry or independent physical audits does not deter adversaries—it merely enriches defense lobbyists and corporate contractors. Real military deterrence is forged through transparent engineering, ruthless testing accountability, and verifiable physics.",
        "Audit the cost-plus hypersonic contracts, demand unredacted telemetry from flight tests, and refuse to fund failure disguised as national security. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="hypersonic_fraud")
    img.save(IMG_EP40, "WEBP", quality=92)
    print(f"Saved: {IMG_EP40}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP40, output_mp4, duration=10)
    
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
        IMG_EP40,
        IMG_REX,
        IMG_EP40,
        IMG_STUDIO,
        IMG_EP40,
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
