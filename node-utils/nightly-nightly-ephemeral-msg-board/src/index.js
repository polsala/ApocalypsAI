const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, '..', 'data');
const DATA_FILE = path.join(DATA_DIR, 'messages.json');

// Ensure data directory exists when the module is loaded
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

/**
 * Loads messages from the data file.
 * @returns {Array<Object>} An array of message objects.
 */
function loadMessages() {
    if (!fs.existsSync(DATA_FILE)) {
        return [];
    }
    try {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error("Error loading messages:", error.message);
        return [];
    }
}

/**
 * Saves messages to the data file.
 * @param {Array<Object>} messages - The array of message objects to save.
 */
function saveMessages(messages) {
    try {
        fs.writeFileSync(DATA_FILE, JSON.stringify(messages, null, 2), 'utf8');
    } catch (error) {
        console.error("Error saving messages:", error.message);
    }
}

/**
 * Checks if a message has expired.
 * @param {Object} message - The message object.
 * @returns {boolean} True if the message has expired, false otherwise.
 */
function isMessageExpired(message) {
    const now = Date.now();
    if (message.ttl && message.timestamp + message.ttl * 60 * 1000 < now) {
        return true;
    }
    if (message.maxViews && message.views >= message.maxViews) {
        return true;
    }
    return false;
}

/**
 * Cleans up expired messages from the array.
 * @param {Array<Object>} messages - The array of message objects.
 * @returns {Array<Object>} A new array with only active messages.
 */
function cleanupMessages(messages) {
    return messages.filter(msg => !isMessageExpired(msg));
}

/**
 * Posts a new message.
 * @param {string} content - The message content.
 * @param {number} [ttl] - Time-to-live in minutes.
 * @param {number} [maxViews] - Maximum number of views.
 */
function postMessage(content, ttl, maxViews) {
    const messages = loadMessages();
    const newMessage = {
        id: Date.now().toString(), // Simple unique ID
        content,
        timestamp: Date.now(),
        ttl: ttl ? parseInt(ttl, 10) : undefined,
        maxViews: maxViews ? parseInt(maxViews, 10) : undefined,
        views: 0
    };
    messages.push(newMessage);
    saveMessages(messages);
    console.log("Message posted successfully.");
}

/**
 * Lists all active messages.
 */
function listMessages() {
    let messages = loadMessages();
    messages = cleanupMessages(messages); // Clean up before listing

    if (messages.length === 0) {
        console.log("No active messages found.");
        return;
    }

    console.log("\n--- Active Ephemeral Messages ---");
    messages.forEach((msg) => {
        console.log(`\nMessage ID: ${msg.id}`);
        console.log(`Content: ${msg.content}`);
        console.log(`Posted: ${new Date(msg.timestamp).toLocaleString()}`);
        if (msg.ttl) {
            const remainingTime = Math.ceil((msg.timestamp + msg.ttl * 60 * 1000 - Date.now()) / (60 * 1000));
            console.log(`Expires in: ${remainingTime} minutes`);
        }
        if (msg.maxViews) {
            console.log(`Views: ${msg.views}/${msg.maxViews}`);
        }

        // Increment view count for listed messages
        msg.views++;
    });
    console.log("\n---------------------------------");
    saveMessages(messages); // Save updated view counts
}

/**
 * Main CLI entry point.
 */
function main(args) {
    const command = args[2];
    const messageContent = args[3];
    const ttlIndex = args.indexOf('--ttl');
    const maxViewsIndex = args.indexOf('--max-views');

    const ttl = ttlIndex !== -1 ? args[ttlIndex + 1] : undefined;
    const maxViews = maxViewsIndex !== -1 ? args[maxViewsIndex + 1] : undefined;

    switch (command) {
        case 'post':
            if (!messageContent) {
                console.error("Error: Message content is required for 'post' command.");
                console.log("Usage: node src/index.js post \"Your message here\" [--ttl <minutes>] [--max-views <count>]");
                process.exit(1);
            }
            postMessage(messageContent, ttl, maxViews);
            break;
        case 'list':
            listMessages();
            break;
        case 'clean':
            let messages = loadMessages();
            const initialCount = messages.length;
            messages = cleanupMessages(messages);
            if (messages.length < initialCount) {
                saveMessages(messages);
                console.log(`Cleaned up ${initialCount - messages.length} expired messages.`);
            } else {
                console.log("No expired messages to clean up.");
            }
            break;
        default:
            console.log("Usage:");
            console.log("  node src/index.js post \"Your message here\" [--ttl <minutes>] [--max-views <count>]");
            console.log("  node src/index.js list");
            console.log("  node src/index.js clean");
            process.exit(1);
    }
}

// Only run main if this file is executed directly
if (require.main === module) {
    main(process.argv);
}

// Export functions for testing
module.exports = {
    loadMessages,
    saveMessages,
    isMessageExpired,
    cleanupMessages,
    postMessage,
    listMessages,
    main,
    DATA_FILE,
    DATA_DIR
};
