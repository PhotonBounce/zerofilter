# engine/produce_episode_21.py
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

IMG_EP21 = os.path.join(THUMBS_DIR, "2026-10-06-21.webp")
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
    "id": "2026-10-06-21",
    "hour": "21:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "corruption",
    "title": "Silicon Valley Defense VC Cartels, Dual-Use Tech Diversion & KGB Directorate T Lineage",
    "subject": "Hourly uncensored breakdown: Yuri Shvets analyzes how Soviet Directorate T industrial espionage pipelines laid the groundwork for modern Beijing and Moscow shell companies laundering venture-backed dual-use semiconductor and autonomous drone IP out of California.",
    "script_paragraphs": [
        "ZeroFilter broadcast twenty-one. I'm Rex Vance. Walk through Sand Hill Road in Menlo Park tonight, and every venture capital fund has rebranded itself as an American dynamism patriot—claiming to build sovereign defense tech for the Pentagon. But follow the limited partnership capitalization tables and cap-table Cayman shells, and you find a web of sovereign wealth capital, front companies, and technology transfer conduits bleeding critical dual-use intellectual property directly to foreign adversaries.",

        "Former KGB foreign counter-intelligence analyst Yuri Shvets traces this exact corporate deception doctrine back to its historical genesis: the KGB's Directorate T, the scientific and technological intelligence branch of the First Chief Directorate. In the late 1970s and 1980s, the Soviet Union could not fabricate high-density microprocessors; Directorate T orchestrated front companies in Vienna, Zurich, and Hong Kong to purchase American photolithography steppers and computer numerical control milling machines under the guise of civilian laboratory supply firms.",

        "Today, as Yuri Shvets exposes, foreign intelligence services do not need to smuggle hardware through neutral European embassies. Instead, they exploit Silicon Valley's obsession with liquidity. Adversary intelligence networks set up venture syndicates and angel networks, taking non-controlling five-percent stakes in American autonomous robotics, gallium-nitride radar semiconductor, and computer-vision startups. Under standard investor agreements, those minority stakes grant full technical information rights—blueprints, source code, and supply-chain supplier lists.",

        "The Department of Commerce's Bureau of Industry and Security and the Committee on Foreign Investment in the United States remain chronically under-resourced, caught in twentieth-century bureaucratic definitions of defense articles. An inertial measurement unit or an FPGA chip is classified as dual-use commercial goods until it ends up inside a Russian Iskander cruise missile or an Iranian Shahed loitering drone recovering from a Ukrainian impact site.",

        "Yuri Shvets emphasizes that when captured Russian missiles are disassembled in Kyiv laboratories, over seventy percent of the precision guidance microelectronics—micro-controllers, digital signal processors, and high-frequency RF transceivers—originate from American and European chip manufacturers. They do not arrive through official defense channels; they are routed through three layers of shell corporations in Kazakhstan, Turkey, and the United Arab Emirates, funded by Western-backed venture capital arbitrage.",

        "The bottom line is an indictment of corporate greed masquerading as patriotism. You cannot defend the free world with one hand while selling the blueprint of your defense grid to an adversarial shell company with the other. Yuri Shvets' counter-intelligence warning is clear: financial forensics must penetrate every venture capital cap-table, unmask the hidden proxies, and treat technology diversion as treason. I'm Rex Vance. Audit the cap tables, protect the source code, and never trade strategic survival for venture returns."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Silicon Valley Sand Hill Road Defense VC Rebrand"},
        {"time": 30, "frame": "f02.webp", "caption": "Yuri Shvets on KGB Directorate T Tech Diversion Lineage"},
        {"time": 62, "frame": "f03.webp", "caption": "Minority Stake Angel Syndicates & Source Code Rights"},
        {"time": 95, "frame": "f04.webp", "caption": "Dual-Use BIS Regulatory Loopholes & FPGA Smuggling"},
        {"time": 125, "frame": "f05.webp", "caption": "Kyiv Laboratory Teardowns of Western Electronics in Missiles"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Cap-Table Financial Forensics Synthesis"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP21, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP21,
        IMG_REX,
        IMG_EP21,
        IMG_STUDIO,
        IMG_EP21,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 21...")
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
