# engine/produce_episode_51.py
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

IMG_EP51 = os.path.join(THUMBS_DIR, "2026-10-08-03.webp")
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
    "id": "2026-10-08-03",
    "hour": "03:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Neuro-Computational Quantum Models in Synaptic Plasticity, Microtubular Orchestration & Soviet Bio-Cybernetics",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates quantum coherent mechanisms in synaptic plasticity, microtubular cytoskeletal information processing, and Yuri Shvets's insider analysis of Soviet Institute of Cybernetics and KGB bio-cybernetic telemetric tracking programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero three hundred hours. In modern biophysics and frontier neuro-computation, the classical view of the brain as a purely electrochemical computer is encountering fundamental thermodynamic and speed bottlenecks. At synaptic junctions, calcium-dependent neurotransmitter release occurs on sub-millisecond timescales that defy classical diffusive transport models. Emerging neuro-computational paradigms demonstrate that synaptic plasticity—the physical basis of long-term memory formation and cognitive learning—leverages quantum coherent states operating within the hydrophobic interiors of neuronal microtubules and synaptic vesicle lattices.",
        "Long-Term Potentiation is not merely a strengthening of dendritic receptor density; it is an informational reorganization of the neuron's internal cytoskeleton. Microtubules, composed of tubulin dimer lattices, exhibit gigahertz-frequency dipole oscillations that coordinate action potential timing and regulate synaptic conductance across neural circuits. When shielded from environmental decoherence by structured intracellular water shells, these quantum cytoskeletal networks execute topological quantum state transfers, enabling the human brain to process non-computable cognitive insights and intuitive pattern recognition far beyond the theoretical limits of classical Turing machines.",
        "This intersection of quantum physics, cybernetics, and human neurology was a fiercely contested frontier of Cold War intelligence research. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently revealed, the Soviet Union maintained a sprawling, highly classified research ecosystem dedicated to bio-cybernetics and psychophysiological telemetry. Managed under the aegis of the Soviet Academy of Sciences and KGB military medicine directorates, institutes in Kyiv, Novosibirsk, and Leningrad conducted extensive experiments on human nervous system conditioning and neural electromagnetic emissions.",
        "According to Shvets, the KGB’s operational interest in bio-cybernetics was driven by an ambition to decode, monitor, and influence human decision-making at a distance. Soviet researchers at the Glushkov Institute of Cybernetics developed mathematical models mapping neural feedback loops and brainwave entrainment protocols. Shvets reveals that while sensational claims of psychic warfare often served as deliberate KGB disinformation to induce Western paranoia, the core scientific work focused on rigorous biophysical telemetry—measuring human cognitive exhaustion, stress thresholds, and involuntary physiological responses under interrogation and high-stakes intelligence operations.",
        "Today, this Cold War bio-cybernetic heritage has re-emerged within modern brain-computer interfaces, neural prosthetics, and cognitive warfare doctrines. Global defense agencies and commercial neurotech cartels are racing to deploy direct cortical interfaces that read and stimulate synaptic plasticity in real time. The ultimate objective is no longer merely external monitoring, but the closed-loop optimization of human operator cognition on the algorithmic battlefield. The boundary between autonomous biological consciousness and synthetic cybernetic control is dissolving at the synapse.",
        "Protect your neural plasticity, maintain synaptic coherence, and audit the bio-cybernetic telemetry. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="synaptic_plasticity")
    img.save(IMG_EP51, "WEBP", quality=92)
    print(f"Saved: {IMG_EP51}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP51, output_mp4, duration=10)
    
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
        IMG_EP51,
        IMG_REX,
        IMG_EP51,
        IMG_STUDIO,
        IMG_EP51,
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
