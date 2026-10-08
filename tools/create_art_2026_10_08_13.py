import os
import math
import random
from PIL import Image, ImageDraw

W, H = 1376, 768
OUT_DIR = "web/art/2026-10-08-13"
THUMB_PATH = "web/thumbs/2026-10-08-13.webp"

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

def add_noise(img):
    draw = ImageDraw.Draw(img)
    for _ in range(3000):
        x = random.randint(0, W - 1)
        y = random.randint(0, H - 1)
        draw.point((x, y), fill=(random.randint(180, 255), random.randint(180, 255), random.randint(180, 255)))
    return img

def render_f01():
    # Persian Gulf tanker struck off Qatar
    img = create_base((24, 12, 8), (4, 3, 6))
    draw = ImageDraw.Draw(img)
    
    # Burning horizon & ocean
    for y in range(460, H, 10):
        draw.line([(0, y), (W, y)], fill=(int(20 + (y-460)*0.2), int(14 + (y-460)*0.1), 18), width=5)
        
    # Tanker silhouette
    hull = [(220, 520), (360, 470), (1020, 470), (1160, 510), (1100, 580), (280, 580)]
    draw.polygon(hull, fill=(18, 16, 20), outline=(80, 60, 50), width=2)
    draw.rectangle([900, 370, 1040, 470], fill=(26, 22, 28), outline=(90, 70, 60), width=2)
    
    # Impact explosion / fire glow
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([640, 360, 840, 520], fill=(255, 120, 20, 180))
    ov_draw.ellipse([680, 390, 800, 490], fill=(255, 230, 80, 220))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "PERSIAN GULF // PROJECTILE STRIKE OFF QATAR", fill=(255, 140, 40))
    draw.text((60, 90), "COMMERCIAL CHEMICAL TANKER IMPACT · STRAIT OF HORMUZ SURVEILLANCE", fill=(200, 180, 160))
    return add_noise(img)

def render_f02():
    # Ukrainian passenger bus strike / emergency response
    img = create_base((12, 14, 22), (2, 3, 8))
    draw = ImageDraw.Draw(img)
    
    # Destroyed transit canopy and wreckage
    draw.rectangle([180, 260, 1180, 310], fill=(28, 34, 45), outline=(70, 85, 110), width=2)
    for px in [250, 520, 840, 1110]:
        draw.line([(px, 310), (px, 600)], fill=(80, 95, 120), width=6)
        
    # Bus silhouettes
    draw.rectangle([340, 420, 680, 590], fill=(20, 24, 32), outline=(180, 60, 60), width=3)
    draw.rectangle([760, 430, 1080, 590], fill=(16, 20, 28), outline=(120, 40, 40), width=2)
    
    # Emergency siren light pulse
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([100, 380, 400, 680], fill=(0, 140, 255, 60))
    ov_draw.ellipse([980, 380, 1280, 680], fill=(255, 40, 40, 60))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    
    draw = ImageDraw.Draw(img)
    draw.text((60, 60), "UKRAINE MASS CASUALTY // PASSENGER BUS STRIKE", fill=(255, 80, 80))
    draw.text((60, 90), "TRANSIT TERMINAL BARRAGE · 30 CIVILIAN CASUALTIES CONFIRMED", fill=(180, 200, 220))
    return add_noise(img)

def render_f03():
    # 2026 Nobel Prize in Science: Neutrino oscillation & optogenetics
    img = create_base((8, 18, 28), (2, 4, 10))
    draw = ImageDraw.Draw(img)
    
    cx, cy = W // 2, H // 2
    # Neutrino sphere detector / Cherenkov radiation ring
    for r in [80, 160, 240, 320]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 210, 255), width=2)
        
    for angle in range(0, 360, 20):
        rad = math.radians(angle)
        x = cx + math.cos(rad) * 240
        y = cy + math.sin(rad) * 240
        draw.ellipse([x - 8, y - 8, x + 8, y + 8], fill=(255, 220, 80), outline=(255, 255, 255), width=1)
        
    draw.text((60, 60), "2026 NOBEL PRIZES // GHOST PARTICLES & NEURAL OPTOGENETICS", fill=(255, 215, 0))
    draw.text((60, 90), "NEUTRINO MASS OSCILLATION · MOLECULAR CHIRALITY · CORTICAL LIGHT SWITCHES", fill=(180, 230, 255))
    return add_noise(img)

def render_f04():
    # Quantum reading capacity bounds / optical storage
    img = create_base((16, 8, 26), (4, 2, 10))
    draw = ImageDraw.Draw(img)
    
    cx, cy = W // 2, H // 2
    # Photon number / capacity curve graph
    draw.line([(240, 580), (1140, 580)], fill=(120, 100, 160), width=2)
    draw.line([(240, 200), (240, 580)], fill=(120, 100, 160), width=2)
    
    pts = []
    for x in range(240, 1140, 10):
        norm = (x - 240) / 900
        cap = math.log(1 + norm * 8) / math.log(9) * 320
        pts.append((x, int(580 - cap)))
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=(0, 255, 200), width=3)
        
    draw.text((60, 60), "QUANTUM INFORMATION // ENERGY-CONSTRAINED READING CAPACITY", fill=(0, 240, 200))
    draw.text((60, 90), "ARXIV:2610.08945 · OPTICAL MEMORY STORAGE NUMERICAL BOUNDS", fill=(210, 180, 255))
    return add_noise(img)

def render_f05():
    # NASA Artemis II Moon Flight Trove
    img = create_base((2, 4, 12), (1, 1, 4))
    draw = ImageDraw.Draw(img)
    
    # Moon surface silhouette
    draw.ellipse([W // 2 - 380, 360, W // 2 + 380, 1120], fill=(50, 55, 65), outline=(120, 130, 145), width=2)
    # Artemis capsule trajectory loop
    capsule_x, capsule_y = W // 2 + 180, 280
    draw.ellipse([capsule_x - 12, capsule_y - 12, capsule_x + 12, capsule_y + 12], fill=(255, 255, 255), outline=(0, 180, 255), width=2)
    draw.arc([W // 2 - 440, 220, W // 2 + 440, 680], start=160, end=380, fill=(0, 200, 255), width=2)
    
    draw.text((60, 60), "DEEP SPACE TELEMETRY // NASA ARTEMIS II LUNAR DATASET", fill=(0, 200, 255))
    draw.text((60, 90), "FAR-SIDE DOSIMETRY & ORBITAL GRAVITATIONAL ANOMALIES RELEASED", fill=(200, 220, 240))
    return add_noise(img)

def render_f06():
    # Ava Vance Studio Closing / Receipts
    img = create_base((10, 16, 26), (3, 6, 12))
    draw = ImageDraw.Draw(img)
    
    for x in range(0, W, 180):
        draw.line([(x, 0), (x, H)], fill=(25, 38, 55), width=2)
    draw.polygon([(280, 520), (1096, 520), (1240, 768), (136, 768)], fill=(16, 24, 34), outline=(0, 220, 200), width=2)
    draw.rectangle([480, 560, 896, 720], fill=(8, 12, 18), outline=(60, 90, 120), width=2)
    for b in range(32):
        bx = 500 + b * 12
        bh = random.randint(15, 95)
        draw.rectangle([bx, 700 - bh, bx + 8, 700], fill=(0, 240, 180) if b < 24 else (255, 160, 40))
        
    draw.rectangle([670, 420, 706, 510], fill=(220, 170, 50), outline=(255, 230, 140), width=2)
    draw.line([(688, 510), (688, 560)], fill=(180, 180, 180), width=5)
    
    draw.text((60, 60), "ZEROFILTER BROADCAST STUDIO // AVA VANCE", fill=(0, 240, 200))
    draw.text((60, 90), "EPISODE 2026-10-08-13 · VERIFIED BROADCAST COMPLETE · STAY LUCID", fill=(200, 220, 240))
    return add_noise(img)

def render_thumb():
    f1 = render_f01().resize((W // 2, H // 2))
    f2 = render_f02().resize((W // 2, H // 2))
    f3 = render_f03().resize((W // 2, H // 2))
    f4 = render_f05().resize((W // 2, H // 2))
    
    thumb = Image.new("RGB", (W, H))
    thumb.paste(f1, (0, 0))
    thumb.paste(f2, (W // 2, 0))
    thumb.paste(f3, (0, H // 2))
    thumb.paste(f4, (W // 2, H // 2))
    
    draw = ImageDraw.Draw(thumb)
    draw.line([(W // 2, 0), (W // 2, H)], fill=(0, 220, 255), width=4)
    draw.line([(0, H // 2), (W, H // 2)], fill=(0, 220, 255), width=4)
    
    bw, bh = 600, 120
    draw.rectangle([(W - bw) // 2, (H - bh) // 2, (W + bw) // 2, (H + bh) // 2], fill=(6, 10, 16), outline=(0, 240, 200), width=3)
    draw.text(((W - bw) // 2 + 50, (H - bh) // 2 + 30), "ZEROFILTER · EPISODE 2026-10-08-13", fill=(255, 255, 255))
    draw.text(((W - bw) // 2 + 50, (H - bh) // 2 + 65), "GULF TANKER // 2026 NOBEL // ARTEMIS II", fill=(0, 240, 200))
    return add_noise(thumb)

print("Saving f01..f06 and thumb...")
render_f01().save(os.path.join(OUT_DIR, "f01.webp"), "WEBP", quality=90)
render_f02().save(os.path.join(OUT_DIR, "f02.webp"), "WEBP", quality=90)
render_f03().save(os.path.join(OUT_DIR, "f03.webp"), "WEBP", quality=90)
render_f04().save(os.path.join(OUT_DIR, "f04.webp"), "WEBP", quality=90)
render_f05().save(os.path.join(OUT_DIR, "f05.webp"), "WEBP", quality=90)
render_f06().save(os.path.join(OUT_DIR, "f06.webp"), "WEBP", quality=90)
render_thumb().save(THUMB_PATH, "WEBP", quality=90)
print("Art generation complete!")
