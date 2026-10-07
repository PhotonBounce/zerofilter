import sys
import os
import json
import asyncio
sys.path.insert(0, ".")
from engine.voice import synthesize_episode_audio, DEFAULT_VOICE, DEFAULT_RATE, DEFAULT_PITCH

EXPANSIONS = {
    "2026-10-03-12": [
        "Welcome to ZeroFilter. It is twelve-hundred hours UTC. In Washington, congressional auditors released a blistering assessment of the American defense industrial base, revealing persistent supply bottlenecks in artillery shell production and solid rocket motor propellants. While defense primes continue issuing tens of billions in corporate stock buybacks and executive bonuses, critical munitions pipelines remain backlogged by years. Taxpayers are subsidizing corporate financial engineering rather than sovereign production capacity, while key lawmakers on armed services subcommittees trade the exact defense equities they oversee.",
        "Across the Ukrainian battlespace, long-range domestic strike drones carried out a coordinated nocturnal operation against Russian ammunition depots and staging bases in occupied Luhansk. Forward telemetry confirms the destruction of multiple rail-bound supply transfers and hardened fuel caches deep behind the line of contact. As conventional artillery ammunition remains constrained by Western political delays, Ukraine's rapidly scaling domestic drone doctrine is neutralizing hostile logistics networks at a fraction of legacy military costs.",
        "Frontier compute and global infrastructure. An in-depth investigation in Nature documents the escalating physical bottleneck facing artificial intelligence scaling: power grid saturation and thermal dissipation limits. Training future frontier foundation models requires multi-gigawatt power substations, sparking fierce competition with regional domestic utilities and heavy manufacturing grids. Algorithmic expansion is no longer bounded by software ingenuity or raw silicon chips, but by the thermodynamic realities of electrical transmission and cooling infrastructure.",
        "Subatomic reality. A groundbreaking paper in Physical Review Letters demonstrates topological protection in Majorana zero-mode nanowire architectures, clearing a crucial obstacle on the roadmap to fault-tolerant quantum computing. Because topological quantum states store phase information non-locally across paired endpoints, they remain immune to the localized environmental noise that destabilizes conventional superconducting qubits. This experimental breakthrough brings resilient, room-temperature fault-tolerant quantum error correction within empirical experimental reach.",
        "Consciousness desk. Neuroscientists publishing in bioRxiv report direct causal evidence that the human claustrum acts as a central temporal synchronization hub, coordinating multi-sensory cortical binding during conscious perceptual states. Transient optogenetic inhibition of claustrum projections momentarily disrupts perceptual unity without inducing unconsciousness, indicating that subjective experience relies on continuous temporal phasing across distributed cortical zones. Human awareness is not a static property of mind, but an actively phase-locked neural broadcast.",
        "Here are tonight's verified receipts. Defense supply backlogs scrutinized while Ukrainian drones dismantle rear logistics. Power grids straining under foundation model compute. Topological qubits conquering quantum noise, and the claustrum mapped as the conductor of conscious awareness. Both corporate political factions profit directly by keeping you distracted, compliant, and numb. Reject their synthetic script. Check every source in the dossier drawer, verify the empirical data, and stay lucid. I'm Ava Vance."
    ]
}

async def main():
    manifest_path = "web/data/episodes.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for ep in data["episodes"]:
        if ep["id"] in EXPANSIONS:
            ep["paragraphs"] = EXPANSIONS[ep["id"]]
            wc = sum(len(p.split()) for p in ep["paragraphs"])
            print(f"Episode {ep['id']} expanded to {wc} words. Synthesizing audio...")
            out_audio = f"web/audio/{ep['id']}.mp3"
            seconds, cues = await synthesize_episode_audio(ep["paragraphs"], out_audio)
            ep["seconds"] = round(seconds)
            ep["cues"] = cues
            for frame, t in zip(ep["art"]["frames"], cues):
                frame["t"] = t
            print(f"  -> {ep['id']} audio updated: {seconds}s, cues: {cues}")
            
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("Done updating manifest!")

if __name__ == "__main__":
    asyncio.run(main())
