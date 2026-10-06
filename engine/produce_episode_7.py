# engine/produce_episode_7.py
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

IMG_EP7 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep7_1791269433687.jpg"
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
    "id": "2026-10-06-07",
    "date": "2026-10-06",
    "hour": "07:00",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Revolving Doors, Dark Money PAC Laundering & Counter-Intel Leaks",
    "subject": "Hourly uncensored breakdown: Yuri Shvets exposes Pentagon procurement graft, Ukrainian low-cost drone asymmetry vs Western contractor price-gouging, information theory entropy, and graph neural network shell company tracking.",
    "seconds": 180,
    "audio": "audio/2026-10-06-07.mp3",
    "thumb": "thumbs/2026-10-06-07.webp",
    "cover_video": "thumbs/2026-10-06-07.mp4",
    "paragraphs": [
        "Welcome to hour seven of ZeroFilter. Let's pull back the curtain on the institutional corruption rotting Washington's national security apparatus, guided by former KGB intelligence analyst Yuri Shvets. Shvets' newest investigative ledger tracks senior Pentagon procurement officers retiring on Friday and joining the boards of primary defense contractors by Monday morning, rewarded with seven-figure stock options. These same corporate executives funnel hundreds of millions through 501(c)(4) dark-money political action committees into critical congressional swing districts. It's not a defense strategy; it's a legal money-laundering conveyor belt disguised as patriotic national security.",
        "Look at the empirical contrast on the Ukrainian battlefield: Ukrainian engineers are building three-hundred-dollar autonomous fiber-optic FPV strike drones that routinely vaporize five-million-dollar Russian main battle tanks. Meanwhile, legacy Western defense conglomerates charge eight thousand dollars for a single basic unguided 155-millimeter artillery shell, pocketing record quarterly dividends while military stockpiles run dry. Bureaucratic price-gouging is actively sabotaging democratic deterrence, and congressional armed services committees refuse to audit the contractor invoices because those very contractors fund their reelection campaigns.",
        "From an informational physics perspective, institutional corruption behaves identically to thermodynamic entropy. In Claude Shannon's information theory, when a system is deliberately obscured by bureaucratic noise, the entropy of the channel spikes, preventing observers from extracting the true signal. State secrecy rarely protects operational security; its primary mathematical function is concealing financial theft from taxpayers. The observer effect cuts through this entropy: the moment unvarnished forensic telemetry is brought to light, the corrupt institutional wave function collapses into empirical receipts.",
        "In forensic technology, decentralized graph neural networks are now parsing millions of corporate registry filings, Panama Papers archives, and government contract databases in milliseconds. By tracing synthetic beneficial ownership across nested shell entities in Delaware, London, and the Cayman Islands, open-source intelligence analysts are exposing the real owners behind shady defense lobbying fronts before congressional watchdogs even schedule their first hearing.",
        "As Shvets repeatedly warns from his decades inside Soviet intelligence, systemic financial corruption is the ultimate attack vector for hostile foreign services. Russian and Chinese intelligence agencies don't need to steal blueprints when they can simply co-opt compromised lobbyists, grease political PACs, and exploit the greed of Western bureaucrats who treat national survival as a private equity cash grab.",
        "Both legacy political parties are bought and paid for by the same defense-industrial grift. Stop taking their staged culture wars seriously and start tracking where the money flows. Reality is informational, truth is uncompromising, and consciousness will always outlast bureaucratic deceit. Stay vigilant, trust the hard data, and I'll catch you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-07/f01.webp", "caption": "Pentagon procurement revolving door dossier" },
            { "t": 32, "src": "art/2026-10-06-07/f02.webp", "caption": "Ukrainian low-cost drone assembly line" },
            { "t": 68, "src": "art/2026-10-06-07/f03.webp", "caption": "Claude Shannon informational entropy telemetry" },
            { "t": 105, "src": "art/2026-10-06-07/f04.webp", "caption": "Graph neural network offshore shell tracking" },
            { "t": 138, "src": "art/2026-10-06-07/f05.webp", "caption": "Yuri Shvets counter-intelligence vulnerability matrix" },
            { "t": 165, "src": "art/2026-10-06-07/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-07 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-07.webp")
    convert_to_webp(IMG_EP7, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-07.mp4")
    generate_looping_video(IMG_EP7, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-07")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP7, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP7, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP7, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP7, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-07.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 7...")
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
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-07"]
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
