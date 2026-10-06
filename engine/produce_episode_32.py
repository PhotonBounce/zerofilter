# engine/produce_episode_32.py
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

IMG_EP32 = os.path.join(THUMBS_DIR, "2026-10-07-08.webp")
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
    "id": "2026-10-07-08",
    "hour": "08:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "corruption",
    "title": "Aerospace Maintenance Monopolies, Diagnostic Paywalls & Soviet Line X Infiltration",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates proprietary defense contractor maintenance monopolies, diagnostic software DRM locks grounding frontline fighters, and Yuri Shvets's revelations regarding Soviet Line X industrial espionage exploiting commercialized aviation supply chains.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero eight hundred hours. The most devastating threat to modern air superiority is not adversary surface-to-air missile batteries; it is proprietary diagnostic software locks engineered by domestic defense primes. Across the fifth-generation fighter fleet, military maintainers are legally prohibited from inspecting flight-control telemetry, replacing hydraulic actuators, or repairing avionics modules without paying exorbitant proprietary licensing fees back to the original contractor. Frontline combat aircraft are grounded for months not by battle damage, but by digital rights management paywalls.",
        "This contractual lock-in represents the ultimate evolution of defense procurement extraction. When taxpayers fund the multi-billion dollar research and development costs of a weapon system, the government naively surrenders intellectual property and diagnostic tooling rights to prime contractors. By turning sustainment and logistics into a mandatory, sole-source monopoly lasting forty years, aerospace conglomerates generate seventy percent of program profits after delivery, transforming national defense into a captive subscription service.",
        "As Washington counter-intelligence insider and former KGB Major Yuri Shvets has extensively analyzed, commercialized defense maintenance monopolies create enormous structural vulnerabilities for adversarial intelligence exploitation. During the Cold War, Soviet Directorate T and its specialized Line X apparatus did not attempt to steal completed fighter jets; they targeted the commercial maintenance contractors, third-party component overhaul facilities, and avionics supply hubs. Middlemen and commercial subcontractors lack classified security perimeters, making them soft targets for industrial espionage.",
        "When maintenance architectures rely on cloud-connected diagnostic portals like ODIN and proprietary off-board mission support servers, the cyber attack surface expands exponentially. Hostile foreign intelligence services do not need to penetrate hardened military networks; they compromise third-party commercial vendors and maintenance sub-contractors, quietly injecting malicious firmware into engine control units or exfiltrating operational readiness telemetry directly from diagnostic data streams.",
        "Breaking this stranglehold requires enforcing immediate Right to Repair mandates across the entire Department of Defense. We must compel defense contractors to deliver complete, non-proprietary technical data packages, open-standard diagnostic protocols, and depot-level repair manuals as a non-negotiable condition of contract awards. Military mechanics in combat zones must possess sovereign authority and technical capability to repair their own weapon systems without waiting for vendor technicians or corporate digital authorizations.",
        "Audit the proprietary sustainment contracts, dismantle the diagnostic paywalls, and demand full technical data sovereignty for the warfighter. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="aerospace_monopoly")
    img.save(IMG_EP32, "WEBP", quality=92)
    print(f"Saved: {IMG_EP32}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP32, output_mp4, duration=10)
    
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
        IMG_EP32,
        IMG_REX,
        IMG_EP32,
        IMG_STUDIO,
        IMG_EP32,
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
