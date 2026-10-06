# engine/produce_episode_67.py
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

IMG_EP67 = os.path.join(THUMBS_DIR, "2026-10-08-19.webp")
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
    "id": "2026-10-08-19",
    "hour": "19:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Hypersonic Flight Test Concealment, Cost-Plus Lobbying Waivers & Soviet Scramjet Espionage",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates chronic hypersonic flight test failures concealed from congressional oversight, revolving-door cost-plus lobbying waivers, and Yuri Shvets's insider analysis of Soviet scramjet aerodynamic espionage networks.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is nineteen hundred hours. While the Pentagon publicly broadcasts panicked alarms of Russian and Chinese hypersonic missile supremacy, American hypersonic glide vehicle and scramjet development programs have quietly descended into a multi-billion-dollar quagmire of concealed test aborts, thermal boundary-layer delaminations, and chronic cost-plus contracting abuse. Behind classified special access program firewalls, prime aerospace contractors routinely mask catastrophic flight test disintegrations under vague bureaucratic press releases citing telemetry anomalies and partial data collection successes.",
        "The physical reality of hypersonic flight at velocities exceeding Mach 5 is violently unforgiving. Air-breathing scramjet engines must sustain supersonic combustion within a millimeter-thin airflow channel where volatile hydrocarbon or hydrogen fuel has barely one millisecond to mix, atomize, and ignite. At sustained hypersonic speeds, extreme atmospheric friction creates stagnation temperatures surpassing two thousand degrees Celsius, ionizing surrounding atmospheric gases into a blinding plasma sheath that severs radio-frequency telemetry and causes microscopic delaminations in carbon-carbon leading edges. Rather than solving fundamental boundary-layer turbulence and severe thermal shock physics, contractors rely on classified lobbying waivers to bypass mandatory flight test benchmarks while collecting lucrative cost-plus award fees.",
        "This cycle of technological overpromising and procurement deception has a direct historical parallel in Soviet defense procurement. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet aerospace ministries and Gosplan planners routinely concealed scramjet test failures and aerodynamic research dead-ends to preserve their classified black budgets. Directorate T of the KGB was specifically tasked with stealing American scramjet computational fluid dynamics codes and high-temperature alloy patents to cover up domestic design blunders.",
        "According to Shvets, Soviet intelligence stations across North America systematically targeted university aerospace engineering departments, wind tunnel facilities, and defense sub-tier contractors to harvest telemetry and ceramic matrix composite secrets. Soviet planners understood that bureaucratic self-preservation in the defense industrial complex always takes precedence over engineering truth. Shvets emphasizes that modern American defense procurement mirrors late-Soviet Gosplan stagnation: a lucrative revolving door of retired flag officers joining aerospace lobbying boards, securing classified cost-plus contract extensions regardless of catastrophic flight failures.",
        "Today, the systematic concealment of hypersonic flight failures represents an existential threat to sovereign defense credibility. You cannot deceive the immutable laws of aerothermodynamics with slick marketing spin or congressional lobbying waivers. When kinetic reality confronts the balance sheet, paper hypersonic prototypes incinerate upon re-entry.",
        "Audit the flight telemetry, inspect the lobbying waivers, and verify the scramjet combustors. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="scramjet_failure")
    img.save(IMG_EP67, "WEBP", quality=92)
    print(f"Saved: {IMG_EP67}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP67, output_mp4, duration=10)
    
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
        IMG_EP67,
        IMG_REX,
        IMG_EP67,
        IMG_STUDIO,
        IMG_EP67,
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
