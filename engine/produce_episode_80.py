# engine/produce_episode_80.py
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

IMG_EP80 = os.path.join(THUMBS_DIR, "2026-10-09-08.webp")
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
    "id": "2026-10-09-08",
    "hour": "08:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "quantum",
    "title": "Diamond NV Center Quantum Gravimetry, Subterranean Bunker Mapping & Soviet Deep ASW Sensors",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates nitrogen-vacancy diamond quantum gravity gradiometry for mapping deep underground bunkers without GPS, and Yuri Shvets on Soviet non-acoustic submarine detection.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero eight hundred hours. Across modern military geophysics, the most elusive tactical domain remains the deep subterranean. Hardened underground command bunkers, ballistic missile launch silos, and covert centrifuge cascades are burrowed hundreds of meters beneath granite mountains, impervious to synthetic aperture radar and optical reconnaissance. However, applied quantum metrology is eliminating subterranean concealment through diamond nitrogen-vacancy center quantum gravimetry and gravity gradiometry. By measuring infinitesimal variations in the Earth's gravitational field caused by subsurface mass density deficits, quantum sensors render underground voids visible from airborne platforms.",
        "At the core of this quantum sensor is an atomic defect within a synthetic diamond crystal lattice: a nitrogen atom adjacent to a vacant carbon site. When optically pumped with a green laser, the electron spin state of the nitrogen-vacancy center exhibits exquisite sensitivity to external gravitational gradient shifts and magnetic anomalies. Operating at room temperature without requiring cryogenic cooling, diamond NV gravity gradiometers can detect the subtle gravitational anomaly created by a hollow subterranean concrete bunker or an undetected tunnel complex, functioning as an unjammable, passive subterranean scanner in GPS-denied combat environments.",
        "The strategic imperative to detect hidden mass anomalies without active emissions has deep historical roots in Cold War counter-intelligence. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently disclosed, the Soviet military-industrial complex poured vast classified budgets into non-acoustic detection and gravity gradiometry throughout the late Soviet era. Soviet planners sought non-acoustic sensors capable of tracking United States Ohio-class ballistic missile submarines by measuring their hydrodynamic wake displacement and minute gravitational anomalies across ocean choke points.",
        "According to Shvets, Soviet intelligence stations targeted Western solid-state physics laboratories to acquire advanced synthetic diamond deposition techniques and laser metrology components. Simultaneously, the Kremlin utilized these geological anomaly mapping concepts to fortify its own deep underground command bastions—such as the massive subterranean facilities carved into Mount Yamantau in the Urals. Shvets revealed that Soviet military intelligence weaponized geophysical data to ensure strategic command survival, establishing the precedent for today's quantum gravimetric battlefield.",
        "As military superpowers construct increasingly deep underground nuclear command bunkers, quantum diamond gravimeters are rendering geological concealment obsolete. Passive, unjammable, and operating at the atomic limit, quantum gravity sensors are stripping away the last physical hiding places on Earth. In the quantum era, there is no subterranean sanctuary.",
        "Audit the NV center spin resonance traces, verify the gravitational gradient anomalies, and inspect the classified subterranean blueprints. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="nv_gravimetry")
    img.save(IMG_EP80, "WEBP", quality=92)
    print(f"Saved: {IMG_EP80}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP80, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP80, IMG_REX, IMG_STUDIO, IMG_EP80, IMG_REX, IMG_EP80]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep80_procedural.webp"
    with Image.open(IMG_EP80) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
