# engine/produce_episode_82.py
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

IMG_EP82 = os.path.join(THUMBS_DIR, "2026-10-09-10.webp")
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
    "id": "2026-10-09-10",
    "hour": "10:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Barents Sea Nuclear Submarine Bastions, Arctic SOSUS Hydrophone Arrays & Northern Fleet Sanctuary Doctrines",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Russian Northern Fleet ballistic missile submarine bastion warfare in the Barents Sea, NATO Arctic SOSUS hydrophone barriers, and Yuri Shvets on Soviet undersea strategic nuclear sanctuary doctrines.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is ten hundred hours. Beneath the shifting polar pack ice and frigid waters of the Barents Sea lies the ultimate center of gravity for Russian strategic nuclear deterrence: the Arctic naval bastion. Since the early 1970s, the Russian Northern Fleet has organized its entire surface, subsurface, and aerospace combat architecture around a single imperative—protecting its nuclear-powered ballistic missile submarines, or SSBNs, within heavily fortified maritime sanctuaries. From the Kola Peninsula to the ice edge north of Novaya Zemlya, the Barents Sea is engineered as a layered acoustic fortress.",
        "To penetrate this sanctuary, Western naval planners have deployed advanced SOSUS hydrophone barriers along the Greenland-Iceland-United Kingdom Gap and across the Svalbard-Norway maritime corridor. Fixed seabed sonar arrays listening for acoustic cavitation signatures are supplemented by autonomous underwater gliders and Virginia-class attack submarines. However, inside the Barents bastion, extreme acoustic thermoclines, jagged undersea ridges, and seasonal ice keels create intense acoustic baffling. Russian Borei-class SSBNs navigate beneath the polar ice shelf, utilizing the natural ambient acoustic noise of fracturing ice sheets to mask their pump-jet propulsion signatures from Western passive sonars.",
        "This sanctuary warfare concept is the purest surviving legacy of Soviet maritime strategic planning. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet naval leadership recognized after the Cuban Missile Crisis that their nuclear submarines could not survive open-ocean transit across the North Atlantic against NATO's pervasive SOSUS network. Under Admiral Sergey Gorshkov, Soviet doctrine executed a radical strategic pivot: rather than sending submarines out into contested oceans, the USSR brought its ballistic missile submarines home into heavily defended bastions.",
        "According to Shvets, the KGB's First Chief Directorate and technical intelligence departments played a pivotal role in constructing this northern fortress. The KGB secured bathymetric profiles of the Barents seabed and smuggled acoustic quieting technology, including precision multi-axis Japanese CNC milling machines, to manufacture silent submarine propellers. Shvets revealed that corrupt Soviet naval procurement officials engaged in massive budget inflation, diverting billions in Arctic defense appropriations while reporting inflated readiness statistics to the Kremlin. Yet despite pervasive institutional graft, the geopolitical geometry of the Arctic bastion remains unaltered.",
        "As melting Arctic ice sheets open new northern sea routes and intensify great power competition, NATO and Russian forces are locked in an escalating acoustic arms race. The Barents Sea remains the primary flashpoint where covert undersea collisions could trigger strategic nuclear escalation. In the high north, silence is the only margin of survival.",
        "Audit the Arctic bathymetric contours, monitor the Barents hydrophone telemetry, and track the northern bastions. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="barents_bastion")
    img.save(IMG_EP82, "WEBP", quality=92)
    print(f"Saved: {IMG_EP82}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP82, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP82, IMG_REX, IMG_STUDIO, IMG_EP82, IMG_REX, IMG_EP82]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep82_procedural.webp"
    with Image.open(IMG_EP82) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
