# engine/produce_episode_52.py
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

IMG_EP52 = os.path.join(THUMBS_DIR, "2026-10-08-04.webp")
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
    "id": "2026-10-08-04",
    "hour": "04:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "corruption",
    "title": "Commercial Satellite Imagery Monopolies, NRO Tasking Overrides & Soviet Space Reconnaissance Diversions",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates commercial satellite imagery monopolies, National Reconnaissance Office tasking priority overrides and shutter control, and Yuri Shvets's insider analysis of Soviet space-based optical reconnaissance diversion and maskirovka overflight scheduling.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero four hundred hours. High above the atmosphere, low-Earth orbit has become the ultimate proprietary Panopticon. While the commercial space sector advertises satellite earth observation as a democratic, transparent tool for climate monitoring and global commerce, the reality on the ground is governed by classified monopoly contracts. Under the National Reconnaissance Office’s Electro-Optical Commercial Layer agreements, a handful of venture-backed aerospace defense primes have monopolized high-resolution orbital imaging, transforming civilian constellations into de facto intelligence extensions of the United States defense apparatus.",
        "The architecture of this orbital monopoly relies on dual-use tasking priority overrides and legal shutter control. Under federal regulatory frameworks and classified service agreements, defense agencies possess the unilateral authority to commandeer private satellite sensors during geopolitical flashpoints. When an international conflict or military deployment occurs, commercial imagery pipelines are instantly throttled: high-resolution passes over sensitive combat zones are classified, pre-emptively purchased through exclusive buyout contracts, or degraded to lower-fidelity resolutions before reaching open-source analysts, effectively censoring the public's perception of global warfare.",
        "This systemic manipulation of space-based visibility mirrors the orbital deception doctrines perfected during the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet military planning was entirely synchronized around Western satellite reconnaissance schedules. Operating under the strategic deception doctrine known as maskirovka, the Soviet General Staff and KGB First Chief Directorate tracked the exact orbital ephemerides and overflight windows of American KH-11 optical reconnaissance satellites.",
        "According to Shvets, Soviet defense installations executed elaborate camouflage, concealment, and decoy procedures the moment an American spy satellite crossed the horizon. Aircraft mockups were moved onto airfields, false missile silos were painted on tarmac, and sensitive technical operations were halted until the spacecraft dropped below the horizon. Shvets reveals that the Soviet space program’s Kosmos reconnaissance satellites operated under identical state secrecy, routinely masking optical surveillance payloads beneath nominal civilian meteorological and scientific designations to disguise intelligence-gathering orbital paths.",
        "In orbit today, the line between commercial transparency and military monopolization has vanished entirely. By locking up commercial optical and synthetic aperture radar constellations behind exclusive Pentagon tasking agreements, defense agencies ensure that sovereign states maintain an absolute monopoly on actionable real-time truth. When billions in defense dollars dictate who is permitted to look at the Earth, commercial space ceases to be an open scientific frontier and becomes a private, classified surveillance utility.",
        "Track the orbital overflight ephemerides, pierce the commercial tasking buyouts, and audit the satellite imagery monopolies. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="satellite_monopoly")
    img.save(IMG_EP52, "WEBP", quality=92)
    print(f"Saved: {IMG_EP52}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP52, output_mp4, duration=10)
    
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
        IMG_EP52,
        IMG_REX,
        IMG_EP52,
        IMG_STUDIO,
        IMG_EP52,
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
