# engine/produce_episode_143.py
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

IMG_EP143 = os.path.join(THUMBS_DIR, "2026-10-11-23.webp")
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
    "id": "2026-10-11-23",
    "hour": "23:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "corruption",
    "title": "Pentagon JADC2 Defense Cloud Pass-Throughs, AI Interoperability Grift & Soviet C3I Vaults",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the Pentagon Joint Warfighting Cloud Capability (JWCC) and JADC2 architecture, multi-billion-dollar middleware pass-through markups, vendor lock-in traps, and Yuri Shvets on Soviet automated command and control systems (ASU) and KGB SIGINT interception vulnerabilities.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-three hundred hours. The Pentagon calls it the holy grail of modern warfare: Joint All-Domain Command and Control, or JADC2. The premise is seductive: linking sensors and shooters across air, land, sea, space, and cyberspace into a unified, AI-driven kill web. Under the nine-billion-dollar Joint Warfighting Cloud Capability contract, the Department of Defense split its enterprise cloud across four tech giants. Yet behind the marketing slide decks lies a staggering multi-cloud grift: custom API wrapper pass-throughs, runaway data egress tariffs, and proprietary interoperability bottlenecks.",
        "Instead of delivering a seamless battlefield cloud, the multi-vendor compromise created an integration nightmare. Prime defense IT contractors and beltway consultancies billing hundreds of millions invoice the Pentagon for basic translation middleware—custom software bridges required simply to allow disparate commercial clouds to exchange targeting packets. Internal audits reveal that these proprietary software connectors carry cost markups exceeding eight hundred percent, while zero-trust cybersecurity mandates are routinely waived in Statements of Work to meet arbitrary deployment deadlines.",
        "The result is a dangerous paradox: tactical warfighters on edge platforms—from F-35 fighters to naval strike groups—suffer severe data latency and packet drops during joint exercises, while defense cloud vendors lock the Pentagon into indefinite subscription licensing and compounding data egress penalties. Taxpayers foot the bill for billions in redundant software bridges that enrich Silicon Valley and defense IT conglomerates without delivering battlefield survivability.",
        "Yet this vulnerability in centralized military command architectures has clear Cold War precedents. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, the Soviet military spent decades constructing massive automated command and control networks that suffered from the exact same systemic flaws.",
        "According to Shvets, the Soviet Armed Forces invested billions of rubles into their automated control systems, known as ASU, including the Vozdukh air defense grid and the Manevr battlefield network. Shvets revealed that Soviet design bureaus inflated procurement costs by manufacturing incompatible proprietary hardware for each military branch, creating bureaucratic fiefdoms that resisted centralized integration. Crucially, Shvets disclosed that the KGB Sixteenth Directorate and Western SIGINT exploited these unstandardized communication nodes, intercepting unencrypted data relays during live exercises and compromising the Kremlin's strategic command vaults.",
        "From Soviet ASU design bureaus manufacturing incompatible hardware to Pentagon contractors billing eight-hundred-percent markups on cloud API wrappers, the institutional pathology is identical: command and control architectures become vehicles for contractor grift rather than battlefield resilience. Audit the cloud invoices, inspect the middleware contracts, and stay alert. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="jadc2", title=EPISODE_DATA["title"])
    img.save(IMG_EP143, "WEBP", quality=92)
    print(f"Saved: {IMG_EP143}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP143, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP143,
        IMG_STUDIO,
        IMG_EP143,
        IMG_REX,
        IMG_EP143,
        IMG_STUDIO
    ]
    create_art_frames(EPISODE_DATA["id"], src_frames)
    
    # 4. Neural Voice Audio Synthesis
    print("[4/5] Synthesizing neural voice (Rex Vance via edge-tts)...")
    full_script = " ... \n\n ".join(EPISODE_DATA["paragraphs"])
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, mp3_path)
    actual_seconds = get_audio_duration(mp3_path)
    print(f"Synthesized Rex Vance audio: {mp3_path} ({actual_seconds}s)")
    
    # 5. Manifest & Metadata Registration
    print("[5/5] Registering in episodes.json...")
    t_step = actual_seconds / 6.0
    frame_times = [int(round(i * t_step)) for i in range(6)]
    
    full_episode_entry = {
        "id": EPISODE_DATA["id"],
        "hour": EPISODE_DATA["hour"],
        "date": EPISODE_DATA["date"],
        "kind": EPISODE_DATA["kind"],
        "category": EPISODE_DATA["category"],
        "title": EPISODE_DATA["title"],
        "subject": EPISODE_DATA["subject"],
        "paragraphs": EPISODE_DATA["paragraphs"],
        "art": {
            "frames": [
                {"t": frame_times[i], "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
                for i in range(6)
            ]
        },
        "seconds": actual_seconds,
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
        
    manifest["episodes"].insert(0, full_episode_entry)
    manifest["updated"] = "2026-10-06T16:45:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
