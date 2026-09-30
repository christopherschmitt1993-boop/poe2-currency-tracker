/*
 * PoE2 Precursor Tablet - Daten
 * ==============================
 * Quelle: craftofexile.com (Screenshots, manuell erfasst) + In-Game-Tooltips
 * fuer die Unique Tablets.
 *
 * Alle "normalen" (nicht-Unique) Tablet-Typen teilen sich denselben
 * PREFIX_POOL (13 Praefixe). Die Suffixe sind pro Typ unterschiedlich,
 * auch wenn sich ein Kern-Set (Azmeri Spirits/Essences/Rogue Exiles/
 * Shrines/Strongboxes/Summoning Circles-Chance + ein paar generische
 * Zeilen) durch fast alle Typen zieht.
 *
 * Diese Datei ist bewusst als einfaches, editierbares Datenobjekt gehalten -
 * bei einem Spiel-Patch koennen hier Zeilen ergaenzt/geaendert werden, ohne
 * den Rest von index.html anzufassen.
 */

const PREFIX_POOL = [
  "(10-15)% increased Effectiveness of Monsters in your Maps",
  "(12-18)% increased Experience gain in your Maps",
  "(25-35)% increased Gold found in your Maps",
  "(30-40)% increased Magic Monsters",
  "(15-20)% increased Monster Rarity",
  "(5-7)% increased Pack Size",
  "(25-35)% increased Rare Monsters",
  "(8-12)% increased Rarity of Items found",
  "Area contains 1 additional Azmeri Spirit",
  "Area contains an additional Summoning Circle",
  "Your Maps are inhabited by 1 additional Rogue Exile",
  "Your Maps contain (2-3) additional Rare Chests",
  "Your Maps contain an additional Essence",
];

const TABLET_TYPES = {
  abyss: {
    label: "Abyss Tablet",
    suffixes: [
      "(1-2) additional Rare Monsters are spawned from Abysses",
      "(20-30)% increased chance for Abyssal monsters to have Abyssal Modifiers",
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(20-30)% increased chance to find Desecrated Currency",
      "(30-40)% increased Quantity of Waystones found",
      "Abyss Pits in Area are twice as likely to have Rewards",
      "Abyssal Monsters have (8-12)% increased Effectiveness for each closed Pit, up to 100%",
      "Abysses have (10-20)% increased chance to lead to an Abyssal Depths",
      "Abysses have a (20-40)% chance to contain 4 additional Pits",
      "Abysses spawn (20-30)% increased Monsters",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Abyss",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  breach: {
    label: "Breach Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(5-20)% increased Effectiveness of Rare Breach Monsters",
      "(30-60)% increased Quantity of Hiveblood found",
      "(30-40)% increased Quantity of Waystones found",
      "(30-60)% increased Quantity of Wombgifts found",
      "Breaches have (5-15)% increased Monster density",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Unstable Breaches have (20-50)% increased chance to contain Vruun, Marshal of Xesht",
      "Unstable Breaches spawn (1-3) additional Rare Monsters when Stabilised",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  delirium: {
    label: "Delirium Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(15-30)% increased chance to manifest additional Unique Boss Shards within Delirium Fog",
      "(15-30)% increased Fracturing Mirrors manifested within Delirium Fog",
      "(30-40)% increased Quantity of Waystones found",
      "(15-30)% increased Stack size of Simulacrum Splinters found in your Maps",
      "Delirium Fog dissipates (20-30)% slower",
      "Delirium Fog in your Maps lasts (6-12) additional seconds before dissipating",
      "Delirium in your Maps increases (15-30)% faster with distance from the mirror",
      "Delirium Monsters in your Maps have (15-30)% increased Pack Size",
      "Slaying Rare Monsters in your Maps pauses the Delirium Mirror Timer for (3-5) seconds",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  expedition: {
    label: "Expedition Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(12-18)% increased Effect of Remnants in your Maps",
      "(15-30)% increased Expedition Explosive Placement Range",
      "(15-30)% increased Expedition Explosive Radius",
      "(25-40)% increased number of Rare Expedition Monsters",
      "(15-30)% increased number of Runic Monster Markers",
      "(15-30)% increased quantity of Artifacts dropped by Monsters in your Maps",
      "(15-30)% increased Quantity of Expedition Logbooks dropped by Runic Monsters in your Maps",
      "(30-40)% increased Quantity of Waystones found",
      "Expeditions in your Maps have +(1-2) Remnants",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  irradiated: {
    label: "Irradiated Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(30-40)% increased Quantity of Waystones found",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  overseer: {
    label: "Overseer Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(13-20)% increased Quantity of Items dropped by Map Bosses",
      "(18-30)% increased Quantity of Waystones dropped by Map Bosses",
      "(30-40)% increased Quantity of Waystones found",
      "(35-60)% increased Rarity of Items dropped by Map Bosses",
      "Areas with Powerful Map Bosses contain (1-2) additional Azmeri Spirits",
      "Areas with Powerful Map Bosses contain (1-2) additional Essences",
      "Areas with Powerful Map Bosses contain (1-2) additional Shrines",
      "Areas with Powerful Map Bosses contain (1-2) additional Strongboxes",
      "Map Bosses grant (40-80)% increased Experience",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  ritual: {
    label: "Ritual Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(30-40)% increased Quantity of Waystones found",
      "Deferring Favours at Ritual Altars in your Maps costs (20-30)% reduced Tribute",
      "Favours Deferred at Ritual Altars in your Maps reappear (25-40)% sooner",
      "Favours Rerolled at Ritual Altars in your Maps have (3-6)% chance to cost no Tribute",
      "Monsters Sacrificed at Ritual Altars grant (18-30)% increased Tribute",
      "Rerolling Favours at Ritual Altars costs (20-30)% reduced Tribute",
      "Revived Monsters from Ritual Altars have (35-70)% increased chance to be Magic",
      "Revived Monsters from Ritual Altars have (25-40)% increased chance to be Rare",
      "Ritual Altars allow rerolling Favours (1-3) additional times",
      "Ritual Favours in your Maps have (35-70)% increased chance to be Omens",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
  temple: {
    label: "Temple Tablet",
    suffixes: [
      "(70-100)% increased chance of Azmeri Spirits",
      "(70-100)% increased chance of Essences",
      "(70-100)% increased chance of Rogue Exiles",
      "(70-100)% increased chance of Shrines",
      "(70-100)% increased chance of Strongboxes",
      "(70-100)% increased chance of Summoning Circles",
      "(25-50)% increased chance Vaal Beacons summon additional Monsters",
      "(30-40)% increased Quantity of Waystones found",
      "Unique Monsters in your Maps have 1 additional Rare Modifier",
      "Your Maps contain an additional Shrine",
      "Your Maps contain an additional Strongbox",
      "Your Maps have (1-2) additional random Modifier",
    ],
  },
};

// Unique Tablets. "type" verweist auf den passenden Key in TABLET_TYPES
// (fuer Gruppierung im Dropdown). Roll-Ranges wo vom Nutzer angegeben,
// sonst als Fixwert/ohne Range uebernommen.
// TODO: Ritual-, Expedition- und Temple-Uniques fehlen noch (bei Bedarf ergaenzen).
const UNIQUE_TABLETS = [
  {
    name: "Unforeseen Consequences",
    type: "abyss",
    implicit: "Adds Abysses to a Map (1 use remaining)",
    mods: ["Map is overrun by the Abyssal - Map contains (14-18) additional Abysses"],
  },
  {
    name: "Wraeclast Besieged",
    type: "breach",
    implicit: "Adds an Otherworldy Breach to a Map (5 uses remaining)",
    mods: [
      "Breach Hives in Map have (2-5) additional waves of Hiveborn Monsters",
      "Breaches in Map have (-20-10)% increased/reduced Pack Size",
      "Unstable Breaches in Map take 120 additional seconds to collapse after timer is filled",
      "Unstable Breaches in Map spawn (2-5) additional Rare Monsters when Stabilised",
    ],
  },
  {
    name: "Clear Skies",
    type: "delirium",
    implicit: "Adds a Mirror of Delirium to a Map (5 uses remaining)",
    mods: [
      "Delirium Fog in your Maps never dissipates",
      "Delirium Fog in Map applies (-10-10)% increased/reduced Deliriousness to Players",
    ],
  },
  {
    name: "Mastered Domain",
    type: "irradiated",
    implicit: "Adds Irradiated to a Map (1 use remaining)",
    mods: [
      "[Expand] Area counts as <Random map biome> Biome " +
        "(Water / Mountain / Grass / Forest / Swamp / Desert Area)",
    ],
  },
  {
    name: "The Grand Project",
    type: "irradiated",
    implicit: "Adds Irradiated to a Map (1 use remaining)",
    mods: [
      "Can only be applied to Precursor Tower Maps",
      "Completing the Tower makes all nearby Maps accessible",
    ],
  },
  {
    name: "Visions of Paradise",
    type: "irradiated",
    implicit: "Adds Irradiated to a Map (1 use remaining)",
    mods: ["If Map was not previously Irradiated, completing Map adds Irradiation instead"],
  },
  {
    name: "Cruel Hegemony",
    type: "overseer",
    implicit: "Empowers the Map Boss of a Map (5 uses remaining)",
    mods: ["Map Bosses have 1 additional Modifier"],
  },
  {
    name: "Season of the Hunt",
    type: "overseer",
    implicit: "Empowers the Map Boss of a Map (5 uses remaining)",
    mods: ["Map Bosses are Hunted by Azmeri Spirits"],
  },
  {
    name: "Freedom of Faith",
    type: "ritual",
    implicit: "Adds Ritual Altars to a Map (5 uses remaining)",
    mods: [
      "Favours at Ritual Altars in Area costs (10-15)% increased Tribute",
      "Can Reroll Favours at Ritual Altars in your Maps twice as many times",
    ],
  },
];
