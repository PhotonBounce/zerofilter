# engine/produce_episode_45.py
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

IMG_EP45 = os.path.join(THUMBS_DIR, "2026-10-07-21.webp")
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
    "id": "2026-10-07-21",
    "hour": "21:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Quantum Annealing in Flux Qubits, Adiabatic Shortcuts & Soviet Supercomputing Cryptanalysis",
    "subject": "Hourly uncensored breakdown: Rex Vance explores quantum annealing across superconducting flux qubit lattices, adiabatic shortcuts to ground states, and Yuri Shvets's insider analysis of Soviet Eighth Chief Directorate cryogenic cryptanalysis programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twenty-one hundred hours. While universal quantum computing architectures battle dielectric decoherence and fragile surface codes, quantum annealers solve computational bottlenecks through a fundamentally different physical mechanism: adiabatic quantum evolution. Chilled to eleven millikelvin, thousands of superconducting flux qubits—metallic loops interrupted by Josephson junctions—circulate macroscopic persistent currents. By tuning external magnetic flux biases, physicists program combinatorial optimization problems directly into the Ising spin Hamiltonian of the lattice.",
        "Rather than gate-based circuit pulses, annealing relies on quantum tunneling. The processor initiates in a uniform transverse magnetic field where all qubits exist in a quantum superposition of circulating clock-wise and counter-clockwise states. As the transverse field is slowly diminished and the problem Hamiltonian is engaged, quantum tunneling allows the system to traverse non-convex energy barriers rather than climbing over them thermally. Using counterdiabatic driving and accelerated shortcuts to adiabaticity, the system settles into the global ground state, solving NP-hard logistics and portfolio problems in microseconds.",
        "The strategic implications of solving non-convex optimization problems have long fascinated intelligence cryptanalysts. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, Soviet cryptologic institutions recognized early on that mathematical encryption is fundamentally an optimization puzzle. The KGB's Eighth Chief Directorate, working alongside elite mathematicians in closed academic cities like Novosibirsk, continually sought hardware architectures capable of bypassing brute-force combinatorial limits to break Western diplomatic ciphers.",
        "According to Shvets, Soviet intelligence established clandestine cryogenic research groups in the late 1970s and 1980s, attempting to harness superconducting Josephson junction arrays for high-speed mathematical cryptanalysis. While primitive Soviet cleanrooms could not reliably fabricate dense, coherent multi-qubit lattices, their theoretical models accurately predicted that whichever superpower mastered quantum annealing would eventually possess the algorithmic capability to unmask complex cryptographic key schedules and decrypt stored Western defense communications.",
        "Today, quantum annealing has transitioned from academic theoretical physics into active defense production. Major aerospace contractors and national security laboratories are utilizing five-thousand-qubit Pegasus flux processors to optimize phased-array radar beam-forming, schedule autonomous multi-domain drone swarms, and execute real-time counter-stealth sensor fusion across contested theaters. In the accelerating arena of automated electronic warfare, whichever power calculates optimal solutions across non-linear conflict spaces first will irrevocably dominate the operational battlespace.",
        "Audit the dilution cryostats, master adiabatic shortcuts to the ground state, and refuse to let obsolete classical computational models compromise our strategic horizon. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="quantum_annealing")
    img.save(IMG_EP45, "WEBP", quality=92)
    print(f"Saved: {IMG_EP45}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP45, output_mp4, duration=10)
    
    # 3. Audio Synthesis (Rex Vance Baritone)
    print("[3/5] Synthesizing audio via edge-tts (ChristopherNeural)...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    
    actual_duration = get_audio_duration(audio_path)
    print(f"Audio synthesized: {audio_path} ({actual_duration}s)")
    EPISODE_DATA["seconds"] = actual_duration
    
    # 4. Synchronized Art Frames
    print("[4/5] Creating 6 synchronized art frames...")
    art_sources = [
        IMG_EP45,
        IMG_REX,
        IMG_EP45,
        IMG_STUDIO,
        IMG_EP45,
        IMG_REX
    ]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = actual_duration / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
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
    
    print(f"[+] Successfully produced Episode {EPISODE_DATA['id']} ({actual_duration}s)!")

if __name__ == "__main__":
    asyncio.run(main())
