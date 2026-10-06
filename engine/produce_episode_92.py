# engine/produce_episode_92.py
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

IMG_EP92 = os.path.join(THUMBS_DIR, "2026-10-09-20.webp")
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
    "id": "2026-10-09-20",
    "hour": "20:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "quantum",
    "title": "Bose-Einstein Condensate Atom Interferometry, Subterranean Bunker Gravimetry & Soviet Non-Acoustic ASW",
    "subject": "Hourly uncensored breakdown: Rex Vance explores cold-atom Bose-Einstein condensate matter-wave gravimetry revealing deeply buried command bunkers, and Yuri Shvets on Soviet non-acoustic naval submarine tracking secrets.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty hundred hours. While defense intelligence has historically relied on synthetic aperture radar and seismic sensor nets to monitor adversary underground installations, an unshieldable quantum surveillance frontier is overturning subterranean warfare. Bose-Einstein condensate atom interferometry exploits macroscopic matter-wave coherence to measure gravitational acceleration gradients with sensitivities exceeding ten to the minus nine meters per second squared. Because gravity cannot be attenuated, blocked, or jammed by any known material, buried reinforced command bunkers and deep underground nuclear enrichment facilities are stripped of their physical concealment.",
        "Inside a cold-atom quantum gravimeter, clouds of Rubidium-eighty-seven or Strontium atoms are cooled by optical molasses to tens of picokelvin above absolute zero. Retro-reflected laser pulses act as quantum beamsplitters and mirrors, splitting the atomic wavepackets along divergent vertical trajectories before recombining them to produce matter-wave interference fringes. Any localized mass deficit—such as a hollow underground tunnel complex, a reinforced missile silo, or a submarine hull displacing thousands of tons of seawater—induces a distinct gravitational phase shift measurable from airborne or orbital survey platforms.",
        "This pursuit of non-acoustic gravitational and density anomaly detection is not merely an academic physics milestone; it represents the realization of a classified Soviet naval obsession. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet naval design bureaus and the KGB First Chief Directorate dedicated astronomical black budgets throughout the nineteen-eighties toward developing non-acoustic anti-submarine warfare sensors under codenames such as Project Sokol.",
        "According to Shvets, as American Ohio-class ballistic missile submarines achieved acoustic quietness that rendered passive hydrophone arrays ineffective, Soviet leadership grew desperate for non-acoustic tracking breakthroughs. Soviet research institutes explored laser airborne wake detection, internal wave thermal scarring, and sensitive torsional gravity gradient meters. Shvets revealed that Soviet military intelligence attempted to deploy airborne gravimeters along transatlantic transit routes to detect the minute mass displacement and hydro-magnetic signatures of submerged NATO ballistic missile submarines running silent beneath the thermocline.",
        "Today, the transition from crude mechanical Soviet torsion balances to cold-atom matter-wave interferometers makes subterranean and maritime concealment nearly impossible. Military powers can bury command centers beneath hundreds of meters of solid granite, yet airborne quantum gravimetric gradiometers can reconstruct the exact three-dimensional architecture of the hollowed-out chambers simply by measuring local gravity anomalies. In the emerging quantum battlespace, there are no unmapped voids; the mass density of the Earth itself becomes transparent.",
        "Track the defense advanced quantum sensor procurements, audit the airborne gravimetric mapping flights, and understand that in quantum mechanics, true opacity does not exist. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="bec", title=EPISODE_DATA["title"])
    img.save(IMG_EP92, "WEBP", quality=92)
    print(f"Saved: {IMG_EP92}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP92, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP92, IMG_REX, IMG_STUDIO, IMG_EP92, IMG_REX, IMG_EP92]
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
    brain_cover = r"assets\cover_ep92_procedural.webp"
    with Image.open(IMG_EP92) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
