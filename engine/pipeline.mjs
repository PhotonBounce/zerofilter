// pipeline.mjs — ZeroFilter Hourly Release Pipeline Orchestrator

import { readFileSync, writeFileSync } from "node:fs";
import { resolve, join } from "node:path";
import { validateEpisode } from "../web/js/episodes.js";
import { selfTest as testVideo } from "./video-cover.mjs";

console.log("=== ZeroFilter Pipeline Orchestrator ===");

const args = process.argv.slice(2);
const isDryRun = args.includes("--dry-run");

if (isDryRun) {
  console.log("Mode: Dry Run / Validation");
  testVideo();
  console.log("Pipeline dry run completed successfully.");
  process.exit(0);
}

console.log("To run automated hourly generation:");
console.log("  node pipeline.mjs --generate --date YYYY-MM-DD --hour HH:00");
