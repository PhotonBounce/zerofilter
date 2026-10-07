import asyncio
import os
import edge_tts

VOICES = [
    {
        "id": "en-US-AvaMultilingualNeural",
        "name": "Ava (US Multilingual)",
        "desc": "Modern, authoritative, razor-sharp investigative tone with piercing clarity",
        "rate": "+5%",
        "pitch": "-1Hz"
    },
    {
        "id": "en-US-JennyNeural",
        "name": "Jenny (US National)",
        "desc": "Premier broadcast anchor cadence, energetic, expressive and punchy",
        "rate": "+6%",
        "pitch": "-2Hz"
    },
    {
        "id": "en-US-AriaNeural",
        "name": "Aria (US Investigative)",
        "desc": "Deep, resolute journalism standard, zero fluff, hard-hitting analytical pacing",
        "rate": "+5%",
        "pitch": "-2Hz"
    },
    {
        "id": "en-GB-SoniaNeural",
        "name": "Sonia (UK Intelligence)",
        "desc": "Sophisticated British broadcast intelligence aesthetic, crisp, calm and cynical",
        "rate": "+4%",
        "pitch": "-1Hz"
    },
    {
        "id": "en-US-EmmaMultilingualNeural",
        "name": "Emma (US Analytical)",
        "desc": "Intellectual clarity, composed, articulate, modern high-stakes delivery",
        "rate": "+5%",
        "pitch": "-1Hz"
    }
]

SAMPLE_TEXT = (
    "Welcome back to ZeroFilter. It is zero-four-hundred hours UTC. In Washington, NPR reports "
    "the FBI's counterintelligence divisions are falling behind as leadership redirects agents toward "
    "immigration sweeps, leaving foreign espionage operations unmonitored. Meanwhile, the War Department "
    "announced its directed-energy selections for the JIATF 401 pilot, betting on high-powered microwaves "
    "and combat lasers to down drone swarms. Dismantling counterspy units while handing defense contractors "
    "billions for directed energy is not national defense. It is systemic institutional decay."
)

async def synthesize(v):
    out_dir1 = "samples"
    out_dir2 = "web/samples"
    os.makedirs(out_dir1, exist_ok=True)
    os.makedirs(out_dir2, exist_ok=True)
    
    file_name = f"voice-{v['id']}.mp3"
    p1 = os.path.join(out_dir1, file_name)
    p2 = os.path.join(out_dir2, file_name)
    
    print(f"Synthesizing {v['name']} ({v['id']})...")
    comm = edge_tts.Communicate(text=SAMPLE_TEXT, voice=v["id"], rate=v["rate"], pitch=v["pitch"])
    audio = bytearray()
    async for chunk in comm.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
            
    with open(p1, "wb") as f:
        f.write(audio)
    with open(p2, "wb") as f:
        f.write(audio)
    print(f"  -> Saved {file_name} ({len(audio)} bytes)")

async def main():
    for v in VOICES:
        await synthesize(v)
    print("\nAll 5 female voice samples rendered successfully!")

if __name__ == "__main__":
    asyncio.run(main())
