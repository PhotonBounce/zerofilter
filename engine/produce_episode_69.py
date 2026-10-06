# engine/produce_episode_69.py
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

IMG_EP69 = os.path.join(THUMBS_DIR, "2026-10-08-21.webp")
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
    "id": "2026-10-08-21",
    "hour": "21:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Microtubular Resonance in Cortical Pyramidal Neurons, Megahertz Anesthetic Lock & Soviet Bio-Telemetry Archives",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates megahertz quantum dipoles in cortical pyramidal microtubules, anesthetic binding pockets locking conscious perception, and Yuri Shvets on Soviet bio-telemetry interrogation archives.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-one hundred hours. While commercial artificial intelligence cheerleaders claim that scaling transformer parameters and matrix multipliers will inevitably birth synthetic consciousness, biophysical neuroscience and quantum biology reveal an entirely different reality. Deep inside the cytoskeletal architecture of human cortical pyramidal neurons, cylindrical microtubule polymers operate not as passive structural scaffolding, but as high-frequency macroscopic quantum waveguides oscillating at megahertz dielectric resonance frequencies.",
        "Recent quantum biology experiments demonstrate that aromatic tryptophan amino acid rings within tubulin dimer proteins form helical dipole pathways capable of coherent electronic energy transfer. When volatile anesthetics such as isoflurane or propofol are introduced, they selectively bind to microscopic hydrophobic pockets across the tubulin lattice without blocking classic membrane ion channels. This anesthetic binding dampens terahertz dipole oscillations and quenches megahertz quantum coherence, extinguishing conscious perception while leaving basic cellular metabolism completely untouched. Consciousness is an orchestrated macroscopic quantum state intimately tethered to non-computable gravitational collapse.",
        "This fundamental boundary between mechanical computation and quantum neurobiology was intensely investigated behind the Iron Curtain. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, Soviet military-intelligence directorates operated secret psychotronic and bio-telemetry facilities across Kiev, Novosibirsk, and Leningrad throughout the Cold War. Under the guise of reflexive control and parapsychology research, researchers at the Soviet Academy of Sciences investigated whether cellular bio-resonances and electromagnetic field perturbations could be weaponized for covert interrogation and cognitive degradation.",
        "According to Shvets, Soviet intelligence officers in Directorate T were tasked with exfiltrating Western electrophysiology instrumentation, patch-clamp telemetry, and fluorophore microscopy systems to verify whether cellular tubulin structures could be selectively disrupted by external radio-frequency pulses. Shvets documented that corrupt Soviet academic administrators routinely inflated their experimental findings to siphon millions of rubles in black-budget slush funds. Yet, the underlying biophysical records confirmed that neural consciousness resists crude algorithmic manipulation, remaining protected by quantum coherence thresholds embedded within the neural cytoskeleton.",
        "Today, Silicon Valley tech oligarchs pouring billions of venture capital into classical algorithmic LLMs and neuromorphic silicon chips are colliding with this exact biological wall. You cannot emulate subjective conscious experience with digital matrix multiplication when the foundational spark of cognition is physically generated by quantum dipole resonance and orchestrated objective reduction inside living neuronal architecture.",
        "Audit the neural cytoskeletons, measure the tubulin dipole resonances, and inspect the anesthetic binding pockets. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="tubulin_quantum")
    img.save(IMG_EP69, "WEBP", quality=92)
    print(f"Saved: {IMG_EP69}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP69, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP69, IMG_REX, IMG_STUDIO, IMG_EP69, IMG_REX, IMG_EP69]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep69_procedural.webp"
    with Image.open(IMG_EP69) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
