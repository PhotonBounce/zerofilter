# engine/produce_episode_115.py
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

IMG_EP115 = os.path.join(THUMBS_DIR, "2026-10-10-19.webp")
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
    "id": "2026-10-10-19",
    "hour": "19:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "corruption",
    "title": "Drone Swarm Telemetry Price Gouging, VC Pass-Through Shells & Soviet Bureau Cartels",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates congressional audits exposing Silicon Valley defense venture capital syndicates inflating commercial off-the-shelf drone telemetry avionics by 4,000 percent through pass-through shell entities, and Yuri Shvets on Soviet design bureau price-fixing cartels.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is nineteen hundred hours. In modern tactical warfare, low-cost autonomous drone swarms were supposed to democratize firepower, delivering asymmetric strike capabilities for a fraction of the cost of traditional missiles. Commercial off-the-shelf quadcopters and fixed-wing kamikaze drones manufactured for five hundred dollars have repeatedly neutralized multimillion-dollar armored columns and naval combatants. Yet inside the Pentagon's procurement labyrinth, that low-cost promise has been captured and mutilated by defense venture capital syndicates passing off rebranded hobbyist avionics at catastrophic, four-thousand-percent taxpayer markups.",
        "Recent congressional oversight hearings and Department of Defense Inspector General audits reveal a systematic pattern of procurement price gouging. Silicon Valley venture-backed defense startups establish cascading layers of pass-through shell companies to launder dual-use commercial telemetry modules. A flight controller board purchased from overseas consumer suppliers for forty dollars is repackaged in a ruggedized aluminum shell, assigned a proprietary mil-spec part number, and invoiced to the Defense Logistics Agency for eight thousand two hundred dollars per unit. When whistleblowers question the margins, contractors claim proprietary algorithmic intellectual property and threaten supply-chain blackouts.",
        "This institutionalized padding of military technology costs is the modern capitalist reincarnation of the bureaucratic cartels that hollowed out the Soviet defense budget from within. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively disclosed, Soviet defense design bureaus perfected price-fixing and artificial cost inflation decades ago.",
        "According to Shvets, Soviet defense design bureaus like Mikoyan, Sukhoi, and Tupolev operated as entrenched monopoly cartels under Gosplan. Rather than competing to reduce military expenditures, chief designers colluded to pad technical specifications, demanding ever-larger allocations of state roubles, rare titanium alloys, and Western microchips procured by KGB Line X. Shvets revealed that design bureau chiefs routinely inflated development costs by five hundred percent, claiming fictitious scientific breakthroughs and falsifying test logs to justify continuous state subsidies while delivering aircraft plagued by severe avionics flaws.",
        "Today, the faces on the marketing brochures are venture capitalists in fleece vests rather than Soviet bureaucrats in grey suits, but the extraction mechanism is identical. Cost-plus research grants and unvetted rapid-procurement contracts allow tech-defense syndicates to bleed military budgets dry while delivering frontline troops overpriced, fragile gear. When national defense relies on monopoly brokers laundering commercial chips behind classified billing codes, fiscal discipline collapses and soldiers pay the price in blood.",
        "Audit the pass-through shell entities draining tactical defense budgets, strip proprietary shields off commercial drone avionics, and remember that when a five-hundred-dollar drone costs eight thousand dollars, corruption is the primary payload. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="drone_gouging", title=EPISODE_DATA["title"])
    img.save(IMG_EP115, "WEBP", quality=92)
    print(f"Saved: {IMG_EP115}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP115, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP115,
        IMG_STUDIO,
        IMG_EP115,
        IMG_REX,
        IMG_EP115,
        IMG_STUDIO
    ]
    create_art_frames(EPISODE_DATA["id"], src_frames)
    
    # 4. Neural Voice Audio Synthesis
    print("[4/5] Synthesizing neural voice (Rex Vance via edge-tts)...")
    full_script = " ... \n\n ".join(EPISODE_DATA["paragraphs"])
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, mp3_path)
    actual_seconds = get_audio_duration(mp3_path)
    print(f"Synthesized Rex Vance audio: {mp3_path} ({actual_seconds}s)")
    
    # 5. Manifest & Metadata Registration
    print("[5/5] Registering in episodes.json...")
    t_step = actual_seconds / 6.0
    frame_times = [int(round(i * t_step)) for i in range(6)]
    
    full_episode_entry = {
        "id": EPISODE_DATA["id"],
        "hour": EPISODE_DATA["hour"],
        "date": EPISODE_DATA["date"],
        "kind": EPISODE_DATA["kind"],
        "category": EPISODE_DATA["category"],
        "title": EPISODE_DATA["title"],
        "subject": EPISODE_DATA["subject"],
        "paragraphs": EPISODE_DATA["paragraphs"],
        "art": {
            "frames": [
                {"t": frame_times[i], "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
                for i in range(6)
            ]
        },
        "seconds": actual_seconds,
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Prepend new episode if not already present
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
    
    manifest["episodes"].insert(0, full_episode_entry)
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully published Episode {EPISODE_DATA['id']} to manifest ({len(manifest['episodes'])} episodes total).")

if __name__ == "__main__":
    asyncio.run(main())
