# engine/produce_episode_14.py
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

IMG_EP14 = os.path.join(THUMBS_DIR, "2026-10-06-14.webp")
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
    "id": "2026-10-06-14",
    "hour": "14:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Roger Penrose Orch-OR Quantum Biology, Non-Computable Algorithms & KGB Bio-Telemetry",
    "subject": "Hourly uncensored breakdown: Sir Roger Penrose's non-computable Orch-OR microtubule physics, aromatic tryptophan resonances, and Yuri Shvets on Soviet KGB psychotronic counter-intelligence files.",
    "script_paragraphs": [
        "ZeroFilter broadcast fourteen. I'm Rex Vance. If you ask Silicon Valley what consciousness is, they claim it's merely matrix multiplication—silicon transistors burning megawatts until self-awareness miraculously pops out. That is corporate sales collateral. Decades ago, Sir Roger Penrose proved mathematically through Godel's incompleteness theorems that human understanding transcends algorithmic computation. Our brains solve non-computable truths that no classical Turing machine can ever calculate.",

        "The physiological substrate of that non-computable collapse is not synaptic firing; synapses are merely peripheral switches. Penrose and Stuart Hameroff located the true quantum engine: cylindrical protein lattices inside neurons known as microtubules. Within these tubulin cylinders, quantum coherent superpositions persist, shielded from decoherence by structured water layers. At the Planck-scale threshold, the superposition undergoes Objective Reduction—spontaneous self-collapse dictated by spacetime geometry.",

        "Mainstream reductionists ridiculed Orch-OR for years, claiming warm biology was far too noisy for quantum states. That arrogance collapsed when ultra-fast spectroscopy confirmed quantum coherence across aromatic tryptophan lattices within tubulin, vibrating at multi-gigahertz frequencies. Furthermore, clinical anesthesia selectively binds to these hydrophobic tubulin pockets without shutting down general synaptic activity. Anesthesia disrupts the quantum dipole resonances that allow conscious reality to bind.",

        "Here is where intelligence history intersects biophysics. Former Soviet KGB foreign counter-intelligence analyst Yuri Shvets has documented how the KGB's Service A and Section 8 poured millions into psychotronic bio-information programs during the 1980s. While Washington tracked missile silos, Lubyanka analysts studied whether electromagnetic and microwave frequency pulses could induce tubulin decoherence across target populations. Soviet intelligence recognized that manipulating the biological interface is far more potent than intercepting signals.",

        "Yuri Shvets notes that modern Russian reflexive control borrows directly from these Cold War psychological archives. When adversary networks flood information feeds with synthetic disinformation, they aren't trying to sell a specific lie. They are inducing cognitive disorientation—overwhelming human perceptual filtering until the public surrenders critical verification and retreats into apathy. It is psychotronics stripped of mysticism and automated through digital feeds.",

        "The conclusion is decisive. If Penrose is right and consciousness relies on non-computable quantum gravity collapse within cellular microtubules, artificial general intelligence on classical silicon hardware will remain forever hollow—a parrot with zero inner observer. But if adversary intelligence understands the bio-quantum interface, the battlefield is not your server; it is your consciousness. I'm Rex Vance. Stay sharp, verify your signal, and never surrender your reality filter."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Sir Roger Penrose Orch-OR Quantum Biology Architecture"},
        {"time": 30, "frame": "f02.webp", "caption": "Microtubule Tubulin Quantum Lattice Superposition"},
        {"time": 62, "frame": "f03.webp", "caption": "Tryptophan Resonance & Anesthesia Binding Sites"},
        {"time": 95, "frame": "f04.webp", "caption": "Yuri Shvets KGB Bio-Information & Section 8 Files"},
        {"time": 125, "frame": "f05.webp", "caption": "Modern Reflexive Control & Cognitive Decoherence"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Bio-Quantum Telemetry Synthesis"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP14, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP14,
        IMG_REX,
        IMG_EP14,
        IMG_STUDIO,
        IMG_EP14,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 14...")
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
