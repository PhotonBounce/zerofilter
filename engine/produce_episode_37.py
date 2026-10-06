# engine/produce_episode_37.py
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

IMG_EP37 = os.path.join(THUMBS_DIR, "2026-10-07-13.webp")
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
    "id": "2026-10-07-13",
    "hour": "13:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Nonlinear Optics in Photonic Crystals, Microcavities & Soviet Laser Weapon Deception",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes photonic crystal bandgaps, slow-light microcavities, second-harmonic generation, and Yuri Shvets's insider revelations regarding Soviet Terra-3 laser weapon deception programs at Sary-Shagan.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is thirteen hundred hours. Controlling the propagation of light at the sub-micron scale has long represented the holy grail of modern optical physics. By etching periodic arrays of nanoscale dielectric structures into high-index silicon, physicists create photonic crystals—synthetic materials possessing a photonic bandgap that completely forbids specific optical frequencies from propagating through the lattice. When engineered with point defect microcavities, these crystals trap photons for millions of oscillations, compressing electromagnetic energy and slowing the group velocity of light to a crawl.",
        "At these ultra-slow velocities, nonlinear optical effects are amplified by multiple orders of magnitude. Phenomena like second-harmonic generation, Kerr-effect phase modulation, and four-wave mixing—ordinarily requiring massive high-intensity pulse lasers—can now be triggered on a microscopic chip at milliwatt power levels. This breakthrough is revolutionizing integrated photonics, enabling all-optical quantum switching, chip-scale frequency combs, and unbreakable on-chip cryptographic key distribution networks.",
        "Yet the weaponization of laser optics carries a long history of geopolitical deception and intelligence theater. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, the Soviet Union executed one of the most sophisticated disinformation campaigns in military history around its laser weapons programs. In the late 1970s and 1980s, Soviet intelligence actively fed exaggerated intelligence reports to Western defense attaches regarding the Terra-3 and Omega laser test complexes at Sary-Shagan in Kazakhstan.",
        "According to Shvets, the KGB's First Chief Directorate and Directorate T deliberately stoked American fears that Soviet scientists had achieved a functional ground-based anti-satellite laser weapon capable of blinding orbital surveillance. In reality, Soviet gas-dynamic and excimer lasers were plagued by atmospheric thermal blooming, catastrophic beam jitter, and insufficient electrical power grids. The Kremlin's primary objective was not immediate deployment, but baiting the United States into sinking hundreds of billions into counter-programs while concealing genuine technological bottlenecks.",
        "Today, as global superpowers race to field directed-energy weapons, laser anti-satellite counter-measures, and optical quantum networks, separating physical reality from strategic posturing remains paramount. While megawatt-class thermal lasers still grapple with atmospheric turbulence and weather attenuation, the real optical revolution is occurring in microscopic silicon photonics—where nonlinear microcavities process and encrypt telemetry faster than electronic interceptors can track.",
        "Audit the photonic bandgaps, separate physical capability from intelligence deception, and judge optical supremacy by mathematical proof rather than geopolitical theater. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="photonic_crystals")
    img.save(IMG_EP37, "WEBP", quality=92)
    print(f"Saved: {IMG_EP37}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP37, output_mp4, duration=10)
    
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
        IMG_EP37,
        IMG_REX,
        IMG_EP37,
        IMG_STUDIO,
        IMG_EP37,
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
