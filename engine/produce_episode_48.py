# engine/produce_episode_48.py
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

IMG_EP48 = os.path.join(THUMBS_DIR, "2026-10-08-00.webp")
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
    "id": "2026-10-08-00",
    "hour": "00:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "corruption",
    "title": "Pentagon Black Budget Audits, Special Access Program Phantom Line Items & Soviet Gosplan Diversions",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the Pentagon's multi-trillion-dollar audit failures, Unacknowledged Special Access Program phantom line items, and Yuri Shvets's insider analysis of Soviet Gosplan military intelligence diversion apparatuses.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero hundred hours. For the seventh consecutive year, the United States Department of Defense has failed its comprehensive financial audit, unable to account for more than sixty percent of its four-trillion-dollar asset base. Beneath the public budget debates lies the black budget—an opaque archipelago of Unacknowledged Special Access Programs where hundreds of billions in taxpayer capital vanish into classified line items, waived Congressional reporting schedules, and phantom vendor accounts shielded by national security exemptions.",
        "The forensic accounting architecture of the black budget is deliberately engineered to prevent external oversight. Through Pass-Through Accounts and budget carve-outs in Air Force and DARPA balance sheets, procurement funds are routed through tier-one defense primes directly to off-the-books subcontractors. Assets are booked under placeholder ledger entries known as phantom lines, where physical inventory audits are legally blocked by security compartmentalization. Prime contractors exploit this classification barrier to obscure cost overruns, billing taxpayers tens of millions for unverified engineering deliverables that exist only as red-stripe binders in subterranean SCIFs.",
        "This systemic fiscal evasion bears an uncanny structural resemblance to the historical diversion architectures of Soviet central planning. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has extensively analyzed, the late Soviet state operated a shadow economy known as the Gosplan diversion apparatus. Under the pretext of state secrecy and military parity, Soviet ministries diverted up to twenty percent of the USSR’s gross domestic product into classified military-industrial complexes, completely hidden from the nominal civilian state budget.",
        "According to Shvets, the KGB’s military-economic directorates worked hand-in-hand with Gosplan apparatchiks to siphon off raw materials, foreign hard currency reserves, and precision industrial tooling into unmonitored military production lines. Because the system lacked independent audit mechanisms, Soviet defense bureaucrats systematically inflated component requirements, embezzled production surpluses, and falsified industrial output statistics. Shvets emphasizes that this unchecked classification cartel not only concealed rampant internal graft, but ultimately accelerated the structural economic insolvency and collapse of the Soviet Union.",
        "In Washington today, the identical pathology operates under the legal banner of Special Access Program compartmentalization. By walling off defense expenditures behind classification firewalls, the Pentagon and its contractor cartel replicate Soviet-style bureaucratic capture: endless cost-plus inflation, zero accountability, and massive capital misallocation disguised as strategic deterrence. When billions can be made to disappear into unacknowledged programs with a single security waiver, national defense ceases to be an instrument of public security and becomes a self-sustaining sovereign slush fund.",
        "Follow the classified ledgers, pierce the compartmented firewalls, and audit the phantom line items. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="black_budget")
    img.save(IMG_EP48, "WEBP", quality=92)
    print(f"Saved: {IMG_EP48}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP48, output_mp4, duration=10)
    
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
        IMG_EP48,
        IMG_REX,
        IMG_EP48,
        IMG_STUDIO,
        IMG_EP48,
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
