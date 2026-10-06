# engine/produce_episode_106.py
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

IMG_EP106 = os.path.join(THUMBS_DIR, "2026-10-10-10.webp")
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
    "id": "2026-10-10-10",
    "hour": "10:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Barents Sea Polar Fiber Sabotage, Spitsbergen Surveillance & Soviet Northern Fleet Cable Warfare",
    "subject": "Hourly uncensored breakdown: Rex Vance examines deep-seabed hybrid warfare targeting dual-use polar fiber-optic cables and acoustic hydrophone arrays across the Barents Sea and Svalbard archipelago, and Yuri Shvets on Soviet Northern Fleet undersea cable interdiction.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is ten hundred hours. In the frozen expanse of the high Arctic, geopolitical warfare is sinking beneath the polar ice caps. The Svalbard archipelago and the Barents Sea floor host some of the most sensitive critical infrastructure on Earth, including dual-use polar fiber-optic telecommunications cables and acoustic oceanographic sensor grids. Connecting polar satellite downlinks to European defense command hubs, these abyssal data conduits have become prime targets for Russian deep-sea reconnaissance and seabed sabotage operations.",
        "Operating under Russia's Main Directorate of Deep-Sea Research, or GUGI, specialized oceanographic research ships like the Yantar deploy unmanned autonomous submersibles and titanium-hulled deep-diving submarines to loiter directly above subsea fiber lines. At depths exceeding three thousand meters, these submersibles cut dual-redundant power and data fibers or attach non-invasive inductive taps. Forensic investigations following suspicious severed cable incidents between Longyearbyen and mainland Norway revealed clear mechanical trauma consistent with specialized seabed dredging and heavy subsea manipulator arms.",
        "This modern Arctic seabed offensive represents the systematic expansion of Soviet naval interdiction doctrines developed at the height of the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, the Soviet Northern Fleet and naval intelligence maintained dedicated special-purpose underwater reconnaissance brigades tasked with cutting Western undersea telegraph and SOSUS acoustic tracking cables across the Greenland-Iceland-United Kingdom Gap.",
        "According to Shvets, Soviet naval planners understood that in the opening phase of any major conflict, severing NATO undersea communications was essential to blind American anti-submarine warfare networks and allow Northern Fleet nuclear submarines to surge through the Barents Sea bastion into open Atlantic waters. Shvets revealed that KGB coastal surveillance posts in Murmansk and Kola tracked commercial cable maintenance ships closely, mapping physical coordinates of subsea repeaters to ensure rapid demolition by Spetsnaz combat divers and midget submarines.",
        "Today, that acoustic and telecommunication battlefield has intensified as commercial Arctic shipping lanes open and satellite downlink volumes surge. Svalbard's unique legal demilitarized status under the 1920 treaty creates an exploitable grey-zone operational vacuum, allowing Russian state vessels to conduct hydrographic mapping under the guise of marine scientific research. By pre-positioning sabotage payloads and acoustic monitoring beacons, Moscow retains the capability to instantly plunge Arctic intelligence collection into absolute darkness.",
        "Track the deployment of GUGI seabed surveillance vessels, monitor polar fiber telemetry across the Barents shelf, and recognize that the most vulnerable arteries of modern digital civilization lie silent on the ocean floor. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="svalbard_cable", title=EPISODE_DATA["title"])
    img.save(IMG_EP106, "WEBP", quality=92)
    print(f"Saved: {IMG_EP106}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP106, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP106, IMG_REX, IMG_STUDIO, IMG_EP106, IMG_REX, IMG_EP106]
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
    brain_cover = r"assets\cover_ep106_procedural.webp"
    with Image.open(IMG_EP106) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
