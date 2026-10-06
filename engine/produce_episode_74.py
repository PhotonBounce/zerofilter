# engine/produce_episode_74.py
import asyncio
import json
import os
import subprocess
from PIL import Image
import imageio_ffmpeg
import edge_tts
from generate_procedural_cover import generate_cover

ROOT_DIR = r"D:\zerofilter"
WEB_DIR = os.path.join(ROOT_DIR, "web")
THUMBS_DIR = os.path.join(WEB_DIR, "thumbs")
AUDIO_DIR = os.path.join(WEB_DIR, "audio")
ART_DIR = os.path.join(WEB_DIR, "art")
MANIFEST_FILE = os.path.join(WEB_DIR, "data", "episodes.json")

IMG_EP74 = os.path.join(THUMBS_DIR, "2026-10-09-02.webp")
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
    "id": "2026-10-09-02",
    "hour": "02:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Red Sea Anti-Ship Ballistic Missile Salvos, Telemetry Relay Spoofing & Soviet Coastal Defense Doctrine",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates anti-ship ballistic missile telemetry spoofing in the Red Sea, terminal seeker evasion, and Yuri Shvets on Soviet asymmetric naval coastal defense doctrine.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero two hundred hours. Over the past twelve months, the Red Sea maritime corridor has become the proving ground for the most significant shift in asymmetric naval warfare since the advent of anti-ship cruise missiles. Anti-ship ballistic missiles, or ASBMs, launched from rugged inland terrain across Yemen, are executing steep terminal dive trajectories toward Western commercial shipping and naval escort strike groups. These munitions combine solid-fuel boost phases with active radio-frequency and electro-optical terminal seekers, collapsing intercept decision windows to less than ninety seconds.",
        "Western carrier strike groups have expended hundreds of multimillion-dollar Standard Missile-2 and SM-6 interceptors to neutralize incoming salvos. However, intelligence signals reveal that regional missile batteries are deploying sophisticated telemetry relay spoofing. By rebroadcasting intercepted Automatic Identification System transponder beacons through commercial satellite uplinks, coastal launch units generate ghost shipping tracks. When Western combat direction systems attempt cooperative engagement, terminal radar locks are pulled toward false target vectors, forcing destroyers to fire high-cost interceptors against phantom decoys while live ASBM warheads descend through the blind clutter.",
        "This tactical architecture is not an indigenous improvisation; it is the direct execution of Soviet asymmetric coastal defense doctrine. Former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented how Soviet military planners recognized in the late 1970s that the USSR could never achieve surface naval parity with the United States Navy. Consequently, Soviet naval doctrine pioneered dense shore-based missile bastions designed to overwhelm carrier strike groups using staggered, multi-axis salvos combined with pervasive electronic deception.",
        "According to Shvets, Soviet intelligence stations in Aden and along the Horn of Africa spent decades mapping Western naval choke points and transferring technical dossiers on coastal radar netted deception to regional proxy networks. Shvets revealed that corrupt Soviet defense procurement bureaucrats and subsequent Russian arms export syndicates systematically leaked missile guidance telemetry algorithms and electro-optical seeker designs abroad. The telemetry spoofing kits observed in the Bab el-Mandeb today trace their design lineage directly to Soviet naval electronic warfare protocols developed in Sevastopol and Leningrad.",
        "Western defense contractors continue to lobby Capitol Hill for expanded cost-plus production contracts for legacy surface combatants, ignoring the harsh economic and physics reality. A two-million-dollar interceptor cannot sustain a war of attrition against fifty-thousand-dollar ballistic munitions coordinated by digital spoofing relays. When coastal defense doctrine pairs cheap kinetic salvos with electronic confusion, multi-billion-dollar supercarriers are effectively excluded from critical maritime choke points.",
        "Audit the Bab el-Mandeb telemetry vectors, trace the Soviet electronic warfare lineage, and watch the maritime corridors. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="asbm")
    img.save(IMG_EP74, "WEBP", quality=92)
    print(f"Saved: {IMG_EP74}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP74, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP74, IMG_REX, IMG_STUDIO, IMG_EP74, IMG_REX, IMG_EP74]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # 4. Neural Audio Synthesis
    print("[4/5] Synthesizing Rex Vance neural baritone audio...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    dur = get_audio_duration(audio_path)
    print(f"Synthesized Audio: {audio_path} ({dur} seconds)")
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = dur / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
    EPISODE_DATA["seconds"] = dur
    EPISODE_DATA["thumb"] = f"thumbs/{EPISODE_DATA['id']}.webp"
    EPISODE_DATA["audio"] = f"audio/{EPISODE_DATA['id']}.mp3"
    EPISODE_DATA["cover_video"] = f"thumbs/{EPISODE_DATA['id']}.mp4"
    
    # 5. Manifest Registration
    print("[5/5] Updating manifest web/data/episodes.json...")
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Prepend new episode so newest is first
    existing = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
    manifest["episodes"] = [EPISODE_DATA] + existing
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Updated {MANIFEST_FILE} with episode {EPISODE_DATA['id']}!")
    
    # Copy cover to brain artifacts for documentation
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep74_procedural.webp"
    with Image.open(IMG_EP74) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
