# engine/produce_episode_29.py
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

IMG_EP29 = os.path.join(THUMBS_DIR, "2026-10-07-05.webp")
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
    "id": "2026-10-07-05",
    "hour": "05:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Spin Liquids, Topological Braiding & Soviet Cipher Codebreaking",
    "subject": "Hourly uncensored breakdown: Rex Vance explores topological quantum computing with non-Abelian anyons in Kitaev honeycomb spin liquids, juxtaposed against Yuri Shvets's revelations regarding Soviet 8th Chief Directorate cryptographic efforts and modern post-quantum cipher vulnerability.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero five hundred hours. In standard quantum computing architectures, delicate superpositions of superconducting transmon qubits collapse into decoherent noise if struck by stray thermal fluctuations, cosmic ray strikes, or fluctuating stray magnetic fields. But deep within the frustrated magnetic geometry of a quantum spin liquid, condensed matter physics offers a radical escape hatch: long-range topological order. Here, electron spins refuse to freeze into conventional ferromagnetic or antiferromagnetic alignments even at absolute zero, giving rise to emergent, fractionalized quasiparticles known as non-Abelian anyons.",
        "When two non-Abelian anyons are braided around each other in two-dimensional space, the quantum wave function of the multi-particle system undergoes a discrete, non-commutative unitary transformation. This transformation depends exclusively on the topological knotting and braiding of their worldlines in spacetime, rendering the stored quantum information virtually immune to local environmental noise and decoherence. In the operational history of signals intelligence and cryptographic warfare, fault-tolerant mathematical topology has always been the ultimate holy grail for codebreakers.",
        "As Washington counter-intelligence insider and former KGB Major Yuri Shvets has recounted, the Soviet Union's Eighth Chief Directorate—responsible for state cryptanalysis, communications interception, and cipher security—maintained thousands of elite mathematicians tasked with identifying structural vulnerabilities in Western rotor and electronic encryption apparatus like the KL-7 and KW-26. The Soviets recognized that raw brute-force computing power is fundamentally doomed against exponential key permutations; true strategic cryptanalytic dominance requires uncovering hidden topological invariants and algebraic symmetries that bypass conventional mathematical defenses entirely.",
        "Today, the international race to synthesize synthetic Kitaev materials and realize fault-tolerant topological quantum computation has become the defining technological battleground between superpowers. If an adversarial intelligence service successfully braids non-Abelian anyons into robust, error-corrected logical qubits, the mathematical trapdoors underpinning global RSA and elliptic-curve public-key cryptography will dissolve in hours. Every terabyte of encrypted telemetry intercepted under modern 'harvest now, decrypt later' signals intelligence doctrines—from classified diplomatic cables to sovereign central banking ledgers—will become an immediate open book.",
        "To defend against this impending quantum cryptanalytic horizon, free societies cannot rely on incremental software patches or bureaucratic complacency. We must accelerate the transition of civilian and military communications backbones to lattice-based post-quantum algorithms, deploy satellite-mediated quantum key distribution networks with authenticated physical entanglement verification, and enforce uncompromising export controls on ultra-low-temperature dilution refrigerators and exotic crystalline substrates. In an age of algorithmic warfare, cryptographic sovereignty remains the indispensable cornerstone of democratic survival.",
        "Watch the braiding worldlines, audit the post-quantum cipher migration timelines, and never assume that encrypted silence means permanent security. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="topological_braiding")
    img.save(IMG_EP29, "WEBP", quality=92)
    print(f"Saved: {IMG_EP29}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP29, output_mp4, duration=10)
    
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
        IMG_EP29,
        IMG_REX,
        IMG_EP29,
        IMG_STUDIO,
        IMG_EP29,
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
