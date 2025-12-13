const transports = [
    "Rust-bucket Hovercraft",
    "Temporal Rickshaw",
    "Quantum Skateboard",
    "Glow-worm Express",
    "Scrap-metal Strider",
    "Whisperwind Glider"
];

const destinations = [
    "The Whispering Wastes",
    "Glimmering Grotto",
    "The Forgotten Archives",
    "Echoing Canyons",
    "The Shifting Sands Bazaar",
    "Chronos's Clockwork Tower"
];

const anomalies = [
    "Minor Time Slip",
    "Echoes of the Past",
    "Future Vision Glitch",
    "Temporal Ripple",
    "Reality Flicker",
    "Deja Vu Loop"
];

function getRandomElement(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
}

function generateCommutePlan() {
    const transport = getRandomElement(transports);
    const destination = getRandomElement(destinations);
    const anomaly = getRandomElement(anomalies);

    return { transport, destination, anomaly };
}

if (require.main === module) {
    const plan = generateCommutePlan();
    console.log("--- Your Nightly Chrono-Commute Plan ---");
    console.log(`Mode of Transport: ${plan.transport}`);
    console.log(`Destination:       ${plan.destination}`);
    console.log(`Expected Anomaly:  ${plan.anomaly}`);
    console.log("---------------------------------------");
}

module.exports = { generateCommutePlan, transports, destinations, anomalies };
