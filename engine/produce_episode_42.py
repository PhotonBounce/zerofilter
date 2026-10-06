# engine/produce_episode_42.py
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

IMG_EP42 = os.path.join(THUMBS_DIR, "2026-10-07-18.webp")
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
    "id": "2026-10-07-18",
    "hour": "18:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Hormuz Strait Electronic Spoofing, Drone Guidance Backdoors & Axis Tech Barter",
    "subject": "Hourly uncensored breakdown: Rex Vance details Iranian GNSS spoofing rings in the Strait of Hormuz, Shahed loitering munition inertial navigation systems, and Yuri Shvets's insider analysis of Moscow-Tehran military-technical exchanges and illicit dual-use avionics pipelines.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eighteen hundred hours. In the narrow maritime choke point of the Strait of Hormuz, commercial tankers, container ships, and naval patrols are encountering unprecedented electronic warfare. High-power shore-based transmitters operated by the Islamic Revolutionary Guard Corps are actively spoofing civilian Global Navigation Satellite Systems, broadcasting false satellite ephemeris data that manipulates vessel automatic identification systems. Tankers operating in international transit lanes suddenly find their shipboard chartplotters indicating they have entered Iranian territorial waters, creating artificial navigational pretexts for maritime seizures and coastal boardings.",
        "Simultaneously, Iranian drone engineers have upgraded the navigation stacks across their Shahed-series one-way attack drones. Originally reliant on commercial satellite positioning receivers vulnerable to tactical GPS jamming, recent teardowns of downed airframes reveal multi-element CRPA controlled-reception pattern antennas and advanced strapdown inertial navigation systems. These hardened guidance units integrate MEMS gyroscopes and optical terrain-matching sensors, allowing loitering munitions to maintain dead-reckoning accuracy across contested corridors even when adversary jamming pods blanket the entire electromagnetic spectrum.",
        "This rapid avionics leap is not an isolated domestic achievement; it is fueled by a direct bilateral technology exchange. As former KGB intelligence officer and Washington counter-intelligence insider Yuri Shvets has repeatedly disclosed, the geopolitical partnership between Moscow and Tehran has transformed into a high-stakes military barter pact. Faced with crippling international sanctions, Russia trades advanced electronic warfare gear, air defense radars, and space-based reconnaissance data directly in exchange for Iranian drone swarms and ballistic missile shipments.",
        "According to Shvets, the intelligence lineage behind this cooperation traces directly back to Soviet-era Middle Eastern proxy networks. Moscow's defense establishment provides Tehran with specialized frequency-hopping electronic countermeasures and signals interception software originally perfected against NATO borders. In return, Iranian technical teams supply combat telemetry and field diagnostics, enabling both regimes to iteratively patch guidance vulnerabilities and circumvent Western export controls through third-party shell corporations operating in Dubai and Central Asia.",
        "Western policy responses remain dangerously reactive, treating maritime harassment in the Persian Gulf and aerial strikes across Eastern Europe as disconnected regional crises. In reality, they represent a unified, synchronized asymmetric warfare testbed. Dual-use microelectronics manufactured in allied nations continue slipping through porous supply chains, ending up in both Iranian drones and Russian guidance computers to test Western integrated air defenses.",
        "Audit the avionics supply chains, sever the illicit maritime tech corridors, and dismantle the barter networks before electronic warfare blinds our strategic waterways. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="hormuz_spoofing")
    img.save(IMG_EP42, "WEBP", quality=92)
    print(f"Saved: {IMG_EP42}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP42, output_mp4, duration=10)
    
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
        IMG_EP42,
        IMG_REX,
        IMG_EP42,
        IMG_STUDIO,
        IMG_EP42,
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
