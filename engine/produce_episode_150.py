# engine/produce_episode_150.py
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

IMG_EP150 = os.path.join(THUMBS_DIR, "2026-10-12-06.webp")
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
    "id": "2026-10-12-06",
    "hour": "06:00",
    "date": "2026-10-12",
    "kind": "hourly",
    "category": "geopolitics",
    "title": "Arctic Yamal LNG Shadow Fleets, Rosatom Icebreaker Chokepoints & Soviet Northern Sea Route Command",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the Russian Arctic shadow fleet hauling liquified natural gas from the Yamal Peninsula, Arc7 reinforced ice-class vessel sanction evasion, Rosatom's state monopoly on nuclear icebreaker piloting through the Vilkitsky Strait, and Yuri Shvets on Soviet Glavsevmorput militarized logistics and KGB Arctic maritime border surveillance.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero six hundred hours. Five hundred miles north of the Arctic Circle, on the frozen western shore of the Gulf of Ob, sits the industrial megalith of Sabetta: the production terminal for Yamal LNG and Arctic LNG Two. Designed to tap hundreds of billions of cubic meters of natural gas trapped beneath permafrost, this facility is Russia’s flagship energy frontier. But with Western sanctions banning port access, insurance coverage, and shipyard maintenance for Russian gas carriers, the Kremlin has deployed an unprecedented maritime gambit: an Arctic shadow fleet of reinforced ice-class LNG tankers navigating the treacherous Northern Sea Route.",
        "Navigating polar sea ice requires specialized Arc7 ice-class vessels, engineered with reinforced steel double hulls and specialized azipod thrusters capable of operating astern to crush ice ridges over two meters thick. Because Western and South Korean shipbuilders terminated joint venture contracts, Moscow has engaged in opaque corporate shell maneuvers across Dubai, Singapore, and Panama to mask tanker ownership and flag registrations, loading discounted cryogenic liquefied methane and ferrying it directly through the polar ice to Chinese industrial terminals.",
        "Yet transit across this Siberian shipping corridor is impossible without continuous state escort. Russian state atomic energy corporation Rosatom maintains an absolute legal and physical monopoly over the route, commanding a fleet of nuclear-powered icebreakers including the massive Project 22220 Arktika-class vessels. Rosatom charges exorbitant escort tariffs and dictates passage through key choke points like the Vilkitsky Strait and the New Siberian Islands, effectively converting an international sea lane into a sovereign Russian toll canal.",
        "This militarized control over Arctic navigation directly revives the historical structure of Soviet polar expansion. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Arctic logistics were always subordinated to Soviet defense doctrine and political police oversight.",
        "According to Shvets, the Chief Directorate of the Northern Sea Route—known as Glavsevmorput—operated during the Cold War not as a commercial shipping agency, but as an auxiliary arm of the Soviet Navy and the KGB Border Troops. Shvets revealed that every civil vessel transiting the Arctic was assigned KGB surveillance officers to monitor crew loyalty, conduct acoustic reconnaissance of Western submarines operating under polar ice sheets, and maintain secrecy around coastal SIGINT listening posts lining the Siberian archipelago.",
        "From Glavsevmorput’s militarized polar convoys in the twentieth century to modern Arc7 shadow tankers escorted by Rosatom nuclear icebreakers through the Kara Sea, the Northern Sea Route remains the Kremlin's ultimate strategic energy fortress. Track the AIS transponder spoofing, monitor the Vilkitsky ice leads, and stay sharp. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="yamal_icebreaker", title=EPISODE_DATA["title"])
    img.save(IMG_EP150, "WEBP", quality=92)
    print(f"Saved: {IMG_EP150}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP150, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP150,
        IMG_STUDIO,
        IMG_EP150,
        IMG_REX,
        IMG_EP150,
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
    manifest["updated"] = "2026-10-06T18:00:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
