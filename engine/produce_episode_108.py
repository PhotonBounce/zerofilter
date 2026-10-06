# engine/produce_episode_108.py
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

IMG_EP108 = os.path.join(THUMBS_DIR, "2026-10-10-12.webp")
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
    "id": "2026-10-10-12",
    "hour": "12:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "quantum",
    "title": "Majorana Zero Modes in Hybrid Nanowires, Non-Abelian Braiding & Soviet Landau Cryogenics",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates topological quantum computing breakthrough claims in semiconductor-superconductor hybrid nanowires, non-Abelian anyon braiding for fault-tolerant qubits, and Yuri Shvets on Soviet Landau Institute cryogenic intelligence programs.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is twelve hundred hours. In the global race for fault-tolerant quantum computing, conventional superconducting transmons and trapped ions remain plagued by environmental decoherence and catastrophic error cascades. To build machines capable of breaking modern public-key cryptography, defense research laboratories are turning toward topological quantum computing: encoding logical qubits into non-local topological states using Majorana zero modes that emerge at the physical boundaries of semiconductor-superconductor hybrid nanowires.",
        "Majorana zero modes are exotic quasi-particles governed by non-Abelian exchange statistics, meaning that exchanging two modes alters the quantum state of the system in a path-dependent, topological manner rather than merely adding a phase factor. By coupling high spin-orbit semiconductor nanowires—such as indium antimonide or indium arsenide—to epitaxial aluminum superconducting shells under precise magnetic Zeeman fields, condensed matter physicists induce topological superconductivity. Zero-bias conductance peaks at wire boundaries signify the emergence of isolated Majorana modes whose spatial separation renders the encoded quantum information immune to local thermal and electrical fluctuations.",
        "This theoretical foundation traces its conceptual lineage directly to Soviet low-temperature physics and espionage networks that sustained Moscow during the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet solid-state physics relied heavily on the legendary Landau Institute for Theoretical Physics and Kapitza Institute for Physical Problems to crack macroscopic quantum mechanics when Soviet microelectronics manufacturing collapsed.",
        "According to Shvets, the KGB First Chief Directorate's Directorate T maintained dedicated scientific intelligence officers tracking Western cryogenic and solid-state laboratories. Soviet physicists understood that they could never match Western sub-micron silicon yields, leading Soviet defense planners to aggressively pursue topological and cryogenic quantum phenomena as asymmetric shortcuts. Shvets disclosed that KGB operatives routinely targeted international low-temperature physics conferences in Zurich and Helsinki, seeking Western dilution refrigeration blueprints and superconductivity preprints to feed closed military research institutes in Chernogolovka.",
        "Today, the strategic stakes have evolved from theoretical paper exchanges to billion-dollar national security imperatives. Major defense contractors and intelligence agencies recognize that topological anyon braiding represents the ultimate hardware-level quantum error correction, bypassing millions of fragile physical error-mitigation qubits. The nation that first realizes scalable non-Abelian braiding will achieve unconstrained cryptanalytic dominance over classical and post-quantum encryption standards alike, rendering current classified signal archives transparent to non-local quantum decoding.",
        "Demand rigorous experimental replication over press release hype, verify zero-bias conductance signatures against trivial disorder states, and remember that when quantum computation becomes topological, geometry itself becomes the cryptographic battleground. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="majorana_zero_modes", title=EPISODE_DATA["title"])
    img.save(IMG_EP108, "WEBP", quality=92)
    print(f"Saved: {IMG_EP108}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP108, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP108,
        IMG_STUDIO,
        IMG_EP108,
        IMG_REX,
        IMG_EP108,
        IMG_STUDIO
    ]
    create_art_frames(EPISODE_DATA["id"], src_frames)
    
    # 4. Neural Voice Audio Synthesis
    print("[4/5] Synthesizing neural voice (Rex Vance via edge-tts)...")
    full_script = " ... \n\n ".join(EPISODE_DATA["paragraphs"])
    mp3_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, mp3_path)
    actual_seconds = get_audio_duration(mp3_path)
    print(f"Synthesized Rex Vance audio: {mp3_path} ({actual_seconds}s)")
    
    # 5. Manifest & Metadata Registration
    print("[5/5] Registering in episodes.json...")
    t_step = actual_seconds / 6.0
    frame_times = [int(round(i * t_step)) for i in range(6)]
    
    full_episode_entry = {
        "id": EPISODE_DATA["id"],
        "hour": EPISODE_DATA["hour"],
        "date": EPISODE_DATA["date"],
        "kind": EPISODE_DATA["kind"],
        "category": EPISODE_DATA["category"],
        "title": EPISODE_DATA["title"],
        "subject": EPISODE_DATA["subject"],
        "paragraphs": EPISODE_DATA["paragraphs"],
        "art": {
            "frames": [
                {"t": frame_times[i], "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
                for i in range(6)
            ]
        },
        "seconds": actual_seconds,
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    # Prepend new episode if not already present
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
    
    manifest["episodes"].insert(0, full_episode_entry)
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully published Episode {EPISODE_DATA['id']} to manifest ({len(manifest['episodes'])} episodes total).")

if __name__ == "__main__":
    asyncio.run(main())
