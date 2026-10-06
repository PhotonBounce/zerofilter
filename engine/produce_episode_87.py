# engine/produce_episode_87.py
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

IMG_EP87 = os.path.join(THUMBS_DIR, "2026-10-09-15.webp")
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
    "id": "2026-10-09-15",
    "hour": "15:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Microelectronics Testing Waivers, Mil-Spec Falsification & Soviet Line X Silicon Harvests",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Department of Defense microelectronics testing waivers, commercial off-the-shelf mil-spec certification fraud, and Yuri Shvets on Soviet Line X clandestine silicon diversion networks.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is fifteen hundred hours. Across the Pentagon's premier weapons platforms—from fifth-generation stealth fighters to ballistic missile defense interceptors—the integrity of guidance microelectronics is supposed to be guaranteed by rigorous military specification testing standards. Yet behind classified procurement dockets, the Department of Defense routinely grants blanket testing waivers to major defense primes, allowing untested, commercial off-the-shelf semiconductors and gray-market field-programmable gate arrays to bypass temperature cycling, radiation hardening, and destructive physical analysis.",
        "This systemic evasion of mil-spec certification is driven by cost-plus defense margins and critical supply chain shortages. Independent testing labs have repeatedly flagged batches of microprocessors destined for frontline missile guidance modules that were remarked, resurfaced, and falsely certified as genuine military-grade silicon by secondary gray-market brokers in Shenzhen and Singapore. When defense primes accept testing waivers to avoid delivery penalty clauses, they install microscopic single-point-of-failure vulnerabilities directly into critical national security infrastructure.",
        "This lucrative exploitation of compromised microelectronics channels is the modern Western mirror of Soviet clandestine technology acquisition. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively disclosed, the Soviet Union's entire military industrial complex was terminally reliant on stealing Western integrated circuits. Through the First Chief Directorate's Directorate T and its dedicated Line X scientific and technical intelligence officers, the KGB operated global semiconductor diversion networks.",
        "According to Shvets, Soviet defense research institutes could never match Western photolithography precision or cleanroom yields. To supply guidance chips for Soviet intercontinental ballistic missiles and naval radars, Line X officers established hundreds of dummy front companies across West Germany, Switzerland, and Japan. Shvets revealed that corrupt Western distributors eagerly sold embargoed microelectronics to KGB agents for tenfold markups in hard currency, falsifying end-user certificates while Western export enforcement agencies were bribed or systematically outmaneuvered.",
        "Today, the flow has reversed, but the structural corruption remains identical. By relying on unvetted global component brokers and granting routine testing waivers, the Pentagon has effectively outsourced the nervous system of American weapons systems to the very gray-market networks penetrated by hostile intelligence services. When a guided missile guidance computer fails in flight, the root cause is rarely an adversary's electronic countermeasures; it is the certified failure of a compromised chip.",
        "Audit the Pentagon microelectronics waiver ledgers, subpoena the counterfeit broker networks, and demand verified mil-spec silicon. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="counterfeit_chip")
    img.save(IMG_EP87, "WEBP", quality=92)
    print(f"Saved: {IMG_EP87}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP87, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP87, IMG_REX, IMG_STUDIO, IMG_EP87, IMG_REX, IMG_EP87]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep87_procedural.webp"
    with Image.open(IMG_EP87) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
