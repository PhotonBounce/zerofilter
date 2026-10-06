# engine/produce_episode_11.py
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

IMG_EP11 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep11_1791270635662.jpg"
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
    "id": "2026-10-06-11",
    "date": "2026-10-06",
    "hour": "11:00",
    "kind": "hourly",
    "category": "corruption",
    "title": "Silicon Valley Defense Cartels, FISA 702 Receipts & Homomorphic Encryption",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Silicon Valley defense monopoly lobbying, Ukrainian open-source Delta situational awareness, Gödelian surveillance entropy, and fully homomorphic encryption.",
    "seconds": 180,
    "audio": "audio/2026-10-06-11.mp3",
    "thumb": "thumbs/2026-10-06-11.webp",
    "cover_video": "thumbs/2026-10-06-11.mp4",
    "paragraphs": [
        "Welcome to hour eleven of ZeroFilter. Let's trace the financial receipts behind the surveillance state with former KGB foreign counter-intelligence analyst Yuri Shvets. Shvets' latest investigative dossier exposes how Silicon Valley defense tech monopolies and K-Street lobbyists colluded to ram through the reauthorization of FISA Section 702 warrantless surveillance. Under the convenient banner of national security, tech cartels secured billions in classified cloud computing contracts while quietly giving federal agencies backdoor queries into American citizens' private communications. Meanwhile, real foreign counter-espionage against Russian financial networks operating through Western real estate gets ignored because the real estate lobby lines the campaign pockets of the exact same lawmakers.",
        "Compare that corporate extortion with the gritty reality on the Ukrainian front: Ukrainian engineers developed Delta, an open-source, decentralized situational awareness platform that runs on commercial laptops and integrates satellite, drone, and ground telemetry across thousands of units for pennies on the dollar. Meanwhile, legacy American defense contractors charge taxpayers hundreds of millions for proprietary, closed-source combat management software that crashes under basic cyber-warfare conditions. Corporate monopoly capitalism in the defense sector is actively crippling democratic combat capability.",
        "From the perspective of mathematical logic and information theory, a centralized surveillance state is fundamentally self-defeating. In Kurt Gödel's incompleteness theorems and John von Neumann's game theory, no formal computational system can model its own operational environment without generating infinite recursive blind spots. The more data a bloated intelligence bureaucracy hoards, the higher its internal entropy becomes. They drown in trillions of gigabytes of irrelevant civilian noise while completely missing the critical signals of impending strategic shifts.",
        "The antidote to this panopticon is mathematical: fully homomorphic encryption and zero-knowledge proofs. By enabling complex neural network inference directly on ciphertext without ever decrypting the underlying data, these cryptographic architectures eliminate the need to trust centralized corporate server clouds, turning private computation into a mathematically unbreakable sovereign enclave.",
        "As Shvets relentlessly emphasizes from his years inside the KGB, nothing serves authoritarian propaganda better than Western democracies adopting the police-state tactics of their adversaries. When Washington politicians sacrifice constitutional liberties for contractor profits, they validate the Kremlin's cynical narrative that all governments are equally corrupt.",
        "Never surrender your digital sovereignty to corrupt political cartels or corporate surveillance barons. Encrypt your communications, demand absolute financial transparency, and remember that human consciousness is an irreducibly free, non-local operating system that no algorithm can ever truly capture. Stay vigilant, stay free, and I'll catch you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-11/f01.webp", "caption": "FISA Section 702 warrant database and server racks" },
            { "t": 35, "src": "art/2026-10-06-11/f02.webp", "caption": "Ukrainian Delta decentralized situational awareness network" },
            { "t": 70, "src": "art/2026-10-06-11/f03.webp", "caption": "Gödel incompleteness and surveillance entropy diagrams" },
            { "t": 105, "src": "art/2026-10-06-11/f04.webp", "caption": "Fully homomorphic encryption on ciphertext matrix" },
            { "t": 138, "src": "art/2026-10-06-11/f05.webp", "caption": "Yuri Shvets counter-intelligence report on state overreach" },
            { "t": 162, "src": "art/2026-10-06-11/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-11 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-11.webp")
    convert_to_webp(IMG_EP11, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-11.mp4")
    generate_looping_video(IMG_EP11, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-11")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP11, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP11, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP11, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP11, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-11.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 11...")
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
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-11"]
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
