# engine/produce_episode_110.py
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

IMG_EP110 = os.path.join(THUMBS_DIR, "2026-10-10-14.webp")
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
    "id": "2026-10-10-14",
    "hour": "14:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Strait of Hormuz Hydrophone Gates, Fast-Boat Swarms & Soviet Persian Gulf Naval Strategy",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates undersea acoustic hydrophone gate closure operations in the Strait of Hormuz, IRGC fast-attack missile boat swarm coordination, and Yuri Shvets on Soviet 5th Operational Squadron Persian Gulf interdiction doctrine.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is fourteen hundred hours. Barely twenty-one nautical miles across at its narrowest constriction, the Strait of Hormuz represents the single most volatile energy chokepoint on Earth. Through this shallow maritime corridor passes more than twenty percent of global petroleum consumption and massive liquefied natural gas shipments. Yet beneath the heavily trafficked commercial shipping lanes, an undeclared asymmetric siege is hardening: the deployment of autonomous seabed hydrophone tripwires, seabed mine arrays, and coordinated fast-attack craft designed to slam the maritime gate shut at a moment's notice.",
        "Recent satellite synthetic aperture radar passes and naval intelligence intercepts reveal dense undersea surveillance infrastructure installed along the Musandam Peninsula and Qeshm Island. Iran's Islamic Revolutionary Guard Corps Navy has integrated bottom-moored passive acoustic hydrophone arrays with coastal anti-ship missile batteries and swarm-optimized Peykaap-class missile boats. By networking acoustic signature databases with low-observable reconnaissance drones, adversary command nodes can calculate targeting coordinates for dual-mode anti-ship ballistic missiles without ever turning on active coastal search radars, stripping US carrier strike groups of early electronic warning.",
        "This doctrine of weaponizing narrow maritime choke points is not an indigenous Persian Gulf innovation; it is the modern refinement of Soviet naval strategy developed to counter Western carrier battle groups during the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively disclosed, the Soviet Navy's 5th Operational Squadron maintained comprehensive operational plans to interdict Western naval task forces in the Persian Gulf and Indian Ocean.",
        "According to Shvets, the KGB First Chief Directorate closely observed Operation Earnest Will in the late 1980s, analyzing Western naval minesweeping deficiencies and the lethal vulnerability of major combatants to low-cost sea mines and asymmetric gunboat attacks. Soviet naval strategists realized that the US Navy's blue-water supremacy was neutralized in confined, shallow littorals where acoustic reverberation cripples passive sonar. Shvets documented that Soviet naval advisors quietly transferred acoustic sea mine telemetry and anti-ship missile doctrine to regional proxies, establishing the blueprint for the very access-denial networks operating in Hormuz today.",
        "Decades later, the Pentagon's Fifth Fleet is attempting to counter this threat through Task Force 59's uncrewed surface vessels and artificial intelligence acoustic processing grids. Yet the strategic math remains unforgiving. A single commercial supertanker hull breach or a salvo of sea-skimming cruise missiles coordinated across the shipping channels would trigger immediate maritime insurance cancellations, collapsing global crude transit and sending world energy markets into an uncontrollable vertical spike.",
        "Never trust official freedom-of-navigation assurances in shallow waters, monitor the acoustic tripwires lining the straits, and remember that when maritime choke points are weaponized, global commerce hangs by a microscopic thread. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="hormuz_hydrophone", title=EPISODE_DATA["title"])
    img.save(IMG_EP110, "WEBP", quality=92)
    print(f"Saved: {IMG_EP110}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP110, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP110,
        IMG_STUDIO,
        IMG_EP110,
        IMG_REX,
        IMG_EP110,
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
