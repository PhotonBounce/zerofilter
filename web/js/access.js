// ZeroFilter Access Control & Monetization Engine
// Handles: 7-Day Free Trial, 50% Episode Preview Paywall, and Developer Unlimited Link

export const DEV_KEY_HASH = "a9ff673bb3d81b15848ee9f57311cddb50924f2d1dec970ded002f592afec529";
export const TRIAL_DURATION_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

// Pure SHA-256 helper compatible with both modern browser WebCrypto and Node.js
export async function hashKey(str) {
  if (!str) return null;
  if (typeof crypto !== "undefined" && crypto.subtle) {
    const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(str));
    return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
  }
  // Node.js fallback for unit test execution
  try {
    const nodeCrypto = await import("crypto");
    return nodeCrypto.createHash("sha256").update(str).digest("hex");
  } catch (_) {
    return null;
  }
}

export function checkAccess(storage = (typeof localStorage !== "undefined" ? localStorage : null), now = Date.now()) {
  if (!storage) {
    return { tier: "free", trialLeftMs: 0, isUnlocked: false, trialDaysLeft: 0 };
  }

  // Developer / VIP permanent bypass
  if (storage.getItem("zf_unlimited_dev") === "true") {
    return { tier: "developer", trialLeftMs: 0, isUnlocked: true, trialDaysLeft: 0 };
  }

  // First visit timestamp tracking
  let firstVisit = Number(storage.getItem("zf_first_visit"));
  if (!firstVisit || isNaN(firstVisit) || firstVisit <= 0) {
    firstVisit = now;
    storage.setItem("zf_first_visit", String(firstVisit));
  }

  const elapsed = Math.max(0, now - firstVisit);
  const trialLeftMs = Math.max(0, TRIAL_DURATION_MS - elapsed);
  const isTrial = trialLeftMs > 0;
  const trialDaysLeft = Math.ceil(trialLeftMs / (24 * 60 * 60 * 1000));

  return {
    tier: isTrial ? "trial" : "free",
    trialLeftMs,
    isUnlocked: isTrial,
    trialDaysLeft
  };
}

export function canPlayTime(currentTime, duration, accessState) {
  if (accessState.isUnlocked) return true;
  if (!duration || duration <= 0) return true;
  // Free post-trial tier: 50% cutoff
  return currentTime < (duration * 0.5);
}

export async function verifyAndApplyDevKey(candidateKey, storage = (typeof localStorage !== "undefined" ? localStorage : null)) {
  if (!candidateKey) return false;
  const hash = await hashKey(candidateKey.trim());
  if (hash === DEV_KEY_HASH) {
    if (storage) {
      storage.setItem("zf_unlimited_dev", "true");
      storage.setItem("zf_access_tier", "developer");
    }
    return true;
  }
  return false;
}
