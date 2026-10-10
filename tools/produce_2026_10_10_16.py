#!/usr/bin/env python3
"""
tools/produce_2026_10_10_16.py - Autonomous Production for Episode 2026-10-10-16
Trump's Putin Pivot, Russian Diesel Concessions & Yuri Shvets Intelligence Analysis
"""

import os
import sys
import json
import math
import random
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent

EP_ID = "2026-10-10-16"
DATE = "2026-10-10"
HOUR = "16:00"

PARAGRAPHS = [
    "Welcome back to ZeroFilter. It is sixteen hundred hours UTC on the tenth of October. Ukrainian national security officials report being completely blindsided by Donald Trump's diplomatic pivot to Vladimir Putin following repeated unmonitored telephone exchanges. In an exclusive investigation published by the Kyiv Independent, senior Kyiv defense officials revealed that sudden backchannel demands to capitulate sovereign territory felt like an orchestrated ambush. While European partners met in Miami attempting to stabilize defense coordination, Washington signaled readiness to permit Moscow to offload millions of tons of refined diesel into Western and global maritime markets.",
    "Economic concessions and sanctions rollback. The British Broadcasting Corporation and National Public Radio confirmed that Donald Trump announced a bilateral arrangement allowing Russian state petroleum refineries to supply diesel directly to Western distribution networks, deliberately easing economic sanctions on the Kremlin to suppress domestic fuel pump prices ahead of upcoming midterm elections. Ukrainian President Volodymyr Zelensky condemned the concession as an existential gift to Vladimir Putin, directly subsidizing Russia's wartime defense industrial base while Russian glide bomb salvos continue pounding civilian logistical infrastructure across eastern frontline oblasts.",
    "Strategic intelligence assessment. In a newly released intelligence briefing on his channel, former foreign intelligence officer Yuri Shvets analyzed the operational mechanics of Moscow's coercive leverage. Shvets emphasized that the Kremlin's periodic nuclear sabre-rattling and private telephone diplomacy are calibrated psychological operations designed to intimidate risk-averse Western political factions into unilateral concessions. According to Shvets, granting Moscow economic relief and territorial acquiescence rewards aggressive warfare and destabilizes European collective defense, dismantling eighty years of post-war security architecture.",
    "Frontier artificial intelligence research. Turning to computational frontiers, an investigation released on arXiv presents Synthesis Through Simulation: Generating Coherent Enterprise Data via Scalable Agent-System Interaction. Deploying multi-agent generative frameworks, computer scientists modeled high-dimensional organizational workflows to evaluate systemic failure modes. By simulating complex transactional negotiation graphs across hundreds of autonomous agents, researchers discovered emergent coordination bottlenecks and latent vulnerabilities, offering new mathematical benchmarks for stabilizing distributed decision networks against catastrophic multi-agent cascading errors.",
    "Frontier neuroscience desk. A pre-print published on bioRxiv delivers vital insights into human cognitive architecture. Neurobiologists discovered that the electrophysiological aperiodic slope of continuous electroencephalography during motor and cognitive learning directly predicts nocturnal sleep-based memory consolidation. Tracking high-density spectral power in human subjects, researchers proved that cortical excitation-to-inhibition balancing during daytime training dictates synaptic reorganization during subsequent slow-wave sleep cycles, unmasking the biophysical signatures of neural memory preservation.",
    "Tonight receipts. The Kyiv Independent exclusive on Donald Trump's phone pivot blindsiding Ukraine. The BBC and NPR reports on the Russian diesel concession overriding war sanctions. Frontline intelligence debriefs on the fatal trap of appeasing Kremlin nuclear coercion, scalable multi-agent enterprise simulations on arXiv, and electrophysiological aperiodic markers of memory consolidation on bioRxiv. Every receipt is linked in the source drawer. Read the wire reporting for yourself. I am Ava Vance for ZeroFilter. Stay lucid."
]

SOURCES = [
    {
        "para": 0,
        "url": "https://kyivindependent.com/exclusive-it-felt-like-a-trap-how-ukraine-was-blindsided-by-trumps-putin-pivot/",
        "title": "Exclusive: 'It felt like a trap.' How Ukraine was blindsided by Trump's Putin pivot",
        "published": "2026-10-10"
    },
    {
        "para": 0,
        "url": "https://kyivindependent.com/trump-says-russia-agreed-to-supply-millions-of-tons-of-diesel-to-us-global-markets/",
        "title": "Trump allows Russia to supply millions of tons of diesel to US, global markets",
        "published": "2026-10-09"
    },
    {
        "para": 1,
        "url": "https://www.bbc.co.uk/news/articles/cm1dwgr666wno?at_medium=RSS&at_campaign=rss",
        "title": "Trump announces deal for Russian diesel as Zelensky calls it a gift to Putin",
        "published": "2026-10-10"
    },
    {
        "para": 1,
        "url": "https://www.npr.org/2026/10/09/nx-s1-5996912/trump-says-u-s-to-get-diesel-from-russia-relaxing-pressure-on-moscow-to-ease-prices-before-midterms",
        "title": "Trump says U.S. to get diesel from Russia, relaxing pressure on Moscow to ease prices before midterms",
        "published": "2026-10-09"
    },
    {
        "para": 2,
        "url": "https://www.youtube.com/watch?v=IC4ArMD41AU",
        "speaker": "Yuri Shvets",
        "title": "ВОЙНА В УКРАИНЕ ПЕРЕСТРАИВАЕТ МИР / ПУТИН ТЕРЯЕТ ЯДЕРНЫЙ БЛЕФ /№1218/ Юрий Швец",
        "published": "2026-10-08"
    },
    {
        "para": 3,
        "url": "https://arxiv.org/abs/2610.10549",
        "title": "Synthesis Through Simulation: Generating Coherent Enterprise Data via Scalable Agent-System Interaction",
        "published": "2026-10-10"
    },
    {
        "para": 4,
        "url": "https://www.biorxiv.org/content/10.64898/2026.10.02.756363v1?rss=1",
        "title": "Using the aperiodic slope across learning to predict sleep-based memory consolidation",
        "published": "2026-10-10"
    }
]

# Output directories
OUT_DIR = ROOT / "web" / "art" / EP_ID
OUT_DIR.mkdir(parents=True, exist_ok=True)
THUMB_PATH = ROOT / "web" / "thumbs" / f"{EP_ID}.webp"
THUMB_PATH.parent.mkdir(parents=True, exist_ok=True)

W, H = 1376, 768

def create_base(top_color, bot_color):
    img = Image.new("RGB", (W, H), top_color)
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(top_color[0] * (1 - ratio) + bot_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bot_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bot_color[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img

def add_noise(img):
    pix = img.load()
    for _ in range(12000):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        r, g, b = pix[x, y]
        noise = random.randint(-18, 18)
        pix[x, y] = (max(0, min(255, r + noise)), max(0, min(255, g + noise)), max(0, min(255, b + noise)))
    return img

def render_f01():
    img = create_base((12, 14, 24), (4, 6, 12))
    draw = ImageDraw.Draw(img)
    # Geopolitical hotline and territorial map grid
    draw.rectangle([40, 40, W - 40, H - 40], outline=(0, 240, 255), width=2)
    draw.line([(40, 110), (W - 40, 110)], fill=(0, 180, 220), width=1)
    
    # Telephone waveform / intercept grid
    for x in range(100, W - 100, 30):
        h = int(math.sin(x * 0.04) * 80 + 100)
        draw.line([(x, 400 - h // 2), (x, 400 + h // 2)], fill=(255, 60, 60), width=4)
        
    draw.text((60, 60), "GEOPOLITICS // TRUMP-PUTIN PHONE DIPLOMACY & BACKCHANNEL PIVOT", fill=(0, 240, 255))
    draw.text((60, 85), "KYIV INDEPENDENT EXCLUSIVE // UKRAINE BLINDSIDED BY CAPITULATION PIVOT", fill=(180, 200, 220))
    return add_noise(img)

def render_f02():
    img = create_base((18, 10, 8), (6, 3, 2))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, W - 40, H - 40], outline=(255, 140, 0), width=2)
    draw.line([(40, 110), (W - 40, 110)], fill=(200, 100, 0), width=1)
    
    # Oil refinery towers and pipeline vectors
    draw.rectangle([200, 250, 450, 650], fill=(30, 20, 15), outline=(255, 120, 0), width=3)
    draw.rectangle([550, 300, 800, 650], fill=(30, 20, 15), outline=(255, 120, 0), width=3)
    draw.line([(450, 480), (550, 480)], fill=(255, 180, 50), width=8)
    draw.line([(800, 480), (1200, 480)], fill=(255, 180, 50), width=8)
    
    draw.text((60, 60), "COMMODITIES & SANCTIONS // RUSSIAN DIESEL RELIEF & MIDTERM PUMP ACCORD", fill=(255, 160, 0))
    draw.text((60, 85), "BBC & NPR // ZELENSKY WARNS CONCESSIONS DIRECTLY FUND KREMLIN MILITARY MACHINE", fill=(240, 210, 180))
    return add_noise(img)

def render_f03():
    img = create_base((8, 16, 26), (2, 5, 12))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, W - 40, H - 40], outline=(0, 240, 200), width=2)
    draw.line([(40, 110), (W - 40, 110)], fill=(0, 180, 150), width=1)
    
    # Yuri Shvets intelligence debriefing HUD
    draw.rectangle([150, 220, 1226, 620], fill=(10, 25, 35), outline=(0, 220, 180), width=2)
    draw.text((180, 260), "OFFICIAL DEBRIEF // YURI SHVETS (FORMER INTELLIGENCE OFFICER)", fill=(0, 240, 200))
    draw.text((180, 310), "ASSESSMENT: KREMLIN NUCLEAR SABRE-RATTLING & PRESSURE COERCION", fill=(200, 240, 230))
    draw.text((180, 360), "PSYCHOLOGICAL WARFARE TARGETING DOMESTIC US ELECTORAL VULNERABILITIES", fill=(180, 220, 210))
    draw.text((180, 420), "CONCESSIONS DEMANTLE EUROPEAN DETERRENCE AND ACCELERATE CONFLICT ESCALATION", fill=(255, 100, 100))
    
    draw.text((60, 60), "INTELLIGENCE DESK // YURI SHVETS DEBRIEF ON KREMLIN COERCIVE DIPLOMACY", fill=(0, 240, 200))
    draw.text((60, 85), "YOUTUBE #1218 // OPERATIONAL ANALYSIS OF WAR RESTRUCTURING & NUCLEAR BLUFF", fill=(180, 220, 210))
    return add_noise(img)

def render_f04():
    img = create_base((12, 10, 28), (4, 2, 14))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, W - 40, H - 40], outline=(160, 90, 255), width=2)
    draw.line([(40, 110), (W - 40, 110)], fill=(120, 60, 200), width=1)
    
    # Multi-agent simulation graph
    center_nodes = [(300, 400), (550, 300), (550, 500), (850, 300), (850, 500), (1100, 400)]
    for (x1, y1) in center_nodes:
        for (x2, y2) in center_nodes:
            if (x1, y1) != (x2, y2):
                draw.line([(x1, y1), (x2, y2)], fill=(70, 40, 110), width=1)
    for (x, y) in center_nodes:
        draw.ellipse([x - 20, y - 20, x + 20, y + 20], fill=(180, 100, 255), outline=(255, 255, 255), width=2)
        
    draw.text((60, 60), "AI ARCHITECTURE // SCALABLE MULTI-AGENT ENTERPRISE SIMULATION", fill=(180, 120, 255))
    draw.text((60, 85), "ARXIV 2610.10549 // MODELING TRANSACTIONAL DECISION GRAPHS UNDER STRESS", fill=(210, 190, 240))
    return add_noise(img)

def render_f05():
    img = create_base((10, 20, 20), (3, 7, 8))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, W - 40, H - 40], outline=(0, 255, 180), width=2)
    draw.line([(40, 110), (W - 40, 110)], fill=(0, 180, 120), width=1)
    
    # EEG Spectral Power / Aperiodic Slope Decay
    for x in range(150, 1200, 2):
        f = (x - 150) / 1050 * 50 + 1
        power = math.log10(1 / (f ** 1.8)) * 80 + 350
        draw.ellipse([x - 1, power - 1, x + 1, power + 1], fill=(0, 255, 200))
        
    draw.line([(150, 250), (1200, 550)], fill=(255, 90, 90), width=3)
    draw.text((700, 360), "APERIODIC SLOPE 1/f^χ // EXCITATION-INHIBITION BALANCE", fill=(255, 120, 120))
    
    draw.text((60, 60), "NEUROSCIENCE // APERIODIC SPECTRAL SLOPE & SLEEP MEMORY CONSOLIDATION", fill=(0, 255, 180))
    draw.text((60, 85), "BIORXIV // MOTOR LEARNING SYNAPTIC REORGANIZATION PREDICTOR", fill=(180, 230, 210))
    return add_noise(img)

def render_f06():
    img = create_base((8, 12, 22), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, W - 40, H - 40], outline=(0, 240, 255), width=2)
    draw.line([(40, 110), (W - 40, 110)], fill=(0, 160, 200), width=1)
    
    receipts = [
        "[01] KYIV INDEPENDENT: TRUMP PUTIN PIVOT BLINDSIDES UKRAINIAN DEFENSE LEADERSHIP",
        "[02] KYIV INDEPENDENT: RUSSIAN REFINED DIESEL EXPORT DEAL TO US & ALLIED MARKETS",
        "[03] BBC WORLD & NPR: ZELENSKY WARNS DIESEL CONCESSIONS DIRECTLY FUND INVASION",
        "[04] YURI SHVETS INTEL: DEBRIEF #1218 ON KREMLIN NUCLEAR BLUFF & PRESSURE STRATEGY",
        "[05] ARXIV 2610.10549: SCALABLE MULTI-AGENT ENTERPRISE SIMULATION & STRESS TEST",
        "[06] BIORXIV: APERIODIC SPECTRAL EEG SLOPE PREDICTS NOCTURNAL MEMORY CONSOLIDATION"
    ]
    for i, r in enumerate(receipts):
        draw.rectangle([80, 160 + i * 85, W - 80, 225 + i * 85], fill=(10, 20, 35), outline=(40, 90, 130), width=1)
        draw.text((110, 185 + i * 85), r, fill=(0, 240, 200))
        
    draw.text((60, 60), "ZEROFILTER VERIFIED RECEIPTS // HOUR 2026-10-10-16:00 UTC", fill=(0, 240, 255))
    draw.text((60, 85), "AVA VANCE ANCHOR // ALL SOURCES COLLECTED FROM HOURLY LIVE INGEST", fill=(180, 200, 220))
    return add_noise(img)

print("Rendering 6 1376x768 WebP story frames...")
renderers = [render_f01, render_f02, render_f03, render_f04, render_f05, render_f06]
for idx, fn in enumerate(renderers, 1):
    frame = fn()
    path = OUT_DIR / f"f{idx:02d}.webp"
    frame.save(path, "WEBP", quality=90)
    print(f"Saved {path}")

# Cover thumbnail
f01 = render_f01()
f01.save(THUMB_PATH, "WEBP", quality=85)
print(f"Saved cover thumbnail {THUMB_PATH}")

# Voice synthesis
sys.path.append(str(ROOT / "engine"))
from voice import synthesize_episode_audio

async def run_voice_and_manifest():
    out_audio = ROOT / "web" / "audio" / f"{EP_ID}.mp3"
    print(f"Synthesizing voice audio to {out_audio}...")
    seconds, cues = await synthesize_episode_audio(PARAGRAPHS, str(out_audio))
    print(f"Audio complete: {seconds}s, cues: {cues}")

    manifest_path = ROOT / "web" / "data" / "episodes.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Filter out if already exists
    data["episodes"] = [e for e in data.get("episodes", []) if e.get("id") != EP_ID]

    new_ep = {
        "id": EP_ID,
        "hour": HOUR,
        "date": DATE,
        "kind": "hourly",
        "category": "geopolitics",
        "ingest": EP_ID,
        "title": "Trump's Putin Pivot, Russian Diesel Concessions & Yuri Shvets on Kremlin Strategy",
        "subject": "Hourly sourced brief: Kyiv Independent details how Ukraine was blindsided by Trump's unmonitored Putin calls and territorial pressure, BBC and NPR verify bilateral Russian diesel export deal easing sanctions, Yuri Shvets intelligence debrief exposes Kremlin nuclear coercion tactics, scalable multi-agent enterprise simulations on arXiv, and bioRxiv reveals EEG aperiodic slope markers of memory consolidation.",
        "paragraphs": PARAGRAPHS,
        "sources": SOURCES,
        "art": {
            "frames": [
                {"t": cues[0], "src": f"art/{EP_ID}/f01.webp"},
                {"t": cues[1], "src": f"art/{EP_ID}/f02.webp"},
                {"t": cues[2], "src": f"art/{EP_ID}/f03.webp"},
                {"t": cues[3], "src": f"art/{EP_ID}/f04.webp"},
                {"t": cues[4], "src": f"art/{EP_ID}/f05.webp"},
                {"t": cues[5], "src": f"art/{EP_ID}/f06.webp"}
            ]
        },
        "seconds": round(seconds),
        "audio": f"audio/{EP_ID}.mp3",
        "thumb": f"thumbs/{EP_ID}.webp",
        "cover_video": f"thumbs/{EP_ID}.mp4",
        "cues": cues
    }

    data["episodes"].insert(0, new_ep)
    data["updated"] = f"{DATE}T{HOUR.replace(':', '')}00Z"

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Updated {manifest_path} with new episode {EP_ID}.")

asyncio.run(run_voice_and_manifest())
