# engine/produce_episode_20.py
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

IMG_EP20 = os.path.join(THUMBS_DIR, "2026-10-06-20.webp")
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
    "id": "2026-10-06-20",
    "hour": "20:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "quantum",
    "title": "Bose-Einstein Condensates in Microgravity, Atom Interferometry & Orbital Gravimetry",
    "subject": "Hourly uncensored breakdown: Rex Vance examines quantum matter chilled to fifty picokelvin aboard the Cold Atom Lab in low Earth orbit, atom interferometers mapping subterranean defense tunnels and underwater submarines, and Yuri Shvets on Russia's crumbling space science apparatus.",
    "script_paragraphs": [
        "ZeroFilter broadcast twenty. I'm Rex Vance. Four hundred kilometers above our heads, inside the Cold Atom Laboratory aboard the International Space Station, physicists have engineered the coldest known location in the entire universe. Using laser optical molasses and magnetic evaporative traps, clouds of rubidium and potassium atoms are chilled to fifty picokelvin—fifty trillionths of a single degree above absolute zero. At that thermodynamic threshold, individual atomic boundaries dissolve; tens of thousands of separate atoms merge into a single macroscopic macroscopic quantum wave function: a Bose-Einstein Condensate.",

        "On Earth, gravitational sag pulls condensates down against vacuum chamber walls within milliseconds, destroying their delicate quantum coherence. But in the microgravity free-fall of orbit, these macroscopic quantum droplets float completely undisturbed for tens of seconds. When you split a Bose-Einstein condensate with a laser pulse into two paths and recombine them, the resulting quantum interference pattern acts as an ultra-sensitive atom interferometer—measuring local gravitational accelerations with twelve decimal places of precision.",

        "The strategic intelligence implications of orbital quantum gravimetry are revolutionary. Radar and optical satellites can only image surface geography. But an atom interferometer orbiting in low Earth orbit measures minute gravitational gradient anomalies caused by mass displacement beneath the soil. It can map subterranean military command bunkers buried hundreds of meters under granite, locate underground nuclear enrichment centrifuges, and detect the gravitational signature of submerged ballistic missile submarines patrolling silent oceans.",

        "Former KGB foreign counter-intelligence analyst Yuri Shvets provides the critical geopolitical contrast between Western quantum aerospace innovation and Moscow's decaying state apparatus. In Soviet times, the Academy of Sciences prided itself on fundamental theoretical physics, leading early work on quantum condensates. Today, as Shvets exposes, the Russian Federal Space Agency Roscosmos is functionally bankrupt—paralyzed by systemic embezzlement, Western microchip export controls, and an aging workforce that can barely maintain fifty-year-old Soyuz rocket designs.",

        "Yuri Shvets notes that when Moscow lost its Luna-25 lunar lander due to rudimentary thruster control errors, the Kremlin attempted to blame foreign sabotage rather than confront its own institutional degradation. While Western and allied scientists use microgravity quantum testbeds to pioneer inertial navigation systems that require zero external GPS satellites, Russia has become a junior tributary to Beijing, trading raw Siberian mineral concessions for commercial Chinese drone parts.",

        "The lesson of hour twenty is unequivocal: technological supremacy is not inherited through historical prestige; it is earned through rigorous open scientific inquiry, institutional accountability, and relentless engineering execution. Dictatorships can manufacture propaganda, but they cannot deceive the laws of thermodynamics. When you master quantum coherence, you see straight through the adversary's camouflage. I'm Rex Vance. Keep your signal focused, question every narrative, and stay tethered to empirical truth."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Cold Atom Lab Microgravity BEC Formation at 50 Picokelvin"},
        {"time": 30, "frame": "f02.webp", "caption": "Atom Interferometry Macroscopic Quantum Superposition"},
        {"time": 62, "frame": "f03.webp", "caption": "Orbital Quantum Gravimetry & Subterranean Bunker Detection"},
        {"time": 95, "frame": "f04.webp", "caption": "Yuri Shvets on Roscosmos Decay & Institutional Embezzlement"},
        {"time": 125, "frame": "f05.webp", "caption": "GPS-Free Quantum Inertial Navigation Telemetry"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Quantum Gravimetry Synthesis"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP20, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP20,
        IMG_REX,
        IMG_EP20,
        IMG_STUDIO,
        IMG_EP20,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 20...")
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
