# engine/produce_episode_66.py
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

IMG_EP66 = os.path.join(THUMBS_DIR, "2026-10-08-18.webp")
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
    "id": "2026-10-08-18",
    "hour": "18:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Suwalki Gap Heavy Armor Logistics, Railway Gauge Incompatibility & Soviet Kaliningrad Corridor Doctrine",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the logistical nightmare of defending NATO's Suwalki Gap, railway break-of-gauge chokepoints between European standard and Russian broad gauge, and Yuri Shvets's insider analysis of Soviet military operational plans for the Kaliningrad transit corridor.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eighteen hundred hours. The Suwalki Gap—a narrow, sixty-five-mile strip of land wedged between the heavily fortified Russian military exclave of Kaliningrad and Belarus—is universally recognized as the most perilous strategic choke point on NATO's eastern frontier. But while defense think tanks obsess over hypersonic strikes and electronic warfare, the fatal vulnerability is far more mundane, brutal, and mechanical: railway transport logistics. If hostile forces sever this narrow corridor, the Baltic republics of Lithuania, Latvia, and Estonia are instantly severed from overland allied reinforcement.",
        "The physical mechanics of heavy armor mobility across Eastern Europe collapse at the break-of-gauge boundary. Western European railways operate on standard gauge of 1,435 millimeters, whereas the Baltic rail networks still rely on the legacy Soviet broad gauge of 1,520 millimeters. Moving heavy armored divisions, M1A2 Abrams main battle tanks, and heavy artillery requires painstaking break-of-gauge transshipment at the Polish-Lithuanian border—manually swapping wheel bogies or crane-lifting sixty-ton armored hulls between incompatible rail cars. In a contested combat environment saturated by loitering drone munitions and ballistic missile strikes, this logistical bottleneck creates a catastrophic stationary target.",
        "This geographic and logistical vulnerability was engineered by design during the Soviet era. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet General Staff operational planning explicitly preserved railway gauge incompatibility across former satellite states to prevent rapid Western mechanized counter-offensives. The Soviet Baltic Military District and Belarusian military commands maintained detailed operational dossiers on the Suwalki approaches, designating the corridor as the supreme operational axis to secure land communications with Kaliningrad.",
        "According to Shvets, the KGB's military counter-intelligence directorates closely coordinated with the Soviet Ministry of Railways to ensure that transport infrastructure directly served strategic deterrence. Today, modern interoperability projects like Rail Baltica remain years behind schedule and billions over budget due to bureaucratic inertia, contractor grift, and political infighting. Shvets emphasizes that while Western politicians deliver hawkish speeches on Baltic deterrence, they have systematically failed to fund the heavy transport logistics, reinforced railbeds, and heavy bridges required to move mechanized divisions across the Suwalki choke point.",
        "Today, the Suwalki Gap stands as an unforgiving reality check: wars are won by heavy logistics, industrial rail capacity, and supply lines, not empty political rhetoric. Without standardized rail corridors, reinforced river crossings, and hardened transshipment depots, rapid response forces remain paralyzed in transit. Military deterrence is a paper tiger without the steel rails to move it.",
        "Audit the rail gauge transfers, track the heavy armor logistics, and verify the transit corridors. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="suwalki_gap")
    img.save(IMG_EP66, "WEBP", quality=92)
    print(f"Saved: {IMG_EP66}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP66, output_mp4, duration=10)
    
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
        IMG_EP66,
        IMG_REX,
        IMG_EP66,
        IMG_STUDIO,
        IMG_EP66,
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
