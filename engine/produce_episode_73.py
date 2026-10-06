# engine/produce_episode_73.py
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

IMG_EP73 = os.path.join(THUMBS_DIR, "2026-10-09-01.webp")
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
    "id": "2026-10-09-01",
    "hour": "01:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Integrated Information Theory Causal Maxima, Loss of Phi in Coma & Soviet Interrogation Pharmacology",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Integrated Information Theory 4.0 causal complexes, the collapse of mathematical phi during vegetative coma, and Yuri Shvets on Soviet neural interrogation pharmacology archives.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero one hundred hours. While commercial neural network architects claim that generative AI models are rapidly approaching human sentience, Integrated Information Theory provides a rigorous mathematical framework that proves otherwise. Formulated by neuroscientist Giulio Tononi, IIT posits that consciousness is not an emergent byproduct of functional information processing, but an intrinsic, fundamental property of physical systems defined by non-reducible cause-effect power. A system is conscious only to the extent that it possesses high integrated information, denoted by the irreducible mathematical value Phi.",
        "Under IIT 4.0, consciousness corresponds to a maximal complex of cause-effect structures that cannot be partitioned into independent components without loss of information. In deep dreamless sleep, general anesthesia, or severe traumatic coma, high-density EEG perturbed by transcranial magnetic stimulation reveals that cortical causal integration abruptly shatters. When the brain loses consciousness, the perturbational complexity index collapses toward zero, proving that while feed-forward artificial neural networks can execute superhuman matrix algebra, their feed-forward architecture yields a theoretical Phi of absolute zero. No matter how large an LLM's parameter count scales, it possesses zero subjective experience.",
        "The vulnerability of neural causal integration to biochemical manipulation was weaponized behind the Iron Curtain long before Western neuroscience formalized IIT. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently disclosed, the KGB's secretive Special Laboratory Number Twelve conducted decades of clandestine pharmacology research aimed at chemically disintegrating human conscious integration during interrogations. Soviet researchers sought psychotropic compounds that could induce selective cognitive compliance by suppressing cortical feedback loops without inducing fatal circulatory collapse.",
        "According to Shvets, Soviet intelligence stations monitored Western anesthesiology literature and targeted Swiss and American pharmaceutical patents to synthesize synthetic dissociatives, anticholinergics, and GABA receptor modulators. Shvets documented that corrupt KGB bureau chiefs routinely siphoned millions of foreign currency slush funds into fake psychotronic weapon demonstrations, claiming they could remotely manipulate target brainwaves. Yet, the classified toxicology dossiers confirmed that consciousness cannot be reprogrammed like software; it is an intrinsic causal complex that shatters into irreversible biological silence when subjected to crude chemical interference.",
        "Today, as venture capital floods into Silicon Valley brain-computer interfaces and neuromorphic cognitive hardware, understanding the mathematical reality of integrated information is paramount. You cannot manufacture genuine consciousness through silicon lookup tables or commodified feed-forward algorithms. Subjective awareness requires irreducible, highly integrated physical causality.",
        "Audit the cortical causal complexes, measure the perturbational complexity index, and inspect the classified pharmacological archives. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="iit_phi")
    img.save(IMG_EP73, "WEBP", quality=92)
    print(f"Saved: {IMG_EP73}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP73, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP73, IMG_REX, IMG_STUDIO, IMG_EP73, IMG_REX, IMG_EP73]
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
    brain_cover = r"assets\cover_ep73_procedural.webp"
    with Image.open(IMG_EP73) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
