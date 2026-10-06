# engine/produce_episode_49.py
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

IMG_EP49 = os.path.join(THUMBS_DIR, "2026-10-08-01.webp")
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
    "id": "2026-10-08-01",
    "hour": "01:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "quantum",
    "title": "Topological Insulators, Dissipationless Helical Edge States & Soviet Solid-State Physics Intelligence Rings",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates topological insulators, quantum spin Hall dissipationless edge channels protected by time-reversal symmetry, and Yuri Shvets's insider analysis of Soviet Directorate T and Line X solid-state physics acquisition rings.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero one hundred hours. In modern condensed matter physics, topological insulators represent an unprecedented state of quantum matter: materials that behave as bulk electrical insulators while conducting electricity along their outer boundaries with near-zero energy dissipation. Unlike conventional conductors, the boundary conduction in two-dimensional and three-dimensional topological insulators is governed by helical edge states. In these quantum corridors, an electron's momentum is inextricably locked to its spin vector—an intrinsic quantum spin Hall effect protected by fundamental time-reversal symmetry.",
        "This topological protection means that electrons traversing helical edge channels cannot undergo backscattering from non-magnetic impurities, crystal defects, or surface roughness. Because backscattering requires reversing the electron's spin—which time-reversal symmetry strictly prohibits—current flows without the resistive heat losses that plague modern silicon semiconductors. In materials like mercury telluride quantum wells and bismuth selenide crystals, these dissipationless channels provide the hardware foundation for fault-tolerant spintronic processing, low-power defense sensors, and topological quantum computing architectures immune to local environmental decoherence.",
        "This race to control quantum materials has historical intelligence roots stretching back to the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, the Soviet Union's intelligence apparatus prioritized the acquisition of Western solid-state physics and crystal growth secrets above almost all other technical targets. Operating under KGB Directorate T and the military-industrial commission’s Line X task forces, Soviet scientific intelligence systematically infiltrated European and American solid-state laboratories throughout the late twentieth century.",
        "According to Shvets, Soviet defense leadership recognized early on that electronic warfare, radar cross-section analysis, and ballistic missile guidance systems were fundamentally bottlenecked by semiconductor physics and crystal purity. Through front companies established in Austria, Switzerland, and West Germany, Directorate T agents acquired Western molecular beam epitaxy machines, high-purity gallium arsenide ingots, and proprietary academic preprints. Shvets notes that Soviet physicists at secret institutes in Zelenograd relied heavily on these stolen Western crystallization methodologies to reverse-engineer microelectronic components for nuclear submarines and interceptor aircraft.",
        "Today, the geopolitical struggle over topological insulators and quantum materials has escalated into a high-stakes electronic warfare race. Modern defense primes and sovereign adversaries are competing to deploy topological spintronics into next-generation phased-array radars, cryogenic signal processors, and post-silicon cryptographic hardware. Just as in the Soviet era, scientific intelligence networks actively target research clusters to bypass decades of metallurgical trial and error. The boundary between academic solid-state physics and strategic statecraft remains as thin as a single topological monolayer.",
        "Track the helical edge currents, preserve time-reversal symmetry, and audit the scientific intelligence conduits. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="topological_insulators")
    img.save(IMG_EP49, "WEBP", quality=92)
    print(f"Saved: {IMG_EP49}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP49, output_mp4, duration=10)
    
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
        IMG_EP49,
        IMG_REX,
        IMG_EP49,
        IMG_STUDIO,
        IMG_EP49,
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
