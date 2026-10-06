# engine/produce_episode_17.py
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

IMG_EP17 = os.path.join(THUMBS_DIR, "2026-10-06-17.webp")
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
    "id": "2026-10-06-17",
    "hour": "17:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "corruption",
    "title": "Pentagon Cost-Plus Contracting Cartels, Hypersonic Failure Audits & Revolving-Door Grift",
    "subject": "Hourly uncensored breakdown: Yuri Shvets analyzes Washington defense contracting monopolies billing billions for stalled hypersonic glide prototypes, F-35 supply chain failures, and how former defense officials cash out onto military-industrial corporate boards.",
    "script_paragraphs": [
        "ZeroFilter broadcast seventeen. I'm Rex Vance. If an aerospace startup in Silicon Valley burned twelve billion dollars over a decade without delivering a functioning commercial prototype, their investors would fire leadership and liquidate the assets by sunset. But if you are Lockheed Martin, Raytheon, or General Dynamics billing the United States Department of Defense under a cost-plus contract, catastrophic technical failure is not a liability—it is an annuity. The more delays you engineer, the larger your taxpayer-funded management margin becomes.",

        "Look at America's stalled hypersonic glide weapon programs. While China fields operational Mach-8 DF-17 glide vehicles and Russia hypes its Kinzhal platforms, American defense conglomerates have consumed over fifteen billion dollars in developmental contracts, yielding aborted flight tests, sensor thermal fractures, and endless scheduling extensions. The problem is not engineering talent; American laboratory physicists are the finest on Earth. The disease is institutional procurement design: cost-plus contracts reward inefficiency and penalize rapid, cost-effective completion.",

        "Former KGB foreign counter-intelligence analyst Yuri Shvets exposes the underlying architecture that keeps this parasitic ecosystem intact: the Washington revolving door. When a three-star admiral or Pentagon undersecretary oversees procurement milestones, their final years in uniform are an audition for defense industry board seats. The moment they retire, they register as corporate advisors, collecting seven-figure retainers and stock options from the exact contractors whose cost overruns they routinely rubber-stamped.",

        "Yuri Shvets notes that this structural rot mirrors the internal decay that paralyzed the Soviet military-industrial complex in the 1980s. When centralized bureaucratic ministries prioritize patronage networks over frontline operational reality, equipment becomes bloated, unmaintainable, and astronomically expensive. Today, the Government Accountability Office reports that the F-35 fleet suffers from mission-capable rates hovering near fifty percent due to proprietary software locks and contractor maintenance monopolies that prevent military mechanics from fixing their own aircraft.",

        "Asymmetric warfare on the Ukrainian front line has thoroughly dismantled this legacy procurement paradigm. Low-cost autonomous FPV strike drones fabricated for five hundred dollars apiece are systematically destroying multi-million-dollar armored vehicles and surface-to-air missile radars. A thousand dispersed garage workshops out-produce rigid corporate monopolies every single day. The future of defense is rapid modular iteration, open software architectures, and fixed-price competitive delivery.",

        "The verdict is indisputable: our national security is being held hostage by a protected cartel that trades frontline readiness for quarterly stock buybacks. Yuri Shvets' analysis gives us the unredacted diagnosis: an empire that cannot audit its Pentagon expenditures is an empire rotting from the inside out. Real strength requires accountability, transparency, and dismantling the corporate grift. I'm Rex Vance. Track the invoices, question the consensus, and never accept excuses for incompetence."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Cost-Plus Defense Contracting Cartels & Waste"},
        {"time": 30, "frame": "f02.webp", "caption": "Hypersonic Glide Vehicle Test Telemetry & Delays"},
        {"time": 62, "frame": "f03.webp", "caption": "Yuri Shvets on Pentagon Revolving Door Retainers"},
        {"time": 95, "frame": "f04.webp", "caption": "F-35 Maintenance Monopolies & Mission-Capable Deficits"},
        {"time": 125, "frame": "f05.webp", "caption": "Low-Cost Asymmetric FPV Swarms vs Bloated Armor"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Procurement Forensic Audit"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP17, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP17,
        IMG_REX,
        IMG_EP17,
        IMG_STUDIO,
        IMG_EP17,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 17...")
    await synthesize_rex_vance(full_text, mp3_path)

    # 4. Measure duration
    dur = get_audio_duration(mp3_path)
    print(f"Audio synthesized: {dur}s -> {mp3_path}")

    # 5. Update web/data/episodes.json
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    new_ep = {
        "id": EPISODE_DATA["id"],
        "date": EPISODE_DATA["date"],
        "hour": EPISODE_DATA["hour"],
        "kind": EPISODE_DATA["kind"],
        "category": EPISODE_DATA["category"],
        "title": EPISODE_DATA["title"],
        "subject": EPISODE_DATA["subject"],
        "seconds": dur,
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4",
        "paragraphs": EPISODE_DATA["script_paragraphs"],
        "art": {
            "frames": [
                {
                    "t": stem["time"],
                    "src": f"art/{EPISODE_DATA['id']}/{stem['frame']}",
                    "caption": stem["caption"]
                }
                for stem in EPISODE_DATA["art_stems"]
            ]
        }
    }

    manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != new_ep["id"]]
    manifest["episodes"].insert(0, new_ep)

    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    print("Manifest episodes.json updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())
