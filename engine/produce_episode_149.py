# engine/produce_episode_149.py
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

IMG_EP149 = os.path.join(THUMBS_DIR, "2026-10-12-05.webp")
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
    "id": "2026-10-12-05",
    "hour": "05:00",
    "date": "2026-10-12",
    "kind": "hourly",
    "category": "consciousness",
    "title": "Stuart Hameroff Quantum Microtubule Anesthesia, Xenon Dipoles & Soviet Neuro-Aerosol Telemetry",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates Dr. Stuart Hameroff and Sir Roger Penrose's Orch-OR theory of quantum consciousness, volatile anesthetic gas binding inside tubulin hydrophobic pockets, terahertz dipole oscillation dampening, and Yuri Shvets on Soviet KGB Directorate S / Lab-12 aerosol neuro-pharmacology programs targeting rapid brainstem consciousness collapse.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is zero five hundred hours. For over a century, clinical neurobiology has struggled to explain the fundamental physical mystery of general anesthesia: how structurally diverse, chemically inert gases—ranging from elemental noble gas xenon to fluorinated ethers like isoflurane and sevoflurane—can selectively extinguish subjective conscious experience while leaving autonomic brainstem cardiorespiratory functions intact. Classical neuroscience pointed vaguely to synaptic receptor blockade, but the Meyer-Overton correlation demonstrated that anesthetic potency correlates strictly with solubility in nonpolar, hydrophobic environments. Inside the brain, that critical environment is not the cell membrane, but the interior of neuronal microtubules.",
        "Renowned anesthesiologist Dr. Stuart Hameroff and mathematical physicist Sir Roger Penrose demonstrated that consciousness arises not from classical axonal firing rates, but from quantum optical and dipole computations orchestrated within the neuronal cytoskeleton. Microtubules—cylindrical lattice polymers composed of thirteen protofilaments of alpha and beta tubulin protein heterodimers—host nonpolar hydrophobic pockets where aromatic amino acids like tryptophan and tyrosine form delocalized pi-electron resonance rings. These hydrophobic channels oscillate in coherent terahertz dipole frequencies, creating topological quantum optical networks protected from thermal decoherence.",
        "Volatile anesthetics bind inside these exact hydrophobic quantum pockets through ultra-weak London dispersion van der Waals forces. Even chemically inert xenon gas, lacking any permanent electric dipole, possesses a highly polarizable outer electron shell that inserts into the tubulin cavity. Once nested inside, anesthetic molecules physically dampen the terahertz dipole oscillations, decoupling the quantum collective resonance required for conscious awareness without arresting underlying metabolic cellular respiration.",
        "This precise pharmacological mechanism of rapid consciousness disruption was intensively researched as a covert weapon throughout the Cold War. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has documented, Soviet intelligence maintained specialized biochemical laboratories focused on rapid consciousness suppression and tactical neuro-incapacitation.",
        "According to Shvets, the KGB’s clandestine technical divisions—most notably the notorious Lab Twelve and Directorate S—developed weaponized aerosol formulations combining volatile anesthetics, ultra-potent fentanyl derivatives, and xenon gas to induce immediate neuro-paralytic incapacitation. Shvets revealed that Soviet military biochemists mapped the exact threshold dosages needed to knock out human cortical awareness in enclosed tactical environments, an experimental doctrine that ultimately surfaced decades later during the catastrophic Dubrovka Theater raid in Moscow.",
        "From the quantum hydrophobic cores of tubulin protofilaments to Soviet aerosol neuro-telemetry, the science of anesthesia reveals that human consciousness is a delicate quantum optical state vulnerable to molecular dampening. Track the terahertz resonance, audit the neuro-pharmacology, and stay conscious. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="orch_or_anesthesia", title=EPISODE_DATA["title"])
    img.save(IMG_EP149, "WEBP", quality=92)
    print(f"Saved: {IMG_EP149}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP149, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP149,
        IMG_STUDIO,
        IMG_EP149,
        IMG_REX,
        IMG_EP149,
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
    manifest["updated"] = "2026-10-06T17:45:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
