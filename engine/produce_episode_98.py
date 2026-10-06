# engine/produce_episode_98.py
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

IMG_EP98 = os.path.join(THUMBS_DIR, "2026-10-10-02.webp")
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
    "id": "2026-10-10-02",
    "hour": "02:00",
    "date": "2026-10-10",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Kuril Islands Bastion Fortification, Sea of Okhotsk Anti-Access Gates & Soviet Pacific Fleet ASW Doctrine",
    "subject": "Hourly uncensored breakdown: Rex Vance examines the strategic fortification of the Kuril Islands chain turning the Sea of Okhotsk into an impenetrable ballistic missile submarine sanctuary, and Yuri Shvets on Soviet Pacific Fleet bastion defense architecture.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero two hundred hours. In Pacific naval strategy, geography dictates oceanic chokepoints with brutal clarity. While global maritime attention remains fixated on the First Island Chain and the Taiwan Strait, a far more militarized anti-access bastion has locked down the Northwest Pacific. Spanning twelve hundred kilometers from the Kamchatka Peninsula to northern Hokkaido, the Kuril Islands archipelago serves as a natural volcanic wall, converting the entire Sea of Okhotsk into a fortified sovereign naval bastion.",
        "The military geography of the Sea of Okhotsk is engineered around an asymmetric defensive objective: protecting Russian nuclear ballistic missile submarines from Western anti-submarine warfare penetration. Through the deployment of K-300P Bastion-P supersonic coastal anti-ship missile complexes on Matua and Paramushir islands, paired with long-range S-400 air defense batteries, the transit straits have been transformed into lethal interception gates. Any hostile surface combatant or maritime patrol aircraft attempting to penetrate deep straits like Bussol or Kruzenstern faces multi-tiered hypersonic crossfire.",
        "This contemporary bastion doctrine represents the direct execution of plans formulated during the height of the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has illuminated, the Soviet General Staff and the KGB's Third Chief Directorate for military counter-intelligence viewed the Pacific Fleet's submarine sanctuary in the Sea of Okhotsk as an indispensable pillar of nuclear survivability.",
        "According to Shvets, Soviet intelligence was gripped by deep alarm over US Navy maritime strategy under Admiral James Watkins in the 1980s, which explicitly planned for American attack submarines to breach Soviet bastions and hunt Delta-class SSBNs during the opening hours of a conflict. In response, the Kremlin directed immense defense resources toward lining the Kuril trenches with deep-water stationary hydrophone arrays and acoustic tripwires. Shvets noted that Soviet Pacific Fleet commanders considered losing control over a single Kuril passage an existential vulnerability to their second-strike deterrent.",
        "Today, that acoustic fortification is being aggressively modernized with autonomous subsea gliders, seabed sonar nodes, and Tu-142 maritime reconnaissance patrols. As geopolitical tensions rise across East Asia, Moscow's refusal to negotiate Kuril sovereignty with Tokyo reflects not diplomatic stubbornness, but raw naval physics: relinquishing the southern islands would rupture the acoustic perimeter, allowing Allied nuclear attack submarines unmonitored entry into the Pacific Fleet's primary underwater redoubt.",
        "Map the maritime choke points, track the deployment of hypersonic coastal defense batteries along the volcanic island arc, and understand that in modern naval warfare, natural geography remains the ultimate force multiplier. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="kuril_bastion", title=EPISODE_DATA["title"])
    img.save(IMG_EP98, "WEBP", quality=92)
    print(f"Saved: {IMG_EP98}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP98, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP98, IMG_REX, IMG_STUDIO, IMG_EP98, IMG_REX, IMG_EP98]
    create_art_frames(EPISODE_DATA["id"], art_sources)
    
    # 4. Neural Audio Synthesis
    print("[4/5] Synthesizing Rex Vance neural baritone audio...")
    full_script = " ".join(EPISODE_DATA["paragraphs"])
    audio_path = os.path.join(AUDIO_DIR, f"{EPISODE_DATA['id']}.mp3")
    await synthesize_rex_vance(full_script, audio_path)
    dur = get_audio_duration(audio_path)
    print(f"Synthesized Audio: {audio_path} ({dur} seconds)")
    
    # Calculate art frame timestamps based on actual audio duration
    p_step = dur / 6.0
    EPISODE_DATA["art"] = {
        "frames": [
            {"t": round(i * p_step), "src": f"art/{EPISODE_DATA['id']}/f0{i+1}.webp"}
            for i in range(6)
        ]
    }
    EPISODE_DATA["seconds"] = dur
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
    print(f"Updated {MANIFEST_FILE} with episode {EPISODE_DATA['id']}!")
    
    # Copy cover to brain artifacts for documentation
    brain_cover = r"assets\cover_ep98_procedural.webp"
    with Image.open(IMG_EP98) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
