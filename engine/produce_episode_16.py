# engine/produce_episode_16.py
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

IMG_EP16 = os.path.join(THUMBS_DIR, "2026-10-06-16.webp")
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
    "id": "2026-10-06-16",
    "hour": "16:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Key Distribution Downlinks, Atmospheric Decoherence & China's Micius Network",
    "subject": "Hourly uncensored breakdown: Yuri Shvets analyzes Beijing's state-backed quantum communications infrastructure, free-space entangled photon satellite links, adaptive optics counter-decoherence, and Western intelligence cryptographic vulnerabilities.",
    "script_paragraphs": [
        "ZeroFilter broadcast sixteen. I'm Rex Vance. If you rely on RSA-4096 or elliptic-curve cryptography to secure your communications, you are living on borrowed mathematical time. Within the decade, fault-tolerant quantum computing clusters running Shor's algorithm will crack legacy public-key encryption in seconds. Western intelligence agencies know this; they call it Harvest Now, Decrypt Later. But while Washington engages in endless committee hearings, Beijing has spent billions building a functioning sovereign quantum communications backbone in low Earth orbit.",

        "The centerpiece of this capability began with the Micius satellite platform. Chinese physicists achieved what Western skeptics called impossible: transmitting entangled photon pairs across twelve hundred kilometers of free space directly to ground optical telescope stations in Delingha and Lijiang, verifying violation of Bell's inequalities at satellite scale. Under the laws of quantum mechanics, any third-party interception attempt irrevocably collapses the quantum wave function, instantly alerting both sender and receiver to the intrusion.",

        "The engineering obstacle to practical quantum key distribution has never been orbital optics; it is atmospheric turbulence. When an entangled photon beam traverses the lowest ten kilometers of Earth's atmosphere, thermal air pockets, wind shear, and particulate scatter induce phase decoherence and beam wander, destroying the quantum bit error rate. Chinese defense laboratories solved this by integrating dual-wavelength adaptive optics mirrors pulsing at ten kilohertz, actively deforming telescope mirrors to cancel atmospheric wavefront distortion in real time.",

        "Here is the strategic reality former KGB counter-intelligence analyst Yuri Shvets emphasizes: technology is only as sovereign as the state apparatus controlling it. Beijing claims their two-thousand-kilometer Beijing-Shanghai quantum trunk line and satellite links represent an unhackable democratic science achievement. In reality, as Shvets points out, every quantum repeater node across that infrastructure requires classical trusted relays managed directly by the Ministry of State Security. The quantum link between nodes is provably uncrackable, but the nodes themselves are centralized totalitarian inspection points.",

        "Meanwhile, Western defense contractors have prioritized software-based post-quantum mathematical algorithms—lattice-based cryptography—because it requires zero expensive aerospace infrastructure. But mathematical complexity is an assumption, not a physical law. An adversary with a revolutionary quantum algorithm can shatter lattice cryptography overnight. Physical quantum key distribution, grounded in the Heisenberg uncertainty principle, is the only security architecture guaranteed by the laws of physics themselves.",

        "The strategic takeaway is transparent: you cannot protect tomorrow's intelligence with yesterday's mathematical comfort blankets. True information dominance requires mastering both the quantum physical substrate and the human institutional integrity operating it. Yuri Shvets' warning remains absolute: authoritarian states will always attempt to centralize the bottleneck; free minds must decentralize the architecture. I'm Rex Vance. Protect your encryption, verify every node, and never trust a black box."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Harvest Now Decrypt Later & Post-Quantum Vulnerability"},
        {"time": 30, "frame": "f02.webp", "caption": "Micius Free-Space Entanglement Satellite Downlink"},
        {"time": 62, "frame": "f03.webp", "caption": "Adaptive Optics Atmospheric Turbulence Correction"},
        {"time": 95, "frame": "f04.webp", "caption": "Yuri Shvets on Beijing MSS Quantum Relay Nodes"},
        {"time": 125, "frame": "f05.webp", "caption": "Lattice Cryptography vs Physical Quantum Key Distribution"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Quantum Information Sovereignty Synthesis"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP16, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP16,
        IMG_REX,
        IMG_EP16,
        IMG_STUDIO,
        IMG_EP16,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 16...")
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
