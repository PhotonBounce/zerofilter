# engine/produce_episode_36.py
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

IMG_EP36 = os.path.join(THUMBS_DIR, "2026-10-07-12.webp")
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
    "id": "2026-10-07-12",
    "hour": "12:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense AI Non-Competes, Revolving-Door Advisory Boards & Soviet Kickback Rings",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes Pentagon enterprise AI sole-source contracts, revolving-door advisory board collusion, indemnification shields, and Yuri Shvets's insider revelations regarding Soviet Special Department kickback cartels and falsified weapons readiness reports.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twelve hundred hours. Over the past four years, the Pentagon has allocated tens of billions of dollars toward enterprise artificial intelligence and autonomous battlefield systems. Programs like the Joint Warfighting Cloud Capability and expanded Project Maven consortia were pitched to taxpayers as competitive, cutting-edge initiatives designed to preserve American technological dominance. But behind the press releases lies an entrenched cartel architecture: non-compete clauses, classified single-source sole-award contracts, and cozy indemnification shields that guarantee massive profits regardless of technical delivery.",
        "At the center of this contracting grift sits the revolving door between Silicon Valley defense ventures and the Department of Defense. Former executives and venture capital partners routinely rotate into senior Pentagon advisory boards, write technical procurement specifications tailored exclusively to their former portfolio companies, and then rotate back out into multimillion-dollar equity packages. Traditional defense primes and venture-backed AI unicorns operate in lockstep, erecting insurmountable classification moats that lock out independent software auditors while billing taxpayers cost-plus markups for commodity algorithmic models.",
        "This institutionalized collusion is not a new aberration of late-stage capitalism; it is the inevitable degeneration of any unmonitored military-industrial monopoly. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, the Soviet military apparatus suffered from an identical pathology. Soviet defense ministries and the KGB's military counter-intelligence Special Departments established elaborate kickback cartels. High-ranking officers and factory directors routinely approved fabricated weapons acceptance tests and diverted state funds into private dacha construction, while stamping non-functional hardware combat-ready.",
        "Shvets emphasizes that when internal audit mechanisms are co-opted by the very officials tasked with oversight, systemic failure becomes mathematically certain. In the late Soviet era, military factories produced tanks with missing optics and radios that could not operate in cold weather, yet every bureaucrat signed off because everyone received their cut. Today, when the Pentagon fails seven consecutive financial audits and cannot account for trillions in assets, the underlying mechanism is functionally identical.",
        "Deploying unverified, proprietary black-box AI models into critical military command chains without rigorous, adversarial third-party audits is an existential vulnerability. Adversaries do not need to hack our networks if our procurement cartels deliver bloated, fragile systems designed for quarterly investor dividends rather than actual combat resilience. National defense cannot survive as a subsidized money-laundering conduit for political donors and venture monopolies.",
        "Audit the non-competes, dismantle the revolving-door advisory cartels, and hold defense contractors criminally accountable for non-delivery. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="defense_ai_cartel")
    img.save(IMG_EP36, "WEBP", quality=92)
    print(f"Saved: {IMG_EP36}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP36, output_mp4, duration=10)
    
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
        IMG_EP36,
        IMG_REX,
        IMG_EP36,
        IMG_STUDIO,
        IMG_EP36,
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
