# engine/produce_episode_27.py
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

IMG_EP27 = os.path.join(THUMBS_DIR, "2026-10-07-03.webp")
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
    "id": "2026-10-07-03",
    "hour": "03:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "quantum",
    "title": "Wheeler's Smoky Dragon, Retrocausality & Deep-Cover Illegal Infiltration Rings",
    "subject": "Hourly uncensored breakdown: Rex Vance explores John Archibald Wheeler's smoky dragon quantum delayed-choice paradox alongside ex-KGB Major Yuri Shvets's revelations regarding Directorate S illegal deep-cover networks embedded inside Western nuclear and quantum physics laboratories.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero three hundred hours. In John Archibald Wheeler's iconic formulation of quantum mechanics, a photon traveling from an ancient quasar to an earthbound telescope is like a great smoky dragon: we see the tail where the photon entered the beam-splitter, and we see the teeth where it hits the detector, but the body in between is an unobservable cloud of pure potentiality. Until the measurement choice is executed in the present, the historical path of the particle remained completely unfixed. The present choice retroactively dictates whether the past took one route or both.",
        "In the operational tradecraft of Soviet intelligence, this smoky dragon metaphor describes the anatomy of an illegal deep-cover network. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has documented, Directorate S specialized in planting sleeper operatives—known as 'illegals'—under stolen identities of deceased Western infants. For decades, these agents established benign academic credentials, infiltrating prestigious European and American physics research centers to observe sensitive quantum and nuclear developments from the inside without generating an active intelligence signature.",
        "In delayed-choice retrocausality experiments, the measurement apparatus acts as the boundary condition that collapses the historical wave function. In counter-espionage investigations, an illegal operative functions identically. They remain passive quantum potential—sleeping quietly in academic tenure tracks—until a high-priority geopolitical activation order forces a sudden operational measurement. The moment they transmit classified telemetry, the entire historical timeline of their associations, publications, and graduate student placements must be retroactively audited and reinterpreted through the lens of counter-intelligence.",
        "This counter-intelligence vulnerability has grown exponentially as nation-states race for quantum computing and sensing primacy. From the Klaus Fuchs and Manhattan Project spy rings to modern talent recruitment pipelines operating through ostensibly civilian scientific exchange programs, foreign intelligence services exploit the open, collaborative ethos of academic physics departments. Western universities conduct groundbreaking research on topological qubits, neutral atom arrays, and cryogenic control systems, while adversarial shell entities quietly recruit postdoctoral researchers and divert dual-use blueprints.",
        "Securing the quantum frontier against deep-cover academic infiltration requires dismantling the naive distinction between fundamental basic research and national security technologies. We must implement cryptographic identity verification for laboratory access, zero-trust provenance logging on dual-use simulation code, and rigorous foreign talent disclosure audits. In quantum mechanics, observing a system alters its state; in laboratory counter-intelligence, persistent auditing of funding corridors collapses illicit espionage channels before intellectual property crosses international borders.",
        "Wheeler's smoky dragon reminds us that what appears to be an innocent academic path may conceal a decisive hidden trajectory. Question the past, audit the laboratories, and never mistake passive silence for innocent neutrality. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="smoky_dragon")
    img.save(IMG_EP27, "WEBP", quality=92)
    print(f"Saved: {IMG_EP27}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP27, output_mp4, duration=10)
    
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
        IMG_EP27,
        IMG_REX,
        IMG_EP27,
        IMG_STUDIO,
        IMG_EP27,
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
