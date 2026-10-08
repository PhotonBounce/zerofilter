import os
import math
import random
from PIL import Image, ImageDraw

W, H = 1376, 768
OUT_DIR = "web/art/2026-10-08-14"
THUMB_PATH = "web/thumbs/2026-10-08-14.webp"

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
    # Downed Russian drone with Polish SIM card / forensic workbench
    img = create_base((10, 16, 26), (2, 4, 8))
    draw = ImageDraw.Draw(img)
    
    # Forensic inspection table grid
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill=(20, 30, 45), width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill=(20, 30, 45), width=1)
        
    # Drone fuselage wreckage
    draw.polygon([(260, 480), (450, 340), (880, 350), (1050, 520), (750, 620), (380, 600)], fill=(22, 28, 38), outline=(80, 100, 130), width=2)
    # Circuit board bay
    draw.rectangle([520, 390, 780, 510], fill=(12, 40, 24), outline=(40, 140, 80), width=2)
    # Magnified Polish SIM card slot
    draw.rectangle([600, 420, 700, 480], fill=(210, 40, 40), outline=(255, 230, 230), width=2)
    draw.rectangle([615, 430, 660, 470], fill=(230, 190, 50), outline=(255, 255, 255), width=1)
    
    # Forensic callouts
    draw.line([(700, 450), (950, 320)], fill=(0, 220, 255), width=2)
    draw.rectangle([950, 280, 1260, 360], fill=(6, 14, 24), outline=(0, 220, 255), width=2)
    draw.text((965, 295), "HARDWARE FORENSICS // POLAND", fill=(255, 80, 80))
    draw.text((965, 325), "DOMESTIC GSM/LTE SIM DETECTED", fill=(0, 240, 200))
    
    draw.text((60, 60), "NATO BORDER SECURITY // DOWNED DRONE INSPECTION", fill=(0, 220, 255))
    draw.text((60, 90), "POLISH TELECOM CARDS RECOVERED INSIDE RUSSIAN RECON AIRFRAME", fill=(180, 200, 220))
    return add_noise(img)

def render_f02():
    # Operation Vivaldi: Ground combat robot & FPV drone in Donetsk
    img = create_base((18, 14, 10), (4, 3, 2))
    draw = ImageDraw.Draw(img)
    
    # Battlefield trench landscape
    draw.polygon([(0, 500), (W, 460), (W, 768), (0, 768)], fill=(32, 26, 20), outline=(60, 50, 40), width=2)
    draw.polygon([(180, 550), (450, 510), (780, 580), (1200, 530), (1050, 768), (300, 768)], fill=(18, 14, 10))
    
    # Ground robotic combat vehicle (UGV)
    draw.rectangle([380, 470, 640, 560], fill=(25, 32, 28), outline=(60, 85, 70), width=3)
    # Heavy tracks
    draw.rectangle([360, 530, 660, 580], fill=(12, 14, 14), outline=(90, 100, 90), width=2)
    # Remote weapon turret / machine gun
    draw.rectangle([480, 420, 560, 470], fill=(30, 38, 34), outline=(80, 105, 90), width=2)
    draw.line([(560, 440), (680, 435)], fill=(120, 140, 130), width=5)
    
    # FPV drone flying overhead with glowing rotors
    dx, dy = 880, 260
    draw.ellipse([dx - 30, dy - 10, dx + 30, dy + 10], fill=(20, 25, 30), outline=(0, 240, 200), width=2)
    draw.line([(dx - 45, dy - 20), (dx + 45, dy + 20)], fill=(0, 240, 255), width=2)
    draw.line([(dx - 45, dy + 20), (dx + 45, dy - 20)], fill=(0, 240, 255), width=2)
    
    draw.text((60, 60), "OPERATION VIVALDI // DONETSK OBLAST COUNTER-OFFENSIVE", fill=(0, 240, 200))
    draw.text((60, 90), "AUTONOMOUS COMBAT ROBOTICS & FPV SWARMS BREACH TRENCH FORTS", fill=(220, 200, 180))
    return add_noise(img)

def render_f03():
    # Route-Verify-Vote reasoning architecture
    img = create_base((8, 12, 26), (2, 4, 10))
    draw = ImageDraw.Draw(img)
    
    cx, cy = W // 2, H // 2
    # Network flowchart nodes: Route -> Verify -> Vote
    nodes = [
        (cx - 360, cy, "INPUT TRACE", (0, 180, 255)),
        (cx - 120, cy - 90, "SYMBOLIC ROUTE", (255, 180, 40)),
        (cx - 120, cy + 90, "EMPIRICAL ROUTE", (255, 180, 40)),
        (cx + 140, cy, "VERIFIER GATE", (0, 240, 180)),
        (cx + 380, cy, "CONSISTENCY VOTE", (255, 90, 140))
    ]
    
    # Draw connections
    draw.line([(cx - 360, cy), (cx - 120, cy - 90)], fill=(80, 110, 160), width=3)
    draw.line([(cx - 360, cy), (cx - 120, cy + 90)], fill=(80, 110, 160), width=3)
    draw.line([(cx - 120, cy - 90), (cx + 140, cy)], fill=(0, 240, 180), width=3)
    draw.line([(cx - 120, cy + 90), (cx + 140, cy)], fill=(0, 240, 180), width=3)
    draw.line([(cx + 140, cy), (cx + 380, cy)], fill=(255, 90, 140), width=4)
    
    for nx, ny, label, color in nodes:
        draw.rectangle([nx - 95, ny - 35, nx + 95, ny + 35], fill=(12, 18, 30), outline=color, width=2)
        draw.text((nx - 75, ny - 10), label, fill=color)
        
    draw.text((60, 60), "FRONTIER COMPUTE // ROUTE-VERIFY-VOTE REASONING", fill=(0, 220, 255))
    draw.text((60, 90), "ARXIV:2610.08814 · PROCEDURE-CONDITIONED SELF-CONSISTENCY", fill=(200, 180, 240))
    return add_noise(img)

def render_f04():
    # Arctic permafrost woody geotextile blanket
    img = create_base((12, 20, 22), (3, 6, 8))
    draw = ImageDraw.Draw(img)
    
    # Arctic permafrost terrain
    draw.polygon([(0, 420), (W, 390), (W, 768), (0, 768)], fill=(34, 40, 44), outline=(60, 75, 85), width=2)
    
    # Geotextile woody insulation grid
    for x in range(120, 1260, 60):
        draw.line([(x, 430), (x - 60, 720)], fill=(180, 140, 90), width=2)
        draw.line([(x - 60, 430), (x, 720)], fill=(180, 140, 90), width=2)
    draw.polygon([(120, 430), (1200, 400), (1140, 720), (60, 720)], fill=(140, 105, 65, 100), outline=(210, 170, 110), width=3)
    
    # Thermal temperature gradient HUD
    draw.line([(60, 220), (460, 220)], fill=(0, 200, 255), width=4)
    draw.text((60, 195), "THERMAL INSULATION BARRIER · -8.4°C CORE STABILIZATION", fill=(0, 220, 255))
    
    draw.text((60, 60), "PLANETARY ENGINEERING // PERMAFROST INSULATION BLANKETS", fill=(220, 170, 90))
    draw.text((60, 90), "NATURE REPORT · MITIGATING ARCTIC METHANE FEEDBACK LOOPS", fill=(180, 220, 240))
    return add_noise(img)

def render_f05():
    # Primate visual cortex food reactivation in REM sleep
    img = create_base((18, 6, 16), (4, 1, 4))
    draw = ImageDraw.Draw(img)
    
    cx, cy = W // 2, H // 2
    # Primate brain silhouette & visual cortex highlight
    draw.ellipse([cx - 320, cy - 180, cx + 320, cy + 180], fill=(22, 10, 18), outline=(120, 40, 90), width=2)
    # High-level visual cortex area glowing
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([cx + 90, cy - 80, cx + 280, cy + 100], fill=(255, 60, 120, 90))
    ov_draw.ellipse([cx + 130, cy - 40, cx + 240, cy + 60], fill=(255, 200, 60, 140))
    img.paste(Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"))
    
    draw = ImageDraw.Draw(img)
    # EEG theta / REM wave pattern
    prev = (180, 560)
    for x in range(180, 1200, 8):
        y = 560 + int(math.sin(x * 0.06) * 24 + math.cos(x * 0.18) * 10)
        draw.line([prev, (x, y)], fill=(255, 90, 160), width=2)
        prev = (x, y)
        
    draw.text((60, 60), "CONSCIOUSNESS DESK // NEURAL REPLAY DURING REM SLEEP", fill=(255, 100, 160))
    draw.text((60, 90), "BIORXIV · REACTIVATION OF REWARD FOOD STIMULI IN HIGH-LEVEL VISUAL CORTEX", fill=(230, 190, 210))
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
    draw.text((60, 90), "EPISODE 2026-10-08-14 · VERIFIED BROADCAST COMPLETE · STAY LUCID", fill=(200, 220, 240))
    return add_noise(img)

def render_thumb():
    f1 = render_f01().resize((W // 2, H // 2))
    f2 = render_f02().resize((W // 2, H // 2))
    f3 = render_f03().resize((W // 2, H // 2))
    f4 = render_f04().resize((W // 2, H // 2))
    
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
    draw.text(((W - bw) // 2 + 50, (H - bh) // 2 + 30), "ZEROFILTER · EPISODE 2026-10-08-14", fill=(255, 255, 255))
    draw.text(((W - bw) // 2 + 50, (H - bh) // 2 + 65), "POLISH SIMS // OP VIVALDI // REM DREAMS", fill=(0, 240, 200))
    return add_noise(thumb)

print("Saving f01..f06 and thumb...")
render_f01().save(os.path.join(OUT_DIR, "f01.webp"), "WEBP", quality=90)
render_f02().save(os.path.join(OUT_DIR, "f02.webp"), "WEBP", quality=90)
render_f03().save(os.path.join(OUT_DIR, "f03.webp"), "WEBP", quality=90)
render_f04().save(os.path.join(OUT_DIR, "f04.webp"), "WEBP", quality=90)
render_f05().save(os.path.join(OUT_DIR, "f05.webp"), "WEBP", quality=90)
render_f06().save(os.path.join(OUT_DIR, "f06.webp"), "WEBP", quality=90)
render_thumb().save(THUMB_PATH, "WEBP", quality=90)
print("Art generation complete for 14:00!")
