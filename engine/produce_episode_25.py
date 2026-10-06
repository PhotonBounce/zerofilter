# engine/produce_episode_25.py
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

IMG_EP25 = os.path.join(THUMBS_DIR, "2026-10-07-01.webp")
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
    "id": "2026-10-07-01",
    "hour": "01:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Casimir Micro-Thrusters, Quantum Vacuum Engineering & Russian ASAT Kinematics",
    "subject": "Hourly uncensored breakdown: Rex Vance links dynamic Casimir effect micro-propulsion and quantum vacuum energy extraction with ex-KGB Major Yuri Shvets's analysis of Russian kinetic and co-orbital anti-satellite deployment strategies.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero one hundred hours. The empty vacuum of space is not empty at all; it is a roiling, ultra-dense sea of virtual particle-antiparticle pairs fluctuating at zero-point energy. In theoretical and experimental physics, the Casimir effect demonstrated that conductive boundary conditions force vacuum modes to exert measurable mechanical pressure. With modern nanofabrication and optomechanical resonators, the dynamic Casimir effect allows us to perturb the quantum vacuum dynamically, converting virtual photons into real, propagating electromagnetic propulsion without expending chemical propellant.",
        "In the geopolitical theater, the struggle to maneuver in orbital space without massive propellant signatures intersects directly with anti-satellite weapon doctrines. As Washington counter-intelligence analyst and former KGB Major Yuri Shvets has exposed, Moscow's space command has historically concealed kinetic anti-satellite hunter-killer satellites under the guise of peaceful orbital inspector spacecraft, such as the Cosmos-2542 and Cosmos-2543 missions that stalked sensitive US National Reconnaissance Office payloads.",
        "Standard orbital maneuvering is limited by the Tsiolkovsky rocket equation: every kilogram of hydrazine or xenon propellant you launch exponentially penalizes your payload capacity. Vacuum engineering breaks this bottleneck. By oscillating nanostructured metamaterial cavities at gigahertz frequencies, quantum micro-thrusters theoretically induce asymmetric radiation reaction forces directly from vacuum fluctuation gradients. Even micro-Newton thrust profiles, applied continuously over weeks in deep orbit, enable perpetual station-keeping, evasive maneuvering, and propellant-free constellation phasing that evade conventional ground radar orbital tracking algorithms.",
        "This explains why both the Pentagon's DARPA and the Russian Aerospace Forces are heavily financing advanced non-chemical propulsion laboratories. If an adversary fields co-orbital ASAT interceptors armed with kinetic fragmentation kill vehicles, stationary or predictable target satellites are sitting ducks. But if high-value orbital assets possess continuous, low-signature autonomous quantum maneuverability, kinetic collision trajectories become statistically impossible to lock on.",
        "Neutralizing the threat of kinetic space aggression demands combining continuous-burn vacuum maneuvering with distributed satellite defensive perimeters. By pairing quantum optomechanical micro-propulsion with autonomous laser proximity sensors and edge-computed evasion routines, next-generation orbital platforms can dodge incoming hypervelocity debris or interceptors without exhausting limited station-keeping fuel. Space superiority belongs to whatever faction decouples its orbital maneuverability from terrestrial supply lines.",
        "The universe offers infinite propulsion to those who understand the mathematics of the quantum vacuum. Trace the orbital flight paths, watch the inspection satellites, and never assume the vacuum is inert. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="casimir")
    img.save(IMG_EP25, "WEBP", quality=92)
    print(f"Saved: {IMG_EP25}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP25, output_mp4, duration=10)
    
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
        IMG_EP25,
        IMG_REX,
        IMG_EP25,
        IMG_STUDIO,
        IMG_EP25,
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
