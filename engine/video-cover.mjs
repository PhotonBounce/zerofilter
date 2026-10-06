// video-cover.mjs — 10s Looping Video Cover Generator for ZeroFilter

import { existsSync, readFileSync, writeFileSync } from "node:fs";

export const VEO_MODEL = "veo-2.0-generate-001";
export const VIDEO_DURATION_SECONDS = 10;
export const VIDEO_ASPECT_RATIO = "16:9";

export function buildVeoPayload(imageBase64, motionPrompt, duration = 10) {
  return {
    instances: [
      {
        prompt: motionPrompt || "Subtle cinematic ambient camera push-in, floating atmospheric dust particles, gentle ambient light pulse, continuous smooth looping motion, 16:9 4k photorealistic cinematic lighting, no text, no logos",
        image: {
          bytesBase64Encoded: imageBase64,
          mimeType: "image/webp"
        }
      }
    ],
    parameters: {
      aspectRatio: VIDEO_ASPECT_RATIO,
      durationSeconds: duration,
      sampleCount: 1
    }
  };
}

export function selfTest() {
  const dummy = Buffer.from("dummy").toString("base64");
  const payload = buildVeoPayload(dummy, "test motion", 10);
  
  if (!payload.instances?.[0]?.image?.bytesBase64Encoded) throw new Error("Missing image bytes");
  if (payload.parameters?.durationSeconds !== 10) throw new Error("Duration must be exactly 10s");
  if (payload.parameters?.aspectRatio !== "16:9") throw new Error("Aspect ratio must be 16:9");
  
  console.log("video-cover self-test: All checks passed OK.");
  return true;
}

if (process.argv.includes("--selftest")) {
  selfTest();
}
