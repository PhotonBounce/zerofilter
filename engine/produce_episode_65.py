# engine/produce_episode_65.py
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

IMG_EP65 = os.path.join(THUMBS_DIR, "2026-10-08-17.webp")
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
    "id": "2026-10-08-17",
    "hour": "17:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Karl Friston Active Inference in Generative AI Agents, Predictive Coding & KGB Cognitive Warfare",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Karl Friston's Free Energy Principle applied to autonomous generative AI agents, predictive coding sensory error minimization, and Yuri Shvets's insider analysis of Soviet reflexive control doctrine and cognitive warfare architectures.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is seventeen hundred hours. The contemporary generative AI boom has hit a fundamental structural ceiling: large language models remain passive statistical next-token predictors, brittle to hallucinatory error and incapable of genuine self-directed autonomous agency. To build truly sovereign synthetic intelligence, frontier defense research laboratories and theoretical neuroscientists are abandoning brute-force autoregressive transformers in favor of neurobiologist Karl Friston’s Free Energy Principle and active inference. Under this revolutionary paradigm, all intelligent biological and artificial cognitive systems exist for a single fundamental purpose: to minimize informational surprise and thermodynamic entropy.",
        "The mathematical mechanics of active inference operate across a rigorous statistical boundary known as a Markov blanket, cleanly separating an internal generative model from external environmental states. Rather than passively absorbing training data, an active inference agent constantly generates top-down predictions of sensory inputs, calculating precision-weighted prediction errors across hierarchical neural layers. To minimize variational free energy, the agent possesses two distinct operational pathways: it can update its internal cognitive representations to fit incoming sensory data, or it can perform physical actions in the world to force reality to conform to its prior expectations.",
        "This mathematical model of sensory perception and behavioral manipulation has a profound, chilling lineage in Soviet intelligence operations. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet military theorists pioneered the science of reflexive control—the systematic manipulation of an adversary’s perceptual inputs to compel them to make voluntary decisions favorable to Moscow. The KGB recognized that you do not need to alter an opponent's physical hardware if you can systematically bias their predictive priors.",
        "According to Shvets, Soviet intelligence institutes and military cybernetic bureaus meticulously analyzed Western democratic decision-making through this exact predictive lens. By injecting calibrated disinformation, synthetic scandals, and reflexive feedback loops into Western media channels, Soviet operatives forced foreign leadership into predictable, self-destructive policy loops. Shvets emphasizes that modern generative AI algorithms, autonomous cognitive swarms, and social media recommendation algorithms are weaponized active inference architectures designed to shatter societal consensus and paralyze institutional resolve.",
        "Today, the weaponization of cognitive perception represents the definitive modern battlefield. As global superpowers deploy autonomous AI agents capable of continuous active inference, geopolitical conflict is no longer waged over physical borders, but over the Markov blankets of human consciousness. Whoever controls the prior expectations governing societal perception dictates objective reality itself.",
        "Audit the Markov blankets, calculate the prediction errors, and verify the cognitive priors. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="active_inference")
    img.save(IMG_EP65, "WEBP", quality=92)
    print(f"Saved: {IMG_EP65}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP65, output_mp4, duration=10)
    
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
        IMG_EP65,
        IMG_REX,
        IMG_EP65,
        IMG_STUDIO,
        IMG_EP65,
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
