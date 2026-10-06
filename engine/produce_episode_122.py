# engine/produce_episode_122.py
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

IMG_EP122 = os.path.join(THUMBS_DIR, "2026-10-11-02.webp")
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
    "id": "2026-10-11-02",
    "hour": "02:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Strait of Gibraltar ASW Acoustic Barriers, Moroccan Radar & Soviet 5th Eskadra Chokepoints",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the subsea acoustics and acoustic convergence zones of the Strait of Gibraltar, Moroccan-Spanish radar integration, nuclear submarine thermocline transit tactics, and Yuri Shvets on the Soviet Navy's 5th Operational Squadron Mediterranean choke point surveillance.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero two hundred hours. Separating Europe from Africa by just fourteen kilometers of turbulent water, the Strait of Gibraltar is the supreme naval gate of the Mediterranean Basin. Every vessel, commercial container carrier, and nuclear submarine moving between the Atlantic Ocean and the Mediterranean must navigate this narrow corridor bounded by Spain's Tarifa Point and the Moroccan promontories of Cape Spartel and Jebel Musa. Beneath the surface, NATO operates one of the most sophisticated fixed seabed acoustic barrier gates on Earth.",
        "The hydrography of Gibraltar creates an extraordinary two-layer fluid dynamic battlefield. Low-salinity Atlantic surface water rushes relentlessly eastward into the Mediterranean at speeds exceeding two and a half knots, while colder, hypersaline Mediterranean deep water plunges westward into the Atlantic below one hundred and fifty meters depth. At the Camarinal Sill, the shallowest underwater ridge at two hundred and eighty meters, this velocity shear generates massive internal soliton waves and a severe thermocline acoustic shadow that bends sonar arrays, creating blind acoustic zones where stealth submarines attempt covert transit.",
        "To counter submarine penetration, NATO has integrated fixed SOSUS hydrophone arrays anchored across the sill with joint Spanish-Moroccan coastal surface radar corridors and maritime patrol aircraft. Any nuclear attack submarine attempting to pass through Gibraltar must either surface and declare its transit under international law or execute a perilous cold-drift run, cutting propulsion engines and drifting silently on the deep outgoing or surface incoming currents beneath the thermocline baffle.",
        "This tactical game of acoustic cat-and-mouse was central to Cold War Soviet naval operations. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, penetrating and surveilling the Strait of Gibraltar was a paramount operational directive for the Soviet Navy's 5th Operational Squadron, the Mediterranean Eskadra.",
        "According to Shvets, the 5th Eskadra operated out of Syria's Port of Tartus and forward anchorages off the North African coast, tasked with tracking US Sixth Fleet aircraft carriers and ballistic missile submarines. Shvets revealed that Soviet Victor and Charlie-class nuclear submarines developed daring thermocline-riding transit profiles through Gibraltar, using the turbulent internal wave noise to mask their reactor pump cavitation. Soviet naval intelligence closely monitored Western acoustic listening posts in Gibraltar and Ceuta, mapping acoustic convergence zones to identify blind corridors where Soviet hunter-killer subs could slip into the Atlantic undetected.",
        "Today, with the Mediterranean contested by Russian Mediterranean detachments and expanding Chinese commercial port investments, the Gibraltar chokepoint remains a silent, high-stakes acoustic fortress. In the undersea domain, geography is destiny, and whoever masters the thermocline controls the transit of continents. Monitor the subsea barriers, track the unseen currents, and never assume the sea floor is neutral. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="gibraltar_asw", title=EPISODE_DATA["title"])
    img.save(IMG_EP122, "WEBP", quality=92)
    print(f"Saved: {IMG_EP122}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP122, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP122,
        IMG_STUDIO,
        IMG_EP122,
        IMG_REX,
        IMG_EP122,
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
    manifest["updated"] = "2026-10-06T14:08:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
