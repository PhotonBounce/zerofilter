import os
import glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

TARGET_W, TARGET_H = 1376, 768

IMAGE_MAP = {
    "2026-10-01-12": ("ep_2026_10_01_cover_*.jpg", "Black Sea Asymmetric Defense, Sanctions Loopholes & Relativistic Quantum Clocks"),
    "2026-10-02-12": ("ep_2026_10_02_cover_*.jpg", "Strategic Air Defenses in Kyiv, Defense Contracting Monopolies & Macroscopic Entanglement"),
    "2026-10-03-12": ("ep_2026_10_03_cover_*.jpg", "Long-Range Drone Interdiction, Export Control Failures & Non-Local Quantum Telemetry"),
    "2026-10-04-12": ("ep_2026_10_04_cover_*.jpg", "Critical Infrastructure Hardening, Pentagon Supply Chain Audits & Topological Qubits"),
    "2026-10-05-12": ("ep_2026_10_05_cover_*.jpg", "Naval Strike Corridor Neutralization, Congressional Defense Trades & Delayed-Choice Erasers"),
    "2026-10-07-12": ("ep_2026_10_07_cover_*.jpg", "Orbital Reconnaissance Satellites, Electronic Warfare Vectors & Superconducting Qubit Networks"),
}

ARTIFACT_DIR = r"C:\Users\fucktrumpandrednecks\.gemini\antigravity-ide\brain\ec7d1274-aa5d-41b0-a439-acd899042a8d"

def process_cover(ep_id, pattern, title):
    matches = glob.glob(os.path.join(ARTIFACT_DIR, pattern))
    if not matches:
        print(f"No match for {pattern}")
        return
    src_file = matches[-1]
    
    im = Image.open(src_file)
    im = im.resize((TARGET_W, TARGET_H), Image.Resampling.LANCZOS)
    
    # Slight contrast enhancement & dark gradient overlay for HUD contrast
    enhancer = ImageEnhance.Contrast(im)
    im = enhancer.enhance(1.12)
    
    overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)
    
    # Gradient on top and bottom for text legibility
    for y in range(160):
        alpha = int((1.0 - y / 160.0) * 180)
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(8, 11, 16, alpha))
        
    for y in range(TARGET_H - 140, TARGET_H):
        alpha = int(((y - (TARGET_H - 140)) / 140.0) * 200)
        draw_ov.line([(0, y), (TARGET_W, y)], fill=(8, 11, 16, alpha))
        
    im = Image.alpha_composite(im.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(im)
    
    font_mono_header = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 26)
    font_footer = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 20)
    
    # Header HUD
    draw.text((72, 50), "ZERO//FILTER", fill=(255, 255, 255), font=font_mono_header)
    date_str = ep_id[:10]
    draw.text((TARGET_W - 380, 50), f"{date_str} 12:00 UTC · BRIEFING", fill=(0, 229, 255), font=font_footer)
    
    # Footer
    draw.text((72, TARGET_H - 60), f"CLASSIFIED SOURCED BRIEFING // REX & AVA VANCE // DECLASSIFIED RECEIPTS", fill=(160, 175, 195), font=font_footer)
    
    out_path = f"web/thumbs/{ep_id}.webp"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    im.save(out_path, "WEBP", quality=92)
    print(f"Processed cover: {out_path} ({TARGET_W}x{TARGET_H})")
    
    # Also copy 10s cover video loop
    mp4_path = f"web/thumbs/{ep_id}.mp4"
    if not os.path.exists(mp4_path):
        import shutil
        shutil.copy("web/thumbs/2026-10-06-22.mp4", mp4_path)
        print(f"Copied cover video: {mp4_path}")

def main():
    for ep_id, (pat, title) in IMAGE_MAP.items():
        process_cover(ep_id, pat, title)

if __name__ == "__main__":
    main()
