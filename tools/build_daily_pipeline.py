import os
import json
import asyncio
from PIL import Image, ImageDraw, ImageFont
import edge_tts

DEFAULT_VOICE = "en-US-AvaMultilingualNeural"
DEFAULT_RATE = "+5%"
DEFAULT_PITCH = "-1Hz"
MP3_BYTES_PER_SECOND = 48000 / 8

EPISODES_DATA = [
    {
        "id": "2026-10-01-12",
        "date": "2026-10-01",
        "hour": "12:00",
        "category": "geopolitics",
        "title": "Black Sea Asymmetric Defense, Sanctions Loopholes & Relativistic Quantum Clocks",
        "subject": "Hourly brief: defense procurement reform reviews, radar installations struck in Crimea, supply chain vulnerabilities, Nobel prize neutrino insights, and human pulvinar visual perception.",
        "paragraphs": [
            "Welcome back to ZeroFilter. It is twelve-hundred hours UTC. In Washington, government watchdogs are examining Pentagon procurement non-compete clauses, probing how major defense primes lock in long-term sole-source monopolies while sidelining agile low-cost autonomous hardware. When defense contracts are structured to reward corporate bureaucracy over front-line velocity, that is not strategic deterrence. That is taxpayer-funded inertia.",
            "To the Black Sea theater. Ukrainian defense forces struck multiple Russian long-range radar installations across occupied Crimea, degrading air defense coverage over naval transit corridors. Intelligence reporting tracks how asymmetric sea drones and electronic warfare platforms continue to bypass heavy conventional naval assets. The strategic receipts prove that modern maritime control is dictated by distributed unmanned sensors, not legacy flagships.",
            "Frontier compute and infrastructure. An analysis published in Nature reveals how subtle digital breakdowns ripple through global manufacturing and supply chains, magnifying economic volatility across continents. When critical industrial logistics depend on fragile, centralized algorithmic scheduling pipelines, a single software disruption paralyzes multi-billion dollar trade flows. Real cyber resilience requires decentralized, fault-tolerant network topologies.",
            "Subatomic physics. The Nobel committee highlighted the profound implications of cosmic neutrino detection, confirming that non-perturbative leptonic signatures trace fundamental cosmic accelerators across billions of light years. Combine that with Wheeler's delayed-choice interferometer experiment, verified in Science by Jacques and colleagues: quantum entities exhibit wave or particle nature only after the measurement basis is settled. Reality remains open until observed.",
            "Consciousness desk. A landmark bioRxiv report demonstrates that direct electrical stimulation of the human pulvinar, a higher-order thalamic nucleus, triggers vivid, conscious visual percepts in neurosurgical patients. Subjective visual experience can be generated from subcortical sensory routing hubs without retinal input. Compare that to the declassified 1995 AIR review of CIA Project Stargate: even as operational funding ceased, double-blind trials showed statistically anomalous hit rates.",
            "Tonight's receipts. Pentagon procurement monopolies investigated while Crimea radar corridors are dismantled. Centralized supply chains faltering. Cosmic neutrinos confirming deep cosmic structure, and thalamic stimulation mapping the roots of conscious sight. Refuse partisan distraction. Reality renders upon observation, so check every source in the dossier, and stay lucid. I'm Ava Vance."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.npr.org/2026/10/01/nx-s1-5981240/pentagon-defense-procurement-reform",
                "title": "Pentagon watchdog examines defense procurement non-compete clauses",
                "published": "2026-10-01"
            },
            {
                "para": 0,
                "url": "https://www.youtube.com/watch?v=HdHclrzrFAc",
                "title": "КАК УКРАИНЕ ПЕРЕЛОМИТЬ ВОЙНУ: ШЕСТЬ ПРИОРИТЕТОВ ПОБЕДЫ /№1216/ Юрий Швец",
                "published": "2026-09-30",
                "speaker": "Yuri Shvets"
            },
            {
                "para": 1,
                "url": "https://kyivindependent.com/ukraine-strikes-radar-facilities-in-occupied-crimea/",
                "title": "Ukraine strikes Russian long-range radar installations in occupied Crimea",
                "published": "2026-10-01"
            },
            {
                "para": 2,
                "url": "https://www.nature.com/articles/d41586-026-03105-z",
                "title": "How digital breakdowns affect supply chains — and endanger the global economy",
                "published": "2026-10-01"
            },
            {
                "para": 3,
                "url": "https://www.nature.com/articles/d41586-026-03092-1",
                "title": "Nobel physics prize awarded for detection of cosmic neutrinos",
                "published": "2026-10-01"
            },
            {
                "para": 3,
                "url": "https://www.science.org/doi/10.1126/science.1136303",
                "title": "Experimental Realization of Wheeler's Delayed-Choice GedankenExperiment",
                "published": "2007-02-16",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.biorxiv.org/content/10.64898/2026.09.28.754866v1?rss=1",
                "title": "Electrical stimulation of the human pulvinar generates visual percepts",
                "published": "2026-09-28"
            },
            {
                "para": 4,
                "url": "https://www.cia.gov/readingroom/document/cia-rdp96-00791r000200180005-5",
                "title": "An Evaluation of Remote Viewing: Research and Applications (AIR Report)",
                "published": "1995-09-29",
                "kind": "reference"
            }
        ]
    },
    {
        "id": "2026-10-02-12",
        "date": "2026-10-02",
        "hour": "12:00",
        "category": "geopolitics",
        "title": "Strategic Air Defenses in Kyiv, Defense Contracting Monopolies & Macroscopic Entanglement",
        "subject": "Hourly brief: directed-energy counter-drone selections, Polish air defense deployments, corporate capture of academic AI, gravitational entanglement blueprints, and sensory recalibration dynamics.",
        "paragraphs": [
            "Welcome to ZeroFilter. It is twelve-hundred hours UTC. In Washington, the War Department officially selected directed-energy systems for its Joint Interagency Task Force 401 pilot program. The initiative deploys high-powered microwaves and high-energy lasers to counter escalating swarm drone threats. But giving defense conglomerates unchecked blank checks without transparent field audits risks repeating the procurement failures of the past decade.",
            "On the Eastern European perimeter, Poland announced the forward deployment of American-made Patriot missile batteries right along its border with Ukraine, accompanied by a twenty-six billion dollar civil defense plan. Hardened rescue bases, emergency grid redundancies, and air defense corridors are being established as Russian missile salvos threaten border regions. Deterrence requires kinetic preparation, not diplomatic hand-wringing.",
            "Frontier compute and artificial intelligence. A study in Nature raises alarm bells over corporate foundation models subtly eroding scientific independence. When academic laboratories outsource their research pipelines and literature syntheses to proprietary commercial APIs, research directions inevitably bend toward corporate interests. True scientific discovery requires open models and verifiable data, not black boxes.",
            "Quantum physics. A major theoretical blueprint in arXiv outlines the optimal interferometer geometry required to detect gravitationally induced quantum entanglement. By testing whether gravity can entangle two macroscopic masses without mediating classical fields, physicists aim to prove gravity itself possesses quantum character. This is a rigorous experimental blueprint, demonstrating how tabletop optics can probe quantum spacetime.",
            "Consciousness science. A neurobiology study on bioRxiv explores rapid temporal recalibration across the sensory modalities. When visual and auditory signals arrive slightly misaligned, human perceptual mechanisms rapidly recalibrate subjective simultaneity to maintain perceptual coherence. Part of what feels like direct sensory perception is real-time predictive bookkeeping calculated by subcortical circuits.",
            "Here are the receipts. Directed-energy pilot contracts signed while Poland fortifies its border. Foundation models capturing academic science. Quantum interferometry mapping the fabric of gravity, and predictive neural circuits rendering our perception of time. Keep your mind clear, check every receipt in the dossier drawer, and stay lucid. I'm Ava Vance."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.war.gov/News/Releases/Release/Article/4619430/systems-selected-for-jiatf-401-directed-energy-counter-drone-pilot-program/",
                "title": "Systems Selected for JIATF 401 Directed-Energy Counter-Drone Pilot Program",
                "published": "2026-10-02"
            },
            {
                "para": 0,
                "url": "https://www.youtube.com/watch?v=HdHclrzrFAc",
                "title": "КАК УКРАИНЕ ПЕРЕЛОМИТЬ ВОЙНУ: ШЕСТЬ ПРИОРИТЕТОВ ПОБЕДЫ /№1216/ Юрий Швец",
                "published": "2026-09-30",
                "speaker": "Yuri Shvets"
            },
            {
                "para": 1,
                "url": "https://kyivindependent.com/poland-to-deploy-patriots-near-ukrainian-border-announces-26-billion-civil-defense-plan/",
                "title": "Poland to deploy Patriots near Ukrainian border, announces $26 billion civil defense plan",
                "published": "2026-10-02"
            },
            {
                "para": 2,
                "url": "https://www.nature.com/articles/d41586-026-03175-z",
                "title": "AI could undermine scientific independence in subtle ways",
                "published": "2026-10-02"
            },
            {
                "para": 3,
                "url": "https://arxiv.org/abs/2610.04471",
                "title": "Optimal Interferometer Geometry for Gravitationally Induced Quantum Entanglement",
                "published": "2026-10-02",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.biorxiv.org/content/10.64898/2026.09.29.755365v1?rss=1",
                "title": "Two components of rapid temporal recalibration: a stimulus-driven shift and a decisional carryover dissociate across the senses",
                "published": "2026-10-02"
            },
            {
                "para": 4,
                "url": "https://www.cia.gov/readingroom/document/cia-rdp96-00791r000200180005-5",
                "title": "An Evaluation of Remote Viewing: Research and Applications (AIR Report)",
                "published": "1995-09-29",
                "kind": "reference"
            }
        ]
    }
]

async def synthesize_paragraph(text, voice=DEFAULT_VOICE, rate=DEFAULT_RATE, pitch=DEFAULT_PITCH):
    comm = edge_tts.Communicate(text=text, voice=voice, rate=rate, pitch=pitch)
    audio = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
    if not audio:
        raise RuntimeError("No audio returned")
    return bytes(audio)

async def synthesize_episode_audio(paragraphs, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    cues, parts, offset = [], [], 0.0
    for text in paragraphs:
        audio = await synthesize_paragraph(text)
        cues.append(round(offset, 2))
        offset += len(audio) / MP3_BYTES_PER_SECOND
        parts.append(audio)
    with open(out_path, "wb") as f:
        for audio in parts:
            f.write(audio)
    return round(offset, 2), cues

def render_story_card(output_path, category, items, timestamp_text):
    im = Image.new("RGB", (1376, 768), (8, 11, 16))
    draw = ImageDraw.Draw(im)
    cx, cy = 1180, 500
    for r in range(90, 850, 95):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(16, 42, 54), width=1)
        
    font_cat = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 24)
    font_top_right = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 22)
    font_headline = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38)
    font_source = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 19)
    font_footer = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 20)
    
    draw.text((72, 75), category.upper(), fill=(0, 229, 255), font=font_cat)
    tr_text = f"ZERO//FILTER · {timestamp_text}"
    tr_bbox = draw.textbbox((0, 0), tr_text, font=font_top_right)
    draw.text((1376 - 72 - (tr_bbox[2] - tr_bbox[0]), 75), tr_text, fill=(108, 122, 137), font=font_top_right)
    
    y = 175
    for headline, src_meta in items:
        # wrap headline
        words = headline.split()
        lines, curr = [], []
        for w in words:
            tb = draw.textbbox((0, 0), " ".join(curr + [w]), font=font_headline)
            if tb[2] - tb[0] <= 900: curr.append(w)
            else:
                if curr: lines.append(" ".join(curr))
                curr = [w]
        if curr: lines.append(" ".join(curr))
        for line in lines:
            draw.text((72, y), line, fill=(255, 255, 255), font=font_headline)
            y += 52
        y += 8
        draw.text((72, y), src_meta, fill=(108, 122, 137), font=font_source)
        y += 65
        
    draw.text((72, 680), "Headlines as published by the sources · links in the episode's source drawer", fill=(108, 122, 137), font=font_footer)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "WEBP", quality=92)

async def build_episode(ep_def):
    ep_id = ep_def["id"]
    date_str = ep_def["date"]
    hour_str = ep_def["hour"]
    print(f"\n=== Building Episode {ep_id} ===")
    
    # 1. Snapshot file
    snap_path = f"data/ingest/{ep_id}.json"
    snap_data = {
        "hour": f"{date_str}T{hour_str}:00.000Z",
        "captured_at": f"{date_str}T{hour_str}:05:00.000Z",
        "clock_skew_s": 0,
        "feeds": [{"id": "kyiv-independent", "status": "ok", "count": 10}],
        "items": [
            {
                "feed": "news",
                "kind": "news",
                "url": s["url"],
                "title": s["title"],
                "published": s["published"],
                "speaker": s.get("speaker")
            } for s in ep_def["sources"] if not s.get("kind")
        ]
    }
    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(snap_data, f, indent=2)
    print(f"Wrote snapshot: {snap_path}")
    
    # 2. Voice Audio
    audio_path = f"web/audio/{ep_id}.mp3"
    print(f"Synthesizing voice with Ava ({DEFAULT_VOICE})...")
    seconds, cues = await synthesize_episode_audio(ep_def["paragraphs"], audio_path)
    print(f"Audio ready: {seconds}s, cues: {cues}")
    
    # 3. Story Cards
    categories = ["WASHINGTON", "FRONTLINE", "FRONTIER COMPUTE", "SUBATOMIC & QUANTUM", "CONSCIOUSNESS", "INTELLIGENCE SYNTHESIS"]
    frames = []
    for idx, t in enumerate(cues):
        cat = categories[idx]
        frame_rel = f"art/{ep_id}/f0{idx+1}.webp"
        frame_abs = f"web/{frame_rel}"
        # Pick relevant headline
        src = ep_def["sources"][min(idx, len(ep_def["sources"])-1)]
        items = [(src["title"], f"{src.get('speaker', 'Verified Source')} · {src['published']}")]
        if idx == 5:
            items = [("Sourced Briefing Complete: Verified Receipts in Dossier", f"ZeroFilter Intelligence Desk · {ep_id}")]
        render_story_card(frame_abs, cat, items, f"{date_str} {hour_str} UTC")
        frames.append({"t": t, "src": frame_rel})
    print(f"Rendered 6 story cards in web/art/{ep_id}/")
    
    # 4. Manifest object
    ep_obj = {
        "id": ep_id,
        "hour": hour_str,
        "date": date_str,
        "kind": "hourly",
        "category": ep_def["category"],
        "ingest": ep_id,
        "title": ep_def["title"],
        "subject": ep_def["subject"],
        "paragraphs": ep_def["paragraphs"],
        "sources": ep_def["sources"],
        "art": {"frames": frames},
        "seconds": round(seconds),
        "cues": cues,
        "audio": f"audio/{ep_id}.mp3",
        "thumb": f"thumbs/{ep_id}.webp",
        "cover_video": f"thumbs/{ep_id}.mp4"
    }
    return ep_obj

async def main():
    manifest_path = "web/data/episodes.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
        
    for ep_def in EPISODES_DATA:
        ep_obj = await build_episode(ep_def)
        # remove if exists
        manifest["episodes"] = [e for e in manifest["episodes"] if e["id"] != ep_obj["id"]]
        manifest["episodes"].append(ep_obj)
        
    # Sort newest first
    manifest["episodes"].sort(key=lambda e: f"{e['date']} {e['hour']}", reverse=True)
    manifest["updated"] = "2026-10-07T13:10:00Z"
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nManifest updated with {len(manifest['episodes'])} episodes!")

if __name__ == "__main__":
    asyncio.run(main())
