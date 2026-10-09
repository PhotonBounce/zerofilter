#!/usr/bin/env python3
"""
tools/produce_2026_10_09_03.py - Autonomous Production for Episode 2026-10-09-03
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

EP_ID = "2026-10-09-03"
DATE = "2026-10-09"
HOUR = "03:00"

PARAGRAPHS = [
    "Welcome back to ZeroFilter. It is zero three hundred hours UTC on the ninth of October. In London, the United Kingdom unveiled a seventy-one million dollar emergency winter aid package for Ukraine, funding essential repairs to damaged power generation grids, decentralizing municipal heating plants, and shielding civilian communities. Meanwhile at Westminster Magistrates Court, a British service member made their first court appearance charged with espionage for Russia, accused of collecting protected military intelligence to assist foreign state agents. Defense officials reaffirmed that operational counterintelligence defenses remain fully heightened across European command theaters.",
    "Strategic defense procurement. In Washington, the Department of War executed a massive 6.3 billion dollar multi-year contract award to RTX subsidiary Raytheon. The commitment funds full-rate production and long-term sustainment for Standard Missile-3 Block IB interceptors, the frontline kinetic core of naval Aegis Ballistic Missile Defense systems. Under the contract terms, Raytheon will expand domestic manufacturing lines to replenish depleted munitions inventories, harden aerospace supply chains against sub-tier bottlenecks, and sustain maritime deterrence across both Indo-Pacific and European naval theaters.",
    "Global culture desk. The Swedish Academy has officially awarded the 2026 Nobel Prize in Literature to Canadian poet and classical scholar Anne Carson. Carson was recognized for her luminous, genre-defying oeuvre bridging ancient Greek drama with radical contemporary verse. Celebrated internationally for seminal works like Autobiography of Red and Nox, Carson combines classical scholarship with mathematical emotional precision, deconstructing conventional narrative forms to examine grief, erotic obsession, and human mortality on the global literary stage.",
    "Frontier quantum science. A new pre-print on arXiv introduces a major step forward in neutral-atom quantum computing: high-fidelity inter-species Rydberg gates via optimized two-photon driving. Dual-species optical tweezer arrays have long struggled with laser phase noise and state leakage during entangling pulses. By optimizing intermediate detuning and dynamic pulse shaping, researchers achieved two-qubit entangling gates between distinct atomic elements with fidelities surpassing ninety-eight percent, opening a clean path toward crosstalk-free quantum error correction.",
    "Neurobiology desk. An investigation on bioRxiv uncovers a direct molecular pathway linking dietary nutrients to synaptic plasticity. Researchers demonstrated that oral magnesium supplementation enhances long-term spatial memory by activating the intracellular Hippo signaling cascade. In animal models, increased extracellular magnesium promoted nuclear translocation of the coactivator YAP within hippocampal neurons, stimulating dendritic spine morphogenesis and synaptic potentiation to protect against cognitive decline.",
    "So, tonight receipts. The United Kingdom seventy-one million dollar winter energy package alongside military espionage proceedings. The War Department 6.3 billion dollar Raytheon interceptor contract. Anne Carson Nobel Prize in Literature, high-fidelity inter-species Rydberg gates, and magnesium-activated Hippo pathways enhancing memory. Every receipt is verified and linked in the drawer. Check the source wires for yourself. I am Ava Vance for ZeroFilter. Stay lucid."
]

SOURCES = [
    {
        "para": 0,
        "url": "https://kyivindependent.com/uk-to-provide-71-million-winter-aid-package-to-ukraine/",
        "title": "UK to provide $71 million winter aid package to Ukraine",
        "published": "2026-10-09"
    },
    {
        "para": 0,
        "url": "https://kyivindependent.com/uk-service-member-charged-with-spying-for-russia-makes-first-court-appearance/",
        "title": "UK service member charged with spying for Russia makes first court appearance",
        "published": "2026-10-08"
    },
    {
        "para": 1,
        "url": "https://www.war.gov/News/Releases/Release/Article/4622796/department-of-war-awards-63-billion-multi-year-contract-to-rtxs-raytheon-for-sm/",
        "title": "Department of War Awards $6.3 Billion Multi-Year Contract to RTX's Raytheon for SM-3 BLOCK IB Interceptors",
        "published": "2026-10-08"
    },
    {
        "para": 2,
        "url": "https://www.bbc.co.uk/news/articles/cq4g1j54nepyo?at_medium=RSS&at_campaign=rss",
        "title": "'Bold and inventive' Canadian poet Anne Carson wins Nobel Literature Prize",
        "published": "2026-10-08"
    },
    {
        "para": 3,
        "url": "https://arxiv.org/abs/2610.08926",
        "title": "High-Fidelity Inter-Species Rydberg Gates with Two-Photon Driving",
        "published": "2026-10-08"
    },
    {
        "para": 4,
        "url": "https://www.biorxiv.org/content/10.64898/2026.10.02.756214v1?rss=1",
        "title": "Dietary magnesium supplement enhances memory through Hippo signaling",
        "published": "2026-10-08"
    }
]

total_words = sum(len(p.split()) for p in PARAGRAPHS)
print(f"Total words: {total_words} (Formula target: 430-490)")
assert 430 <= total_words <= 490, f"Word count {total_words} outside formula range"

# --- Art Generation ---
W, H = 1376, 768
OUT_DIR = ROOT / "web" / "art" / EP_ID
THUMB_PATH = ROOT / "web" / "thumbs" / f"{EP_ID}.webp"

OUT_DIR.mkdir(parents=True, exist_ok=True)
(ROOT / "web" / "thumbs").mkdir(parents=True, exist_ok=True)

def create_base(c1, c2):
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        ratio = y / H
        r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
        g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
        b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    return img

def add_noise(img):
    draw = ImageDraw.Draw(img)
    for _ in range(3000):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        draw.point((x, y), fill=(random.randint(180, 255), random.randint(180, 255), random.randint(180, 255)))
    return img

def render_f01():
    # UK Winter Aid & Espionage Arrest
    img = create_base((10, 16, 28), (4, 7, 14))
    draw = ImageDraw.Draw(img)
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(20, 32, 50), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(20, 32, 50), width=1)
    
    # Power grid & winter heating conduits
    for i in range(5):
        y_pos = 280 + i * 50
        draw.line([(120, y_pos), (580, y_pos)], fill=(0, 200, 255), width=2)
        draw.rectangle([580, y_pos - 10, 640, y_pos + 10], fill=(15, 30, 50), outline=(0, 240, 255), width=1)
    
    # Energy substation icon
    draw.rectangle([180, 550, 480, 680], fill=(12, 24, 40), outline=(0, 220, 255), width=2)
    draw.text((210, 600), "UK WINTER ENERGY AID // $71M", fill=(0, 240, 255))
    
    # Counterintelligence / Westminster court shield
    draw.polygon([(880, 240), (1140, 240), (1200, 420), (1010, 620), (820, 420)], fill=(24, 16, 30), outline=(255, 120, 40), width=3)
    draw.line([(1010, 240), (1010, 620)], fill=(255, 140, 50), width=2)
    draw.text((890, 380), "WESTMINSTER\nCOUNTER-ESPIONAGE", fill=(255, 180, 60))
    
    draw.text((60, 60), "UKRAINE WINTER PACKAGE // $71M POWER GRID & INFRASTRUCTURE RESTORATION", fill=(0, 230, 255))
    draw.text((60, 90), "WESTMINSTER MAGISTRATES // ARMED FORCES SERVICE MEMBER CHARGED WITH ESPIONAGE", fill=(220, 210, 190))
    return add_noise(img)

def render_f02():
    # Raytheon $6.3B SM-3 Block IB Interceptors
    img = create_base((8, 14, 24), (2, 5, 10))
    draw = ImageDraw.Draw(img)
    # Phased array radar sweeps
    for r in range(80, 500, 80):
        draw.arc([400 - r, 500 - r, 400 + r, 500 + r], start=220, end=350, fill=(0, 180, 255), width=1)
    
    # Ballistic trajectory vs kinetic intercept vector
    draw.line([(200, 650), (950, 220)], fill=(255, 180, 40), width=3) # Intercept boost
    draw.line([(1200, 150), (950, 220)], fill=(255, 60, 60), width=2) # Incoming warhead
    draw.ellipse([935, 205, 965, 235], fill=(255, 240, 100), outline=(255, 80, 50), width=3) # Kinetic impact point
    
    # Tactical missile telemetry box
    draw.rectangle([100, 200, 440, 380], fill=(10, 20, 35), outline=(0, 220, 255), width=2)
    draw.text((120, 220), "AEGIS BMD // SM-3 BLOCK IB", fill=(0, 240, 255))
    draw.text((120, 260), "CONTRACT: $6.3 BILLION\nVENDOR: RTX RAYTHEON\nSTATUS: FULL-RATE PRODUCTION", fill=(200, 220, 240))
    
    draw.text((60, 60), "MISSILE DEFENSE // DEPARTMENT OF WAR CONTRACT AWARD", fill=(255, 200, 50))
    draw.text((60, 90), "RTX RAYTHEON // $6.3B MULTI-YEAR PROCUREMENT OF SM-3 BLOCK IB INTERCEPTORS", fill=(210, 220, 235))
    return add_noise(img)

def render_f03():
    # Anne Carson Nobel Prize in Literature
    img = create_base((18, 10, 26), (6, 3, 10))
    draw = ImageDraw.Draw(img)
    
    # Classical Greek column motifs and geometric verse lines
    for i in range(4):
        x = 220 + i * 80
        draw.line([(x, 240), (x, 620)], fill=(80, 50, 100), width=4)
        draw.rectangle([x - 15, 220, x + 15, 240], fill=(120, 80, 150), outline=(240, 200, 80), width=1)
        draw.rectangle([x - 15, 620, x + 15, 640], fill=(120, 80, 150), outline=(240, 200, 80), width=1)
        
    # Nobel Medallion representation
    cx, cy, mr = 850, 420, 160
    draw.ellipse([cx - mr, cy - mr, cx + mr, cy + mr], fill=(40, 25, 10), outline=(240, 200, 80), width=4)
    draw.ellipse([cx - mr + 20, cy - mr + 20, cx + mr - 20, cy + mr - 20], outline=(200, 160, 50), width=2)
    draw.text((cx - 85, cy - 25), "NOBEL PRIZE\nLITERATURE 2026\nANNE CARSON", fill=(255, 220, 100))
    
    draw.text((60, 60), "GLOBAL CULTURE // SWEDISH ACADEMY ANNOUNCEMENT", fill=(240, 200, 90))
    draw.text((60, 90), "CANADIAN POET ANNE CARSON AWARDED 2026 NOBEL PRIZE IN LITERATURE", fill=(230, 210, 240))
    return add_noise(img)

def render_f04():
    # Inter-Species Rydberg Gates with Two-Photon Driving
    img = create_base((4, 18, 28), (1, 6, 12))
    draw = ImageDraw.Draw(img)
    
    # Two-species tweezer array
    for idx, (x, col, label) in enumerate([(420, (0, 255, 200), "SPECIES A (Rb)"), (900, (255, 120, 200), "SPECIES B (Cs)")]):
        draw.ellipse([x - 60, 380, x + 60, 500], fill=(10, 30, 45), outline=col, width=3)
        draw.text((x - 45, 430), label, fill=col)
        # Laser driving arrows
        draw.line([(x, 220), (x, 380)], fill=(0, 220, 255), width=2)
        draw.line([(x + 20, 220), (x + 20, 380)], fill=(255, 200, 50), width=2)
        draw.text((x - 40, 190), "2-PHOTON DRIVE", fill=(200, 220, 255))
        
    # Entanglement blockade radius
    draw.ellipse([320, 300, 1000, 580], outline=(0, 240, 255), width=1)
    draw.line([(480, 440), (840, 440)], fill=(0, 255, 180), width=3)
    draw.text((580, 410), "RYDBERG BLOCKADE // FIDELITY > 98%", fill=(0, 255, 200))
    
    draw.text((60, 60), "QUANTUM COMPUTING // NEUTRAL-ATOM HYBRID ARCHITECTURES", fill=(0, 255, 200))
    draw.text((60, 90), "ARXIV 2610.08926 // HIGH-FIDELITY INTER-SPECIES RYDBERG GATES VIA TWO-PHOTON DRIVING", fill=(200, 220, 240))
    return add_noise(img)

def render_f05():
    # Magnesium Enhancing Memory via Hippo Signaling
    img = create_base((16, 6, 22), (5, 2, 8))
    draw = ImageDraw.Draw(img)
    
    # Hippocampal neuron dendrite and spine heads
    draw.line([(180, 450), (1150, 450)], fill=(180, 60, 160), width=14)
    # Synaptic spines
    for sx in range(250, 1100, 110):
        draw.line([(sx, 450), (sx, 320)], fill=(180, 60, 160), width=6)
        draw.ellipse([sx - 25, 280, sx + 25, 330], fill=(80, 20, 70), outline=(255, 120, 220), width=2)
        # Mg2+ ions entering
        draw.ellipse([sx - 10, 220, sx + 10, 240], fill=(255, 220, 80), outline=(255, 255, 255), width=1)
        draw.text((sx - 12, 245), "Mg²⁺", fill=(255, 220, 80))
        
    # Hippo pathway / YAP translocation badge
    draw.rectangle([450, 530, 880, 660], fill=(20, 10, 30), outline=(255, 90, 190), width=2)
    draw.text((480, 560), "HIPPO SIGNALING // YAP NUCLEAR TRANSLOCATION", fill=(255, 130, 220))
    draw.text((480, 600), "ENHANCED SYNAPTIC PLASTICITY & LONG-TERM SPATIAL RETRIEVAL", fill=(220, 200, 230))
    
    draw.text((60, 60), "NEUROBIOLOGY // NUTRITIONAL CHEMISTRY & SYNAPTIC PLASTICITY", fill=(255, 120, 220))
    draw.text((60, 90), "BIORXIV // DIETARY MAGNESIUM ACTIVATES HIPPO PATHWAY TO ENHANCE MEMORY", fill=(220, 200, 230))
    return add_noise(img)

def render_f06():
    # ZeroFilter Receipts HUD
    img = create_base((6, 12, 20), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    draw.rectangle([40, 40, W - 40, H - 40], outline=(0, 220, 255), width=2)
    draw.line([(40, 130), (W - 40, 130)], fill=(0, 160, 200), width=1)
    
    receipts = [
        "[01] KYIV INDEPENDENT: UK $71M EMERGENCY WINTER AID PACKAGE FOR UKRAINE",
        "[02] KYIV INDEPENDENT: BRITISH SERVICE MEMBER FACES RUSSIAN ESPIONAGE CHARGES",
        "[03] WAR DEPT: $6.3B MULTI-YEAR RAYTHEON CONTRACT FOR SM-3 BLOCK IB INTERCEPTORS",
        "[04] BBC WORLD: CANADIAN POET ANNE CARSON WINS 2026 NOBEL PRIZE IN LITERATURE",
        "[05] ARXIV 2610.08926: HIGH-FIDELITY INTER-SPECIES RYDBERG QUANTUM GATES",
        "[06] BIORXIV: DIETARY MAGNESIUM ACTIVATES HIPPO PATHWAY TO ENHANCE MEMORY"
    ]
    for i, r in enumerate(receipts):
        draw.rectangle([80, 170 + i * 85, W - 80, 235 + i * 85], fill=(10, 20, 35), outline=(40, 90, 130), width=1)
        draw.text((110, 195 + i * 85), r, fill=(0, 240, 200))
        
    draw.text((60, 60), "ZEROFILTER VERIFIED RECEIPTS // HOUR 2026-10-09-03:00 UTC", fill=(0, 240, 255))
    draw.text((60, 90), "AVA VANCE ANCHOR // ALL WIRE RECEIPTS TRACED AND VERIFIED", fill=(180, 200, 220))
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
        "title": "UK Winter Shield, $6.3B Raytheon Interceptors & Nobel Laureate Anne Carson",
        "subject": "Hourly sourced brief: UK commits $71M winter energy aid to Ukraine, British soldier charged with espionage for Russia, Department of War awards $6.3B to Raytheon for SM-3 Block IB interceptors, Anne Carson wins 2026 Nobel Prize in Literature, high-fidelity inter-species Rydberg gates on arXiv, and dietary magnesium memory enhancement via Hippo pathway on bioRxiv.",
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
