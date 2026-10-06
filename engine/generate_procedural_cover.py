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

    if theme in ("geopolitics", "red_sea", "asbm", "anti_ship_missile", "red_sea_missile", "hormuz_spoofing", "hormuz_ew", "iran_drone", "hormuz_hydrophone", "persian_gulf", "taiwan_sosus", "hydrophone_barrier", "taiwan_strait", "barents_bastion", "giuk_gap", "malacca_blockade", "hydrophone_gate", "kuril_bastion", "okhotsk_bastion", "kuril_islands", "sea_of_okhotsk"):
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

    elif theme in ("suwalki_gap", "suwalki_corridor", "kaliningrad_ew", "kaliningrad_corridor", "rail_gauge"):
        # Suwalki Gap Heavy Armor Transit Bottleneck & Rail Gauge Discrepancy
        # 1. Geographic Sector Partition (Kaliningrad West, Belarus East, Poland South, Lithuania North)
        # Tactical grid background
        for gy in range(80, height - 80, 30):
            draw.line([(60, gy), (width - 60, gy)], fill=(12, 24, 36), width=1)
        for gx in range(60, width - 60, 40):
            draw.line([(gx, 80), (gx, height - 80)], fill=(12, 24, 36), width=1)

        # Kaliningrad Oblast Zone (Left, Red/Orange tint)
        draw.rectangle([60, cy - 140, cx - 180, cy + 140], fill=(24, 14, 16), outline=(255, 80, 60), width=2)
        draw.text((70, cy - 130), "[KALININGRAD EXCLAVE (RF)]", fill=(255, 90, 70))
        draw.text((70, cy - 110), "11TH ARMY CORPS // ISKANDER-M BDE", fill=(255, 140, 50))
        draw.text((70, cy - 90), "KRASUKHA-4 EW JAMMING EMITTER", fill=(255, 200, 80))

        # Belarus Zone (Right, Amber tint)
        draw.rectangle([cx + 180, cy - 140, width - 60, cy + 140], fill=(22, 16, 12), outline=(255, 140, 40), width=2)
        draw.text((cx + 190, cy - 130), "[BELARUS / GRODNO AXIS]", fill=(255, 160, 50))
        draw.text((cx + 190, cy - 110), "WESTERN MILITARY DISTRICT RELAY", fill=(255, 200, 80))
        draw.text((cx + 190, cy - 90), "1520mm LOGISTICS REINFORCEMENT", fill=(255, 220, 100))

        # The Suwalki Corridor Bottleneck (Center, 65km Gap between Poland and Lithuania)
        corridor_w = 340
        draw.rectangle([cx - corridor_w//2, cy - 160, cx + corridor_w//2, cy + 160], outline=(0, 240, 255), width=2)
        draw.text((cx - 100, cy - 150), "SUWALKI GAP CHOKEPOINT (65 KM)", fill=(0, 255, 240))
        draw.text((cx - 85, cy + 140), "POLAND (SOUTH) <--> LITHUANIA (NORTH)", fill=(100, 220, 255))

        # 2. Kaliningrad Iskander-M & S-400 A2/AD Threat Envelopes (Overlapping red domes)
        kalin_center = (cx - 240, cy)
        for r_threat in [200, 320, 440]:
            draw.arc([kalin_center[0] - r_threat, kalin_center[1] - r_threat, kalin_center[0] + r_threat, kalin_center[1] + r_threat], start=300, end=60, fill=(255, 60, 40), width=1)
        draw.text((cx - 70, cy - 100), "A2/AD ISKANDER-M 500KM ENVELOPE", fill=(255, 80, 60))

        # 3. Rail Gauge Discrepancy (1435mm European Standard vs 1520mm Russian Broad Gauge)
        # European Standard Gauge 1435mm Track (South-to-North through Poland to Mockava, Cyan)
        track_x = cx - 30
        for y_t in range(cy + 150, cy - 10, 8):
            # Rail ties
            draw.line([(track_x - 14, y_t), (track_x + 14, y_t)], fill=(0, 140, 180), width=1)
        draw.line([(track_x - 10, cy + 150), (track_x - 10, cy - 10)], fill=(0, 240, 255), width=2)
        draw.line([(track_x + 10, cy + 150), (track_x + 10, cy - 10)], fill=(0, 240, 255), width=2)
        draw.text((track_x - 120, cy + 90), "1435mm STANDARD GAUGE (NATO)", fill=(0, 255, 240))

        # Russian Broad Gauge 1520mm Track (North through Lithuania & East from Grodno, Amber)
        track_rus_x = cx + 30
        for y_t in range(cy - 10, cy - 150, 9):
            # Broader rail ties
            draw.line([(track_rus_x - 18, y_t), (track_rus_x + 18, y_t)], fill=(200, 120, 30), width=1)
        draw.line([(track_rus_x - 14, cy - 10), (track_rus_x - 14, cy - 150)], fill=(255, 180, 50), width=2)
        draw.line([(track_rus_x + 14, cy - 10), (track_rus_x + 14, cy - 150)], fill=(255, 180, 50), width=2)
        draw.text((track_rus_x + 25, cy - 90), "1520mm RUSSIAN BROAD GAUGE", fill=(255, 180, 50))

        # Break-of-Gauge Transfer Node at Mockava / Sestokai (Center Junction)
        draw.rectangle([cx - 40, cy - 25, cx + 40, cy + 15], fill=(30, 20, 25), outline=(255, 220, 80), width=2)
        draw.text((cx - 32, cy - 20), "SESTOKAI HUB", fill=(255, 220, 80))
        draw.text((cx - 36, cy - 5), "BOGIE EXCHANGE", fill=(255, 140, 40))
        draw.line([(track_x, cy - 10), (track_rus_x, cy - 10)], fill=(255, 220, 80), width=2)

        # Heavy armor bottleneck queue (Tanks/flatcars queued at exchange)
        for i_tank in range(4):
            tx_box = track_x - 8
            ty_box = cy + 30 + i_tank * 26
            draw.rectangle([tx_box - 8, ty_box, tx_box + 8, ty_box + 16], fill=(15, 35, 45), outline=(0, 255, 220), width=1)
            draw.text((tx_box - 24, ty_box + 3), f"M1A2", fill=(0, 255, 200))
        draw.text((track_x - 130, cy + 40), "HEAVY ARMOR FLATCAR QUEUE", fill=(255, 100, 80))

        # 4. Telemetry Dossiers (Logistics & Soviet Line X Intelligence)
        # Left HUD Box: NATO Suwalki Gap Chokepoint Metrics
        draw.rectangle([60, 90, 310, cy - 160], fill=(12, 20, 30), outline=(0, 240, 255), width=1)
        draw.text((70, 98), "[SUWALKI LOGISTICS METRICS]", fill=(0, 240, 255))
        draw.text((70, 118), "CORRIDOR WIDTH: 65 KM (CHOKEPOINT)", fill=(255, 220, 100))
        draw.text((70, 138), "RAIL BREAK: 1435mm / 1520mm GAUGE", fill=(255, 140, 50))
        draw.text((70, 158), "BOGIE TRANSFER DELAY: 48-72 HRS", fill=(255, 80, 80))
        draw.text((70, 178), "BALTIC REINFORCEMENT: 30 DAYS", fill=(0, 255, 200))

        # Right HUD Box: Soviet Rapid Reinforcement & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 160], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET REINFORCEMENT DOCTRINE]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "FORCE: 11TH ARMY CORPS (GUSEV)", fill=(255, 200, 80))
        draw.text((width - 310, 138), "DOCTRINE: BALTIC ENCIRCLEMENT", fill=(255, 100, 80))
        draw.text((width - 310, 158), "PRE-POSITIONED AMMO: 60-DAY", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

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

    elif theme in ("orbital_qkd", "space_sigint", "satellite_monopoly", "nro_recon", "space_recon", "satellite_imagery"):
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

    elif theme in ("iit_phi", "causal_complex"):
        # Integrated Information Theory (IIT 4.0) Phi Complex & Dissociation Dynamics
        # 1. Cause-Effect State Transition Coordinate Lattice (Polar radar grid)
        for r in range(80, max(width, height) // 2, 60):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(15, 45, 60), width=1)
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            ex = cx + int(math.cos(rad) * 450)
            ey = cy + int(math.sin(rad) * 450)
            draw.line([(cx, cy), (ex, ey)], fill=(12, 35, 50), width=1)

        # 2. Central Integrated Causal Maximum (Φ Complex - Core Network)
        random.seed(112)
        core_nodes = []
        for c_idx in range(12):
            ang = (c_idx / 12.0) * 2 * math.pi
            c_dist = random.randint(50, 160)
            nx = cx + int(math.cos(ang) * c_dist)
            ny = cy + int(math.sin(ang) * c_dist)
            core_nodes.append((nx, ny, random.randint(8, 16)))

        # Dense bidirectional feedback arcs within core complex
        for i, (x1, y1, r1) in enumerate(core_nodes):
            for j, (x2, y2, r2) in enumerate(core_nodes):
                if i < j:
                    dist = math.hypot(x1 - x2, y1 - y2)
                    if dist < 180:
                        draw.line([(x1, y1), (x2, y2)], fill=(0, 255, 200), width=2)
                        # Center flow marker
                        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                        draw.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=(255, 255, 255))

        # Render Core Complex Nodes (Gold / Emerald)
        for idx, (nx, ny, rad) in enumerate(core_nodes):
            draw.ellipse([nx - rad - 4, ny - rad - 4, nx + rad + 4, ny + rad + 4], outline=(0, 255, 220), width=1)
            draw.ellipse([nx - rad, ny - rad, nx + rad, ny + rad], fill=(10, 60, 70), outline=(255, 220, 60), width=2)
            draw.text((nx + rad + 3, ny - 6), f"M_{idx}", fill=(255, 240, 120))

        # Center Phi symbol designation
        draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], outline=(0, 255, 240), width=2)
        draw.line([(cx, cy - 42), (cx, cy + 42)], fill=(0, 255, 240), width=3)
        draw.text((cx + 38, cy - 10), "Φ_max = 4.82", fill=(0, 255, 240))

        # 3. Fragmented / Dissociated Outer Sub-Mechanisms (Degraded by psychotropics)
        for o_idx in range(16):
            o_ang = random.uniform(0, 2 * math.pi)
            o_dist = random.randint(240, 420)
            ox = cx + int(math.cos(o_ang) * o_dist)
            oy = cy + int(math.sin(o_ang) * o_dist)
            # Degraded node in warning amber/crimson
            draw.ellipse([ox - 8, oy - 8, ox + 8, oy + 8], fill=(60, 15, 20), outline=(255, 80, 60), width=2)
            draw.text((ox + 10, oy - 6), f"FRACTURED-{o_idx} [Φ→0]", fill=(255, 100, 70))
            # Severed dotted connection lines
            draw.line([(ox, oy), (ox - int(math.cos(o_ang) * 40), oy - int(math.sin(o_ang) * 40))], fill=(255, 60, 40), width=1)

    elif theme in ("smoky_dragon", "retrocausality"):
        # John Archibald Wheeler's Smoky Dragon & Quantum Retrocausality
        # 1. Mach-Zehnder Optical Interferometer Geometry
        bs1_x, bs1_y = cx - 360, cy
        m1_x, m1_y = cx, cy - 200
        m2_x, m2_y = cx, cy + 200
        bs2_x, bs2_y = cx + 360, cy

        # Beam paths (Upper Path A & Lower Path B)
        draw.line([(bs1_x - 100, bs1_y), (bs1_x, bs1_y)], fill=(0, 255, 240), width=3)  # Input laser
        draw.line([(bs1_x, bs1_y), (m1_x, m1_y)], fill=(0, 220, 255), width=2)           # Path A1
        draw.line([(m1_x, m1_y), (bs2_x, bs2_y)], fill=(0, 220, 255), width=2)           # Path A2
        draw.line([(bs1_x, bs1_y), (m2_x, m2_y)], fill=(255, 160, 60), width=2)          # Path B1
        draw.line([(m2_x, m2_y), (bs2_x, bs2_y)], fill=(255, 160, 60), width=2)          # Path B2

        # 2. Wheeler's "Smoky Body" — Swirling unobserved quantum probability field
        random.seed(77)
        for sy in range(cy - 160, cy + 160, 6):
            pts = []
            for sx in range(cx - 240, cx + 240, 8):
                sw1 = math.sin(sx * 0.025 + sy * 0.03)
                sw2 = math.cos(sx * 0.015 - sy * 0.02)
                s_amp = (sw1 + sw2) * 18.0
                pts.append((sx, sy + s_amp))
            if len(pts) > 1:
                # Ghostly smoke gradient
                s_alpha = int(45 + 55 * math.sin((sy - (cy - 160)) / 320.0 * math.pi))
                draw.line(pts, fill=(s_alpha // 2, s_alpha, int(s_alpha * 1.4)), width=1)

        # 3. Optical components (Beamsplitters & Mirrors)
        # BS1 (The Tail)
        draw.line([(bs1_x - 25, bs1_y - 25), (bs1_x + 25, bs1_y + 25)], fill=(255, 255, 255), width=3)
        draw.text((bs1_x - 85, bs1_y - 40), "THE TAIL [BS1]", fill=(0, 255, 220))

        # M1 & M2 Mirrors
        draw.line([(m1_x - 20, m1_y + 20), (m1_x + 20, m1_y - 20)], fill=(0, 200, 255), width=4)
        draw.line([(m2_x - 20, m2_y - 20), (m2_x + 20, m2_y + 20)], fill=(255, 140, 50), width=4)

        # BS2 (Delayed Choice Actuator)
        draw.line([(bs2_x - 25, bs2_y - 25), (bs2_x + 25, bs2_y + 25)], fill=(255, 220, 60), width=3)
        draw.text((bs2_x - 60, bs2_y - 45), "DELAYED-CHOICE BS2", fill=(255, 220, 80))

        # 4. Detectors D1 and D2 (The Teeth)
        d1_x, d1_y = bs2_x + 80, bs2_y - 60
        d2_x, d2_y = bs2_x + 80, bs2_y + 60
        draw.line([(bs2_x, bs2_y), (d1_x, d1_y)], fill=(0, 255, 200), width=2)
        draw.line([(bs2_x, bs2_y), (d2_x, d2_y)], fill=(255, 100, 80), width=2)
        draw.rectangle([d1_x - 8, d1_y - 12, d1_x + 16, d1_y + 12], fill=(10, 50, 60), outline=(0, 255, 220), width=2)
        draw.rectangle([d2_x - 8, d2_y - 12, d2_x + 16, d2_y + 12], fill=(60, 20, 20), outline=(255, 100, 80), width=2)
        draw.text((d1_x + 24, d1_y - 8), "TEETH [D1: WAVE]", fill=(0, 255, 200))
        draw.text((d2_x + 24, d2_y - 8), "TEETH [D2: PARTICLE]", fill=(255, 100, 80))

    elif theme in ("supply_chain_fraud", "subcontractor_grift", "defense_fraud", "aerospace_monopoly", "maintenance_cartel", "diagnostic_lockin", "defense_ai_cartel", "revolving_door", "advisory_collusion", "hypersonic_fraud", "scramjet_failure", "wind_tunnel_fraud", "cfd_falsification", "black_budget", "sap_audit", "pentagon_sap", "gosplan_diversion", "rare_earths", "critical_minerals", "mineral_cartel", "tungsten_carbide", "munitions_fraud", "strategic_metals", "propellant_fraud", "nitrocellulose_cartel", "munitions_degradation", "drone_gouging", "sbir_fraud", "tech_front_company", "counterfeit_chip", "microelectronics_fraud", "line_x"):
        # Defense Industrial Base Supply Chain Fraud & Phantom Subcontractor Invoicing
        # 1. Procurement Cascading Waterfall Funnel (Top-down tiers)
        tiers = [
            (cy - 200, 700, "PRIME CONTRACTOR // COST-PLUS AWARD [DOD PRIME]", (0, 220, 255), "$520 BASE PART"),
            (cy - 100, 560, "TIER-1 SYSTEMS INTEGRATOR // MANAGEMENT OVERHEAD [+38%]", (255, 200, 60), "$1,480 BILLED"),
            (cy, 420, "TIER-2 SHELL ENTITY // BROKERAGE & PASS-THROUGH [+85%]", (255, 140, 50), "$4,650 BILLED"),
            (cy + 100, 280, "TIER-3 SHADOW SUPPLIER // UNVERIFIED COMMERCIAL OFF-THE-SHELF", (255, 80, 60), "$8,900 BILLED"),
            (cy + 200, 160, "FINAL PENTAGON INVOICE // LINE ITEM TOTAL", (255, 40, 40), "$12,450 DELIVERED")
        ]

        # Draw funnel outline and tiers
        for i, (ty, tw, label, col, price) in enumerate(tiers):
            draw.rectangle([cx - tw // 2, ty - 24, cx + tw // 2, ty + 24], fill=(15, 20, 30), outline=col, width=2)
            draw.text((cx - tw // 2 + 15, ty - 8), label, fill=col)
            draw.text((cx + tw // 2 - 130, ty - 8), price, fill=(255, 255, 255))
            if i < len(tiers) - 1:
                next_y, next_w = tiers[i+1][0], tiers[i+1][1]
                # Downward connector arrows
                draw.line([(cx - 40, ty + 24), (cx - 40, next_y - 24)], fill=(255, 120, 50), width=2)
                draw.line([(cx + 40, ty + 24), (cx + 40, next_y - 24)], fill=(255, 120, 50), width=2)
                draw.line([(cx, ty + 24), (cx, next_y - 24)], fill=(255, 220, 60), width=1)

        # 2. Forensic Audit Warnings & Counterfeit Alerts (Side boxes)
        draw.rectangle([60, cy - 120, 240, cy + 120], fill=(40, 12, 16), outline=(255, 60, 60), width=2)
        draw.text((75, cy - 100), "[FORENSIC AUDIT]", fill=(255, 80, 80))
        draw.text((75, cy - 60), "PHANTOM BILLING", fill=(255, 220, 100))
        draw.text((75, cy - 30), "ZERO PHYSICAL", fill=(255, 255, 255))
        draw.text((75, cy - 10), "DELIVERY LOGGED", fill=(255, 255, 255))
        draw.text((75, cy + 30), "STATUS: FRAUD", fill=(255, 40, 40))
        draw.text((75, cy + 60), "AUDIT REF #8942", fill=(200, 200, 200))

        draw.rectangle([width - 240, cy - 120, width - 60, cy + 120], fill=(30, 25, 15), outline=(255, 160, 40), width=2)
        draw.text((width - 225, cy - 100), "[LINE X INTERCEPT]", fill=(255, 180, 50))
        draw.text((width - 225, cy - 60), "COUNTERFEIT CHIP", fill=(255, 80, 60))
        draw.text((width - 225, cy - 30), "TRACE: UNVERIFIED", fill=(255, 255, 255))
        draw.text((width - 225, cy - 10), "BROKER NETWORK", fill=(255, 255, 255))
        draw.text((width - 225, cy + 30), "TAMPER DETECTED", fill=(255, 60, 40))
        draw.text((width - 225, cy + 60), "DIRECTORATE T", fill=(255, 200, 80))

    elif theme in ("fuel_smuggling", "bunkering_fraud", "fuel_cartel", "oil_theft", "bunkering_price_fixing"):
        # Defense Fuel Smuggling Syndicates & Bunkering Fraud Architecture
        # 1. Background petroleum grid / fuel infrastructure schematic
        for gy in range(80, height - 80, 35):
            draw.line([(60, gy), (width - 60, gy)], fill=(18, 24, 20), width=1)
        for gx in range(60, width - 60, 45):
            draw.line([(gx, 80), (gx, height - 80)], fill=(18, 24, 20), width=1)

        # 2. Fuel Storage Tanks (Depots)
        # Tank 1: NATO Forward Storage Terminal (Left)
        t1_x, t1_y = cx - 320, cy - 40
        draw.rectangle([t1_x - 70, t1_y - 80, t1_x + 70, t1_y + 80], fill=(15, 25, 20), outline=(0, 220, 160), width=2)
        draw.ellipse([t1_x - 70, t1_y - 95, t1_x + 70, t1_y - 65], fill=(20, 35, 25), outline=(0, 255, 180), width=2)
        # Liquid fill level indicator (Depleted / Siphoned)
        fill_y = t1_y + 20
        draw.rectangle([t1_x - 66, fill_y, t1_x + 66, t1_y + 76], fill=(40, 30, 10), outline=(255, 140, 40), width=1)
        draw.text((t1_x - 55, t1_y - 45), "JP-8 BULK TANK #01", fill=(0, 255, 200))
        draw.text((t1_x - 55, t1_y - 25), "CAP: 500,000 GAL", fill=(200, 200, 200))
        draw.text((t1_x - 55, t1_y + 35), "ACTUAL LEVEL: 24%", fill=(255, 80, 60))
        draw.text((t1_x - 55, t1_y + 55), "STATUS: SIPHONED", fill=(255, 60, 60))

        # Tank 2: Illicit Commercial Bunkering Barge / Siphon Vessel (Right)
        t2_x, t2_y = cx + 320, cy - 40
        draw.rectangle([t2_x - 70, t2_y - 80, t2_x + 70, t2_y + 80], fill=(25, 18, 15), outline=(255, 120, 50), width=2)
        draw.ellipse([t2_x - 70, t2_y - 95, t2_x + 70, t2_y - 65], fill=(35, 22, 18), outline=(255, 160, 60), width=2)
        # Illicit Fill Level (Overflowing with stolen fuel)
        fill_y2 = t2_y - 50
        draw.rectangle([t2_x - 66, fill_y2, t2_x + 66, t2_y + 76], fill=(50, 40, 15), outline=(255, 200, 50), width=1)
        draw.text((t2_x - 60, t2_y - 45), "OFFSHORE BUNKER BARGE", fill=(255, 160, 60))
        draw.text((t2_x - 60, t2_y - 25), "AIS: SPOOFED/DARK", fill=(255, 60, 60))
        draw.text((t2_x - 60, t2_y + 35), "BLACK MARKET SLOSH", fill=(255, 220, 60))
        draw.text((t2_x - 60, t2_y + 55), "RESALE SPOT: +180%", fill=(0, 255, 200))

        # 3. Pipeline Conduit & Tampered Bypass Manifold (Center)
        pipe_y = cy + 20
        # Official authorized delivery line
        draw.line([(t1_x + 70, pipe_y), (cx, pipe_y)], fill=(0, 220, 180), width=6)
        draw.line([(t1_x + 70, pipe_y), (cx, pipe_y)], fill=(255, 255, 255), width=2)
        # Tampered bypass siphon line to offshore barge
        draw.line([(cx, pipe_y), (cx + 80, pipe_y + 70), (t2_x - 70, pipe_y + 70)], fill=(255, 80, 50), width=4)
        draw.line([(cx, pipe_y), (cx + 80, pipe_y + 70), (t2_x - 70, pipe_y + 70)], fill=(255, 220, 80), width=1)

        # Central Flowmeter Manifold Box
        draw.rectangle([cx - 45, pipe_y - 35, cx + 45, pipe_y + 35], fill=(20, 30, 40), outline=(255, 220, 60), width=2)
        draw.text((cx - 38, pipe_y - 25), "FLOWMETER", fill=(255, 220, 80))
        draw.text((cx - 38, pipe_y - 5), "BYPASS VALVE", fill=(255, 80, 60))
        draw.text((cx - 38, pipe_y + 15), "SEAL: BROKEN", fill=(255, 40, 40))

        # Flow direction animated vectors
        for fx in range(t1_x + 90, cx - 10, 40):
            draw.polygon([(fx, pipe_y - 6), (fx + 10, pipe_y), (fx, pipe_y + 6)], fill=(0, 255, 200))
        for fx in range(cx + 90, t2_x - 80, 40):
            draw.polygon([(fx, pipe_y + 64), (fx + 10, pipe_y + 70), (fx, pipe_y + 76)], fill=(255, 120, 50))

        # 4. Forensic Telemetry Sidebars
        # Left Box: Defense Contract Audit
        draw.rectangle([60, cy - 200, 260, cy - 110], fill=(20, 15, 25), outline=(255, 80, 60), width=1)
        draw.text((70, cy - 190), "[DOD LOGISTICS FORENSICS]", fill=(255, 100, 80))
        draw.text((70, cy - 170), "INVOICED: 2,400,000 GAL JP-8", fill=(255, 220, 100))
        draw.text((70, cy - 150), "PHYSICAL DELIVERED: 420,000", fill=(255, 60, 60))
        draw.text((70, cy - 130), "DISCREPANCY: -$14.8M LOSS", fill=(255, 80, 80))

        # Right Box: Soviet Black Sea Fleet Fuel Diversion Dossier
        draw.rectangle([width - 290, cy - 200, width - 60, cy - 100], fill=(25, 20, 15), outline=(255, 140, 40), width=1)
        draw.text((width - 280, cy - 190), "[SOVIET BLACK SEA FLEET AUDIT]", fill=(255, 160, 50))
        draw.text((width - 280, cy - 170), "SEVASTOPOL NAVAL BUNKER DRAIN", fill=(255, 200, 80))
        draw.text((width - 280, cy - 150), "KGB 3RD DIR / MAFIA COLLUSION", fill=(255, 100, 80))
        draw.text((width - 280, cy - 130), "WARSHIPS COLD AT PIER TO CONCEAL", fill=(255, 220, 120))
        draw.text((width - 280, cy - 110), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("spin_liquid", "kagome_spin_liquid", "spin_liquid_theory", "topological_braiding", "anyon_braiding", "topological_insulator", "topological_insulators", "helical_edge", "topological_superconductivity", "majorana_zero_modes", "majorana_nanowires", "landau_cryogenics"):
        # Kitaev Honeycomb Spin Liquid & Non-Abelian Anyon Braiding Engine
        # 1. Frustrated Honeycomb Lattice / Kagome background
        hex_r = 38
        h_vert = hex_r * 1.5
        h_horiz = hex_r * math.sqrt(3)
        for row in range(-2, 16):
            for col in range(-2, 24):
                hx = int(col * h_horiz + (row % 2) * (h_horiz / 2.0))
                hy = int(row * h_vert)
                # Draw small hexagon vertices and frustrated spin arrows
                pts = []
                for a in range(6):
                    ang = math.radians(a * 60 + 30)
                    pts.append((hx + int(hex_r * 0.7 * math.cos(ang)), hy + int(hex_r * 0.7 * math.sin(ang))))
                draw.polygon(pts, outline=(18, 42, 60), fill=None)
                # Spin orientation arrow
                spin_up = ((row + col) % 2 == 0)
                col_spin = (0, 220, 240) if spin_up else (255, 80, 160)
                sy_dir = -8 if spin_up else 8
                draw.line([(hx, hy - sy_dir), (hx, hy + sy_dir)], fill=col_spin, width=1)
                draw.point((hx, hy), fill=(255, 255, 255))

        # 2. Braiding Worldlines (Non-Abelian Anyon trajectories)
        strands = [
            (cy - 120, (0, 255, 240), 0.007, 0.0, 75, "ANYON γ1 [MAJORANA ZERO MODE]"),
            (cy - 40, (255, 60, 180), 0.009, 1.2, 85, "ANYON γ2 [NON-ABELIAN DEFECT]"),
            (cy + 40, (255, 210, 60), 0.008, 2.4, 80, "ANYON γ3 [CHIRAL EDGE CURRENT]"),
            (cy + 120, (60, 255, 140), 0.006, 3.6, 70, "ANYON γ4 [TOPOLOGICAL QUBIT]")
        ]

        for base_y, col_line, freq, phase, amp, label in strands:
            pts = []
            for x in range(60, width - 60, 3):
                # Braid weaving equation
                y_val = base_y + amp * math.sin(x * freq + phase) + (amp * 0.35) * math.cos(x * freq * 2.2 - phase)
                pts.append((x, y_val))
            if len(pts) > 1:
                # Main braid line with glow
                draw.line(pts, fill=col_line, width=3)
                draw.line([(x, y - 1) for x, y in pts], fill=(col_line[0]//2, col_line[1]//2, col_line[2]//2), width=1)
                draw.line([(x, y + 1) for x, y in pts], fill=(col_line[0]//2, col_line[1]//2, col_line[2]//2), width=1)

            # Strand label
            draw.text((80, base_y - 25), label, fill=col_line)

        # 3. Braiding Node Intersections / Topological Crossings
        random.seed(42)
        for i in range(12):
            bx = 180 + i * 80
            by = cy + int(60 * math.sin(i * 0.8))
            draw.ellipse([bx - 10, by - 10, bx + 10, by + 10], outline=(255, 255, 255), width=2)
            draw.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(0, 255, 240))
            draw.text((bx - 22, by + 14), f"σ_{i+1} BRAID", fill=(200, 240, 255))

        # 4. Cryptographic Parity & Monodromy Matrix HUD
        draw.rectangle([60, cy - 200, 310, cy - 140], fill=(10, 25, 38), outline=(0, 255, 240), width=1)
        draw.text((70, cy - 190), "UNITARY MONODROMY: U = exp(iπ/8 σ_z)", fill=(0, 255, 220))
        draw.text((70, cy - 170), "TOPOLOGICAL PROTECTION: DECOHERENCE = 0", fill=(255, 220, 80))
        draw.text((70, cy - 150), "CHERN NUMBER: C = 1 // CHIRAL FERMION", fill=(255, 120, 200))

        draw.rectangle([width - 330, cy + 140, width - 60, cy + 200], fill=(25, 15, 25), outline=(255, 80, 180), width=1)
        draw.text((width - 320, cy + 150), "[8TH CHIEF DIRECTORATE AUDIT]", fill=(255, 100, 200))
        draw.text((width - 320, cy + 170), "SOVIET CIPHER APPARATUS // FIALKA-M", fill=(255, 220, 100))
        draw.text((width - 320, cy + 185), "STATUS: NON-COMPUTABLE CODEBREAKING", fill=(255, 60, 60))

    elif theme in ("undersea_cable", "gugi_seabed", "seabed_warfare", "arctic_seabed", "lomonosov_ridge", "svalbard_cable", "red_sea_cables", "bab_el_mandeb", "barents_bastion", "bastion_doctrine", "northern_fleet", "giuk_gap", "undersea_drones", "titanium_sub"):
        # Deep Seabed Infrastructure & Russian GUGI Covert Reconnaissance
        # 1. Abyssal Bathymetry Contour Lines (Depth 3,000m+)
        for depth_y in range(120, height, 45):
            pts = []
            for x in range(0, width, 15):
                wave = math.sin(x * 0.005 + depth_y * 0.03) * 22.0 + math.cos(x * 0.012) * 12.0
                pts.append((x, depth_y + int(wave)))
            c_depth = int(10 + (depth_y / height) * 35)
            draw.line(pts, fill=(c_depth // 2, c_depth, int(c_depth * 1.8)), width=1)

        # 2. Transoceanic Fiber Optic Submarine Cable on Ocean Floor
        cable_y_base = cy + 100
        cable_pts = []
        for x in range(40, width - 40, 5):
            cy_pt = cable_y_base + int(35 * math.sin(x * 0.004) + 15 * math.cos(x * 0.009))
            cable_pts.append((x, cy_pt))

        # Heavy armored conduit + glowing optical core
        draw.line(cable_pts, fill=(30, 45, 65), width=8)
        draw.line(cable_pts, fill=(0, 220, 255), width=3)
        draw.line(cable_pts, fill=(255, 255, 255), width=1)

        # Submarine Optical Repeaters along the cable
        for rep_x in (260, 640, 1020):
            rep_y = cable_y_base + int(35 * math.sin(rep_x * 0.004) + 15 * math.cos(rep_x * 0.009))
            draw.rectangle([rep_x - 22, rep_y - 12, rep_x + 22, rep_y + 12], fill=(15, 30, 45), outline=(0, 255, 200), width=2)
            draw.text((rep_x - 30, rep_y + 16), "REPEATER #0" + str(rep_x//200), fill=(0, 240, 255))
            draw.ellipse([rep_x - 4, rep_y - 4, rep_x + 4, rep_y + 4], fill=(255, 220, 50))

        # 3. GUGI Deep-Submergence Spy Vehicle (Yantar / Losharik Class)
        sub_cx = 580
        sub_cy = cy - 80
        # Submersible hull (Titanium spherical compartments inside streamlined casing)
        draw.polygon([
            (sub_cx - 90, sub_cy - 18),
            (sub_cx + 70, sub_cy - 18),
            (sub_cx + 100, sub_cy),
            (sub_cx + 70, sub_cy + 18),
            (sub_cx - 90, sub_cy + 18),
            (sub_cx - 105, sub_cy)
        ], fill=(25, 30, 40), outline=(255, 80, 60), width=2)

        # Conning tower & acoustic array
        draw.rectangle([sub_cx - 15, sub_cy - 35, sub_cx + 25, sub_cy - 18], fill=(35, 40, 55), outline=(255, 100, 80), width=1)
        draw.line([(sub_cx + 5, sub_cy - 48), (sub_cx + 5, sub_cy - 35)], fill=(255, 200, 80), width=2)

        # Manipulator Arm reaching toward fiber cable
        arm_target_x = 620
        arm_target_y = cable_y_base + int(35 * math.sin(arm_target_x * 0.004) + 15 * math.cos(arm_target_x * 0.009))
        draw.line([(sub_cx + 40, sub_cy + 18), (sub_cx + 60, sub_cy + 80)], fill=(255, 140, 40), width=3)
        draw.line([(sub_cx + 60, sub_cy + 80), (arm_target_x, arm_target_y - 6)], fill=(255, 140, 40), width=2)
        # Laser cutting arc / Tap clamp glow
        draw.ellipse([arm_target_x - 12, arm_target_y - 18, arm_target_x + 12, arm_target_y + 6], outline=(255, 60, 40), width=2)
        draw.point((arm_target_x, arm_target_y - 6), fill=(255, 255, 255))

        # Spotlights shining into dark abyss
        draw.polygon([(sub_cx + 70, sub_cy), (arm_target_x - 50, arm_target_y + 30), (arm_target_x + 50, arm_target_y + 30)], fill=None, outline=(50, 100, 140))

        # 4. Seabed Sonar & Tap Status HUD
        draw.rectangle([60, 100, 310, 170], fill=(12, 18, 28), outline=(255, 80, 60), width=1)
        draw.text((70, 110), "[GUGI SEABED TELEMETRY]", fill=(255, 90, 70))
        draw.text((70, 130), "DEPTH: 3,420 METERS // HIGH PRESSURE", fill=(200, 220, 255))
        draw.text((70, 150), "TARGET: TRANSATLANTIC FIBER C-8", fill=(255, 200, 80))

        draw.rectangle([width - 320, 100, width - 60, 170], fill=(20, 15, 15), outline=(255, 60, 60), width=1)
        draw.text((width - 310, 110), "[SOSUS ACOUSTIC ALERT]", fill=(255, 80, 80))
        draw.text((width - 310, 130), "ANOMALOUS CAVITATION DETECTED", fill=(255, 180, 60))
        draw.text((width - 310, 150), "CLASSIFICATION: RUSSIAN SPECIAL SUBS", fill=(255, 60, 40))

    elif theme in ("free_energy", "markov_blanket", "active_inference", "hft_neuro_feedback", "neuro_feedback", "trading_biometrics", "reflex_modification"):
        # Karl Friston Free Energy Principle & Markov Blanket Architecture
        # 1. External States: Chaotic Langevin Fluctuations in outer perimeter
        random.seed(77)
        for _ in range(80):
            ex = random.randint(40, width - 40)
            ey = random.randint(40, height - 40)
            dist_to_center = math.hypot(ex - cx, ey - cy)
            if dist_to_center > 240:
                # Stochastic environmental fluctuation vectors
                ang = random.uniform(0, 2 * math.pi)
                flen = random.randint(15, 35)
                draw.line([(ex, ey), (ex + int(math.cos(ang) * flen), ey + int(math.sin(ang) * flen))], fill=(35, 60, 95), width=1)
                draw.point((ex, ey), fill=(100, 160, 240))

        # 2. Markov Blanket Boundary: Sensory States (Cyan) & Active States (Amber)
        blanket_rx = 260
        blanket_ry = 180
        # Sensory partition arc (left/top)
        draw.arc([cx - blanket_rx, cy - blanket_ry, cx + blanket_rx, cy + blanket_ry], start=90, end=270, fill=(0, 240, 255), width=3)
        # Active partition arc (right/bottom)
        draw.arc([cx - blanket_rx, cy - blanket_ry, cx + blanket_rx, cy + blanket_ry], start=270, end=90, fill=(255, 180, 50), width=3)

        # Blanket boundary nodes
        for deg in range(0, 360, 20):
            rad = math.radians(deg)
            bx = cx + int(blanket_rx * math.cos(rad))
            by = cy + int(blanket_ry * math.sin(rad))
            is_sensory = (90 <= deg <= 270)
            col_b = (0, 255, 240) if is_sensory else (255, 180, 50)
            draw.ellipse([bx - 6, by - 6, bx + 6, by + 6], fill=(10, 25, 40), outline=col_b, width=2)
            draw.point((bx, by), fill=(255, 255, 255))

        draw.text((cx - blanket_rx - 110, cy - 10), "SENSORY STATES [s]", fill=(0, 255, 240))
        draw.text((cx + blanket_rx + 20, cy - 10), "ACTIVE STATES [a]", fill=(255, 180, 50))

        # 3. Internal States (Generative Model inside the blanket)
        inner_r = 130
        draw.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r], fill=(15, 20, 35), outline=(180, 100, 255), width=2)

        # Internal Bayesian Belief Network (nodes & message passing)
        internal_nodes = [
            (cx - 50, cy - 40, "μ1 [PRIOR]"),
            (cx + 50, cy - 40, "μ2 [LIKELIHOOD]"),
            (cx, cy + 30, "μ3 [POSTERIOR]"),
            (cx - 60, cy + 50, "ε_p [ERROR]"),
            (cx + 60, cy + 50, "ε_v [VARIANCE]")
        ]
        for nx, ny, nlabel in internal_nodes:
            draw.ellipse([nx - 14, ny - 14, nx + 14, ny + 14], fill=(20, 15, 40), outline=(220, 120, 255), width=2)
            draw.text((nx - 24, ny - 24), nlabel, fill=(200, 220, 255))

        # Message passing links
        for i in range(len(internal_nodes)):
            for j in range(i + 1, len(internal_nodes)):
                draw.line([(internal_nodes[i][0], internal_nodes[i][1]), (internal_nodes[j][0], internal_nodes[j][1])], fill=(90, 50, 140), width=1)

        # 4. Free Energy Variational Gradient Curve HUD
        draw.rectangle([60, cy + 130, 320, cy + 200], fill=(10, 20, 35), outline=(0, 255, 220), width=1)
        draw.text((70, cy + 140), "VARIATIONAL BOUND: F = D_KL + E_q[ln p]", fill=(0, 255, 220))
        draw.text((70, cy + 160), "SURPRISE REDUCTION: -ln p(y) <= F", fill=(255, 220, 80))
        draw.text((70, cy + 180), "STATUS: HOMEOSTATIC EQUILIBRIUM", fill=(120, 255, 180))

        draw.rectangle([width - 340, cy - 200, width - 60, cy - 130], fill=(30, 15, 20), outline=(255, 80, 80), width=1)
        draw.text((width - 330, cy - 190), "[KGB REFLEXIVE CONTROL AUDIT]", fill=(255, 90, 80))
        draw.text((width - 330, cy - 170), "LEFEBVRE ALGEBRA // AFFECT MATRIX", fill=(255, 180, 60))
        draw.text((width - 330, cy - 150), "TARGET INFERENCE HACK: ACTIVE INJECTION", fill=(255, 60, 60))

    elif theme in ("quantum_darwinism", "pointer_states", "theremin_bug"):
        # Wojciech Zurek Quantum Darwinism & Soviet Passive Resonant Bugging
        # 1. Environmental Proliferation Sectors (Information Redundancy)
        for ring_r in range(70, 360, 45):
            draw.ellipse([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], outline=(20, 50, 70), width=1)
            # Sector partition spokes
            for deg in range(0, 360, 30):
                rad = math.radians(deg)
                px = cx + int(ring_r * math.cos(rad))
                py = cy + int(ring_r * math.sin(rad))
                draw.point((px, py), fill=(0, 255, 240))

        # Replicated pointer state information bits in environment
        random.seed(137)
        for i in range(64):
            ang = random.uniform(0, 2 * math.pi)
            rad_dist = random.uniform(80, 340)
            px = cx + int(rad_dist * math.cos(ang))
            py = cy + int(rad_dist * math.sin(ang))
            bit_val = (i % 2 == 0)
            col_bit = (0, 240, 255) if bit_val else (255, 140, 60)
            draw.text((px, py), "1" if bit_val else "0", fill=col_bit)

        # 2. Central Quantum System (The Seed)
        sys_r = 35
        draw.ellipse([cx - sys_r, cy - sys_r, cx + sys_r, cy + sys_r], fill=(15, 30, 50), outline=(0, 255, 240), width=2)
        draw.text((cx - 24, cy - 8), "|ψ_S⟩", fill=(255, 255, 255))

        # 3. Léon Theremin Passive Cavity Resonator (The Great Seal Bug cross-section)
        bug_x = cx + 380
        bug_y = cy - 40
        # Cylindrical brass cavity
        draw.ellipse([bug_x - 45, bug_y - 80, bug_x + 45, bug_y + 80], outline=(255, 180, 50), width=2)
        # Thin metallic membrane (Capacitive microphone)
        draw.line([(bug_x, bug_y - 70), (bug_x, bug_y + 70)], fill=(255, 240, 100), width=2)
        # Monopole antenna rod protruding
        draw.line([(bug_x, bug_y - 80), (bug_x, bug_y - 140)], fill=(255, 200, 60), width=3)
        draw.ellipse([bug_x - 4, bug_y - 144, bug_x + 4, bug_y - 136], fill=(255, 255, 255))
        draw.text((bug_x - 55, bug_y + 90), "THEREMIN CAVITY", fill=(255, 200, 60))
        draw.text((bug_x - 50, bug_y + 110), "MEMBRANE Q: 45K", fill=(200, 220, 255))

        # Acoustic RF interrogation wave incident on bug
        for wav_x in range(bug_x - 160, bug_x - 40, 25):
            draw.arc([wav_x, bug_y - 50, wav_x + 30, bug_y + 50], start=300, end=60, fill=(0, 220, 255), width=2)
        draw.text((bug_x - 150, bug_y - 65), "330MHz RF BEAM", fill=(0, 220, 255))

        # 4. Quantum Darwinism Classicality HUD
        draw.rectangle([60, cy - 200, 320, cy - 130], fill=(10, 25, 40), outline=(0, 255, 240), width=1)
        draw.text((70, cy - 190), "MUTUAL INFO: I(S : E_k) = H(S) [PLATEAU]", fill=(0, 255, 220))
        draw.text((70, cy - 170), "REDUNDANCY R = 10^12 COPIES // OBJECTIVE", fill=(255, 220, 80))
        draw.text((70, cy - 150), "DECOHERENCE TIME: τ_D = 10^-23 SECONDS", fill=(120, 255, 200))

        draw.rectangle([60, cy + 130, 320, cy + 200], fill=(25, 20, 15), outline=(255, 140, 50), width=1)
        draw.text((70, cy + 140), "[KGB PASSIVE RESONANCE AUDIT]", fill=(255, 160, 50))
        draw.text((70, cy + 160), "BATTERYLESS CAVITY // ZERO EMISSION", fill=(255, 220, 100))
        draw.text((70, cy + 180), "STATUS: ILLUMINATION-ACTIVATED ONLY", fill=(255, 80, 80))

    elif theme in ("orch_or", "penrose_hameroff", "tubulin_quantum", "synaptic_plasticity", "microtubules", "bio_cybernetics", "biophoton", "biophotonic", "mitogenetic_radiation", "bio_resonance"):
        # Penrose Orch-OR Gravitational Collapse & Tubulin Quantum Anesthesia
        # 1. Spacetime bifurcation sheets (Gravitational Objective Reduction)
        sheet_top = cy - 220
        sheet_bot = cy + 220
        for sx in range(80, width - 80, 30):
            # Curved geodesics bifurcating into two alternate spacetime geometries
            t_ratio = (sx - 80) / (width - 160)
            sep = int(math.sin(t_ratio * math.pi) * 75)
            
            # Geometry sheet A (cyan superposition branch)
            draw.line([(sx, cy - sep), (sx + 20, cy - sep - 15)], fill=(0, int(160 + 90 * t_ratio), 255), width=1)
            # Geometry sheet B (magenta/violet superposition branch)
            draw.line([(sx, cy + sep), (sx + 20, cy + sep + 15)], fill=(int(200 * t_ratio), 100, 255), width=1)

        # Objective Reduction threshold boundary (gravitational collapse line at x = width//2 + 80)
        collapse_x = width // 2 + 80
        draw.line([(collapse_x, 80), (collapse_x, height - 80)], fill=(255, 220, 60), width=2)
        draw.text((collapse_x + 8, 95), "ORCH-OR COLLAPSE THRESHOLD: E_G = ℏ / τ", fill=(255, 220, 80))
        draw.text((collapse_x + 8, 115), "NON-COMPUTABLE REDUCTION // 40Hz GAMMA", fill=(0, 255, 220))

        # 2. Microtubule Protofilament Lattice (Cylindrical Array of Tubulin Dimers)
        mt_left = cx - 380
        mt_right = cx + 60
        random.seed(137)
        for col_idx, tx in enumerate(range(mt_left, mt_right, 32)):
            for row_idx, ty in enumerate(range(cy - 160, cy + 160, 24)):
                # Tubulin dimer: alpha-tubulin (emerald) & beta-tubulin (amber/gold)
                is_alpha = ((col_idx + row_idx) % 2 == 0)
                dimer_col = (30, 240, 160) if is_alpha else (255, 200, 50)
                
                # Superposition oscillation offset
                osc = math.sin(tx * 0.04 + ty * 0.03) * 6
                
                # Tubulin dimer node
                draw.ellipse([tx - 8, int(ty + osc - 7), tx + 8, int(ty + osc + 7)], fill=(10, 35, 45), outline=dimer_col, width=2)
                
                # Aromatic ring pi-cloud resonance center
                if (col_idx * 3 + row_idx) % 5 == 0:
                    draw.ellipse([tx - 3, int(ty + osc - 3), tx + 3, int(ty + osc + 3)], fill=(0, 255, 240))
                    # Dipole vector line
                    draw.line([(tx, int(ty + osc)), (tx + 12, int(ty + osc - 8))], fill=(0, 240, 255), width=1)
                
                # Anesthetic binding site (quenched dipole shown in red)
                if col_idx == 4 and row_idx in (5, 6, 7):
                    draw.rectangle([tx - 6, int(ty + osc - 6), tx + 6, int(ty + osc + 6)], outline=(255, 60, 60), width=2)
                    draw.point((tx, int(ty + osc)), fill=(255, 100, 100))

        # Annotations on Microtubule Lattice
        draw.text((mt_left, cy - 195), "13-PROTOFILAMENT MICROTUBULE CYLINDER", fill=(0, 255, 240))
        draw.text((mt_left, cy + 175), "TUBULIN DIPOLE AROMATIC CLOUD // 8.3 MHz HARMONIC", fill=(30, 240, 160))
        
        # Anesthetic Lock Callout
        callout_x = mt_left + 4 * 32
        callout_y = cy - 20
        draw.line([(callout_x, callout_y), (callout_x + 90, callout_y - 70)], fill=(255, 70, 70), width=1)
        draw.rectangle([callout_x + 90, callout_y - 110, callout_x + 310, callout_y - 50], fill=(30, 10, 10), outline=(255, 60, 60), width=1)
        draw.text((callout_x + 100, callout_y - 100), "ANESTHETIC BINDING POCKET", fill=(255, 100, 100))
        draw.text((callout_x + 100, callout_y - 80), "ISOFLURANE DIPOLE QUENCH: LOSS OF CONSCIOUSNESS", fill=(255, 180, 180))
        draw.text((callout_x + 100, callout_y - 65), "QUANTUM COHERENCE COLLAPSED", fill=(255, 60, 60))

        # 3. Telemetry HUD: Non-Computability & Soviet KGB Bio-Telemetry
        draw.rectangle([width - 340, cy - 180, width - 50, cy - 90], fill=(10, 25, 40), outline=(0, 255, 240), width=1)
        draw.text((width - 330, cy - 170), "[PENROSE NON-COMPUTABILITY]", fill=(0, 255, 240))
        draw.text((width - 330, cy - 150), "GÖDELIAN COGNITIVE UNBOUNDEDNESS", fill=(255, 220, 80))
        draw.text((width - 330, cy - 130), "AI ARCHITECTURE LIMIT: TURING TAPE", fill=(200, 220, 255))
        draw.text((width - 330, cy - 110), "BIOLOGICAL ORCH-OR: GRAVITATIONAL", fill=(0, 240, 180))

        draw.rectangle([width - 340, cy + 80, width - 50, cy + 180], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 330, cy + 90), "[KGB 1ST CHIEF BIO-TELEMETRY]", fill=(255, 140, 50))
        draw.text((width - 330, cy + 110), "LAB-12 INTERROGATION PHARMACOLOGY", fill=(255, 200, 80))
        draw.text((width - 330, cy + 130), "RECEPTOR TARGET: TUBULIN DIPOLE GRID", fill=(255, 220, 120))
        draw.text((width - 330, cy + 150), "STATUS: ARCHIVAL DOSSIER DISCLOSED", fill=(255, 80, 80))

    elif theme in ("photonic_crystals", "laser_optics", "microcavity", "nonlinear_optics", "cavity_qed", "rabi_splitting", "microresonators", "atomic_laser", "topological_photonics", "photonic_waveguide", "optical_computing", "nv_center", "diamond_magnetometry", "quantum_magnetometer", "nv_diamond", "nv_gravimetry", "quantum_gravimetry", "rydberg", "rydberg_atom", "rydberg_rf", "quantum_rf"):
        # Nonlinear Optics in Photonic Crystals & Microcavity Laser Localization
        # 1. 2D Photonic Crystal Hexagonal Array of Dielectric Rods
        grid_start_x = cx - 360
        grid_end_x = cx + 360
        grid_start_y = cy - 200
        grid_end_y = cy + 200
        
        # Draw waveguide channel (missing row at cy)
        draw.rectangle([grid_start_x - 30, cy - 22, grid_end_x + 30, cy + 22], fill=(12, 22, 35), outline=(0, 160, 220), width=1)
        
        # Photonic bandgap dielectric lattice
        random.seed(532)
        for gx in range(grid_start_x, grid_end_x + 1, 36):
            for gy in range(grid_start_y, grid_end_y + 1, 32):
                # Offset every second column for hexagonal packing
                col_id = (gx - grid_start_x) // 36
                y_offset = 16 if (col_id % 2 == 1) else 0
                actual_y = gy + y_offset
                
                # Omit waveguide channel around cy
                if abs(actual_y - cy) < 26:
                    continue
                    
                # High-index silicon dielectric rod node
                draw.ellipse([gx - 7, actual_y - 7, gx + 7, actual_y + 7], fill=(10, 40, 60), outline=(0, 220, 255), width=2)
                # Core refractive index center
                draw.point((gx, actual_y), fill=(255, 255, 255))
        
        # 2. Central High-Q Point Defect Microcavity (Trapped Laser Mode)
        cavity_x = cx
        cavity_y = cy
        # Resonance standing wave interference ripples
        for cr in range(65, 8, -6):
            factor = (65 - cr) / 57.0
            col_r = int(255 * factor)
            col_g = int(210 * factor)
            draw.ellipse([cavity_x - cr, cavity_y - cr, cavity_x + cr, cavity_y + cr], outline=(col_r, col_g, 40), width=2)
        # Laser core
        draw.ellipse([cavity_x - 12, cavity_y - 12, cavity_x + 12, cavity_y + 12], fill=(255, 255, 255), outline=(255, 180, 40), width=2)
        
        # 3. Waveguide Propagation Beams: Fundamental Pump (1550nm) & Second Harmonic (775nm)
        # Input Fundamental Pump Beam (entering from left)
        draw.line([(grid_start_x - 40, cy), (cavity_x, cy)], fill=(0, 240, 255), width=4)
        draw.line([(grid_start_x - 40, cy - 6), (cavity_x, cy - 6)], fill=(0, 180, 220), width=1)
        draw.line([(grid_start_x - 40, cy + 6), (cavity_x, cy + 6)], fill=(0, 180, 220), width=1)
        
        # Output Frequency-Doubled Harmonic Beam (emerging to right)
        draw.line([(cavity_x, cy), (grid_end_x + 40, cy)], fill=(180, 70, 255), width=4)
        draw.line([(cavity_x, cy - 6), (grid_end_x + 40, cy - 6)], fill=(220, 120, 255), width=1)
        draw.line([(cavity_x, cy + 6), (grid_end_x + 40, cy + 6)], fill=(220, 120, 255), width=1)
        
        # Optical Annotations
        draw.text((grid_start_x - 30, cy - 42), "PUMP: 1550nm FUNDAMENTAL", fill=(0, 240, 255))
        draw.text((grid_end_x - 170, cy - 42), "SECOND HARMONIC: 775nm [SHG]", fill=(200, 100, 255))
        draw.text((cavity_x - 80, cy + 75), "HIGH-Q CAVITY: Q = 1.2 x 10^6", fill=(255, 210, 50))
        draw.text((cavity_x - 80, cy + 95), "NONLINEAR KERR PHASE SHIFT", fill=(255, 255, 255))
        
        # 4. Intelligence Side Panels: Sary-Shagan Laser Facility & Soviet Disinformation
        draw.rectangle([60, cy - 160, 280, cy - 70], fill=(10, 25, 35), outline=(0, 255, 240), width=1)
        draw.text((70, cy - 150), "[PHOTONIC BANDGAP DEFECT]", fill=(0, 255, 240))
        draw.text((70, cy - 130), "DIELECTRIC CONSTANT: ε = 11.9 (Si)", fill=(255, 220, 80))
        draw.text((70, cy - 110), "BANDGAP RATIO: Δω/ω_0 = 18.4%", fill=(200, 220, 255))
        draw.text((70, cy - 90), "SLOW-LIGHT GROUP VELOCITY: c/35", fill=(0, 240, 180))

        draw.rectangle([width - 320, cy - 160, width - 50, cy - 50], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, cy - 150), "[SARY-SHAGAN TERRA-3 DECEPTION]", fill=(255, 140, 50))
        draw.text((width - 310, cy - 130), "SOVIET ASAT LASER WEAPON THEATER", fill=(255, 200, 80))
        draw.text((width - 310, cy - 110), "EXAGGERATED HIGH-POWER CAPABILITY", fill=(255, 220, 120))
        draw.text((width - 310, cy - 90), "DIRECTORATE T DISINFORMATION", fill=(255, 80, 80))
        draw.text((width - 310, cy - 70), "STATUS: ARCHIVAL SIGINT REVEALED", fill=(200, 200, 200))

    elif theme in ("bec", "atom_interferometer", "atom_interferometry", "quantum_gravimeter", "gravimetric_mapping", "cold_atom"):
        # Bose-Einstein Condensate Atom Interferometry & Subterranean Gravimetric Void Mapping
        # 1. Subsurface Geological Density Stratification Grid
        for gy in range(cy - 120, height - 80, 30):
            pts = []
            for gx in range(60, width - 60, 20):
                g_wave = math.sin(gx * 0.01 + gy * 0.02) * 8.0
                pts.append((gx, gy + int(g_wave)))
            draw.line(pts, fill=(18, 30, 42), width=1)

        # 2. Vertical Atom Fountain Vacuum Column & Bragg Laser Pulses
        col_x = cx - 120
        col_w = 90
        draw.rectangle([col_x - col_w//2, 90, col_x + col_w//2, height - 90], fill=(10, 22, 35), outline=(0, 220, 255), width=2)
        draw.text((col_x - 42, 98), "VACUUM TUBE", fill=(0, 240, 255))
        draw.text((col_x - 38, 114), "10^-10 MBAR", fill=(120, 220, 255))

        # Three Horizontal Optical Raman/Bragg Pulses (π/2, π, π/2)
        pulse_positions = [
            (cy - 140, "π/2 SPLITTER PULSE (k_eff)"),
            (cy, "π MIRROR PULSE (INVERSION)"),
            (cy + 140, "π/2 RECOMBINER PULSE")
        ]
        for py, plabel in pulse_positions:
            # Laser beam line
            draw.line([(col_x - col_w//2 - 40, py), (col_x + col_w//2 + 40, py)], fill=(0, 255, 200), width=3)
            draw.line([(col_x - col_w//2 - 40, py), (col_x + col_w//2 + 40, py)], fill=(255, 255, 255), width=1)
            draw.text((col_x + col_w//2 + 48, py - 6), plabel, fill=(0, 255, 220))

        # Cold Matter Wave Trajectories (Two interfering atomic paths)
        pts_path_a = []
        pts_path_b = []
        for step in range(60):
            t_rel = step / 59.0
            y_curr = (cy - 140) + int(280 * t_rel)
            # Rhombus-like interferometer envelope
            sep = math.sin(t_rel * math.pi) * 28.0
            pts_path_a.append((col_x - int(sep), y_curr))
            pts_path_b.append((col_x + int(sep), y_curr))

        draw.line(pts_path_a, fill=(255, 200, 60), width=2)
        draw.line(pts_path_b, fill=(0, 240, 255), width=2)

        # Condensate Cloud Source (Rb-87 Condensate at top)
        draw.ellipse([col_x - 12, cy - 152, col_x + 12, cy - 128], fill=(0, 255, 240), outline=(255, 255, 255), width=2)
        draw.text((col_x - 48, cy - 170), "Rb-87 BEC (50 pK)", fill=(255, 240, 100))

        # 3. Subterranean Bunker Void / Gravimetric Anomaly (Right)
        void_x, void_y = cx + 240, cy + 60
        void_w, void_h = 180, 110
        # Hardened bunker structure outline
        draw.rectangle([void_x - void_w//2, void_y - void_h//2, void_x + void_w//2, void_y + void_h//2], fill=(25, 14, 18), outline=(255, 80, 60), width=2)
        draw.text((void_x - 70, void_y - 45), "[SUBTERRANEAN BUNKER VOID]", fill=(255, 100, 80))
        draw.text((void_x - 70, void_y - 25), "MASS DEFICIT: -1.4 x 10^7 KG", fill=(255, 200, 80))
        draw.text((void_x - 70, void_y + 15), "DEPTH: 48M BURIED // REINFORCED", fill=(200, 200, 200))
        draw.text((void_x - 70, void_y + 35), "GRAVITY GRADIENT: Δg = -14.2 EÖTVÖS", fill=(255, 60, 60))

        # Gravity anomaly gradient arrows converging on deficit
        for deg in range(0, 360, 45):
            rad = math.radians(deg)
            ax1 = void_x + int(math.cos(rad) * 130)
            ay1 = void_y + int(math.sin(rad) * 90)
            ax2 = void_x + int(math.cos(rad) * 105)
            ay2 = void_y + int(math.sin(rad) * 70)
            draw.line([(ax1, ay1), (ax2, ay2)], fill=(255, 120, 50), width=2)

        # 4. Telemetry Sidebars
        # Left Box: Quantum Interferometer Sensor Specs
        draw.rectangle([60, cy - 200, 290, cy - 90], fill=(12, 24, 38), outline=(0, 220, 255), width=1)
        draw.text((70, cy - 190), "[QUANTUM GRAVIMETRY TELEMETRY]", fill=(0, 240, 255))
        draw.text((70, cy - 170), "PHASE: ΔΦ = k_eff · g · T^2", fill=(255, 220, 100))
        draw.text((70, cy - 150), "SENSITIVITY: 10^-9 m/s^2 / √Hz", fill=(0, 255, 200))
        draw.text((70, cy - 130), "REPETITION: 2.0 Hz CONTINUOUS", fill=(200, 220, 255))
        draw.text((70, cy - 110), "DRIFT: ZERO ABSOLUTE CALIBRATION", fill=(0, 255, 220))

        # Right Box: Soviet Non-Acoustic ASW & Submarine Detection Dossier
        draw.rectangle([width - 320, cy - 200, width - 60, cy - 90], fill=(25, 18, 12), outline=(255, 140, 40), width=1)
        draw.text((width - 310, cy - 190), "[SOVIET NON-ACOUSTIC ASW]", fill=(255, 160, 50))
        draw.text((width - 310, cy - 170), "PROJECT SOKOL-K // WAKE DETECTION", fill=(255, 200, 80))
        draw.text((width - 310, cy - 150), "MAGNETIC & DENSITY ANOMALY DETECTOR", fill=(255, 100, 80))
        draw.text((width - 310, cy - 130), "SUBMARINE DISPLACEMENT TRACKING", fill=(255, 220, 120))
        draw.text((width - 310, cy - 110), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("pear_reg", "cognitive_field", "anomalous_entanglement", "field_reg"):
        # Princeton PEAR Laboratory Quantum Noise REG & Field Consciousness Network
        # 1. Statistical Random Walk Coordinates & Parabolic Sigma Envelopes
        chart_left = cx - 380
        chart_right = cx + 380
        chart_top = cy - 180
        chart_bot = cy + 180
        
        # Grid lines and zero expectation baseline
        draw.rectangle([chart_left, chart_top, chart_right, chart_bot], fill=(8, 16, 26), outline=(20, 60, 90), width=1)
        draw.line([(chart_left, cy), (chart_right, cy)], fill=(0, 180, 220), width=2)
        draw.text((chart_left + 15, cy - 18), "EXPECTATION BASELINE: μ = 0.00", fill=(0, 220, 255))
        
        # Parabolic Sigma Confidence Envelopes (±2σ 95%, ±3σ 99.7%)
        pts_p2, pts_m2 = [], []
        pts_p3, pts_m3 = [], []
        for x in range(chart_left, chart_right + 1, 10):
            n = (x - chart_left) / 10.0
            sigma = math.sqrt(n) * 8.5
            pts_p2.append((x, int(cy - 2 * sigma)))
            pts_m2.append((x, int(cy + 2 * sigma)))
            pts_p3.append((x, int(cy - 3 * sigma)))
            pts_m3.append((x, int(cy + 3 * sigma)))
            
        draw.line(pts_p2, fill=(30, 120, 160), width=1)
        draw.line(pts_m2, fill=(30, 120, 160), width=1)
        draw.line(pts_p3, fill=(180, 60, 60), width=1)
        draw.line(pts_m3, fill=(180, 60, 60), width=1)
        draw.text((chart_right - 90, pts_p2[-1][1] - 14), "+2σ (95%)", fill=(30, 160, 200))
        draw.text((chart_right - 90, pts_p3[-1][1] - 14), "+3σ (99.7%)", fill=(255, 80, 80))
        
        # 2. Cumulative Deviation Trace (Operator Intention Bias Trail)
        random.seed(914)
        walk_pts = []
        cur_y = float(cy)
        for x in range(chart_left, chart_right + 1, 6):
            # Intentional upward drift + quantum noise
            step = random.gauss(0.85, 2.8)
            cur_y -= step
            walk_pts.append((x, int(cur_y)))
            
        draw.line(walk_pts, fill=(255, 200, 50), width=3)
        draw.line(walk_pts, fill=(255, 255, 255), width=1)
        
        # Final terminal point and significance badge
        term_x, term_y = walk_pts[-1]
        draw.ellipse([term_x - 6, term_y - 6, term_x + 6, term_y + 6], fill=(255, 220, 50), outline=(255, 255, 255), width=2)
        draw.rectangle([term_x - 170, term_y - 45, term_x - 15, term_y + 5], fill=(35, 25, 10), outline=(255, 180, 40), width=1)
        draw.text((term_x - 160, term_y - 40), "CUMULATIVE DEVIATION", fill=(255, 220, 60))
        draw.text((term_x - 160, term_y - 22), "Z = 4.12 // p = 3.8 x 10^-5", fill=(255, 255, 255))
        draw.text((term_x - 160, term_y - 6), "NON-RANDOM BIAS DETECTED", fill=(0, 255, 220))

        # 3. Telemetry Sidebars: Noise Diode Apparatus & Soviet Psychic Disinformation
        draw.rectangle([60, cy - 160, 280, cy - 70], fill=(10, 25, 35), outline=(0, 255, 240), width=1)
        draw.text((70, cy - 150), "[PEAR NOISE DIODE REG]", fill=(0, 255, 240))
        draw.text((70, cy - 130), "SOLID-STATE SHOT NOISE SOURCE", fill=(255, 220, 80))
        draw.text((70, cy - 110), "SAMPLE RATE: 1,000 BITS/SEC", fill=(200, 220, 255))
        draw.text((70, cy - 90), "OPERATOR INTENTION COUPLING", fill=(0, 240, 180))

        draw.rectangle([width - 320, cy + 50, width - 50, cy + 160], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, cy + 60), "[KGB PSYCHOTRONICS DOSSIER]", fill=(255, 140, 50))
        draw.text((width - 310, cy + 80), "BIO-INFORMATION BLACK BUDGET", fill=(255, 200, 80))
        draw.text((width - 310, cy + 100), "FABRICATED TELEPATHY CLAIMS", fill=(255, 220, 120))
        draw.text((width - 310, cy + 120), "PURPOSE: SLUSH FUND DIVERSION", fill=(255, 80, 80))
        draw.text((width - 310, cy + 140), "STATUS: DISCLOSURE BY SHVETS", fill=(200, 200, 200))

    elif theme in ("transmon_qubit", "surface_code", "quantum_cryptanalysis", "fault_tolerant_qc", "jpa", "quantum_amplifier", "squeezed_vacuum", "cat_state", "parity_measurement", "quantum_error_correction"):
        # Superconducting Transmon Qubits & Surface Code Fault-Tolerance
        # 1. Planar 2D Surface Code Lattice Grid
        grid_origin_x = cx - 280
        grid_origin_y = cy - 180
        spacing = 70
        
        # Plaquette colored faces (Z-plaquettes in emerald, X-plaquettes in amber)
        for r in range(5):
            for c in range(7):
                px = grid_origin_x + c * spacing
                py = grid_origin_y + r * spacing
                is_x = ((r + c) % 2 == 0)
                plaq_col = (25, 45, 30) if is_x else (45, 30, 20)
                draw.rectangle([px, py, px + spacing, py + spacing], fill=plaq_col, outline=(20, 50, 70), width=1)
                
                # Plaquette center ancilla stabilizer node
                mid_x = px + spacing // 2
                mid_y = py + spacing // 2
                anc_col = (255, 140, 50) if is_x else (30, 240, 160)
                draw.ellipse([mid_x - 8, mid_y - 8, mid_x + 8, mid_y + 8], fill=(10, 20, 30), outline=anc_col, width=2)
                anc_type = "X" if is_x else "Z"
                draw.text((mid_x - 4, mid_y - 7), anc_type, fill=anc_col)
                
                # Coupler entangling lines connecting ancilla to 4 surrounding data vertices
                for dx, dy in [(-spacing//2, -spacing//2), (spacing//2, -spacing//2), (-spacing//2, spacing//2), (spacing//2, spacing//2)]:
                    draw.line([(mid_x, mid_y), (mid_x + dx, mid_y + dy)], fill=(0, 140, 180), width=1)

        # 2. Data Qubits at Vertices (Rotated transmon capacitor pads with Josephson junctions)
        for r in range(6):
            for c in range(8):
                vx = grid_origin_x + c * spacing
                vy = grid_origin_y + r * spacing
                
                # Transmon Data Qubit (Diamond Pad)
                draw.polygon([
                    (vx, vy - 9),
                    (vx + 9, vy),
                    (vx, vy + 9),
                    (vx - 9, vy)
                ], fill=(10, 35, 55), outline=(0, 240, 255), width=2)
                
                # Josephson Junction indicator (crossed box in center)
                draw.rectangle([vx - 3, vy - 3, vx + 3, vy + 3], outline=(255, 220, 80), width=1)
                draw.point((vx, vy), fill=(255, 255, 255))

        # Annotations on Surface Code
        draw.text((grid_origin_x, grid_origin_y - 28), "ROTATED SURFACE CODE LATTICE (d = 7 FAULT-TOLERANT)", fill=(0, 255, 240))
        draw.text((grid_origin_x, grid_origin_y + 5 * spacing + 15), "PHYSICAL DATA TRANSMONS (CYAN) // ANCILLA SYNDROME READOUT (ORANGE/GREEN)", fill=(0, 220, 200))

        # 3. Dilution Refrigerator Telemetry & 8th Chief Cryptanalysis Dossier
        draw.rectangle([60, cy - 160, 250, cy - 60], fill=(10, 25, 40), outline=(0, 255, 240), width=1)
        draw.text((70, cy - 150), "[DILUTION CRYOSTAT]", fill=(0, 255, 240))
        draw.text((70, cy - 130), "MIXING CHAMBER: 14.8 mK", fill=(120, 220, 255))
        draw.text((70, cy - 110), "COHERENCE T1: 118 μs", fill=(255, 220, 80))
        draw.text((70, cy - 90), "DEPHASING T2*: 94 μs", fill=(0, 240, 180))
        draw.text((70, cy - 70), "TWO-LEVEL LOSS: Q_i = 1.8M", fill=(200, 200, 200))

        draw.rectangle([width - 320, cy - 160, width - 50, cy - 40], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, cy - 150), "[SOVIET 8TH CHIEF SIGINT]", fill=(255, 140, 50))
        draw.text((width - 310, cy - 130), "HARVEST-NOW DECRYPT-LATER", fill=(255, 200, 80))
        draw.text((width - 310, cy - 110), "TARGET: RSA-2048 / ECC-256", fill=(255, 220, 120))
        draw.text((width - 310, cy - 90), "EXFILTRATION: FIBER SPLICE", fill=(255, 80, 80))
        draw.text((width - 310, cy - 70), "POST-QUANTUM MIGRATION REQ", fill=(200, 200, 200))
        draw.text((width - 310, cy - 50), "STATUS: SHVETS DISCLOSURE", fill=(0, 255, 220))

    elif theme in ("gateway_hemisync", "hemisync", "monroe_gateway", "binaural_beat", "binaural_ffr", "eeg_microstates", "ffr", "telepathy_disinfo"):
        # Robert Monroe Gateway Hemi-Sync & Soviet Psychotronic Telemetry
        # 1. Background EEG frequency spectral grid
        for gy in range(cy - 220, cy + 220, 30):
            draw.line([(60, gy), (width - 60, gy)], fill=(12, 25, 40), width=1)
        for gx in range(60, width - 60, 50):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(12, 25, 40), width=1)

        # 2. Dual Binaural Waves & Amplitude Modulated Envelope (Hemi-Sync)
        # Left channel (100 Hz Carrier, Cyan), Right channel (104 Hz Carrier, Amber)
        left_pts = []
        right_pts = []
        beat_pts = []
        env_top = []
        env_bot = []

        w_start, w_end = 80, width - 80
        for px in range(w_start, w_end, 2):
            t = (px - w_start) / (w_end - w_start) * 12.0 * math.pi
            # Left carrier (cyan)
            yl = (cy - 40) + math.sin(t * 1.00) * 35.0
            left_pts.append((px, yl))
            # Right carrier (amber)
            yr = (cy - 40) + math.sin(t * 1.04) * 35.0
            right_pts.append((px, yr))
            # Beat wave (superposition)
            carrier = math.sin(t * 1.02)
            envelope = math.cos(t * 0.04)
            yb = (cy + 110) + (carrier * envelope) * 55.0
            beat_pts.append((px, yb))
            env_top.append((px, (cy + 110) - abs(envelope) * 55.0))
            env_bot.append((px, (cy + 110) + abs(envelope) * 55.0))

        # Draw carrier waveforms
        if len(left_pts) > 1:
            draw.line(left_pts, fill=(0, 220, 255), width=2)
        if len(right_pts) > 1:
            draw.line(right_pts, fill=(255, 180, 50), width=2)

        # Draw modulated beat envelope (Theta frequency following response)
        if len(env_top) > 1:
            draw.line(env_top, fill=(160, 100, 240), width=1)
            draw.line(env_bot, fill=(160, 100, 240), width=1)
        if len(beat_pts) > 1:
            draw.line(beat_pts, fill=(220, 140, 255), width=3)

        # Channel labels
        draw.text((w_start, cy - 90), "LEFT AUDIO: 100.0 Hz CARRIER [CYAN]", fill=(0, 220, 255))
        draw.text((w_start + 320, cy - 90), "RIGHT AUDIO: 104.0 Hz CARRIER [AMBER]", fill=(255, 180, 50))
        draw.text((w_start, cy + 35), "HEMI-SYNC SUPERIOR OLIVARY NUCLEUS: 4.0 Hz THETA BEAT ENVELOPE [PURPLE]", fill=(220, 140, 255))

        # 3. Brainwave Coherence Telemetry Dossier & Soviet Psychotronics
        # Left HUD Box: Gateway Experience Protocol
        draw.rectangle([60, 90, 310, cy - 110], fill=(15, 10, 25), outline=(180, 100, 240), width=1)
        draw.text((70, 98), "[MONROE GATEWAY INTERFACE]", fill=(200, 140, 255))
        draw.text((70, 118), "STATE: FOCUS 12 (EXPANDED)", fill=(255, 220, 100))
        draw.text((70, 138), "HEMISPHERIC SYNC: 98.4%", fill=(0, 255, 200))
        draw.text((70, 158), "FREQ RESPONSE: 4.0 Hz THETA", fill=(180, 140, 255))
        draw.text((70, 178), "PHASE CONJUGATION: LOCKED", fill=(100, 220, 255))
        draw.text((70, 198), "CIA ARCHIVE: IR-83-0001", fill=(200, 200, 200))

        # Right HUD Box: Soviet Psychotronic Telemetry & Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 110], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET PSYCHOTRONIC LAB]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "FACILITY: KIEV / NOVOSIBIRSK", fill=(255, 200, 80))
        draw.text((width - 310, 138), "RESEARCH: BIO-RESONANCE EW", fill=(255, 100, 80))
        draw.text((width - 310, 158), "REMOTE VIEW: ENCRYPTED SITE", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SLUSH FUNDING: UNRESTRICTED", fill=(255, 60, 60))
        draw.text((width - 310, 198), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("p300_biometrics", "neuro_telemetry", "eeg_p300", "cognitive_load", "hft_neuro_feedback", "neuro_feedback", "trading_biometrics", "reflex_modification", "focused_ultrasound", "ultrasound_neuromodulation", "sonoporation", "neuro_sonics"):
        # Real-Time EEG P300 Biometrics & Neuro-Adaptive Cognitive Load Telemetry
        # 1. Background Event-Related Potential (ERP) Coordinate Grid
        grid_left = cx - 360
        grid_right = cx + 360
        grid_top = cy - 160
        grid_bot = cy + 160
        draw.rectangle([grid_left, grid_top, grid_right, grid_bot], fill=(8, 16, 26), outline=(20, 60, 90), width=1)
        
        # Zero microvolt baseline and stimulus onset marker (t = 0 ms)
        draw.line([(grid_left, cy), (grid_right, cy)], fill=(0, 180, 220), width=2)
        draw.text((grid_left + 15, cy - 18), "BASELINE: 0.0 μV", fill=(0, 220, 255))
        
        stim_x = grid_left + 120
        draw.line([(stim_x, grid_top), (stim_x, grid_bot)], fill=(255, 220, 60), width=2)
        draw.text((stim_x + 8, grid_top + 10), "STIMULUS ONSET [t = 0 ms]", fill=(255, 220, 80))

        # 2. ERP Waveform Curves: Standard Non-Target (Cyan) vs P300 Target Recognition Spike (Amber/Crimson)
        non_target_pts = []
        target_pts = []
        for px in range(stim_x, grid_right + 1, 4):
            t_ms = (px - stim_x) / float(grid_right - stim_x) * 800.0  # 0 to 800ms
            y_std = cy - 12.0 * math.sin(t_ms * 0.02) * math.exp(-t_ms * 0.005)
            non_target_pts.append((px, int(y_std)))
            
            p300_amp = 75.0 * math.exp(-((t_ms - 320.0) / 70.0)**2)
            y_tar = cy - (12.0 * math.sin(t_ms * 0.02) + p300_amp)
            target_pts.append((px, int(y_tar)))

        draw.line(non_target_pts, fill=(0, 160, 200), width=2)
        draw.line(target_pts, fill=(255, 80, 60), width=3)
        draw.line(target_pts, fill=(255, 220, 80), width=1)

        # P300 Peak callout
        p300_x = stim_x + int(320.0 / 800.0 * (grid_right - stim_x))
        p300_y = cy - 75
        draw.ellipse([p300_x - 6, p300_y - 6, p300_x + 6, p300_y + 6], fill=(255, 255, 255), outline=(255, 60, 60), width=2)
        draw.rectangle([p300_x - 140, p300_y - 50, p300_x - 15, p300_y - 10], fill=(30, 15, 20), outline=(255, 80, 60), width=1)
        draw.text((p300_x - 130, p300_y - 45), "P300 ERP PEAK (+16.4 μV)", fill=(255, 100, 80))
        draw.text((p300_x - 130, p300_y - 28), "SUB-CONSCIOUS TARGET HIT", fill=(255, 220, 60))

        # 3. 10-20 Electrode Scalp Topography Diagram (Left)
        scalp_cx, scalp_cy = cx - 440, cy
        scalp_r = 55
        draw.ellipse([scalp_cx - scalp_r, scalp_cy - scalp_r, scalp_cx + scalp_r, scalp_cy + scalp_r], outline=(0, 240, 255), width=2)
        draw.line([(scalp_cx - 8, scalp_cy - scalp_r), (scalp_cx, scalp_cy - scalp_r - 12), (scalp_cx + 8, scalp_cy - scalp_r)], fill=(0, 240, 255), width=2)
        electrodes = [
            (scalp_cx, scalp_cy - 30, "Fz"),
            (scalp_cx, scalp_cy, "Cz"),
            (scalp_cx, scalp_cy + 30, "Pz*"),
            (scalp_cx, scalp_cy + 45, "Oz")
        ]
        for ex, ey, elabel in electrodes:
            col_e = (255, 60, 60) if "Pz" in elabel else (0, 220, 255)
            draw.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=col_e)
            draw.text((ex + 8, ey - 6), elabel, fill=col_e)

        # 4. Telemetry Sidebars
        # Left Box: Cognitive Load Index
        draw.rectangle([60, 90, 310, cy - 110], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[COGNITIVE LOAD TELEMETRY]", fill=(0, 240, 255))
        draw.text((70, 118), "THETA/BETA RATIO: 4.82 [HIGH]", fill=(255, 220, 100))
        draw.text((70, 138), "PUPIL DILATION: +1.8mm (OVERLOAD)", fill=(255, 140, 50))
        draw.text((70, 158), "MICROSTATE DURA: 74 ms [FRAGMENT]", fill=(255, 80, 80))
        draw.text((70, 178), "TARGET DETECTION CONF: 99.1%", fill=(0, 255, 200))

        # Right Box: Soviet Bio-Information Dossier
        draw.rectangle([width - 320, 90, width - 60, cy - 110], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[KGB BIO-INFORMATION AUDIT]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "REFLEXIVE CONTROL // COGNITIVE HACK", fill=(255, 200, 80))
        draw.text((width - 310, 138), "INVOLUNTARY RECOGNITION EXPLOIT", fill=(255, 100, 80))
        draw.text((width - 310, 158), "PILOT FATIGUE WEAPONIZATION", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("defense_cloud_fisa", "fisa_702", "cloud_lobbying", "jwcc"):
        # Silicon Valley Defense Cloud Lobbying & FISA 702 Warrantless Surveillance
        # 1. Hyperscale Datacenter Server Racks (JWCC Multi-Cloud Architecture)
        rack_y = cy - 120
        rack_h = 240
        rack_w = 110
        racks = [
            (cx - 380, "AWS SECRET"),
            (cx - 240, "AZURE GOV"),
            (cx - 100, "GCP CLOUD"),
            (cx + 40, "ORACLE IC"),
            (cx + 180, "NSA UPSTREAM"),
            (cx + 320, "FISA 702 REPO")
        ]

        for rx, rlabel in racks:
            # Server chassis rack
            draw.rectangle([rx, rack_y, rx + rack_w, rack_y + rack_h], fill=(12, 18, 28), outline=(0, 180, 240), width=2)
            draw.text((rx + 8, rack_y + 8), rlabel, fill=(0, 240, 255))
            
            # Server blade units (individual 2U server slots)
            for s_idx in range(9):
                by = rack_y + 30 + s_idx * 22
                draw.rectangle([rx + 4, by, rx + rack_w - 4, by + 18], fill=(18, 28, 42), outline=(30, 60, 90), width=1)
                # LED activity array (green/cyan/amber)
                for led_i in range(5):
                    lx = rx + 12 + led_i * 10
                    ly = by + 9
                    col_led = (0, 255, 180) if (s_idx + led_i) % 2 == 0 else (255, 180, 50)
                    draw.point((lx, ly), fill=col_led)
                # Blade slot ID
                draw.text((rx + 68, by + 4), f"U-{s_idx+1}", fill=(100, 160, 200))

        # 2. Optical Fiber Backbones & FISA 702 Optical Splitter Beam
        fiber_y = cy + 150
        draw.line([(60, fiber_y), (width - 60, fiber_y)], fill=(0, 220, 255), width=4)
        draw.line([(60, fiber_y), (width - 60, fiber_y)], fill=(255, 255, 255), width=1)
        draw.text((70, fiber_y + 10), "COMMERCIAL TRANSIT FIBER TRUNK [100G DWDM]", fill=(0, 220, 255))

        # Optical Splitter Prism (Room 641A Style Beam Splitter)
        tap_x = cx + 80
        draw.polygon([(tap_x - 16, fiber_y - 20), (tap_x + 16, fiber_y - 20), (tap_x, fiber_y + 20)], fill=(30, 40, 60), outline=(255, 80, 60), width=2)
        draw.text((tap_x - 45, fiber_y - 38), "FISA 702 BEAM SPLITTER", fill=(255, 90, 70))

        # 10% Interception Tap Line diverted straight into NSA Upstream / FISA Repo rack
        tap_pts = [(tap_x, fiber_y), (tap_x, fiber_y - 70), (cx + 230, rack_y + rack_h), (cx + 230, rack_y + 120)]
        draw.line(tap_pts, fill=(255, 60, 50), width=3)
        draw.text((cx + 120, fiber_y - 45), "WARRANTLESS INTERCEPTION TAP (10% DIVERTER)", fill=(255, 80, 60))

        # 3. Silicon Valley Lobbying & KGB OTU Telecommunications Wiretap Dossiers
        # Left HUD Box: Defense Cloud Lobbying Flow
        draw.rectangle([60, 90, 310, cy - 140], fill=(15, 20, 30), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[DEFENSE CLOUD LOBBYING]", fill=(0, 240, 255))
        draw.text((70, 118), "PROGRAM: JWCC ($9.0 BILLION)", fill=(255, 220, 100))
        draw.text((70, 138), "TECH CARTEL: BIG 4 ALLIANCE", fill=(0, 255, 200))
        draw.text((70, 158), "K STREET PAC CONTRIBS: $48M", fill=(255, 140, 50))
        draw.text((70, 178), "REVOLVING DOOR: SECDEF ADVISORS", fill=(255, 80, 80))

        # Right HUD Box: FISA 702 & KGB OTU Surveillance Lineage
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 15), outline=(255, 80, 60), width=1)
        draw.text((width - 310, 98), "[SURVEILLANCE LINEAGE]", fill=(255, 100, 70))
        draw.text((width - 310, 118), "FISA 702 BACKDOOR SEARCHES", fill=(255, 200, 80))
        draw.text((width - 310, 138), "US PERSON QUERIES: 278,000+", fill=(255, 60, 60))
        draw.text((width - 310, 158), "KGB 12TH DEPT OTU LINEAGE", fill=(255, 160, 50))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DISCLOSURE", fill=(0, 255, 220))

    elif theme in ("quantum_annealing", "flux_qubit", "adiabatic_quantum", "ising_spin", "fluxonium_qubit", "fluxonium", "phase_slip"):
        # Quantum Annealing, Superconducting Flux Qubits & Adiabatic Ground State Trajectories
        # 1. Background Adiabatic Energy Landscape (Non-convex potential with tunneling valleys)
        for gy in range(cy - 220, cy + 220, 25):
            pts = []
            for gx in range(60, width - 60, 8):
                # Double-well potential with multiple local minima
                x_norm = (gx - cx) / 220.0
                pot = (x_norm**4 - 2.2 * x_norm**2 + 0.3 * math.sin(x_norm * 8.0)) * 25.0
                pts.append((gx, gy + int(pot * 0.4)))
            if len(pts) > 1:
                draw.line(pts, fill=(15, 30, 48), width=1)

        # 2. Superconducting Flux Qubit Lattice (Chimera / Pegasus Cross-Coupled Loops)
        lattice_ox = cx - 180
        lattice_oy = cy - 140
        unit_spacing = 90

        # Draw 4x4 array of coupled flux loops
        for row in range(4):
            for col in range(5):
                qx = lattice_ox + col * unit_spacing
                qy = lattice_oy + row * unit_spacing

                # Horizontal Flux Qubit Loop (Cyan)
                draw.rounded_rectangle([qx - 36, qy - 10, qx + 36, qy + 10], radius=4, fill=(10, 28, 45), outline=(0, 220, 255), width=2)
                # Vertical Flux Qubit Loop (Gold/Amber)
                draw.rounded_rectangle([qx - 10, qy - 36, qx + 10, qy + 36], radius=4, fill=(25, 20, 12), outline=(255, 180, 50), width=2)

                # Center Josephson Junction RF-SQUID coupler loop
                draw.rectangle([qx - 4, qy - 4, qx + 4, qy + 4], fill=(255, 255, 255), outline=(0, 255, 200), width=1)
                
                # Coupler weight links (J_ij)
                if col < 4:
                    draw.line([(qx + 36, qy), (qx + unit_spacing - 36, qy)], fill=(0, 160, 200), width=1)
                if row < 3:
                    draw.line([(qx, qy + 36), (qx, qy + unit_spacing - 36)], fill=(200, 140, 40), width=1)

        draw.text((lattice_ox - 10, lattice_oy - 30), "SUPERCONDUCTING FLUX QUBIT LATTICE // TUNABLE RF-SQUID COUPLERS", fill=(0, 255, 240))

        # 3. Quantum Tunneling Path Trajectory (Adiabatic Shortcut avoiding Energy Gap)
        tunnel_pts = []
        for step in range(80):
            prog = step / 80.0
            tx = 80 + int(prog * (width - 160))
            # Trajectory tunneling across the energy landscape
            ty = cy + 130 - int(math.sin(prog * 5.0 * math.pi) * 35.0 * math.exp(-prog * 1.5))
            tunnel_pts.append((tx, ty))
        
        if len(tunnel_pts) > 1:
            draw.line(tunnel_pts, fill=(180, 100, 255), width=3)
            # Glowing ground-state convergence point
            gx_end, gy_end = tunnel_pts[-1]
            draw.ellipse([gx_end - 8, gy_end - 8, gx_end + 8, gy_end + 8], fill=(255, 255, 255), outline=(180, 100, 255), width=2)
            draw.text((gx_end - 120, gy_end + 12), "GLOBAL MINIMUM GROUND STATE", fill=(200, 160, 255))

        # 4. Telemetry Dossiers (Annealer & Soviet Cryogenic Supercomputing)
        # Left HUD Box: Annealer QPU Telemetry
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[QUANTUM ANNEALER QPU]", fill=(0, 240, 255))
        draw.text((70, 118), "ARCH: PEGASUS P16 (5,640 Q)", fill=(255, 220, 100))
        draw.text((70, 138), "ANNEAL TIME: 20.0 μs", fill=(0, 255, 200))
        draw.text((70, 158), "DILUTION TEMP: 11.2 mK", fill=(120, 220, 255))
        draw.text((70, 178), "ENERGY GAP: Δ_min = 4.2 GHz", fill=(255, 140, 50))

        # Right HUD Box: Soviet 8th Chief Cryogenic Cryptanalysis
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET 8TH CHIEF CIPHER]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "CRYOGENIC JOSEPHSON ARRAYS", fill=(255, 200, 80))
        draw.text((width - 310, 138), "ISINC GRAPH DECOMPOSITION", fill=(255, 100, 80))
        draw.text((width - 310, 158), "NP-HARD CIPHER CONVERGENCE", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("optomechanics", "drum_resonator", "mechanical_resonator", "optomechanical_entanglement", "quantum_drum"):
        # Macroscopic Quantum Entanglement in Mechanical Drum Resonators
        # 1. Background laser interferometry grid & cavity mode lines
        for gy in range(cy - 220, cy + 220, 25):
            draw.line([(60, gy), (width - 60, gy)], fill=(10, 24, 38), width=1)
        for gx in range(60, width - 60, 45):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(10, 24, 38), width=1)

        # 2. Optical Fabry-Perot Cavity Laser Axis (Horizontal circulating beam)
        laser_y = cy
        beam_glow_pts = []
        for x in range(80, width - 80, 4):
            # Standing wave optical intensity envelope
            env = math.sin((x - 80) * 0.08) * 6.0
            beam_glow_pts.append((x, laser_y + env))
        draw.line(beam_glow_pts, fill=(0, 180, 220), width=4)
        draw.line([(80, laser_y), (width - 80, laser_y)], fill=(255, 255, 255), width=1)

        # Cavity coupling mirrors
        for mx in [cx - 280, cx + 280]:
            draw.rectangle([mx - 6, cy - 70, mx + 6, cy + 70], fill=(20, 45, 65), outline=(0, 240, 255), width=2)
            draw.text((mx - 25, cy - 88), "MIRROR R=99.99%", fill=(100, 220, 255))

        # 3. Dual Macroscopic Drum Resonators (Micro-fabricated Al Membranes)
        drums = [
            (cx - 140, "DRUM RESONATOR A [10.4 MHz]"),
            (cx + 140, "DRUM RESONATOR B [10.4 MHz]")
        ]

        for dx, dlabel in drums:
            # Outer silicon substrate frame
            draw.rectangle([dx - 80, cy - 80, dx + 80, cy + 80], fill=(12, 22, 34), outline=(40, 80, 110), width=2)
            # Membrane anchor suspension cross-beams
            draw.line([(dx - 78, cy), (dx + 78, cy)], fill=(0, 160, 200), width=2)
            draw.line([(dx, cy - 78), (dx, cy + 78)], fill=(0, 160, 200), width=2)
            
            # Vibrating Drum Membrane (Concentric acoustic mode contours)
            for r, col in [(52, (20, 60, 90)), (40, (0, 180, 220)), (28, (0, 240, 255)), (14, (200, 255, 255))]:
                draw.ellipse([dx - r, cy - r, dx + r, cy + r], outline=col, width=2)
            
            # Drum center displacement node
            draw.ellipse([dx - 5, cy - 5, dx + 5, cy + 5], fill=(255, 255, 255))
            draw.text((dx - 70, cy + 90), dlabel, fill=(0, 240, 255))

        # 4. Macroscopic Entanglement Bridge (Two-Mode Squeezing Correlation Waves)
        entangle_pts = []
        for ex in range(cx - 140, cx + 140, 3):
            # Phase-locked entangled phonon trajectory
            t = (ex - (cx - 140)) / 280.0 * 6.0 * math.pi
            ey = cy + math.sin(t) * 28.0 * (1.0 - abs(ex - cx) / 160.0)
            entangle_pts.append((ex, ey))
        if len(entangle_pts) > 1:
            draw.line(entangle_pts, fill=(180, 100, 255), width=3)
        draw.text((cx - 130, cy - 35), "EPR ENTANGLEMENT LINK // E_N = 0.54", fill=(220, 160, 255))

        # 5. Balanced Homodyne Detector (Bottom Center)
        bs_y = cy + 150
        draw.polygon([(cx - 16, bs_y - 16), (cx + 16, bs_y - 16), (cx, bs_y + 16)], fill=(20, 35, 55), outline=(0, 240, 255), width=2)
        draw.line([(cx, cy), (cx, bs_y)], fill=(0, 200, 240), width=2)
        draw.text((cx - 85, bs_y + 22), "BALANCED HOMODYNE DETECTOR", fill=(0, 255, 220))

        # 6. Telemetry Dossiers (Optomechanics & Soviet Laser Espionage)
        # Left HUD Box: Macroscopic Optomechanics Telemetry
        draw.rectangle([60, 90, 310, cy - 120], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[MACROSCOPIC DRUM TELEMETRY]", fill=(0, 240, 255))
        draw.text((70, 118), "MEMBRANE: 15μm Al ON SiN", fill=(255, 220, 100))
        draw.text((70, 138), "MECH FREQ: Ω_m = 10.4 MHz", fill=(0, 255, 200))
        draw.text((70, 158), "COOLING: 0.18 PHONONS", fill=(120, 220, 255))
        draw.text((70, 178), "PHASE NOISE: -142 dBc/Hz", fill=(255, 140, 50))
        draw.text((70, 198), "ENTANGLEMENT: E_N = 0.54", fill=(180, 140, 255))

        # Right HUD Box: Soviet Laser Espionage & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 120], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET LASER ESPIONAGE]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "FACILITY: LEBEDEV PHYSICAL INST", fill=(255, 200, 80))
        draw.text((width - 310, 138), "TARGET: LASER INTERFEROMETRY", fill=(255, 100, 80))
        draw.text((width - 310, 158), "LINE X MILITARY SMUGGLING", fill=(255, 220, 120))
        draw.text((width - 310, 178), "DEEP ASW ACOUSTIC DETECTORS", fill=(255, 60, 60))
        draw.text((width - 310, 198), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("cv_qkd", "continuous_variable_qkd", "gaussian_modulation", "fiber_qkd"):
        # Continuous-Variable Quantum Key Distribution (CV-QKD) & Gaussian Modulation
        # 1. Background optical transit grid
        for gy in range(cy - 220, cy + 220, 25):
            draw.line([(60, gy), (width - 60, gy)], fill=(10, 24, 38), width=1)
        for gx in range(60, width - 60, 45):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(10, 24, 38), width=1)

        # 2. Phase Space Gaussian Quadrature Distribution (Alice's Modulation, Center-Left)
        ps_cx, ps_cy = cx - 140, cy
        # Coordinate axes (x and p quadratures)
        draw.line([(ps_cx - 120, ps_cy), (ps_cx + 120, ps_cy)], fill=(0, 180, 220), width=1)
        draw.line([(ps_cx, ps_cy - 120), (ps_cx, ps_cy + 120)], fill=(0, 180, 220), width=1)
        draw.text((ps_cx + 95, ps_cy + 6), "x_A", fill=(0, 240, 255))
        draw.text((ps_cx + 6, ps_cy - 115), "p_A", fill=(0, 240, 255))

        # Concentric Gaussian Wigner distribution variance rings
        for vr, alpha_v in [(100, 20), (75, 45), (50, 75), (25, 120)]:
            draw.ellipse([ps_cx - vr, ps_cy - vr, ps_cx + vr, ps_cy + vr], outline=(0, alpha_v, int(alpha_v * 1.5)), width=1)

        # Gaussian-modulated coherent state constellation (Alice's random quad samples)
        random.seed(912)
        for _ in range(48):
            # Box-Muller Gaussian random coordinates
            u1, u2 = random.random(), random.random()
            z0 = math.sqrt(-2.0 * math.log(max(u1, 1e-9))) * math.cos(2.0 * math.pi * u2)
            z1 = math.sqrt(-2.0 * math.log(max(u1, 1e-9))) * math.sin(2.0 * math.pi * u2)
            kx = ps_cx + int(z0 * 28.0)
            ky = ps_cy + int(z1 * 28.0)
            # Shot-noise uncertainty disc
            draw.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=(10, 35, 55), outline=(0, 255, 240), width=1)
            draw.point((kx, ky), fill=(255, 255, 255))

        draw.text((ps_cx - 100, ps_cy + 130), "GAUSSIAN MODULATED PHASE SPACE // V_A = 4.5 SNU", fill=(0, 255, 240))

        # 3. Optical Fiber Backbone & Eavesdropping Tap Attempt (Center-Right)
        fiber_y = cy - 20
        # Telecom single-mode fiber core (1550nm)
        draw.line([(cx - 10, fiber_y), (width - 70, fiber_y)], fill=(0, 200, 255), width=4)
        draw.line([(cx - 10, fiber_y), (width - 70, fiber_y)], fill=(255, 255, 255), width=1)
        draw.text((cx + 10, fiber_y - 20), "1550nm TELECOM SMF-28 FIBER", fill=(0, 220, 255))

        # Micro-bend cable tap pod (Soviet 8th Chief interception attempt)
        tap_x = cx + 120
        draw.polygon([(tap_x - 14, fiber_y - 18), (tap_x + 14, fiber_y - 18), (tap_x, fiber_y + 16)], fill=(30, 20, 25), outline=(255, 60, 40), width=2)
        draw.text((tap_x - 50, fiber_y - 34), "MICRO-BEND TAP POD", fill=(255, 80, 60))
        # Leakage flux vector diverted
        draw.line([(tap_x, fiber_y), (tap_x + 40, fiber_y + 50)], fill=(255, 80, 50), width=2)
        draw.text((tap_x + 45, fiber_y + 45), "EXCESS NOISE SPIKE: Δξ = +0.038", fill=(255, 100, 70))

        # 4. Bob's Balanced Homodyne Detector (Far Right)
        det_x = width - 120
        draw.rectangle([det_x - 20, fiber_y - 45, det_x + 20, fiber_y + 45], fill=(15, 30, 45), outline=(0, 255, 200), width=2)
        draw.text((det_x - 30, fiber_y + 55), "HOMODYNE DETECTOR", fill=(0, 255, 200))
        draw.text((det_x - 25, fiber_y + 70), "LOCAL OSCILLATOR", fill=(120, 220, 255))

        # 5. Telemetry Dossiers (CV-QKD Metrics & Soviet Cryptanalysis)
        # Left HUD Box: CV-QKD System Telemetry
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[CV-QKD TELEMETRY METRICS]", fill=(0, 240, 255))
        draw.text((70, 118), "MODULATION: GAUSSIAN COHERENT", fill=(255, 220, 100))
        draw.text((70, 138), "CARRIER: 1550nm DWDM CO-EXIST", fill=(0, 255, 200))
        draw.text((70, 158), "EXCESS NOISE: ξ = 0.003 SNU", fill=(120, 220, 255))
        draw.text((70, 178), "SECRET KEY: 12.4 Mbps @ 50KM", fill=(255, 140, 50))

        # Right HUD Box: Soviet 8th Chief Cryptanalysis & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET 8TH CHIEF SIGINT]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "TARGET: TELECOM FIBER TAP", fill=(255, 200, 80))
        draw.text((width - 310, 138), "LINE X ACQUISITION: HYBRIDS", fill=(255, 100, 80))
        draw.text((width - 310, 158), "HARVEST-NOW DECRYPT-LATER FAILS", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("red_sea_cables", "bab_el_mandeb", "houthi_cables", "subsea_cables"):
        # Bab el-Mandeb Subsea Telecommunications Cable Interdiction & Bathymetric Trench
        # 1. Background hydrographic grid & depth sounding lines
        for gy in range(cy - 220, cy + 220, 25):
            draw.line([(60, gy), (width - 60, gy)], fill=(8, 20, 32), width=1)
        for gx in range(60, width - 60, 45):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(8, 20, 32), width=1)

        # 2. Strait Coastlines & Bathymetric Shelves
        # West Coast (Djibouti / Ras Siyyan, Left)
        draw.polygon([(60, cy - 220), (cx - 240, cy - 140), (cx - 210, cy + 30), (cx - 280, cy + 220), (60, cy + 220)], fill=(12, 22, 28), outline=(60, 120, 140), width=2)
        draw.text((80, cy - 120), "DJIBOUTI / RAS SIYYAN", fill=(80, 160, 180))
        draw.text((80, cy - 100), "BAB EL-MANDEB WESTERN SHORE", fill=(60, 120, 140))

        # East Coast (Yemen / Ras Bab el-Mandeb, Right)
        draw.polygon([(width - 60, cy - 220), (cx + 240, cy - 160), (cx + 200, cy - 10), (cx + 270, cy + 220), (width - 60, cy + 220)], fill=(24, 16, 14), outline=(160, 90, 60), width=2)
        draw.text((width - 290, cy - 120), "YEMEN / RAS MENHELI", fill=(200, 120, 80))
        draw.text((width - 290, cy - 100), "HOUTHI A2/AD COASTAL BATTERY", fill=(255, 80, 60))

        # Perim Island (Mayyun) in center of strait
        draw.ellipse([cx - 45, cy - 65, cx + 45, cy - 15], fill=(20, 30, 25), outline=(180, 160, 70), width=2)
        draw.text((cx - 38, cy - 45), "PERIM ISLAND", fill=(255, 220, 100))
        draw.text((cx - 36, cy - 30), "(MAYYUN)", fill=(200, 180, 80))

        # Bathymetric depth contour lines (Depth 20m, 50m, 100m, 180m Trench)
        for r_depth, d_label, col in [
            (160, "DEPTH CONTOUR: -50M", (0, 120, 150)),
            (110, "DEPTH CONTOUR: -100M", (0, 160, 200)),
            (70, "DEEP CHANNEL: -185M", (0, 210, 240))
        ]:
            draw.arc([cx - r_depth, cy - 140, cx + r_depth, cy + 180], start=45, end=315, fill=col, width=1)

        # 3. Submarine Fiber-Optic Cables traversing the channel
        cables = [
            ("AAE-1 (ASIA-AFRICA-EUROPE 1)", cx - 120, cx - 10, (0, 240, 255), False),
            ("EIG (EUROPE INDIA GATEWAY)", cx - 70, cx + 30, (0, 255, 200), True),
            ("SEA-ME-WE 5 (SMW-5)", cx - 20, cx + 70, (255, 200, 50), False),
            ("SEACOM / TGN-EURASIA", cx + 30, cx + 110, (180, 120, 255), True)
        ]

        for c_name, start_x, end_x, col, is_severed in cables:
            pts = []
            for y_step in range(cy - 220, cy + 220, 10):
                # Gentle curve through the maritime trench
                t = (y_step - (cy - 220)) / 440.0
                x_pos = int(start_x * (1 - t) + end_x * t + math.sin(t * math.pi * 3) * 18)
                pts.append((x_pos, y_step))

            if is_severed:
                # Cable severed at mid-point (anchor drag / ROV cut)
                sever_idx = len(pts) // 2
                draw.line(pts[:sever_idx - 2], fill=col, width=2)
                draw.line(pts[sever_idx + 2:], fill=col, width=2)
                
                # Sever fracture point & OTDR fault reflection alert
                sx, sy = pts[sever_idx]
                draw.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], outline=(255, 60, 40), width=2)
                draw.line([(sx - 8, sy - 8), (sx + 8, sy + 8)], fill=(255, 60, 40), width=2)
                draw.line([(sx - 8, sy + 8), (sx + 8, sy - 8)], fill=(255, 60, 40), width=2)
                draw.text((sx + 14, sy - 12), "SEVER FAULT: OTDR +0.0KM", fill=(255, 80, 60))
                draw.text((sx + 14, sy + 4), f"{c_name.split()[0]} DISRUPTED", fill=(255, 140, 50))
            else:
                draw.line(pts, fill=col, width=2)
                draw.text((pts[-1][0] - 40, cy + 200), c_name.split()[0], fill=col)

        # 4. Houthi Underwater ROV / Anchor Drag Interdiction Vector
        rov_x, rov_y = cx + 55, cy + 30
        draw.rectangle([rov_x - 18, rov_y - 14, rov_x + 18, rov_y + 14], fill=(30, 20, 25), outline=(255, 80, 50), width=2)
        draw.line([(rov_x - 12, rov_y), (rov_x + 12, rov_y)], fill=(255, 200, 80), width=1)
        draw.text((rov_x - 55, rov_y - 32), "[HOUTHI SUBMERSIBLE ROV]", fill=(255, 90, 60))
        draw.text((rov_x - 45, rov_y + 18), "DEPTH: -142M // CLAW ENGAGED", fill=(255, 160, 60))
        # Anchor drag chain vector across seabed
        draw.line([(cx + 120, cy - 80), (rov_x, rov_y)], fill=(255, 120, 40), width=1)
        draw.text((cx + 80, cy - 60), "RUBYMAR ANCHOR SCARRING", fill=(255, 140, 50))

        # 5. Telemetry Dossiers (Subsea Cable Infrastructure & Soviet Horn of Africa SIGINT)
        # Left HUD Box: Subsea Infrastructure Telemetry
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[BAB EL-MANDEB CABLE HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "TRANSIT: 17% GLOBAL INTERNET", fill=(255, 220, 100))
        draw.text((70, 138), "CHOKEPOINT WIDTH: 29 KM", fill=(0, 255, 200))
        draw.text((70, 158), "LATENCY PENALTY: +148ms CAPE", fill=(120, 220, 255))
        draw.text((70, 178), "FIBER STATUS: 4 LINES SEVERED", fill=(255, 80, 60))

        # Right HUD Box: Soviet 8th Eskadra Naval Doctrine & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET 8TH ESKADRA RED SEA]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "DAHLAK ISLAND NAVAL BASE", fill=(255, 200, 80))
        draw.text((width - 310, 138), "SOCOTRA ANCHORAGE SIGINT", fill=(255, 100, 80))
        draw.text((width - 310, 158), "SEABED WARFARE PRECEDENT", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("black_budget", "pentagon_sap", "sap_carveouts", "defense_audit", "failed_audit"):
        # Unacknowledged Special Access Programs (USAPs), Audit Exemption Carve-Outs & Slush Funds
        # 1. Background classified budget ledger grid
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(28, 18, 12), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(28, 18, 12), width=1)

        # 2. Classified Redaction Bars across ledger rows
        random.seed(319)
        for r_bar in range(16):
            rx = random.randint(70, width - 360)
            ry = cy - 200 + r_bar * 25
            rw = random.randint(140, 280)
            # Solid black redaction block with warning outline
            draw.rectangle([rx, ry, rx + rw, ry + 18], fill=(10, 6, 8), outline=(255, 60, 40), width=1)
            draw.text((rx + 10, ry + 2), "[REDACTED // 10 U.S.C. § 119 WAIVER]", fill=(255, 80, 50))

        # 3. Center: Accounting Black Hole & Diverted Funds Vortex
        bh_cx, bh_cy = cx, cy
        for vr in range(130, 20, -12):
            factor = (130 - vr) / 110.0
            col = (int(255 * factor), int(120 * factor), 40)
            draw.ellipse([bh_cx - vr, bh_cy - vr, bh_cx + vr, bh_cy + vr], outline=col, width=2)

        # Center core: Unaccounted Void
        draw.ellipse([bh_cx - 28, bh_cy - 28, bh_cx + 28, bh_cy + 28], fill=(12, 4, 6), outline=(255, 40, 40), width=2)
        draw.text((bh_cx - 24, bh_cy - 8), "$1.9T VOID", fill=(255, 220, 100))

        # FASAB Statement 56 Classified Accounting Shield Seal (Upper Center)
        draw.rectangle([cx - 160, cy - 145, cx + 160, cy - 105], fill=(30, 15, 12), outline=(255, 160, 40), width=2)
        draw.text((cx - 145, cy - 140), "FASAB STATEMENT 56 FINANCIAL SHIELD", fill=(255, 180, 50))
        draw.text((cx - 130, cy - 122), "UNACKNOWLEDGED SAP AUDIT EXEMPTION", fill=(255, 80, 60))

        # Capital Flow Routing Conduits (Title 10 Appropriations -> Prime Vault)
        # Left flow: Title 10 Congressional defense appropriation diverted
        draw.line([(cx - 220, cy), (cx - 40, cy)], fill=(255, 140, 50), width=3)
        draw.polygon([(cx - 40, cy), (cx - 52, cy - 6), (cx - 52, cy + 6)], fill=(255, 140, 50))
        draw.text((cx - 220, cy + 10), "CONGRESSIONAL ALLOCATION", fill=(255, 180, 80))
        draw.text((cx - 220, cy + 26), "DIVERTED PASS-THROUGH", fill=(255, 80, 60))

        # Right flow: Prime Contractor Vault (Off-Book Overhead)
        draw.line([(cx + 40, cy), (cx + 220, cy)], fill=(255, 100, 60), width=3)
        draw.polygon([(cx + 220, cy), (cx + 208, cy - 6), (cx + 208, cy + 6)], fill=(255, 100, 60))
        draw.text((cx + 80, cy + 10), "PRIME CONTRACTOR SCIF", fill=(255, 180, 80))
        draw.text((cx + 80, cy + 26), "COST-PLUS OVERHEAD: +840%", fill=(255, 80, 60))

        # 4. Floating Classified Program Nicknames & Compartments
        usap_tags = [
            ("COMPARTMENT: RETRACT LARCH", cx - 210, cy + 80),
            ("WAIVED SAP: SENIOR ICE", cx + 60, cy + 80),
            ("SPECIAL ACCESS PROGRAM: COLD WILLOW", cx - 150, cy + 130)
        ]
        for tag, tx, ty in usap_tags:
            draw.rectangle([tx - 6, ty - 4, tx + 240, ty + 18], fill=(20, 10, 14), outline=(180, 60, 50), width=1)
            draw.text((tx, ty), tag, fill=(255, 120, 80))

        # 5. Telemetry Dossiers (Audit Black Hole & Soviet Slush Funds)
        # Left HUD Box: Pentagon Audit Failure Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(22, 12, 14), outline=(255, 80, 60), width=1)
        draw.text((70, 98), "[PENTAGON FAILED AUDIT HUD]", fill=(255, 90, 70))
        draw.text((70, 118), "AUDIT RESULT: 7 CONSECUTIVE FAILS", fill=(255, 200, 80))
        draw.text((70, 138), "UNTRACKED ASSETS: $3.8 TRILLION", fill=(255, 60, 60))
        draw.text((70, 158), "USAP EXEMPTION: 10 U.S.C. 119", fill=(255, 160, 50))
        draw.text((70, 178), "INVOICE DISCREPANCIES: SHREDDED", fill=(255, 100, 80))

        # Right HUD Box: Soviet Black Budget Lineage & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET BLACK BUDGET LINEAGE]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "MOD OFF-BOOK SPECIAL ACCOUNTS", fill=(255, 200, 80))
        draw.text((width - 310, 138), "KGB FIRST CHIEF SLUSH FUNDS", fill=(255, 100, 80))
        draw.text((width - 310, 158), "GOSPLAN FRAUD & SHADOW THEFT", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("big_toe", "digital_physics", "campbell_simulation", "cellular_automata", "entropy_reduction"):
        # Thomas Campbell's Big TOE, Digital Physics, Cellular Automata & Entropy Reduction
        # 1. Background Discrete Planck Pixel Matrix (Cellular Automaton Lattice)
        cell_size = 18
        grid_start_x = 60
        grid_end_x = width - 60
        grid_start_y = cy - 220
        grid_end_y = cy + 220

        # Draw discrete computing grid
        for gy in range(grid_start_y, grid_end_y, cell_size):
            draw.line([(grid_start_x, gy), (grid_end_x, gy)], fill=(8, 20, 34), width=1)
        for gx in range(grid_start_x, grid_end_x, cell_size):
            draw.line([(gx, grid_start_y), (gx, grid_end_y)], fill=(8, 20, 34), width=1)

        # 2. Cellular Automaton Active Bits (Game of Life / Rule 30 patterns)
        random.seed(424)
        for gy in range(grid_start_y, grid_end_y, cell_size):
            for gx in range(grid_start_x, grid_end_x, cell_size):
                # Pseudo-computational active state
                r_val = random.random()
                dist_c = math.hypot(gx - cx, gy - cy)
                if dist_c < 220 and r_val < 0.28:
                    col = (0, 240, 255) if r_val < 0.14 else (180, 100, 255)
                    draw.rectangle([gx + 2, gy + 2, gx + cell_size - 2, gy + cell_size - 2], fill=col)
                elif r_val < 0.08:
                    draw.rectangle([gx + 3, gy + 3, gx + cell_size - 3, gy + cell_size - 3], fill=(15, 45, 65))

        # 3. Center: Larger Consciousness System (LCS) Core Node & Entropy Funnel
        lcs_cx, lcs_cy = cx, cy
        # Outer informational boundary rings
        for r_lcs in [150, 110, 75]:
            draw.ellipse([lcs_cx - r_lcs, lcs_cy - r_lcs, lcs_cx + r_lcs, lcs_cy + r_lcs], outline=(0, 220, 255), width=1)
        
        # Central LCS Core
        draw.ellipse([lcs_cx - 40, lcs_cy - 40, lcs_cx + 40, lcs_cy + 40], fill=(12, 28, 48), outline=(200, 140, 255), width=2)
        draw.text((lcs_cx - 28, lcs_cy - 16), "LCS CORE", fill=(255, 255, 255))
        draw.text((lcs_cx - 32, lcs_cy + 2), "ΔS < 0 EVOL", fill=(0, 255, 200))

        # Data Stream Conduits to IUOCs (Individuated Units of Consciousness)
        iuocs = [
            (cx - 200, cy - 90, "IUOC α_1 (OBSERVER)"),
            (cx + 200, cy - 90, "IUOC α_2 (OBSERVER)"),
            (cx, cy + 140, "VIRTUAL REALITY RENDER ENGINE")
        ]
        for ix, iy, ilabel in iuocs:
            # Data link ray
            draw.line([(lcs_cx, lcs_cy), (ix, iy)], fill=(0, 240, 255), width=2)
            # Node circle
            draw.ellipse([ix - 24, iy - 24, ix + 24, iy + 24], fill=(15, 30, 50), outline=(0, 255, 220), width=2)
            draw.ellipse([ix - 4, iy - 4, ix + 4, iy + 4], fill=(255, 255, 255))
            draw.text((ix - 60, iy + 28), ilabel, fill=(180, 220, 255))

        # Rendering On Demand Callout (Center Lower)
        draw.rectangle([cx - 180, cy + 45, cx + 180, cy + 85], fill=(15, 22, 35), outline=(0, 240, 255), width=1)
        draw.text((cx - 165, cy + 50), "RENDER ON MEASUREMENT // CALCULATION SAVINGS", fill=(0, 255, 240))
        draw.text((cx - 150, cy + 68), "WAVEFUNCTION AS UNRENDERED PROBABILITY DISTRIBUTION", fill=(200, 160, 255))

        # 4. Telemetry Dossiers (Big TOE Metrics & Soviet Psychotronics)
        # Left HUD Box: Digital Physics Telemetry
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[DIGITAL PHYSICS HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "FRAME RATE: 1/t_P = 1.85e43 Hz", fill=(255, 220, 100))
        draw.text((70, 138), "SPATIAL PIXEL: l_P = 1.62e-35 m", fill=(0, 255, 200))
        draw.text((70, 158), "OBJECTIVE: MINIMIZE ENTROPY S", fill=(120, 220, 255))
        draw.text((70, 178), "MODEL: CELLULAR AUTOMATON VR", fill=(200, 140, 255))

        # Right HUD Box: Soviet Bio-Information & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET BIO-INFORMATION]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "UNIT 10003 PSI RESEARCH", fill=(255, 200, 80))
        draw.text((width - 310, 138), "NON-LOCAL INFORMATION QUERY", fill=(255, 100, 80))
        draw.text((width - 310, 158), "BIO-CYBERNETIC TELEMETRY", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("gibraltar_asw", "gibraltar_strait", "strait_of_gibraltar", "morocco_radar"):
        # Strait of Gibraltar Undersea Acoustic Arrays, Thermocline Baffles & Soviet 5th Eskadra
        # 1. Background hydrographic grid & depth sounding lines
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(8, 22, 34), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(8, 22, 34), width=1)

        # 2. Strait Coastlines (North: Spain/Gibraltar, South: Morocco/Ceuta)
        # European Coastline (North, Upper Section)
        draw.polygon([(60, cy - 220), (cx - 160, cy - 130), (cx + 80, cy - 145), (cx + 220, cy - 110), (width - 60, cy - 220)], fill=(15, 24, 28), outline=(60, 130, 150), width=2)
        draw.text((cx - 140, cy - 170), "SPAIN // TARIFA POINT", fill=(80, 180, 200))
        draw.text((cx + 100, cy - 160), "ROCK OF GIBRALTAR [UK]", fill=(255, 220, 100))
        draw.text((cx + 100, cy - 142), "NATO ASW SURVEILLANCE RADAR", fill=(0, 240, 255))

        # African Coastline (South, Lower Section)
        draw.polygon([(60, cy + 220), (cx - 150, cy + 130), (cx + 60, cy + 150), (cx + 240, cy + 115), (width - 60, cy + 220)], fill=(24, 18, 14), outline=(160, 100, 60), width=2)
        draw.text((cx - 130, cy + 175), "MOROCCO // CAPE SPARTEL", fill=(200, 140, 80))
        draw.text((cx + 80, cy + 170), "CEUTA // JEBEL MUSA", fill=(255, 140, 50))
        draw.text((cx + 80, cy + 188), "MOROCCAN COASTAL RADAR GATE", fill=(255, 80, 60))

        # 3. Two-Layer Counter-Current Flow & Halocline Thermocline
        # Atlantic Surface Inflow (Eastward, Cyan)
        for arrow_x in range(cx - 240, cx + 240, 70):
            draw.line([(arrow_x, cy - 40), (arrow_x + 45, cy - 40)], fill=(0, 240, 255), width=2)
            draw.polygon([(arrow_x + 45, cy - 40), (arrow_x + 36, cy - 44), (arrow_x + 36, cy - 36)], fill=(0, 240, 255))
        draw.text((cx - 120, cy - 58), "ATLANTIC INFLOW: +2.8 KTS (EASTBOUND)", fill=(0, 255, 240))

        # Mediterranean Deep Outflow (Westward, Amber)
        for arrow_x in range(cx - 240, cx + 240, 70):
            draw.line([(arrow_x + 45, cy + 40), (arrow_x, cy + 40)], fill=(255, 140, 40), width=2)
            draw.polygon([(arrow_x, cy + 40), (arrow_x + 9, cy + 36), (arrow_x + 9, cy + 44)], fill=(255, 140, 40))
        draw.text((cx - 130, cy + 50), "MEDITERRANEAN DEEP OUTFLOW: -2.1 KTS (WESTBOUND)", fill=(255, 160, 50))

        # Camarinal Sill Bathymetric Ridge (Center Barrier at 280m Depth)
        draw.arc([cx - 120, cy - 50, cx + 120, cy + 50], start=160, end=380, fill=(0, 200, 240), width=2)
        draw.text((cx - 75, cy - 12), "CAMARINAL SILL [280M]", fill=(0, 255, 220))

        # 4. SOSUS Fixed Seabed Hydrophone Barrier Array
        hydro_x1, hydro_x2 = cx - 180, cx + 180
        draw.line([(hydro_x1, cy), (hydro_x2, cy)], fill=(255, 60, 40), width=2)
        for hx in range(hydro_x1, hydro_x2 + 1, 40):
            # Hydrophone sensor node
            draw.rectangle([hx - 4, cy - 4, hx + 4, cy + 4], fill=(255, 255, 255), outline=(255, 60, 40), width=1)
            # Acoustic detection cone radiating upward
            draw.line([(hx, cy), (hx - 12, cy - 25)], fill=(255, 80, 60), width=1)
            draw.line([(hx, cy), (hx + 12, cy - 25)], fill=(255, 80, 60), width=1)
        draw.text((cx - 95, cy + 12), "FIXED SOSUS HYDROPHONE ARRAY", fill=(255, 80, 60))

        # Submarine Silhouette / Drift Transit Profile (Project 671 Victor-class under thermocline)
        sub_x, sub_y = cx + 30, cy + 20
        draw.ellipse([sub_x - 32, sub_y - 8, sub_x + 32, sub_y + 8], fill=(18, 12, 16), outline=(255, 200, 60), width=2)
        draw.rectangle([sub_x - 6, sub_y - 16, sub_x + 6, sub_y - 8], fill=(255, 200, 60))
        draw.text((sub_x - 55, sub_y - 28), "SOVIET VICTOR-CLASS DRIFT", fill=(255, 220, 80))

        # 5. Telemetry Dossiers (Gibraltar ASW & Soviet 5th Eskadra)
        # Left HUD Box: Gibraltar ASW Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[GIBRALTAR ASW BARRIER HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "WIDTH: 14.3 KM CHOKEPOINT", fill=(255, 220, 100))
        draw.text((70, 138), "THERMOCLINE DEPTH: 120M", fill=(0, 255, 200))
        draw.text((70, 158), "INTERNAL SOLITON WAVES: ACTIVE", fill=(120, 220, 255))
        draw.text((70, 178), "SOSUS DETECTION PROB: 94.2%", fill=(255, 140, 50))

        # Right HUD Box: Soviet 5th Eskadra & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET 5TH ESKADRA MED]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "TARTUS NAVAL SUPPORT HUB", fill=(255, 200, 80))
        draw.text((width - 310, 138), "COLD DRIFT ENGINE-OFF TRANSIT", fill=(255, 100, 80))
        draw.text((width - 310, 158), "HALOCLINE ACOUSTIC SHADOW", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("logistics_fraud", "phantom_containers", "freight_grift", "warehouse_theft", "demurrage_fraud"):
        # Defense Logistics Phantom Container Invoicing & Warehouse Theft Networks
        # 1. Background Shipping Manifest Ledger Grid
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(28, 20, 14), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(28, 20, 14), width=1)

        # Shipping manifest codes across background
        manifest_codes = [
            ("MSKU-98214-7 // SHUAIBA PORT", 70, cy - 190),
            ("TGHU-41092-3 // GHOST CONTAINER", cx - 80, cy - 190),
            ("DEMURRAGE: 412 DAYS BILLED", width - 300, cy - 190),
            ("CARGO: TACTICAL FIELD GEAR", 70, cy - 150),
            ("DISCREPANCY: 0 TONS DELIVERED", cx - 80, cy - 150),
            ("PASS-THROUGH: DUBAI FZE LLC", width - 300, cy - 150)
        ]
        for m_text, mx, my in manifest_codes:
            draw.text((mx, my), m_text, fill=(200, 100, 60))

        # 2. Intermodal Shipping Container Stacks (Center)
        # Stack A (Left Center): Solid billed container
        stack_x1, stack_y1 = cx - 180, cy - 40
        c_w, c_h = 160, 60
        # Solid container body (Amber/Orange)
        draw.rectangle([stack_x1, stack_y1, stack_x1 + c_w, stack_y1 + c_h], fill=(35, 22, 14), outline=(255, 140, 40), width=2)
        # Corrugated vertical ribs
        for rib_x in range(stack_x1 + 15, stack_x1 + c_w - 10, 15):
            draw.line([(rib_x, stack_y1 + 4), (rib_x, stack_y1 + c_h - 4)], fill=(180, 90, 30), width=1)
        draw.text((stack_x1 + 12, stack_y1 + 10), "BILLED CONTAINER", fill=(255, 180, 50))
        draw.text((stack_x1 + 12, stack_y1 + 28), "STATUS: PHANTOM MANIFEST", fill=(255, 80, 60))
        draw.text((stack_x1 + 12, stack_y1 + 44), "INVOICE: $184,000", fill=(255, 220, 100))

        # Stack B (Right Center): Wireframe "Ghost" Phantom Container
        stack_x2, stack_y2 = cx + 20, cy - 40
        # Dashed / Wireframe outline representing phantom container
        draw.rectangle([stack_x2, stack_y2, stack_x2 + c_w, stack_y2 + c_h], fill=(18, 10, 14), outline=(255, 60, 40), width=2)
        for rib_x in range(stack_x2 + 15, stack_x2 + c_w - 10, 20):
            draw.line([(rib_x, stack_y2 + 8), (rib_x, stack_y2 + c_h - 8)], fill=(120, 40, 30), width=1)
        # Big "GHOST" warning stamp across container
        draw.text((stack_x2 + 25, stack_y2 + 10), "[GHOST INVOICE]", fill=(255, 60, 60))
        draw.text((stack_x2 + 15, stack_y2 + 28), "CONTAINER UNLOCATED", fill=(255, 100, 80))
        draw.text((stack_x2 + 15, stack_y2 + 44), "DEMURRAGE: +620%", fill=(255, 140, 50))

        # Bottom Container Foundation (Stacked below)
        stack_y3 = cy + 30
        draw.rectangle([stack_x1 + 40, stack_y3, stack_x1 + 40 + c_w + 80, stack_y3 + c_h], fill=(24, 16, 12), outline=(200, 120, 50), width=2)
        draw.text((stack_x1 + 55, stack_y3 + 12), "FREIGHT FORWARDING PASS-THROUGH CONDUIT", fill=(255, 160, 60))
        draw.text((stack_x1 + 55, stack_y3 + 30), "SHELL ENTITY MARKUP: 42% // CENTCOM THEATER", fill=(255, 90, 70))

        # 3. Capital Diverting Arrow Flow (Appropriations -> Dubai Shell -> Kickback)
        draw.line([(cx - 240, cy + 130), (cx + 240, cy + 130)], fill=(255, 100, 50), width=2)
        draw.polygon([(cx + 240, cy + 130), (cx + 228, cy + 124), (cx + 228, cy + 136)], fill=(255, 100, 50))
        draw.text((cx - 220, cy + 110), "DEFENSE LOGISTICS ALLOCATION", fill=(255, 180, 80))
        draw.text((cx - 30, cy + 110), "PORT DEMURRAGE CHURN", fill=(255, 80, 60))
        draw.text((cx + 120, cy + 110), "SUBCONTRACTOR REBATE", fill=(255, 220, 100))

        # 4. Telemetry Dossiers (Logistics Fraud & Soviet Voentorg Grift)
        # Left HUD Box: Defense Logistics Fraud Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(22, 14, 12), outline=(255, 80, 60), width=1)
        draw.text((70, 98), "[DEFENSE LOGISTICS FRAUD HUD]", fill=(255, 90, 70))
        draw.text((70, 118), "AUDIT: CENTCOM CONTAINER AUDIT", fill=(255, 200, 80))
        draw.text((70, 138), "PHANTOM DEMURRAGE: $720M", fill=(255, 60, 60))
        draw.text((70, 158), "GHOST UNITS: 1,840 CONTAINERS", fill=(255, 160, 50))
        draw.text((70, 178), "INSPECTION SEAL: BYPASSED", fill=(255, 100, 80))

        # Right HUD Box: Soviet Voentorg Lineage & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET WAREHOUSE THEFT]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "VOENTORG DEPOT DIVERSIONS", fill=(255, 200, 80))
        draw.text((width - 310, 138), "GRAU RAILCAR THEFT RINGS", fill=(255, 100, 80))
        draw.text((width - 310, 158), "BLACK MARKET LOGISTICS AXIS", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

    elif theme in ("rydberg_electrometry", "rydberg_sensor", "sub_thz_quantum", "microwave_electrometry"):
        # Rydberg Atom Quantum Electrometry, EIT Autler-Townes Splitting & Sub-THz Sensing
        # 1. Background optical frequency and RF interference grid
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(10, 24, 38), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(10, 24, 38), width=1)

        # 2. Central Quartz Vapor Cell (Rubidium Atom Gas)
        cell_x, cell_y = cx, cy - 30
        cell_w, cell_h = 240, 90
        # Quartz glass envelope
        draw.rectangle([cell_x - cell_w//2, cell_y - cell_h//2, cell_x + cell_w//2, cell_y + cell_h//2], fill=(12, 25, 42), outline=(0, 220, 255), width=2)
        draw.text((cell_x - cell_w//2 + 10, cell_y - cell_h//2 + 8), "RUBIDIUM-85 VAPOR CELL", fill=(0, 240, 255))
        draw.text((cell_x - cell_w//2 + 10, cell_y - cell_h//2 + 24), "OPTICAL PATH: L = 25mm", fill=(120, 220, 255))

        # Counter-Propagating Laser Beams traversing the cell
        # 780nm Probe Laser (Red/Orange, Left to Right)
        beam_y = cell_y + 10
        draw.line([(cell_x - cell_w//2 - 60, beam_y), (cell_x + cell_w//2 + 60, beam_y)], fill=(255, 60, 60), width=3)
        draw.text((cell_x - cell_w//2 - 130, beam_y - 8), "780nm PROBE", fill=(255, 80, 80))

        # 480nm Coupling Laser (Electric Cyan/Blue, Right to Left)
        draw.line([(cell_x + cell_w//2 + 60, beam_y), (cell_x - cell_w//2 - 60, beam_y)], fill=(0, 240, 255), width=1)
        draw.text((cell_x + cell_w//2 + 70, beam_y - 8), "480nm COUPLING", fill=(0, 255, 240))

        # Exaggerated Rydberg Giant Orbit Atoms (n=50 excited state)
        random.seed(815)
        for _ in range(12):
            ax = random.randint(cell_x - cell_w//2 + 30, cell_x + cell_w//2 - 30)
            ay = random.randint(cell_y - cell_h//2 + 35, cell_y + cell_h//2 - 15)
            # Huge Rydberg atomic electron orbit
            r_orbit = random.randint(14, 24)
            draw.ellipse([ax - r_orbit, ay - r_orbit, ax + r_orbit, ay + r_orbit], outline=(0, 255, 220), width=1)
            # Ionic core
            draw.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=(255, 255, 255))
            # Valence electron at apogee
            th = random.uniform(0, 2 * math.pi)
            ex = ax + int(math.cos(th) * r_orbit)
            ey = ay + int(math.sin(th) * r_orbit)
            draw.point((ex, ey), fill=(255, 220, 100))

        # 3. Incident Microwave RF Wavefronts (Upper section impinging on cell)
        for rf_y in range(cell_y - 120, cell_y - 55, 18):
            draw.line([(cell_x - 140, rf_y), (cell_x + 140, rf_y)], fill=(255, 180, 50), width=2)
            # Wavefront propagation arrowheads
            draw.polygon([(cell_x, rf_y + 12), (cell_x - 6, rf_y + 4), (cell_x + 6, rf_y + 4)], fill=(255, 180, 50))
        draw.text((cell_x - 110, cell_y - 135), "INCIDENT SUB-THz MICROWAVE FIELD (E_MW)", fill=(255, 200, 80))

        # 4. EIT & Autler-Townes Splitting Spectrum Plot (Lower Center)
        spec_x, spec_y = cx - 180, cy + 90
        spec_w, spec_h = 360, 80
        draw.rectangle([spec_x, spec_y, spec_x + spec_w, spec_y + spec_h], fill=(10, 18, 28), outline=(0, 200, 240), width=1)
        draw.text((spec_x + 10, spec_y + 8), "EIT TRANSMISSION // AUTLER-TOWNES SPLITTING: 2Ω_MW = 2μ E / ℏ", fill=(0, 255, 240))
        
        # Dual-Peak Autler-Townes curve
        spec_pts = []
        for sx in range(spec_w - 20):
            x_rel = (sx - (spec_w // 2 - 10)) / 22.0
            # Double Lorentzian peak from RF Stark splitting
            peak1 = 38.0 / (1.0 + (x_rel - 2.8)**2)
            peak2 = 38.0 / (1.0 + (x_rel + 2.8)**2)
            sy_val = spec_y + spec_h - 15 - int(peak1 + peak2)
            spec_pts.append((spec_x + 10 + sx, sy_val))
        if len(spec_pts) > 1:
            draw.line(spec_pts, fill=(0, 255, 200), width=2)
        draw.text((spec_x + spec_w // 2 - 40, spec_y + 45), "Δf = 142.4 MHz", fill=(255, 220, 100))

        # 5. Telemetry Dossiers (Rydberg Electrometry & Soviet Microwave SIGINT)
        # Left HUD Box: Quantum Sensor Telemetry
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 35), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[RYDBERG ELECTROMETRY HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "ATOMIC LEVEL: Rb-85 |50D_5/2⟩", fill=(255, 220, 100))
        draw.text((70, 138), "SENSITIVITY: 1.2 μV/cm/√Hz", fill=(0, 255, 200))
        draw.text((70, 158), "BANDWIDTH: DC TO 1.0 THz", fill=(120, 220, 255))
        draw.text((70, 178), "CALIBRATION: SI TRACEABLE", fill=(200, 140, 255))

        # Right HUD Box: Soviet Microwave SIGINT & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET MICROWAVE SIGINT]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "MOSCOW EMBASSY MICROWAVES", fill=(255, 200, 80))
        draw.text((width - 310, 138), "KGB 8TH CHIEF ILLUMINATION", fill=(255, 100, 80))
        draw.text((width - 310, 158), "ANTENNA-LESS SENSOR ARRAY", fill=(255, 220, 120))
    elif theme in ("orch_or", "orch_or_anesthesia", "tubulin_quantum", "quantum_anesthesia"):
        # Penrose-Hameroff Orch-OR Microtubule Lattice & Anesthetic Dipole Decoupling
        # 1. Background hexagonal lattice grid & quantum coherence field
        for gy in range(cy - 220, cy + 220, 26):
            draw.line([(60, gy), (width - 60, gy)], fill=(12, 28, 36), width=1)
        for gx in range(60, width - 60, 44):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(12, 28, 36), width=1)

        # 2. Central Cylindrical Microtubule Lattice
        # Representing 13 protofilaments of alpha & beta tubulin heterodimers
        tub_x_start = cx - 240
        tub_x_end = cx + 240
        tub_y_center = cy - 20
        num_cols = 16
        col_w = (tub_x_end - tub_x_start) // num_cols

        # Outer sheath envelope
        draw.rectangle([tub_x_start - 10, tub_y_center - 75, tub_x_end + 10, tub_y_center + 75], fill=(8, 16, 26), outline=(0, 255, 200), width=1)
        draw.text((tub_x_start, tub_y_center - 95), "MICROTUBULE CYLINDER (25nm DIAMETER // 13 PROTOFILAMENTS)", fill=(0, 255, 200))

        # Tubulin Dimers (Alternating Alpha and Beta subunits with pi-electron dipoles)
        for col in range(num_cols):
            x_pos = tub_x_start + col * col_w + col_w // 2
            for row in range(-3, 4):
                y_pos = tub_y_center + row * 18
                # Alternate alpha/beta tubulin
                is_alpha = (col + row) % 2 == 0
                color_sub = (0, 220, 255) if is_alpha else (180, 100, 255)
                # Dimer ellipse
                draw.ellipse([x_pos - 9, y_pos - 7, x_pos + 9, y_pos + 7], fill=(15, 30, 45), outline=color_sub, width=1)
                # Hydrophobic core dipole point
                dipole_color = (255, 230, 100) if (col * 3 + row) % 4 == 0 else (100, 255, 220)
                draw.ellipse([x_pos - 2, y_pos - 2, x_pos + 2, y_pos + 2], fill=dipole_color)

        # Coherent terahertz quantum resonance wave traversing the microtubule
        wave_pts = []
        for wx in range(tub_x_start, tub_x_end, 6):
            rel_x = (wx - tub_x_start) * 0.05
            wy = tub_y_center + int(28 * math.sin(rel_x))
            wave_pts.append((wx, wy))
        if len(wave_pts) > 1:
            draw.line(wave_pts, fill=(255, 220, 80), width=2)
        draw.text((tub_x_start + 40, tub_y_center + 80), "COHERENT THz DIPOLE OSCILLATION (614 THz RESONANCE)", fill=(255, 220, 100))

        # 3. Anesthetic Molecule Insertion & Quantum Decoherence Pinning
        # Xenon / Halothane molecules binding in hydrophobic pockets
        anes_positions = [(cx - 100, tub_y_center - 15), (cx + 80, tub_y_center + 20), (cx + 10, tub_y_center - 35)]
        for ax, ay in anes_positions:
            draw.ellipse([ax - 12, ay - 12, ax + 12, ay + 12], fill=(255, 50, 70), outline=(255, 255, 255), width=2)
            draw.text((ax - 6, ay - 6), "Xe", fill=(255, 255, 255))
            # Decoherence perturbation field
            draw.arc([ax - 18, ay - 18, ax + 18, ay + 18], 0, 360, fill=(255, 120, 120), width=1)
        draw.text((cx - 120, tub_y_center - 45), "ANESTHETIC BINDING // DIPOLE QUENCHING", fill=(255, 80, 80))

        # 4. Penrose Gravitational Collapse Curve (Lower center plot)
        spec_x, spec_y = cx - 180, cy + 105
        spec_w, spec_h = 360, 65
        draw.rectangle([spec_x, spec_y, spec_x + spec_w, spec_y + spec_h], fill=(10, 18, 26), outline=(0, 200, 240), width=1)
        draw.text((spec_x + 10, spec_y + 6), "PENROSE ORCH-OR COLLAPSE: τ = ℏ / E_G (SELF-COLLAPSE)", fill=(0, 255, 220))
        # Decay / quantum superposition collapse trajectory
        col_pts = []
        for sx in range(spec_w - 20):
            norm_x = sx / (spec_w - 20)
            amp = math.exp(-2.5 * norm_x) * math.cos(norm_x * 22)
            cy_val = spec_y + 35 - int(amp * 20)
            col_pts.append((spec_x + 10 + sx, cy_val))
        if len(col_pts) > 1:
            draw.line(col_pts, fill=(0, 255, 180), width=2)

        # 5. Telemetry Dossiers (Orch-OR Quantum Bio & KGB Telemetry)
        # Left HUD Box: Orch-OR Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(10, 22, 32), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[ORCH-OR QUANTUM BIOLOGY]", fill=(0, 240, 255))
        draw.text((70, 118), "LATTICE: 13-PROTOFILAMENT TUBULIN", fill=(255, 220, 100))
        draw.text((70, 138), "DIPOLE FREQ: 614 THz COHERENCE", fill=(0, 255, 200))
        draw.text((70, 158), "COLLAPSE: GRAVITATIONAL E_G", fill=(120, 220, 255))
        draw.text((70, 178), "ANESTHESIA: ELECTRON QUENCH", fill=(255, 100, 100))

        # Right HUD Box: KGB Pharmacological Dossier & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 14, 18), outline=(255, 90, 120), width=1)
        draw.text((width - 310, 98), "[KGB PHARMACOLOGICAL TELEMETRY]", fill=(255, 100, 120))
        draw.text((width - 310, 118), "KGB 12TH DEPT NARCO-ANALYSIS", fill=(255, 200, 80))
        draw.text((width - 310, 138), "PSYCHOTROPIC TELEMETRY LABS", fill=(255, 100, 80))
        draw.text((width - 310, 158), "CONSCIOUSNESS SUPPRESSION", fill=(255, 220, 120))
    elif theme in ("northern_sea_route", "arctic_route", "yamal_icebreaker", "glavsevmorput"):
        # Arctic Northern Sea Route, Nuclear Icebreaker Escort & Yamal LNG Logistics
        # 1. Background Polar Coordinate / Arctic Latitude Grid
        for r_pol in range(80, 260, 35):
            draw.arc([cx - r_pol, cy - 30 - r_pol, cx + r_pol, cy - 30 + r_pol], 0, 360, fill=(15, 32, 45), width=1)
        for ang in range(0, 360, 30):
            rad = math.radians(ang)
            draw.line([(cx + int(60 * math.cos(rad)), cy - 30 + int(60 * math.sin(rad))),
                       (cx + int(250 * math.cos(rad)), cy - 30 + int(250 * math.sin(rad)))], fill=(15, 32, 45), width=1)

        # 2. Polar Sea Ice Sheet (Polygon fractured ice pack)
        ice_pts = [
            (cx - 260, cy - 140), (cx - 180, cy - 170), (cx - 60, cy - 150), (cx + 80, cy - 180),
            (cx + 220, cy - 140), (cx + 260, cy - 80), (cx + 190, cy - 20), (cx + 240, cy + 40),
            (cx + 120, cy + 80), (cx - 40, cy + 60), (cx - 160, cy + 90), (cx - 250, cy + 20)
        ]
        draw.polygon(ice_pts, fill=(8, 22, 34), outline=(120, 220, 255))
        draw.text((cx - 110, cy - 165), "ARCTIC PACK ICE // MULTI-YEAR POLAR CAP", fill=(140, 230, 255))

        # 3. Carved Open Lead Channel / Wake Corridor (West to East)
        channel_y = cy - 20
        draw.polygon([(cx - 240, channel_y - 20), (cx + 240, channel_y - 20),
                      (cx + 240, channel_y + 20), (cx - 240, channel_y + 20)], fill=(5, 12, 22), outline=(0, 255, 220), width=1)
        draw.text((cx - 120, channel_y - 38), "SEVMORPUT OPEN LEAD [ICEBREAKER CARVED CHANNEL]", fill=(0, 255, 220))

        # 4. Nuclear Icebreaker Lead Vessel (Project 22220 Arktika-class)
        ib_x, ib_y = cx + 80, channel_y
        # Slanted ice-breaking bow rake & hull
        draw.polygon([(ib_x + 60, ib_y), (ib_x + 35, ib_y - 14), (ib_x - 50, ib_y - 14),
                      (ib_x - 50, ib_y + 14), (ib_x + 35, ib_y + 14)], fill=(20, 35, 50), outline=(255, 80, 60), width=2)
        # Nuclear superstructure & dual RITM-200 reactors
        draw.rectangle([ib_x - 20, ib_y - 8, ib_x + 15, ib_y + 8], fill=(255, 60, 40))
        draw.ellipse([ib_x - 4, ib_y - 4, ib_x + 4, ib_y + 4], fill=(255, 255, 255))
        draw.text((ib_x - 45, ib_y - 28), "PROJECT 22220 NUCLEAR ICEBREAKER", fill=(255, 100, 80))

        # Arc7 Yamal LNG Carrier in Escort Wake (Trailing behind icebreaker)
        lng_x, lng_y = cx - 120, channel_y
        draw.rectangle([lng_x - 55, lng_y - 12, lng_x + 45, lng_y + 12], fill=(15, 28, 40), outline=(0, 200, 255), width=2)
        # Spherical / membrane LNG cargo tanks
        for tx in range(lng_x - 35, lng_x + 35, 22):
            draw.ellipse([tx - 8, lng_y - 8, tx + 8, lng_y + 8], outline=(0, 255, 200), width=1)
        draw.text((lng_x - 50, lng_y + 18), "YAMAL ARC7 LNG CARRIER", fill=(0, 220, 255))

        # 5. Sabetta Port & Coastal Bastion Defense Radar Gate
        draw.ellipse([cx - 200, cy + 110, cx - 140, cy + 170], outline=(255, 200, 60), width=1)
        draw.point((cx - 170, cy + 140), fill=(255, 255, 255))
        draw.text((cx - 195, cy + 125), "SABETTA LNG HUB", fill=(255, 220, 80))
        draw.text((cx - 210, cy + 175), "BASTION-P MISSILE PERIMETER", fill=(255, 90, 70))

        # 6. Telemetry Dossiers (NSR Logistics & Soviet Glavsevmorput)
        # Left HUD Box: NSR Transit Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 32), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[NORTHERN SEA ROUTE HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "ROUTE: BARENTS TO BERING STRAIT", fill=(255, 220, 100))
        draw.text((70, 138), "DISTANCE SAVINGS: 4,000 NM", fill=(0, 255, 200))
        draw.text((70, 158), "ESCORT MONOPOLY: ROSATOMFLOT", fill=(120, 220, 255))
        draw.text((70, 178), "YAMAL LNG VOLUME: 20 MTPA", fill=(255, 140, 50))

        # Right HUD Box: Glavsevmorput & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET GLAVSEVMORPUT]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "POLAR STRATEGIC CORRIDOR", fill=(255, 200, 80))
        draw.text((width - 310, 138), "KGB BORDER GUARD FLOTILLA", fill=(255, 100, 80))
        draw.text((width - 310, 158), "NORTHERN FLEET SUB ESCORT", fill=(255, 220, 120))
    elif theme in ("f35_alis", "f35_software", "software_lockin", "contractor_lockin"):
        # Pentagon F-35 ALIS/ODIN Software Escalation & Defense Contractor IP Lock-In
        # 1. Background Source Code / Hex Memory Dump Grid
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(24, 16, 20), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(24, 16, 20), width=1)

        # Code snippets across the grid
        code_lines = [
            ("ALIS_KERNEL::DIAG_FAULT_BUS [0x8F41A]", 70, cy - 190),
            ("PROPRIETARY IP LOCK // LOCKHEED MARTIN", cx - 80, cy - 190),
            ("DOD ACCESS DENIED: REFACTOR BLOCKED", width - 300, cy - 190),
            ("SLOC COUNT: 24,180,000 LINES C++", 70, cy - 150),
            ("FALSE ALARM GROUNDING: CODE 419-X", cx - 80, cy - 150),
            ("SUSTAINMENT BILLING: $1.7T ESTIMATE", width - 300, cy - 150)
        ]
        for c_txt, cx_pos, cy_pos in code_lines:
            draw.text((cx_pos, cy_pos), c_txt, fill=(220, 80, 80))

        # 2. Stealth Fighter Silhouette (F-35 Lightning II Wireframe Profile)
        f_cx, f_cy = cx, cy - 30
        # Swept delta wings and stealth fuselage
        f35_pts = [
            (f_cx, f_cy - 70),          # Radome nose
            (f_cx + 18, f_cy - 20),      # Chined forebody right
            (f_cx + 120, f_cy + 30),     # Right wingtip
            (f_cx + 80, f_cy + 45),      # Right wing trailing edge
            (f_cx + 35, f_cy + 75),      # Right tail empennage
            (f_cx + 12, f_cy + 55),      # Exhaust right
            (f_cx - 12, f_cy + 55),      # Exhaust left
            (f_cx - 35, f_cy + 75),      # Left tail empennage
            (f_cx - 80, f_cy + 45),      # Left wing trailing edge
            (f_cx - 120, f_cy + 30),     # Left wingtip
            (f_cx - 18, f_cy - 20)       # Chined forebody left
        ]
        draw.polygon(f35_pts, fill=(16, 20, 28), outline=(255, 60, 60), width=2)
        # Cockpit canopy
        draw.polygon([(f_cx, f_cy - 45), (f_cx + 8, f_cy - 20), (f_cx - 8, f_cy - 20)], fill=(0, 220, 255))
        draw.text((f_cx - 95, f_cy - 90), "F-35 LIGHTNING II // AUTONOMIC LOGISTICS INTERFACE", fill=(255, 120, 100))

        # 3. Proprietary Software Dependency Lock-In Chains
        # Digital lock icon and constraint brackets over airframe
        draw.rectangle([f_cx - 25, f_cy - 5, f_cx + 25, f_cy + 25], fill=(30, 10, 15), outline=(255, 200, 50), width=2)
        draw.arc([f_cx - 15, f_cy - 22, f_cx + 15, f_cy + 5], 180, 360, fill=(255, 200, 50), width=2)
        draw.text((f_cx - 70, f_cy + 32), "[PROPRIETARY LOCK: NO REPAIR RIGHTS]", fill=(255, 220, 80))

        # 4. Lifecycle Sustainment Cost Escalation Curve (Lower center plot)
        spec_x, spec_y = cx - 180, cy + 95
        spec_w, spec_h = 360, 75
        draw.rectangle([spec_x, spec_y, spec_x + spec_w, spec_y + spec_h], fill=(18, 12, 16), outline=(255, 80, 60), width=1)
        draw.text((spec_x + 10, spec_y + 8), "ALIS / ODIN LIFECYCLE COST RUNAWAY // $1.7 TRILLION", fill=(255, 100, 80))
        # Exponential runaway cost line
        cost_pts = []
        for sx in range(spec_w - 20):
            norm_x = sx / (spec_w - 20)
            cost_val = int(12.0 * math.exp(norm_x * 1.5))
            cy_val = spec_y + spec_h - 15 - cost_val
            cost_pts.append((spec_x + 10 + sx, cy_val))
        if len(cost_pts) > 1:
            draw.line(cost_pts, fill=(255, 60, 40), width=2)
        draw.text((spec_x + spec_w - 110, spec_y + 25), "ESCALATION: +340%", fill=(255, 220, 100))

        # 5. Telemetry Dossiers (F-35 Software Fraud & Soviet MAP Kickbacks)
        # Left HUD Box: F-35 Software Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(22, 12, 16), outline=(255, 80, 60), width=1)
        draw.text((70, 98), "[F-35 ALIS/ODIN AUDIT]", fill=(255, 90, 70))
        draw.text((70, 118), "FLEET MISSION CAPABLE: 51.9%", fill=(255, 200, 80))
        draw.text((70, 138), "SOFTWARE LOCK: LOCKHEED MARTIN", fill=(255, 60, 60))
        draw.text((70, 158), "SPARE PARTS VISIBILITY: 0%", fill=(255, 160, 50))
        draw.text((70, 178), "FALSE FAULT CODES: CHRONIC", fill=(255, 100, 80))

        # Right HUD Box: Soviet MAP Lineage & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET AVIATION KICKBACKS]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "MINISTRY AVIATION IND (MAP)", fill=(255, 200, 80))
        draw.text((width - 310, 138), "PHANTOM PARTS PADDING", fill=(255, 100, 80))
        draw.text((width - 310, 158), "BUREAU-PLANT CARTELS", fill=(255, 220, 120))
    elif theme in ("majorana_zero_modes", "topological_quantum", "anyon_braiding", "cryogenic_cryptography"):
        # Topological Majorana Zero Modes & Non-Abelian Anyon Braiding
        # 1. Background Cryogenic Dilution Refrigerator Grid (mK Temperatures)
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(10, 26, 42), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(10, 26, 42), width=1)

        # 2. Semiconductor-Superconductor Nanowire (InAs Core with Epitaxial Aluminum Shell)
        nw_x1, nw_x2 = cx - 220, cx + 220
        nw_y = cy - 40
        nw_h = 24
        # Nanowire body
        draw.rectangle([nw_x1, nw_y - nw_h//2, nw_x2, nw_y + nw_h//2], fill=(12, 35, 55), outline=(0, 220, 255), width=2)
        # Superconducting aluminum capping shell
        draw.rectangle([nw_x1 + 30, nw_y - nw_h//2 - 6, nw_x2 - 30, nw_y - nw_h//2], fill=(140, 220, 255))
        draw.text((cx - 110, nw_y - 36), "InAs/Al TOPOLOGICAL NANOWIRE [T = 15 mK]", fill=(120, 240, 255))

        # 3. Localized Majorana Zero Modes (γ1 and γ2 at wire endpoints)
        # Left Majorana Bound State (γ1)
        draw.ellipse([nw_x1 - 18, nw_y - 18, nw_x1 + 18, nw_y + 18], fill=(255, 60, 100), outline=(255, 255, 255), width=2)
        draw.text((nw_x1 - 8, nw_y - 7), "γ1", fill=(255, 255, 255))
        draw.text((nw_x1 - 35, nw_y + 24), "MAJORANA ZERO MODE", fill=(255, 120, 140))

        # Right Majorana Bound State (γ2)
        draw.ellipse([nw_x2 - 18, nw_y - 18, nw_x2 + 18, nw_y + 18], fill=(255, 60, 100), outline=(255, 255, 255), width=2)
        draw.text((nw_x2 - 8, nw_y - 7), "γ2", fill=(255, 255, 255))
        draw.text((nw_x2 - 35, nw_y + 24), "MAJORANA ZERO MODE", fill=(255, 120, 140))

        # Non-local fermion state equation between γ1 and γ2
        draw.text((cx - 120, nw_y + 16), "NON-LOCAL FERMION: f = (γ1 + iγ2) / √2 // ZERO ENERGY", fill=(0, 255, 200))

        # 4. Non-Abelian Braiding Trajectories in Spacetime (Lower Center Diagram)
        braid_x, braid_y = cx - 180, cy + 70
        braid_w, braid_h = 360, 95
        draw.rectangle([braid_x, braid_y, braid_x + braid_w, braid_y + braid_h], fill=(10, 20, 32), outline=(0, 200, 240), width=1)
        draw.text((braid_x + 10, braid_y + 8), "NON-ABELIAN BRAIDING IN SPACETIME // TOPOLOGICAL PROTECTION", fill=(0, 255, 220))
        # Entangled worldlines representing anyon exchange
        for step in range(braid_w - 40):
            norm = step / (braid_w - 40)
            # Worldline 1 (Cyan)
            y1 = braid_y + 45 + int(24 * math.sin(norm * math.pi * 3))
            # Worldline 2 (Amber)
            y2 = braid_y + 45 - int(24 * math.sin(norm * math.pi * 3))
            draw.point((braid_x + 20 + step, y1), fill=(0, 240, 255))
            draw.point((braid_x + 20 + step, y2), fill=(255, 180, 50))
        draw.text((braid_x + braid_w // 2 - 50, braid_y + braid_h - 20), "BRAID OPERATOR: B = exp(±π/4 γ1 γ2)", fill=(255, 220, 100))

        # 5. Telemetry Dossiers (Majorana Metrics & Soviet Cryo-Crypto)
        # Left HUD Box: Majorana Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(10, 24, 38), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[MAJORANA ZERO MODE HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "ZEEMAN FIELD: B_z > √(Δ² + μ²)", fill=(255, 220, 100))
        draw.text((70, 138), "COHERENCE: TOPOLOGICALLY IMMUNE", fill=(0, 255, 200))
        draw.text((70, 158), "LOCAL DECOHERENCE: ZERO", fill=(120, 220, 255))
        draw.text((70, 178), "BRAIDING GATE ERROR: 10⁻⁶", fill=(255, 140, 50))

        # Right HUD Box: Soviet Cryo-Crypto Lineage & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET CRYO-CRYPTOGRAPHY]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "KAPITZA INSTITUTE RESEARCH", fill=(255, 200, 80))
        draw.text((width - 310, 138), "KGB 8TH CHIEF HARDWARE", fill=(255, 100, 80))
        draw.text((width - 310, 158), "JOSEPHSON JUNCTION CIPHERS", fill=(255, 220, 120))
    elif theme in ("anil_seth_hallucination", "controlled_hallucination", "bayesian_brain", "predictive_coding"):
        # Anil Seth Controlled Hallucination & KGB Reflexive Perception Warfare
        # 1. Background Cortical Layer Grid & Neural Predictive Flow
        for gy in range(cy - 220, cy + 220, 26):
            draw.line([(60, gy), (width - 60, gy)], fill=(18, 20, 36), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(18, 20, 36), width=1)

        # 2. Hierarchical Predictive Coding Architecture (Top-Down Priors vs Bottom-Up Errors)
        # Cortical Hierarchy Layers: Higher Cortex (Top) to Sensory Periphery (Bottom)
        layer_names = ["PREFRONTAL PRIOR P(H)", "ASSOCIATION CORTEX", "PRIMARY SENSORY V1", "RAW SENSORY INPUT Y"]
        layer_ys = [cy - 90, cy - 30, cy + 30, cy + 90]
        for l_idx, (l_name, ly) in enumerate(zip(layer_names, layer_ys)):
            draw.line([(cx - 200, ly), (cx + 200, ly)], fill=(0, 200, 255), width=2)
            draw.text((cx - 190, ly - 18), f"LAYER {4 - l_idx} // {l_name}", fill=(120, 220, 255))

        # Descending Top-Down Predictions (Cyan Arrows pointing downward: g(μ))
        for ax in (-120, 0, 120):
            for ly_top, ly_bot in zip(layer_ys[:-1], layer_ys[1:]):
                draw.line([(cx + ax - 25, ly_top + 4), (cx + ax - 25, ly_bot - 4)], fill=(0, 255, 200), width=2)
                draw.polygon([(cx + ax - 25, ly_bot - 4), (cx + ax - 29, ly_bot - 12), (cx + ax - 21, ly_bot - 12)], fill=(0, 255, 200))
        draw.text((cx - 165, cy - 5), "TOP-DOWN PREDICTION: g(μ) [CONTROLLED HALLUCINATION]", fill=(0, 255, 180))

        # Ascending Prediction Errors (Red/Amber Arrows pointing upward: ε = y - g(μ))
        for ax in (-120, 0, 120):
            for ly_top, ly_bot in zip(layer_ys[:-1], layer_ys[1:]):
                draw.line([(cx + ax + 25, ly_bot - 4), (cx + ax + 25, ly_top + 4)], fill=(255, 80, 80), width=2)
                draw.polygon([(cx + ax + 25, ly_top + 4), (cx + ax + 21, ly_top + 12), (cx + ax + 29, ly_top + 12)], fill=(255, 80, 80))
        draw.text((cx + 10, cy - 5), "PREDICTION ERROR: ε = y - g(μ)", fill=(255, 100, 80))

        # 3. Central Perceptual Attractor Well (Center HUD Circle)
        draw.ellipse([cx - 45, cy - 45, cx + 45, cy + 45], outline=(255, 220, 80), width=2)
        draw.text((cx - 38, cy - 8), "PERCEPT", fill=(255, 220, 80))
        draw.text((cx - 32, cy + 8), "EQUILIBRIUM", fill=(255, 180, 50))

        # 4. Telemetry Dossiers (Bayesian Brain & KGB Reflexive Control)
        # Left HUD Box: Bayesian Predictive Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 16, 28), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[BAYESIAN PREDICTIVE HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "PRIOR BIAS: 91.4% DOMINANCE", fill=(255, 220, 100))
        draw.text((70, 138), "SENSORY SUPPRESSION: ACTIVE", fill=(0, 255, 200))
        draw.text((70, 158), "PRECISION WEIGHTING: HYPER-TUNED", fill=(120, 220, 255))
        draw.text((70, 178), "HALLUCINATED CONSENSUS: TRUE", fill=(200, 140, 255))

        # Right HUD Box: KGB Reflexive Perception Warfare & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 12, 18), outline=(255, 100, 60), width=1)
        draw.text((width - 310, 98), "[KGB REFLEXIVE PERCEPTION]", fill=(255, 110, 70))
        draw.text((width - 310, 118), "SERVICE A ACTIVE MEASURES", fill=(255, 200, 80))
        draw.text((width - 310, 138), "COGNITIVE PRIOR INVERSION", fill=(255, 100, 80))
        draw.text((width - 310, 158), "REALITY FABRICATION DOCTRINE", fill=(255, 220, 120))
    elif theme in ("suwalki_gap", "kaliningrad_corridor", "baltic_chokepoint", "iskander_enclave"):
        # Suwalki Gap Chokepoint, Kaliningrad Iskander Bastion & Baltic Rail Interdiction
        # 1. Background Topographic & Tactical Grid
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(24, 18, 14), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(24, 18, 14), width=1)

        # 2. Border Geography Representation (Suwalki Gap Corridor)
        # Poland (Southwest) and Lithuania (Northeast) forming the narrow 65km neck
        # Kaliningrad Exclave (West) to Belarus (East)
        draw.polygon([(cx - 240, cy - 140), (cx - 80, cy - 140), (cx - 100, cy + 80), (cx - 240, cy + 120)], fill=(25, 12, 14), outline=(255, 60, 40), width=2)
        draw.text((cx - 220, cy - 120), "KALININGRAD EXCLAVE [BALTIC FLEET HQ]", fill=(255, 90, 70))

        draw.polygon([(cx + 80, cy - 140), (cx + 240, cy - 140), (cx + 240, cy + 120), (cx + 100, cy + 80)], fill=(20, 16, 26), outline=(200, 100, 255), width=2)
        draw.text((cx + 100, cy - 120), "BELARUS // WESTERN MILITARY AXIS", fill=(220, 120, 255))

        # Suwalki Gap Narrow Land Bridge (Center Chokepoint)
        gap_x1, gap_x2 = cx - 80, cx + 80
        draw.rectangle([gap_x1, cy - 80, gap_x2, cy + 60], fill=(12, 22, 16), outline=(0, 255, 200), width=1)
        draw.text((cx - 65, cy - 70), "SUWALKI GAP [65 KM]", fill=(0, 255, 200))
        draw.text((cx - 70, cy + 40), "POLAND // LITHUANIA BORDER", fill=(120, 220, 255))

        # 3. Strategic Rail Transit Line (1520mm Russian Broad-Gauge Corridor)
        rail_y = cy - 10
        draw.line([(cx - 220, rail_y), (cx + 220, rail_y)], fill=(255, 200, 60), width=2)
        for rx in range(cx - 210, cx + 220, 16):
            draw.line([(rx, rail_y - 6), (rx, rail_y + 6)], fill=(255, 220, 80), width=1)
        draw.text((cx - 110, rail_y - 24), "1520mm STRATEGIC TRANSIT RAIL CONDUIT", fill=(255, 220, 100))

        # 4. Kaliningrad Iskander-M Missile Threat Envelope (Overlapping Range Arcs)
        draw.arc([cx - 280, cy - 180, cx + 80, cy + 180], 300, 60, fill=(255, 60, 60), width=2)
        draw.text((cx - 60, cy - 160), "ISKANDER-M 500KM A2/AD BUBBLE", fill=(255, 80, 60))

        # Pincer Attack Vector Arrows (Northwest & Southeast pinching the Gap)
        # Top-down vector
        draw.line([(cx, cy - 130), (cx, cy - 90)], fill=(255, 60, 40), width=3)
        draw.polygon([(cx, cy - 85), (cx - 6, cy - 95), (cx + 6, cy - 95)], fill=(255, 60, 40))
        # Bottom-up vector
        draw.line([(cx, cy + 110), (cx, cy + 70)], fill=(255, 60, 40), width=3)
        draw.polygon([(cx, cy + 65), (cx - 6, cy + 75), (cx + 6, cy + 75)], fill=(255, 60, 40))
        draw.text((cx + 12, cy + 85), "TACTICAL PINCER", fill=(255, 80, 60))

        # 5. Telemetry Dossiers (Suwalki Metrics & Soviet Baltic War Plans)
        # Left HUD Box: Suwalki Chokepoint Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(22, 14, 12), outline=(255, 80, 60), width=1)
        draw.text((70, 98), "[SUWALKI GAP CHOKEPOINT HUD]", fill=(255, 90, 70))
        draw.text((70, 118), "CORRIDOR WIDTH: 65.4 KM", fill=(255, 200, 80))
        draw.text((70, 138), "RAIL STATUS: TRANSIT BYPASS RISK", fill=(255, 60, 60))
        draw.text((70, 158), "A2/AD ENVELOPE: OVERLAPPING", fill=(255, 160, 50))
        draw.text((70, 178), "DEFENSE TIME HORIZON: 72 HOURS", fill=(255, 100, 80))

        # Right HUD Box: Soviet Baltic Military District & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET BALTIC COMMAND]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "BALTIC MD RAPID INTERDICTION", fill=(255, 200, 80))
        draw.text((width - 310, 138), "KALININGRAD FLEET LOGISTICS", fill=(255, 100, 80))
        draw.text((width - 310, 158), "KGB RAIL SURVEILLANCE RINGS", fill=(255, 220, 120))
    elif theme in ("optomechanics_entanglement", "optomechanics", "membrane_entanglement", "laser_acoustics"):
        # Optomechanical Membrane Entanglement, Gravitational Decoherence & Laser Acoustics
        # 1. Background Optical Cavity Standing Wave Grid
        for gy in range(cy - 220, cy + 220, 24):
            draw.line([(60, gy), (width - 60, gy)], fill=(12, 24, 38), width=1)
        for gx in range(60, width - 60, 48):
            draw.line([(gx, cy - 220), (gx, cy + 220)], fill=(12, 24, 38), width=1)

        # 2. Fabry-Pérot Optical Cavity (Mirrors M1 and M2)
        cav_w = 400
        m1_x, m2_x = cx - cav_w//2, cx + cav_w//2
        cav_y = cy - 30
        cav_h = 120
        # Left Mirror M1 (Curved dielectric mirror)
        draw.rectangle([m1_x - 16, cav_y - cav_h//2, m1_x, cav_y + cav_h//2], fill=(20, 40, 60), outline=(0, 255, 240), width=2)
        draw.text((m1_x - 30, cav_y + cav_h//2 + 8), "MIRROR M1 [R > 99.99%]", fill=(0, 240, 255))

        # Right Mirror M2
        draw.rectangle([m2_x, cav_y - cav_h//2, m2_x + 16, cav_y + cav_h//2], fill=(20, 40, 60), outline=(0, 255, 240), width=2)
        draw.text((m2_x - 80, cav_y + cav_h//2 + 8), "MIRROR M2 [PIEZO-TUNED]", fill=(0, 240, 255))

        # Intracavity Standing Optical Wave (1064nm intra-cavity red/cyan photons)
        stand_pts = []
        for x_pos in range(m1_x, m2_x, 4):
            rel_ph = (x_pos - m1_x) * 0.12
            y_val = cav_y + int(36 * math.sin(rel_ph))
            stand_pts.append((x_pos, y_val))
        if len(stand_pts) > 1:
            draw.line(stand_pts, fill=(0, 255, 220), width=2)

        # 3. High-Stress Silicon Nitride Membrane (Si3N4) at Intra-cavity Node
        mem_x = cx
        mem_h = 100
        # Vibrating membrane line with quantum displacement amplitude
        draw.line([(mem_x, cav_y - mem_h//2), (mem_x, cav_y + mem_h//2)], fill=(255, 220, 60), width=3)
        # Membrane mechanical vibration envelope
        draw.ellipse([mem_x - 12, cav_y - 30, mem_x + 12, cav_y + 30], outline=(255, 180, 50), width=1)
        draw.text((mem_x - 65, cav_y - cav_h//2 - 22), "Si3N4 VIBRATING MEMBRANE", fill=(255, 220, 80))
        draw.text((mem_x - 60, cav_y + cav_h//2 - 12), "PHONON GROUND STATE: n < 0.2", fill=(255, 180, 50))

        # 4. Gravitational Decoherence & Self-Collapse Lower HUD Plot
        spec_x, spec_y = cx - 180, cy + 90
        spec_w, spec_h = 360, 75
        draw.rectangle([spec_x, spec_y, spec_x + spec_w, spec_y + spec_h], fill=(10, 18, 28), outline=(0, 200, 240), width=1)
        draw.text((spec_x + 10, spec_y + 6), "GRAVITATIONAL DECOHERENCE BOUND // DIÓSI-PENROSE COLLAPSE", fill=(0, 255, 220))
        # Quantum coherence vs mass-displacement curve
        dec_pts = []
        for sx in range(spec_w - 20):
            norm_x = sx / (spec_w - 20)
            amp_val = math.exp(-2.2 * norm_x) * math.cos(norm_x * 18)
            cy_val = spec_y + 38 - int(amp_val * 24)
            dec_pts.append((spec_x + 10 + sx, cy_val))
        if len(dec_pts) > 1:
            draw.line(dec_pts, fill=(255, 100, 80), width=2)
        draw.text((spec_x + spec_w - 130, spec_y + 45), "E_G = ℏ / τ_COLLAPSE", fill=(255, 220, 100))

        # 5. Telemetry Dossiers (Optomechanics & Soviet Laser Acoustics)
        # Left HUD Box: Optomechanical Metrics
        draw.rectangle([60, 90, 310, cy - 140], fill=(12, 22, 34), outline=(0, 220, 255), width=1)
        draw.text((70, 98), "[OPTOMECHANICS QUANTUM HUD]", fill=(0, 240, 255))
        draw.text((70, 118), "CAVITY FINESSE: F = 120,000", fill=(255, 220, 100))
        draw.text((70, 138), "COUPLING RATE: g_0 = 2π × 180 kHz", fill=(0, 255, 200))
        draw.text((70, 158), "ENTANGLEMENT: PHONON-PHOTON", fill=(120, 220, 255))
        draw.text((70, 178), "MACROSCOPIC MASS: 10 ng SUPERPOS", fill=(200, 140, 255))

        # Right HUD Box: Soviet Laser Acoustics & Yuri Shvets Disclosure
        draw.rectangle([width - 320, 90, width - 60, cy - 140], fill=(25, 15, 10), outline=(255, 120, 50), width=1)
        draw.text((width - 310, 98), "[SOVIET LASER ACOUSTICS]", fill=(255, 140, 50))
        draw.text((width - 310, 118), "KGB OTU WINDOW INTERFEROMETRY", fill=(255, 200, 80))
        draw.text((width - 310, 138), "SEABED OPTICAL HYDROPHONES", fill=(255, 100, 80))
        draw.text((width - 310, 158), "NON-ACOUSTIC SUB WAKE LASER", fill=(255, 220, 120))
        draw.text((width - 310, 178), "SOURCE: YURI SHVETS DOSSIER", fill=(0, 255, 220))

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
    elif theme in ("suwalki_gap", "kaliningrad_ew"):
        draw.text((40, 60), "SUWALKI CORRIDOR EW SIGINT // KALININGRAD ISKANDER-M TELEMETRY // 54.3°N, 23.3°E", fill=(255, 90, 60))
    elif theme in ("hormuz_spoofing", "hormuz_ew", "iran_drone", "hormuz_hydrophone", "persian_gulf"):
        draw.text((40, 60), "STRAIT OF HORMUZ ASW GATE // SEABED HYDROPHONE ARRAYS // SOVIET NAVAL DOCTRINE", fill=(255, 140, 40))
    elif theme in ("taiwan_sosus", "hydrophone_barrier", "taiwan_strait"):
        draw.text((40, 60), "TAIWAN STRAIT ASW CORRIDOR // SOSUS SEABED HYDROPHONE ARRAYS // COORD: 24.2°N, 119.8°E", fill=(0, 240, 255))
    elif theme in ("red_sea", "asbm", "anti_ship_missile", "red_sea_missile"):
        draw.text((40, 60), "RED SEA ASBM SALVOS // TELEMETRY RELAY SPOOFING // SOVIET NAVAL DOCTRINE", fill=(255, 140, 40))
    elif theme == "quantum":
        draw.text((40, 60), "QKD SATELLITE TELEMETRY // FREE-SPACE ENTANGLEMENT FIDELITY 99.4% // 1550nm DOWNLINK", fill=(0, 240, 255))
    elif theme == "bec":
        draw.text((40, 60), "BEC MICROGRAVITY ATOM INTERFEROMETRY // RUBIDIUM-87 CONDENSATE // TEMP: 50 PICOKELVIN", fill=(120, 220, 255))
    elif theme == "corruption":
        draw.text((40, 60), "DEFENSE PROCUREMENT FORENSICS // AUDIT TRAIL: COST-PLUS CARTELS // UNREDACTED", fill=(255, 90, 70))
    elif theme in ("black_budget", "sap_audit", "pentagon_sap", "gosplan_diversion"):
        draw.text((40, 60), "PENTAGON BLACK BUDGET FORENSICS // UNACKNOWLEDGED SAP PHANTOM AUDIT // GOSPLAN DIVERSION", fill=(255, 60, 60))
    elif theme in ("supply_chain_fraud", "subcontractor_grift", "defense_fraud", "aerospace_monopoly", "maintenance_cartel", "diagnostic_lockin", "defense_ai_cartel", "revolving_door", "advisory_collusion", "hypersonic_fraud", "scramjet_failure", "wind_tunnel_fraud", "cfd_falsification"):
        draw.text((40, 60), "DEFENSE PROCUREMENT FORENSICS // HYPERSONIC SCRAMJET FAILURE AUDIT // UNREDACTED", fill=(255, 60, 60))
    elif theme in ("rare_earths", "critical_minerals", "mineral_cartel", "tungsten_carbide", "munitions_fraud", "strategic_metals"):
        draw.text((40, 60), "STRATEGIC TUNGSTEN DIVERSION // MUNITIONS STOCKPILE DEFICIT // SOVIET LINE X METALS", fill=(255, 140, 40))
    elif theme in ("propellant_fraud", "nitrocellulose_cartel", "munitions_degradation"):
        draw.text((40, 60), "MUNITIONS PROPELLANT DEGRADATION // NITROCELLULOSE CARTEL // SOVIET SHELL ADULTERATION", fill=(255, 140, 40))
    elif theme in ("drone_gouging", "sbir_fraud", "tech_front_company"):
        draw.text((40, 60), "DRONE MUNITIONS PRICE GOUGING // SBIR FRAUD SYNDICATES // SOVIET TECH FRONTS", fill=(255, 60, 60))
    elif theme in ("counterfeit_chip", "microelectronics_fraud", "line_x"):
        draw.text((40, 60), "DEFENSE MICROELECTRONICS FORENSICS // COUNTERFEIT BROKER RINGS // LINE X INFILTRATION", fill=(255, 60, 60))
    elif theme in ("fuel_smuggling", "bunkering_fraud", "fuel_cartel", "oil_theft", "bunkering_price_fixing"):
        draw.text((40, 60), "DEFENSE FUEL LOGISTICS FORENSICS // NATO BUNKERING PRICE-FIXING CARTELS // BLACK SEA SIPHON", fill=(255, 140, 40))
    elif theme in ("casimir", "vacuum_thruster"):
        draw.text((40, 60), "DYNAMIC CASIMIR NANOCAVITY // ZERO-POINT VACUUM FLUCTUATION PRESSURE // ASYMMETRIC REACTION", fill=(255, 200, 60))
    elif theme in ("orbital_qkd", "space_sigint"):
        draw.text((40, 60), "ORBITAL QKD DOWNLINK // 1550nm ADAPTIVE OPTICS // 500KM LEO TRACK // GROUND SIGINT CONDUIT", fill=(0, 255, 200))
    elif theme in ("satellite_monopoly", "nro_recon", "space_recon", "satellite_imagery"):
        draw.text((40, 60), "SATELLITE IMAGERY MONOPOLY // NRO DUAL-USE PRIORITY OVERRIDES // SOVIET KOSMOS SIGINT", fill=(255, 140, 40))
    elif theme in ("holographic", "scrambler"):
        draw.text((40, 60), "HAYDEN-PRESKILL QUANTUM SCRAMBLING // EVENT HORIZON HAWKING EMISSION // ADS/CFT HORIZON", fill=(200, 160, 255))
    elif theme in ("smoky_dragon", "retrocausality"):
        draw.text((40, 60), "WHEELER'S SMOKY DRAGON // DELAYED-CHOICE INTERFEROMETER // DIRECTORATE S INFILTRATION AUDIT", fill=(0, 240, 255))
    elif theme in ("iit_phi", "causal_complex"):
        draw.text((40, 60), "INTEGRATED INFORMATION THEORY (IIT 4.0) // MAXIMAL CAUSAL COMPLEX Φ = 4.82 // LAB-12 TOXICOLOGY", fill=(255, 220, 60))
    elif theme in ("conscious_agents", "hoffman"):
        draw.text((40, 60), "CONSCIOUS AGENT DYNAMICS // MARKOVIAN TRANSITION KERNELS // SPACETIME PROJECTION MATRIX", fill=(0, 255, 220))
    elif theme in ("topological_superconductivity", "majorana_zero_modes", "majorana_nanowires", "landau_cryogenics"):
        draw.text((40, 60), "TOPOLOGICAL SUPERCONDUCTIVITY // MAJORANA ZERO MODES // SOVIET LANDAU CRYOGENIC SECRETS", fill=(0, 255, 240))
    elif theme in ("kagome_spin_liquid", "spin_liquid_theory"):
        draw.text((40, 60), "QUANTUM SPIN LIQUID // KAGOME ANTIFERROMAGNET // SOVIET SOLID-STATE THEORY AUDIT", fill=(0, 255, 240))
    elif theme in ("spin_liquid", "topological_braiding", "anyon_braiding", "topological_insulator", "topological_insulators", "helical_edge"):
        draw.text((40, 60), "TOPOLOGICAL INSULATOR // HELICAL EDGE STATES // SOVIET SOLID-STATE INTELLIGENCE AUDIT", fill=(0, 255, 220))
    elif theme in ("free_energy", "markov_blanket", "active_inference"):
        draw.text((40, 60), "FREE ENERGY PRINCIPLE // MARKOV BLANKET NEURAL INFERENCE // REFLEXIVE CONTROL MODEL", fill=(200, 140, 255))
    elif theme in ("p300_biometrics", "neuro_telemetry", "eeg_p300", "cognitive_load", "hft_neuro_feedback", "neuro_feedback", "trading_biometrics", "reflex_modification"):
        draw.text((40, 60), "EEG P300 BIOMETRIC SURVEILLANCE // COGNITIVE OVERLOAD TELEMETRY // KGB REFLEXIVE CONTROL", fill=(200, 140, 255))
    elif theme in ("focused_ultrasound", "ultrasound_neuromodulation", "sonoporation", "neuro_sonics"):
        draw.text((40, 60), "TRANSCRANIAL FOCUSED ULTRASOUND // BLOOD-BRAIN SONOPORATION // SOVIET NEURO-MODULATION", fill=(200, 140, 255))
    elif theme in ("big_toe", "digital_physics", "campbell_simulation", "cellular_automata"):
        draw.text((40, 60), "THOMAS CAMPBELL BIG TOE // DIGITAL CELLULAR AUTOMATA // KGB BIO-INFORMATION PSI ARCHIVES", fill=(200, 140, 255))
    elif theme in ("black_budget", "pentagon_sap", "sap_carveouts", "defense_audit", "failed_audit"):
        draw.text((40, 60), "UNACKNOWLEDGED SAP CARVE-OUTS // PENTAGON AUDIT BLACK HOLE // KGB OFF-BOOK SLUSH FUNDS", fill=(255, 100, 70))
    elif theme in ("logistics_fraud", "phantom_containers", "freight_grift", "warehouse_theft", "demurrage_fraud"):
        draw.text((40, 60), "DEFENSE LOGISTICS PHANTOM INVOICING // FREIGHT PASS-THROUGH SHELLS // SOVIET WAREHOUSE THEFT", fill=(255, 120, 50))
    elif theme in ("gibraltar_asw", "gibraltar_strait", "strait_of_gibraltar", "morocco_radar"):
        draw.text((40, 60), "STRAIT OF GIBRALTAR ASW BARRIER // THERMOCLINE ACOUSTIC BAFFLE // SOVIET 5TH ESKADRA INTEL", fill=(0, 240, 255))
    elif theme in ("red_sea_cables", "bab_el_mandeb"):
        draw.text((40, 60), "RED SEA SUBSEA CABLE CORRIDOR // BAB EL-MANDEB CHOKEPOINT // SOVIET HORN OF AFRICA SIGINT", fill=(255, 140, 40))
    elif theme in ("malacca_blockade", "hydrophone_gate", "malacca_strait"):
        draw.text((40, 60), "STRAIT OF MALACCA DRONE BLOCKADE // SUBSEA ACOUSTIC GATES // SOVIET NAVAL DOCTRINE", fill=(0, 220, 255))
    elif theme in ("suwalki_gap", "suwalki_corridor", "kaliningrad_corridor"):
        draw.text((40, 60), "SUWALKI GAP HEAVY ARMOR LOGISTICS // RAIL GAUGE CHOKEPOINTS // KALININGRAD CORRIDOR", fill=(255, 90, 70))
    elif theme in ("giuk_gap", "undersea_drones", "titanium_sub"):
        draw.text((40, 60), "GIUK GAP ACOUSTIC BARRIER // UNDERSEA DRONE SWARMS // SOVIET TITANIUM SUBMARINES", fill=(0, 220, 255))
    elif theme in ("kuril_bastion", "okhotsk_bastion", "kuril_islands", "sea_of_okhotsk"):
        draw.text((40, 60), "KURIL ISLANDS BASTION // SEA OF OKHOTSK ASW GATE // SOVIET PACIFIC FLEET DOCTRINE", fill=(255, 140, 40))
    elif theme in ("lomonosov_ridge", "arctic_seabed"):
        draw.text((40, 60), "ARCTIC LOMONOSOV RIDGE ANNEXATION // SEABED BATHYMETRY MAPPING // SOVIET POLAR BASTION ASW", fill=(0, 240, 255))
    elif theme in ("undersea_cable", "gugi_seabed", "seabed_warfare", "svalbard_cable", "barents_bastion", "bastion_doctrine", "northern_fleet"):
        draw.text((40, 60), "BARENTS BASTION ASW DOCTRINE // ARCTIC SOSUS TRENCH BAFFLES // NORTHERN FLEET SIGINT", fill=(255, 90, 70))
    elif theme in ("quantum_darwinism", "pointer_states", "theremin_bug"):
        draw.text((40, 60), "QUANTUM DARWINISM // POINTER STATE PROLIFERATION // THEREMIN CAVITY RESONATOR Q: 45K", fill=(0, 255, 240))
    elif theme in ("biophoton", "biophotonic", "mitogenetic_radiation", "bio_resonance"):
        draw.text((40, 60), "BIOPHOTONIC CELLULAR SIGNALING // MITOGENETIC RADIATION // SOVIET BIO-RESONANCE ARCHIVES", fill=(30, 240, 160))
    elif theme in ("orch_or", "penrose_hameroff", "tubulin_quantum", "synaptic_plasticity", "microtubules", "bio_cybernetics"):
        draw.text((40, 60), "QUANTUM SYNAPTIC PLASTICITY // MICROTUBULE ORCHESTRATION // KGB BIO-CYBERNETIC TELEMETRY", fill=(30, 240, 160))
    elif theme in ("nv_center", "diamond_magnetometry", "quantum_magnetometer", "nv_diamond", "nv_gravimetry", "quantum_gravimetry"):
        draw.text((40, 60), "QUANTUM DIAMOND NV GRAVIMETRY // SUBTERRANEAN BUNKER MAPPING // SOVIET ASW SENSORS", fill=(0, 240, 255))
    elif theme in ("rydberg", "rydberg_atom", "rydberg_rf", "quantum_rf"):
        draw.text((40, 60), "RYDBERG ATOM RF SENSOR // ELECTROMAGNETICALLY INDUCED TRANSPARENCY // SOVIET MICROWAVE SIGINT", fill=(0, 240, 255))
    elif theme in ("topological_photonics", "photonic_waveguide", "optical_computing"):
        draw.text((40, 60), "TOPOLOGICAL PHOTONIC WAVEGUIDES // QUANTUM HALL LIGHT ROUTING // SOVIET OPTICAL COMPUTING", fill=(0, 240, 255))
    elif theme in ("photonic_crystals", "laser_optics", "microcavity", "nonlinear_optics", "cavity_qed", "rabi_splitting", "microresonators", "atomic_laser"):
        draw.text((40, 60), "CAVITY QUANTUM ELECTRODYNAMICS // VACUUM RABI SPLITTING // SOVIET ATOMIC SPECTROSCOPY", fill=(0, 240, 255))
    elif theme in ("pear_reg", "cognitive_field", "anomalous_entanglement", "field_reg"):
        draw.text((40, 60), "PEAR QUANTUM NOISE REG // CUMULATIVE DEVIATION p = 3.8 x 10^-5 // KGB SLUSH AUDIT", fill=(255, 210, 50))
    elif theme in ("cat_state", "parity_measurement", "quantum_error_correction"):
        draw.text((40, 60), "BOSONIC CAT-STATE QUBITS // REAL-TIME PARITY MEASUREMENT // SOVIET QUANTUM SIGINT", fill=(0, 240, 255))
    elif theme in ("transmon_qubit", "surface_code", "quantum_cryptanalysis", "fault_tolerant_qc", "jpa", "quantum_amplifier", "squeezed_vacuum"):
        draw.text((40, 60), "JOSEPHSON PARAMETRIC AMPLIFIER // SQUEEZED VACUUM STATES // SOVIET RADAR SIGINT", fill=(0, 240, 255))
    elif theme in ("quantum_annealing", "flux_qubit", "adiabatic_quantum", "ising_spin", "fluxonium_qubit", "fluxonium", "phase_slip"):
        draw.text((40, 60), "SUPERCONDUCTING FLUXONIUM QUBIT // HIGH-HARMONIC PHASE SLIP // SOVIET CRYOGENICS ARCHIVES", fill=(0, 240, 255))
    elif theme in ("defense_cloud_fisa", "fisa_702", "cloud_lobbying", "jwcc"):
        draw.text((40, 60), "DEFENSE CLOUD LOBBYING // FISA 702 WARRANTLESS BACKDOORS // KGB OTU SURVEILLANCE", fill=(255, 100, 70))
    elif theme in ("gateway_hemisync", "hemisync", "monroe_gateway", "binaural_beat", "binaural_ffr", "eeg_microstates", "ffr", "telepathy_disinfo"):
        draw.text((40, 60), "MONROE GATEWAY HEMI-SYNC // BINAURAL 4.0Hz THETA COHERENCE // SOVIET PSYCHOTRONICS", fill=(200, 160, 255))
    elif theme in ("optomechanics", "drum_resonator", "mechanical_resonator", "optomechanical_entanglement", "quantum_drum"):
        draw.text((40, 60), "MACROSCOPIC DRUM ENTANGLEMENT // OPTOMECHANICAL PHASE NOISE SUPPRESSION // SOVIET LASER ESPIONAGE", fill=(0, 240, 255))
    elif theme in ("cv_qkd", "continuous_variable_qkd", "gaussian_modulation", "fiber_qkd"):
        draw.text((40, 60), "CONTINUOUS-VARIABLE QKD // GAUSSIAN MODULATION 1550nm // SOVIET CABLE-TAP CRYPTANALYSIS", fill=(0, 240, 255))
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
