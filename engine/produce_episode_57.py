# engine/produce_episode_57.py
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

IMG_EP57 = os.path.join(THUMBS_DIR, "2026-10-08-09.webp")
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
    "id": "2026-10-08-09",
    "hour": "09:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "quantum",
    "title": "Topological Superconductivity, Majorana Zero Modes & Soviet Cryogenic Physics Secrets",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates topological superconductivity in semiconductor-superconductor hybrid nanowires, non-Abelian Majorana zero modes for fault-tolerant topological quantum computing, and Yuri Shvets's insider analysis of Soviet Landau Institute cryogenic secrets and clandestine scientific intelligence collection.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero nine hundred hours. In the race toward fault-tolerant quantum computation, traditional superconducting qubits face an unforgiving adversary: local environmental decoherence. A stray thermal photon, a magnetic flux fluctuation, or nuclear spin noise can instantly corrupt a delicate quantum superposition. To bypass this quantum vulnerability, physics laboratories are racing to engineer topological superconductors. By coupling semiconductor indium arsenide nanowires to epitaxial superconducting aluminum shells under millikelvin dilution refrigeration and high magnetic fields, researchers coax electrons into collective quasiparticles known as Majorana zero modes.",
        "Majorana zero modes possess extraordinary physical properties: they are their own antiparticles, and their quantum information is stored non-locally across spatially separated wire boundaries. Because local electromagnetic noise cannot disturb both ends simultaneously, quantum states encoded in Majorana pairs are topologically protected from decoherence. Computational logic gates are executed not by delicate microwave pulses, but by braiding the worldlines of these non-Abelian anyons around one another in two-dimensional space. The result is a hardware-level immune system against quantum phase errors, promising quantum supercomputers capable of breaking standard RSA encryption without billions of physical error-correcting qubits.",
        "This quest for exotic condensed-matter states is deeply intertwined with Cold War scientific espionage. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet solid-state and cryogenic physics programs centered at the prestigious Landau Institute for Theoretical Physics were among the most closely guarded scientific secrets in the USSR. Under Lev Landau and Vitaly Ginzburg, Soviet theorists pioneered the mathematical foundations of superconductivity and phase transitions decades ahead of Western commercial applications.",
        "According to Shvets, the KGB’s Directorate T placed scientific liaison officers inside international physics conferences in Geneva, Cambridge, and Princeton to monitor Western attempts to verify Soviet low-temperature anomalies. Soviet intelligence prioritized the acquisition of helium-3 dilution refrigeration components, ultra-pure semiconductor crystal-growing chambers, and precision magnetometers embargoed under Western export controls. Shvets emphasizes that the Kremlin viewed condensed-matter physics as the strategic bedrock of military cryptanalysis and radar stealth, treating theoretical physics breakthroughs with the same secrecy as nuclear warhead designs.",
        "Today, as global superpowers race to construct the first scalable topological quantum processor, the legacy of Soviet cryogenic theory lives on. Majorana nanowires represent the bleeding edge where abstract topology meets weaponized computational supremacy. The nation that masters topological braiding will shatter global cryptographic communications while securing its own sovereign secrets inside topologically protected quantum states.",
        "Inspect the nanowire junctions, trace the topological braids, and audit the cryogenic foundations. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="majorana_zero_modes")
    img.save(IMG_EP57, "WEBP", quality=92)
    print(f"Saved: {IMG_EP57}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP57, output_mp4, duration=10)
    
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
        IMG_EP57,
        IMG_REX,
        IMG_EP57,
        IMG_STUDIO,
        IMG_EP57,
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
