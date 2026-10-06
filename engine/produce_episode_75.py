# engine/produce_episode_75.py
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

IMG_EP75 = os.path.join(THUMBS_DIR, "2026-10-09-03.webp")
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
    "id": "2026-10-09-03",
    "hour": "03:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "corruption",
    "title": "Special Access Program Financial Obfuscation, Defense Intelligence SAP Unvouchered Funds & Soviet Clandestine Accounts",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates unvouchered funds inside defense Special Access Programs, phantom billing carve-outs, and Yuri Shvets on KGB First Chief Directorate clandestine bank accounts.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero three hundred hours. In the classified recesses of the United States defense apparatus, the most impregnable barrier against financial oversight is not encryption or perimeter security, but classification itself. Under the umbrella of Special Access Programs, or SAPs, billions of taxpayer dollars flow through unvouchered accounts and carved-out black budgets where standard government accounting rules cease to exist. By legally restricting audits to a tiny, compartmentalized cadre of cleared personnel, defense intelligence agencies and legacy aerospace primes have constructed a self-sealing financial ecosystem immune to congressional subpoena.",
        "Recent internal audits from the Department of Defense Inspector General reveal that unacknowledged SAPs frequently fail to maintain basic transaction ledgers. Defense primes exploit this opacity by assigning massive overhead markups to classified line items, billing the Pentagon for phantom subcontractor networks, unverified software licenses, and redundant prototyping facilities that are never subjected to independent inventory verification. When government auditors request transaction receipts, program managers invoke national security statutory waivers, effectively stonewalling oversight while siphoning capital into unmonitored corporate balance sheets.",
        "This institutionalized financial obfuscation is the Western corporate mirror of the clandestine accounting systems perfected by Soviet intelligence. Former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed how the KGB's First Chief Directorate operated parallel financial mechanisms completely severed from the state budget. The First Chief Directorate established hundreds of commercial shell companies, offshore accounts in Switzerland, Austria, and Cyprus, and unvouchered hard-currency slush funds ostensibly earmarked for foreign clandestine operations.",
        "According to Shvets, corrupt KGB general officers and Gosplan apparatchiks routinely diverted state gold reserves and energy export revenues into these unmonitored accounts. Because the funds were classified as top secret intelligence reserves, no Soviet state audit organ possessed the clearance to inspect the ledgers. When the Soviet Union collapsed, billions of dollars vanished overnight into private offshore bank accounts controlled by former KGB officers, creating the very oligarchic networks that dominate the Kremlin today.",
        "When modern defense contractors lobby to expand unacknowledged Special Access Programs under the guise of geopolitical urgency, they are replicating this exact mechanism. Compartmentalization designed to protect technical blueprints becomes a protective shield for systemic billing fraud and institutional self-enrichment. Secrecy without independent audit inevitably breeds institutional corruption.",
        "Audit the unvouchered SAP ledgers, trace the offshore shell conduits, and demand unredacted defense balance sheets. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="black_budget")
    img.save(IMG_EP75, "WEBP", quality=92)
    print(f"Saved: {IMG_EP75}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP75, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP75, IMG_REX, IMG_STUDIO, IMG_EP75, IMG_REX, IMG_EP75]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # 4. Neural Audio Synthesis
    print("[4/5] Synthesizing Rex Vance neural baritone audio...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    dur = get_audio_duration(audio_path)
    print(f"Synthesized Audio: {audio_path} ({dur} seconds)")
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = dur / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
    EPISODE_DATA["seconds"] = dur
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
    print(f"Updated {MANIFEST_FILE} with episode {EPISODE_DATA['id']}!")
    
    # Copy cover to brain artifacts for documentation
    brain_cover = r"assets\cover_ep75_procedural.webp"
    with Image.open(IMG_EP75) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
