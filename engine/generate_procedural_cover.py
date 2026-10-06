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

    if theme in ("geopolitics", "red_sea", "suwalki_gap", "kaliningrad_ew", "hormuz_spoofing", "hormuz_ew", "iran_drone", "taiwan_sosus", "hydrophone_barrier", "taiwan_strait"):
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

    elif theme in ("supply_chain_fraud", "subcontractor_grift", "defense_fraud", "aerospace_monopoly", "maintenance_cartel", "diagnostic_lockin", "defense_ai_cartel", "revolving_door", "advisory_collusion", "hypersonic_fraud", "scramjet_failure", "black_budget", "sap_audit", "pentagon_sap", "gosplan_diversion", "rare_earths", "critical_minerals", "mineral_cartel", "drone_gouging", "sbir_fraud", "tech_front_company"):
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

    elif theme in ("spin_liquid", "topological_braiding", "anyon_braiding", "topological_insulator", "topological_insulators", "helical_edge", "topological_superconductivity", "majorana_zero_modes", "majorana_nanowires", "landau_cryogenics"):
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

    elif theme in ("undersea_cable", "gugi_seabed", "seabed_warfare", "arctic_seabed", "svalbard_cable", "red_sea_cables", "bab_el_mandeb", "barents_bastion", "bastion_doctrine", "northern_fleet", "giuk_gap", "undersea_drones", "titanium_sub"):
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

    elif theme in ("photonic_crystals", "laser_optics", "microcavity", "nonlinear_optics", "cavity_qed", "rabi_splitting", "microresonators", "atomic_laser", "nv_center", "diamond_magnetometry", "quantum_magnetometer", "nv_diamond"):
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

    elif theme in ("transmon_qubit", "surface_code", "quantum_cryptanalysis", "fault_tolerant_qc"):
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

    elif theme in ("gateway_hemisync", "hemisync", "monroe_gateway", "binaural_beat"):
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

    elif theme in ("quantum_annealing", "flux_qubit", "adiabatic_quantum", "ising_spin"):
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
    elif theme in ("hormuz_spoofing", "hormuz_ew", "iran_drone"):
        draw.text((40, 60), "STRAIT OF HORMUZ MARITIME EW // GNSS SPOOFING CIRCLES // COORD: 26.5°N, 56.2°E", fill=(255, 140, 40))
    elif theme in ("taiwan_sosus", "hydrophone_barrier", "taiwan_strait"):
        draw.text((40, 60), "TAIWAN STRAIT ASW CORRIDOR // SOSUS SEABED HYDROPHONE ARRAYS // COORD: 24.2°N, 119.8°E", fill=(0, 240, 255))
    elif theme == "red_sea":
        draw.text((40, 60), "RED SEA MARITIME STRIKE // BAB EL-MANDEB ASW CORRIDOR // COORD: 12.5°N, 43.3°E", fill=(255, 140, 40))
    elif theme == "quantum":
        draw.text((40, 60), "QKD SATELLITE TELEMETRY // FREE-SPACE ENTANGLEMENT FIDELITY 99.4% // 1550nm DOWNLINK", fill=(0, 240, 255))
    elif theme == "bec":
        draw.text((40, 60), "BEC MICROGRAVITY ATOM INTERFEROMETRY // RUBIDIUM-87 CONDENSATE // TEMP: 50 PICOKELVIN", fill=(120, 220, 255))
    elif theme == "corruption":
        draw.text((40, 60), "DEFENSE PROCUREMENT FORENSICS // AUDIT TRAIL: COST-PLUS CARTELS // UNREDACTED", fill=(255, 90, 70))
    elif theme in ("black_budget", "sap_audit", "pentagon_sap", "gosplan_diversion"):
        draw.text((40, 60), "PENTAGON BLACK BUDGET FORENSICS // UNACKNOWLEDGED SAP PHANTOM AUDIT // GOSPLAN DIVERSION", fill=(255, 60, 60))
    elif theme in ("supply_chain_fraud", "subcontractor_grift", "defense_fraud", "aerospace_monopoly", "maintenance_cartel", "diagnostic_lockin", "defense_ai_cartel", "revolving_door", "advisory_collusion", "hypersonic_fraud", "scramjet_failure"):
        draw.text((40, 60), "DEFENSE PROCUREMENT FORENSICS // HYPERSONIC SCRAMJET FAILURE AUDIT // UNREDACTED", fill=(255, 60, 60))
    elif theme in ("rare_earths", "critical_minerals", "mineral_cartel"):
        draw.text((40, 60), "CRITICAL MINERAL CHOKEPOINTS // DEFENSE STOCKPILE DEFICIT // SOVIET CARTEL ARBITRAGE", fill=(255, 140, 40))
    elif theme in ("drone_gouging", "sbir_fraud", "tech_front_company"):
        draw.text((40, 60), "DRONE MUNITIONS PRICE GOUGING // SBIR FRAUD SYNDICATES // SOVIET TECH FRONTS", fill=(255, 60, 60))
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
    elif theme in ("spin_liquid", "topological_braiding", "anyon_braiding", "topological_insulator", "topological_insulators", "helical_edge"):
        draw.text((40, 60), "TOPOLOGICAL INSULATOR // HELICAL EDGE STATES // SOVIET SOLID-STATE INTELLIGENCE AUDIT", fill=(0, 255, 220))
    elif theme in ("free_energy", "markov_blanket", "active_inference"):
        draw.text((40, 60), "FREE ENERGY PRINCIPLE // MARKOV BLANKET NEURAL INFERENCE // REFLEXIVE CONTROL MODEL", fill=(200, 140, 255))
    elif theme in ("hft_neuro_feedback", "neuro_feedback", "trading_biometrics", "reflex_modification"):
        draw.text((40, 60), "HFT NEURO-FEEDBACK BIOMETRICS // COGNITIVE FATIGUE TELEMETRY // KGB REFLEX MODIFICATION", fill=(200, 140, 255))
    elif theme in ("red_sea_cables", "bab_el_mandeb"):
        draw.text((40, 60), "RED SEA SUBSEA CABLE CORRIDOR // BAB EL-MANDEB CHOKEPOINT // SOVIET HORN OF AFRICA SIGINT", fill=(255, 140, 40))
    elif theme in ("giuk_gap", "undersea_drones", "titanium_sub"):
        draw.text((40, 60), "GIUK GAP ACOUSTIC BARRIER // UNDERSEA DRONE SWARMS // SOVIET TITANIUM SUBMARINES", fill=(0, 220, 255))
    elif theme in ("undersea_cable", "gugi_seabed", "seabed_warfare", "arctic_seabed", "svalbard_cable", "barents_bastion", "bastion_doctrine", "northern_fleet"):
        draw.text((40, 60), "BARENTS BASTION ASW DOCTRINE // ARCTIC SOSUS TRENCH BAFFLES // NORTHERN FLEET SIGINT", fill=(255, 90, 70))
    elif theme in ("quantum_darwinism", "pointer_states", "theremin_bug"):
        draw.text((40, 60), "QUANTUM DARWINISM // POINTER STATE PROLIFERATION // THEREMIN CAVITY RESONATOR Q: 45K", fill=(0, 255, 240))
    elif theme in ("biophoton", "biophotonic", "mitogenetic_radiation", "bio_resonance"):
        draw.text((40, 60), "BIOPHOTONIC CELLULAR SIGNALING // MITOGENETIC RADIATION // SOVIET BIO-RESONANCE ARCHIVES", fill=(30, 240, 160))
    elif theme in ("orch_or", "penrose_hameroff", "tubulin_quantum", "synaptic_plasticity", "microtubules", "bio_cybernetics"):
        draw.text((40, 60), "QUANTUM SYNAPTIC PLASTICITY // MICROTUBULE ORCHESTRATION // KGB BIO-CYBERNETIC TELEMETRY", fill=(30, 240, 160))
    elif theme in ("nv_center", "diamond_magnetometry", "quantum_magnetometer", "nv_diamond"):
        draw.text((40, 60), "QUANTUM DIAMOND NV MAGNETOMETRY // GPS-DENIED NAVIGATION // SOVIET SENSOR ESPIONAGE", fill=(0, 240, 255))
    elif theme in ("photonic_crystals", "laser_optics", "microcavity", "nonlinear_optics", "cavity_qed", "rabi_splitting", "microresonators", "atomic_laser"):
        draw.text((40, 60), "CAVITY QUANTUM ELECTRODYNAMICS // VACUUM RABI SPLITTING // SOVIET ATOMIC SPECTROSCOPY", fill=(0, 240, 255))
    elif theme in ("pear_reg", "cognitive_field", "anomalous_entanglement", "field_reg"):
        draw.text((40, 60), "PEAR QUANTUM NOISE REG // CUMULATIVE DEVIATION p = 3.8 x 10^-5 // KGB SLUSH AUDIT", fill=(255, 210, 50))
    elif theme in ("transmon_qubit", "surface_code", "quantum_cryptanalysis", "fault_tolerant_qc"):
        draw.text((40, 60), "SUPERCONDUCTING TRANSMON SURFACE CODE d=7 // 14.8mK CRYOSTAT // 8TH CHIEF SIGINT", fill=(0, 240, 255))
    elif theme in ("quantum_annealing", "flux_qubit", "adiabatic_quantum", "ising_spin"):
        draw.text((40, 60), "QUANTUM ANNEALING // PEGASUS FLUX QUBIT LATTICE // ADIABATIC TUNNELING // 8TH CHIEF", fill=(0, 240, 255))
    elif theme in ("defense_cloud_fisa", "fisa_702", "cloud_lobbying", "jwcc"):
        draw.text((40, 60), "DEFENSE CLOUD LOBBYING // FISA 702 WARRANTLESS BACKDOORS // KGB OTU SURVEILLANCE", fill=(255, 100, 70))
    elif theme in ("gateway_hemisync", "hemisync", "monroe_gateway", "binaural_beat"):
        draw.text((40, 60), "MONROE GATEWAY HEMI-SYNC // BINAURAL 4.0Hz THETA COHERENCE // SOVIET PSYCHOTRONICS", fill=(200, 160, 255))
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
