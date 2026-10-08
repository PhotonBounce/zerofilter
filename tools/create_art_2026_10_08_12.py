import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1376, 768
OUT_DIR = "web/art/2026-10-08-12"
THUMB_PATH = "web/thumbs/2026-10-08-12.webp"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs("web/thumbs", exist_ok=True)

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

def add_noise(img, factor=12):
    draw = ImageDraw.Draw(img)
    for _ in range(3000):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        draw.point((x, y), fill=(random.randint(180, 255), random.randint(180, 255), random.randint(180, 255)))
    return img

def render_f01():
    # Secret ICE warehouse detention facility / industrial night surveillance
    img = create_base((8, 12, 20), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    
    # Industrial warehouse skyline
    draw.rectangle([100, 320, 550, 768], fill=(12, 16, 24), outline=(30, 45, 65), width=2)
    draw.rectangle([500, 240, 1100, 768], fill=(16, 22, 32), outline=(40, 55, 80), width=2)
    draw.rectangle([1050, 360, 1320, 768], fill=(10, 14, 20), outline=(25, 38, 55), width=2)
    
    # Warehouse windows
    for row in range(4):
        for col in range(8):
            wx = 540 + col * 65
            wy = 280 + row * 90
            color = (255, 180, 70) if (row + col) % 3 == 0 else (30, 40, 55)
            draw.rectangle([wx, wy, wx + 40, wy + 55], fill=color)

    # High-intensity surveillance spotlight cone
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.polygon([(820, 220), (200, 768), (1200, 768)], fill=(255, 230, 150, 40))
    ov_draw.polygon([(820, 220), (450, 768), (950, 768)], fill=(255, 240, 200, 60))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    
    # Razor wire / security fence in foreground
    draw = ImageDraw.Draw(img)
    for x in range(0, W, 40):
        draw.line([(x, 620), (x + 30, 768)], fill=(120, 140, 160), width=2)
        draw.line([(x + 30, 620), (x, 768)], fill=(100, 120, 140), width=2)
    draw.line([(0, 620), (W, 620)], fill=(180, 190, 200), width=3)
    draw.line([(0, 680), (W, 680)], fill=(140, 150, 160), width=2)
    
    # HUD text
    draw.text((60, 60), "FACILITY INTEL // ROXBURY NJ WAREHOUSE", fill=(255, 170, 0))
    draw.text((60, 90), "SURVEILLANCE GRID 40.89°N 74.65°W · UNLISTED DETENTION LOGISTICS", fill=(140, 180, 220))
    
    return add_noise(img)

def render_f02():
    # Russian shadow-fleet maritime tanker / UK sanctions intercept radar
    img = create_base((4, 15, 25), (1, 6, 12))
    draw = ImageDraw.Draw(img)
    
    # Ocean horizon & dark waves
    for y in range(480, H, 12):
        shade = int(20 + (y - 480) * 0.4)
        draw.line([(0, y), (W, y)], fill=(shade, shade + 15, shade + 35), width=6)
        
    # Massive shadow-fleet crude tanker silhouette
    hull = [(150, 520), (320, 460), (1050, 460), (1200, 500), (1150, 570), (200, 570)]
    draw.polygon(hull, fill=(18, 22, 28), outline=(60, 80, 100), width=2)
    # Bridge tower & superstructure
    draw.rectangle([920, 360, 1080, 460], fill=(24, 30, 38), outline=(70, 95, 120), width=2)
    draw.rectangle([960, 300, 1020, 360], fill=(20, 26, 34), outline=(60, 85, 110), width=2)
    draw.line([(990, 240), (990, 300)], fill=(180, 200, 220), width=3) # Antenna mast
    
    # Radar scope overlay
    radar = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(radar)
    cx, cy = 450, 320
    for r in [60, 120, 180, 240]:
        r_draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 240, 180, 90), width=2)
    r_draw.line([(cx - 260, cy), (cx + 260, cy)], fill=(0, 240, 180, 70), width=1)
    r_draw.line([(cx, cy - 260), (cx, cy + 260)], fill=(0, 240, 180, 70), width=1)
    # Radar sweep beam
    r_draw.polygon([(cx, cy), (cx + 240, cy - 100), (cx + 220, cy - 170)], fill=(0, 255, 180, 50))
    # Target blips
    r_draw.ellipse([cx + 90, cy - 60, cx + 98, cy - 52], fill=(255, 60, 60, 220))
    r_draw.text((cx + 105, cy - 65), "INTERCEPT // SHADOW TANKER #401", fill=(255, 80, 80, 240))
    
    img.paste(Image.alpha_composite(img.convert("RGBA"), radar).convert("RGB"))
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "MARITIME INTERDICTION // UK SANCTIONS", fill=(0, 240, 200))
    draw.text((60, 90), "NORTH SEA CORRIDOR · OIL & CRYPTO TRADING SYNDICATE BLOCKED", fill=(160, 200, 220))
    
    return add_noise(img)

def render_f03():
    # Frontier compute: Quantum readout complexity / quantum processor lattices
    img = create_base((12, 6, 24), (4, 2, 10))
    draw = ImageDraw.Draw(img)
    
    # Silicon wafer grid and gold circuit traces
    cx, cy = W // 2, H // 2
    for ring in range(12):
        radius = 80 + ring * 45
        draw.rectangle([cx - radius, cy - radius, cx + radius, cy + radius], outline=(70, 40, 120), width=1)
        
    for angle in range(0, 360, 15):
        rad = math.radians(angle)
        x1 = cx + math.cos(rad) * 90
        y1 = cy + math.sin(rad) * 90
        x2 = cx + math.cos(rad) * 480
        y2 = cy + math.sin(rad) * 480
        draw.line([(x1, y1), (x2, y2)], fill=(210, 160, 40) if angle % 30 == 0 else (120, 80, 180), width=2 if angle % 30 == 0 else 1)
        
    # Central quantum core with glowing qubits
    draw.rectangle([cx - 90, cy - 90, cx + 90, cy + 90], fill=(25, 14, 45), outline=(0, 230, 255), width=3)
    for qx in range(-2, 3):
        for qy in range(-2, 3):
            qx_pos = cx + qx * 30
            qy_pos = cy + qy * 30
            draw.ellipse([qx_pos - 6, qy_pos - 6, qx_pos + 6, qy_pos + 6], fill=(0, 255, 220))
            
    # Matrix maths & readout complexity annotations
    draw.text((60, 60), "FRONTIER COMPUTE // QUANTUM READOUT COMPLEXITY", fill=(0, 230, 255))
    draw.text((60, 90), "ARXIV:2610.08890 · NORMALIZED LINEAR FUNCTIONAL BOUNDS", fill=(200, 170, 255))
    draw.text((cx - 160, cy + 180), "STATE VECTOR TRANSFORMATION: ⟨ψ|M|ψ⟩ ≤ O(1/ε²)", fill=(240, 190, 80))
    
    return add_noise(img)

def render_f04():
    # Two-photon driving neutral-atom Rydberg optical trap
    img = create_base((3, 10, 22), (1, 3, 8))
    draw = ImageDraw.Draw(img)
    
    cx, cy = W // 2, H // 2
    
    # Laser optical cross-beams (two-photon laser excitation)
    beam = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    b_draw = ImageDraw.Draw(beam)
    
    # 780nm (amber/red) and 480nm (electric cyan/blue) beams intersecting
    b_draw.line([(0, cy - 140), (W, cy + 140)], fill=(255, 90, 40, 140), width=18)
    b_draw.line([(0, cy - 140), (W, cy + 140)], fill=(255, 200, 120, 220), width=6)
    
    b_draw.line([(0, cy + 140), (W, cy - 140)], fill=(0, 180, 255, 140), width=18)
    b_draw.line([(0, cy + 140), (W, cy - 140)], fill=(160, 240, 255, 220), width=6)
    
    # Dual-species neutral atom optical tweezers array
    for i in range(-5, 6):
        ax = cx + i * 85
        # Species A (Rubidium)
        b_draw.ellipse([ax - 18, cy - 40, ax + 18, cy - 4], fill=(255, 110, 50, 220), outline=(255, 220, 180, 255), width=2)
        # Species B (Cesium)
        b_draw.ellipse([ax - 18, cy + 4, ax + 18, cy + 40], fill=(0, 210, 255, 220), outline=(180, 255, 255, 255), width=2)
        # Entanglement coupling line
        b_draw.line([(ax, cy - 22), (ax, cy + 22)], fill=(255, 255, 255, 180), width=2)
        
    img.paste(Image.alpha_composite(img.convert("RGBA"), beam).convert("RGB"))
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "PRECISION QUANTUM // INTER-SPECIES RYDBERG GATES", fill=(255, 160, 80))
    draw.text((60, 90), "ARXIV:2610.08926 · TWO-PHOTON COHERENT DRIVING LATTICE", fill=(140, 220, 255))
    
    return add_noise(img)

def render_f05():
    # Consciousness desk: Neural latent representations / Intracranial EEG
    img = create_base((18, 4, 14), (5, 1, 4))
    draw = ImageDraw.Draw(img)
    
    # Cortical silhouette and neural connectome network
    cx, cy = W // 2, H // 2
    nodes = []
    for _ in range(80):
        nx = random.randint(cx - 450, cx + 450)
        ny = random.randint(cy - 220, cy + 220)
        nodes.append((nx, ny))
        
    for i in range(len(nodes)):
        for j in range(i + 1, min(i + 5, len(nodes))):
            dist = math.hypot(nodes[i][0] - nodes[j][0], nodes[i][1] - nodes[j][1])
            if dist < 140:
                alpha = int(255 * (1 - dist / 140))
                draw.line([nodes[i], nodes[j]], fill=(240, 70, 120), width=1)
                
    for n in nodes:
        draw.ellipse([n[0] - 5, n[1] - 5, n[0] + 5, n[1] + 5], fill=(255, 200, 220), outline=(255, 50, 100), width=2)
        
    # EEG Waveforms across the base
    for row in range(3):
        wy = 540 + row * 60
        prev_pt = (0, wy)
        for x in range(0, W, 8):
            freq = 0.04 * (row + 1)
            noise_val = math.sin(x * freq) * 22 + math.cos(x * 0.12) * 8
            pt = (x, int(wy + noise_val))
            draw.line([prev_pt, pt], fill=(255, 100, 150) if row == 1 else (180, 60, 90), width=2)
            prev_pt = pt

    draw.text((60, 60), "CONSCIOUSNESS DESK // INTRACRANIAL LATENT CONFIDENCE", fill=(255, 120, 160))
    draw.text((60, 90), "BIORXIV · PRE-RESPONSE CONFIDENCE SIGNATURES ACROSS DEEP CORTEX", fill=(240, 190, 200))
    
    return add_noise(img)

def render_f06():
    # Ava Vance ZeroFilter bunker studio / receipts broadcast closing
    img = create_base((10, 16, 26), (3, 6, 12))
    draw = ImageDraw.Draw(img)
    
    # Concrete bunker wall panels & studio acoustic diffusers
    for x in range(0, W, 180):
        draw.line([(x, 0), (x, H)], fill=(25, 38, 55), width=2)
        for y in range(0, H, 140):
            draw.rectangle([x + 10, y + 10, x + 170, y + 130], outline=(35, 50, 72), width=1)
            
    # Central host desk with golden amber microphone and telemetry monitors
    draw.polygon([(280, 520), (1096, 520), (1240, 768), (136, 768)], fill=(16, 24, 34), outline=(0, 220, 200), width=2)
    # Broadcast audio console & spectrum display
    draw.rectangle([480, 560, 896, 720], fill=(8, 12, 18), outline=(60, 90, 120), width=2)
    for b in range(32):
        bx = 500 + b * 12
        bh = random.randint(15, 95)
        draw.rectangle([bx, 700 - bh, bx + 8, 700], fill=(0, 240, 180) if b < 24 else (255, 160, 40))
        
    # Studio broadcast mic silhouette
    draw.rectangle([670, 420, 706, 510], fill=(220, 170, 50), outline=(255, 230, 140), width=2)
    draw.line([(688, 510), (688, 560)], fill=(180, 180, 180), width=5)
    
    # Broadcast graphic overlay
    draw.text((60, 60), "ZEROFILTER BROADCAST STUDIO // AVA VANCE", fill=(0, 240, 200))
    draw.text((60, 90), "EPISODE 2026-10-08-12 · RECEIPTS COMPLETE · STAY LUCID", fill=(200, 220, 240))
    
    return add_noise(img)

def render_thumb():
    # Composite dramatic cover
    f1 = render_f01().resize((W // 2, H // 2))
    f2 = render_f02().resize((W // 2, H // 2))
    f3 = render_f04().resize((W // 2, H // 2))
    f4 = render_f06().resize((W // 2, H // 2))
    
    thumb = Image.new("RGB", (W, H))
    thumb.paste(f1, (0, 0))
    thumb.paste(f2, (W // 2, 0))
    thumb.paste(f3, (0, H // 2))
    thumb.paste(f4, (W // 2, H // 2))
    
    draw = ImageDraw.Draw(thumb)
    draw.line([(W // 2, 0), (W // 2, H)], fill=(0, 220, 255), width=4)
    draw.line([(0, H // 2), (W, H // 2)], fill=(0, 220, 255), width=4)
    
    # Center badge
    bw, bh = 600, 120
    draw.rectangle([(W - bw) // 2, (H - bh) // 2, (W + bw) // 2, (H + bh) // 2], fill=(6, 10, 16), outline=(0, 240, 200), width=3)
    draw.text(((W - bw) // 2 + 50, (H - bh) // 2 + 30), "ZEROFILTER · EPISODE 2026-10-08-12", fill=(255, 255, 255))
    draw.text(((W - bw) // 2 + 50, (H - bh) // 2 + 65), "GEOPOLITICS // QUANTUM // CONSCIOUSNESS", fill=(0, 240, 200))
    
    return add_noise(thumb)

print("Rendering f01...")
render_f01().save(os.path.join(OUT_DIR, "f01.webp"), "WEBP", quality=90)
print("Rendering f02...")
render_f02().save(os.path.join(OUT_DIR, "f02.webp"), "WEBP", quality=90)
print("Rendering f03...")
render_f03().save(os.path.join(OUT_DIR, "f03.webp"), "WEBP", quality=90)
print("Rendering f04...")
render_f04().save(os.path.join(OUT_DIR, "f04.webp"), "WEBP", quality=90)
print("Rendering f05...")
render_f05().save(os.path.join(OUT_DIR, "f05.webp"), "WEBP", quality=90)
print("Rendering f06...")
render_f06().save(os.path.join(OUT_DIR, "f06.webp"), "WEBP", quality=90)
print("Rendering thumb...")
render_thumb().save(THUMB_PATH, "WEBP", quality=90)
print("All frames and thumb successfully saved!")
