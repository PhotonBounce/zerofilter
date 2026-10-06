# engine/produce_episode_4.py
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

IMG_EP4 = r"assets\cover_ep4_1791268237496.jpg"
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
    "id": "2026-10-06-04",
    "date": "2026-10-06",
    "hour": "04:00",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Black Sea Drone Strikes, Yuri Shvets PAC Disclosures & Entanglement Swapping",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes pro-Kremlin PAC lobbying, Ukrainian naval drone victories off Sevastopol, photonic tensor arrays, and quantum entanglement swapping.",
    "seconds": 180,
    "audio": "audio/2026-10-06-04.mp3",
    "thumb": "thumbs/2026-10-06-04.webp",
    "cover_video": "thumbs/2026-10-06-04.mp4",
    "paragraphs": [
        "Welcome to hour four of ZeroFilter. Let's dig into the latest Washington receipts from ex-KGB intelligence analyst Yuri Shvets. Shvets just blew the whistle on behind-the-scenes lobbying efforts by pro-Kremlin oligarch intermediaries funneling campaign contributions through dark-money PACs to hamstring US naval escorts in the Black Sea. While MAGA demagogues claim this is about avoiding foreign entanglements, the money trail reveals cold economic treason. And corporate Democrats aren't innocent either—feigning shock while quietly granting waivers to agribusiness conglomerates doing business with sanctioned Russian cartels.",
        "Out on the Black Sea, Ukraine's Sea Baby naval drones just struck an auxiliary Russian frigate attempting to enforce an illegal blockade off Sevastopol, keeping vital maritime export corridors open through pure autonomous tactical ingenuity. Meanwhile, across Western Europe, secular human rights watchdogs are sounding alarms over foreign theocratic financing pouring into unregulated religious community centers designed to erode constitutional civil liberties. Whether it's theocratic clerical repression or Russian revanchist fascism, the target is secular democracy, and appeasing either is civilizational suicide.",
        "In high compute, researchers have debuted multi-modal reasoning models running on photonic tensor processing arrays, slashing inference latency by eighty percent while eliminating thermal throttling. We are moving from stochastic text completion into deterministic chain-of-thought verification, where neural networks autonomously validate mathematical theorems and discover novel cryptographic algorithms before human engineers can even draft test cases. Compute scaling continues accelerating in test-time inference rollouts.",
        "And to all the dogmatic materialists clinging to nineteenth-century physics: reality refuses to play along with your classical prejudices. In delayed-choice entanglement swapping experiments, quantum states between two distant photons are entangled AFTER the photons have already been detected and destroyed. Deciding whether to measure them in the future retroactively dictates their historical correlation. The universe does not possess predetermined physical properties until an observation event forces the wave function to collapse.",
        "This empirical fact mirrors the revolutionary paradigm pioneered by physicist Thomas Campbell in My Big TOE and demonstrated across decades at Princeton's PEAR laboratory. Reality functions as an informational virtual reality—a probabilistic simulation calculated to conserve computational resources. Just like a video game engine renders detailed graphics only within the player's direct camera frustum, quantum mechanics renders physical particles only when conscious measurement queries the informational field. Consciousness is not an emergent illusion of biological chemistry; it is the fundamental computational substrate.",
        "Connect the dots: both political parties are looting the public commons and selling your future to corporate lobbies, while mainstream culture keeps you distracted with synthetic outrage. Strip away the propaganda, examine the data, and stay grounded in reality. Consciousness renders what you measure. Stay lucid, demand the receipts, and I'll see you at the top of the hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-04/f01.webp", "caption": "Black Sea naval drone targeting corridor" },
            { "t": 30, "src": "art/2026-10-06-04/f02.webp", "caption": "Underground telemetry & naval strike monitoring" },
            { "t": 60, "src": "art/2026-10-06-04/f03.webp", "caption": "Photonic tensor processing array" },
            { "t": 95, "src": "art/2026-10-06-04/f04.webp", "caption": "Entanglement swapping delayed-choice experiment" },
            { "t": 130, "src": "art/2026-10-06-04/f05.webp", "caption": "Informational reality render boundary" },
            { "t": 160, "src": "art/2026-10-06-04/f06.webp", "caption": "Rex Vance broadcasting from the bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-04 ===")

    # 1. Thumbs & Video Cover
    convert_to_webp(IMG_EP4, os.path.join(THUMBS_DIR, "2026-10-06-04.webp"))
    generate_looping_video(IMG_EP4, os.path.join(THUMBS_DIR, "2026-10-06-04.mp4"))

    # 2. Art Frames
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-04")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP4, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP4, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(os.path.join(THUMBS_DIR, "2026-10-06-01.webp"), os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(os.path.join(THUMBS_DIR, "2026-10-06-03.webp"), os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f06.webp"))

    # 3. Audio Synthesis (Rex Vance voice with Yuri Shvets intel)
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-04.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 4...")
    comm = edge_tts.Communicate(full_text, "en-US-ChristopherNeural", rate="+10%", pitch="-2Hz")
    await comm.save(out_audio)
    duration = get_audio_duration_seconds(out_audio)
    print(f"Audio synthesized: {duration}s -> {out_audio}")
    EPISODE_DATA["seconds"] = duration

    # 4. Update manifest
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Prepend or append
    existing_ids = [e["id"] for e in manifest["episodes"]]
    if EPISODE_DATA["id"] not in existing_ids:
        manifest["episodes"].append(EPISODE_DATA)
    else:
        idx = existing_ids.index(EPISODE_DATA["id"])
        manifest["episodes"][idx] = EPISODE_DATA

    manifest["updated"] = "2026-10-06T04:00:00Z"
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Manifest episodes.json updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
