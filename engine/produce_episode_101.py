# engine/produce_episode_101.py
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

IMG_EP101 = os.path.join(THUMBS_DIR, "2026-10-10-05.webp")
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
    "id": "2026-10-10-05",
    "hour": "05:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Transcranial Focused Ultrasound Neuromodulation, Blood-Brain Sonoporation & Soviet Remote Neuro-Targeting",
    "subject": "Hourly uncensored breakdown: Rex Vance explores low-intensity transcranial focused ultrasound (tFUS) achieving millimetric deep-brain neuromodulation and reversible blood-brain barrier sonoporation, and Yuri Shvets on Soviet remote neurological intervention programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero five hundred hours. For decades, modulating neural circuits deep within the living human brain required surgical electrode implantation or imprecise electromagnetic coils that diffused energy across broad cortical swathes. Today, low-intensity transcranial focused ultrasound, or tFUS, has shattered that limitation entirely, focusing millimeter-precision acoustic pressure wave vectors through the intact human skull into deep subcortical structures like the thalamus, amygdala, and hippocampus without requiring a single surgical incision.",
        "Operating at low megahertz frequencies, focused acoustic radiation exerts mechanical shear stress on mechanosensitive ion channels in neuronal membranes, altering membrane capacitance and triggering action potentials on demand. Unlike electromagnetic stimulation, which disperses rapidly through intervening tissue, acoustic pressure waves focus deep into three-dimensional neural circuits with sub-millimeter spatial resolution. At slightly higher acoustic intensities combined with circulating microbubbles, focused ultrasound achieves transient, reversible sonoporation of the blood-brain barrier, temporarily opening tight endothelial junctions to deliver targeted pharmacological compounds directly into specific neural nuclei before the barrier reseals within hours.",
        "This capability to non-invasively manipulate deep brain structures mirrors a heavily classified pursuit within Cold War intelligence services. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet scientific institutes under the First Chief Directorate and military research sections in Novosibirsk investigated acoustic resonance, radio-frequency modulation, and remote physiological disruption throughout the late Soviet era.",
        "According to Shvets, Soviet intelligence ran extensive experimental programs investigating whether directed acoustic and electromagnetic fields could induce disorientation, sleep disruption, or cognitive degradation in foreign embassy personnel and military command staff. Shvets revealed that KGB technical specialists actively studied the acoustic impedance of the human skull, seeking frequencies capable of penetrating cranial bone without causing immediate thermal lesions, aiming to induce subtle behavioral suppression and psychological instability in target individuals.",
        "In the modern defense domain, that research has achieved frightening clinical maturity. Military and intelligence interest in transcranial ultrasound has shifted from coarse disruption to covert cognitive control and accelerated soldier performance. With phased acoustic transducer arrays capable of dynamically steering focal points across the brain in milliseconds, the boundary between therapeutic neuro-modulation and remote behavioral manipulation is dissolving under the cover of medical research contracts.",
        "Audit the military neuro-technology grants, demand strict ethical safeguards on non-invasive brain intervention devices, and remember that when sound waves can alter human thought at the cellular level, the mind is no longer private property. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="focused_ultrasound", title=EPISODE_DATA["title"])
    img.save(IMG_EP101, "WEBP", quality=92)
    print(f"Saved: {IMG_EP101}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP101, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP101, IMG_REX, IMG_STUDIO, IMG_EP101, IMG_REX, IMG_EP101]
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
    brain_cover = r"assets\cover_ep101_procedural.webp"
    with Image.open(IMG_EP101) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
