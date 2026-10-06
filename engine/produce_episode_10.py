# engine/produce_episode_10.py
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

IMG_EP10 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep10_1791270338167.jpg"
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
    "id": "2026-10-06-10",
    "date": "2026-10-06",
    "hour": "10:00",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Donald Hoffman's Perception Interface, KGB Deception Architecture & Neuro-Quantum Resonance",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Soviet Service A active measures, Donald Hoffman's Fitness Beats Truth theorem, Ukrainian kinetic kill telemetry vs media narratives, and 40Hz gamma entrainment.",
    "seconds": 180,
    "audio": "audio/2026-10-06-10.mp3",
    "thumb": "thumbs/2026-10-06-10.webp",
    "cover_video": "thumbs/2026-10-06-10.mp4",
    "paragraphs": [
        "Welcome to hour ten of ZeroFilter. Let's dissect the architecture of cognitive warfare with former KGB foreign counter-intelligence analyst Yuri Shvets. Shvets documented how Soviet Service A engineered entire synthetic reality bubbles designed to trap Western academic and political elites inside curated perceptual cul-de-sacs. Fast-forward to today's algorithmic feed architectures, and that Soviet doctrine has been fully automated: social media algorithms intentionally exploit human evolutionary cognitive vulnerabilities, trapping millions inside polarized outrage loops where emotion completely eclipses verifiable physical data. If you don't actively audit your information intake, your perception is being manufactured by hostile intelligence operatives and corporate ad brokers.",
        "Examine the real-world consequence on the Ukrainian battlefield: television pundits endlessly debate manufactured diplomatic talking points about territorial concessions, completely ignoring the hard physical receipts. Frontline telemetry confirms that Russian mechanized assaults are losing seventy percent of their armored vehicles to precision FPV drone strikes within four hundred meters of crossing the departure line. Authoritarian regimes manufacture loud psychological narratives precisely to conceal their catastrophic kinetic losses. In warfare, narrative is cheap; physics and industrial attrition are absolute.",
        "Now look at cognitive science at the deepest mathematical level: cognitive psychologist Donald Hoffman's Interface Theory of Perception. Through rigorous evolutionary game theory simulations, Hoffman demonstrated the Fitness Beats Truth theorem: the mathematical probability that natural selection shaped our sensory organs to perceive objective reality as it truly is, is precisely zero. Space, time, and physical objects are not fundamental reality; they are a 3D desktop user interface designed to hide the overwhelming informational complexity of the cosmos. Treating physical matter as fundamental reality is like confusing a desktop trashcan icon for the physical CPU logic gates inside your computer.",
        "In cutting-edge neural engineering, clinical researchers are deploying high-density closed-loop transcranial magnetic entrainment. By synchronizing forty-hertz gamma-band oscillations across the prefrontal cortex, these neuromodulation protocols break through dopamine-conditioned ideological rigidities, instantly restoring autonomous cognitive processing and perceptual lucidity in subjects trapped in algorithmic echo chambers.",
        "This is exactly why state propagandists and corporate media cartels are terrified of genuine cognitive freedom. If consciousness is the fundamental informational network from which physical space-time is rendered, then authoritarian systems possess zero fundamental power over you. Their authority exists solely inside the sensory desktop illusion they manipulate.",
        "Shut off their manufactured noise. Question the interface icons, follow the empirical data, and reclaim your conscious sovereignty. Reality is not what they project onto your screens; reality is the conscious observer experiencing the data. Stay analytical, stay lucid, and I will see you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-10/f01.webp", "caption": "KGB Service A active measures and algorithmic echo chambers" },
            { "t": 35, "src": "art/2026-10-06-10/f02.webp", "caption": "Frontline kinetic attrition telemetry vs media talking points" },
            { "t": 72, "src": "art/2026-10-06-10/f03.webp", "caption": "Donald Hoffman Fitness Beats Truth perception interface" },
            { "t": 110, "src": "art/2026-10-06-10/f04.webp", "caption": "40Hz gamma entrainment closed-loop neural headset" },
            { "t": 142, "src": "art/2026-10-06-10/f05.webp", "caption": "Conscious agent hyper-dimensional geometric manifold" },
            { "t": 165, "src": "art/2026-10-06-10/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-10 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-10.webp")
    convert_to_webp(IMG_EP10, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-10.mp4")
    generate_looping_video(IMG_EP10, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-10")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP10, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP10, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP10, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP10, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-10.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 10...")
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
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-10"]
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
