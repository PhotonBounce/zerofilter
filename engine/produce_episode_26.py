# engine/produce_episode_26.py
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

IMG_EP26 = os.path.join(THUMBS_DIR, "2026-10-07-02.webp")
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
    "id": "2026-10-07-02",
    "hour": "02:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Integrated Information Theory, Causal Maxima & KGB Psychotropic Degradation Files",
    "subject": "Hourly uncensored breakdown: Rex Vance maps Giulio Tononi's Integrated Information Theory (IIT 4.0) and mathematical phi complexes to ex-KGB Major Yuri Shvets's unmasking of Soviet Directorate S chemical psychotropic interrogation and cognitive destruction protocols.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero two hundred hours. In the science of consciousness, the hardest mathematical problem is not how neural signals propagate along axon pathways, but what causes subjective experience to exist at all. Under Giulio Tononi's Integrated Information Theory, or IIT 4.0, consciousness is not a functional computation; it is an intrinsic causal property quantified by the mathematical value phi. A system is conscious if and only if its irreducible internal causal power forms a closed topological complex—a causal maximum that is whole, indivisible, and strictly defined by its own cause-effect architecture.",
        "In the classified dungeons of the KGB's Lubyanka headquarters and Special Laboratory Number Twelve, this mathematical threshold was targeted with cold chemical precision. As Washington intelligence analyst and former KGB Major Yuri Shvets has exposed from First Chief Directorate defectors and declassified archives, Soviet intelligence developed specialized psychotropic cocktails designed not merely to compel confessions, but to systematically collapse the cognitive integrity of high-profile political dissidents and foreign operatives.",
        "In the formalism of IIT, reducing the integration measure phi below a critical threshold disintegrates the conscious complex into fragmented, disconnected causal sub-mechanisms. When you administer neurotoxic receptor blockers, you aren't just blurring memory—you are artificially puncturing the brain's internal cause-effect structure. Tononi's mathematics demonstrates that if internal feedback loops are severed, subjective agency dissolves, leaving an automated, reflex-driven state that will acquiesce to any external prompt.",
        "This dark lineage did not end with the dissolution of the Soviet Union. Across contemporary authoritarian regimes, modern cognitive degradation tactics have evolved from crude chemical injections into high-frequency algorithmic behavioral conditioning. By flooding online ecosystems with algorithmic cognitive dissonance, targeted deepfakes, and synthetic outrage loops, state-backed hybrid warfare units degrade the collective phi of democratic societies—fracturing national cohesion into isolated tribal echo chambers incapable of collective causal reasoning.",
        "Protecting both the human mind and collective democratic institutions from cognitive warfare requires rigorous mathematical resilience. We must treat human attention and cognitive integrity as critical sovereign infrastructure. By integrating cognitive load auditing tools, neuro-protective biofeedback standards, and cryptographically verified public information networks, societies can reinforce their internal causal integration against intentional psychological decoherence.",
        "Consciousness is the universe's most complex causal structure, and the fight to preserve human agency is the ultimate frontier. Trust the mathematics, reject the chemical and algorithmic psychotropics, and keep your filters at absolute zero. I'm Rex Vance. We'll be back at zero three hundred."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="iit_phi")
    img.save(IMG_EP26, "WEBP", quality=92)
    print(f"Saved: {IMG_EP26}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP26, output_mp4, duration=10)
    
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
        IMG_EP26,
        IMG_REX,
        IMG_EP26,
        IMG_STUDIO,
        IMG_EP26,
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
