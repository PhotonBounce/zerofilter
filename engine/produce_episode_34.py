# engine/produce_episode_34.py
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

IMG_EP34 = os.path.join(THUMBS_DIR, "2026-10-07-10.webp")
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
    "id": "2026-10-07-10",
    "hour": "10:00",
    "date": "2026-10-07",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Suwalki Gap Electronic Warfare, Kaliningrad Nuclear Bluffs & Reflexive Escalation",
    "subject": "Hourly uncensored breakdown: Rex Vance analyzes the sixty-mile Suwalki corridor choke point between Belarus and Kaliningrad, high-power Murmansk-BN electronic warfare jamming corridors, and Yuri Shvets's insider revelations regarding Russian General Staff escalatory threshold deception.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is ten hundred hours. NATO's most precarious geographic artery is a narrow sixty-mile strip of land connecting Poland and Lithuania: the Suwalki Gap. Pinched directly between heavily militarized Belarus to the southeast and Russia's Baltic naval exclave of Kaliningrad to the northwest, this corridor represents the sole overland logistics conduit linking Western Europe to the three Baltic states. In any high-intensity conflict, closing this gap cuts off Estonia, Latvia, and Lithuania from land reinforcement in under seventy-two hours.",
        "Yet the battle for the Suwalki Gap is already being fought silently in the electromagnetic spectrum. Russian forces deployed in Kaliningrad operate cutting-edge electronic warfare complexes, including the Krasukha-4 and the ultra-long-range Murmansk-BN system. Over the past twelve months, commercial airliners flying Baltic transit corridors have reported pervasive GPS spoofing, synthetic transponder drift, and loss of satellite communication. This is not incidental spillover; it is an active military trial designed to blind NATO command and control before armor ever moves.",
        "As Washington counter-intelligence insider and former KGB Major Yuri Shvets has repeatedly documented, Kremlin military strategy operates on the doctrine of reflexive escalation control. Whenever Moscow perceives a conventional disadvantage along its western periphery, the General Staff executes theatrical nuclear signaling—stationing nuclear-capable Iskander-M missiles in Kaliningrad, conducting unannounced tactical warhead deployment drills, and issuing apocalyptic rhetorical threats. Shvets emphasizes that these displays are calculated mathematical bluffs designed to induce policy paralysis in Western capitals.",
        "The strategic goal of reflexive nuclear posturing is to exploit democratic risk aversion. By convincing Western decision-makers that defending the Suwalki Gap risks uncontrolled thermonuclear escalation, Moscow seeks to fracture NATO's Article Five deterrence architecture without firing a single missile. The Kremlin understands that deterrence does not collapse when an adversary strikes; it collapses the moment allied leadership hesitates out of manufactured fear.",
        "Neutralizing this escalatory bluff requires uncompromising deterrence and asymmetric reinforcement. NATO must permanently forward-deploy mechanized multinational brigade combat teams directly inside the Suwalki corridor, harden civilian and military avionics against electronic warfare jamming, and deploy counter-battery systems capable of neutralizing Kaliningrad's missile batteries within minutes of an offensive launch. True peace is preserved not by appeasing threats, but by making aggression mathematically unviable.",
        "Audit the electronic warfare corridors, expose the reflexive nuclear theater, and never surrender a single inch of sovereign territory to manufactured fear. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="suwalki_gap")
    img.save(IMG_EP34, "WEBP", quality=92)
    print(f"Saved: {IMG_EP34}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP34, output_mp4, duration=10)
    
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
        IMG_EP34,
        IMG_REX,
        IMG_EP34,
        IMG_STUDIO,
        IMG_EP34,
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
