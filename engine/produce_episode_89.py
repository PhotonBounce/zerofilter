# engine/produce_episode_89.py
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

IMG_EP89 = os.path.join(THUMBS_DIR, "2026-10-09-17.webp")
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
    "id": "2026-10-09-17",
    "hour": "17:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Integrated Information Theory, Coma Perturbational Complexity & Soviet Psychotropic Trials",
    "subject": "Hourly uncensored breakdown: Rex Vance explores Giulio Tononi's Integrated Information Theory (IIT 4.0), causal maxima and Perturbational Complexity Index in coma patients, and Yuri Shvets on Soviet psychotropic interrogation files.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is seventeen hundred hours. For centuries, philosophers and neurologists debated whether consciousness was merely an elusive epiphenomenon of complex computation, or an irreducible property of physical systems with specific causal architecture. In contemporary theoretical neuroscience, neuroscientist Giulio Tononi's Integrated Information Theory, or IIT four point zero, provides the mathematical resolution. Consciousness is neither an abstract algorithm nor behavior; it is identical to the maximal integrated cause-effect power intrinsic to a physical system, quantified as Phi.",
        "To transition from mathematical formalism to clinical diagnosis, researchers developed the Perturbational Complexity Index, or PCI. By administering transcranial magnetic stimulation pulses to the cerebral cortex and recording the spatiotemporal reverberations through high-density EEG, clinicians can directly measure the compressibility of the brain's causal response. In healthy waking consciousness, the perturbation sparks a non-compressible, widely integrated cortical cascade. But in dreamless sleep, general anesthesia, or vegetative coma, the cortical response collapses into either localized silence or a stereotypic, disintegrated wave, driving Phi toward zero.",
        "This objective boundary between conscious agency and cognitive disintegration was precisely what intelligence agencies sought to exploit during the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively detailed, Soviet intelligence maintained classified psychopharmacological research programs aimed at chemically unraveling an operative's integrated cognitive architecture without leaving physical marks.",
        "According to Shvets, the KGB's First Chief Directorate and its clandestine operational-technical departments tested synthetic dissociatives, anticholinergics, and neuroleptics on human subjects. Soviet interrogators discovered that specific chemical cocktails could selectively sever reciprocal thalamocortical feedback loops. In the language of Integrated Information Theory, these agents systematically fractured the brain's maximal causal complex, destroying a prisoner's capacity to synthesize past memories with present intent, effectively abolishing willpower and psychological resistance while preserving mechanical speech.",
        "Tononi's integrated information framework delivers a chilling warning for modern counter-intelligence and cognitive warfare. Consciousness is not an unassailable spiritual bastion; it is a delicate physical cause-effect complex that can be quantified, monitored by external telemetry, and systematically dismantled. When state actors possess both the causal mathematical models and the pharmacological tools to fragment human Phi, individual psychological sovereignty becomes a contested electronic and chemical battlespace.",
        "Audit the clinical perturbational complexity research, trace the classified psychotropic interrogation archives, and defend your causal integrity against external manipulation. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="iit_phi")
    img.save(IMG_EP89, "WEBP", quality=92)
    print(f"Saved: {IMG_EP89}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP89, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP89, IMG_REX, IMG_STUDIO, IMG_EP89, IMG_REX, IMG_EP89]
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
    brain_cover = r"assets\cover_ep89_procedural.webp"
    with Image.open(IMG_EP89) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
