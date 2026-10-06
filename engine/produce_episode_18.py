# engine/produce_episode_18.py
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

IMG_EP18 = os.path.join(THUMBS_DIR, "2026-10-06-18.webp")
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
    "id": "2026-10-06-18",
    "hour": "18:00",
    "date": "2026-10-06",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Stuart Hameroff's Quantum Anesthesia, Neural Biophotons & KGB Bio-Resonance Files",
    "subject": "Hourly uncensored breakdown: Rex Vance explores Dr. Stuart Hameroff's clinical discovery of anesthetic quantum dipole dampening within tubulin lattices, cellular biophoton emission cascades, and Yuri Shvets on declassified Soviet Section 8 bio-resonance archives.",
    "script_paragraphs": [
        "ZeroFilter broadcast eighteen. I'm Rex Vance. If you have ever undergone major surgery, you experienced a phenomenon that mainstream neuroscience still cannot explain with classical models. An anesthesiologist pushed a colorless vapor or intravenous liquid into your bloodstream, and in under twenty seconds, your conscious awareness vanished—not because your brain died, and not because synaptic electrical firing ceased. Under general anesthesia, evoked potential monitors show sensory signals still entering the thalamus and cortex. The peripheral wiring remains active, but the observer inside the theater has completely evaporated.",

        "Dr. Stuart Hameroff, chief of anesthesiology at the University of Arizona and co-architect of Orch-OR theory with Sir Roger Penrose, spent forty years asking the question neuroscientists avoided: what does anesthesia actually bind to? The answer is not membrane receptors or ion channels; volatile anesthetics bind via weak London dispersion forces directly inside hydrophobic pockets of tubulin proteins inside neural microtubules. In those shielded nanoscale chambers, anesthetics dampen multi-terahertz quantum dipole oscillations, severing the microscopic coherence necessary for conscious reality to emerge.",

        "Recent biophysical discoveries have taken this from theoretical biology into hard quantum photonics. University laboratories utilizing ultra-sensitive photomultiplier tubes have recorded continuous, ultra-weak biophoton emissions radiating from living neural networks. Neurons are not merely electrical copper wires firing spikes; they are optical waveguides. Microtubules act as coherent optical cavities, channeling biophotons across cellular architectures to synchronize cortical regions far faster than ionic diffusion speeds could ever permit.",

        "Now let's examine the declassified national security dimension. Former Soviet KGB foreign counter-intelligence analyst Yuri Shvets has frequently highlighted the massive scientific espionage efforts directed by the First Chief Directorate's Directorate T during the late Cold War. Moscow was obsessed with bio-resonance and non-ionizing electromagnetic telemetry. In secret institutes across Novosibirsk and Zagorsk, Soviet military biophysicists attempted to replicate Western anesthesia studies to determine whether directed microwave frequencies could induce synthetic tubulin dampening at standoff range.",

        "Yuri Shvets notes that while Soviet psychotronics never succeeded in building magical telepathic weapons, their research produced rigorous data on how human cognitive filtering breaks down under external electromagnetic and psychological stress. Modern Russian electronic warfare and informational influence operations exploit this physiological reality: flood the human interface with high-entropy noise until the brain's internal quantum coherence degrades, inducing apathy, fatalism, and paralysis in the targeted populace.",

        "The lesson for free individuals is profound. Your consciousness is not an accidental chemical glitch or an algorithmic spreadsheet; it is an exquisite quantum optical instrument deeply interwoven with the fundamental fabric of spacetime. If authoritarian regimes and monolithic tech monopolies seek to degrade your perceptual sovereignty, your greatest defense is deliberate signal hygiene: question corporate authority, cultivate mental coherence, and refuse to surrender your inner observer. I'm Rex Vance. Keep your signal pristine, trust the physics, and I'll see you at the next broadcast."
    ],
    "art_stems": [
        {"time": 0, "frame": "f01.webp", "caption": "Clinical General Anesthesia & Observer Evaporation"},
        {"time": 30, "frame": "f02.webp", "caption": "Tubulin Hydrophobic Pockets & London Dispersion Forces"},
        {"time": 62, "frame": "f03.webp", "caption": "Neural Biophoton Emission & Optical Waveguide Telemetry"},
        {"time": 95, "frame": "f04.webp", "caption": "Yuri Shvets on KGB Directorate T Bio-Resonance Archives"},
        {"time": 125, "frame": "f05.webp", "caption": "Reflexive Decoherence & Cognitive Signal Protection"},
        {"time": 155, "frame": "f06.webp", "caption": "Rex Vance Bio-Quantum Sovereignty Synthesis"}
    ]
}

async def main():
    print(f"=== Producing Episode {EPISODE_DATA['id']} ===")
    
    full_text = "\n\n".join(EPISODE_DATA["script_paragraphs"])
    words = full_text.split()
    print(f"Total word count: {len(words)}")

    # 1. Video cover
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP18, mp4_path, duration=10)

    # 2. Art frames
    art_sources = [
        IMG_EP18,
        IMG_REX,
        IMG_EP18,
        IMG_STUDIO,
        IMG_EP18,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)

    # 3. Audio synthesis
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    print(f"Synthesizing Rex Vance audio for Episode 18...")
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
