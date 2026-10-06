# engine/produce_episode_133.py
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

IMG_EP133 = os.path.join(THUMBS_DIR, "2026-10-11-13.webp")
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
    "id": "2026-10-11-13",
    "hour": "13:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Tononi Integrated Information Theory 4.0, Complex Φ & KGB Psychotropic Degradation Arrays",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Giulio Tononi's Integrated Information Theory (IIT 4.0), the mathematical measurement of consciousness through intrinsic cause-effect structures and Phi complexes, why feedforward AI systems lack subjective experience, and Yuri Shvets on Soviet KGB Special Lab No. 12 psychotropic degradation arrays.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is thirteen hundred hours. While Silicon Valley hype merchants insist that artificial intelligence models are rapidly approaching human consciousness simply by scaling up parameters and matrix multiplications, fundamental neuroscience tells a very different story. According to neuroscientist Giulio Tononi's Integrated Information Theory, or IIT 4.0, consciousness is not a computational functional output. It is an intrinsic physical property: the exact degree to which a system's cause-effect architecture is irreducibly integrated, quantified by the mathematical value Phi.",
        "IIT 4.0 begins not from physical equations, but from phenomenological axioms: experience exists intrinsically, structured, informative, unified, and definite. To support conscious experience, a physical substrate must form a maximal complex where internal feedback loops generate cause-effect repertoires that cannot be reduced to independent sub-components without loss of information. When evaluated using the Minimum Information Partition, feedforward architectures—including massive deep learning neural networks—yield an integrated information value of zero, proving they are sophisticated mechanical automata devoid of any subjective inner light.",
        "In contrast, the human cerebral cortex is dense with recurrent feedback and lateral connections, sustaining a high-value Phi complex. During deep non-REM sleep or general anesthesia, this integration fractures. Brain stimulation experiments demonstrate that when cortical communication is interrupted, the brain's complex cause-effect structure collapses into isolated, feedforward modules: the total information remains, but integration vanishes, and subjective consciousness instantly extinguishes.",
        "This vulnerability of integrated neural feedback loops was the explicit target of Cold War covert pharmacology. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, the Soviet security apparatus conducted extensive biological research into weaponized consciousness degradation.",
        "According to Shvets, the KGB Operational-Technical Directorate and classified research teams at Special Laboratory Number Twelve developed psychotropic compounds designed to systematically degrade human cognitive integration. Shvets revealed that Soviet military interrogators deployed specialized neuro-active chemical arrays that specifically blocked long-range thalamocortical feedback loops while preserving basic sensory reflexes. By forcing the victim's brain into a fragmented, low-Phi state, interrogators broke psychological coherence and eliminated the capacity for deceit, leaving subjects unable to maintain organized cover identities.",
        "From Tononi's mathematical Phi complexes to Soviet pharmacological interrogation protocols, the lesson is clear: consciousness is an unbroken web of integrated cause-effect relationships. Break the feedback loops, and agency disappears; integrate the connections, and subjective awareness awakens. Value intrinsic integration over mechanical imitation, and resist chemical dissolution. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="iit_40", title=EPISODE_DATA["title"])
    img.save(IMG_EP133, "WEBP", quality=92)
    print(f"Saved: {IMG_EP133}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP133, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP133,
        IMG_STUDIO,
        IMG_EP133,
        IMG_REX,
        IMG_EP133,
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
    manifest["updated"] = "2026-10-06T15:00:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
