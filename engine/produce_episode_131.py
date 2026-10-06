# engine/produce_episode_131.py
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

IMG_EP131 = os.path.join(THUMBS_DIR, "2026-10-11-11.webp")
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
    "id": "2026-10-11-11",
    "hour": "11:00",
    "date": "2026-10-11",
    "kind": "hourly",
    "category": "corruption",
    "title": "Pentagon Unacknowledged SAP Carve-Outs, Audit Waiver Networks & Soviet Slush Funds",
    "subject": "Hourly uncensored breakdown: Rex Vance investigates the Pentagon's multi-trillion-dollar accounting black hole, Unacknowledged Special Access Programs (USAPs), FASAB Statement 56 financial obfuscation rules, statutory reporting waivers under Title 10 Section 119, and Yuri Shvets on Soviet Ministry of Defense off-the-books slush funds and Gosplan diversion conduits.",
    "paragraphs": [
        "Welcome back to ZeroFilter. It is eleven hundred hours. For seven consecutive fiscal years, the Department of Defense has failed its independent financial audit, unable to account for over half of its four trillion dollars in physical and capital assets. While mainstream media depicts this as bureaucratic incompetence, forensic accountants know better: the black hole is an engineered architectural feature. Deep inside the defense appropriations machinery lies a legal mechanism designed to bypass constitutional oversight entirely: Unacknowledged Special Access Programs, or USAPs.",
        "Governed by statutory carve-outs under Title Ten, Section One Hundred Nineteen of the United States Code, unacknowledged SAPs are classified to such extreme levels that their very existence is denied to all but an eight-member congressional gang. Behind this firewall, prime defense contractors operate shadow balance sheets shielded by Federal Accounting Standards Advisory Board Statement Fifty-Six. Under Statement Fifty-Six, federal agencies are legally authorized to falsify, redact, and misstate financial statements to prevent the disclosure of sensitive national security programs, turning public accounting ledgers into legalized fiction.",
        "Under the cover of these classified reporting waivers, hundreds of billions in pass-through appropriations flow directly to private defense conglomerates. Aerospace giants bill the government under cost-plus overhead structures where classified subcontractors submit unitemized invoices for phantom components, black-site facility leases, and proprietary testing programs that can never be audited by the Government Accountability Office. When an accounting system explicitly permits false bookkeeping entries, corruption is no longer a bug—it is the operational doctrine.",
        "This institutionalized evasion of fiscal oversight is the direct ideological heir to Soviet defense budget obfuscation. As former KGB foreign intelligence officer and Washington counter-intelligence analyst Yuri Shvets has exposed, the Soviet defense apparatus operated under identical off-the-books accounting mechanisms to conceal massive resource misallocations.",
        "According to Shvets, the Soviet Ministry of Defense, working alongside the KGB and Gosplan, maintained sprawling classified off-budget accounts known as Special Purpose Slush Funds. Shvets revealed that military design bureaus and manufacturing directors routinely siphoned hard-currency reserves and strategic materials into shadow accounts, masking operational cost overruns and funding covert foreign operations without Central Committee oversight. Because state auditors who demanded verification of classified line items were immediately threatened by military counter-intelligence, the system became an unchecked haven for self-enriching defense cartels.",
        "From Soviet Gosplan shadow accounts to FASAB Statement Fifty-Six audit exemptions, the playbook of military-industrial theft never changes: invoke national security, classify the ledger, and dare the public to demand the receipts. Real national defense requires mathematical accountability, not trillion-dollar blank checks hidden behind black-budget waivers. Audit the contractors, strip away Statement Fifty-Six, and open the books. I'm Rex Vance. Keep your filters at absolute zero."
    ]
}

async def main():
    print(f"=== Producing ZeroFilter Episode {EPISODE_DATA['id']} ===")
    total_words = sum(len(p.split()) for p in EPISODE_DATA["paragraphs"])
    print(f"Script word count: {total_words} words (Target: 380-550 words)")
    assert 380 <= total_words <= 550, f"Word count {total_words} out of bounds!"
    
    # 1. Procedural Cover Generation
    print("[1/5] Generating procedural cyber-noir cover...")
    img = generate_cover(theme="sap_carveouts", title=EPISODE_DATA["title"])
    img.save(IMG_EP131, "WEBP", quality=92)
    print(f"Saved: {IMG_EP131}")
    
    # 2. Looping 10s MP4 Cover
    print("[2/5] Generating 10s looping MP4 cover...")
    mp4_path = os.path.join(THUMBS_DIR, f"{EPISODE_DATA['id']}.mp4")
    generate_looping_video(IMG_EP131, mp4_path, duration=10)
    
    # 3. Create Art Frames
    print("[3/5] Synchronizing 6 story art frames...")
    src_frames = [
        IMG_EP131,
        IMG_STUDIO,
        IMG_EP131,
        IMG_REX,
        IMG_EP131,
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
    manifest["updated"] = "2026-10-06T14:50:00Z"
    
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Episode {EPISODE_DATA['id']} registered successfully! Total episodes: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
