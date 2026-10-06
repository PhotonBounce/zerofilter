# engine/produce_pilot_releases.py
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
ASSETS_DIR = os.path.join(WEB_DIR, "assets")
ART_DIR = os.path.join(WEB_DIR, "art")
DATA_DIR = os.path.join(WEB_DIR, "data")
MANIFEST_FILE = os.path.join(DATA_DIR, "episodes.json")

# Artifact image paths from brain
IMG_REX = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\rex_vance_portrait_1791259648813.jpg"
IMG_STUDIO = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\zerofilter_studio_bunker_1791259662454.jpg"
IMG_EP1 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep1_1791259677227.jpg"
IMG_EP2 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep2_1791259694910.jpg"
IMG_EP3 = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep3_1791259708337.jpg"

FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def convert_to_webp(src_path, dst_path, quality=90):
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with Image.open(src_path) as im:
        im.save(dst_path, "WEBP", quality=quality)
    print(f"Saved WebP: {dst_path}")

def generate_looping_video(image_path, output_mp4, duration=10):
    os.makedirs(os.path.dirname(output_mp4), exist_ok=True)
    # 10s subtle slow push-in zoompan with smooth fade in/out loop
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
        print(f"FFmpeg error for {output_mp4}: {res.stderr}")
    else:
        print(f"Generated 10s Looping Cover: {output_mp4}")

def get_audio_duration_seconds(audio_path):
    cmd = [
        FFMPEG_EXE,
        "-i", audio_path,
        "-f", "null",
        "-"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    # Parse time from ffmpeg output: time=00:02:45.12
    import re
    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return round(int(h) * 3600 + int(m) * 60 + float(s))
    return 180

async def synthesize_all_episodes():
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    for ep in manifest["episodes"]:
        ep_id = ep["id"]
        out_audio = os.path.join(WEB_DIR, ep["audio"])
        os.makedirs(os.path.dirname(out_audio), exist_ok=True)
        print(f"Synthesizing Rex Vance audio for [{ep_id}]...")
        full_text = "\n\n".join(ep["paragraphs"])
        # Fast, energetic delivery with baritone depth
        comm = edge_tts.Communicate(full_text, "en-US-ChristopherNeural", rate="+10%", pitch="-2Hz")
        await comm.save(out_audio)
        duration = get_audio_duration_seconds(out_audio)
        print(f"Synthesized [{ep_id}]: {duration}s -> {out_audio}")
        ep["seconds"] = duration

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("Updated episodes.json with exact audio durations.")

def build_art_frames():
    """Populates synchronized story frames for each episode."""
    ep_images = {
        "2026-10-06-01": IMG_EP1,
        "2026-10-06-02": IMG_EP2,
        "2026-10-06-03": IMG_EP3
    }
    
    for ep_id, cover_src in ep_images.items():
        ep_art_dir = os.path.join(ART_DIR, ep_id)
        os.makedirs(ep_art_dir, exist_ok=True)
        
        # Frame 1: Cover / Main theme
        convert_to_webp(cover_src, os.path.join(ep_art_dir, "f01.webp"))
        # Frame 2: Studio / Radar telemetry
        convert_to_webp(IMG_STUDIO, os.path.join(ep_art_dir, "f02.webp"))
        # Frame 3: Tech focus
        convert_to_webp(cover_src, os.path.join(ep_art_dir, "f03.webp"))
        # Frame 4: Anomaly / Apparatus
        convert_to_webp(IMG_EP2 if ep_id != "2026-10-06-02" else IMG_EP1, os.path.join(ep_art_dir, "f04.webp"))
        # Frame 5: Simulation / Reality Matrix
        convert_to_webp(IMG_EP3 if ep_id != "2026-10-06-03" else IMG_STUDIO, os.path.join(ep_art_dir, "f05.webp"))
        # Frame 6: Host Rex Vance in bunker
        convert_to_webp(IMG_REX, os.path.join(ep_art_dir, "f06.webp"))
        print(f"Generated 6 story frames for {ep_id}")

def main():
    print("=== Processing ZeroFilter Assets & Releases ===")
    
    # 1. Assets
    convert_to_webp(IMG_REX, os.path.join(ASSETS_DIR, "rex_vance.webp"))
    convert_to_webp(IMG_STUDIO, os.path.join(ASSETS_DIR, "studio_bunker.webp"))
    
    # 2. Episode covers
    convert_to_webp(IMG_EP1, os.path.join(THUMBS_DIR, "2026-10-06-01.webp"))
    convert_to_webp(IMG_EP2, os.path.join(THUMBS_DIR, "2026-10-06-02.webp"))
    convert_to_webp(IMG_EP3, os.path.join(THUMBS_DIR, "2026-10-06-03.webp"))
    
    # 3. 10s Looping Video Covers
    generate_looping_video(IMG_EP1, os.path.join(THUMBS_DIR, "2026-10-06-01.mp4"))
    generate_looping_video(IMG_EP2, os.path.join(THUMBS_DIR, "2026-10-06-02.mp4"))
    generate_looping_video(IMG_EP3, os.path.join(THUMBS_DIR, "2026-10-06-03.mp4"))
    
    # 4. Story Art frames
    build_art_frames()
    
    # 5. Rex Vance Audio Synthesis
    asyncio.run(synthesize_all_episodes())
    
    print("=== All Pilot Releases Successfully Produced! ===")

if __name__ == "__main__":
    main()
