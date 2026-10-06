# engine/produce_episode_53.py
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

IMG_EP53 = os.path.join(THUMBS_DIR, "2026-10-08-05.webp")
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
    "id": "2026-10-08-05",
    "hour": "05:00",
    "date": "2026-10-08",
    "kind": "hourly",
    "category": "quantum",
    "title": "Cavity Quantum Electrodynamics in Photonic Microresonators, Vacuum Rabi Splitting & Soviet Atomic Spectroscopy",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates cavity quantum electrodynamics in ultra-high-Q photonic microresonators, vacuum Rabi splitting and polaritonic state transfers, and Yuri Shvets's insider analysis of Soviet atomic laser spectroscopy surveillance and closed-city optics acquisition.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero five hundred hours. At the extreme limits of quantum optics, Cavity Quantum Electrodynamics allows physicists to trap and manipulate individual quanta of light with unprecedented precision. By confining single photons within ultra-high-Q photonic microresonators—such as whispering-gallery microtoroids and photonic crystal defect cavities—the local electromagnetic vacuum field becomes intensely concentrated. When a single atom or quantum dot is positioned inside this mode volume, the interaction rate exceeds the decay rates of both the cavity and the atom, thrusting the system into the regime of strong light-matter coupling.",
        "Under strong coupling, the photon and atom lose their individual identities, hybridizing into entangled polaritonic states. This coherent energy exchange manifests experimentally as vacuum Rabi splitting—a spectral doublet where the resonance peak bifurcates in response to the presence of a single photon. This microscopic quantum entanglement enables single-photon optical transistors, deterministic quantum phase gates, and non-destructive photon number counters. Operating at room temperature in integrated on-chip silicon photonics, cavity QED architectures bypass the cryogenic bulk of superconducting qubits, establishing the physical foundation for unjammable optical quantum memory networks and quantum key distribution routing.",
        "The geopolitical pursuit of laser physics and atomic spectroscopy has a deep intelligence lineage. As former KGB foreign intelligence officer and Washington counter-intelligence insider Yuri Shvets has frequently detailed, Soviet scientific intelligence placed laser frequency stabilization and atomic spectroscopy at the very center of its military-technical acquisition directives. Through the 1970s and 1980s, the KGB’s Directorate T targeted Western laser laboratories to acquire precision optics for missile defense, isotope separation, and clandestine remote audio surveillance.",
        "According to Shvets, Soviet closed cities and elite military research institutes—such as Arzamas-16, the Lebedev Physical Institute, and Sary-Shagan—depended heavily on Western technical literature and smuggled optical components to develop their own high-power gas dynamic and solid-state lasers. Shvets reveals that Soviet intelligence prioritized atomic spectroscopy not just for nuclear enrichment diagnostics, but for anti-satellite optical tracking and long-range airborne chemical weapon detection. The race to achieve optical frequency precision was viewed in Moscow as a critical prerequisite for achieving strategic nuclear parity.",
        "Today, cavity QED has transformed atomic laser spectroscopy into a sovereign intelligence asset. Sovereign defense laboratories and intelligence agencies are racing to weaponize microresonators into chip-scale atomic clocks, quantum gravimeters for subterranean tunnel detection, and ultra-sensitive photonic sensors capable of intercepting fiber-optic communications without inducing measurable signal attenuation. What began in twentieth-century physics laboratories as basic quantum electrodynamics has matured into the operational backbone of next-generation signals intelligence.",
        "Measure the vacuum Rabi splitting, calibrate your microcavities, and audit the optical frequency channels. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="cavity_qed")
    img.save(IMG_EP53, "WEBP", quality=92)
    print(f"Saved: {IMG_EP53}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP53, output_mp4, duration=10)
    
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
        IMG_EP53,
        IMG_REX,
        IMG_EP53,
        IMG_STUDIO,
        IMG_EP53,
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
