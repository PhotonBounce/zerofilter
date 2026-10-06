// categories.js — ZeroFilter content taxonomy & tag definitions

export const CATEGORIES = Object.freeze({
  "geopolitics": {
    id: "geopolitics",
    label: "Geopolitics",
    badgeClass: "category-badge",
    description: "Frontlines of Ukraine, Taiwan, anti-authoritarian defense, and theocracy exposed."
  },
  "quantum": {
    id: "quantum",
    label: "Quantum & AI",
    badgeClass: "category-badge",
    description: "Wheeler delayed choice, entanglement, quantum compute, and frontier AI reasoning."
  },
  "consciousness": {
    id: "consciousness",
    label: "Consciousness",
    badgeClass: "category-badge",
    description: "Declassified Project Stargate, PEAR lab data, Thomas Campbell, Monroe Gateway."
  },
  "corruption": {
    id: "corruption",
    label: "Corruption Exposed",
    badgeClass: "category-badge",
    description: "Bipartisan congressional graft, MAGA theocracy, and corporate Democratic hypocrisy."
  }
});

export function categoryOf(key) {
  return CATEGORIES[key] || CATEGORIES.geopolitics;
}
