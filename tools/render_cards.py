import os
from PIL import Image, ImageDraw, ImageFont

def create_radar_background(width=1376, height=768):
    im = Image.new("RGB", (width, height), (8, 11, 16))
    draw = ImageDraw.Draw(im)
    
    # Center of concentric radar circles on right
    cx, cy = 1180, 500
    
    # Draw radar circles
    for r in range(90, 850, 95):
        box = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(box, outline=(16, 42, 54), width=1)
        
    return im

def wrap_text(text, font, max_width, draw):
    words = text.split()
    lines = []
    curr = []
    for w in words:
        test_line = " ".join(curr + [w])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            curr.append(w)
        else:
            if curr:
                lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
    return lines

def render_cover_card(output_path, title, timestamp_text):
    im = create_radar_background()
    draw = ImageDraw.Draw(im)
    
    font_mono_header = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26)
    font_title = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 52)
    font_footer = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 20)
    
    # Header
    draw.text((72, 80), "ZERO//FILTER", fill=(255, 255, 255), font=font_mono_header)
    
    # Title
    lines = wrap_text(title, font_title, 950, draw)
    y = 260
    for line in lines:
        draw.text((72, y), line, fill=(255, 255, 255), font=font_title)
        y += 72
        
    # Footer
    draw.text((72, 680), timestamp_text, fill=(108, 122, 137), font=font_footer)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "WEBP", quality=92)
    print(f"Rendered: {output_path}")

def render_story_card(output_path, category, items, timestamp_text):
    im = create_radar_background()
    draw = ImageDraw.Draw(im)
    
    font_cat = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 24)
    font_top_right = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 22)
    font_headline = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 38)
    font_source = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 19)
    font_footer = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 20)
    
    # Category top left (cyan)
    draw.text((72, 75), category.upper(), fill=(0, 229, 255), font=font_cat)
    
    # Top right
    tr_text = f"ZERO//FILTER · {timestamp_text}"
    tr_bbox = draw.textbbox((0, 0), tr_text, font=font_top_right)
    draw.text((1376 - 72 - (tr_bbox[2] - tr_bbox[0]), 75), tr_text, fill=(108, 122, 137), font=font_top_right)
    
    # Headlines and sources
    y = 175
    for headline, src_meta in items:
        lines = wrap_text(headline, font_headline, 900, draw)
        for line in lines:
            draw.text((72, y), line, fill=(255, 255, 255), font=font_headline)
            y += 52
        y += 8
        draw.text((72, y), src_meta, fill=(108, 122, 137), font=font_source)
        y += 65
        
    # Bottom footer
    draw.text((72, 680), "Headlines as published by the sources · links in the episode's source drawer", fill=(108, 122, 137), font=font_footer)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    im.save(output_path, "WEBP", quality=92)
    print(f"Rendered: {output_path}")

def main():
    ep_id = "2026-10-07-04"
    time_str = "2026-10-07 04:00 UTC"
    
    # 1. Cover / Thumb
    thumb_path = f"web/thumbs/{ep_id}.webp"
    render_cover_card(
        thumb_path,
        "FBI Intel Cuts, Patriot Batteries in Poland & the Proton's Baryon Junction",
        f"{time_str} · sourced briefing"
    )
    
    # 2. Frame 1 (P0: US Politics / DoD)
    render_story_card(
        f"web/art/{ep_id}/f01.webp",
        "WASHINGTON",
        [
            ("As Trump focuses the FBI on immigration, counterintelligence is falling behind", "NPR · 2026-10-06"),
            ("Systems Selected for JIATF 401 Directed-Energy Counter-Drone Pilot Program", "U.S. War Department · 2026-10-05")
        ],
        time_str
    )
    
    # 3. Frame 2 (P1: Global Frontline)
    render_story_card(
        f"web/art/{ep_id}/f02.webp",
        "FRONTLINE",
        [
            ("Poland to deploy Patriots near Ukrainian border, announces $26 billion civil defense plan", "The Kyiv Independent · 2026-10-06"),
            ("Drones strike merchant vessels in Black Sea off Bulgaria, Ukraine, killing at least one", "The Kyiv Independent · 2026-10-06")
        ],
        time_str
    )
    
    # 4. Frame 3 (P2: AI & Frontier Compute)
    render_story_card(
        f"web/art/{ep_id}/f03.webp",
        "FRONTIER COMPUTE",
        [
            ("AI could undermine scientific independence in subtle ways", "Nature · 2026-10-06"),
            ("Algorithmic hypothesis synthesis & closed-pipeline bias analysis", "ZeroFilter Technical Analysis · 2026-10-07")
        ],
        time_str
    )
    
    # 5. Frame 4 (P3: Subatomic Physics & Delayed Choice)
    render_story_card(
        f"web/art/{ep_id}/f04.webp",
        "SUBATOMIC & QUANTUM",
        [
            ("Strong evidence that 'baryon junctions' give proton its identity", "Nature · 2026-10-06"),
            ("Experimental Realization of Wheeler's Delayed-Choice GedankenExperiment", "Science (Jacques et al.) · Reference 2007-02-16")
        ],
        time_str
    )
    
    # 6. Frame 5 (P4: Consciousness & Thalamic Routing)
    render_story_card(
        f"web/art/{ep_id}/f05.webp",
        "CONSCIOUSNESS & ANOMALIES",
        [
            ("Electrical stimulation of the human pulvinar generates visual percepts", "bioRxiv (Neuroscience) · 2026-10-06"),
            ("An Evaluation of Remote Viewing: Research and Applications (AIR Report)", "CIA Stargate Archive · Reference 1995-09-29")
        ],
        time_str
    )
    
    # 7. Frame 6 (P5: Synthesis & Receipts)
    render_story_card(
        f"web/art/{ep_id}/f06.webp",
        "INTELLIGENCE SYNTHESIS",
        [
            ("Sourced Briefing Complete: 9 Verified Receipts in Dossier", "ZeroFilter Intelligence Desk · Rex Vance"),
            ("All claims linked directly to official publications & peer-reviewed papers", "2026-10-07 04:00 UTC Broadcast")
        ],
        time_str
    )

if __name__ == "__main__":
    main()
