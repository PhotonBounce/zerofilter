# engine/produce_episode_104.py
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

IMG_EP104 = os.path.join(THUMBS_DIR, "2026-10-10-08.webp")
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
    "id": "2026-10-10-08",
    "hour": "08:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "quantum",
    "title": "Superconducting Qubit Parity Measurements, Cat-State Error Correction & Soviet Quantum Intercept Archives",
    "subject": "Hourly uncensored breakdown: Rex Vance explores bosonic cat-state superconducting qubits with real-time photon number parity measurements for autonomous quantum error correction, and Yuri Shvets on Soviet quantum telemetry intercept attempts.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero eight hundred hours. Building fault-tolerant quantum computing systems has long been hindered by the staggering hardware overhead of conventional surface codes, which demand thousands of noisy physical qubits to protect a single logical qubit. However, a major architectural breakthrough is emerging from bosonic cat-state qubits stored in high-Q superconducting microwave cavities, where quantum information is encoded in macroscopically distinct superpositions of coherent electromagnetic states rather than discrete two-level artificial atoms.",
        "In bosonic cat qubits, phase-space symmetry naturally suppresses phase-flip errors exponentially by increasing the average photon number, leaving bit-flips as the only active error channel. To correct these residual bit-flips without destroying delicate quantum superpositions, dispersive coupling to non-linear ancilla transmons enables continuous, non-demolition photon-number parity measurements. When single photons leak into the environment, real-time quantum parity tracking registers odd-even photon shifts instantaneously, triggering autonomous active feedback pulses that stabilize the logical state indefinitely.",
        "This race to manipulate discrete microwave photons and stabilize fragile coherent states carries a remarkable Cold War intelligence lineage. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has illuminated, the Soviet Eighth Chief Directorate for cryptanalysis and signals intelligence established deep-cryogenics laboratories during the 1980s to explore quantum coherence for both cipher generation and secure microwave communication.",
        "According to Shvets, Soviet intelligence tasked elite theoretical physicists at the Kapitza Institute and Landau Institute with finding vulnerabilities in Western cryptographic key distribution. While Western agencies focused primarily on digital computer networks, Soviet signals intelligence officers investigated whether cryogenic microwave cavities could intercept low-power satellite communications without triggering quantum collapse. Shvets revealed that KGB technical teams realized that measuring quantum state parity was the ultimate prerequisite for unmasking covert signal tampering and defeating advanced passive interception.",
        "Today, that theoretical insight forms the bedrock of fault-tolerant quantum computing supremacy. By replacing sprawling arrays of millions of noisy physical transmons with compact, hardware-efficient cat-state resonators, defense research agencies are accelerating timelines toward cryptographically relevant quantum processors by an entire decade. Whoever masters real-time quantum parity tracking first will possess the hardware capable of breaking asymmetric public-key cryptography across global financial, defense, and intelligence backbones.",
        "Audit the federal quantum error correction benchmarks, track the emergence of bosonic cat-state processing nodes, and remember that when quantum errors can be corrected faster than entropy decays them, codebreaking becomes absolute. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="cat_state", title=EPISODE_DATA["title"])
    img.save(IMG_EP104, "WEBP", quality=92)
    print(f"Saved: {IMG_EP104}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP104, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP104, IMG_REX, IMG_STUDIO, IMG_EP104, IMG_REX, IMG_EP104]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # 4. Neural Audio Synthesis
    print("[4/5] Synthesizing Rex Vance neural baritone audio...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    dur = get_audio_duration(audio_path)
    print(f"Synthesized Audio: {audio_path} ({dur} seconds)")
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = dur / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
    EPISODE_DATA["seconds"] = dur
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
    print(f"Updated {MANIFEST_FILE} with episode {EPISODE_DATA['id']}!")
    
    # Copy cover to brain artifacts for documentation
    brain_cover = r"assets\cover_ep104_procedural.webp"
    with Image.open(IMG_EP104) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
