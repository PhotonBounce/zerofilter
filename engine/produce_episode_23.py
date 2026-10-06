# engine/produce_episode_23.py
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

IMG_EP23 = os.path.join(THUMBS_DIR, "2026-10-06-23.webp")
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
    "id": "2026-10-06-23",
    "hour": "23:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "quantum",
    "title": "Holographic Information Scrambling, Black Hole Horizons & Cyprus Tech Laundering",
    "subject": "Hourly uncensored breakdown: Rex Vance pairs the holographic principle and Hayden-Preskill quantum information scrambling with ex-KGB Major Yuri Shvets's unmasking of Cyprus offshore shell networks laundering sanctioned Western military microelectronics into Russian drone factories.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It's twenty-three hundred hours. Modern high-energy physics and international financial forensics are governed by the exact same fundamental conservation law: information cannot be destroyed, no matter how violently you attempt to scramble it. In theoretical quantum gravity, the holographic principle and the Hayden-Preskill protocol demonstrate that when information falls past the event horizon of a black hole, it isn't annihilated. It is rapidly scrambled across the boundary surface through maximal quantum chaos, waiting to be reconstructed by an observer with access to the Hawking radiation spectrum.",
        "In the financial underworld, illicit procurement cartels attempt to treat offshore shell company networks as event horizons. But as Washington intelligence insider and former KGB Major Yuri Shvets has exposed, no offshore banking corridor is an information sink. Shvets's disclosures reveal how Moscow's intelligence apparatus utilizes Limassol and Nicosia fiduciary trusts to disguise wire transfers from sanctioned Russian defense conglomerates, purchasing dual-use FPGA processors and navigation chips through ostensibly neutral commercial front companies.",
        "In quantum scrambling, the Hayden-Preskill thought experiment proved that once a system reaches thermal equilibrium, extracting a single qubit of injected information requires collecting only a few additional photons of radiation—provided you possess the system's prior entanglement history. In counter-intelligence financial forensics, the mechanics are identical. You don't need to subpoena every intermediary bank account along the shell pipeline. If you possess the source funding telemetry and the destination receiving manifests at the drone assembly plants, the intermediary scrambling network resolves instantaneously.",
        "The receipts coming out of downed Russian Geran and Lancet strike drones confirm this mathematical inevitability. Despite dozens of sanctions packages enacted by Western coalitions, teardown forensic audits by Ukrainian military intelligence consistently uncover Texas Instruments power regulators, Analog Devices signal converters, and Swiss-manufactured GNSS transceivers. The components didn't materialize through magic—they were funneled through Cyprus, the UAE, and Central Asian transit conduits using layered shell structures designed to mimic thermodynamic noise.",
        "Disarming these transnational smuggling pipelines requires replacing legacy bureaucratic sanctions enforcement with real-time graph neural networks and cryptographic bill-of-materials provenance. By embedding physical unclonable functions into defense-critical semiconductors and tracking blockchain-anchored custody handoffs, Western manufacturers can turn every chip into an active provenance beacon. You cannot obscure illicit diversion when every transaction generates immutable telemetry.",
        "Black holes scramble information, but they never destroy it—and neither do Cypriot bank vaults. The receipts always emerge in the radiation. Trust the physics, follow the wire transfers, and keep your filters at absolute zero. I'm Rex Vance. We'll see you at the top of the hour."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="holographic")
    img.save(IMG_EP23, "WEBP", quality=92)
    print(f"Saved: {IMG_EP23}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP23, output_mp4, duration=10)
    
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
        IMG_EP23,
        IMG_REX,
        IMG_EP23,
        IMG_STUDIO,
        IMG_EP23,
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
