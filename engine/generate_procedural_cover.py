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

    if theme in ("geopolitics", "red_sea"):
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

    elif theme in ("conscious_agents", "hoffman"):
        # Donald Hoffman Conscious Agent Network & Mathematical Spacetime Emergence
        # 1. Perspective spacetime grid projection (emerging from below)
        horizon_y = cy + 40
        for gx in range(0, width + 100, 40):
            # Perspective rays radiating from vanishing point (cx, horizon_y)
            draw.line([(cx, horizon_y), (gx, height)], fill=(20, 50, 70), width=1)
        for gy in range(horizon_y, height, 15):
            factor = (gy - horizon_y) / (height - horizon_y)
            alpha_b = int(25 + 70 * factor)
            draw.line([(0, gy), (width, gy)], fill=(15, alpha_b, int(alpha_b * 1.4)), width=1)

        # 2. Markovian Conscious Agent Network (Constellation of connected nodes)
        random.seed(42)
        agent_nodes = []
        for a_idx in range(18):
            ax = random.randint(140, width - 140)
            ay = random.randint(70, horizon_y - 20)
            agent_nodes.append((ax, ay, random.randint(12, 28)))

        # Transition kernel connections between agents
        for i, (ax1, ay1, r1) in enumerate(agent_nodes):
            for j, (ax2, ay2, r2) in enumerate(agent_nodes):
                if i < j:
                    dist = math.hypot(ax1 - ax2, ay1 - ay2)
                    if dist < 260:
                        # Arc intensity inversely proportional to distance
                        p_intensity = int(180 * (1.0 - dist / 260.0))
                        draw.line([(ax1, ay1), (ax2, ay2)], fill=(int(p_intensity * 0.4), p_intensity, int(p_intensity * 0.8)), width=1)
                        # Probability weight label on mid-point
                        if dist < 140 and (i + j) % 3 == 0:
                            mx, my = (ax1 + ax2) // 2, (ay1 + ay2) // 2
                            draw.text((mx + 2, my - 6), f"P_{i}{j}={dist/300:.2f}", fill=(p_intensity, 255, 200))

        # Agent node rendering (glowing spheres with core and ring)
        for idx, (ax, ay, rad) in enumerate(agent_nodes):
            # Outer aura ring
            draw.ellipse([ax - rad - 6, ay - rad - 6, ax + rad + 6, ay + rad + 6], outline=(30, 160, 220), width=1)
            # Core circle
            draw.ellipse([ax - rad, ay - rad, ax + rad, ay + rad], fill=(10, 45, 75), outline=(0, 240, 255), width=2)
            # Center nexus
            draw.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=(255, 255, 255))
            draw.text((ax + rad + 4, ay - 8), f"AGENT α_{idx}", fill=(0, 255, 220))

        # 3. Asymptotic projection cone from network to spacetime plane
        for (ax, ay, _) in agent_nodes[::4]:
            draw.line([(ax, ay), (cx + (ax - cx) * 1.3, height - 30)], fill=(0, 180, 240), width=1)

    elif theme in ("holographic", "scrambler"):
        # Holographic Principle & Hayden-Preskill Quantum Information Scrambler
        # 1. Gravitational lensing accretion ring & event horizon
        for r in range(280, 40, -8):
            factor = (280 - r) / 240.0
            color_int = int(255 * factor)
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(int(color_int * 0.9), int(color_int * 0.6), 255), width=2)

        # 2. Black hole central singularity (pure darkness absorbing index)
        draw.ellipse([cx - 50, cy - 50, cx + 50, cy + 50], fill=(0, 0, 0), outline=(180, 100, 255), width=3)

        # 3. Holographic boundary scrambling matrix (radial quantum entanglement cords)
        random.seed(88)
        for deg in range(0, 360, 6):
            rad = math.radians(deg)
            inner_r = 55
            outer_r = 420 + random.randint(-20, 40)
            x1 = cx + int(math.cos(rad) * inner_r)
            y1 = cy + int(math.sin(rad) * inner_r)
            x2 = cx + int(math.cos(rad) * outer_r)
            y2 = cy + int(math.sin(rad) * outer_r)
            beam_col = (random.randint(60, 160), random.randint(180, 255), random.randint(220, 255))
            draw.line([(x1, y1), (x2, y2)], fill=beam_col, width=1)
            if deg % 24 == 0:
                draw.text((x2 - 15, y2 - 6), f"ψ_{deg}°", fill=(100, 255, 240))

        # 4. Hawking radiation photon emission scatter
        for _ in range(45):
            angle = random.uniform(0, 2 * math.pi)
            dist = random.uniform(80, 500)
            px = cx + int(math.cos(angle) * dist)
            py = cy + int(math.sin(angle) * dist)
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 240, 120), outline=(255, 255, 255))

    elif theme in ("orbital_qkd", "space_sigint"):
        # Orbital QKD Downlinks & Space-Based SIGINT Laser Architecture
        # 1. Earth limb curved horizon (large arc at bottom)
        earth_cy = height + 400
        earth_r = 750
        draw.ellipse([cx - earth_r, earth_cy - earth_r, cx + earth_r, earth_cy + earth_r], fill=(4, 18, 30), outline=(0, 160, 220), width=2)
        # Atmospheric glow layer
        for dr in range(2, 28, 4):
            alpha_atm = int(120 * (1.0 - dr / 28.0))
            draw.ellipse([cx - (earth_r + dr), earth_cy - (earth_r + dr), cx + (earth_r + dr), earth_cy + (earth_r + dr)], outline=(0, alpha_atm, int(alpha_atm * 1.5)), width=2)

        # 2. Orbital altitude tracks & constellation planes
        for alt in [160, 240, 320]:
            draw.arc([cx - (earth_r + alt), earth_cy - (earth_r + alt), cx + (earth_r + alt), earth_cy + (earth_r + alt)], start=210, end=330, fill=(15, 60, 90), width=1)

        # 3. Satellites and laser downlink conduits
        sats = [
            (cx - 380, 140, "QKD-SAT #01 [LEO 510km]"),
            (cx, 90, "QKD-SAT #02 [PRIMARY BEACON]"),
            (cx + 360, 150, "SIGINT-RELAY #03 [MOLNIYA-O]")
        ]
        ground_stations = [
            (cx - 240, height - 70, "GS-NORD [67.8°N]"),
            (cx + 180, height - 85, "GS-MID [38.2°N]")
        ]

        # Draw laser downlinks (pencil-thin beams with glow)
        for sx, sy, _ in sats:
            for gx, gy, _ in ground_stations:
                if abs(sx - gx) < 450:
                    draw.line([(sx, sy), (gx, gy)], fill=(0, 255, 200), width=2)
                    draw.line([(sx - 1, sy), (gx - 1, gy)], fill=(0, 120, 255), width=1)
                    draw.line([(sx + 1, sy), (gx + 1, gy)], fill=(0, 120, 255), width=1)
                    # Mid-path atmospheric decoherence scintillation blips
                    for step in range(3, 8):
                        mx = sx + (gx - sx) * (step / 8.0)
                        my = sy + (gy - sy) * (step / 8.0)
                        if my > height - 180:
                            draw.ellipse([mx - 3, my - 3, mx + 3, my + 3], outline=(255, 120, 50), width=1)

        # Render Satellites (body + solar panels)
        for sx, sy, label in sats:
            # Solar panels
            draw.rectangle([sx - 24, sy - 4, sx - 8, sy + 4], fill=(0, 120, 200), outline=(0, 220, 255))
            draw.rectangle([sx + 8, sy - 4, sx + 24, sy + 4], fill=(0, 120, 200), outline=(0, 220, 255))
            # Bus
            draw.rectangle([sx - 7, sy - 7, sx + 7, sy + 7], fill=(240, 240, 255), outline=(0, 255, 220), width=2)
            draw.text((sx - 60, sy - 24), label, fill=(0, 255, 240))

        # Render Ground Station radomes
        for gx, gy, label in ground_stations:
            draw.ellipse([gx - 12, gy - 12, gx + 12, gy + 12], fill=(20, 80, 120), outline=(0, 255, 200), width=2)
            draw.text((gx - 40, gy + 14), label, fill=(0, 220, 255))

    elif theme in ("casimir", "vacuum_thruster"):
        # Dynamic Casimir Effect & Quantum Vacuum Propulsion Architecture
        # 1. Background vacuum zero-point fluctuation field
        random.seed(99)
        for _ in range(120):
            fx = random.randint(40, width - 40)
            fy = random.randint(40, height - 40)
            # Virtual particle-antiparticle pair
            offset = random.randint(4, 12)
            draw.point((fx, fy), fill=(0, 255, 220))
            draw.point((fx + offset, fy), fill=(255, 100, 120))
            draw.arc([fx, fy - offset // 2, fx + offset, fy + offset // 2], start=0, end=180, fill=(40, 120, 180), width=1)

        # 2. Parallel Casimir Conducting Nanocavity Plates
        plate_w = 40
        plate_h = 380
        gap = 140
        p1_x = cx - gap // 2 - plate_w
        p2_x = cx + gap // 2
        p_y = cy - plate_h // 2

        # Left plate (Conductive mirror 1)
        draw.rectangle([p1_x, p_y, p1_x + plate_w, p_y + plate_h], fill=(12, 40, 65), outline=(0, 240, 255), width=2)
        # Right plate (Conductive mirror 2)
        draw.rectangle([p2_x, p_y, p2_x + plate_w, p_y + plate_h], fill=(12, 40, 65), outline=(0, 240, 255), width=2)

        # Plate texture / nanoscale gratings
        for gy in range(p_y + 10, p_y + plate_h - 10, 15):
            draw.line([(p1_x + 4, gy), (p1_x + plate_w - 4, gy)], fill=(0, 180, 220), width=1)
            draw.line([(p2_x + 4, gy), (p2_x + plate_w - 4, gy)], fill=(0, 180, 220), width=1)

        # 3. Suppressed standing waves inside gap (only allowed modes fit)
        for wy in range(p_y + 20, p_y + plate_h - 20, 40):
            pts = []
            for wx in range(p1_x + plate_w, p2_x, 4):
                rel_x = (wx - (p1_x + plate_w)) / float(gap)
                amp = math.sin(rel_x * math.pi) * 14.0
                pts.append((wx, wy + amp))
            if len(pts) > 1:
                draw.line(pts, fill=(0, 255, 240), width=2)

        # 4. External vacuum radiation pressure vectors (arrows pushing inward)
        for ay in range(p_y + 30, p_y + plate_h - 30, 45):
            # Left push
            draw.line([(p1_x - 60, ay), (p1_x - 8, ay)], fill=(255, 140, 50), width=2)
            draw.line([(p1_x - 8, ay), (p1_x - 18, ay - 6)], fill=(255, 140, 50), width=2)
            draw.line([(p1_x - 8, ay), (p1_x - 18, ay + 6)], fill=(255, 140, 50), width=2)
            # Right push
            draw.line([(p2_x + plate_w + 60, ay), (p2_x + plate_w + 8, ay)], fill=(255, 140, 50), width=2)
            draw.line([(p2_x + plate_w + 8, ay), (p2_x + plate_w + 18, ay - 6)], fill=(255, 140, 50), width=2)
            draw.line([(p2_x + plate_w + 8, ay), (p2_x + plate_w + 18, ay + 6)], fill=(255, 140, 50), width=2)

        # 5. Asymmetric dynamic photon exhaust cone (propulsion vector exiting upward)
        for off in range(-35, 36, 10):
            draw.line([(cx + off, p_y), (cx + off * 2.5, p_y - 120)], fill=(255, 200, 60), width=2)
        draw.text((cx - 70, p_y - 145), "CASIMIR THRUST VECTOR [F_vac]", fill=(255, 220, 80))
        draw.text((cx - 50, cy + plate_h // 2 + 15), "NANOCAVITY d = 82 nm", fill=(0, 255, 220))

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
    elif theme == "red_sea":
        draw.text((40, 60), "RED SEA MARITIME STRIKE // BAB EL-MANDEB ASW CORRIDOR // COORD: 12.5°N, 43.3°E", fill=(255, 140, 40))
    elif theme == "quantum":
        draw.text((40, 60), "QKD SATELLITE TELEMETRY // FREE-SPACE ENTANGLEMENT FIDELITY 99.4% // 1550nm DOWNLINK", fill=(0, 240, 255))
    elif theme == "bec":
        draw.text((40, 60), "BEC MICROGRAVITY ATOM INTERFEROMETRY // RUBIDIUM-87 CONDENSATE // TEMP: 50 PICOKELVIN", fill=(120, 220, 255))
    elif theme == "corruption":
        draw.text((40, 60), "DEFENSE PROCUREMENT FORENSICS // AUDIT TRAIL: COST-PLUS CARTELS // UNREDACTED", fill=(255, 90, 70))
    elif theme == "vc_theft":
        draw.text((40, 60), "DEFENSE VC FORENSICS // DUAL-USE TECH DIVERSION // DIRECTORATE T INTERCEPT", fill=(255, 120, 50))
    elif theme in ("casimir", "vacuum_thruster"):
        draw.text((40, 60), "DYNAMIC CASIMIR NANOCAVITY // ZERO-POINT VACUUM FLUCTUATION PRESSURE // ASYMMETRIC REACTION", fill=(255, 200, 60))
    elif theme in ("orbital_qkd", "space_sigint"):
        draw.text((40, 60), "ORBITAL QKD DOWNLINK // 1550nm ADAPTIVE OPTICS // 500KM LEO TRACK // GROUND SIGINT CONDUIT", fill=(0, 255, 200))
    elif theme in ("holographic", "scrambler"):
        draw.text((40, 60), "HAYDEN-PRESKILL QUANTUM SCRAMBLING // EVENT HORIZON HAWKING EMISSION // ADS/CFT HORIZON", fill=(200, 160, 255))
    elif theme in ("conscious_agents", "hoffman"):
        draw.text((40, 60), "CONSCIOUS AGENT DYNAMICS // MARKOVIAN TRANSITION KERNELS // SPACETIME PROJECTION MATRIX", fill=(0, 255, 220))
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
