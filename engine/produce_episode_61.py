# engine/produce_episode_61.py
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

IMG_EP61 = os.path.join(THUMBS_DIR, "2026-10-08-13.webp")
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
    "id": "2026-10-08-13",
    "hour": "13:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Diamond NV-Center Magnetometry, GPS-Denied Navigation & Soviet Solid-State Sensors",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates quantum diamond nitrogen-vacancy center magnetometers, geomagnetic crustal anomaly mapping for unjammable GPS-denied navigation, and Yuri Shvets's insider analysis of Soviet solid-state sensor espionage and clandestine quantum physics pipelines.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is thirteen hundred hours. In modern electronic warfare, satellite-based GPS navigation is a fragile, easily severed tether. Across contested conflict zones, high-power radio-frequency jammers and spoofing transmitters render conventional satellite positioning useless. To survive in GPS-denied battlespaces, advanced defense aerospace platforms and autonomous undersea vehicles are turning to quantum sensor physics: diamond nitrogen-vacancy center magnetometry. By embedding point defects into synthetic diamond crystal lattices—replacing two carbon atoms with a single nitrogen atom and an adjacent atomic vacancy—physicists create atomic-scale magnetic sensors operating at room temperature.",
        "The quantum operational mechanics are astonishingly elegant. When illuminated by green laser light, the electron spin state of the nitrogen-vacancy defect can be initialized and read out via optically detected magnetic resonance. External magnetic fields induce Zeeman energy splitting in the triplet ground state, causing precise shifts in the emitted red photoluminescence. These quantum diamond sensors can detect magnetic variations as minute as picoteslas. By cross-referencing real-time magnetic fluctuations against high-resolution geological crustal magnetic maps, aircraft, cruise missiles, and nuclear submarines can navigate across the globe with pinpoint accuracy without emitting a single radio signal or relying on external satellite downlinks.",
        "This mastery of solid-state quantum anomalies has a direct Cold War pedigree. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet defense leadership recognized that American GPS navigation would dominate future warfare. In response, the Soviet Ministry of Electronics Industry and the KGB’s Directorate T launched massive clandestine intelligence programs focused on solid-state sensor physics, optical crystal synthesis, and magnetometry to counter Western electronic warfare.",
        "According to Shvets, Soviet intelligence stations in Western Europe systematically targeted synthetic diamond research laboratories, high-purity chemical vapor deposition suppliers, and precision microwave spectroscopy firms. Soviet military theorists sought passive, unjammable navigation and submarine detection systems that could map the Earth’s gravitational and magnetic contours. Shvets emphasizes that the Kremlin viewed quantum-level solid-state sensing as the ultimate asymmetric counterweight to Western satellite dominance, investing heavily in domestic crystal synthesis institutes across Moscow and Leningrad.",
        "Today, as electronic warfare curtains black out satellite navigation across global skies, quantum magnetometry is revolutionizing sovereign deterrence. In an era where satellites can be jammed, blinded, or destroyed in low Earth orbit, the immutable magnetic signature of the Earth's crust provides an unjammable navigational baseline. Quantum diamond sensors prove that when space-based systems fail, atomic-scale physics holds the line.",
        "Audit the magnetic anomaly maps, inspect the diamond crystal lattices, and verify the quantum sensors. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="diamond_magnetometry")
    img.save(IMG_EP61, "WEBP", quality=92)
    print(f"Saved: {IMG_EP61}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP61, output_mp4, duration=10)
    
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
        IMG_EP61,
        IMG_REX,
        IMG_EP61,
        IMG_STUDIO,
        IMG_EP61,
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
