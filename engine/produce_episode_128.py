# engine/produce_episode_128.py
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

IMG_EP128 = os.path.join(THUMBS_DIR, "2026-10-11-08.webp")
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
    "id": "2026-10-11-08",
    "hour": "08:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "quantum",
    "title": "Majorana Zero Modes, Non-Abelian Anyon Braiding & Soviet Cryogenic Cryptography",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates topological quantum computing, Majorana zero modes in semiconductor-superconductor nanowires, fault-tolerant quantum gates via non-Abelian anyon braiding, and Yuri Shvets on Soviet Kapitza Institute low-temperature physics research and KGB Eighth Chief Directorate cryogenic cryptographic hardware.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero eight hundred hours. Conventional quantum computers are notoriously fragile: a stray thermal photon or acoustic vibration collapses delicate superpositions, requiring thousands of physical qubits just to correct the errors of a single logical qubit. But inside condensed matter laboratories, physicists are pursuing the ultimate prize in fault-tolerant information: topological quantum computing. By engineering exotic quasiparticles that act as their own antiparticles—Majorana zero modes—quantum information is stored non-locally, rendering it impervious to local environmental noise.",
        "Majorana modes emerge at the interfaces of one-dimensional semiconductor nanowires with strong spin-orbit coupling, such as indium arsenide, coated with an epitaxial superconducting aluminum shell. When cooled to millikelvin temperatures inside dilution refrigerators and subjected to a precise longitudinal magnetic Zeeman field, the wire transitions into a topological superconducting phase. At zero energy, localized Majorana bound states appear at opposite ends of the nanowire. Because a single fermionic qubit is split across two physically separated spatial points, no local perturbation can flip the quantum state without simultaneously affecting both ends.",
        "Computation in topological systems is executed not through microwave pulses, but through non-Abelian braiding. By physically exchanging the positions of Majorana zero modes in a network of wire junctions, the system's ground state undergoes unitary transformations that depend solely on the topology of the worldline knot in spacetime. These braiding operations form topologically protected quantum logic gates with hardware error rates orders of magnitude lower than transmon qubits, creating an unhackable cryptographic computing architecture for defense and signals intelligence.",
        "This marriage of low-temperature physics and state cryptographic security has deep roots in Soviet strategic science. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, the Soviet defense establishment prioritized extreme-environment physics decades before modern quantum computing existed.",
        "According to Shvets, elite institutions like the Kapitza Institute for Physical Problems and the Landau Institute conducted classified research for the KGB Eighth Chief Directorate and military signals command. Shvets revealed that Soviet intelligence deployed specialized cryogenic hardware, including superconducting Josephson junction arrays and liquid helium chillers, inside hardened command bunkers and strategic ballistic missile submarines. The goal was to build electronic ciphers and ultra-sensitive magnetic anomaly sensors immune to electromagnetic pulses and electronic eavesdropping, establishing a Cold War foundation for modern topological hardware.",
        "From Soviet liquid helium cryptographic vaults to modern Majorana anyon braiding, the ultimate defense against signal interception is non-local quantum topology. When information is woven into the geometry of spacetime, no adversary can sever the knot from the outside. Braiding the worldlines, cool to fifteen millikelvin, and trust the topological gap. I'm Rex Vance. Keep your filters at absolute zero."
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
    img.save(IMG_EP128, "WEBP", quality=92)
    print(f"Saved: {IMG_EP128}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP128, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP128,
        IMG_STUDIO,
        IMG_EP128,
        IMG_REX,
        IMG_EP128,
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
        "audio": f"audio/{EPISODE_DATA['id']}.mp3",
        "thumb": f"thumbs/{EPISODE_DATA['id']}.webp",
        "cover_video": f"thumbs/{EPISODE_DATA['id']}.mp4"
    }
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    existing_ids = [ep["id"] for ep in manifest["episodes"]]
    if EPISODE_DATA["id"] in existing_ids:
        manifest["episodes"] = [ep for ep in manifest["episodes"] if ep["id"] != EPISODE_DATA["id"]]
        
    manifest["episodes"].insert(0, full_episode_entry)
    manifest["updated"] = "2026-10-06T14:35:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
