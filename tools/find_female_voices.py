import asyncio
import edge_tts

async def main():
    voices = await edge_tts.list_voices()
    females = [v for v in voices if v.get("Gender") == "Female" and v.get("Locale", "").startswith("en-")]
    for v in females:
        print(f"{v['ShortName']:<35} | {v['Locale']:<10} | {v.get('FriendlyName', '')}")

if __name__ == "__main__":
    asyncio.run(main())
