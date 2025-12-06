const fs = require('fs');
const path = require('path');

// Default inventory file (can be overridden for testing)
const DEFAULT_INVENTORY_PATH = path.join(__dirname, '..', 'inventory.json');

function loadInventory(inventoryPath = DEFAULT_INVENTORY_PATH) {
  try {
    const data = fs.readFileSync(inventoryPath, 'utf8');
    return JSON.parse(data);
  } catch (err) {
    // If file does not exist or is malformed, start with empty inventory
    return {};
  }
}

function saveInventory(inventory, inventoryPath = DEFAULT_INVENTORY_PATH) {
  const dir = path.dirname(inventoryPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(inventoryPath, JSON.stringify(inventory, null, 2), 'utf8');
}

function addItem(name, weight, inventoryPath = DEFAULT_INVENTORY_PATH) {
  if (!name) throw new Error('Item name is required');
  const w = parseFloat(weight);
  if (isNaN(w) || w <= 0) throw new Error('Weight must be a positive number');
  const inventory = loadInventory(inventoryPath);
  inventory[name] = w;
  saveInventory(inventory, inventoryPath);
  return inventory;
}

function removeItem(name, inventoryPath = DEFAULT_INVENTORY_PATH) {
  if (!name) throw new Error('Item name is required');
  const inventory = loadInventory(inventoryPath);
  if (inventory.hasOwnProperty(name)) {
    delete inventory[name];
    saveInventory(inventory, inventoryPath);
  }
  return inventory;
}

function listItems(inventoryPath = DEFAULT_INVENTORY_PATH) {
  const inventory = loadInventory(inventoryPath);
  return Object.entries(inventory).map(([name, weight]) => ({ name, weight }));
}

function totalWeight(inventoryPath = DEFAULT_INVENTORY_PATH) {
  const inventory = loadInventory(inventoryPath);
  return Object.values(inventory).reduce((sum, w) => sum + w, 0);
}

// CLI handling
if (require.main === module) {
  const [, , command, ...args] = process.argv;
  try {
    switch (command) {
      case 'add':
        if (args.length < 2) throw new Error('Usage: add <name> <weight>');
        addItem(args[0], args[1]);
        console.log(`Added \"${args[0]}\" (${args[1]} kg)`);
        break;
      case 'remove':
        if (args.length < 1) throw new Error('Usage: remove <name>');
        removeItem(args[0]);
        console.log(`Removed \"${args[0]}\"`);
        break;
      case 'list':
        const items = listItems();
        if (items.length === 0) console.log('Inventory is empty.');
        else items.forEach(i => console.log(`${i.name}: ${i.weight} kg`));
        break;
      case 'total':
        console.log(`Total weight: ${totalWeight()} kg`);
        break;
      default:
        console.error('Unknown command. Available: add, remove, list, total');
        process.exit(1);
    }
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { addItem, removeItem, listItems, totalWeight, loadInventory, saveInventory };
