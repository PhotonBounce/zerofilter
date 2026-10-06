# engine/produce_episode_33.py
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

IMG_EP33 = os.path.join(THUMBS_DIR, "2026-10-07-09.webp")
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
    "id": "2026-10-07-09",
    "hour": "09:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Darwinism, Environmental Witnessing & Soviet Passive Resonator Surveillance",
    "subject": "Hourly uncensored breakdown: Rex Vance explores Wojciech Zurek's Quantum Darwinism and pointer state redundancy in emergent classicality, alongside Yuri Shvets's revelations regarding Soviet passive resonant acoustic surveillance apparatus like Léon Theremin's Thing.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero nine hundred hours. How does our familiar, objective classical reality emerge from the delicate, probabilistic fog of the quantum realm? The prevailing answer is Wojciech Zurek's formulation of Quantum Darwinism. Rather than environmental decoherence merely acting as a passive destroyer of quantum superpositions, the environment acts as an active witness. It relentlessly measures the system, proliferating trillions of redundant copies of robust, non-fragile quantum states known as pointer states into surrounding photon and particle fields.",
        "Because countless independent observers can measure separate fragments of the surrounding environment without perturbing the original system, they all deduce the exact same classical outcome. Objectivity is not an intrinsic property of solitary matter; it is an emergent consensus manufactured by information redundancy across an omnipresent ambient environment. If a quantum state cannot leave multiple indelible footprints in its surrounding thermal bath, it is systematically culled from classical existence.",
        "In the operational history of technical surveillance, Soviet intelligence pioneered this exact principle of using the ambient environment as an invisible witness. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has recounted, Soviet inventor Léon Theremin designed 'The Thing'—a covert passive cavity resonator bug embedded inside a carved wooden Great Seal of the United States hung in the American ambassador's Moscow office. The device contained no batteries, no vacuum tubes, and no active transmitter; it was completely inert until illuminated by an external radio frequency beam.",
        "When spoken words vibrated a microscopic metallic diaphragm across the cavity, the sound modulated the reflected radio wave, transmitting diplomatic conversations across Moscow rooftops. Just as Quantum Darwinism treats stray photons as passive carriers of redundant quantum pointer states, Soviet technical counter-intelligence recognized that passive acoustic reflection transforms the electromagnetic environment itself into an unmonitored intelligence conduit, defying standard swept radio frequency detectors for seven years.",
        "Today, the intersection of quantum sensing and passive ambient reconnaissance represents the frontier of modern electronic warfare. From optomechanical laser microphones measuring microscopic window vibrations to quantum magnetometer arrays detecting submarine magnetic anomalies through oceanic noise, security perimeters can no longer focus solely on active emitters. True counter-intelligence requires auditing every photon and acoustic wave that witnesses classified activity before environmental redundancy broadcasts your secrets to an adversary.",
        "Audit your physical environments, inspect the passive cavity reflections, and remember that nature is always keeping redundant records. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="quantum_darwinism")
    img.save(IMG_EP33, "WEBP", quality=92)
    print(f"Saved: {IMG_EP33}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP33, output_mp4, duration=10)
    
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
        IMG_EP33,
        IMG_REX,
        IMG_EP33,
        IMG_STUDIO,
        IMG_EP33,
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
