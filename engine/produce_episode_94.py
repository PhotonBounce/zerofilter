# engine/produce_episode_94.py
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

IMG_EP94 = os.path.join(THUMBS_DIR, "2026-10-09-22.webp")
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
    "id": "2026-10-09-22",
    "hour": "22:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Arctic Seabed Annexation, Lomonosov Ridge Mapping & Soviet Polar Bastion Acoustic Bathymetry",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the militarized battle for the Arctic seabed, unilateral continental shelf claims over the Lomonosov Ridge, and Yuri Shvets on Soviet polar nuclear submarine bastion acoustic bathymetry.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-two hundred hours. Beneath the permanent ice cap of the high Arctic, an aggressive geopolitical land-grab is unfolding largely out of sight of international public awareness. For more than two decades, the Kremlin has staged high-profile scientific expeditions to plant titanium flags on the seafloor at the North Pole, claiming that the underwater Lomonosov and Mendeleev Ridges are direct geological extensions of the Siberian continental shelf. Under the United Nations Convention on the Law of the Sea, this legal maneuvers seek exclusive sovereign rights over more than one point two million square kilometers of hydrocarbon-rich Arctic seabed.",
        "However, scientific resource extraction claims are merely a diplomatic smoke screen for intense seabed militarization. The Lomonosov Ridge spans eighteen hundred kilometers directly across the central Arctic basin, dividing the Amerasian and Eurasian sub-basins. By deploying specialized deep-submergence bathymetric mapping submersibles operated by the secretive Main Directorate of Undersea Research, or GUGI, Moscow is not merely gathering core samples; it is laying the acoustic foundation for an unassailable polar bastion strategy, installing autonomous nuclear-powered seabed listening posts and hydrophone transponders directly along underwater mountain ranges.",
        "This weaponization of polar oceanography is the direct modern continuation of Cold War naval doctrine. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively detailed, Soviet Northern Fleet SSBN survivability was predicated entirely on mastering the treacherous, uncharted acoustic environment beneath the Arctic pack ice.",
        "According to Shvets, the KGB First Chief Directorate and Soviet hydrographic institutes prioritized bathymetric mapping of polar underwater canyons above almost all conventional oceanographic research. Soviet Typhoon and Delta-class ballistic missile submarines utilized the ice canopy to baffle Western passive sonar, but navigating these sub-zero trenches without colliding with deep-draft ice keels required ultra-precise seafloor topographic telemetry. Shvets revealed that Soviet oceanographic research ships routinely falsified academic research clearances, using civilian academic oceanography covers to record acoustic reflection profiles that allowed Soviet missile submarines to launch nuclear retaliatory strikes directly from under the polar ice cap.",
        "Today, climate warming has opened previously inaccessible northern transit corridors, transforming the high Arctic from an impassable frozen desert into a premier military theater. As allied surface combatants and anti-submarine aircraft attempt to pierce the polar frontier, they face a heavily instrumented underwater fortress. The battle over the Lomonosov Ridge is not about scientific pride; it is an armed contest to secure absolute nuclear strike impunity beneath the polar ice.",
        "Audit the international continental shelf commission filings, track the deep-sea research submersible deployments, and never mistake Arctic science for civilian neutrality. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="lomonosov_ridge", title=EPISODE_DATA["title"])
    img.save(IMG_EP94, "WEBP", quality=92)
    print(f"Saved: {IMG_EP94}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP94, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP94, IMG_REX, IMG_STUDIO, IMG_EP94, IMG_REX, IMG_EP94]
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
    brain_cover = r"assets\cover_ep94_procedural.webp"
    with Image.open(IMG_EP94) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
