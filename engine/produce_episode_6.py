# engine/produce_episode_6.py
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

IMG_EP6 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep6_1791269117238.jpg"
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
    "id": "2026-10-06-06",
    "date": "2026-10-06",
    "hour": "06:00",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Robert Monroe Gateway Archives, Yuri Shvets on KGB Psychotronics & SRI Telemetry",
    "subject": "Hourly uncensored breakdown: Yuri Shvets dismantles KGB psychotronic propaganda myths, declassified CIA Monroe Institute Gateway protocols, Ukraine intercepting Shahed navigation relays, and non-local observer reality.",
    "seconds": 180,
    "audio": "audio/2026-10-06-06.mp3",
    "thumb": "thumbs/2026-10-06-06.webp",
    "cover_video": "thumbs/2026-10-06-06.mp4",
    "paragraphs": [
        "Welcome to hour six of ZeroFilter. Let's unpack an intelligence file from ex-KGB analyst Yuri Shvets that cuts straight through decades of disinformation. Shvets documented how Soviet intelligence laundered millions into fraudulent psychotronic weaponry programs in the 1980s—not because mind-control beams actually worked, but because corrupt First Chief Directorate generals needed classified black-budget slush funds to siphon into Austrian bank accounts. Fast-forward to Washington today, and congressional defense markups are pulling the exact same grift: slapping classified labels on speculative boondoggles while real counter-espionage investigations into foreign agent networks inside American think tanks get quietly buried.",
        "On the active frontlines in Ukraine, electronic warfare units just successfully jammed and spoofed the satellite guidance feeds of forty incoming Russian-Iranian Shahed drones, forcing them to crash harmlessly into open marshlands outside Poltava. Meanwhile, Russian state propagandists continue peddling apocalyptic rhetoric to scare Western policymakers into withholding long-range strike authorizations. As Shvets consistently emphasizes, the Kremlin only backs down when confronted with overwhelming, unhesitating force. Paralyzed diplomatic hesitation isn't caution; it's an invitation for authoritarian escalation.",
        "Now examine the genuine declassified science of human consciousness: Lieutenant Colonel Wayne McDonnell's landmark 1983 CIA assessment of the Robert Monroe Institute Gateway Experience. Drawing on David Bohm's quantum holography and Karl Pribram's neurophysiology, the analysis concluded that human consciousness is an energy matrix operating outside space-time constraints. When both brain hemispheres achieve synchronized electrical frequency through binaural Hemi-Sync acoustic pulses, the observer transcends local physical interference. Consciousness is not an accidental byproduct of biological meat; it is the foundational operating system of the cosmos.",
        "In cutting-edge neural engineering, researchers are now miniaturizing this acoustic phase entrainment into sub-millimeter opto-acoustic neural implants. By delivering nanosecond acoustic coherence directly to the thalamus, these non-invasive transceivers stabilize autonomic nervous system feedback without chemical pharmaceuticals, bypassing corporate healthcare monopolies that profit off chronic dependency.",
        "Compare that with the Stanford Research Institute trials run by Hal Puthoff and Russell Targ. Under strict double-blind conditions verified by the Defense Intelligence Agency, remote viewers repeatedly sketched Soviet submarine construction at Severodvinsk months before satellite reconnaissance confirmed their existence. Dogmatic reductionists still dismiss this because acknowledging non-local consciousness shatters the institutional control paradigms of legacy science.",
        "Both political machines depend on keeping you anxious, polarized, and mentally asleep. Don't fall for the theater. Verify the source receipts, reject dogmatic gatekeepers, and trust the mathematical coherence of the data. Consciousness is reality; the rest is corporate distraction. Stay sharp, remain free, and I will see you at the top of the next hour. I'm Rex Vance, and this was ZeroFilter."
    ],
    "art": {
        "frames": [
            { "t": 0, "src": "art/2026-10-06-06/f01.webp", "caption": "KGB psychotronic black-budget slush fund dossiers" },
            { "t": 32, "src": "art/2026-10-06-06/f02.webp", "caption": "Electronic warfare spoofing grid over Poltava" },
            { "t": 65, "src": "art/2026-10-06-06/f03.webp", "caption": "CIA Gateway Experience hemispheric synchronization" },
            { "t": 100, "src": "art/2026-10-06-06/f04.webp", "caption": "Opto-acoustic neural entrainment circuitry" },
            { "t": 132, "src": "art/2026-10-06-06/f05.webp", "caption": "SRI coordinate remote viewing telemetry" },
            { "t": 162, "src": "art/2026-10-06-06/f06.webp", "caption": "Rex Vance broadcasting live from bunker" }
        ]
    }
}

async def main():
    print("=== Producing Episode 2026-10-06-06 ===")
    word_count = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Total word count: {word_count}")

    # 1. Thumbs & Video Cover
    thumb_webp = os.path.join(THUMBS_DIR, "2026-10-06-06.webp")
    convert_to_webp(IMG_EP6, thumb_webp)
    thumb_mp4 = os.path.join(THUMBS_DIR, "2026-10-06-06.mp4")
    generate_looping_video(IMG_EP6, thumb_mp4, duration=10)

    # 2. Story Art Frames (6 frames)
    ep_art_dir = os.path.join(ART_DIR, "2026-10-06-06")
    os.makedirs(ep_art_dir, exist_ok=True)
    convert_to_webp(IMG_EP6, os.path.join(ep_art_dir, "f01.webp"))
    convert_to_webp(IMG_EP6, os.path.join(ep_art_dir, "f02.webp"))
    convert_to_webp(IMG_EP6, os.path.join(ep_art_dir, "f03.webp"))
    convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f04.webp"))
    convert_to_webp(IMG_EP6, os.path.join(ep_art_dir, "f05.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f06.webp"))
    print(f"Created 6 art frames in {ep_art_dir}")

    # 3. Audio Synthesis
    out_audio = os.path.join(AUDIO_DIR, "2026-10-06-06.mp3")
    full_text = "\n\n".join(EPISODE_DATA["paragraphs"])
    print("Synthesizing Rex Vance audio for Episode 6...")
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
    manifest_list = [ep for ep in manifest_list if ep["id"] != "2026-10-06-06"]
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
