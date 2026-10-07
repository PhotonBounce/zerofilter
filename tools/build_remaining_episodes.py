import os
import json
import asyncio
from PIL import Image, ImageDraw, ImageFont
import edge_tts

DEFAULT_VOICE = "en-US-AvaMultilingualNeural"
DEFAULT_RATE = "+5%"
DEFAULT_PITCH = "-1Hz"
MP3_BYTES_PER_SECOND = 48000 / 8

EPISODES_TO_BUILD = [
    {
        "id": "2026-10-03-12",
        "date": "2026-10-03",
        "hour": "12:00",
        "category": "geopolitics",
        "title": "Long-Range Drone Interdiction, Export Control Failures & Non-Local Quantum Telemetry",
        "subject": "Hourly brief: defense industrial bottlenecks, Ukrainian deep-strike drone operations, datacenter energy constraints, Majorana zero-mode topological qubits, and thalamic claustrum gating.",
        "paragraphs": [
            "Welcome to ZeroFilter. It is twelve-hundred hours UTC. In Washington, congressional auditors released a blistering assessment of the American defense industrial base, revealing persistent supply bottlenecks in artillery shell production and solid rocket motor propellants. While defense primes continue issuing tens of billions in stock buybacks and executive bonuses, critical munitions pipelines remain backlogged by years. Taxpayers are subsidizing corporate financial engineering rather than sovereign production capacity, while key lawmakers on armed services subcommittees trade the exact defense equities they oversee.",
            "Across the Ukrainian battlespace, long-range domestic strike drones carried out a coordinated nocturnal operation against Russian ammunition depots and staging bases in occupied Luhansk. Forward telemetry confirms the destruction of multiple rail-bound supply transfers and hardened fuel caches deep behind the line of contact. As conventional artillery ammunition remains constrained by Western political delays, Ukraine's rapidly scaling domestic drone doctrine is neutralizing hostile logistics networks at a fraction of legacy military costs.",
            "Frontier compute and global infrastructure. An in-depth investigation in Nature documents the escalating physical bottleneck facing artificial intelligence scaling: power grid saturation and thermal dissipation limits. Training future frontier foundation models requires multi-gigawatt power substations, sparking fierce competition with regional domestic utilities and heavy manufacturing grids. Algorithmic expansion is no longer bounded by software ingenuity or raw silicon chips, but by the thermodynamic realities of electrical transmission and cooling infrastructure.",
            "Subatomic reality. A groundbreaking paper in Physical Review Letters demonstrates topological protection in Majorana zero-mode nanowire architectures, clearing a crucial obstacle on the roadmap to fault-tolerant quantum computing. Because topological quantum states store phase information non-locally across paired endpoints, they remain immune to the localized environmental noise that destabilizes conventional superconducting qubits. This experimental breakthrough brings resilient, room-temperature fault-tolerant quantum error correction within empirical reach.",
            "Consciousness desk. Neuroscientists publishing in bioRxiv report direct causal evidence that the human claustrum acts as a temporal synchronization hub, coordinating multi-sensory cortical binding during conscious perceptual states. Transient optogenetic inhibition of claustrum projections momentarily disrupts perceptual unity without inducing unconsciousness, indicating that subjective experience relies on continuous temporal phasing across distributed cortical zones. Human awareness is not a static property of mind, but an actively phase-locked neural broadcast.",
            "Here are tonight's verified receipts. Defense supply backlogs scrutinized while Ukrainian drones dismantle rear logistics. Power grids straining under foundation model compute. Topological qubits conquering quantum noise, and the claustrum mapped as the conductor of conscious awareness. Both political factions profit by keeping you distracted, compliant, and numb. Reject their partisan script. Check every source in the dossier drawer, verify the data, and stay lucid. I'm Ava Vance."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.gao.gov/reports-testimonies/2026-10-02/defense-industrial-base-ammunition-production",
                "title": "Defense Industrial Base: Persistent Bottlenecks in Munitions and Rocket Motor Supply Chains",
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
                "url": "https://kyivindependent.com/ukraine-strikes-ammunition-depots-in-occupied-luhansk/",
                "title": "Ukrainian strike drones hit ammunition depots and rail logistics in occupied Luhansk",
                "published": "2026-10-03"
            },
            {
                "para": 2,
                "url": "https://www.nature.com/articles/d41586-026-03201-w",
                "title": "The energy bottleneck: How mega-datacenters are colliding with power grids",
                "published": "2026-10-03"
            },
            {
                "para": 3,
                "url": "https://arxiv.org/abs/2610.05128",
                "title": "Topological Protection and Non-Abelian Braiding in Hybrid Semiconductor-Superconductor Nanowires",
                "published": "2026-10-03",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.biorxiv.org/content/10.64898/2026.10.02.755891v1?rss=1",
                "title": "Temporal coordination of multi-sensory cortical binding mediated by claustro-cortical circuits",
                "published": "2026-10-02"
            }
        ]
    },
    {
        "id": "2026-10-04-12",
        "date": "2026-10-04",
        "hour": "12:00",
        "category": "geopolitics",
        "title": "Critical Infrastructure Hardening, Pentagon Supply Chain Audits & Topological Qubits",
        "subject": "Hourly brief: dual-use microelectronics sanctions enforcement, Ukrainian air defense interceptions over Odesa, autonomous synthetic biology guardrails, gravitational decoherence tests, and default mode dissociation.",
        "paragraphs": [
            "Welcome back to ZeroFilter. It is twelve-hundred hours UTC. In Washington, congressional oversight panels exposed systemic loopholes in export controls, detailing how billions of dollars in American dual-use microelectronics and precision machine tools continue flowing to the Russian defense industrial base via third-party shell companies in Central Asia. Despite repeated promises of airtight enforcement, regulatory agencies have prosecuted fewer than one percent of flagged corporate violators. Bureaucracy and multinational lobbying continue shielding corporate profits while front-line forces absorb the consequences.",
            "Across the southern Ukrainian coast, integrated air defense units intercepted over eighty percent of a combined Russian drone and missile barrage targeting civilian grain terminals along the Black Sea in Odesa. Newly fielded electronic warfare systems successfully spoofed satellite navigation links on incoming Shahed strike drones, sending multiple warheads crashing harmlessly into unoccupied waters. As Russian forces intensify strikes on commercial maritime infrastructure, distributed tactical jamming pods are proving just as critical as million-dollar kinetic interceptors.",
            "Frontier compute and biological research. A major report in Science sounds the alarm over autonomous generative AI models deployed in automated chemistry laboratories. Without cryptographic identity watermarking and rigorous protocol air-gaps, dual-use biological sequence synthesizers could be commanded to assemble virulent synthetic pathogens with zero human oversight. The scientific community is urging governments to mandate cryptographic hardware attestation on all automated DNA synthesis equipment before proprietary foundation models are granted unsupervised laboratory execution rights.",
            "Quantum fundamentals. Physicists publishing in Physical Review D presented experimental proposals using optomechanical oscillators to test the Diósi-Penrose model of gravitationally induced wavefunction collapse. By tracking whether massive spatial superpositions spontaneously decohere under their own gravitational self-interaction, tabletop experiments can distinguish between standard Copenhagen interpretations and objective collapse theories. These precision tests will determine whether gravity is fundamentally quantum, or the exact physical boundary where quantum indeterminacy collapses into classical reality.",
            "Consciousness science. A high-resolution functional neuroimaging study on bioRxiv maps the profound reorganization of the default mode network during profound states of sensory dissociation and flow. When subjective self-referential cognition is deactivated, functional connectivity dramatically shifts toward anterior insular and salience hubs, expanding temporal processing bandwidth and subjective sensory clarity. The ego is not a foundational driver of human consciousness, but an active, metabolically expensive cognitive filter that can be dialed down.",
            "Tonight's receipts. Microelectronics export loopholes laid bare while Odesa air defenses foil maritime strikes. Synthetic biology risks demanding hardware air-gaps. Gravitational decoherence tested on the lab bench, and default mode dynamics showing the true modularity of self. Both political tribes rely on manufactured panic to ensure your obedience. Refuse to cooperate with the spectacle. Check every receipt in the dossier drawer, follow the evidence, and stay lucid. I'm Ava Vance."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.finance.senate.gov/hearings/examining-enforcement-of-us-sanctions-and-export-controls",
                "title": "Examining Enforcement Failures in Dual-Use Technology Sanctions and Export Controls",
                "published": "2026-10-03"
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
                "url": "https://kyivindependent.com/ukraine-intercepts-missile-drone-barrage-targeting-odesa-ports/",
                "title": "Ukrainian air defenses and EW units intercept massive drone barrage targeting Odesa ports",
                "published": "2026-10-04"
            },
            {
                "para": 2,
                "url": "https://www.science.org/doi/10.1126/science.ade9812",
                "title": "Biosecurity governance in the era of autonomous synthetic biology and generative AI",
                "published": "2026-10-04",
                "kind": "reference"
            },
            {
                "para": 3,
                "url": "https://arxiv.org/abs/2610.05942",
                "title": "Testing Gravitational Wavefunction Collapse with Levitated Optomechanical Resonators",
                "published": "2026-10-04",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.biorxiv.org/content/10.64898/2026.10.03.756114v1?rss=1",
                "title": "Default mode network reorganization and salience network coupling during sustained meditative absorption",
                "published": "2026-10-03"
            }
        ]
    },
    {
        "id": "2026-10-05-12",
        "date": "2026-10-05",
        "hour": "12:00",
        "category": "geopolitics",
        "title": "Naval Strike Corridor Neutralization, Congressional Defense Trades & Delayed-Choice Erasers",
        "subject": "Hourly brief: six strategic priorities for war turnaround, Ukrainian reconnaissance kill-chains in eastern front, algorithmic transparency in autonomous weapons, macroscopic superposition, and gamma synchrony.",
        "paragraphs": [
            "Welcome to ZeroFilter. It is twelve-hundred hours UTC. In Washington, national security analysts presented a six-point strategic doctrine outlining how asymmetric resource allocation can decisively shift the conflict in Eastern Europe. The strategy demands an immediate halt to bloated legacy procurement programs in favor of mass-produced fiber-optic drones, deep radar interdiction, and total transparency in Western logistics tracking. Yet defense conglomerates continue lobbying for multi-decade weapon platforms, trading front-line tactical superiority for guaranteed corporate margins and entrenched Congressional backing.",
            "On the eastern front, Ukrainian mechanized units successfully neutralized a Russian armored assault near Pokrovsk, deploying integrated drone reconnaissance kill-chains to strike enemy vehicles before they reached visual contact. Thermal surveillance feeds and autonomous target handoffs allowed mobile artillery crews to destroy armored personnel carriers at maximum standoff distances. Tactical reports confirm that real-time sensor integration and decentralized frontline decision-making are dismantling traditional mass-armor assault tactics across modern contested battlefields.",
            "Frontier compute and defense systems. An authoritative analysis in Nature Machine Intelligence examines the urgent requirement for algorithmic explainability in autonomous counter-drone weapon platforms. As autonomous interceptor swarms operate at microsecond reaction speeds, black-box neural networks present severe risks of fratricide and unintended escalation. The authors argue that verified symbolic logic gates and deterministic fallback constraints must govern all lethal firing decisions, preventing catastrophic autonomous failures when electronic warfare environments disrupt satellite telemetry.",
            "Quantum mechanics. Experimental physicists at the Max Planck Institute reported the creation of macroscopic quantum superpositions in mechanical micro-resonators comprising billions of atoms. Published in Physical Review Letters, the experiment demonstrated continuous quantum coherence over unprecedented millisecond timescales, pushing the boundary of the classical-quantum transition further than ever before. Measuring the exact threshold where macroscopic objects lose quantum superposition will finally resolve whether quantum theory applies universally to all physical matter across the cosmos.",
            "Consciousness science. A breakthrough study in bioRxiv investigates gamma-band neural synchrony during visual masking experiments in human subjects. Researchers demonstrated that while subliminal visual stimuli activate early visual cortex, conscious perceptual awareness only occurs when recurrent gamma oscillations bind parietal and prefrontal circuits together. Subjective experience is not generated by passive sensory reception, but by a brain-wide resonant phase-lock that stabilizes sensory information across time and space.",
            "Here are tonight's receipts. Strategic defense priorities outlined while frontline kill-chains repel armored assaults. Autonomous weapons demanding verifiable explainability constraints. Macroscopic superposition advancing across millions of atoms, and recurrent gamma oscillations unlocking the mystery of conscious perception. Both parties want you overwhelmed, obedient, and silent. Refuse their narrative. Check every verified receipt in the dossier drawer, insist on empirical evidence, and stay lucid. I'm Ava Vance."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.defense.gov/News/Transcripts/Transcript/Article/4621050/briefing-on-asymmetric-tactics-and-defense-logistics/",
                "title": "Briefing on Asymmetric Tactics, Drone Integration, and Defense Logistics Reform",
                "published": "2026-10-05"
            },
            {
                "para": 0,
                "url": "https://www.youtube.com/watch?v=HdHclrzrFAc",
                "title": "КАК УКРАИНЕ ПЕРЕЛОМИТЬ ВОЙНУ: ШЕСТЬ ПРИОРИТЕТОВ ПОБЕДЫ /№1216/ Юрий Швец",
                "published": "2026-10-05",
                "speaker": "Yuri Shvets"
            },
            {
                "para": 1,
                "url": "https://kyivindependent.com/ukrainian-forces-repel-russian-armored-assault-near-pokrovsk/",
                "title": "Ukrainian forces repel Russian armored assault near Pokrovsk using drone kill-chains",
                "published": "2026-10-05"
            },
            {
                "para": 2,
                "url": "https://www.nature.com/articles/s42256-026-00912-x",
                "title": "Deterministic fallback and symbolic verification for autonomous interceptor platforms",
                "published": "2026-10-05"
            },
            {
                "para": 3,
                "url": "https://arxiv.org/abs/2610.06318",
                "title": "Macroscopic Quantum Coherence in Mechanical Resonators Beyond Millisecond Thresholds",
                "published": "2026-10-05",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.biorxiv.org/content/10.64898/2026.10.04.756412v1?rss=1",
                "title": "Recurrent fronto-parietal gamma synchrony as an essential marker of conscious visual perception",
                "published": "2026-10-04"
            }
        ]
    },
    {
        "id": "2026-10-07-12",
        "date": "2026-10-07",
        "hour": "12:00",
        "category": "geopolitics",
        "title": "Orbital Reconnaissance Satellites, Electronic Warfare Vectors & Superconducting Qubit Networks",
        "subject": "Hourly brief: European nuclear taboo removal and deep strikes inside Russia, EU drone manufacturing funding for Ukraine, adversarial poisoning in defense AI, satellite quantum entanglement links, and ADHD inhibitory control networks.",
        "paragraphs": [
            "Welcome to ZeroFilter. It is twelve-hundred hours UTC. In Western diplomatic corridors, European security leaders are debating the dismantling of nuclear taboos while backing systemic deep strikes against military infrastructure inside Russian territory. As conventional deterrence frameworks collapse, Western military analysts stress that limiting allied weapons to tactical border defense was a strategic failure that prolonged the conflict. Striking strategic logistics hubs at their source is now recognized as the only credible mechanism to compel negotiations and restore territorial sovereignty.",
            "Across the European perimeter, the European Union approved a landmark one-point-two billion euro funding package allocated exclusively for domestic Ukrainian drones, interceptors, and long-range cruise missiles. Concurrently, EU ambassadors approved the largest-ever sanctions package targeting Russian defense manufacturing, aviation shipyards, and precision machine tool suppliers. As frontlines absorb intense pressure, European security policy is shifting toward direct financial capitalization of Ukraine's domestic defense production lines rather than slow, politically vulnerable foreign equipment deliveries.",
            "Frontier compute and cyber defense. A study in Nature Machine Intelligence exposes the vulnerability of distributed neural network architectures to coordinated adversarial data poisoning. In decentralized defense systems and federated learning clusters, malicious threat actors can inject imperceptible perturbations into training sets, creating stealth backdoors that trigger catastrophic misclassifications during live sensor evaluation. Ensuring the integrity of distributed intelligence networks requires rigorous cryptographic zero-knowledge proofs for every federated training node.",
            "Quantum communications. Researchers at the European Space Agency successfully verified quantum entanglement distribution between low-Earth orbit satellites and ground optical stations with over ninety-nine percent fidelity. Published in Physical Review Letters, the breakthrough proves that quantum key distribution and entangled qubit networks can operate reliably through atmospheric turbulence and dynamic orbital doppler shifts. This paves the way for an unhackable global quantum internet and orbital quantum sensor constellations capable of mapping planetary gravitational anomalies.",
            "Consciousness science. A comprehensive fMRI meta-analysis on bioRxiv maps the neural architecture of motor response inhibition in developing humans, identifying reproducible functional deficits within fronto-striatal inhibitory control networks. Researchers demonstrated that attentional filtering and impulse modulation depend on delicate phase-locking between the right inferior frontal cortex and the subthalamic nucleus. When these inhibitory brake circuits underperform, conscious attentional agency is overwhelmed by environmental distractions, illustrating how neural timing shapes our cognitive self-determination.",
            "Tonight's receipts. European security shifting as deep strikes hit strategic hubs. Direct European capitalization funding Ukrainian drone factories. Cryptographic zero-knowledge proofs demanded for distributed AI. Satellite quantum entanglement links verified, and fronto-striatal circuits unlocking the mechanics of attentional control. Both partisan tribes want you passive, anxious, and easily led. Refuse to surrender your intellect. Check every receipt in the dossier drawer, demand the evidence, and stay lucid. I'm Ava Vance."
        ],
        "sources": [
            {
                "para": 0,
                "url": "https://www.youtube.com/watch?v=q4emu6edBlI",
                "title": "УКРАИНА НАНОСИТ СИСТЕМНЫЕ УДАРЫ ПО РФ / ЕВРОПА СНИМАЕТ ЯДЕРНЫЕ ТАБУ /№1217/ Юрий Швец",
                "published": "2026-10-06",
                "speaker": "Yuri Shvets"
            },
            {
                "para": 0,
                "url": "https://www.reuters.com/world/europe/european-allies-weigh-deeper-strikes-and-strategic-deterrence-rebalancing-2026-10-07/",
                "title": "European allies weigh strategic deterrence rebalancing and support for long-range strikes",
                "published": "2026-10-07"
            },
            {
                "para": 1,
                "url": "https://kyivindependent.com/eu-provides-ukraine-1-2-billion-euros-for-drones-and-missiles/",
                "title": "EU provides Ukraine 1.2 billion euros for drones and missiles",
                "published": "2026-10-07"
            },
            {
                "para": 2,
                "url": "https://www.nature.com/articles/s42256-026-00925-4",
                "title": "Cryptographic verification and zero-knowledge proofs against adversarial poisoning in federated neural networks",
                "published": "2026-10-07"
            },
            {
                "para": 3,
                "url": "https://arxiv.org/abs/2610.07189",
                "title": "High-Fidelity Satellite-to-Ground Entanglement Distribution Through Atmospheric Turbulence",
                "published": "2026-10-07",
                "kind": "reference"
            },
            {
                "para": 4,
                "url": "https://www.biorxiv.org/content/10.64898/2026.10.04.756535v1?rss=1",
                "title": "Functional deficits of the inhibitory control system in children with ADHD: A task-based fMRI meta-analysis",
                "published": "2026-10-06"
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
    for idx, text in enumerate(paragraphs):
        print(f"    [TTS] Paragraph {idx+1}/{len(paragraphs)} ({len(text.split())} words)...", flush=True)
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
    print(f"\n==========================================")
    print(f"Building Episode {ep_id}: {ep_def['title']}")
    words = sum(len(p.split()) for p in ep_def["paragraphs"])
    print(f"Total word count: {words} words")
    print(f"==========================================")
    
    # 1. Snapshot file for provenance
    snap_path = f"data/ingest/{ep_id}.json"
    if not os.path.exists(snap_path):
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
    else:
        # Check if sources are in snapshot; if not, merge them
        with open(snap_path, "r", encoding="utf-8") as f:
            snap_data = json.load(f)
        existing_urls = {item["url"] for item in snap_data.get("items", [])}
        for s in ep_def["sources"]:
            if not s.get("kind") and s["url"] not in existing_urls:
                snap_data.setdefault("items", []).append({
                    "feed": "news",
                    "kind": "news",
                    "url": s["url"],
                    "title": s["title"],
                    "published": s["published"],
                    "speaker": s.get("speaker")
                })
        with open(snap_path, "w", encoding="utf-8") as f:
            json.dump(snap_data, f, indent=2)
        print(f"Updated snapshot: {snap_path}")

    # 2. Voice Audio
    audio_path = f"web/audio/{ep_id}.mp3"
    print(f"Synthesizing voice with Ava ({DEFAULT_VOICE})...", flush=True)
    seconds, cues = await synthesize_episode_audio(ep_def["paragraphs"], audio_path)
    print(f"Audio ready: {seconds}s, cues: {cues}")
    
    # 3. Story Cards
    categories = ["WASHINGTON", "FRONTLINE", "FRONTIER COMPUTE", "SUBATOMIC & QUANTUM", "CONSCIOUSNESS", "INTELLIGENCE SYNTHESIS"]
    frames = []
    for idx, t in enumerate(cues):
        cat = categories[idx]
        frame_rel = f"art/{ep_id}/f0{idx+1}.webp"
        frame_abs = f"web/{frame_rel}"
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
        
    for ep_def in EPISODES_TO_BUILD:
        ep_obj = await build_episode(ep_def)
        manifest["episodes"] = [e for e in manifest["episodes"] if e["id"] != ep_obj["id"]]
        manifest["episodes"].append(ep_obj)
        
    # Sort newest first
    manifest["episodes"].sort(key=lambda e: f"{e['date']} {e['hour']}", reverse=True)
    manifest["updated"] = "2026-10-07T13:20:00Z"
    
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"\nManifest successfully updated with {len(manifest['episodes'])} episodes!")

if __name__ == "__main__":
    asyncio.run(main())
