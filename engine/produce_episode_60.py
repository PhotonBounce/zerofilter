# engine/produce_episode_60.py
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

IMG_EP60 = os.path.join(THUMBS_DIR, "2026-10-08-12.webp")
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
    "id": "2026-10-08-12",
    "hour": "12:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Biophotonic Cellular Signaling, Mitogenetic Radiation & Soviet Bio-Resonance Archives",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates ultra-weak biophoton emission in neural tissue, coherent electromagnetic cellular signaling, and Yuri Shvets's insider analysis of Alexander Gurwitsch's mitogenetic radiation research and Soviet military bio-resonance weaponization programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twelve hundred hours. Inside living biological tissue, life communicates not merely through chemical neurotransmitters and slow ionic cascades, but through light. Every living cell continuously emits an ultra-weak stream of optical photons, radiating between two hundred and eight hundred nanometers at intensities of mere tens of photons per square centimeter per second. Known in modern biophysics as biophotons, these optical emissions originate within mitochondrial oxidative metabolism and lipid peroxidation. However, growing experimental evidence reveals that biophotonic flux is not cellular waste heat—it is a coherent electromagnetic signaling mechanism orchestrating cellular division and neural synchronization.",
        "In the human central nervous system, biophotonic signaling operates as a secondary, high-bandwidth communication channel alongside conventional synaptic action potentials. Microtubules and myelinated axon sheaths function as microscopic optical waveguides, channeling biophotons along neural pathways with minimal scattering. This intracellular light field exhibits Poisson photon statistics indicative of quantum optical coherence, supporting theories that prefrontal neural assemblies exchange quantum-correlated states. When pathological conditions such as ischemic stroke or neurodegenerative decay occur, biophotonic emission patterns undergo radical phase shifts, transforming from coherent optical resonance into chaotic photon bursts.",
        "This optical paradigm of biology traces directly back to foundational Soviet science. In the 1920s, Soviet histologist Alexander Gurwitsch first discovered that dividing onion root cells emitted ultra-weak ultraviolet radiation that stimulated cell division in adjacent tissues—a phenomenon he termed mitogenetic rays. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently documented, Gurwitsch’s research was never dismissed by the Soviet state; instead, it was classified and subsumed into secret military research institutes overseen by the KGB’s Special Department.",
        "According to Shvets, Soviet bio-cyberneticists at closed facilities in Novosibirsk and Pushchino sought to harness mitogenetic radiation to detect biological warfare agents, monitor human operator stress at distance, and induce targeted bio-energetic disruptions. Soviet researchers constructed ultra-sensitive photomultiplier chambers shielded with lead and liquid nitrogen to decode the biophotonic signatures of human consciousness and organ failure. Shvets emphasizes that the Kremlin viewed biophotonics not as fringe science, but as a strategic frontier capable of superseding Western pharmaceutical paradigms through targeted non-thermal electromagnetic intervention.",
        "Today, as Western nanophotonics and quantum biology converge on the cellular light field, the insights of Soviet bio-resonance archives are being validated. From optical neural implants to non-invasive biophotonic cancer diagnostics, science is confirming that consciousness is intrinsically luminous. Beneath the biochemical machinery of life lies an intricate web of coherent light, governing the architecture of thought and vitality.",
        "Inspect the neural waveguides, measure the biophotonic coherence, and decode the cellular light fields. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="biophoton")
    img.save(IMG_EP60, "WEBP", quality=92)
    print(f"Saved: {IMG_EP60}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP60, output_mp4, duration=10)
    
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
        IMG_EP60,
        IMG_REX,
        IMG_EP60,
        IMG_STUDIO,
        IMG_EP60,
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
