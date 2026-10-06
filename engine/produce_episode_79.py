# engine/produce_episode_79.py
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

IMG_EP79 = os.path.join(THUMBS_DIR, "2026-10-09-07.webp")
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
    "id": "2026-10-09-07",
    "hour": "07:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Microelectronics Gray Markets, Counterfeit FPGA Diversion & Soviet Line X Semiconductor Smuggling",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates gray market defense microelectronics brokers, re-marked counterfeit FPGAs in military drones, and Yuri Shvets on KGB Directorate T Line X semiconductor smuggling networks.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero seven hundred hours. In the complex supply chains supporting modern aerospace and defense weapons systems, the most critical single point of vulnerability is not advanced stealth coatings or aerodynamic airframes, but integrated circuit silicon. Across military drones, radar transceivers, and precision-guided glide bombs, defense primes rely on advanced Field-Programmable Gate Arrays, or FPGAs. However, decades of commercial offshoring and unregulated defense sub-tier contracting have created a thriving global gray market where counterfeit, reclaimed, and cloned microchips routinely infiltrate the Department of Defense inventory.",
        "Recent investigations into recovered reconnaissance drones in Eastern Europe have revealed commercial-grade microcontrollers and repurposed consumer FPGAs that were chemically scraped, laser re-marked with false military specification part numbers, and laundered through third-country brokers. Because prime defense contractors frequently waive physical destructive lot testing to avoid production bottlenecks, counterfeit chips with altered firmware and severe thermal vulnerabilities enter active weapons inventories. Simultaneously, unmonitored broker rings divert genuine military-grade radiation-hardened chips directly into sanctioned Russian missile manufacturing facilities.",
        "This global microelectronics smuggling pipeline is the direct contemporary evolution of Soviet clandestine technology acquisition. Former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively documented how the KGB's Directorate T—specifically the elite officers of Line X—spent the Cold War orchestrating illicit technology pipelines. Line X officers embedded within Soviet trade delegations, embassies, and academic exchanges were tasked with bypassing Western export controls to acquire embargoed American microelectronics and semiconductor manufacturing machinery.",
        "According to Shvets, the KGB established intricate networks of dummy import-export firms across Austria, Switzerland, Singapore, and West Germany to siphon Silicon Valley microprocessors back to Moscow. Soviet military aviation and ballistic missile guidance systems were entirely dependent on reverse-engineered Intel and Texas Instruments architectures smuggled by Line X couriers. Shvets revealed that corrupt Soviet defense ministers funneled millions in hard-currency kickbacks to Western middleman brokers while suppressing internal reports warning that reverse-engineered chips exhibited catastrophic reliability failures in field operations.",
        "Today, the names have changed, but the structural corruption remains identical. By allowing defense procurement to rely on tiered, opaque broker networks without end-to-end silicon provenance verification, Western defense agencies are actively funding the illicit diversion networks that arm their adversaries while delivering compromised hardware to their own frontlines.",
        "Audit the silicon wafer provenance, trace the third-country broker conduits, and verify the microelectronics lot testing. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="counterfeit_chip")
    img.save(IMG_EP79, "WEBP", quality=92)
    print(f"Saved: {IMG_EP79}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP79, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP79, IMG_REX, IMG_STUDIO, IMG_EP79, IMG_REX, IMG_EP79]
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
    brain_cover = r"assets\cover_ep79_procedural.webp"
    with Image.open(IMG_EP79) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
