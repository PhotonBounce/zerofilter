# engine/produce_episode_84.py
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

IMG_EP84 = os.path.join(THUMBS_DIR, "2026-10-09-12.webp")
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
    "id": "2026-10-09-12",
    "hour": "12:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "quantum",
    "title": "Macroscopic Drum Resonator Entanglement, Optomechanical Phase Noise & Soviet Laser Espionage",
    "subject": "Hourly uncensored breakdown: Rex Vance examines macroscopic quantum entanglement in aluminum drum resonators, laser optomechanical phase noise suppression, and Yuri Shvets on Soviet Line X laser interferometry espionage.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twelve hundred hours. For nearly a century, textbook physicists insisted that quantum weirdness was strictly confined to the microscopic domain—safely isolated inside individual atoms, photons, and superconducting qubits. But inside advanced quantum optomechanics laboratories, that comfortable classical boundary has officially ruptured. Experimental physicists have successfully established macroscopic quantum entanglement between two distinct micro-mechanical aluminum drum resonators, each containing trillions of atoms and physically visible under an ordinary laboratory microscope.",
        "These mechanical drums, vibrating at radio frequencies around ten megahertz, are embedded inside a high-finesse optical Fabry-Perot cavity. By continuously illuminating the system with red-detuned laser pulses, radiation pressure dynamically extracts thermal phonons, cooling the macroscopic vibrating membranes directly into their quantum ground state. Through continuous two-mode squeezed light interactions, the spatial displacement of one drum instantaneously dictates the momentum of the other, defying classical phase space limits and suppressing optical phase noise significantly below the standard quantum limit.",
        "While civilian academia frames macroscopic optomechanics as a triumph of foundational physics, the national security establishment has always recognized its primary strategic value: unjammable subterranean gravimetry and ultra-sensitive laser interferometry. And this exact scientific frontier was a premier operational target of Soviet clandestine espionage. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively detailed, the First Chief Directorate's Directorate T and Line X scientific collectors prioritized Western laser interferometry and optoelectronic sensors above nearly all other technical requirements.",
        "According to Shvets, the Soviet Academy of Sciences and Lebedev Physical Institute were desperate to acquire American high-vacuum optical cavity designs and ultra-low-noise laser stabilization patents. Soviet naval planners urgently needed sub-femtometer acoustic sensors to detect silent Western nuclear submarines patrolling the GIUK Gap and Barents Sea bastions. Shvets revealed that KGB tech-diversion networks routinely funneled Western optical components through dummy trading fronts in Vienna and Zurich, attempting to reverse-engineer Western cavity optomechanics for deep-ocean hydrophone arrays.",
        "Today, macroscopic quantum entanglement in mechanical resonators is rapidly transitioning from a laboratory milestone to a decisive defense capability. Quantum optomechanical accelerometers and quantum-enhanced gyroscopes operate entirely independent of vulnerable GPS constellations, completely immune to theater-wide electronic warfare spoofing. When macroscopic matter enters non-local quantum superposition, both inertial navigation and strategic surveillance cross into an era where classical physical barriers can no longer conceal subterranean bunkers or silent undersea movements.",
        "Audit the optomechanical laser cavity defense patents, track the quantum sensor procurement ledgers, and never accept the comfortable illusion of classical boundaries. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="optomechanics")
    img.save(IMG_EP84, "WEBP", quality=92)
    print(f"Saved: {IMG_EP84}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP84, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP84, IMG_REX, IMG_STUDIO, IMG_EP84, IMG_REX, IMG_EP84]
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
    brain_cover = r"assets\cover_ep84_procedural.webp"
    with Image.open(IMG_EP84) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
