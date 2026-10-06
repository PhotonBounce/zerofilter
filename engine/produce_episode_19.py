# engine/produce_episode_19.py
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

IMG_EP19 = os.path.join(THUMBS_DIR, "2026-10-06-19.webp")
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
    "id": "2026-10-06-19",
    "hour": "19:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Red Sea Asymmetric Drone Blockades, Iranian Guidance Telemetry & Axis Barter Pacts",
    "subject": "Hourly uncensored breakdown: Yuri Shvets analyzes the Iranian-Russian military drone barter pipeline, Houthi anti-ship ballistic missile targeting telemetry in the Bab el-Mandeb strait, and Western multi-million-dollar interceptor cost asymmetry.",
    "script_paragraphs": [
        "ZeroFilter broadcast nineteen. I'm Rex Vance. Twelve percent of global seaborne commerce traverses the Bab el-Mandeb strait at the southern choke point of the Red Sea. Tonight, container vessels and fuel tankers are routing thousands of miles around the Cape of Good Hope, adding weeks of transit time and burning billions in extra bunker fuel. Why? Because a non-state insurgent militia armed with cheap loitering munitions has successfully neutralized Western freedom-of-navigation operations across an entire international maritime highway.",

        "Look closely at the economic mathematics of this engagement. Western naval strike groups—operating Arleigh Burke destroyers and Type 45 escorts—are expending Standard Missile 2 and Aster 30 interceptors that cost anywhere from two to four million dollars per launch. They are firing these multi-million-dollar interceptors against two-thousand-dollar delta-wing drones built with consumer fiberglass and lawnmower engines. That is not defense; that is financial attrition. No navy on Earth possesses deep enough magazine capacity to sustain that exchange ratio indefinitely.",

        "Former KGB foreign counter-intelligence analyst Yuri Shvets exposes the underlying supply chain connecting the Red Sea to the Ukrainian front: the Moscow-Tehran military barter axis. Tehran did not build this precision maritime targeting grid in isolation. Russian military intelligence operates signals collection platforms and electronic reconnaissance suites that pass real-time commercial vessel transponder data directly to Iranian proxy operators, enabling precise kinetic targeting while keeping Iranian and Russian fingerprints formally obscured.",

        "In exchange, Yuri Shvets reveals the reciprocal payoff: Iran delivers thousands of Shahed-136 loitering munitions and licenses local assembly lines inside Russia's Tatarstan region in the Alabuga special economic zone. Russia, in return, transfers advanced Su-35 air superiority fighters, electronic warfare pods, and satellite reconnaissance feeds to Tehran. This is not ideological alliance; this is cynical, transactional barter between isolated authoritarian regimes seeking to divide and exhaust Western defense resources across multiple theaters.",

        "The response from Western defense establishments has been predictably sluggish—relying on legacy multi-billion-dollar exquisite platforms rather than deploying rapid asymmetric counter-measures. To permanently break a drone blockade, you do not shoot three-million-dollar missiles into empty sky. You deploy high-power microwave energy suites, autonomous containerized interceptor drones costing pennies on the dollar, and you interdict the Iranian smuggling dhows carrying guidance electronics before they reach Yemen's coast.",

        "Yuri Shvets' intelligence synthesis cuts to the essential geopolitical core: when an adversary realizes your defense costs a thousand times more than their offense, they will bleed your magazines dry without ever fighting a fleet engagement. The West must abandon obsolete twentieth-century naval dogma and adapt to decentralized, software-defined autonomous warfare. I'm Rex Vance. Track the trade choke points, calculate the real exchange ratios, and never confuse armor for strategic victory."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Bab el-Mandeb Maritime Choke Point & Commercial Divert"},
        {"time": 30, "frame": "f02.webp", "caption": "Asymmetric Interceptor Cost Exchange Ratio Telemetry"},
        {"time": 62, "frame": "f03.webp", "caption": "Yuri Shvets on Moscow-Tehran Military Barter Axis"},
        {"time": 95, "frame": "f04.webp", "caption": "Alabuga Shahed-136 Assembly Lines & Su-35 Transfers"},
        {"time": 125, "frame": "f05.webp", "caption": "High-Power Microwave & Directed Energy Drone Countermeasures"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Red Sea Naval Telemetry Synthesis"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP19, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP19,
        IMG_REX,
        IMG_EP19,
        IMG_STUDIO,
        IMG_EP19,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 19...")
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
