# engine/produce_episode_28.py
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

IMG_EP28 = os.path.join(THUMBS_DIR, "2026-10-07-04.webp")
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
    "id": "2026-10-07-04",
    "hour": "04:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Supply Chain Phantom Billing, Cost-Plus Grift & Soviet Line X Infiltration",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates systemic defense procurement fraud, multi-tier subcontracting pass-through markups, and Yuri Shvets's analysis of historical KGB Line X industrial espionage exploiting unverified commercial supply chains.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero four hundred hours. If you want to understand how a sovereign nation loses a protracted industrial conflict before the first shot is fired, look no further than the cascading procurement funnel of the modern defense industrial base. A standard bolt, manufactured for eighty cents in a domestic foundry, travels through five discrete layers of prime contractors, systems integrators, and pass-through shell brokers—finally billing the Pentagon at eleven thousand dollars per unit. This is not bureaucratic inefficiency; it is an organized, legal skimming syndicate disguised as national security.",
        "As Washington counter-intelligence insider and former KGB Major Yuri Shvets has repeatedly documented, Soviet foreign intelligence never relied solely on stolen military blueprints. Through Directorate T and its elite scientific-technical apparatus known as Line X, Soviet intelligence systematically exploited Western commercial supply chains, funneling dual-use electronics, precision ball bearings, and specialized alloys through third-country front companies. The Soviets understood that when defense procurement becomes an opaque, multi-tiered marketplace of subcontracted middlemen, verifying the chain of custody becomes virtually impossible.",
        "Today, that exact architectural vulnerability has metastasized across the American defense sector. Forensic audits conducted on major aerospace and naval programs reveal that prime contractors routinely charge taxpayers for phantom labor hours, undocumented engineering change orders, and unverified commercial off-the-shelf components. Because cost-plus contracts reward excessive overhead rather than operational speed or fiscal restraint, primes have every economic incentive to stretch timelines, pad subcontractor invoices, and resist rigorous forensic accounting.",
        "The strategic consequence of this procurement grift is not merely financial insolvency; it is catastrophic industrial fragility. While adversaries produce precision munitions, hypersonic glide bodies, and electronic warfare suites at industrial scale, Western defense primes report multi-year backlogs for basic artillery shells and missile replacement motors. When counterfeit chips and unverified microelectronics from overseas brokers infiltrate frontline weapon systems, mission-critical avionics are compromised before aircraft ever leave the tarmac.",
        "Dismantling this multi-billion dollar racket requires aggressive, non-partisan structural intervention. We must mandate fixed-price procurement contracts for all mature weapon systems, institute cryptographic immutable provenance tracking across every tier-one through tier-four supplier, and enforce immediate criminal liability for defense executives who certify phantom subcontractor billings. In an era of great power competition, national defense is an existential duty, not a perpetual-growth hedge fund subsidized by working citizens.",
        "Audit the pass-through shell brokers, follow the invoices to the brass boardroom doors, and demand absolute supply chain transparency. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="supply_chain_fraud")
    img.save(IMG_EP28, "WEBP", quality=92)
    print(f"Saved: {IMG_EP28}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP28, output_mp4, duration=10)
    
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
        IMG_EP28,
        IMG_REX,
        IMG_EP28,
        IMG_STUDIO,
        IMG_EP28,
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
