# engine/produce_episode_127.py
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

IMG_EP127 = os.path.join(THUMBS_DIR, "2026-10-11-07.webp")
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
    "id": "2026-10-11-07",
    "hour": "07:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "corruption",
    "title": "Pentagon F-35 ALIS Software Cost Escalations, Lockheed IP Lock-In & Soviet Plant Kickbacks",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the trillion-dollar F-35 sustainment crisis, the catastrophic software failure and vendor lock-in of the Autonomic Logistics Information System (ALIS) and ODIN, Lockheed Martin's proprietary data rights monopoly, and Yuri Shvets on Soviet Ministry of Aviation Industry (MAP) plant kickbacks and aircraft factory corruption.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero seven hundred hours. In the annals of military procurement disasters, no single weapon system embodies systemic software grift quite like the F-35 Joint Strike Fighter. Projected to cost over one point seven trillion dollars across its lifecycle, the jet's greatest vulnerability is not enemy radar or surface-to-air missiles. It is an algorithmic black box: the Autonomic Logistics Information System, or ALIS, and its perpetually delayed replacement, the Operational Data Integrated Network, known as ODIN.",
        "Conceived as a revolutionary diagnostic brain that would predict mechanical failures and automate global spare parts delivery, ALIS became a bureaucratic nightmare of over twenty-four million lines of code. Military flight line maintainers discovered that ALIS routinely generated false alarm fault codes, grounded combat-ready aircraft over non-existent electronic errors, and required manual workarounds that added hundreds of thousands of maintenance hours. Government Accountability Office audits revealed that the system frequently lost track of critical spare parts, while the fleet's mission-capable rate plummeted below fifty-five percent.",
        "The root cause of this paralysis is contractor intellectual property lock-in. Prime contractor Lockheed Martin designed ALIS as a closed, proprietary architecture, refusing to transfer underlying technical data rights and diagnostic software source code to the Department of Defense. As a result, military technicians cannot fix, recode, or troubleshoot their own aircraft without paying proprietary licensing fees and contractor field support rates that siphon billions of taxpayer dollars annually into private balance sheets.",
        "This monopolistic extraction of state treasury resources through military hardware sustainment is the modern mirror of Soviet defense production corruption. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, Soviet aviation manufacturing operated under an identical regime of institutionalized extortion and artificial parts bottlenecks.",
        "According to Shvets, the Soviet Ministry of Aviation Industry, or MAP, alongside design bureaus like Mikoyan and Sukhoi, perfected bureaucratic kickback networks between manufacturing plants and military procurement directorates. Shvets revealed that plant directors routinely falsified aircraft delivery readiness, shipping fighters with defective avionics and missing critical sub-assemblies. To keep squadrons operational, military commanders had to pay off factory directors through shadow barter channels and off-the-books slush funds, ensuring that state aircraft factories enjoyed perpetual repair subsidies regardless of catastrophic fleet readiness rates.",
        "From Soviet aviation ministry factory kickbacks to modern proprietary code lock-in on the F-35, defense contractors have mastered the art of holding military readiness hostage to sustainment contracts. When the government does not own the code, it does not own the weapon. Demand software sovereignty, audit the contractor monopolies, and never fly on proprietary faith. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="f35_alis", title=EPISODE_DATA["title"])
    img.save(IMG_EP127, "WEBP", quality=92)
    print(f"Saved: {IMG_EP127}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP127, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP127,
        IMG_STUDIO,
        IMG_EP127,
        IMG_REX,
        IMG_EP127,
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
    manifest["updated"] = "2026-10-06T14:30:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
