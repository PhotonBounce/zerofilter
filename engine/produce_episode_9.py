# engine/produce_episode_9.py
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

IMG_EP9 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep9_1791270025386.jpg"
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
    "id": "2026-10-06-09",
    "date": "2026-10-06",
    "hour": "09:00",
    "kind": "hourly",
    "category": "quantum",
    "title": "Delayed-Choice Quantum Eraser, Wheeler's Smoky Dragon & SIGINT Interceptions",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Russian tactical communications lapses, Ukrainian cognitive SDR spectrum monitoring, the delayed-choice quantum eraser retrocausality proofs, and Wheeler's participatory universe.",
    "seconds": 180,
    "audio": "audio/2026-10-06-09.mp3",
    "thumb": "thumbs/2026-10-06-09.webp",
    "cover_video": "thumbs/2026-10-06-09.mp4",
    "paragraphs": [
        "Welcome to hour nine of ZeroFilter. Let's start with a signals intelligence breakdown from ex-KGB foreign intelligence analyst Yuri Shvets. Shvets' newest investigation details how Five Eyes SIGINT arrays systematically penetrate high-level Russian military command communications. While Moscow spends billions claiming its tactical networks are cryptographically impenetrable, frontline Russian commanders routinely bypass their own secure protocols to use civilian radio handsets and commercial messaging apps. That operational laziness allowed Western electronic intelligence to map Russian general staff headquarters and feed precision coordinates directly to Ukrainian artillery batteries in real-time. In modern warfare, bad communications discipline is an immediate death sentence.",
        "Across the frontline, Ukrainian software engineers have deployed autonomous cognitive software-defined radio interceptors along the entire seven-hundred-mile contact line. These low-cost cognitive arrays scan gigahertz of spectrum per millisecond, using onboard machine learning models to identify frequency-hopping Russian drone telemetry and pinpoint the launch crews within seconds. Meanwhile, legacy Western procurement committees take eighteen months just to review paperwork for basic field radios. In an existential war of electronic adaptation, bureaucratic inertia is actively lethal.",
        "Now confront the profound frontier of quantum mechanics: the Kim, Scully, and Shih delayed-choice quantum eraser. By entangling twin photons through a barium borate crystal and delaying the measurement of which-way information until long after the signal photon has already registered on a detector, physicists proved that measuring or erasing path information in the present retroactively determines whether an interference pattern existed in the past. As John Archibald Wheeler famously formulated with his great smoky dragon metaphor: no elementary quantum phenomenon is a phenomenon until it is an observed phenomenon. The past does not exist as a fixed physical record until observation forces the wave function to crystallize.",
        "In applied physics, quantum engineers have successfully integrated this delayed-choice entanglement onto sub-wavelength silicon-photonic chips. By encoding topological qubits into zero-dispersion optical waveguides, these quantum cryptographic processors establish unhackable key distribution channels where any eavesdropping attempt instantly collapses the quantum state, providing mathematically guaranteed physical security.",
        "This demolishes the outdated classical myth of a mechanistic, pre-rendered clockwork universe. You are not a passive spectator trapped inside an indifferent, predetermined material machine. The universe is fundamentally informational, participatory, and observer-dependent. Consciousness is the active measurement that collapses infinite potential into physical actuality.",
        "Reject the corporate media's attempt to keep your consciousness trapped in anxiety and tribal outrage. Demand the source documents, trust empirical physics over dogmatic ideology, and recognize your power as an observer. The signal is pure; the noise is artificial. Stay analytical, demand the truth, and I'll catch you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-09/f01.webp", "caption": "Five Eyes SIGINT interception array and radio waterfall" },
            { "t": 35, "src": "art/2026-10-06-09/f02.webp", "caption": "Cognitive SDR frequency hopping spectrum mapping" },
            { "t": 72, "src": "art/2026-10-06-09/f03.webp", "caption": "Kim Scully Shih delayed-choice quantum eraser optical table" },
            { "t": 110, "src": "art/2026-10-06-09/f04.webp", "caption": "Sub-wavelength silicon-photonic quantum key chip" },
            { "t": 142, "src": "art/2026-10-06-09/f05.webp", "caption": "Wheeler smoky dragon participatory universe model" },
            { "t": 165, "src": "art/2026-10-06-09/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-09 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-09.webp")
    convert_to_webp(IMG_EP9, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-09.mp4")
    generate_looping_video(IMG_EP9, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-09")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP9, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP9, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP9, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP9, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-09.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 9...")
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
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-09"]
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
