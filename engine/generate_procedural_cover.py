# engine/generate_procedural_cover.py
"""
Procedural Offline Cover Generator for ZeroFilter Pipeline.
Fallback engine when external cloud image generation APIs hit rate limits or 429 quotas.
Generates high-definition (1280x720) cyber-noir scientific broadcast visuals:
- Multi-frequency quantum wave interference fields
- Nanoscale lattice / microtubule matrix representations
- CRT scanlines, chromatic aberration & phosphor blooms
- Classified intelligence heads-up telemetry HUD overlays
"""

import math
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_quantum_field(width=1280, height=720, theme="consciousness"):
    im = Image.new("RGB", (width, height), (8, 12, 18))
    draw = ImageDraw.Draw(im)

    # 1. Background radial gradient & ambient glow
    cx, cy = width // 2, height // 2
    for r in range(max(width, height), 0, -16):
        intensity = int(35 * (1.0 - r / max(width, height)))
        color = (intensity // 2, intensity, int(intensity * 1.5))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=8)

    # 2. Procedural quantum interference / microtubule lattice waves
    for y in range(0, height, 4):
        points = []
        for x in range(0, width, 10):
            # Interference of two spatial frequencies
            w1 = math.sin(x * 0.015 + y * 0.02)
            w2 = math.cos(x * 0.008 - y * 0.01)
            w3 = math.sin((x + y) * 0.005)
            dy = (w1 + w2 + w3) * 18.0
            points.append((x, y + dy))
        
        # Color gradient based on depth/position
        alpha = int(90 + 80 * math.sin(y * 0.01))
        line_color = (
            int(15 + 20 * math.sin(y * 0.02)),
            int(120 + 80 * math.cos(y * 0.015)),
            int(180 + 70 * math.sin(y * 0.01))
        )
        if len(points) > 1:
            draw.line(points, fill=line_color, width=1)

    # 3. Microtubule hexagonal / lattice nodes if theme == consciousness
    random.seed(42)
    for _ in range(45):
        nx = random.randint(150, width - 150)
        ny = random.randint(100, height - 100)
        nr = random.randint(4, 18)
        draw.ellipse([nx - nr, ny - nr, nx + nr, ny + nr], outline=(0, 240, 255), width=2)
        draw.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=(255, 255, 255))
        # Connect nearby nodes
        if random.random() > 0.4:
            draw.line([(nx, ny), (nx + random.randint(-80, 80), ny + random.randint(-60, 60))], fill=(0, 180, 220), width=1)

    # 4. Blur pass for bloom & atmosphere
    bloom = im.filter(ImageFilter.GaussianBlur(radius=3))
    im = Image.blend(im, bloom, 0.35)
    draw = ImageDraw.Draw(im)

    # 5. Cyber-noir CRT scanlines
    for y in range(0, height, 3):
        draw.line([(0, y), (width, y)], fill=(0, 0, 0), width=1)

    # 6. HUD / Telemetry Overlays
    # Border & crosshairs
    draw.rectangle([20, 20, width - 20, height - 20], outline=(0, 220, 240), width=1)
    draw.rectangle([24, 24, width - 24, height - 24], outline=(0, 100, 120), width=1)
    
    # Corner brackets
    c_len = 30
    for cx_c, cy_c in [(20, 20), (width - 20, 20), (20, height - 20), (width - 20, height - 20)]:
        sx = 1 if cx_c == 20 else -1
        sy = 1 if cy_c == 20 else -1
        draw.line([(cx_c, cy_c), (cx_c + sx * c_len, cy_c)], fill=(0, 255, 240), width=3)
        draw.line([(cx_c, cy_c), (cx_c, cy_c + sy * c_len)], fill=(0, 255, 240), width=3)

    # Status text overlay
    draw.text((40, 40), "[CLASSIFIED INTEL // ZEROFILTER BROADCAST TELEMETRY]", fill=(0, 255, 240))
    draw.text((40, 60), "ORCH-OR QUANTUM MICROTUBULE RESONANCE // SIGINT FREQ: 432.8 MHz", fill=(0, 180, 200))
    draw.text((40, height - 60), "SYS: FALLBACK PROCEDURAL GENERATOR // RESTRAINT LEVEL: UNREDACTED", fill=(0, 255, 200))
    draw.text((width - 320, height - 60), "HOST: REX VANCE // 24/7 AUTOPILOT", fill=(0, 220, 255))

    return im

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "procedural_test.webp"
    theme = sys.argv[2] if len(sys.argv) > 2 else "consciousness"
    img = generate_quantum_field(theme=theme)
    img.save(out_path, "WEBP", quality=92)
    print(f"[+] Successfully generated procedural cover: {out_path}")
