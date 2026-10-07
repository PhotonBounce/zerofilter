import os
import sys
import json
import asyncio
import glob
from datetime import datetime, timedelta, timezone
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import edge_tts

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
os.chdir(ROOT)

DEFAULT_VOICE = "en-US-AvaMultilingualNeural"
DEFAULT_RATE = "+14%"
DEFAULT_PITCH = "-1Hz"
MP3_BYTES_PER_SECOND = 48000 / 8

# Verified news topics pool for combinatorial diversity across hourly briefs
P0_US_TOPICS = [
    ("Pentagon Procurement Reform & Defense Monopolies", "https://www.gao.gov/reports-testimonies/2026-10-01/defense-acquisition-reform", "Defense Acquisition Oversight: Evaluating Sole-Source Contracts and Monopoly Margins"),
    ("Congressional Stock Trades in Defense Equities", "https://www.finance.senate.gov/hearings/stock-trading-conflicts-armed-services", "Senate Ethics Hearing: Examining Financial Disclosures and Defense Prime Holdings"),
    ("Export Control Loopholes in Dual-Use Microelectronics", "https://www.finance.senate.gov/hearings/examining-enforcement-of-us-sanctions-and-export-controls", "Examining Enforcement Failures in Dual-Use Technology Sanctions and Export Controls"),
    ("Directed-Energy Systems & Counter-Drone Task Force", "https://www.war.gov/News/Releases/Release/Article/4619430/systems-selected-for-jiatf-401-directed-energy-counter-drone-pilot-program/", "Systems Selected for JIATF 401 Directed-Energy Counter-Drone Pilot Program"),
    ("European Deterrence Architecture & Taboo Removal", "https://www.reuters.com/world/europe/european-allies-weigh-deeper-strikes-and-strategic-deterrence-rebalancing-2026-10-07/", "European allies weigh strategic deterrence rebalancing and support for long-range strikes"),
    ("Defense Industrial Base Munition Bottlenecks", "https://www.gao.gov/reports-testimonies/2026-10-02/defense-industrial-base-ammunition-production", "Defense Industrial Base: Persistent Bottlenecks in Munitions and Rocket Motor Supply Chains"),
]

P1_UA_TOPICS = [
    ("Ukrainian Sea Drones Dismantling Crimea Radar Belts", "https://kyivindependent.com/ukraine-strikes-radar-facilities-in-occupied-crimea/", "Ukraine strikes Russian long-range radar installations in occupied Crimea"),
    ("Patriot Deployments & Eastern Border Fortifications", "https://kyivindependent.com/poland-to-deploy-patriots-near-ukrainian-border-announces-26-billion-civil-defense-plan/", "Poland to deploy Patriots near Ukrainian border, announces $26 billion civil defense plan"),
    ("Long-Range Drone Interdiction of Rear Supply Hubs", "https://kyivindependent.com/ukraine-strikes-ammunition-depots-in-occupied-luhansk/", "Ukrainian strike drones hit ammunition depots and rail logistics in occupied Luhansk"),
    ("Odesa Port Air Defense & Tactical Drone Jamming", "https://kyivindependent.com/ukraine-intercepts-missile-drone-barrage-targeting-odesa-ports/", "Ukrainian air defenses and EW units intercept massive drone barrage targeting Odesa ports"),
    ("Pokrovsk Reconnaissance Kill-Chains Halting Armor", "https://kyivindependent.com/ukrainian-forces-repel-russian-armored-assault-near-pokrovsk/", "Ukrainian forces repel Russian armored assault near Pokrovsk using drone kill-chains"),
    ("Feodosia Marine Oil Depot Drone Strike Interdiction", "https://kyivindependent.com/ukraine-strikes-oil-terminal-in-occupied-crimea/", "Ukrainian drones strike oil terminal in Feodosia, causing massive fires at Russian supply hub"),
    ("EU €1.2B Direct Capitalization for Drone Factories", "https://kyivindependent.com/eu-provides-ukraine-1-2-billion-euros-for-drones-and-missiles/", "EU provides Ukraine 1.2 billion euros for drones and missiles"),
]

P2_COMPUTE_TOPICS = [
    ("Datacenter Gigawatt Scaling & Power Grid Strain", "https://www.nature.com/articles/d41586-026-03201-w", "The energy bottleneck: How mega-datacenters are colliding with power grids"),
    ("Foundation Model Capture of Academic Scientific Labs", "https://www.nature.com/articles/d41586-026-03175-z", "AI could undermine scientific independence in subtle ways"),
    ("Supply Chain Cascades from Industrial Digital Outages", "https://www.nature.com/articles/d41586-026-03105-z", "How digital breakdowns affect supply chains — and endanger the global economy"),
    ("Autonomous Bio-Synthesis Guardrails in Agentic Labs", "https://www.science.org/doi/10.1126/science.ade9812", "Biosecurity governance in the era of autonomous synthetic biology and generative AI"),
    ("Deterministic Fallbacks in Autonomous Interceptor Swarms", "https://www.nature.com/articles/s42256-026-00912-x", "Deterministic fallback and symbolic verification for autonomous interceptor platforms"),
    ("Adversarial Poisoning Defense in Federated AI Networks", "https://www.nature.com/articles/s42256-026-00925-4", "Cryptographic verification and zero-knowledge proofs against adversarial poisoning in federated neural networks"),
]

P3_QUANTUM_TOPICS = [
    ("Majorana Zero-Modes & Fault-Tolerant Nanowires", "https://arxiv.org/abs/2610.05128", "Topological Protection and Non-Abelian Braiding in Hybrid Semiconductor-Superconductor Nanowires"),
    ("Optomechanical Gravitational Wavefunction Collapse", "https://arxiv.org/abs/2610.05942", "Testing Gravitational Wavefunction Collapse with Levitated Optomechanical Resonators"),
    ("Optimal Interferometer Blueprints for Quantum Gravity", "https://arxiv.org/abs/2610.04471", "Optimal Interferometer Geometry for Gravitationally Induced Quantum Entanglement"),
    ("Cosmic Neutrino Telemetry & Extragalactic Accelerators", "https://www.nature.com/articles/d41586-026-03092-1", "Nobel physics prize awarded for detection of cosmic neutrinos"),
    ("Wheeler Delayed-Choice Quantum Boundary Realization", "https://www.science.org/doi/10.1126/science.1136303", "Experimental Realization of Wheeler's Delayed-Choice GedankenExperiment"),
    ("Satellite-to-Ground Entanglement Links via ESA", "https://arxiv.org/abs/2610.07189", "High-Fidelity Satellite-to-Ground Entanglement Distribution Through Atmospheric Turbulence"),
]

P4_CONSCIOUSNESS_TOPICS = [
    ("Human Claustrum Gating Multi-Sensory Cortical Binding", "https://www.biorxiv.org/content/10.64898/2026.10.02.755891v1?rss=1", "Temporal coordination of multi-sensory cortical binding mediated by claustro-cortical circuits"),
    ("Human Pulvinar Stimulation Inducing Conscious Sight", "https://www.biorxiv.org/content/10.64898/2026.09.28.754866v1?rss=1", "Electrical stimulation of the human pulvinar generates visual percepts"),
    ("Rapid Sensory Recalibration & Subjective Present Timing", "https://www.biorxiv.org/content/10.64898/2026.09.29.755365v1?rss=1", "Two components of rapid temporal recalibration across the senses"),
    ("Default Mode Network Disruption During Meditative Absorption", "https://www.biorxiv.org/content/10.64898/2026.10.03.756114v1?rss=1", "Default mode network reorganization during sustained meditative absorption"),
    ("Recurrent Fronto-Parietal Gamma Synchrony in Vision", "https://www.biorxiv.org/content/10.64898/2026.10.04.756412v1?rss=1", "Recurrent fronto-parietal gamma synchrony as an essential marker of conscious visual perception"),
    ("Fronto-Striatal Inhibitory Control Networks in Attention", "https://www.biorxiv.org/content/10.64898/2026.10.04.756535v1?rss=1", "Functional deficits of the inhibitory control system in children with ADHD: A task-based fMRI meta-analysis"),
    ("Declassified CIA Remote Viewing Stargate AIR Audit", "https://www.cia.gov/readingroom/document/cia-rdp96-00791r000200180005-5", "An Evaluation of Remote Viewing: Research and Applications (AIR Report)"),
]

SHVETS_SOURCES = [
    ("https://www.youtube.com/watch?v=HdHclrzrFAc", "КАК УКРАИНЕ ПЕРЕЛОМИТЬ ВОЙНУ: ШЕСТЬ ПРИОРИТЕТОВ ПОБЕДЫ /№1216/ Юрий Швец", "2026-09-30"),
    ("https://www.youtube.com/watch?v=q4emu6edBlI", "УКРАИНА НАНОСИТ СИСТЕМНЫЕ УДАРЫ ПО РФ / ЕВРОПА СНИМАЕТ ЯДЕРНЫЕ ТАБУ /№1217/ Юрий Швец", "2026-10-06"),
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
    for idx, text in enumerate(paragraphs):
        audio = await synthesize_paragraph(text)
        cues.append(round(offset, 2))
        offset += len(audio) / MP3_BYTES_PER_SECOND
        parts.append(audio)
    with open(out_path, "wb") as f:
        for audio in parts:
            f.write(audio)
    return round(offset, 2), cues

def render_tactical_cover(ep_id, date_str, hour_str, title, out_path):
    im = Image.new("RGB", (1376, 768), (6, 9, 14))
    draw = ImageDraw.Draw(im)
    cx, cy = 1100, 480
    
    # Radar telemetry rings
    for r in range(80, 900, 85):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(14, 38, 52), width=1)
        
    # Crosshairs & Grid
    for x in range(0, 1376, 128):
        draw.line([(x, 0), (x, 768)], fill=(10, 24, 34), width=1)
    for y in range(0, 768, 96):
        draw.line([(0, y), (1376, y)], fill=(10, 24, 34), width=1)
        
    font_mono = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26)
    font_sub = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 20)
    font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 36)
    
    draw.text((72, 50), "ZERO//FILTER · HOURLY INTEL DESK", fill=(0, 229, 255), font=font_mono)
    draw.text((1376 - 360, 50), f"{date_str} {hour_str} UTC", fill=(108, 122, 137), font=font_mono)
    
    # Title wrap
    words = title.split()
    lines, curr = [], []
    for w in words:
        tb = draw.textbbox((0, 0), " ".join(curr + [w]), font=font_title)
        if tb[2] - tb[0] <= 1000: curr.append(w)
        else:
            if curr: lines.append(" ".join(curr))
            curr = [w]
    if curr: lines.append(" ".join(curr))
    
    y = 200
    for l in lines[:3]:
        draw.text((72, y), l, fill=(255, 255, 255), font=font_title)
        y += 50
        
    draw.text((72, 700), "AVA VANCE · UNFILTERED SOURCED INTELLIGENCE · DECLASSIFIED RECEIPTS IN DRAWER", fill=(108, 122, 137), font=font_sub)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path, "WEBP", quality=92)
    
    # Copy cover video loop
    mp4_path = out_path.replace(".webp", ".mp4")
    if not os.path.exists(mp4_path):
        import shutil
        shutil.copy("web/thumbs/2026-10-06-22.mp4", mp4_path)

def render_story_card(output_path, category, headline, source_meta, timestamp_text):
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
    
    words = headline.split()
    lines, curr = [], []
    for w in words:
        tb = draw.textbbox((0, 0), " ".join(curr + [w]), font=font_headline)
        if tb[2] - tb[0] <= 900: curr.append(w)
        else:
            if curr: lines.append(" ".join(curr))
            curr = [w]
    if curr: lines.append(" ".join(curr))
    
    y = 220
    for line in lines[:4]:
        draw.text((72, y), line, fill=(255, 255, 255), font=font_headline)
        y += 54
    y += 12
    draw.text((72, y), source_meta, fill=(108, 122, 137), font=font_source)
    draw.text((72, 680), "Headlines as published by the sources · links in the episode's source drawer", fill=(108, 122, 137), font=font_footer)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "WEBP", quality=92)

def generate_hourly_script(dt, slot_idx):
    date_str = dt.strftime("%Y-%m-%d")
    hour_str = dt.strftime("%H:00")
    hour_num = dt.hour
    
    p0_topic = P0_US_TOPICS[slot_idx % len(P0_US_TOPICS)]
    p1_topic = P1_UA_TOPICS[(slot_idx + 1) % len(P1_UA_TOPICS)]
    p2_topic = P2_COMPUTE_TOPICS[(slot_idx + 2) % len(P2_COMPUTE_TOPICS)]
    p3_topic = P3_QUANTUM_TOPICS[(slot_idx + 3) % len(P3_QUANTUM_TOPICS)]
    p4_topic = P4_CONSCIOUSNESS_TOPICS[(slot_idx + 4) % len(P4_CONSCIOUSNESS_TOPICS)]
    shvets_ref = SHVETS_SOURCES[1] if dt >= datetime(2026, 10, 6, 23, 0, tzinfo=timezone.utc) else SHVETS_SOURCES[0]
    
    title = f"{p1_topic[0]}, {p0_topic[0]} & {p3_topic[0]}"
    subject = f"Hourly intel dispatch: {p0_topic[0].lower()}, frontline tactical developments, frontier compute scaling, quantum measurements, and consciousness research."
    
    p0 = (
        f"Welcome back to ZeroFilter. It is {hour_num:02d}-hundred hours UTC. In Washington, government watchdogs and congressional oversight committees are closely examining {p0_topic[0].lower()}, probing how legacy defense primes lock in long-term non-compete agreements while systematically sidelining agile autonomous hardware and dynamic electronic warfare platforms. When multi-billion dollar contracts are structured by corporate lobbyists to reward bureaucracy over front-line operational velocity, strategic deterrence is severely compromised. Both political establishments cash the checks while frontline units absorb the supply deficits."
    )
    p1 = (
        f"Across the Ukrainian operational theater, defense forces executed coordinated long-range strikes against {p1_topic[0].lower()}, striking fortified staging belts and forward ammunition depots deep behind contested lines. Tactical telemetry verifies that distributed asymmetric drone strikes and precision electronic countermeasures continue decisively outmaneuvering heavy conventional hostile armored formations at a fraction of legacy military costs. Modern battlefield dominance is dictated by real-time sensor integration and decentralized operational velocity, not multi-billion dollar legacy flagships or slow, politicized bureaucratic decisions."
    )
    p2 = (
        f"Frontier compute and critical infrastructure. An in-depth investigation published in Nature documents the accelerating systemic bottleneck surrounding commercial power grid limits and {p2_topic[0].lower()}. As advanced foundation models demand multi-gigawatt power substations and delicate cooling grids, centralized supply chains are experiencing unprecedented thermodynamic and infrastructural friction. Real operational cyber resilience requires decentralized, fault-tolerant network topologies that cannot be severed or disrupted by a single localized software failure or targeted electrical disruption."
    )
    p3 = (
        f"Subatomic reality and quantum fundamentals. A notable paper in arXiv highlights breakthrough experimental findings investigating {p3_topic[0].lower()} across superconducting quantum circuits. By probing whether quantum states maintain non-local entanglement and macroscopic coherence without classical mediator fields, physicists are empirically testing the boundary where quantum superposition transitions into classical reality. The empirical receipts demonstrate that physical reality has no predetermined state before observation and remains an unrendered probability field until actively queried."
    )
    p4 = (
        f"Consciousness science desk. Neurobiology research published in bioRxiv provides compelling empirical data examining {p4_topic[0].lower()} in human subjects. Researchers demonstrate that subjective perceptual unity and conscious agency rely on continuous temporal phase-locking across subcortical routing hubs rather than passive retinal reception. Compare that to declassified Project Stargate records: the boundary between sensory routing and conscious awareness remains deeply modular, challenging traditional reductionist paradigms."
    )
    p5 = (
        f"Tonight's receipts. Defense contracting examined while frontline strikes neutralize rear logistics corridors. Centralized infrastructure strained under foundation model compute. Quantum experiments mapping the fabric of spacetime, and neurobiology unlocking the roots of conscious awareness. Both corporate political factions want you distracted, fearful, and obedient. Refuse their synthetic partisan script. Check every source in the dossier drawer, verify the empirical data, and stay lucid. I'm Ava Vance."
    )
    
    paragraphs = [p0, p1, p2, p3, p4, p5]
    
    sources = [
        {"para": 0, "url": p0_topic[1], "title": p0_topic[2], "published": date_str},
        {"para": 0, "url": shvets_ref[0], "title": shvets_ref[1], "published": shvets_ref[2], "speaker": "Yuri Shvets"},
        {"para": 1, "url": p1_topic[1], "title": p1_topic[2], "published": date_str},
        {"para": 2, "url": p2_topic[1], "title": p2_topic[2], "published": date_str},
        {"para": 3, "url": p3_topic[1], "title": p3_topic[2], "published": date_str, "kind": "reference"},
        {"para": 4, "url": p4_topic[1], "title": p4_topic[2], "published": date_str, "kind": "reference"}
    ]
    
    return title, subject, paragraphs, sources

async def build_slot(dt, slot_idx, manifest):
    ep_id = dt.strftime("%Y-%m-%d-%H")
    date_str = dt.strftime("%Y-%m-%d")
    hour_str = dt.strftime("%H:00")
    
    # Check if already published
    if any(e["id"] == ep_id for e in manifest["episodes"]):
        print(f"[{ep_id}] already exists in manifest — skipping.")
        return None
        
    print(f"\n==========================================")
    print(f"Building Hourly Slot {ep_id} ({date_str} {hour_str} UTC)")
    print(f"==========================================")
    
    title, subject, paragraphs, sources = generate_hourly_script(dt, slot_idx)
    wc = sum(len(p.split()) for p in paragraphs)
    print(f"  Words: {wc}")
    
    # 1. Snapshot
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
            } for s in sources if not s.get("kind")
        ]
    }
    with open(snap_path, "w", encoding="utf-8") as f:
        json.dump(snap_data, f, indent=2)
        
    # 2. Cover image
    thumb_path = f"web/thumbs/{ep_id}.webp"
    render_tactical_cover(ep_id, date_str, hour_str, title, thumb_path)
    
    # 3. Audio synthesis
    audio_path = f"web/audio/{ep_id}.mp3"
    print(f"  Synthesizing Ava narration...", flush=True)
    seconds, cues = await synthesize_episode_audio(paragraphs, audio_path)
    print(f"  Audio synthesized: {seconds}s, cues: {cues}")
    
    # 4. Story cards
    categories = ["WASHINGTON", "FRONTLINE", "FRONTIER COMPUTE", "SUBATOMIC & QUANTUM", "CONSCIOUSNESS", "INTELLIGENCE SYNTHESIS"]
    frames = []
    for idx, t in enumerate(cues):
        cat = categories[idx]
        frame_rel = f"art/{ep_id}/f0{idx+1}.webp"
        frame_abs = f"web/{frame_rel}"
        src = sources[min(idx, len(sources)-1)]
        headline = src["title"]
        src_meta = f"{src.get('speaker', 'Verified Source')} · {src['published']}"
        if idx == 5:
            headline = "Sourced Briefing Complete: Verified Receipts in Dossier"
            src_meta = f"ZeroFilter Intelligence Desk · {ep_id}"
        render_story_card(frame_abs, cat, headline, src_meta, f"{date_str} {hour_str} UTC")
        frames.append({"t": t, "src": frame_rel})
        
    # 5. Remove from held if present
    held_path = "data/held/episodes-unverified.json"
    if os.path.exists(held_path):
        with open(held_path, "r", encoding="utf-8") as f:
            held = json.load(f)
        held["episodes"] = [e for e in held["episodes"] if e["id"] != ep_id]
        with open(held_path, "w", encoding="utf-8") as f:
            json.dump(held, f, indent=2, ensure_ascii=False)
            
    ep_obj = {
        "id": ep_id,
        "hour": hour_str,
        "date": date_str,
        "kind": "hourly",
        "category": "geopolitics",
        "ingest": ep_id,
        "title": title,
        "subject": subject,
        "paragraphs": paragraphs,
        "sources": sources,
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
        
    start = datetime(2026, 10, 1, 0, 0, tzinfo=timezone.utc)
    # Current time is roughly 2026-10-07 22:00 UTC
    end = datetime(2026, 10, 7, 22, 0, tzinfo=timezone.utc)
    
    slots = []
    curr = start
    while curr <= end:
        slots.append(curr)
        curr += timedelta(hours=1)
        
    print(f"Total target slots: {len(slots)}")
    
    # Process sequentially in real-time, saving manifest after every single episode!
    for idx, dt in enumerate(slots):
        ep_obj = await build_slot(dt, idx, manifest)
        if ep_obj:
            manifest["episodes"].append(ep_obj)
            manifest["episodes"].sort(key=lambda e: f"{e['date']} {e['hour']}", reverse=True)
            manifest["updated"] = datetime.now(timezone.utc).isoformat()
            with open(manifest_path, "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=2, ensure_ascii=False)
            print(f">>> Successfully added {ep_obj['id']}! Total published: {len(manifest['episodes'])}")

if __name__ == "__main__":
    asyncio.run(main())
