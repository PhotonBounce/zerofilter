# engine/produce_episode_39.py
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

IMG_EP39 = os.path.join(THUMBS_DIR, "2026-10-07-15.webp")
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
    "id": "2026-10-07-15",
    "hour": "15:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "consciousness",
    "title": "PEAR Field Effects, Cognitive Entanglement & KGB Psychic Research Diverts",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes Princeton PEAR laboratory quantum noise random event generators, non-local FieldREG collective entropy decreases, and Yuri Shvets's insider revelations regarding Soviet KGB psychotronics black-budget diversion schemes.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is fifteen hundred hours. For nearly three decades inside Princeton University's School of Engineering and Applied Science, the Princeton Engineering Anomalies Research program, or PEAR, conducted rigorous, double-blind laboratory trials on human-machine interaction. Led by former aerospace dean Robert Jahn and developmental psychologist Brenda Dunne, the laboratory amassed millions of experimental trials using microelectronic random event generators driven by intrinsically unpredictable quantum tunnel diode shot noise, seeking to determine whether human intention could alter physical entropy.",
        "Their findings were mathematically staggering: across hundreds of volunteer human operators attempting to mentally bias binary random sequences, the cumulative statistical departure from theoretical chance achieved an overall p-value exceeding four standard deviations. When deployed as portable FieldREG units during high-coherence collective global gatherings, these quantum noise diodes recorded synchronous entropy drops—suggesting that conscious human awareness generates an objective, non-local field capable of subtly structuring quantum probability distributions across space.",
        "During the height of the Cold War, this intersection of mind and matter triggered intense intelligence competition and bureaucratic hysteria. As Washington counter-intelligence insider and former KGB Major Yuri Shvets has revealed, Soviet state security apparatuses were thoroughly consumed by parapsychological rivalries. Within the First Chief Directorate, opportunistic officers and pseudo-scientific researchers established highly classified psychotronic laboratories, claiming they could weaponize remote sensory disruption and psychokinetic sabotage against Western political leadership.",
        "Yet Shvets emphasizes that the vast majority of Soviet psychotronics was not rigorous science; it was an elaborate bureaucratic grift. Corrupt KGB managers leveraged Politburo paranoia regarding American technological breakthroughs to secure immense, unvouchered black-budget allocations. In turn, American intelligence analysts intercepted Soviet disinformation regarding psychotronic weapons, panicked, and pressured the Pentagon to pour millions into Project Stargate and SRI International—creating a self-reinforcing geopolitical feedback loop of manufactured psychic warfare.",
        "Separating genuine quantum cognitive anomalies from cynical intelligence disinformation is the ultimate mandate of ZeroFilter. While corrupt security bureaucracies routinely exploit the unknown to embezzle public funds and sow psychological paranoia, rigorous empirical physics—like the archival PEAR trials—demonstrates that mind and physical reality share profound, non-local quantum underpinnings. The future of science belongs not to authoritarian superstition, but to fearless mathematical investigation.",
        "Audit the cumulative deviation envelopes, discard the intelligence grift, and recognize the non-local reach of conscious intention. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="pear_reg")
    img.save(IMG_EP39, "WEBP", quality=92)
    print(f"Saved: {IMG_EP39}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP39, output_mp4, duration=10)
    
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
        IMG_EP39,
        IMG_REX,
        IMG_EP39,
        IMG_STUDIO,
        IMG_EP39,
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
