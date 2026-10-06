# engine/produce_episode_91.py
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

IMG_EP91 = os.path.join(THUMBS_DIR, "2026-10-09-19.webp")
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
    "id": "2026-10-09-19",
    "hour": "19:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Fuel Smuggling Syndicates, NATO Bunkering Fraud & Soviet Black Sea Fleet Diversion Cartels",
    "subject": "Hourly uncensored breakdown: Rex Vance uncovers defense bunkering fraud syndicates, falsified fuel bills of lading at NATO forward logistics hubs, and Yuri Shvets on KGB-sanctioned Soviet naval fuel diversion cartels.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is nineteen hundred hours. While defense ministries publicize multi-billion-dollar drone swarms and hypersonic missile contracts, the unglamorous lifeblood of all military mechanized logistics—petroleum, oil, and lubricants—is hemorrhaging through systemic institutional fraud. Across forward operational airbases and maritime bunkering stations, military-grade aviation turbine fuel JP-8 and naval distillate are systematically diverted into illicit commercial black-market networks through falsified bills of lading, tampered flowmeter seals, and organized defense contractor kickback syndicates.",
        "Recent federal and allied criminal indictments expose an industrial scale of grift. Defense logistics sub-contractors operating across NATO forward hubs in Eastern Europe, the Mediterranean, and the Middle East systematically exploit paper-based inventory vouchers to bill for millions of gallons of phantom fuel. Fuel tankers arrive at forward bases carrying contaminated, water-diluted slurry, while premium JP-8 jet propellant is siphoned into covert offshore bunkering barges and resold to civilian airlines at emergency spot-market prices. These cartels operate with impunity, shielded by compromised quartermasters and revolving-door defense contracting executives.",
        "This brazen looting of frontline defense energy supplies is not an unprecedented tactical anomaly; it is the exact blueprint of Soviet late-Cold War institutional corruption. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has extensively disclosed, the Soviet Armed Forces—and specifically the Black Sea Fleet headquartered in Sevastopol and Odessa—ran the most lucrative state-sanctioned fuel smuggling syndicates in the entire Warsaw Pact.",
        "According to Shvets, senior naval supply officers colluded directly with KGB Third Directorate military counter-intelligence curators and black-market mafia bosses to siphon off hundreds of thousands of metric tons of naval fuel oil and aviation kerosene each month. Operational readiness reports were systematically forged: logs falsely claimed naval battle groups were conducting round-the-clock anti-submarine exercises across the Black Sea, while warships remained tied to piers with their boilers cold to mask the depleted fuel bunkers. Shvets revealed that entire military rail cistern echelons vanished into dummy industrial cooperatives, laundered for hard Western currency.",
        "Today, that exact Soviet diversion playbook has infected Western defense contracting conglomerates. When military fuel accountability is outsourced to opaque private logistics vendors operating without real-time cryptographic flowmeter telemetry or unannounced dip-stick audits, combat units inherit dry tanks and engine-destroying sludge during critical mobilization windows. Pentagon planners can boast of fifth-generation stealth fighters and autonomous armor, but an entire theater campaign collapses when corrupt fuel cartels falsify the bills of lading.",
        "Audit the NATO fuel bunkering cryptographic flowmeters, freeze the offshore contractor bank accounts, and demand absolute forensic accountability across military energy supply lines. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="fuel_smuggling", title=EPISODE_DATA["title"])
    img.save(IMG_EP91, "WEBP", quality=92)
    print(f"Saved: {IMG_EP91}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP91, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP91, IMG_REX, IMG_STUDIO, IMG_EP91, IMG_REX, IMG_EP91]
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
    brain_cover = r"assets\cover_ep91_procedural.webp"
    with Image.open(IMG_EP91) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
