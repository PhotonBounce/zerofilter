# engine/produce_episode_105.py
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

IMG_EP105 = os.path.join(THUMBS_DIR, "2026-10-10-09.webp")
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
    "id": "2026-10-10-09",
    "hour": "09:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Neural Biophoton Emission in Purkinje Cells, Metabolic Uncoupling & KGB Bio-Energetic Files",
    "subject": "Hourly uncensored breakdown: Rex Vance examines ultra-weak biophoton emissions from cerebellar Purkinje neurons linked to mitochondrial reactive oxygen species and non-chemical cell signaling, and Yuri Shvets on Soviet psychotronics and bio-resonance programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero nine hundred hours. In contemporary neurobiology, neural communication has long been treated as an exclusively electrochemical phenomenon—action potentials propagating across axons and neurotransmitters traversing synaptic clefts. Yet an elusive optical dimension operates simultaneously within living brain tissue: ultra-weak biophoton emission. Emitted in the near-ultraviolet to visible spectrum between two hundred and eight hundred nanometers, these spontaneous photons originate from metabolic lipid peroxidation inside neuronal mitochondria.",
        "Recent experimental biophysics demonstrates that cerebellar Purkinje cells—among the most metabolically active and geometrically intricate neurons in the human brain—exhibit distinctive biophoton emission fluctuations during metabolic uncoupling and synaptic excitation. Rather than serving merely as metabolic waste, evidence suggests these guided photons travel along myelin sheaths acting as optical dielectric waveguides. This biological fiber-optic network facilitates non-chemical, speed-of-light signaling across coordinated cerebellar microzones, coordinating motor timing and high-dimensional cognitive integration far beyond chemical diffusion rates.",
        "This optical signaling mechanism directly validates one of the most secretive research agendas pursued by Soviet military intelligence. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet science maintained an institutional obsession with mitogenetic radiation, biophotonics, and bio-energetic field transmission dating back to Alexander Gurwitsch's early discoveries in the 1920s.",
        "According to Shvets, the KGB First Chief Directorate and Department 12 channeled vast off-the-books funding into specialized laboratories at Moscow State University, Novosibirsk, and Rostov. Soviet researchers deployed ultra-sensitive photomultiplier tubes in light-sealed underground bunkers, attempting to detect whether human subjects under extreme stress or cognitive load emitted anomalous biophotonic signatures. Shvets revealed that Soviet military planners sought to exploit cellular optical emissions for remote interrogation monitoring and covert biometric tracking, seeking to quantify human consciousness through raw photon counts.",
        "Today, advanced quantum optics and single-photon avalanche detectors have transformed this historical inquiry into rigorous scientific reality. Modern defense laboratories are exploring whether neural biophotonics can serve as non-invasive diagnostic indicators of cognitive fatigue, traumatic brain injury, or neural degradation in combat pilots and intelligence operators. By capturing the faint optical shimmer of living cerebral tissue, researchers are opening an unmapped optical window into the physical machinery of human awareness.",
        "Audit the military biophotonics and neuro-optical surveillance budgets, track the development of single-photon neural sensors, and remember that deep inside the skull, the living mind generates its own light. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="biophoton", title=EPISODE_DATA["title"])
    img.save(IMG_EP105, "WEBP", quality=92)
    print(f"Saved: {IMG_EP105}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP105, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP105, IMG_REX, IMG_STUDIO, IMG_EP105, IMG_REX, IMG_EP105]
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
    brain_cover = r"assets\cover_ep105_procedural.webp"
    with Image.open(IMG_EP105) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
