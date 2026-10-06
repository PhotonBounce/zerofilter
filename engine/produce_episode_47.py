# engine/produce_episode_47.py
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

IMG_EP47 = os.path.join(THUMBS_DIR, "2026-10-07-23.webp")
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
    "id": "2026-10-07-23",
    "hour": "23:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Active Inference in Generative Neural Architectures, Predictive Coding & Soviet Neuro-Cybernetics",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Karl Friston's active inference framework in deep hierarchical neural networks, variational free energy minimization, and Yuri Shvets's insider analysis of Soviet Pavlovian neuro-cybernetics and cognitive perception manipulation.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-three hundred hours. Modern computational neuroscience and frontier artificial intelligence are converging on a single governing imperative: active inference. Derived from the principle of least action, Karl Friston's free energy principle posits that all self-organizing conscious systems exist to minimize variational free energy—an information-theoretic upper bound on surprise. Rather than passively waiting for sensory inputs, deep hierarchical neural networks continually generate top-down generative predictions about the world, transmitting only the residual prediction error signals back up the cortical processing ladder.",
        "Through active inference, perception and action become two sides of the identical optimization equation. To minimize prediction errors, a neural system can either update its internal Bayesian beliefs to match reality, or execute physical motor actions that force the external environment to conform to its prior expectations. Separating these internal states from external chaos is the Markov blanket—a statistical boundary of sensory and active states that defines biological autonomy. Without this predictive blanket, neural architectures dissolve into thermodynamic entropy and informational noise.",
        "This computational model of human cognition has direct intelligence ancestry. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet science pioneered the weaponization of human sensory conditioning decades before modern generative AI. Drawing directly upon Ivan Pavlov's higher nervous activity doctrine and Pyotr Anokhin's functional system theory, Soviet military cyberneticians modeled the human nervous system as a feedback loop governed by expectation, anticipatory conditioning, and reflex.",
        "According to Shvets, the KGB's operational psychology units applied these neuro-cybernetic models to manipulate political decision-makers. By injecting carefully calibrated anomalies into an adversary's information streams, Soviet deception specialists exploited the brain's predictive coding mechanisms, inducing cognitive dissonance and paralyzing the target's predictive models. Shvets reveals that Soviet intelligence viewed reality not as an objective shared truth, but as a constructible perceptual consensus governed by sensory feedback manipulation.",
        "Today, this neuro-cybernetic doctrine is executed globally through algorithmic feeds and generative synthetic media. Modern recommendation engines and deep learning models act as hyper-optimized active inference systems, systematically shaping human prior probabilities, altering reward expectations, and herding millions of minds into automated affective feedback loops. The battle for geopolitical control is no longer fought over physical territory; it is fought over the predictive priors encoded inside the human prefrontal cortex.",
        "Audit your Bayesian priors, calibrate your Markov blankets, and maintain cognitive autonomy against algorithmic manipulation. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="active_inference")
    img.save(IMG_EP47, "WEBP", quality=92)
    print(f"Saved: {IMG_EP47}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP47, output_mp4, duration=10)
    
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
        IMG_EP47,
        IMG_REX,
        IMG_EP47,
        IMG_STUDIO,
        IMG_EP47,
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
