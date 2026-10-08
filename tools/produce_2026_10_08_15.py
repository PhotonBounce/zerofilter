#!/usr/bin/env python3
"""
tools/produce_2026_10_08_15.py - Autonomous Production for Episode 2026-10-08-15
"""

import os
import sys
import json
import math
import random
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent

EP_ID = "2026-10-08-15"
DATE = "2026-10-08"
HOUR = "15:00"

PARAGRAPHS = [
    "Welcome back to ZeroFilter. It is fifteen hundred hours UTC on the eighth of October. In eastern Ukraine, tragedy unfolded in Donetsk Oblast as a Russian glide bomb struck a municipal bus stop and commuter transit vehicles in Kramatorsk, killing at least thirty-three people and wounding dozens more. Donetsk Governor Vadym Filashkin confirmed that emergency rescue teams are sifting through heavy debris across the transit corridor. Meanwhile in Washington, the War Department's Office of Strategic Capital announced a 1.5 billion dollar conditional loan commitment to Wolfspeed, aiming to secure domestic manufacturing of military-grade silicon carbide semiconductor wafers across commercial fabrication facilities.",
    "Computing history loses a titan today. Margaret Hamilton, the visionary software engineer whose team developed the onboard flight guidance software for Apollo 11, has died at ninety. Hamilton famously coined the discipline name 'software engineering' and designed asynchronous priority scheduling algorithms that prevented Apollo's guidance computer from crashing during its historic 1969 lunar descent. Awarded the Presidential Medal of Freedom, her rigorous testing principles laid the mathematical bedrock for modern aerospace systems and mission-critical concurrent computing architecture.",
    "Geopolitical and military strategy. In his broadcast number twelve seventeen, Yuri Shvets examines how Ukraine's expanding campaign of precision drone strikes against Russian logistical hubs and domestic oil refineries is systematically disrupting rear-area operations. Shvets outlines how sustained interdiction is accelerating debate across European capitals, steadily dismantling historic diplomatic taboos regarding collective defense and long-range tactical deterrence.",
    "Frontier quantum information science. A new paper on arXiv demonstrates the teleportation of a programmable quantum gate. Researchers show how two distributed nodes, Alice and Bob, can successfully execute an arbitrary two-qubit gate with the assistance of a third node transmitting classical parameters. By leveraging shared entangled pairs alongside classical feedforward, this hybrid protocol opens realistic architectures for modular quantum networks, allowing distributed processing nodes to execute entangling operations without direct physical interaction.",
    "Neurobiology desk. Chronic neuroinflammation remains a primary driver of dopaminergic cell loss in Parkinson's disease. A new study on bioRxiv investigates microglial receptor signaling, demonstrating that targeted pharmacological inhibition of the microglial P2Y12 receptor significantly reduces inflammatory neurodegeneration. By decoupling harmful immune overactivation, researchers successfully preserved vulnerable dopamine pathways in the substantia nigra across experimental models, revealing a compelling therapeutic target for future clinical interventions.",
    "So, tonight's receipts. The deadly Kramatorsk bus stop strike, and a 1.5 billion dollar military semiconductor commitment. Honoring Apollo guidance pioneer Margaret Hamilton, systemic deep strike doctrines forcing European strategic realignments, programmable quantum gate teleportation, and microglial P2Y12 targets in Parkinson's research. Every single receipt is linked in the drawer. Verify them for yourself. I'm Ava Vance for ZeroFilter. Stay lucid."
]

SOURCES = [
    {
        "para": 0,
        "url": "https://kyivindependent.com/at-least-12-dead-after-russian-glide-bomb-strikes-kramatorsk-bus-stop/",
        "title": "At least 33 dead after Russian glide bomb strikes Kramatorsk buses",
        "published": "2026-10-08"
    },
    {
        "para": 0,
        "url": "https://www.war.gov/News/Releases/Release/Article/4621223/department-of-wars-office-of-strategic-capital-announces-15-billion-conditional/",
        "title": "Department of War's Office of Strategic Capital Announces $1.5 Billion Conditional Loan Commitment to Wolfspeed, Inc.",
        "published": "2026-10-08"
    },
    {
        "para": 1,
        "url": "https://www.bbc.co.uk/news/articles/cx5yn46j41zpo?at_medium=RSS&at_campaign=rss",
        "title": "Margaret Hamilton, whose software helped land Apollo 11 on the Moon, dies at 90",
        "published": "2026-10-08"
    },
    {
        "para": 2,
        "url": "https://www.youtube.com/watch?v=q4emu6edBlI",
        "title": "УКРАИНА НАНОСИТ СИСТЕМНЫЕ УДАРЫ ПО РФ / ЕВРОПА СНИМАЕТ ЯДЕРНЫЕ ТАБУ /№1217/ Юрий Швец",
        "published": "2026-10-06",
        "speaker": "Yuri Shvets"
    },
    {
        "para": 3,
        "url": "https://arxiv.org/abs/2610.09022",
        "title": "Teleportation of a programmable gate",
        "published": "2026-10-08"
    },
    {
        "para": 4,
        "url": "https://www.biorxiv.org/content/10.64898/2026.10.02.756181v1?rss=1",
        "title": "Targeting microglial P2Y12-receptor signalling attenuates neurodegeneration in experimental Parkinsons disease",
        "published": "2026-10-08"
    }
]

# Verify word count
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
    # Kramatorsk Bus Strike & Defense Silicon
    img = create_base((18, 12, 10), (6, 3, 2))
    draw = ImageDraw.Draw(img)
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(35, 20, 15), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(35, 20, 15), width=1)
    
    # Impact radar / blast crater zone
    for r in range(40, 260, 45):
        draw.ellipse([450 - r, 440 - r, 450 + r, 440 + r], outline=(255, 60, 30), width=2)
    # Bus silhouette / rubble
    draw.rectangle([340, 390, 560, 480], fill=(40, 25, 20), outline=(255, 100, 50), width=2)
    
    # Silicon wafer inset (Wolfspeed / OSC $1.5B loan)
    draw.ellipse([900, 300, 1160, 560], fill=(15, 30, 45), outline=(0, 230, 255), width=3)
    for rad in range(30, 120, 25):
        draw.ellipse([1030 - rad, 430 - rad, 1030 + rad, 430 + rad], outline=(0, 180, 200), width=1)
    draw.rectangle([960, 390, 1100, 470], fill=(10, 20, 30), outline=(0, 255, 180), width=2)
    
    draw.text((60, 60), "DONETSK OBLAST // KRAMATORSK MUNICIPAL TRANSIT ATTACK", fill=(255, 70, 50))
    draw.text((60, 90), "GLIDE BOMB IMPACT CASUALTIES // OSC $1.5B SILICON CARBIDE WAFER COMMITMENT", fill=(200, 210, 220))
    return add_noise(img)

def render_f02():
    # Margaret Hamilton & Apollo 11 Guidance Computer
    img = create_base((8, 12, 22), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    # Lunar trajectory arc
    draw.arc([100, 100, 1200, 900], start=190, end=350, fill=(0, 200, 255), width=2)
    # Lunar surface wireframe
    for x in range(0, W, 30):
        draw.line([(x, 600 + (x%60)*2), (x+15, 750)], fill=(30, 50, 80), width=1)
    # Apollo guidance computer code stack visualization
    draw.rectangle([540, 220, 830, 580], fill=(12, 20, 35), outline=(0, 240, 255), width=2)
    for y in range(250, 560, 20):
        draw.line([(560, y), (810, y)], fill=(60, 140, 200), width=2)
    
    draw.text((60, 60), "IN MEMORIAM // MARGARET HAMILTON (1936-2026)", fill=(0, 220, 255))
    draw.text((60, 90), "FOUNDER OF SOFTWARE ENGINEERING // APOLLO 11 ONBOARD FLIGHT SYSTEM", fill=(220, 230, 245))
    return add_noise(img)

def render_f03():
    # Yuri Shvets / Strategic Deep Strike Analysis
    img = create_base((12, 10, 20), (4, 3, 8))
    draw = ImageDraw.Draw(img)
    for x in range(0, W, 50):
        draw.line([(x, 0), (x, H)], fill=(25, 20, 40), width=1)
    # Strategic strike vectors
    draw.line([(300, 500), (600, 350)], fill=(255, 200, 50), width=3)
    draw.line([(600, 350), (950, 280)], fill=(255, 70, 70), width=3)
    draw.ellipse([930, 260, 970, 300], fill=(255, 50, 50), outline=(255, 255, 255), width=2)
    # Logistics node refinery target icon
    draw.rectangle([910, 320, 990, 420], fill=(20, 15, 30), outline=(255, 120, 50), width=2)
    
    draw.text((60, 60), "STRATEGIC ANALYSIS // YURI SHVETS BROADCAST #1217", fill=(255, 200, 60))
    draw.text((60, 90), "SYSTEMIC REAR-AREA INTERDICTION & EUROPEAN DETERRENCE REALIGNMENT", fill=(210, 210, 230))
    return add_noise(img)

def render_f04():
    # Programmable Quantum Gate Teleportation
    img = create_base((4, 16, 26), (1, 6, 12))
    draw = ImageDraw.Draw(img)
    # Alice, Bob, Charlie quantum teleportation network
    # Node Alice
    draw.ellipse([260, 340, 380, 460], fill=(10, 35, 55), outline=(0, 255, 200), width=3)
    draw.text((300, 390), "ALICE |q0>", fill=(255, 255, 255))
    # Node Bob
    draw.ellipse([990, 340, 1110, 460], fill=(10, 35, 55), outline=(0, 255, 200), width=3)
    draw.text((1030, 390), "BOB |q1>", fill=(255, 255, 255))
    # Mediator Node Charlie
    draw.rectangle([620, 200, 750, 310], fill=(20, 40, 65), outline=(255, 180, 0), width=2)
    draw.text((645, 245), "CHARLIE\nU(theta)", fill=(255, 220, 100))
    
    # Entanglement link between Alice and Bob
    draw.line([(380, 400), (990, 400)], fill=(0, 255, 255), width=2)
    # Classical assist lines
    draw.line([(685, 310), (320, 340)], fill=(255, 160, 50), width=1)
    draw.line([(685, 310), (1050, 340)], fill=(255, 160, 50), width=1)
    
    draw.text((60, 60), "QUANTUM INFORMATION // PROGRAMMABLE GATE TELEPORTATION", fill=(0, 255, 220))
    draw.text((60, 90), "ARXIV 2610.09022 // DISTRIBUTED 2-QUBIT LOGIC VIA CLASSICAL ASSIST", fill=(200, 220, 240))
    return add_noise(img)

def render_f05():
    # Microglial P2Y12 Receptor Inhibition in Parkinson's
    img = create_base((14, 6, 20), (5, 2, 8))
    draw = ImageDraw.Draw(img)
    # Microglia cell body and ramifications
    cx, cy = 680, 400
    for ang in range(0, 360, 30):
        rad = math.radians(ang)
        x2 = cx + int(math.cos(rad) * 220)
        y2 = cy + int(math.sin(rad) * 180)
        draw.line([(cx, cy), (x2, y2)], fill=(180, 60, 160), width=3)
        # Receptor sites
        draw.ellipse([x2 - 15, y2 - 15, x2 + 15, y2 + 15], fill=(255, 100, 200), outline=(255, 255, 255), width=2)
    draw.ellipse([cx - 50, cy - 40, cx + 50, cy + 40], fill=(80, 20, 70), outline=(220, 80, 180), width=3)
    
    draw.text((60, 60), "NEUROBIOLOGY // MICROGLIAL P2Y12-RECEPTOR SIGNALING", fill=(255, 120, 220))
    draw.text((60, 90), "BIORXIV // ATTENUATING DOPAMINERGIC NEURODEGENERATION IN PARKINSON'S", fill=(220, 200, 230))
    return add_noise(img)

def render_f06():
    # ZeroFilter Verified Receipts Drawer HUD
    img = create_base((6, 12, 20), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    # HUD frame borders
    draw.rectangle([40, 40, W - 40, H - 40], outline=(0, 220, 255), width=2)
    draw.line([(40, 130), (W - 40, 130)], fill=(0, 160, 200), width=1)
    
    receipts = [
        "[01] KYIV INDEPENDENT: 33 KILLED IN KRAMATORSK BUS GLIDE BOMB STRIKE",
        "[02] WAR DEPT OSC: $1.5B LOAN FOR WOLFSPEED SILICON CARBIDE WAFERS",
        "[03] BBC WORLD: APOLLO 11 SOFTWARE TITAN MARGARET HAMILTON DIES AT 90",
        "[04] YURI SHVETS #1217: SYSTEMIC UKRAINIAN DEEP STRIKES & EUROPEAN TABOOS",
        "[05] ARXIV 2610.09022: TELEPORTATION OF A PROGRAMMABLE QUANTUM GATE",
        "[06] BIORXIV: MICROGLIAL P2Y12 BLOCKADE IN PARKINSON'S DISEASE MODELS"
    ]
    for i, r in enumerate(receipts):
        draw.rectangle([80, 170 + i * 85, W - 80, 235 + i * 85], fill=(10, 20, 35), outline=(40, 90, 130), width=1)
        draw.text((110, 195 + i * 85), r, fill=(0, 240, 200))
        
    draw.text((60, 60), "ZEROFILTER VERIFIED RECEIPTS // HOUR 2026-10-08-15:00 UTC", fill=(0, 240, 255))
    draw.text((60, 90), "AVA VANCE ANCHOR // ALL SOURCED WIRES CROSS-EXAMINED", fill=(180, 200, 220))
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

# Update web/data/episodes.json
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
    "title": "Kramatorsk Strike, $1.5B Defense Silicon & Quantum Gate Teleportation",
    "subject": "Hourly sourced brief: Russian glide bomb strike kills 33 in Kramatorsk, War Department commits $1.5B to Wolfspeed for silicon carbide semiconductors, Apollo software pioneer Margaret Hamilton passes at 90, Yuri Shvets broadcast #1217, teleportation of programmable quantum gates on arXiv, and microglial P2Y12 receptor inhibition in Parkinson's disease.",
    "paragraphs": PARAGRAPHS,
    "sources": SOURCES,
    "art": {
        "frames": [
            {"t": 0, "src": f"art/{EP_ID}/f01.webp"},
            {"t": 30, "src": f"art/{EP_ID}/f02.webp"},
            {"t": 60, "src": f"art/{EP_ID}/f03.webp"},
            {"t": 90, "src": f"art/{EP_ID}/f04.webp"},
            {"t": 120, "src": f"art/{EP_ID}/f05.webp"},
            {"t": 150, "src": f"art/{EP_ID}/f06.webp"}
        ]
    },
    "seconds": 180,
    "audio": f"audio/{EP_ID}.mp3",
    "thumb": f"thumbs/{EP_ID}.webp",
    "cover_video": f"thumbs/{EP_ID}.mp4",
    "cues": [0, 30, 60, 90, 120, 150]
}

data["episodes"].insert(0, new_ep)
data["updated"] = f"{DATE}T{HOUR.replace(':', '')}00Z"

with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Updated {manifest_path} with new episode {EP_ID}.")
