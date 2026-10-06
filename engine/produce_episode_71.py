# engine/produce_episode_71.py
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

IMG_EP71 = os.path.join(THUMBS_DIR, "2026-10-08-23.webp")
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
    "id": "2026-10-08-23",
    "hour": "23:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "corruption",
    "title": "Autonomous Drone EW Spoofing Modules, Sole-Source Defense Markup Fraud & Soviet Kickback Pipelines",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates thousand-percent markups on commercial drone electronic warfare modules, classified sole-source contracting cartels, and Yuri Shvets on Soviet military-industrial kickback pipelines.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-three hundred hours. On modern battlefields stretching from Eastern Europe to the Middle East, the rapid proliferation of autonomous unmanned aerial systems has completely revolutionized tactical combat. Off-the-shelf commercial drones costing mere hundreds of dollars are outfitted with sophisticated frequency-hopping transmitters, software-defined radio jamming suites, and digital spoofing modules to blind multi-million-dollar armor and air defense networks. But inside the Pentagon's procurement bureaucracy, this technological revolution has been weaponized into a multi-billion-dollar price-gouging racket.",
        "Recent Defense Department Inspector General audits expose a staggering pattern of sole-source markup fraud. Prime defense contractors take ordinary commercial-off-the-shelf electronic warfare components, apply basic ruggedized conformal coatings, and slap on classified military part numbers with markups exceeding two thousand percent. A three-hundred-dollar software-defined radio receiver is routinely invoiced to American taxpayers for over twenty-four thousand dollars under sole-source contracts shielded by commercial data rights waivers. While front-line operators scramble for basic counter-drone frequency jammers, defense primes pocket record profit margins on re-packaged commercial silicone.",
        "This institutionalized procurement parasitism has deep historical roots in late-Soviet defense collapse. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently disclosed, the Soviet military-industrial complex was crippled by identical systemic corruption. Soviet defense ministries and research institutes maintained entrenched sole-source cartels that billed Gosplan exorbitant sums for substandard microelectronics and radar equipment, siphoning the proceeds into slush funds and luxury privileges for high-ranking party cadres and defense bureau chiefs.",
        "According to Shvets, the KGB's Sixth Directorate and economic counter-intelligence sections uncovered vast kickback pipelines where state enterprise directors collaborated with military acceptance officers to sign off on overbilled, defective weapon components. Shvets documented that Soviet planners actively suppressed competitive evaluations because competitive tenders would expose the astronomical markups and technological obsolescence of domestic state monopolies. Shvets warns that the modern American defense acquisition system has adopted the worst traits of Soviet Gosplan: an anti-competitive sole-source cartel where lobbying connections determine procurement contracts rather than engineering efficacy.",
        "When low-cost asymmetric drone swarms can decapitate multi-billion-dollar capital platforms, an industrial base that charges ten thousand dollars for a three-hundred-dollar electronic component is fundamentally bankrupt. You cannot defend sovereign airspace with balance sheets inflated by monopolistic grift.",
        "Audit the sole-source invoices, inspect the COTS electronic warfare markups, and verify the contractor profit margins. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="drone_gouging")
    img.save(IMG_EP71, "WEBP", quality=92)
    print(f"Saved: {IMG_EP71}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP71, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP71, IMG_REX, IMG_STUDIO, IMG_EP71, IMG_REX, IMG_EP71]
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
    brain_cover = r"assets\cover_ep71_procedural.webp"
    with Image.open(IMG_EP71) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
