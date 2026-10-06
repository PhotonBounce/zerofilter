# engine/produce_episode_118.py
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

IMG_EP118 = os.path.join(THUMBS_DIR, "2026-10-10-22.webp")
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
    "id": "2026-10-10-22",
    "hour": "22:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Bab el-Mandeb Subsea Cable Sabotage, Houthi ROVs & Soviet Red Sea Naval Doctrine",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the vulnerability of Red Sea subsea telecommunications corridors in the Bab el-Mandeb strait, commercial anchor-dragging interdictions versus specialized Houthi ROV seabed salvage capabilities, and Yuri Shvets on Soviet 8th Operational Squadron maritime choke point warfare in the Horn of Africa.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-two hundred hours. Beneath the turquoise waters of the Bab el-Mandeb strait lies one of the most concentrated and vulnerable digital bottlenecks on planet Earth. Over seventeen percent of all global internet traffic—carrying trillions of dollars in daily intercontinental banking clearances, cloud server synchronization, and military command data between Europe and Asia—transits through submarine fiber-optic cables traversing this narrow twenty-nine-kilometer maritime passage separating Djibouti and Yemen. Four major transcontinental systems—the Asia-Africa-Europe-One, the Europe India Gateway, SEA-ME-WE Five, and Seacom—run tightly clustered along a shallow, volatile seafloor.",
        "When multiple subsea conduits were severed in a single catastrophic disruption, global telecommunications routing was instantly destabilized. Over twenty-five percent of data traffic between Asia and Europe was severed, forcing automated traffic failovers onto terrestrial paths or the grueling route around the Cape of Good Hope, adding over one hundred and forty milliseconds of critical latency. While initial commercial maritime reports attributed the severing to the dragging anchor of the missile-damaged cargo vessel Rubymar drifting through the strait, technical analysis of optical time-domain reflectometry traces revealed suspicious spatial precision along the bathymetric trench.",
        "Naval intelligence assessments confirmed that regional maritime forces, bolstered by Iranian advisory cadres, have actively integrated autonomous underwater vehicles and commercial remotely operated submersibles equipped with manipulator claws and acoustic beacons. Operating in shallow coastal shelves of less than one hundred and fifty meters depth, these unmanned submersibles can easily locate, tag, and mechanically disrupt armored telecom cables, transforming abyssal infrastructure into an asymmetric weapon of economic and digital warfare.",
        "This systematic targeting of maritime choke points and seabed infrastructure is not a modern innovation; it is the direct tactical inheritance of Soviet Cold War naval doctrine in the Horn of Africa. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet naval planners under Admiral Sergey Gorshkov recognized the Bab el-Mandeb as a decisive planetary pressure point.",
        "According to Shvets, the Soviet Navy's 8th Operational Squadron established forward operating bases on Eritrea's Dahlak Archipelago and permanent anchorages off Socotra Island specifically to contest the Red Sea and monitor Western maritime lifelines. Shvets revealed that KGB Directorate T and naval hydrographic survey vessels meticulously charted every subsea telegraph and telephone cable traversing the Red Sea bed. Soviet planners developed specialized seabed sabotage and wiretap tactics engineered to instantly isolate Western capitals from Middle Eastern oil hubs and Asian allies upon the outbreak of hostilities.",
        "Today, the democratization of cheap subsea drones and state-sponsored proxy warfare has resurrected Soviet seabed interdiction at scale. When regional non-state actors can paralyze continental communications from a fishing dhow without firing a missile, the digital backbone of civilization is dangerously exposed. Track the conduits beneath the waves, audit the physical security of your data packets, and never assume the seabed is secure. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="red_sea_cables", title=EPISODE_DATA["title"])
    img.save(IMG_EP118, "WEBP", quality=92)
    print(f"Saved: {IMG_EP118}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP118, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP118,
        IMG_STUDIO,
        IMG_EP118,
        IMG_REX,
        IMG_EP118,
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
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
        
    manifest["episodes"].insert(0, full_episode_entry)
    manifest["updated"] = "2026-10-06T13:54:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
