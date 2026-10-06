# engine/generate_procedural_cover.py
"""
Procedural Offline Cover Generator for ZeroFilter Pipeline.
Fallback engine when external cloud image generation APIs hit rate limits or 429 quotas.
Generates high-definition (1280x720) cyber-noir scientific broadcast visuals:
- Themes: 'quantum', 'consciousness', 'geopolitics', 'corruption'
- Multi-frequency quantum wave interference fields or radar/sonar vector grids
- CRT scanlines, chromatic aberration & phosphor blooms
- Classified intelligence heads-up telemetry HUD overlays
"""

import math
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_cover(width=1280, height=720, theme="geopolitics", title=""):
    im = Image.new("RGB", (width, height), (6, 10, 16))
    draw = ImageDraw.Draw(im)

    cx, cy = width // 2, height // 2

    if theme == "geopolitics":
        # Amber/Cyan Radar & Maritime Electronic Warfare Sweep
        # 1. Concentric radar range rings
        for r in range(60, max(width, height), 70):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(15, 60, 80), width=1)
            # Distance tick markers
            draw.text((cx + r - 35, cy + 4), f"{r*2}NM", fill=(20, 90, 110))

        # 2. Polar radar grid spokes
        for deg in range(0, 360, 30):
            rad = math.radians(deg)
            ex = cx + int(math.cos(rad) * max(width, height))
            ey = cy + int(math.sin(rad) * max(width, height))
            draw.line([(cx, cy), (ex, ey)], fill=(12, 45, 60), width=1)

        # 3. Radar sweep cone glow
        sweep_angle = 125
        for offset in range(35):
            rad = math.radians(sweep_angle - offset)
            alpha_int = int(80 * (1.0 - offset / 35.0))
            ex = cx + int(math.cos(rad) * 600)
            ey = cy + int(math.sin(rad) * 600)
            draw.line([(cx, cy), (ex, ey)], fill=(int(alpha_int * 0.2), alpha_int, int(alpha_int * 1.2)), width=3)

        # 4. Maritime track vectors & spoofing anomaly targets
        random.seed(105)
        for i in range(28):
            tx = random.randint(120, width - 120)
            ty = random.randint(80, height - 80)
            # Hostile / Shadow fleet tanker (Amber/Orange) vs Friendly (Cyan)
            is_shadow = (i % 3 == 0)
            col = (255, 140, 40) if is_shadow else (0, 220, 240)
            
            # Target blip
            draw.rectangle([tx - 4, ty - 4, tx + 4, ty + 4], outline=col, width=1)
            draw.point((tx, ty), fill=(255, 255, 255))
            
            # Heading vector line
            angle = random.uniform(0, 2 * math.pi)
            v_len = random.randint(20, 50)
            vx = tx + int(math.cos(angle) * v_len)
            vy = ty + int(math.sin(angle) * v_len)
            draw.line([(tx, ty), (vx, vy)], fill=col, width=1)
            
            # AIS metadata callout
            tag = f"SPOOF-AIS #{8400+i}" if is_shadow else f"TRK-{100+i}"
            draw.text((tx + 8, ty - 8), tag, fill=col)

        # 5. GPS EW Jamming distortion zone (wavy interference)
        for jx in range(250, 550, 6):
            for jy in range(150, 400, 6):
                dist = math.hypot(jx - 400, jy - 275)
                if dist < 120:
                    draw.point((jx + int(math.sin(jy*0.2)*4), jy), fill=(240, 70, 40))

    else:
        # Quantum / Consciousness wave field
        for r in range(max(width, height), 0, -16):
            intensity = int(35 * (1.0 - r / max(width, height)))
            color = (intensity // 2, intensity, int(intensity * 1.5))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=8)

        for y in range(0, height, 4):
            points = []
            for x in range(0, width, 10):
                w1 = math.sin(x * 0.015 + y * 0.02)
                w2 = math.cos(x * 0.008 - y * 0.01)
                dy = (w1 + w2) * 16.0
                points.append((x, y + dy))
            line_color = (int(15 + 20 * math.sin(y * 0.02)), int(120 + 80 * math.cos(y * 0.015)), int(180 + 70 * math.sin(y * 0.01)))
            if len(points) > 1:
                draw.line(points, fill=line_color, width=1)

    # Ambient bloom filter
    bloom = im.filter(ImageFilter.GaussianBlur(radius=3))
    im = Image.blend(im, bloom, 0.3)
    draw = ImageDraw.Draw(im)

    # Cyber-noir CRT scanlines
    for y in range(0, height, 3):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=1)

    # Frame border & corner brackets
    draw.rectangle([20, 20, width - 20, height - 20], outline=(0, 220, 240), width=1)
    draw.rectangle([24, 24, width - 24, height - 24], outline=(0, 90, 110), width=1)
    
    c_len = 30
    for cx_c, cy_c in [(20, 20), (width - 20, 20), (20, height - 20), (width - 20, height - 20)]:
        sx = 1 if cx_c == 20 else -1
        sy = 1 if cy_c == 20 else -1
        draw.line([(cx_c, cy_c), (cx_c + sx * c_len, cy_c)], fill=(0, 255, 240), width=3)
        draw.line([(cx_c, cy_c), (cx_c, cy_c + sy * c_len)], fill=(0, 255, 240), width=3)

    # Classified Telemetry Overlay
    draw.text((40, 40), "[CLASSIFIED INTEL // ZEROFILTER BROADCAST TELEMETRY]", fill=(0, 255, 240))
    if theme == "geopolitics":
        draw.text((40, 60), "BALTIC THEATER SIGINT // EW GPS SPOOFING CORRIDOR // COORD: 55.4°N, 19.8°E", fill=(255, 160, 50))
    elif theme == "quantum":
        draw.text((40, 60), "QKD SATELLITE TELEMETRY // FREE-SPACE ENTANGLEMENT FIDELITY 99.4% // 1550nm DOWNLINK", fill=(0, 240, 255))
    elif theme == "corruption":
        draw.text((40, 60), "DEFENSE PROCUREMENT FORENSICS // AUDIT TRAIL: COST-PLUS CARTELS // UNREDACTED", fill=(255, 90, 70))
    elif theme == "consciousness":
        draw.text((40, 60), "NEURAL BIOPHOTON TELEMETRY // TUBULIN DIPOLE HARMONICS // BANDWIDTH 614 THz", fill=(80, 255, 180))
    else:
        draw.text((40, 60), "QUANTUM SPECTROMETRY // RESONANCE SPECTRUM 432.8 MHz", fill=(0, 180, 200))
        
    draw.text((40, height - 60), "SYS: FALLBACK PROCEDURAL GENERATOR // RESTRAINT LEVEL: UNREDACTED", fill=(0, 255, 200))
    draw.text((width - 340, height - 60), "HOST: REX VANCE // 24/7 AUTOPILOT", fill=(0, 220, 255))

    return im

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "procedural_test.webp"
    theme = sys.argv[2] if len(sys.argv) > 2 else "geopolitics"
    img = generate_cover(theme=theme)
    img.save(out_path, "WEBP", quality=92)
    print(f"[+] Successfully generated procedural cover: {out_path} ({theme})")
