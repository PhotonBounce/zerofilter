# engine/produce_episode_46.py
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

IMG_EP46 = os.path.join(THUMBS_DIR, "2026-10-07-22.webp")
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
    "id": "2026-10-07-22",
    "hour": "22:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Red Sea Subsea Cable Sabotage, Bab el-Mandeb Chokepoints & Soviet Horn of Africa SIGINT",
    "subject": "Hourly uncensored breakdown: Rex Vance details the targeting of Red Sea submarine fiber optic conduits, Houthi maritime drone telemetry, and Yuri Shvets's insider analysis of Soviet naval intelligence outposts in the Horn of Africa and modern asymmetric choke-point doctrine.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-two hundred hours. Running through the shallow, treacherous seabed of the Bab el-Mandeb Strait, more than a dozen submarine fiber-optic cables carry over seventeen percent of all global internet traffic connecting Europe, the Middle East, and Asia. Today, this vital digital circulatory system faces unprecedented physical jeopardy. Anchor dragging incidents by targeted commercial vessels, loitering munition strikes, and covert seabed operations have severed major communication trunks, degrading financial telemetry and rerouting massive global data flows around the entire African continent.",
        "While initial media reports blamed maritime accidents, operational intelligence tells a vastly different story. An anchor severance in shallow water requires precise bathymetric positioning, drift calculations, and timing. Iranian-supplied drone reconnaissance boats and electronic intelligence platforms operate continuously across the strait, monitoring vessel tracks and broadcasting spoofed navigational beacons. By synchronizing kinetic shipping harassment with infrastructure degradation, asymmetric proxy forces have effectively transformed the Red Sea into a contested, high-risk electronic and physical bottleneck.",
        "This choke-point strategy is not an ad-hoc local insurgency; it is the execution of a doctrine perfected during the Cold War. As former KGB foreign intelligence officer and Washington insider Yuri Shvets has documented, Soviet naval intelligence prioritized control of the Bab el-Mandeb Strait as an indispensable strategic objective. Operating from heavily fortified military bases on South Yemen's Socotra Island and Dahlak in Ethiopia, Soviet SIGINT units monitored every commercial tanker, Western warship, and submarine transiting between the Indian Ocean and the Mediterranean.",
        "According to Shvets, Soviet naval planners recognized that whoever commands the Bab el-Mandeb choke point holds a hydraulic vice over European energy supplies and transcontinental communications. Today's Moscow-Tehran axis has revived this exact geographic doctrine. By arming regional proxies with advanced anti-ship cruise missiles, loitering submersibles, and satellite targeting telemetry, adversary intelligence networks can impose billions of dollars in global shipping inflation and telecommunications latency without ever declaring formal interstate conflict.",
        "Western naval task forces continue engaging five-thousand-dollar loitering drones with two-million-dollar air defense missiles, an unsustainable economic attrition curve that completely ignores critical underlying structural vulnerabilities. Submarine fiber-optic cables on shallow continental shelves remain largely unpatrolled, physically unarmored, and legally ambiguous in international waters, creating a massive asymmetric opening that adversary alliances are actively exploiting to stress Western economic resilience.",
        "Audit the transoceanic seabed infrastructure, defend critical maritime choke points with dedicated subsea surveillance, and refuse to let asymmetric proxy cartels dictate the terms of global commerce. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="red_sea_cables")
    img.save(IMG_EP46, "WEBP", quality=92)
    print(f"Saved: {IMG_EP46}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP46, output_mp4, duration=10)
    
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
        IMG_EP46,
        IMG_REX,
        IMG_EP46,
        IMG_STUDIO,
        IMG_EP46,
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
