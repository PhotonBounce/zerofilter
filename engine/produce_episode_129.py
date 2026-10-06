# engine/produce_episode_129.py
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

IMG_EP129 = os.path.join(THUMBS_DIR, "2026-10-11-09.webp")
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
    "id": "2026-10-11-09",
    "hour": "09:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Anil Seth Controlled Hallucinations, Bayesian Priors & KGB Reflexive Perception Warfare",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates cognitive neuroscientist Anil Seth's predictive processing framework, the brain as a Bayesian prediction engine generating controlled hallucinations, and Yuri Shvets on KGB Service A reflexive control doctrine, active measures, and state-sponsored perceptual manipulation.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero nine hundred hours. The intuitive assumption that our eyes and ears function like transparent video cameras feeding objective reality directly into our conscious minds is a profound evolutionary illusion. According to cognitive neuroscientist Anil Seth and modern predictive processing theory, perception is not a passive readout of the external world. It is an actively generated, internally simulated fantasy: a controlled hallucination constructed by hierarchical Bayesian prediction engines inside the cerebral cortex.",
        "In the Bayesian brain framework, neural processing runs backwards. The brain does not wait for sensory data to construct perception; instead, higher cortical areas continuously project top-down generative predictions about what is causing incoming sensory inputs. The primary role of our sensory organs is merely to transmit bottom-up prediction errors—the mathematical difference between what the brain predicted and what the receptors registered. When predictions successfully minimize prediction error, the internal hallucination is stabilized and experienced as objective physical reality.",
        "Crucially, the brain balances predictions against incoming data using precision weighting. By dynamically adjusting the gain on prediction error channels, neuromodulators like dopamine and acetylcholine determine whether the brain updates its internal beliefs or stubbornly suppresses contrary sensory evidence. If top-down priors are granted overwhelming precision weight, the brain literally sees what it expects to see, hallucinating certainty while filtering out contradictory external facts.",
        "This computational vulnerability in human consciousness is precisely what psychological warfare and counter-intelligence doctrines have exploited for decades. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, Soviet strategic deception was never about convincing targets of overt lies—it was about systematically manipulating their baseline perceptual priors.",
        "According to Shvets, the KGB First Chief Directorate's Service A—specializing in Active Measures and reflexive control—engineered disinformative operational environments designed to hack adversary decision-makers. Shvets revealed that Soviet specialists studied reflexive control theory developed by Vladimir Lefebvre to inject carefully tailored data streams that reinforced the target's pre-existing cognitive biases. By systematically feeding the adversary's predictive priors, the KGB ensured that the victim's own brain filtered out anomalies and willingly generated the exact false reality desired by Moscow, believing they were acting on independent deductive analysis.",
        "From Anil Seth's Bayesian predictive coding to modern algorithmic information warfare, the battleground of geopolitical power is fought inside the perceptual apparatus itself. When an adversary controls your priors, your own brain manufactures their reality. Question your mental models, audit the prediction errors you suppress, and never mistake a controlled hallucination for objective truth. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="anil_seth_hallucination", title=EPISODE_DATA["title"])
    img.save(IMG_EP129, "WEBP", quality=92)
    print(f"Saved: {IMG_EP129}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP129, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP129,
        IMG_STUDIO,
        IMG_EP129,
        IMG_REX,
        IMG_EP129,
        IMG_STUDIO
    ]
    create_art_frames(EPISODE_DATA["id"], src_frames)
    
    # 4. Neural Voice Audio Synthesis
    print("[4/5] Synthesizing neural voice (Rex Vance via edge-tts)...")
    full_script = " ... \n\n ".join(EPISODE_DATA["paragraphs"])
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, mp3_path)
    actual_seconds = get_audio_duration(mp3_path)
    print(f"Synthesized Rex Vance audio: {mp3_path} ({actual_seconds}s)")
    
    # 5. Manifest & Metadata Registration
    print("[5/5] Registering in episodes.json...")
    t_step = actual_seconds / 6.0
    frame_times = [int(round(i * t_step)) for i in range(6)]
    
    full_episode_entry = {
        "id": EPISODE_DATA["id"],
        "hour": EPISODE_DATA["hour"],
        "date": EPISODE_DATA["date"],
        "kind": EPISODE_DATA["kind"],
        "category": EPISODE_DATA["category"],
        "title": EPISODE_DATA["title"],
        "subject": EPISODE_DATA["subject"],
        "paragraphs": EPISODE_DATA["paragraphs"],
        "art": {
            "frames": [
                {"t": frame_times[i], "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
                for i in range(6)
            ]
        },
        "seconds": actual_seconds,
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
        
    manifest["episodes"].insert(0, full_episode_entry)
    manifest["updated"] = "2026-10-06T14:40:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
