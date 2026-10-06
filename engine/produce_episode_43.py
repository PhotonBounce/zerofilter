# engine/produce_episode_43.py
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

IMG_EP43 = os.path.join(THUMBS_DIR, "2026-10-07-19.webp")
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
    "id": "2026-10-07-19",
    "hour": "19:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Monroe Gateway Hemi-Sync Archives, Frequency Following & Soviet Psychotronic Telemetry",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the Robert Monroe Gateway Experience, binaural frequency following response in hemispheric synchronization, and Yuri Shvets's insider analysis of Soviet KGB psychotronic programs and Kiev remote observation laboratories.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is nineteen hundred hours. In 1983, the Central Intelligence Agency declassified a comprehensive operational assessment of the Monroe Institute's Gateway Experience. Spearheaded by radio executive turned consciousness researcher Robert Monroe, the protocol utilized hemispheric synchronization, or Hemi-Sync, to alter human brainwave states through acoustic neuromodulation. By introducing slightly differentiated audio frequencies to each ear—such as one hundred hertz in the left and one hundred four hertz in the right—the brain's superior olivary nucleus computes the differential, entraining both cortical hemispheres into a synchronized four-hertz theta frequency following response.",
        "Monroe categorized these calibrated mental architectures into distinct Focus levels. Participants systematically advanced from Focus 10, characterized as mind awake and body asleep, to Focus 12, an expanded spatial awareness beyond physical sensory input, and ultimately Focus 15, an apparent state of non-temporal consciousness. Army intelligence officers deployed to Virginia documented profound perceptual anomalies, including localized out-of-body experiences and non-local coordinate viewing, suggesting that human consciousness operates as an entangled quantum holographic receiver rather than a purely closed neurochemical computer.",
        "Across the Atlantic, Soviet intelligence watched these American neuro-acoustic developments with obsessive paranoia. As former KGB foreign intelligence officer and Washington insider Yuri Shvets has documented, the Soviet security apparatus poured millions of rubles into psychotronic and bio-resonance warfare throughout the 1970s and 1980s. Operating out of classified laboratories in Moscow, Novosibirsk, and Kiev, Soviet researchers sought to harness altered mental states for strategic intelligence gathering, attempting to remotely observe American military installations and intercontinental ballistic missile silos.",
        "According to Shvets, while Soviet military leadership genuinely feared American consciousness-projection breakthroughs, the KGB's internal psychotronics division devolved into a massive, unregulated slush fund. Charismatic researchers and state-sanctioned psychics extracted endless defense allocations by promising mind-control frequencies and remote telepathic sabotage. Soviet counter-intelligence operatives eventually realized that much of the domestic psychotronic telemetry was pseudoscientific deception designed to siphon state capital, mirroring the exact bureaucratic grift afflicting conventional defense procurement.",
        "Yet beneath the bureaucratic fraud, the underlying biophysics of acoustic neural entrainment remains experimentally verified. Clinical electroencephalography confirms that binaural coherence alters cortical phase locking, alters default mode network activity, and induces deep parasympathetic dominance. The real battlefield is not mystical telepathy; it is cognitive sovereignty in an era where synthetic acoustic frequencies, digital algorithms, and sensory feeds continually manipulate human neural states.",
        "Synchronize your hemispheres, audit the archives, and maintain absolute signal clarity against algorithmic conditioning. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="gateway_hemisync")
    img.save(IMG_EP43, "WEBP", quality=92)
    print(f"Saved: {IMG_EP43}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP43, output_mp4, duration=10)
    
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
        IMG_EP43,
        IMG_REX,
        IMG_EP43,
        IMG_STUDIO,
        IMG_EP43,
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
