# engine/produce_episode_83.py
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

IMG_EP83 = os.path.join(THUMBS_DIR, "2026-10-09-11.webp")
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
    "id": "2026-10-09-11",
    "hour": "11:00",
    "date": "2026-10-09",
    "kind": "hourly",
    "category": "corruption",
    "title": "Defense Cloud Procurement Collusion, FISA 702 Warrantless Carve-Outs & KGB OTU Wiretap Slush Funds",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates sole-source defense cloud contracting cartels, FISA Section 702 warrantless intelligence database carve-outs, and Yuri Shvets on KGB 12th Department OTU surveillance kickbacks.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eleven hundred hours. Over the past decade, the Pentagon's multi-billion-dollar migration to commercial enterprise cloud infrastructure has been marketed as a vital modernization initiative to ensure digital battlefield superiority. However, behind the press releases for programs like the Joint Warfighting Cloud Capability, or JWCC, lies an entrenched procurement cartel. Legacy defense contractors and dominant Big Tech hyperscalers have orchestrated a closed ecosystem where lucrative cloud hosting contracts are carved up among a protected oligopoly, completely freezing out innovative commercial alternatives.",
        "This procurement collusion is not merely about financial rent-seeking; it is inextricably bound to mass domestic electronic surveillance. By consolidating Department of Defense, NSA, and intelligence community data lakes into centralized commercial cloud repositories, federal agencies exploit statutory carve-outs under Section 702 of the Foreign Intelligence Surveillance Act. Through clandestine fiber-optic splitters and warrantless backdoor database queries, intelligence analysts routinely query the private telecommunications of millions of American citizens without Fourth Amendment probable cause warrants, shielded behind classified Special Access Program NDAs.",
        "This convergence of centralized telecommunications monopolies and state surveillance is the direct Western realization of the technical police state perfected in the Soviet Union. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has frequently disclosed, the KGB's Operational-Technical Directorate, or OTU, and its Twelfth Department operated total monopoly control over all Soviet telecommunications routing and telephone exchanges. No wireline or radio-relay network could be deployed without classified OTU hardware backdoors.",
        "According to Shvets, the KGB's technical surveillance monopoly became one of the most corrupt revenue engines in the Soviet bureaucracy. OTU bureau chiefs demanded massive secret kickbacks from state telecom enterprises to certify hardware as ideologically secure, siphoning millions into clandestine First Chief Directorate operational slush funds. Shvets revealed that corrupt intelligence chiefs routinely used warrantless wiretap files not for legitimate national counter-intelligence, but to blackmail political rivals and protect illegal black-market party embezzlement schemes from state prosecutors.",
        "When Silicon Valley defense primes lobby Congress to reauthorize FISA 702 while securing ten-figure defense cloud contracts, they are perpetuating this exact feedback loop. State surveillance power is traded for monopolistic commercial wealth, transforming democratic digital infrastructure into an unaccountable national security panopticon.",
        "Audit the JWCC cloud procurement ledgers, trace the FISA 702 warrantless queries, and demand unredacted NSA database logs. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="defense_cloud_fisa")
    img.save(IMG_EP83, "WEBP", quality=92)
    print(f"Saved: {IMG_EP83}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    output_mp4 = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP83, output_mp4, duration=10)
    
    # 3. Synchronized Story Art Frames
    print("[3/5] Generating 6 synchronized art frames...")
    art_sources = [IMG_EP83, IMG_REX, IMG_STUDIO, IMG_EP83, IMG_REX, IMG_EP83]
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
    brain_cover = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\66020d49-6cff-42bb-95f3-234ac272d8bc\cover_ep83_procedural.webp"
    with Image.open(IMG_EP83) as im:
        im.save(brain_cover, "WEBP", quality=92)
    print(f"Copied procedural cover to brain: {brain_cover}")

if __name__ == "__main__":
    asyncio.run(main())
