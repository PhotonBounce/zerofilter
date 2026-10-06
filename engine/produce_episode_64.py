# engine/produce_episode_64.py
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

IMG_EP64 = os.path.join(THUMBS_DIR, "2026-10-08-16.webp")
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
    "id": "2026-10-08-16",
    "hour": "16:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Spin Liquids in Kagome Antiferromagnets, Fractionalized Excitations & Soviet Solid-State Theory",
    "subject": "Hourly uncensored breakdown: Rex Vance explores quantum spin liquids in geometric kagome lattices, fractionalized spinon excitations and emergent gauge fields, and Yuri Shvets's insider analysis of Soviet Landau-school solid-state physics theory espionage.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is sixteen hundred hours. In conventional magnetic materials, thermal agitation freezes out as temperatures drop toward absolute zero, locking atomic spins into orderly ferromagnetic or antiferromagnetic crystal alignments. But in frustrated quantum magnets—specifically two-dimensional kagome lattices composed of corner-sharing triangles—geometric constraints prevent any conventional magnetic ordering from ever crystallizing. Even at absolute zero, quantum fluctuations dominate the lattice, creating an exotic, massively entangled state of matter: a quantum spin liquid, where electron spins fluctuate in perpetual, fluid-like macroscopic superposition.",
        "The physical mechanics of kagome antiferromagnets produce astonishing quantum phenomena. Because adjacent triangular spins cannot simultaneously satisfy anti-parallel alignment, the magnetic ground state becomes exponentially degenerate. Instead of conventional spin-wave magnons with integer spin, quantum spin liquids host fractionalized quasiparticle excitations: neutral spinons carrying fractional spin-one-half without electrical charge, and visons governed by emergent topological gauge fields. These non-local entangled states are topologically protected against environmental thermal noise, offering a groundbreaking architectural blueprint for fault-tolerant quantum memory and topological quantum computing.",
        "This mathematical frontier of macroscopic quantum entanglement has deep roots in Cold War theoretical physics. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet theoretical physics was dominated by the elite Landau School in Moscow and the Kapitza Institute for Physical Problems. Soviet physicists were recognized world pioneers in frustrated magnetism, superfluidity, and many-body quantum field theory, recognizing decades ago that condensed matter systems could simulate relativistic high-energy particle physics directly on a laboratory benchtop.",
        "According to Shvets, the KGB's Directorate T maintained dedicated scientific intelligence desks tasked with monitoring Western academic physics literature and tracking international symposiums on geometric frustration, neutron scattering, and cryogenic crystal synthesis. Soviet intelligence sought to cross-reference Western experimental findings against the proprietary theoretical equations produced by Soviet physics academies. Shvets emphasizes that the Kremlin viewed quantum solid-state theory as a supreme strategic asset with direct implications for future quantum cryptanalysis, low-temperature microelectronics, and ultra-sensitive passive submarine detection sensors.",
        "Today, the global race to synthesize pristine kagome mineral crystals like herbertsmithite represents a critical vector in sovereign quantum supremacy. While commercial tech conglomerates waste billions chasing noisy, brute-force physical qubits, the true technological revolution lies in topological quantum spin liquids, where fundamental physics shields quantum information. Whoever masters fractionalized quantum excitations will control the next century of computing.",
        "Audit the kagome spin lattices, track the fractionalized spinons, and verify the quantum gauge fields. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="kagome_spin_liquid")
    img.save(IMG_EP64, "WEBP", quality=92)
    print(f"Saved: {IMG_EP64}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP64, output_mp4, duration=10)
    
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
        IMG_EP64,
        IMG_REX,
        IMG_EP64,
        IMG_STUDIO,
        IMG_EP64,
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
