# engine/produce_episode_15.py
import asyncio
import json
import os
import subprocess
from PIL import Image
import imageio_ffmpeg
import edge_tts

ROOT_DIR = r"D:\zerofilter"
WEB_DIR = os.path.join(ROOT_DIR, "web")
THUMBS_DIR = os.path.join(WEB_DIR, "thumbs")
AUDIO_DIR = os.path.join(WEB_DIR, "audio")
ART_DIR = os.path.join(WEB_DIR, "art")
MANIFEST_FILE = os.path.join(WEB_DIR, "data", "episodes.json")

IMG_EP15 = os.path.join(THUMBS_DIR, "2026-10-06-15.webp")
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
    "id": "2026-10-06-15",
    "hour": "15:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Baltic Sea GPS Jamming Corridors, Kremlin Shadow Tankers & Electronic Warfare Countermeasures",
    "subject": "Hourly uncensored breakdown: Yuri Shvets analyzes Kaliningrad Tobol electronic warfare batteries jamming Baltic civil aviation, illicit Russian shadow fleet sanctions-evasion oil tankers, and NATO autonomous counter-EW telemetry.",
    "script_paragraphs": [
        "ZeroFilter broadcast fifteen. I'm Rex Vance. If you're flying commercial airspace anywhere between Helsinki, Tallinn, and Gdansk tonight, your aircraft's primary satellite navigation receiver is flashing intermittent warning flags. Thousands of civilian flights across Northern Europe have reported complete loss of GPS lock, forced to rely on legacy inertial navigation and terrestrial radio beacons. This is not atmospheric turbulence or solar flare interference; this is persistent, offensive electronic warfare radiating straight out of Russia's Kaliningrad enclave.",

        "Former KGB foreign counter-intelligence analyst Yuri Shvets breaks down the operational hardware: Russia's 14214 military unit operating the Tobol and Zhitel electronic warfare complexes near Pionersky. Originally designed as defensive anti-satellite protection systems for ballistic missile command centers, Moscow has turned these high-power directional emitters into an asymmetric bludgeon against European critical infrastructure, testing NATO's response thresholds without firing a single kinetic munition.",

        "Why blanket the Baltic corridor in navigation distortion? Yuri Shvets exposes the dual objective: first, tactical shielding for the Kremlin's illicit shadow fleet. Hundreds of uninsured, rust-bucket crude oil tankers under false flags of convenience traverse these narrow maritime choke points, smuggling sanctioned Russian petroleum to finance Moscow's war effort. By spoofing Automatic Identification System transmitters and blinding civilian tracking satellites, these ghost vessels slip through Danish straits undetected while Western regulators dither.",

        "The second objective is psychological testing—what Yuri Shvets identifies as classic Soviet reflexive control doctrine. By creating an ambient environment of digital friction and civil aviation vulnerability, Moscow projects an illusion of technological invulnerability while measuring the exact latency and political fractures of Baltic and Nordic governments. If the West treats GPS jamming as an acceptable inconvenience rather than a hostile violation of international aviation treaties, the gray-zone perimeter advances.",

        "NATO's counter-strategy, however, is rendering this electronic bullying obsolete. Modern military strike packages and autonomous reconnaissance platforms no longer depend on fragile civilian satellite constellations. Instead, allied forces are deploying quantum gravimetric map-matching and optical landmark correlation engines—guidance suites that operate in total radio silence, completely immune to RF jamming and spoofing pulses.",

        "Here is your bottom-line truth: dictatorships rely on friction, spoofing, and shadows because transparency is fatal to their survival. Yuri Shvets' analysis cuts through the diplomatic noise: you cannot negotiate with gray-zone aggression; you expose the logistics network, seize the ghost tankers, and out-engineer their jamming arrays. I'm Rex Vance. Keep your beacons tuned to raw signal, verify every heading, and never mistake electronic noise for real authority."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Baltic Sea GPS Jamming & Civil Aviation Disruption"},
        {"time": 30, "frame": "f02.webp", "caption": "Kaliningrad Tobol & Zhitel Electronic Warfare Arrays"},
        {"time": 62, "frame": "f03.webp", "caption": "Yuri Shvets on Kremlin Shadow Tanker Fleet Telemetry"},
        {"time": 95, "frame": "f04.webp", "caption": "Reflexive Control Gray-Zone Doctrine & NATO Response"},
        {"time": 125, "frame": "f05.webp", "caption": "Quantum Gravimetric Navigation & Optical Land-Matching"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Baltic SIGINT Summary"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP15, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP15,
        IMG_REX,
        IMG_EP15,
        IMG_STUDIO,
        IMG_EP15,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 15...")
    await synthesize_rex_vance(full_text, mp3_path)

    # 4. Measure duration
    dur = get_audio_duration(mp3_path)
    print(f"Audio synthesized: {dur}s -> {mp3_path}")

    # 5. Update web/data/episodes.json
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    new_ep = {
        "id": EPISODE_DATA["id"],
        "date": EPISODE_DATA["date"],
        "hour": EPISODE_DATA["hour"],
        "kind": EPISODE_DATA["kind"],
        "category": EPISODE_DATA["category"],
        "title": EPISODE_DATA["title"],
        "subject": EPISODE_DATA["subject"],
        "seconds": dur,
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4",
        "paragraphs": EPISODE_DATA["script_paragraphs"],
        "art": {
            "frames": [
                {
                    "t": stem["time"],
                    "src": f"art/{EPISODE_DATA['id']}/{stem['frame']}",
                    "caption": stem["caption"]
                }
                for stem in EPISODE_DATA["art_stems"]
            ]
        }
    }

    manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != new_ep["id"]]
    manifest["episodes"].insert(0, new_ep)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Manifest episodes.json updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
