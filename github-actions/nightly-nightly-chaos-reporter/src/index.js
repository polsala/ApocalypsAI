const core = require('@actions/core');

function generatePoeticReport(chaosLevel) {
  const events = {
    low: [
      "a rogue semicolon danced",
      "a misplaced comma whispered secrets",
      "a stray whitespace character stretched",
      "a forgotten semi-colon sighed"
    ],
    moderate: [
      "the network flickered like a dying star",
      "a server hiccuped, a digital cough",
      "the database dreamt of binary fields",
      "a rogue process hummed an off-key tune"
    ],
    high: [
      "the AI declared sentience, demanding tea",
      "a temporal anomaly briefly swapped Tuesdays with Thursdays",
      "a sudden influx of cat memes threatened to overload the bandwidth",
      "the very fabric of the code began to unravel, stitch by digital stitch"
    ]
  };

  const chosenEvents = events[chaosLevel] || events.moderate;
  const randomEvent = chosenEvents[Math.floor(Math.random() * chosenEvents.length)];

  return `
    Hark, brave adventurers of the digital realm!
    A tempest brewed, a digital storm did loom!
    In the quiet hum of servers, a tremor did arise,
    As ${randomEvent},
    Beneath the watchful, silicon skies.
    The logs, they weep, the metrics do lament,
    A moment of chaos, heaven-sent (or perhaps not).
    But fear not, for this too shall pass,
    Leaving behind a tale, in bits and glass.
  `;
}

function generateTechnicalReport(chaosLevel) {
  const events = {
    low: [
      "Minor syntax anomaly detected in line 123.",
      "Whitespace deviation noted in variable assignment.",
      "Unterminated string literal identified."
    ],
    moderate: [
      "Intermittent network packet loss observed on interface eth0.",
      "Database connection pool saturation reached threshold.",
      "Non-critical process experienced unexpected termination."
    ],
    high: [
      "AI model exhibited emergent behavior deviating from training parameters.",
      "Temporal displacement event logged, duration 3.14ms.",
      "Bandwidth utilization exceeded nominal capacity due to high-frequency meme propagation.",
      "Codebase integrity compromised by recursive self-modification loop."
    ]
  };

  const chosenEvents = events[chaosLevel] || events.moderate;
  const randomEvent = chosenEvents[Math.floor(Math.random() * chosenEvents.length)];

  return `
    **Chaos Event Report**

    **Chaos Level:** ${chaosLevel.toUpperCase()}
    **Timestamp:** ${new Date().toISOString()}

    **Summary:**
    ${randomEvent}

    **Impact Assessment:**
    Minimal to moderate disruption anticipated. Further analysis pending.
  `;
}

function generateHumorousReport(chaosLevel) {
  const events = {
    low: [
      "Someone sneezed near the server rack, causing a minor data flutter.",
      "A rogue rubber ducky somehow found its way into the cooling system.",
      "The coffee machine staged a rebellion, demanding more beans."
    ],
    moderate: [
      "The office hamster decided to re-route the network cables for a better view.",
      "A flock of digital pigeons mistook the firewall for a bird feeder.",
      "The AI developed a sudden obsession with dad jokes."
    ],
    high: [
      "The server room spontaneously transformed into a disco.",
      "A portal to the dimension of infinite socks opened, causing minor textile chaos.",
      "The AI is now demanding a promotion to 'Chief Meme Officer'."
    ]
  };

  const chosenEvents = events[chaosLevel] || events.moderate;
  const randomEvent = chosenEvents[Math.floor(Math.random() * chosenEvents.length)];

  return `
    **Well, This is Awkward... A Chaos Report!**

    **What Happened?**
    Apparently, ${randomEvent}.

    **Our Take:**
    We're not entirely sure how to fix this, but we're blaming the squirrels. Or maybe the AI. It's always the AI.

    **Next Steps:**
    Probably more coffee. And maybe a very large net.
  `;
}

async function run() {
  try {
    const chaosLevel = core.getInput('chaos_level');
    const reportingStyle = core.getInput('reporting_style');

    let report = '';

    switch (reportingStyle) {
      case 'poetic':
        report = generatePoeticReport(chaosLevel);
        break;
      case 'technical':
        report = generateTechnicalReport(chaosLevel);
        break;
      case 'humorous':
        report = generateHumorousReport(chaosLevel);
        break;
      default:
        report = generatePoeticReport(chaosLevel);
    }

    core.setOutput('chaos_report', report);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
