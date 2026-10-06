# engine/produce_episode_70.py
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

IMG_EP70 = os.path.join(THUMBS_DIR, "2026-10-08-22.webp")
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
    "id": "2026-10-08-22",
    "hour": "22:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Arctic Undersea Fiber-Optic Cable Sabotage, Svalbard Seabed Sonar Arrays & Soviet GUGI Operations",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates severed Arctic fiber-optic trunks, seabed warfare along the Svalbard undersea acoustic perimeter, and Yuri Shvets's insider analysis of Soviet GUGI deep-sea reconnaissance operations.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-two hundred hours. Beneath the freezing surface waters of the Norwegian and Barents Seas, an invisible shadow war is unfolding along the abyssal seabed. Over ninety-five percent of transoceanic internet traffic, interbank financial transfers, and allied military command communications transit through pencil-thin undersea fiber-optic cables resting entirely unprotected on the continental shelf. In the Arctic, repeated catastrophic cable severances around the Svalbard archipelago have exposed a calculated campaign of seabed sabotage and underwater reconnaissance that Western defense ministries are struggling to contain.",
        "The strategic geography of the Svalbard undersea corridor is critical. The twin fiber-optic cables linking Longyearbyen to mainland Norway provide high-speed data transmission for polar satellite ground stations tracking allied reconnaissance orbits. When undersea seismic sensors and fiber trunks were physically cut, forensic oceanographic telemetry revealed that the severed conduits were not damaged by commercial fishing trawlers or natural ice scouring, but cleanly severed by specialized submersibles equipped with robotic manipulators. Beneath the acoustic thermocline, Russian deep-sea special mission submarines operating under the Main Directorate of Deep-Sea Research, known as GUGI, utilize nuclear-powered motherships and auxiliary oceanographic intelligence vessels to map and tap critical seabed chokepoints.",
        "This abyssal warfare doctrine has deep institutional lineage in Cold War intelligence operations. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet naval intelligence and the KGB's First Chief Directorate maintained dedicated seabed reconnaissance teams focused on finding, tapping, and neutralizing NATO's SOSUS acoustic hydrophone arrays. The Soviet Union recognized that controlling the seabed floor was essential to guaranteeing the safe egress of Northern Fleet ballistic missile submarines into the North Atlantic.",
        "According to Shvets, Soviet specialized oceanographic ships routinely operated under the cover of civilian marine biology expeditions and commercial trawler flags to mask their hydrographic charting missions. Shvets documented that Soviet naval engineers developed specialized seabed crawlers and deep-diving bathyscaphes capable of descending thousands of meters to inspect transoceanic cables and plant explosive charges. Shvets emphasizes that today's GUGI operations in the Arctic are the direct evolution of these Cold War programs: a deniable asymmetric weapon designed to blind Western satellite downlinks and severed financial backbones before a broader kinetic escalation.",
        "Western navies are now racing to deploy autonomous undersea drone swarms and seabed acoustic arrays to establish persistent maritime surveillance over critical infrastructure. But protecting hundreds of thousands of kilometers of unarmored glass fibers on the dark ocean floor remains a logistical nightmare. In twenty-first-century conflict, the nation that severs the undersea cables blinds its adversary without firing a single missile.",
        "Audit the abyssal bathymetry, track the shadow oceanographic research vessels, and monitor the Svalbard fiber links. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="svalbard_cable")
    img.save(IMG_EP70, "WEBP", quality=92)
    print(f"Saved: {IMG_EP70}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP70, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP70, IMG_REX, IMG_STUDIO, IMG_EP70, IMG_REX, IMG_EP70]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep70_procedural.webp"
    with Image.open(IMG_EP70) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
