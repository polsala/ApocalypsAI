import { SnackManager } from './snackManager';
import { Snack } from './types';

const manager = new SnackManager();

function printSnack(snack: Snack): string {
  const expiration = new Date(snack.expirationDate);
  const now = new Date();
  now.setHours(0, 0, 0, 0); // Compare only date part
  const diffTime = expiration.getTime() - now.getTime();
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

  let status = '';
  if (diffDays < 0) {
    status = `(EXPIRED ${Math.abs(diffDays)} days ago!)`;
  } else if (diffDays === 0) {
    status = `(Expires TODAY!)`;
  } else if (diffDays === 1) {
    status = `(Expires in 1 day)`;
  } else {
    status = `(Expires in ${diffDays} days)`;
  }

  return `ID: ${snack.id}\n  Name: ${snack.name}\n  Quantity: ${snack.quantity}\n  Expires: ${snack.expirationDate} ${status}\n`;
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case 'add':
        if (args.length !== 4) {
          console.log('Usage: npm start add <name> <quantity> <expiration-date>');
          process.exit(1);
        }
        const name = args[1];
        const quantity = parseInt(args[2], 10);
        const expirationDate = args[3];
        const newSnack = manager.addSnack(name, quantity, expirationDate);
        console.log(`Added snack: ${newSnack.name} (ID: ${newSnack.id})`);
        break;

      case 'list':
        const snacks = manager.listSnacks();
        if (snacks.length === 0) {
          console.log('Your temporal snack stash is empty. Time to scavenge!');
        } else {
          console.log('--- Temporal Snack Stash ---');
          snacks.forEach(snack => console.log(printSnack(snack)));
          console.log('----------------------------');
        }
        break;

      case 'eat':
        if (args.length !== 3) {
          console.log('Usage: npm start eat <snack-id> <quantity-to-eat>');
          process.exit(1);
        }
        const idToEat = args[1];
        const quantityToEat = parseInt(args[2], 10);
        const eatenSnack = manager.eatSnack(idToEat, quantityToEat);
        if (eatenSnack) {
          if (eatenSnack.quantity === 0) {
            console.log(`Fully consumed ${eatenSnack.name}. Delicious!`);
          } else {
            console.log(`Ate ${quantityToEat} of ${eatenSnack.name}. ${eatenSnack.quantity} remaining.`);
          }
        } else {
          console.log(`Snack with ID ${idToEat} not found.`);
        }
        break;

      case 'suggest':
        const suggestedSnacks = manager.suggestSnacks();
        if (suggestedSnacks.length === 0) {
          console.log('No snacks needing urgent consumption. All good for now!');
        } else {
          console.log('--- Suggested Snacks (Eat Soon!) ---');
          suggestedSnacks.forEach(snack => console.log(printSnack(snack)));
          console.log('------------------------------------');
        }
        break;

      default:
        console.log('Unknown command. Available commands: add, list, eat, suggest');
        process.exit(1);
    }
  } catch (error: any) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
