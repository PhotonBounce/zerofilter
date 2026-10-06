# engine/produce_episode_44.py
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

IMG_EP44 = os.path.join(THUMBS_DIR, "2026-10-07-20.webp")
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
    "id": "2026-10-07-20",
    "hour": "20:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "corruption",
    "title": "Silicon Valley Defense Cloud Lobbying, FISA 702 Renewals & KGB Wiretap Lineage",
    "subject": "Hourly uncensored breakdown: Rex Vance exposes the multi-billion-dollar defense cloud lobbying machine, FISA Section 702 warrantless backdoor search loopholes, and Yuri Shvets's insider analysis of Soviet KGB Operational-Technical Directorate telecommunications wiretaps.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty hundred hours. Behind the slick marketing of enterprise innovation, Silicon Valley's tech giants have quietly fused with the American national security state. The Pentagon's nine-billion-dollar Joint Warfighting Cloud Capability contract—divided among Amazon, Microsoft, Google, and Oracle—has unleashed an aggressive, behind-the-scenes lobbying war. Millions of dollars in political action committee funds and revolving-door advisory retainers flood Capitol Hill every quarter, ensuring that federal procurement specifications are tailored exclusively to protect this defense cloud oligopoly.",
        "Simultaneously, this defense cloud infrastructure serves as the primary processing engine for Section 702 of the Foreign Intelligence Surveillance Act. While statutory provisions claim Section 702 strictly targets non-citizens abroad, automated 'backdoor search' exceptions permit domestic intelligence agencies to query captured databases for Americans' personal communications without a judicial warrant. By siphoning raw telecommunications traffic through commercial optical splitters and hosting the resulting repositories on commercial defense cloud servers, the line between foreign signals intelligence and warrantless domestic surveillance has evaporated.",
        "This marriage between telecommunications infrastructure and state security mirrors an established authoritarian playbook. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet intelligence perfected this exact model decades ago. The KGB's Operational-Technical Directorate, specifically the Twelfth Department, held total, uninhibited authority over the Soviet telecommunications grid, hardwiring permanent taps directly into telephone exchanges without requiring legal oversight or institutional justification.",
        "According to Shvets, the institutional philosophy governing domestic wiretapping never changes: once an intelligence agency constructs a technological capability to intercept civilian communications, it will manufacture legal pretexts to preserve that conduit indefinitely. In the Soviet Union, state security invoked internal stability; in Washington, intelligence cartels invoke counter-terrorism and cyber defense. The underlying architecture remains identical: total communications visibility laundered through legal fictions and rubber-stamp compliance reviews.",
        "What makes today's surveillance architecture vastly more dangerous is private-sector collusion. Soviet engineers were constrained by analog copper lines and human transcribers. Today's commercial cloud cartels provide automated machine-learning classifiers, natural language parsing, and indefinite data storage, all funded by taxpayer defense appropriations. Silicon Valley lobbyists aggressively fight legislative warrant requirements because bulk data ingestion constitutes their most lucrative, recurring government revenue stream.",
        "Audit the cloud lobbying slush funds, close the warrantless 702 loopholes, and dismantle the surveillance-industrial complex before civil liberty is encrypted away. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="defense_cloud_fisa")
    img.save(IMG_EP44, "WEBP", quality=92)
    print(f"Saved: {IMG_EP44}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP44, output_mp4, duration=10)
    
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
        IMG_EP44,
        IMG_REX,
        IMG_EP44,
        IMG_STUDIO,
        IMG_EP44,
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
