# engine/produce_episode_63.py
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

IMG_EP63 = os.path.join(THUMBS_DIR, "2026-10-08-15.webp")
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
    "id": "2026-10-08-15",
    "hour": "15:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "corruption",
    "title": "Pentagon Microelectronics Counterfeiting, Gray-Market Broker Rings & Soviet Line X Infiltration",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates widespread counterfeit semiconductors and cloned microchips infiltrating the Department of Defense supply chain, gray-market broker cartels, and Yuri Shvets's insider revelations regarding Soviet KGB Line X technology theft networks.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is fifteen hundred hours. The most terrifying vulnerability in the United States military arsenal is not hypersonic missiles, strategic bombers, or nuclear submarines—it is a two-dollar counterfeit microchip soldered directly onto a missile guidance circuit board. Across the Department of Defense supply chain, tens of thousands of counterfeit, cloned, and remarked semiconductors are routinely discovered inside front-line weapons platforms, from Patriot air defense radars and ballistic missile interceptors to F-35 mission computers, funneled through unvetted gray-market brokers, paper front companies, and phantom suppliers.",
        "The physical forensic mechanisms of semiconductor counterfeiting are astonishingly sophisticated and pervasive. Discarded commercial e-waste circuit boards are acid-washed in overseas chop shops, sanded down with industrial abrasives to remove original manufacturer lot numbers, and re-etched with bogus military-grade military-standard part specifications. Microscopic acoustic microscopy, x-ray inspection, and chemical decapsulation audits frequently reveal defective silicon dies, missing internal bond wires, and unauthorized hardware backdoors designed to induce catastrophic circuit failure under extreme thermal stress, vibration, or high-altitude electromagnetic pulses.",
        "This systematic corruption of Western defense microelectronics is the direct modern continuation of a legendary Cold War operational playbook. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet Directorate T and its elite scientific-technical Line X unit specialized in the clandestine acquisition and sabotage of Western microelectronics. During the peak of the Cold War, Line X operatives established hundreds of commercial front companies, shell brokers, and diversion conduits across Western Europe and North America to bypass international export controls.",
        "According to Shvets, Soviet intelligence understood that infiltrating Western electronics distributors was vastly more effective than stealing blueprints from classified defense contractors. By manipulating unregulated gray-market broker syndicates, Soviet planners not only acquired embargoed integrated circuits for Soviet intercontinental ballistic missiles, but also mapped severe vulnerabilities in Western procurement oversight. Shvets emphasizes that modern defense contracting relies on multi-tiered subcontracts where prime contractors pocket massive cost-plus margins while delegating component purchasing to cut-rate brokers who source tainted chips with zero provenance verification.",
        "Today, the Pentagon's systemic dependence on unmonitored commercial supply chains represents an acute, existential national security emergency. Spending hundreds of billions on fifth-generation stealth platforms is completely meaningless when the microchips controlling their flight controls and telemetry are harvested from discarded e-waste and peddled by shadowy broker cartels. Modern military supremacy collapses the exact second you surrender custody of your silicon.",
        "Audit the silicon dies, inspect the gray-market manifests, and verify the microchip provenance. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="counterfeit_chip")
    img.save(IMG_EP63, "WEBP", quality=92)
    print(f"Saved: {IMG_EP63}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP63, output_mp4, duration=10)
    
    # 3. Audio Synthesis (Rex Vance Baritone)
    print("[3/5] Synthesizing audio via edge-tts (ChristopherNeural)...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    
    actual_duration = get_audio_duration(audio_path)
    print(f"Audio synthesized: {audio_path} ({actual_duration}s)")
    EPISODE_DATA["seconds"] = actual_duration
    
    # 4. Synchronized Art Frames
    print("[4/5] Creating 6 synchronized art frames...")
    art_sources = [
        IMG_EP63,
        IMG_REX,
        IMG_EP63,
        IMG_STUDIO,
        IMG_EP63,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = actual_duration / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
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
    
    print(f"[+] Successfully produced Episode {EPISODE_DATA['id']} ({actual_duration}s)!")

if __name__ == "__main__":
    asyncio.run(main())
