#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const PLANT_FILE = path.join(__dirname, '..', 'plant.json');

function savePlantData(data) {
    fs.writeFileSync(PLANT_FILE, JSON.stringify(data, null, 2));
}

function loadPlantData() {
    if (fs.existsSync(PLANT_FILE)) {
        return JSON.parse(fs.readFileSync(PLANT_FILE, 'utf8'));
    }
    return null;
}

function getDaysSince(dateString) {
    const lastDate = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - lastDate);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
}

function getPlantMood(daysSinceWatered, wateringFrequency) {
    if (daysSinceWatered <= wateringFrequency) {
        return {
            status: 'Happy',
            message: 'Your plant is thriving! Keep up the good work.'
        };
    } else if (daysSinceWatered <= wateringFrequency + 2) {
        return {
            status: 'Thirsty',
            message: 'Your plant looks a bit parched. Maybe a drink soon?'
        };
    } else if (daysSinceWatered <= wateringFrequency + 5) {
        return {
            status: 'Wilting',
            message: 'Oh no! Your plant is wilting. It desperately needs water!'
        };
    } else {
        return {
            status: 'Distressed',
            message: 'Your plant is in critical condition. Water immediately!'
        };
    }
}

function initPlant(name, frequency) {
    if (loadPlantData()) {
        console.log('You already have a plant! Use "check" or "water".');
        return;
    }
    const plantData = {
        name: name || 'Leafy',
        wateringFrequency: parseInt(frequency) || 3, // days
        lastWatered: new Date().toISOString().split('T')[0] // YYYY-MM-DD
    };
    savePlantData(plantData);
    console.log(`🌿 Welcome ${plantData.name}, your new desk plant pal!`);
    console.log(`Remember to water it every ${plantData.wateringFrequency} days.`);
}

function checkPlant() {
    const plantData = loadPlantData();
    if (!plantData) {
        console.log('No plant found. Use "init <name> [frequency]" to get one!');
        return;
    }

    const daysSinceWatered = getDaysSince(plantData.lastWatered);
    const mood = getPlantMood(daysSinceWatered, plantData.wateringFrequency);

    console.log(`\n--- ${plantData.name}'s Status ---`);
    console.log(`Last watered: ${plantData.lastWatered} (${daysSinceWatered} days ago)`);
    console.log(`Watering frequency: Every ${plantData.wateringFrequency} days`);
    console.log(`Current mood: ${mood.status}`);
    console.log(`Message: ${mood.message}`);

    if (daysSinceWatered > plantData.wateringFrequency) {
        console.log(`\n💧 It's time to water ${plantData.name}!`);
    } else {
        console.log(`\n✨ ${plantData.name} is doing great!`);
    }
}

function waterPlant() {
    const plantData = loadPlantData();
    if (!plantData) {
        console.log('No plant found. Use "init <name> [frequency]" to get one!');
        return;
    }

    plantData.lastWatered = new Date().toISOString().split('T')[0];
    savePlantData(plantData);
    console.log(`\n💦 You watered ${plantData.name}! It looks much happier now.`);
    checkPlant(); // Show updated status
}

function run() {
    const args = process.argv.slice(2);
    const command = args[0];

    switch (command) {
        case 'init':
            initPlant(args[1], args[2]);
            break;
        case 'check':
            checkPlant();
            break;
        case 'water':
            waterPlant();
            break;
        default:
            console.log('Usage:');
            console.log('  node src/index.js init <plant_name> [watering_frequency_days]');
            console.log('  node src/index.js check');
            console.log('  node src/index.js water');
            break;
    }
}

// Export for testing
module.exports = {
    run,
    _private: { // Expose private functions for testing purposes
        savePlantData,
        loadPlantData,
        getDaysSince,
        getPlantMood,
        PLANT_FILE
    }
};

// If run directly, execute the main function
if (require.main === module) {
    run();
}
