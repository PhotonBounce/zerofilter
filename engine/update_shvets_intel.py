# engine/update_shvets_intel.py
import json
import asyncio
import os
import edge_tts
import imageio_ffmpeg
import subprocess

MANIFEST_PATH = r"D:\zerofilter\web\data\episodes.json"
WEB_DIR = r"D:\zerofilter\web"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

def get_audio_duration_seconds(audio_path):
    cmd = [FFMPEG_EXE, "-i", audio_path, "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    import re
    match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return round(int(h) * 3600 + int(m) * 60 + float(s))
    return 180

async def update_and_resynthesize():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Ep 1 Paragraph 0
    data["episodes"][0]["paragraphs"][0] = (
        "Welcome to ZeroFilter. Put down the bipartisan kool-aid, check your cognitive biases at the door, "
        "and let's dissect the wreckage. As ex-KGB intelligence analyst and Washington dissident Yuri Shvets "
        "detailed in his latest intelligence brief, congressional disclosures confirm eighty-four lawmakers "
        "traded defense contractor stocks right before voting on weapons supplementals. The MAGA caucus postures "
        "as anti-establishment populists, but as Shvets exposes, they're taking dark-money PAC donations hand over "
        "fist from the same defense lobbyists they pretend to fight. And fuck establishment Democrats too—cashing "
        "checks from private equity while posturing on cable news."
    )

    # Ep 2 Paragraph 0
    data["episodes"][1]["paragraphs"][0] = (
        "Hour two of ZeroFilter. Let's peel back the domestic circus using Yuri Shvets' Washington counter-intelligence reports. "
        "Down in Texas and Oklahoma, white Christian nationalists are gutting public education and installing religious chaplains, "
        "while Russian active measures deliberately exploit American culture wars to paralyze governance. Shvets pointed out the cold "
        "receipts: demagogues distract working families with book bans while corporate lobbyists rob the treasury blind. "
        "And if you think the corporate Democratic machine is fighting back with anything more than empty fundraising emails, you're delusional."
    )

    # Ep 3 Paragraph 0
    data["episodes"][2]["paragraphs"][0] = (
        "Welcome to hour three of ZeroFilter. Looking at the Pacific theater through the lens of Yuri Shvets' national security analysis: "
        "while Washington politicians bicker over culture war nonsense, Chinese naval task forces have intensified blockade drills around Taiwan. "
        "Shvets documented how isolationist MAGA rhetoric directly serves Beijing and Moscow's strategic goal to dismantle American deterrence "
        "without firing a shot. The Taiwanese are hardening their semiconductor foundries into an unassailable silicon fortress, preparing "
        "mobile anti-ship missile batteries along every coastal approach. A Chinese invasion triggers an immediate twenty-trillion-dollar global collapse."
    )

    for ep in data["episodes"]:
        ep_id = ep["id"]
        out_audio = os.path.join(WEB_DIR, ep["audio"])
        full_text = "\n\n".join(ep["paragraphs"])
        print(f"Synthesizing Rex Vance audio with Yuri Shvets intel for [{ep_id}]...")
        comm = edge_tts.Communicate(full_text, "en-US-ChristopherNeural", rate="+10%", pitch="-2Hz")
        await comm.save(out_audio)
        dur = get_audio_duration_seconds(out_audio)
        ep["seconds"] = dur
        print(f"Finished [{ep_id}]: {dur}s")

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print("Successfully updated episodes.json and re-synthesized audio with Yuri Shvets intel!")

if __name__ == "__main__":
    asyncio.run(update_and_resynthesize())
