# engine/produce_episode_59.py
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

IMG_EP59 = os.path.join(THUMBS_DIR, "2026-10-08-11.webp")
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
    "id": "2026-10-08-11",
    "hour": "11:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "corruption",
    "title": "Autonomous Drone Munitions Price Gouging, SBIR Grant Fraud & Soviet Tech Front Companies",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates systemic price gouging across Pentagon autonomous drone munitions procurement, Small Business Innovation Research grant fraud syndicates, and Yuri Shvets's insider analysis of Soviet intelligence shell companies capturing dual-use technologies.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eleven hundred hours. On the battlefields of Eastern Europe and the Middle East, autonomous first-person-view attack drones assembled from commercial off-the-shelf components costing under eight hundred dollars are destroying ten-million-dollar main battle tanks. Yet inside the Pentagon procurement bureaucracy, the exact opposite economic reality prevails: defense contractors are charging the Department of Defense up to eighty thousand dollars for functionally identical autonomous loitering munitions. This predatory price gouging is subsidized by systemic exploitation of federal Small Business Innovation Research grants, creating lucrative slush funds for defense venture syndicates.",
        "Investigative audits reveal a coordinated grift pipeline. Boutique defense startups secure non-dilutive SBIR Phase One and Phase Two research awards ostensibly to invent proprietary artificial intelligence target-recognition algorithms. In reality, these firms repackage open-source computer vision models, enclose consumer quadcopters inside proprietary composite airframes, and slap defense security clearances across the supply bill. By the time prime systems integrators resell these rebranded commercial units to the armed services, unit costs have inflated by ten thousand percent through cascading subcontracting management fees and sole-source technical data rights.",
        "This parasitic defense contracting racket has chilling parallels to Cold War covert procurement. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet foreign intelligence exploited the very same vulnerabilities in Western commercial defense contracting throughout the 1970s and 1980s. Operating through Directorate T, the KGB established hundreds of dummy import-export corporations across Western Europe and North America specifically designed to divert advanced dual-use avionics and microprocessors.",
        "According to Shvets, Soviet intelligence officers recognized that Western venture capitalists and defense subcontractors were blinded by greed and lax federal oversight. Front companies financed by Moscow routinely bid on small-scale defense R&D contracts, using Western taxpayers' own research subsidies to develop guidance software that was immediately exfiltrated back to Moscow design bureaus. Shvets emphasizes that when defense procurement lacks forensic technical accountability, both corrupt domestic cartels and hostile foreign intelligence services feed at the exact same public trough.",
        "Today, as autonomous warfare accelerates into mass algorithmic production, the Pentagon’s cost-plus culture threatens national survival. You cannot fight a prolonged industrial war of robotic attrition when a hostile adversary produces tactical strike drones for pennies on the dollar while domestic defense primes bill the treasury eighty thousand dollars per unit. The greatest threat to Western defense is not foreign hardware—it is the domestic procurement grift that hollows out military capability from within.",
        "Audit the SBIR grants, dismantle the defense price gouging, and follow the shell company money trails. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="drone_gouging")
    img.save(IMG_EP59, "WEBP", quality=92)
    print(f"Saved: {IMG_EP59}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP59, output_mp4, duration=10)
    
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
        IMG_EP59,
        IMG_REX,
        IMG_EP59,
        IMG_STUDIO,
        IMG_EP59,
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
