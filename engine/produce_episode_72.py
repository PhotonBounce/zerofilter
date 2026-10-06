# engine/produce_episode_72.py
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

IMG_EP72 = os.path.join(THUMBS_DIR, "2026-10-09-00.webp")
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
    "id": "2026-10-09-00",
    "hour": "00:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "quantum",
    "title": "Nonlinear Josephson Parametric Amplifiers, Quantum Squeezed Vacuum & Soviet Low-Noise Radar Cryptanalysis",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates quantum-limited microwave amplification with Josephson parametric amplifiers, quantum vacuum squeezed states beating the standard quantum limit, and Yuri Shvets on Soviet low-noise radar cryptanalysis.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is midnight, zero hundred hours. In the ultra-sensitive realm of superconducting quantum measurement and deep-space signals intelligence, amplifying microwave photons without adding quantum noise has long represented the ultimate technological frontier. Conventional semiconductor cryogenic amplifiers inevitably introduce thermal and electronic fluctuations that destroy fragile quantum states. Today, nonlinear Josephson parametric amplifiers, or JPAs, operate right at the fundamental Heisenberg limit, squeezing vacuum fluctuations to read out single-photon microwave signals with unprecedented fidelity.",
        "At the core of a Josephson parametric amplifier is an array of non-dissipative superconducting Josephson junctions embedded within a high-Q microwave resonator. By pumping the non-linear inductance of the junctions with a strong microwave tone at twice the signal frequency, four-wave or three-wave mixing parametric processes amplify the input signal while actively squeezing one quadrature of quantum vacuum noise below the standard quantum limit. In dilution cryostats chilled to ten millikelvin, JPAs allow researchers to perform single-shot, non-destructive dispersive readout of superconducting transmon and fluxonium qubits in under two hundred nanoseconds. Beyond quantum computing, squeezed-state microwave amplification provides astronomical radar and SIGINT intercept receivers with quantum-enhanced sensitivity capable of extracting micro-watt stealth communications from cosmic background noise.",
        "The strategic implications of quantum-limited microwave sensing were understood decades ago by Soviet electronic warfare planners. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently detailed, the Soviet 8th Chief Directorate, responsible for cryptanalysis and SIGINT, and the KGB's Directorate T conducted intensive research into cryogenic parametric amplifiers and maser technology throughout the Cold War. Soviet defense institutes sought to build quantum-limited receivers to intercept NATO deep-space satellite uplinks and detect low-radar-cross-section experimental aircraft.",
        "According to Shvets, Soviet intelligence stations targeted American cryogenic engineering contractors and radar research laboratories across Southern California to exfiltrate patents on niobium thin films and superconducting tunnel junctions. Shvets documented that while Soviet theorists at the Steklov and Lebedev Institutes formulated groundbreaking mathematical proofs on squeezed quantum states and non-classical radiation fields, Gosplan industrial fabrication was plagued by contaminated vacuum chambers and inconsistent junction barriers. Soviet military intelligence attempted to bypass these domestic manufacturing deficits by purchasing dual-use commercial cryogenic microwave equipment through front companies in Vienna and Zurich.",
        "Today, the mastery of quantum-squeezed microwave amplification is quietly determining the future of electronic warfare, post-quantum SIGINT, and quantum radar. The nation that controls quantum-limited detection can penetrate advanced electronic cloaking and decrypt faint orbital communications that classical receivers perceive as empty vacuum noise.",
        "Audit the dilution cryostats, measure the squeezed-state quadratures, and inspect the Josephson parametric circuits. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="jpa")
    img.save(IMG_EP72, "WEBP", quality=92)
    print(f"Saved: {IMG_EP72}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP72, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP72, IMG_REX, IMG_STUDIO, IMG_EP72, IMG_REX, IMG_EP72]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep72_procedural.webp"
    with Image.open(IMG_EP72) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
