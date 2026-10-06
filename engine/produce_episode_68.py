# engine/produce_episode_68.py
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

IMG_EP68 = os.path.join(THUMBS_DIR, "2026-10-08-20.webp")
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
    "id": "2026-10-08-20",
    "hour": "20:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "quantum",
    "title": "Superconducting Fluxonium Qubits, High-Harmonic Phase Slip & Soviet Cryogenic Solid-State Archives",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates superconducting fluxonium qubits with millisecond coherence, quantum phase-slip suppression across Josephson superinductance arrays, and Yuri Shvets on Soviet cryogenic solid-state physics archives.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty hundred hours. In the race for fault-tolerant quantum computation, superconducting fluxonium qubits have emerged as a radical paradigm shift, breaking free from the coherence bottlenecks that plague standard transmon architectures. By pairing a small Josephson junction with a superinductor array composed of hundreds of Josephson junctions, fluxonium suppresses charge noise and low-frequency dielectric loss, achieving record coherence times exceeding one millisecond.",
        "The physical breakthrough of fluxonium lies in its highly non-linear flux potential and quantum phase-slip dynamics. Unlike transmons, which operate with weakly anharmonic energy levels vulnerable to stray microwave excitation and charge fluctuations, fluxonium shunts the junction with an ultra-large inductance. This heavy inductive shunt suppresses 2e phase slips across the junction loop, exponentially protecting the computational zero-to-one transition from energy relaxation while maintaining strong microwave-addressable anharmonicity at high-harmonic drive frequencies. In dilution refrigerators operating at ten millikelvin, fluxonium bypasses two-level dielectric defect losses that cripple traditional planar quantum circuits.",
        "This deep-cryogenic physics frontier has historical roots in Soviet-era solid-state intelligence networks. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently disclosed, the KGB's First Chief Directorate and Directorate T maintained intense surveillance on Western low-temperature physics and Josephson junction developments throughout the 1970s and 1980s. Soviet theoretical physicists at the Landau Institute and Kapitza Institute pioneered macroscopic quantum tunneling and phase-slip theory, but the Soviet defense establishment was paralyzed by an inability to fabricate clean, defect-free thin-film sub-micron junctions.",
        "According to Shvets, Soviet scientific intelligence stations were tasked with illegally obtaining American electron-beam lithography equipment, cryogenic dilution refrigerators, and ultra-high-vacuum sputtering targets from California defense contractors and academic research labs. Shvets documented that while Soviet theorists formulated the mathematical foundations of macroscopic phase slips and superinductance in superconducting wires, Gosplan industrial bottlenecks prevented mass fabrication. Soviet military intelligence sought Western solid-state cryogenic patents to bolster early attempts at superconducting SQUID magnetometers and cryptanalytic hardware.",
        "Today, as Western quantum laboratories scale fluxonium arrays for fault-tolerant logical qubits, the geopolitical contest over cryogenic infrastructure and quantum hardware sovereignty is escalating. The nation that masters high-harmonic phase-slip suppression and large-scale fluxonium connectivity will render classical public-key cryptography obsolete while unlocking fault-tolerant quantum simulation of classified materials.",
        "Audit the dilution cryostats, trace the Josephson superinductance arrays, and inspect the phase-slip telemetry. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="fluxonium_qubit")
    img.save(IMG_EP68, "WEBP", quality=92)
    print(f"Saved: {IMG_EP68}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP68, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP68, IMG_REX, IMG_STUDIO, IMG_EP68, IMG_REX, IMG_EP68]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep68_procedural.webp"
    with Image.open(IMG_EP68) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
