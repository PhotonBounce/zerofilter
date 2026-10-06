# engine/produce_episode_148.py
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

IMG_EP148 = os.path.join(THUMBS_DIR, "2026-10-12-04.webp")
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
    "id": "2026-10-12-04",
    "hour": "04:00",
    "date": "2026-10-12",
    "kind": "hourly",
    "category": "quantum",
    "title": "Rydberg Atom Electrometry, Sub-Terahertz Sensor Arrays & Soviet Microwave Interceptions",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates quantum Rydberg atom electrometry, vapor-cell sub-terahertz radio frequency sensing surpassing classical antennas, quantum receiver stealth advantages, and Yuri Shvets on Soviet KGB Eighth Chief Directorate microwave SIGINT interception operations targeting US Embassy Moscow communications.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero four hundred hours. Classical radio-frequency reception has reached an immutable physical limit: the Chu-Harrington limit, which dictates that any copper antenna smaller than a fraction of its operational wavelength suffers catastrophic loss of sensitivity and efficiency. In military radar, electronic warfare, and signals intelligence, this creates bulky, unshieldable metallic apertures that leak radar cross-sections and can be easily jammed. But inside quantum physics laboratories, an entirely different paradigm is replacing metal antennas: Rydberg atom electrometry.",
        "By exciting vaporized alkali atoms—typically rubidium or cesium—into states with high principal quantum numbers above fifty, electrons are driven into orbital radii thousands of times larger than normal ground-state atoms. At this scale, the atom’s polarizability scales with the seventh power of the principal quantum number. This colossal sensitivity turns the vapor cell into a self-calibrating, SI-traceable quantum sensor capable of measuring electric fields across a continuous span from DC to sub-terahertz frequencies without changing physical antenna hardware.",
        "Using electromagnetically induced transparency and Autler-Townes optical splitting, counter-propagating probe and coupling lasers read out incident RF field amplitudes directly through quantum optical transmission peaks. Because a miniature glass vapor cell contains zero conductive metallic components, it creates no scattered radar signature, cannot be burned out by high-power electromagnetic pulses, and delivers unprecedented dynamic range for intercepting frequency-hopping military waveforms.",
        "This revolutionary leap in microwave interception unlocks capabilities that Soviet cryptanalysts and signals intelligence operatives could only dream of during the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has disclosed, microwave signal harvesting formed the backbone of the Kremlin’s premier intelligence collection against the United States.",
        "According to Shvets, the KGB’s Eighth Chief Directorate—tasked with cryptanalysis and signals interception—and the Sixteenth Directorate deployed massive microwave intercept grids across Soviet embassies and specialized listening posts. Most infamously, Soviet intelligence bathed the United States Embassy in Moscow with targeted microwave beams to activate passive resonant cavities, intercept internal teletype traffic, and monitor encrypted communications. Shvets revealed that Soviet technical divisions struggled constantly with thermal drift and receiver noise in classical copper waveguides—engineering limitations that Rydberg quantum vapor cells completely eliminate today.",
        "From KGB resonant cavity bugging arrays in Cold War Moscow to modern optical Rydberg atomic sensors intercepting sub-terahertz military telemetry, the quantum spectrum domain has eliminated the classical antenna. Track the Autler-Townes splitting, monitor the rubidium vapor cells, and keep your signals locked. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="rydberg_electrometry", title=EPISODE_DATA["title"])
    img.save(IMG_EP148, "WEBP", quality=92)
    print(f"Saved: {IMG_EP148}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP148, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP148,
        IMG_STUDIO,
        IMG_EP148,
        IMG_REX,
        IMG_EP148,
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
    manifest["updated"] = "2026-10-06T17:30:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
