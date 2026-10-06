# engine/produce_episode_24.py
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

IMG_EP24 = os.path.join(THUMBS_DIR, "2026-10-07-00.webp")
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
    "id": "2026-10-07-00",
    "hour": "00:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Orbital QKD Downlinks, Deep-Space Laser Comms & Soviet Cosmic SIGINT Lineage",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes orbital quantum key distribution constellations and atmospheric decoherence alongside ex-KGB Major Yuri Shvets's revelations on Soviet space-based SIGINT interception architectures.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero hundred hours. Midnight in the geopolitical battlespace, where the race for unhackable quantum communications collides with orbital electronic warfare. Low Earth orbit has become the supreme high ground for cryptographic supremacy. Through spaceborne quantum key distribution satellites, defense ministries and intelligence cartels attempt to beam polarization-entangled photons across thousands of kilometers of vacuum, seeking to render strategic communications mathematically immune to cryptanalysis before adversarial quantum supercomputers crack RSA-4096.",
        "But space surveillance is not an invention of the twenty-first century. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, Soviet intelligence pioneered space-based SIGINT through secret directorate satellites and mountain interception arrays like the Lourdes SIGINT station in Cuba. Shvets revealed that Moscow's primary objective was never just reading unencrypted messages, but mapping the physical transmission corridors, signal attenuation profiles, and ground-station telemetry to prepare targeted electronic countermeasures.",
        "In free-space quantum key distribution, the fundamental adversary is not an eavesdropper listening on the wire—it is atmospheric turbulence. When a satellite beams a single-photon stream from a five-hundred-kilometer orbit down to an optical ground station, atmospheric beam wandering, scintillation, and photon absorption induce severe decoherence. A beam aperture that begins at thirty centimeters expands into a five-meter optical footprint at ground level. If an adversary positions a high-altitude drone or a high-gain collector within that perimeter, they can siphon off photons and induce quantum bit error rate spikes that force the entire link into blackout.",
        "This physical bottleneck explains why China's Micius satellite program and the Pentagon's Space Development Agency are racing to field dense low-Earth-orbit constellations with adaptive optics and inter-satellite crosslinks. By routing cryptographic keys through space vacuum rather than atmospheric boundaries, orbital networks minimize decoherence. But as Russian electronic warfare units test high-power ground-based blinding lasers at Krona facilities in the North Caucasus, the line between signal jamming and orbital anti-satellite warfare has effectively dissolved.",
        "Securing the next generation of orbital quantum communications requires deploying multi-layer hybrid encryption architectures. Space agencies must combine hardware-entangled quantum downlinks with post-quantum lattice-based algorithms, multi-path routing across distributed CubeSat meshes, and dynamic spatial filtering to reject hostile dazzling lasers. In orbital counter-intelligence, redundancy is survival: if an adversary blinds your primary optical downlink, your network must instantaneously reroute through deep-space relay nodes before the security key expires.",
        "Entangled photons travel at the speed of light, but they cannot outrun geopolitical realities. Trace the orbital telemetry, monitor the ground stations, and never forget that whoever controls the optical corridor controls the cryptographic frontier. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="orbital_qkd")
    img.save(IMG_EP24, "WEBP", quality=92)
    print(f"Saved: {IMG_EP24}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP24, output_mp4, duration=10)
    
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
        IMG_EP24,
        IMG_REX,
        IMG_EP24,
        IMG_STUDIO,
        IMG_EP24,
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
