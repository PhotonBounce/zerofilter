# engine/produce_episode_41.py
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

IMG_EP41 = os.path.join(THUMBS_DIR, "2026-10-07-17.webp")
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
    "id": "2026-10-07-17",
    "hour": "17:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Superconducting Transmon Qubits, Surface Codes & Soviet SIGINT Cryptanalysis",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes superconducting transmon qubit coherence limits, surface code syndrome extraction, and Yuri Shvets's insider revelations regarding Soviet Eighth Chief Directorate cryptanalysis and modern Harvest Now Decrypt Later operations.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is seventeen hundred hours. Suspended inside multi-stage gold-plated dilution refrigerators chilled to fifteen millikelvin—colder than the vacuum of deep interstellar space—superconducting transmon qubits represent the cutting edge of quantum computation. By coupling nonlinear Josephson junction inductors to microfabricated capacitor pads, physicists create artificial two-level quantum systems capable of macroscopic electromagnetic superposition. But raw physical qubits remain exceptionally fragile, continually assaulted by microscopic dielectric defects, material impurities, and stray thermal photons that destroy phase coherence within microseconds.",
        "To conquer this environmental noise, quantum computer architects deploy planar rotated surface codes. By arranging physical transmons into a two-dimensional lattice, errors are actively detected through continuous, non-destructive syndrome measurements executed by interleaved ancilla qubits. Operating with fault-tolerant distances exceeding seven, these lattices suppress logical error rates exponentially. Once an architecture fields roughly four thousand error-corrected logical qubits, Shor's algorithm transitions from theoretical mathematics into an operational weapon capable of shattering RSA-2048 and elliptic-curve cryptography in seconds.",
        "This looming cryptographic threshold has triggered an aggressive, covert intelligence race across the globe. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, Soviet intelligence recognized the strategic primacy of signals interception decades ago. The KGB's Eighth Chief Directorate was dedicated entirely to breaking Western diplomatic ciphers, tapping undersea military communication conduits, and exfiltrating encrypted diplomatic cables with the explicit intent of storing them until codebreaking advances rendered them readable.",
        "According to Shvets, contemporary foreign intelligence services—especially those operating within Moscow and Beijing—are executing this identical doctrine at massive scale through Harvest Now, Decrypt Later operations. Adversary cyber units are continuously vacuuming up petabytes of encrypted Western military telemetry, diplomatic traffic, and intellectual property. They cannot decrypt this intelligence today; they are banking the data until fault-tolerant quantum processors come online, confident that twenty-year-old secrets will still compromise national security.",
        "Relying on legacy encryption while assuming practical fault-tolerant quantum computers remain decades away is a fatal strategic blunder. The global migration toward post-quantum lattice-based algorithms cannot wait for formal commercial announcements; the exfiltration and storage of encrypted state secrets is occurring right now across compromised backbones. In the modern cryptographic theater, whichever superpower first scales error-corrected quantum coherence will hold the master keys to the digital world.",
        "Audit the dilution cryostats, deploy post-quantum cryptographic standards immediately, and refuse to let tomorrow's algorithms dismantle today's sovereignty. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="transmon_qubit")
    img.save(IMG_EP41, "WEBP", quality=92)
    print(f"Saved: {IMG_EP41}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP41, output_mp4, duration=10)
    
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
        IMG_EP41,
        IMG_REX,
        IMG_EP41,
        IMG_STUDIO,
        IMG_EP41,
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
