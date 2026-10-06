# engine/produce_episode_114.py
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

IMG_EP114 = os.path.join(THUMBS_DIR, "2026-10-10-18.webp")
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
    "id": "2026-10-10-18",
    "hour": "18:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Strait of Malacca Blockade Scenarios, Kra Isthmus Bypasses & Soviet Indian Ocean SIGINT",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes US-allied naval blockade scenarios across the 1.5-mile Phillips Channel bottleneck in the Strait of Malacca, Kra Isthmus pipeline bypass infrastructure, and Yuri Shvets on Soviet 8th Operational Squadron Indian Ocean chokepoint interdiction.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eighteen hundred hours. Stretching five hundred and fifty miles between the Malay Peninsula and the Indonesian island of Sumatra, the Strait of Malacca is the primary maritime carotid artery of the Indo-Pacific. Through its narrowest constriction—the 1.5-nautical-mile Phillips Channel in the Singapore Strait—travels more than sixty percent of China's maritime crude oil imports and a vast fraction of global containerized trade. In modern Indo-Pacific war-gaming, this bottleneck represents Beijing's ultimate strategic nightmare: the Malacca Dilemma, where distant naval blockades could strangle energy supply lines before a single shot is fired in the Taiwan Strait.",
        "To execute or counter an asymmetric blockade, regional militaries are deploying layered maritime access-denial networks. US and allied planners model distant blockade operations anchored at Diego Garcia and the Andaman and Nicobar Islands, deploying uncrewed undersea gliders and P-8A Poseidon maritime patrol aircraft to choke the western approaches. In response, Beijing is accelerating massive overland infrastructure bypasses, including deep-water port concessions in Kyaukpyu, Myanmar, and reviving proposals for Thailand's Kra Isthmus land-bridge canal and energy pipeline corridor to bypass the vulnerable Malacca passage entirely.",
        "This geopolitical contest over Indian Ocean maritime chokepoints directly mirrors the naval confrontation between Moscow and Washington during the peak of the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, the Soviet Navy's 8th Operational Squadron maintained continuous combat patrols across the Indian Ocean to track Western strategic transit through Malacca.",
        "According to Shvets, the KGB First Chief Directorate and Soviet naval intelligence operated specialized intelligence collection ships (AGIs) disguised as commercial hydrographic survey vessels stationed permanently off the Malacca and Sunda Straits. Soviet naval doctrine recognized that control over Indian Ocean sealanes was the vital hinge between European NATO supply networks and Pacific theater logistics. Shvets revealed that Soviet SIGINT stations in Cam Ranh Bay, Vietnam, and Aden, Yemen, maintained an unbroken acoustic tracking perimeter, logging every Western tanker and warship hull signature to feed targeting coordinates to Soviet nuclear attack submarines.",
        "Decades later, the vectors of confrontation have shifted from Soviet cruise-missile submarines to Chinese carrier strike groups and land-based anti-ship ballistic missiles. Yet the geographical choke point remains unchanged. A naval standoff across the Phillips Channel would not merely halt regional shipping; it would trigger an immediate cascading collapse in global supply chains, paralyzing industrial manufacturing across East Asia and sending worldwide maritime freight and insurance rates into an existential shock.",
        "Never evaluate naval balance through fleet tonnage alone, trace the narrow sea corridors where global energy actually flows, and remember that when a maritime artery narrows to one mile, geography dictates the terms of war. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="malacca_blockade", title=EPISODE_DATA["title"])
    img.save(IMG_EP114, "WEBP", quality=92)
    print(f"Saved: {IMG_EP114}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP114, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP114,
        IMG_STUDIO,
        IMG_EP114,
        IMG_REX,
        IMG_EP114,
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
