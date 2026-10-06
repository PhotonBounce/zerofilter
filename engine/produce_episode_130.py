# engine/produce_episode_130.py
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

IMG_EP130 = os.path.join(THUMBS_DIR, "2026-10-11-10.webp")
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
    "id": "2026-10-11-10",
    "hour": "10:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Suwalki Gap Rail Corridors, Kaliningrad Iskanders & Soviet Baltic Chokepoints",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the strategic vulnerability of the Suwalki Gap, Russian broad-gauge railway transit lines between Belarus and Kaliningrad, the Iskander-M nuclear-capable A2/AD missile envelope, and Yuri Shvets on Soviet Baltic Military District operational war plans, KGB transport surveillance, and chokepoint interdiction doctrine.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is ten hundred hours. In the defense geography of Eastern Europe, NATO's most precarious vulnerability is a narrow strip of land barely sixty-five kilometers wide: the Suwalki Gap. Wedged between Poland and Lithuania, this corridor connects the Baltic states to mainland Europe while separating the heavily militarized Russian exclave of Kaliningrad from Moscow's client state, Belarus. In any high-intensity confrontation, a dual-axis armored pincer could sever the corridor within seventy-two hours, trapping three NATO member nations behind an anti-access bubble.",
        "At the center of daily friction is the Russian broad-gauge railway corridor traversing Lithuanian territory under the European Union transit regime. Every day, freight and passenger trains roll between mainland Russia and Kaliningrad, carrying industrial cargo, dual-use electronics, and personnel under specialized sealed transit permits. Western intelligence agencies know that these rail arteries serve as vital logistical conduits for the Russian Baltic Fleet, while simultaneously presenting an acute sabotage and false-flag vector that the Kremlin periodically exploits to probe NATO border enforcement.",
        "Dominating the Suwalki corridor is Kaliningrad's formidable anti-access and area-denial bastion. Armed with hypersonic Iskander-M ballistic missiles, Bastion coastal defense batteries, and S-400 surface-to-air missile regiments, the exclave forms an overlapping kill zone extending five hundred kilometers across Poland, Lithuania, and the southern Baltic Sea. Operating under this protective umbrella, Russian naval and electronic warfare units at Baltiysk can jam commercial GPS signals and deny maritime reinforcement corridors to allied ports.",
        "This strategy of holding the Baltic approaches hostage is the direct operational descendant of Soviet war planning. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, the Soviet General Staff spent decades designing rapid land-bridge offensives to isolate the Baltic rim and sever Western logistical reinforcement.",
        "According to Shvets, the Soviet Baltic Military District—headquartered in Riga—and the KGB Third Chief Directorate maintained exhaustive operational blueprints to sever road and rail corridors across the Suwalki axis during the opening hours of a European war. Shvets revealed that KGB transport directorate officers embedded directly within the Ministry of Railways, monitoring every freight wagon and mapping pre-targeted rail bottlenecks for demolition or seizure by Spetsnaz sabotage detachments, guaranteeing that Baltic supply lines could be severed at a moment's notice.",
        "From Soviet Baltic Military District offensive timetables to modern Iskander missile deployments around Kaliningrad, the geography of the Suwalki Gap remains Eastern Europe's ultimate strategic fulcrum. When a sixty-five kilometer land bridge determines the survival of three sovereign nations, there is no margin for complacency. Monitor the transit rails, track the missile batteries, and secure the northern flank. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="suwalki_gap", title=EPISODE_DATA["title"])
    img.save(IMG_EP130, "WEBP", quality=92)
    print(f"Saved: {IMG_EP130}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP130, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP130,
        IMG_STUDIO,
        IMG_EP130,
        IMG_REX,
        IMG_EP130,
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
    manifest["updated"] = "2026-10-06T14:45:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
