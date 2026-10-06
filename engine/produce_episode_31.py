# engine/produce_episode_31.py
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

IMG_EP31 = os.path.join(THUMBS_DIR, "2026-10-07-07.webp")
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
    "id": "2026-10-07-07",
    "hour": "07:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Karl Friston's Free Energy Principle, Markov Blankets & KGB Reflexive Control",
    "subject": "Hourly uncensored breakdown: Rex Vance explores neurobiologist Karl Friston's Free Energy Principle and Markov blankets in active inference, connecting cybernetic predictive processing to Vladimir Lefebvre's reflexive control mathematics deployed by Soviet counter-intelligence.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero seven hundred hours. In the physics of self-organizing biological systems, how does any living organism resist the inexorable pull of thermodynamic entropy? Renowned neuroscientist Karl Friston provided the mathematical answer with the Free Energy Principle. Any adaptive system that maintains homeostatic integrity must minimize its variational free energy—an upper bound on surprise—by continuously updating an internal generative model of the world to match afferent sensory states.",
        "At the core of Friston's formulation lies the Markov blanket: a statistical boundary consisting of sensory states and active states that separates the organism's internal variables from external environmental reality. Information from the chaotic outside world cannot touch the internal neural architecture directly; it is filtered through sensory receptors, while the system's actions perturb the external environment to confirm its internal generative predictions. Living consciousness is not a passive receiver; it is an active inference engine relentlessly confirming its own existence.",
        "In the operational doctrine of Soviet intelligence, this biological architecture was independently discovered through cybernetic warfare. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has explained, Soviet mathematician Vladimir Lefebvre developed the formal algebra of reflexive control. Lefebvre proved that by understanding a target's internal decision algorithm, an intelligence agency does not need to force an adversary to act against their will; you merely feed carefully calibrated sensory inputs through their cognitive Markov blanket, causing their internal generative model to naturally deduce the exact erroneous conclusion you desire.",
        "Modern information warfare has transformed Friston's active inference into an asymmetric weapon. Algorithmic social media platforms, synthetic deepfake narratives, and synchronized disinformation feeds systematically hack the sensory states of human populations. By artificially inflating predictive error and exploiting cognitive biases, state and commercial actors manipulate the variational free energy landscape of entire nations, driving targeted demographics into polarization, paranoia, and reflexive paralysis.",
        "Defending human agency in this cognitive battlespace requires recognizing the sanctity of our mental Markov blankets. We must cultivate epistemic hygiene, rigorously verify informational supply chains, and audit the algorithmic recommendation engines that mediate our perception of reality. Sovereignty begins not at geographical borders, but at the statistical boundaries of human consciousness. If you do not actively calibrate your internal model against primary reality, an adversary's reflexive control algorithms will gladly calibrate it for you.",
        "Audit your cognitive Markov blankets, challenge your prior probability distributions, and never confuse manipulated sensory inputs with ground truth. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="free_energy")
    img.save(IMG_EP31, "WEBP", quality=92)
    print(f"Saved: {IMG_EP31}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP31, output_mp4, duration=10)
    
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
        IMG_EP31,
        IMG_REX,
        IMG_EP31,
        IMG_STUDIO,
        IMG_EP31,
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
