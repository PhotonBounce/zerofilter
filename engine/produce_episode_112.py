# engine/produce_episode_112.py
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

IMG_EP112 = os.path.join(THUMBS_DIR, "2026-10-10-16.webp")
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
    "id": "2026-10-10-16",
    "hour": "16:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "quantum",
    "title": "Macroscopic Optomechanical Entanglement, Phonon Ground States & Soviet Laser Acoustics",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates breakthroughs in macroscopic quantum optomechanics, laser cooling of micro-fabricated aluminum membranes to their quantum motional ground state, and Yuri Shvets on Soviet laser acoustic espionage programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is sixteen hundred hours. Quantum mechanics is universally recognized as the governing framework of atoms and subatomic particles, but where does the microscopic realm end and our classical macroscopic reality begin? In cryogenic quantum optics laboratories, that long-standing boundary is rapidly dissolving. Physicists have now demonstrated deterministic quantum entanglement between macroscopic mechanical drum resonators—micro-fabricated aluminum membranes comprising trillions of atoms, easily visible under a standard optical microscope, cooled by laser sideband radiation directly into their motional quantum ground state.",
        "To achieve optomechanical entanglement, researchers place micro-machined drum membranes inside a superconducting microwave Fabry-Perot cavity at millikelvin temperatures. By driving the cavity with red-detuned microwave photons, thermal phonon excitations are systematically extracted through radiation pressure dynamical backaction, chilling the mechanical motion to less than zero-point-two phonons. When two separated mechanical resonators are coupled via two-mode squeezed microwave light, their motional states become non-locally entangled, generating Einstein-Podolsky-Rosen correlations in position and momentum across macroscopic physical matter.",
        "This mastery over macroscopic acoustic vibrations and laser-mediated interferometry traces its historical origins to the intense acoustic and optical espionage programs of the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has revealed, Soviet intelligence prioritized non-acoustic detection and laser acoustic interception as central pillars of strategic surveillance.",
        "According to Shvets, the KGB First Chief Directorate's Technical Operations Directorate collaborated with the Lebedev Physical Institute to pioneer laser microphone eavesdropping—bouncing infrared beams off embassy window panes to detect sub-micron acoustic vibrations generated by human speech. In response to Western acoustic baffling, Soviet researchers sought increasingly sensitive interferometers to measure macroscopic mechanical displacement down to the quantum limit. Shvets disclosed that KGB Line X officers in the 1980s aggressively pursued Western cryogenic vibration-isolation technology and high-finesse optical coatings, seeking sensor advantages for deep-ocean submarine acoustic tracking.",
        "Decades later, macroscopic optomechanics has transitioned from covert eavesdropping laboratories to the cutting edge of national defense sensing and global quantum networking. Quantum-entangled mechanical membranes offer unprecedented sensitivity as ultra-precise gravimeters, stealth accelerometers for GPS-denied inertial navigation, and coherent quantum transducers capable of converting fragile superconducting qubit states into telecom-band optical photons. The superpower that first masters macroscopic quantum coherence will deploy unjammable navigation grids that guide strategic submarines across global oceans without ever relying on satellite beacons.",
        "Watch the boundary where microscopic quantum laws command macroscopic physical matter, verify sensor precision against thermal phase noise, and remember that when mechanical membranes entangle, even solid reality loses its classical certainty. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="optomechanics", title=EPISODE_DATA["title"])
    img.save(IMG_EP112, "WEBP", quality=92)
    print(f"Saved: {IMG_EP112}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP112, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP112,
        IMG_STUDIO,
        IMG_EP112,
        IMG_REX,
        IMG_EP112,
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
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Prepend new episode if not already present
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
    
    manifest["episodes"].insert(0, full_episode_entry)
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully published Episode {EPISODE_DATA['id']} to manifest ({len(manifest['episodes'])} episodes total).")

if __name__ == "__main__":
    asyncio.run(main())
