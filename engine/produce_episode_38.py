# engine/produce_episode_38.py
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

IMG_EP38 = os.path.join(THUMBS_DIR, "2026-10-07-14.webp")
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
    "id": "2026-10-07-14",
    "hour": "14:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Arctic Undersea Mineral Rights, Svalbard Cable Sabotage & Northern Fleet Kinematics",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes High North polar transit routes, Svalbard undersea fiber-optic cable sabotage risks, Russian GUGI deep-sea reconnaissance vessels, and Yuri Shvets's insider revelations regarding Soviet Northern Fleet bastion defense doctrine.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is fourteen hundred hours. As polar ice packs recede across the High North, the Arctic Ocean is rapidly transforming from a frozen peripheral barrier into humanity's most contested maritime battleground. Beneath the frigid waters of the Barents and Norwegian Seas lie trillions of dollars in untapped critical mineral deposits, rare earths, and massive hydrocarbon reserves. But the true immediate flashpoint is not mining concessions—it is the fragile constellation of subsea fiber-optic cables connecting Arctic satellite ground stations to the global internet backbone.",
        "Nowhere is this vulnerability more acute than the Svalbard undersea dual-fiber archipelago link. Running hundreds of kilometers across the abyssal seafloor, this conduit transmits raw telemetry from the SvalSat ground station—a critical polar downlink tracking civilian weather constellations, European Space Agency missions, and classified Western military reconnaissance satellites. A severed cable here does not merely cause an isolated communications outage; it creates an immediate strategic blind spot in orbital early-warning and missile-defense networks.",
        "This seabed vulnerability is being actively probed by Russia's Main Directorate of Deep-Sea Research, known by its Russian acronym GUGI. Operating covertly under civilian cover, GUGI deploys specialized nuclear auxiliary submersibles and oceanographic reconnaissance ships like the Yantar, equipped with autonomous deep-diving robotic arms capable of tapping or severing fiber lines at depths exceeding three thousand meters. These operations are integrated directly into the operational kinematics of Russia's Northern Fleet, based along the Kola Peninsula.",
        "As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, Kremlin strategic doctrine treats the High North as an impregnable submarine bastion. During the Cold War, the Soviet Northern Fleet designed complex layered anti-access zones across the Barents Sea to protect ballistic missile submarines from NATO attack. Shvets points out that today's Russian General Staff applies identical bastion logic to hybrid warfare: threatening critical subsea infrastructure to hold European economies hostage while daring NATO to escalate under the threshold of Article Five.",
        "Countering this asymmetric threat requires persistent undersea situational awareness and autonomous seabed patrols. NATO and Nordic allies must deploy distributed acoustic hydrophone grids, uncrewed underwater autonomous drones, and permanent surface escort task forces to monitor Russian auxiliary vessels throughout the GIUK Gap and Arctic transit corridors. Freedom of navigation and data integrity beneath the waves are just as vital to democratic sovereignty as defending airspace.",
        "Audit the abyssal bathymetry, expose the covert seabed warfare, and never permit authoritarian aggression to operate in the darkness of the deep ocean. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="arctic_seabed")
    img.save(IMG_EP38, "WEBP", quality=92)
    print(f"Saved: {IMG_EP38}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP38, output_mp4, duration=10)
    
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
        IMG_EP38,
        IMG_REX,
        IMG_EP38,
        IMG_STUDIO,
        IMG_EP38,
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
