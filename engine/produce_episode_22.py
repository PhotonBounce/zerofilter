# engine/produce_episode_22.py
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

IMG_EP22 = os.path.join(THUMBS_DIR, "2026-10-06-22.webp")
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
    "id": "2026-10-06-22",
    "hour": "22:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Donald Hoffman Conscious Agent Networks, Spacetime Emergence & KGB Reflexive Control",
    "subject": "Hourly uncensored breakdown: Rex Vance maps Donald Hoffman's mathematical conscious agent networks to ex-KGB Major Yuri Shvets's revelations on reflexive control warfare—demonstrating how cognitive deception operations exploit perceptual interfaces rather than objective reality.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It's twenty-two hundred hours. Cognitive science and military psychological operations converge at a singular mathematical juncture: spacetime is not fundamental reality, but an evolutionary desktop interface. Cognitive psychologist Donald Hoffman's Fitness-Beats-Truth theorem proved via evolutionary game theory that sensory perception evolves to guide adaptive action, not to render objective truth. When you perceive an apple or a ballistic missile, you aren't rendering reality—you're looking at a three-dimensional icon designed to keep you alive.",
        "In the operational archives of the Soviet First Chief Directorate, this mathematical insight was weaponized under the doctrine of reflexive control, pioneered by Vladimir Lefebvre at the Institute of Psychology. As Washington counter-intelligence analyst and former KGB Major Yuri Shvets has meticulously detailed, reflexive control is not simple disinformation; it is the deliberate transmission of curated perceptual icons designed to alter a target's internal decision matrix until the target independently arrives at a catastrophic conclusion pre-selected by the operator.",
        "Hoffman's formal model replaces physical spacetime with a network of discrete conscious agents interacting via Markovian kernels. Each agent is a mathematical sextuple representing experiences, actions, and decision probabilities. Spacetime and subatomic particles emerge mathematically as an asymptotic projection of this deeper network—analogous to how two-dimensional pixels on your screen emerge from silicon voltage gates. If physical spacetime is merely a projected data interface, then the geopolitical battlespace is fundamentally informational, not kinetic.",
        "This explains why modern hybrid warfare bypasses defensive missile perimeters to target cognitive architectures directly. From Kremlin troll factories running micro-targeted psychological operations on Western voting demographics to Beijing's united front influence pipelines infiltrating Silicon Valley venture firms, adversaries exploit the known vulnerabilities of our perceptual interface. They flood the cognitive channel with synthetic sensory stimuli, hijacking the heuristic shortcuts our brains evolved across millions of years.",
        "Shielding democratic societies from reflexive cognitive capture requires treating information environments as contested cyber-quantum ecosystems. We must deploy cryptographic provenance chains, decentralized verification nodes, and formal game-theoretic audits to detect synthetic behavioral loops before they manifest as political paralysis or institutional collapse. Hoffman's mathematics provides the diagnostic lens: recognize the desktop interface for what it is, and you can instantly identify when an adversary is tampering with your operating system icons.",
        "Objective reality doesn't live in the corporate news feed, and it certainly doesn't live on cable broadcast panels. Trust the mathematics, trace the intelligence cables, and never mistake the icon on your screen for the underlying reality. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="conscious_agents")
    img.save(IMG_EP22, "WEBP", quality=92)
    print(f"Saved: {IMG_EP22}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP22, output_mp4, duration=10)
    
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
        IMG_EP22,
        IMG_REX,
        IMG_EP22,
        IMG_STUDIO,
        IMG_EP22,
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
