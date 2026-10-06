# engine/produce_episode_99.py
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

IMG_EP99 = os.path.join(THUMBS_DIR, "2026-10-10-03.webp")
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
    "id": "2026-10-10-03",
    "hour": "03:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "corruption",
    "title": "Hypersonic Wind Tunnel Telemetry Falsification, CFD Grant Diversions & Soviet Scramjet Program Padding",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates congressional forensic audits revealing falsified high-enthalpy wind tunnel telemetry and computational fluid dynamics testing grant fraud in hypersonic scramjet contracts, and Yuri Shvets on Soviet scramjet program padding.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero three hundred hours. In aerospace defense procurement, hypersonic flight above Mach 5 is routinely marketed as the absolute frontier of military superiority. Billions of dollars in cost-plus research contracts flow each fiscal quarter into scramjet propulsion and glide-vehicle programs. Yet behind the classified briefings and patriotic press releases lies a devastating technical reality: a massive pattern of computational fluid dynamics grant diversion and falsified high-enthalpy wind tunnel test telemetry designed to hide persistent aerodynamic failure.",
        "At Mach 7, atmospheric friction generates boundary layer temperatures exceeding two thousand degrees Celsius, causing air to dissociate into ionized plasma. True scramjet ignition requires supersonic combustion within a supersonic airstream—an engineering challenge akin to keeping a match lit inside a category-five hurricane. When major aerospace primes repeatedly suffer catastrophic shockwave boundary-layer separations during physical flight tests, forensic defense audits reveal that contractors routinely massage computational aerodynamic models, substituting idealized simulated boundary layers to hit contract milestones and trigger milestone bonus payouts.",
        "This systemic manipulation of high-speed aerospace testing mirrors one of the most corrupt bureaucratic episodes of the Soviet military-industrial complex. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet design bureaus and academic research institutes engaged in massive performance padding and falsification to secure astronomical Gosplan defense allocations throughout the 1970s and 1980s.",
        "According to Shvets, the Central Aerohydrodynamic Institute, or TsAGI, and specialized ramjet design bureaus in Moscow and Leningrad faced immense political pressure from the Politburo to match American hypersonic concepts. Because high-enthalpy shock tunnels were exceedingly rare and technically temperamental, Soviet bureau chiefs routinely submitted synthetic thermodynamic calculations as empirical wind tunnel data. Shvets revealed that KGB First Chief Directorate officers monitoring defense scientific grants knew that half the claimed Mach 6 combustion benchmarks were administrative fictions designed solely to siphon state rubles into ministerial patronage networks.",
        "Decades later, the identical institutional pathology paralyzes Western hypersonic programs. Pentagon Inspector General audits indicate that critical test facilities operate with multi-year backlogs, forcing primes to rely on self-certified computer simulations that fail the moment vehicles encounter real atmospheric turbulence over the Pacific. Billions in cost-plus defense spending have yielded presentation slides and mockups, while genuine supersonic combustion remains bottlenecked by thermal physics that no accounting gimmick can bypass.",
        "Audit the computational fluid dynamics contracts, demand unvarnished telemetry from physical hypersonic test flights, and remember that when defense contractors substitute synthetic simulations for empirical physics, national security becomes an expensive illusion. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="hypersonic_fraud", title=EPISODE_DATA["title"])
    img.save(IMG_EP99, "WEBP", quality=92)
    print(f"Saved: {IMG_EP99}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP99, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP99, IMG_REX, IMG_STUDIO, IMG_EP99, IMG_REX, IMG_EP99]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep99_procedural.webp"
    with Image.open(IMG_EP99) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
