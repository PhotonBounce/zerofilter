# engine/produce_episode_100.py
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

IMG_EP100 = os.path.join(THUMBS_DIR, "2026-10-10-04.webp")
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
    "id": "2026-10-10-04",
    "hour": "04:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "quantum",
    "title": "Topological Photonic Crystal Waveguides, Quantum Hall Light Routing & Soviet Optical Analog Computing",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates topological photonic crystal waveguides utilizing quantum Hall edge states for backscatter-immune optical computing, and Yuri Shvets on Soviet optical analog computing programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero four hundred hours, and our one hundredth broadcast milestone. In the relentless physics race to surpass silicon electronic bottlenecks, photons offer near-infinite propagation velocity and zero ohmic heat dissipation. However, routing light within nanoscale photonic integrated circuits has historically suffered from optical backscattering caused by unavoidable micro-fabrication defects. Now, topological photonics is eliminating this barrier by designing synthetic photonic crystal lattices where light travels exclusively along topologically protected helical edge states.",
        "By emulating the quantum Hall and quantum spin Hall effects in synthetic optical materials, these photonic crystals engineer nonzero topological Chern invariants across their electromagnetic band structures. Light injected into these engineered waveguides bends around sharp corners and fabrication imperfections without losing a single quantum of energy to reflection or radiative decay. Coupled with non-reciprocal magneto-optical materials or synthetic gauge fields, topological photonic waveguides enable backscatter-immune optical signal processing and ultrafast photonic tensor computing at light speed.",
        "This quest to build computing architectures out of directed beams of light carries profound intelligence lineage. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has illuminated, Soviet military science recognized the inevitable physical limits of silicon computing decades before the West, pouring immense covert resources into analog optical computing and Fourier optical processors.",
        "According to Shvets, the Soviet Academy of Sciences and military research institutes in Leningrad and Moscow sought optical computing architectures to process real-time ballistic missile radar cross-sections and synthetic aperture sonar arrays without digital microprocessors, which the USSR could not reliably fabricate. Shvets revealed that KGB Directorate T—the scientific espionage arm—was tasked with stealing Western laser diodes and acousto-optic crystals, while Soviet physicists pioneered theoretical models of non-reciprocal spatial light modulators to perform instantaneous matrix multiplication.",
        "Today, that analog optical computing paradigm has merged with modern quantum topological materials. Modern optical neural networks constructed on topological photonic chips can compute complex deep learning matrices with near-zero latency and negligible electrical power, threatening to disrupt electronic semiconductor dominance. In signals intelligence, electronic warfare, and quantum cryptography, routing uncorrupted light along topological boundaries provides an unjammable computational advantage that purely digital silicon microchips can never match.",
        "Track the strategic semiconductor transition toward on-chip topological photonics, audit the military optical analog computing grants, and recognize that when light itself is harnessed without scatter, computation escapes the confines of matter. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} (CENTURY MILESTONE: EPISODE 100) ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="topological_photonics", title=EPISODE_DATA["title"])
    img.save(IMG_EP100, "WEBP", quality=92)
    print(f"Saved: {IMG_EP100}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP100, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP100, IMG_REX, IMG_STUDIO, IMG_EP100, IMG_REX, IMG_EP100]
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
    brain_cover = r"assets\cover_ep100_procedural.webp"
    with Image.open(IMG_EP100) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
