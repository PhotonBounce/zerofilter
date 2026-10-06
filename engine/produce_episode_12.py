# engine/produce_episode_12.py
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

IMG_EP12 = r"assets\cover_ep12_1791270940111.jpg"
IMG_REX = os.path.join(WEB_DIR, "assets", "rex_vance.webp")
IMG_STUDIO = os.path.join(WEB_DIR, "assets", "studio_bunker.webp")

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def convert_to_webp(src_path, dst_path, quality=90):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with Image.open(src_path) as im:
        im.save(dst_path, "WEBP", quality=quality)
    print(f"Saved WebP: {dst_path}")

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
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"FFmpeg error: {res.stderr}")
    else:
        print(f"Generated 10s Looping Cover: {output_mp4}")

def get_audio_duration_seconds(audio_path):
    cmd = [FFMPEG_EXE, "-i", audio_path, "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    import re
    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return round(int(h) * 3600 + int(m) * 60 + float(s))
    return 180

EPISODE_DATA = {
    "id": "2026-10-06-12",
    "date": "2026-10-06",
    "hour": "12:00",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Taiwan Strait Hellscape Doctrine, Beijing-Moscow Axis & EUV Chokepoints",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Beijing-Moscow strategic coordination, INDOPACOM autonomous Hellscape defense doctrine, TSMC EUV lithography chokepoints, and rare-earth supply chain weaponization.",
    "seconds": 180,
    "audio": "audio/2026-10-06-12.mp3",
    "thumb": "thumbs/2026-10-06-12.webp",
    "cover_video": "thumbs/2026-10-06-12.mp4",
    "paragraphs": [
        "Welcome to hour twelve of ZeroFilter. Let's examine the supreme geopolitical fault line of the twenty-first century with former KGB foreign counter-intelligence analyst Yuri Shvets. Shvets' newest strategic brief exposes the cold transactional mechanics behind Beijing and Moscow's intelligence axis. Xi Jinping treats Vladimir Putin not as an equal partner, but as an expendable battering ram sent to exhaust Western military stockpiles and test American political stamina. Congressional politicians who preach isolationism under the cowardly banner of domestic priority are handing Beijing an open invitation: every hesitation on the Ukrainian front is interpreted in Beijing as a green light for an amphibious blockade of Taiwan.",
        "Look at the operational counter-strategy being deployed across the hundred-mile Taiwan Strait: the United States Indo-Pacific Command's Hellscape doctrine. The moment Chinese amphibious assault ships depart naval berths in Fujian, thousands of autonomous uncrewed surface vessels, loitering strike drones, and smart acoustic sea mines activate simultaneously. By turning the maritime strait into a self-organizing autonomous kill-zone, Taiwan and allied forces eliminate the need for costly carrier strike groups to enter the anti-ship missile envelope, neutralizing numerical invasion forces through radical low-cost asymmetry.",
        "At the fundamental physical layer, global economic civilization rests on an astonishingly fragile material chokepoint: ASML's extreme ultraviolet photolithography mirrors, polished to tolerances narrower than a single silicon atom, operating inside TSMC's fabrication cleanrooms in Hsinchu. Combine that with Beijing's monopolistic chokehold on neodymium and dysprosium rare-earth refining, and you realize that modern microchip computing is not an abstract cloud; it is a precarious thermodynamic miracle tethered to a vulnerable geographic coastline.",
        "In advanced naval engineering, uncrewed submersible motherships are now deploying wake-homing passive acoustic torpedoes. Communicating via blue-green laser satellite links and low-frequency magnetometers, these autonomous underwater sentinels track submarine acoustic signatures without emitting active sonar pings, operating with total acoustic stealth inside contested littoral channels.",
        "As Shvets relentlessly reminds us, totalitarian regimes understand only one dialect: the credible threat of catastrophic physical defeat. The Soviet Union didn't collapse because of diplomatic summit platitudes; it collapsed because it went bankrupt trying to match Western technological superiority. Appeasement never buys peace; it merely finances the next invasion.",
        "Reject the defeatist narratives of compromised politicians who want you to believe totalitarian victory is inevitable. The data proves otherwise. Stand firm for human liberty, audit the supply-chain receipts, and remember that conscious courage is the ultimate asymmetric weapon. Stay sharp, remain free, and I will catch you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-12/f01.webp", "caption": "Beijing-Moscow strategic intelligence dialogue matrix" },
            { "t": 35, "src": "art/2026-10-06-12/f02.webp", "caption": "INDOPACOM Taiwan Strait autonomous drone barrier net" },
            { "t": 72, "src": "art/2026-10-06-12/f03.webp", "caption": "TSMC EUV photolithography sub-atomic mirror optics" },
            { "t": 108, "src": "art/2026-10-06-12/f04.webp", "caption": "Autonomous submersible acoustic wake-homing torpedoes" },
            { "t": 140, "src": "art/2026-10-06-12/f05.webp", "caption": "Yuri Shvets analysis on totalitarian bankruptcies" },
            { "t": 165, "src": "art/2026-10-06-12/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-12 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-12.webp")
    convert_to_webp(IMG_EP12, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-12.mp4")
    generate_looping_video(IMG_EP12, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-12")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP12, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP12, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP12, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP12, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-12.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 12...")
    communicate = edge_tts.Communicate(
        text=full_text,
        voice="en-US-ChristopherNeural",
        rate="+10%",
        pitch="-2Hz"
    )
    await communicate.save(out_audio)
    actual_duration = get_audio_duration_seconds(out_audio)
    print(f"Audio synthesized: {actual_duration}s -> {out_audio}")
    EPISODE_DATA["seconds"] = actual_duration

    # 4. Manifest Update
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    manifest_list = manifest.get("episodes", manifest)
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-12"]
    manifest_list.insert(0, EPISODE_DATA)

    if isinstance(manifest, dict) and "episodes" in manifest:
        manifest["episodes"] = manifest_list
        data_to_write = manifest
    else:
        data_to_write = manifest_list

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(data_to_write, f, indent=2)

    print("Manifest episodes.json updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
