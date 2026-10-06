# engine/produce_episode_95.py
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

IMG_EP95 = os.path.join(THUMBS_DIR, "2026-10-09-23.webp")
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
    "id": "2026-10-09-23",
    "hour": "23:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "corruption",
    "title": "Strategic Tungsten Carbide Diversion, Munitions Stockpile Fraud & Soviet Line X Metal Smuggling",
    "subject": "Hourly uncensored breakdown: Rex Vance exposes fraudulent tungsten carbide certifications in defense armor-piercing kinetic penetrators, depleted national defense stockpiles, and Yuri Shvets on Soviet Line X strategic metal smuggling rings.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-three hundred hours. While the public debates defense budget toplines and aid packages, the physical kinetic lethality of Western artillery shells, tank armor penetrators, and precision guided warheads is being hollowed out from within. At the core of all modern armor-piercing munitions lies tungsten carbide—a ultra-dense refractory metal alloy capable of defeating hardened ceramic and reactive vehicle armor. Yet forensic defense audits reveal that defense sub-tier contractors are systematically substituting substandard, commercial-grade sintered scrap powder while billing the Pentagon and allied ministries for aerospace-certified mil-spec tungsten.",
        "The National Defense Stockpile, established to guarantee twelve months of sovereign industrial surge capacity during major great-power conflicts, has been catastrophically depleted through decades of Congressional liquidation sales and sole-source foreign dependency. Over eighty percent of global tungsten processing is monopolized by geopolitical rivals. To bridge the deficit, defense procurement brokers have turned to third-party shell importers in Central Europe and Southeast Asia, laundering unrefined or adulterated metal through forged metallurgical certificates of conformance to pass routine visual inspections.",
        "This strategic metallurgical vulnerability is not an accidental byproduct of modern globalization; it is the exact asymmetric playbook perfected by Soviet economic intelligence. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively disclosed, the KGB First Chief Directorate's Directorate T and its specialized Line X officers prioritized the covert acquisition and diversion of Western strategic metals and high-temperature alloys above almost all conventional military hardware.",
        "According to Shvets, Soviet defense metallurgists struggled for decades with grain-boundary embrittlement and purity defects in indigenous tungsten and titanium armor penetrators. To compensate, Line X established dummy commercial export fronts in Austria, Sweden, and West Germany to buy up Western high-purity tungsten and molybdenum under the guise of civilian mining drill tooling. Shvets revealed that Soviet intelligence couriers smuggled thousands of metric tons of Western strategic alloys into Soviet defense ministry research combines, simultaneously planting falsified metal quality certificates into European commercial supply chains to degrade Western munitions inventories.",
        "Today, that exact diversion architecture has been weaponized against the Western defense industrial base in reverse. When frontline tank crews fire armor-piercing kinetic rounds manufactured with adulterated tungsten carbide, the penetrators shatter prematurely against modern explosive reactive armor blocks instead of punching through. Private defense cartels reap record cost-plus margins on forged metallurgy, while combat forces inherit brittle munitions that fail during the first hours of high-intensity maneuver warfare.",
        "Audit the National Defense Stockpile metallurgical testing labs, demand independent mass-spectrometer verification of all incoming kinetic penetrator shipments, and prosecute the fraudulent brokers. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="tungsten_carbide", title=EPISODE_DATA["title"])
    img.save(IMG_EP95, "WEBP", quality=92)
    print(f"Saved: {IMG_EP95}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP95, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP95, IMG_REX, IMG_STUDIO, IMG_EP95, IMG_REX, IMG_EP95]
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
    brain_cover = r"assets\cover_ep95_procedural.webp"
    with Image.open(IMG_EP95) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
