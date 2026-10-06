# engine/produce_episode_35.py
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

IMG_EP35 = os.path.join(THUMBS_DIR, "2026-10-07-11.webp")
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
    "id": "2026-10-07-11",
    "hour": "11:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Penrose Orch-OR Gravitational Collapse, Anesthetic Binding & Soviet Bio-Telemetry",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes Sir Roger Penrose's Orchestrated Objective Reduction, Stuart Hameroff's tubulin quantum dipoles, anesthetic binding quenching, and Yuri Shvets's insider revelations regarding Soviet KGB Lab-12 psychopharmacology dossiers.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eleven hundred hours. For over three decades, mainstream neuroscience has insisted that human consciousness is merely the algorithmic output of classical synaptic firing—a complex computational illusion running on wet biological hardware. But mathematical physicist Sir Roger Penrose and anesthesiologist Stuart Hameroff dismantled this dogmatic reductionism through Orchestrated Objective Reduction, or Orch-OR. Their thesis is radical yet mathematically rigorous: conscious experience is not computational. It emerges from quantum coherent state reductions orchestrated within the cylindrical microtubule lattices of neural cytoskeletons.",
        "Inside each neuron, trillions of tubulin dimers form hollow thirteen-protofilament cylinders. Within these lattices, hydrophobic pockets containing aromatic tryptophan rings host collective delocalized pi-electron resonance clouds oscillating at terahertz frequencies. When general anesthetics like isoflurane or xenon extinguish human consciousness, they do not block classical ion channels or synaptic transmission; they selectively bind to these hydrophobic pockets, quenching quantum dipole oscillations. As Penrose proved through Gödel's incompleteness theorems, human mathematical insight transcends algorithmic computation because it accesses non-computable gravitational spacetime reductions where E sub G equals h-bar over tau.",
        "This intersection of quantum neurophysics and subjective awareness was tracked obsessively during the Cold War. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, Soviet intelligence operatives within the First Chief Directorate and the notorious Lab-12 dedicated decades to investigating psychopharmacological consciousness suppression. Declassified archival files reveal Soviet researchers attempted to synthesize pharmacological compounds capable of systematically decoupling neural coherence to induce compliant suggestibility during deep interrogation.",
        "Yet Soviet interrogators repeatedly ran into an insurmountable wall. While chemical toxins could destroy cognitive function or induce delirium, they could never selectively steer conscious will without destroying the delicate quantum resonance of the neural substrate. Shvets notes that Soviet state security repeatedly mistook biological resistance for counter-intelligence discipline, failing to recognize that genuine insight and subjective agency cannot be engineered through algorithmic conditioning or chemical coercion.",
        "In our modern era of surveillance capitalism and frontier artificial intelligence, this lesson is more urgent than ever. Silicon Valley tech monopolies and national security agencies spend billions attempting to reduce human consciousness to predictable behavioral algorithms and training datasets. But if Penrose is correct, machine intelligence will forever remain bounded by the Turing limit—incapable of genuine understanding or conscious agency. Silicon can compute, but it cannot collapse spacetime geometries.",
        "Audit the quantum coherence thresholds, recognize the non-computable foundation of human agency, and never confuse algorithmic simulation with genuine consciousness. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="orch_or")
    img.save(IMG_EP35, "WEBP", quality=92)
    print(f"Saved: {IMG_EP35}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP35, output_mp4, duration=10)
    
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
        IMG_EP35,
        IMG_REX,
        IMG_EP35,
        IMG_STUDIO,
        IMG_EP35,
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
