# engine/produce_episode_78.py
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

IMG_EP78 = os.path.join(THUMBS_DIR, "2026-10-09-06.webp")
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
    "id": "2026-10-09-06",
    "hour": "06:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Strait of Hormuz Acoustic Sensor Gates, Iranian Midget Subs & Soviet Persian Gulf Choke Point Doctrines",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates acoustic hydrophone choke point gates across the Strait of Hormuz, Ghadir-class midget submarine patrols, and Yuri Shvets on Soviet naval bastion warfare in the Persian Gulf.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero six hundred hours. Twenty percent of global petroleum consumption traverses the Strait of Hormuz—a narrow, shallow maritime funnel measuring barely twenty-one nautical miles across at its narrowest constriction. While Western defense planners fixate on surface anti-ship missile batteries and fast-attack swarm craft, the truly decisive theater of denial operates silently along the shallow Persian Gulf seabed. Regional naval forces have deployed permanent, fiber-optic-linked acoustic hydrophone sensor arrays coupled with autonomous seabed tripwires across the inbound and outbound commercial tanker shipping lanes.",
        "These seabed listening gates operate in tandem with diesel-electric Ghadir-class midget submarines. In shallow, hyper-saline waters characterized by severe acoustic thermoclines and intense commercial ambient shipping noise, large Western nuclear attack submarines lose their acoustic stealth advantage. The thirty-meter Ghadir midget subs, resting silently on the sandy seabed with electric motors powered down, serve as pre-positioned launch platforms for wake-homing torpedoes and smart bottom-moored naval mines. Western surface escorts entering the strait operate in an acoustic kill zone where acoustic detection ranges collapse to less than two thousand yards.",
        "This maritime denial architecture represents the direct implementation of Soviet naval doctrine engineered during the height of the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently disclosed, the Soviet Navy's Fifth Operational Squadron and KGB technical intelligence stations conducted exhaustive bathymetric and acoustic surveys of the Persian Gulf and Arabian Sea throughout the 1970s and 1980s. Soviet naval strategists realized they could never defeat the United States Fifth Fleet in open ocean blue-water combat.",
        "According to Shvets, Soviet naval doctrine prioritized closing strategic maritime choke points through asymmetric combinations of seabed acoustic sensors, covert submarine minelaying, and shore-based electronic warfare. Shvets revealed that KGB technical bureaus transferred acoustic hydrophone manufacturing blueprints, passive sonar processing algorithms, and magnetic influence mine firing circuits to regional proxy regimes. The acoustic gate infrastructure spanning Hormuz today is the modern, digitized descendant of Soviet naval acoustic barrier doctrine developed by the Admiral Gorshkov naval staff in Moscow.",
        "Western policy think tanks continue to advocate for freedom of navigation patrols using massive billion-dollar guided-missile cruisers. Yet naval physics cannot be bypassed by political rhetoric. In restricted, shallow acoustic chokepoints, asymmetric midget submarines and seabed sensor gates render high-value surface combatants extraordinarily vulnerable. A single successful seabed mine detonation would instantly paralyze global energy transit.",
        "Audit the Hormuz bathymetric hydrophone telemetry, trace the Soviet naval acoustic lineage, and watch the maritime funnels. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="hormuz_hydrophone")
    img.save(IMG_EP78, "WEBP", quality=92)
    print(f"Saved: {IMG_EP78}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP78, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP78, IMG_REX, IMG_STUDIO, IMG_EP78, IMG_REX, IMG_EP78]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep78_procedural.webp"
    with Image.open(IMG_EP78) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
