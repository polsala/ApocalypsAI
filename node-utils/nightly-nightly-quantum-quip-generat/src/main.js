// Nightly Quantum Quip Generator
// A whimsical utility for generating quantum computing jokes

const jokes = require('./jokes.js');
const chalk = require('chalk');
const inquirer = require('inquirer');
const { Command } = require('commander');

/**
 * Quantum Quip Generator Class
 */
class QuantumQuipGenerator {
  constructor() {
    this.categories = this.getCategories();
  }

  /**
   * Get all available joke categories
   */
  getCategories() {
    const categories = new Set();
    jokes.forEach(joke => {
      categories.add(joke.category);
    });
    return Array.from(categories).sort();
  }

  /**
   * Generate a random joke
   * @param {Object} options - Generation options
   * @param {string} [options.category] - Specific category to filter by
   * @param {boolean} [options.explain] - Whether to include explanation
   * @param {string} [options.format] - Output format (text, json, markdown)
   * @returns {Object} Joke object with text and optional explanation
   */
  generateJoke(options = {}) {
    const { category, explain = false, format = 'text' } = options;

    // Filter jokes by category if specified
    let availableJokes = jokes;
    if (category) {
      availableJokes = jokes.filter(j => j.category.toLowerCase() === category.toLowerCase());
      if (availableJokes.length === 0) {
        throw new Error(`Category '${category}' not found. Available categories: ${this.categories.join(', ')}`);
      }
    }

    // Select random joke
    const randomIndex = Math.floor(Math.random() * availableJokes.length);
    const selectedJoke = availableJokes[randomIndex];

    // Build result object
    const result = {
      text: selectedJoke.text,
      category: selectedJoke.category,
      format: format
    };

    if (explain && selectedJoke.explanation) {
      result.explanation = selectedJoke.explanation;
    }

    return result;
  }

  /**
   * Format output based on specified format
   * @param {Object} joke - Joke object
   * @param {string} format - Output format
   * @returns {string} Formatted output
   */
  formatOutput(joke, format) {
    switch (format.toLowerCase()) {
      case 'json':
        return JSON.stringify(joke, null, 2);
      case 'markdown':
        let output = `## ${this.formatCategory(joke.category)} Joke\n\n${joke.text}\n`;
        if (joke.explanation) {
          output += `\n**Explanation:** ${joke.explanation}\n`;
        }
        return output;
      case 'text':
      default:
        let textOutput = joke.text;
        if (joke.explanation) {
          textOutput += `\n\nExplanation: ${joke.explanation}`;
        }
        return textOutput;
    }
  }

  /**
   * Format category name with proper capitalization
   * @param {string} category - Category name
   * @returns {string} Formatted category
   */
  formatCategory(category) {
    return category.charAt(0).toUpperCase() + category.slice(1);
  }

  /**
   * Run interactive mode
   */
  async interactiveMode() {
    console.log(chalk.cyan('\\nWelcome to the Quantum Quip Generator! \\U0001F9E0\\U0001F602'));
    console.log(chalk.gray('Press Ctrl+C to exit anytime\n'));

    while (true) {
      try {
        const answers = await inquirer.prompt([
          {
            type: 'list',
            name: 'action',
            message: 'What would you like to do?',
            choices: [
              'Generate random joke',
              'Generate joke by category',
              'Generate explained joke',
              'List categories',
              'Exit'
            ]
          }
        ]);

        switch (answers.action) {
          case 'Generate random joke':
            this.displayJoke(this.generateJoke());
            break;
          case 'Generate joke by category': {
            const categoryAnswer = await inquirer.prompt([
              {
                type: 'list',
                name: 'category',
                message: 'Select a category:',
                choices: this.categories
              }
            ]);
            this.displayJoke(this.generateJoke({ category: categoryAnswer.category }));
            break;
          }
          case 'Generate explained joke':
            this.displayJoke(this.generateJoke({ explain: true }));
            break;
          case 'List categories':
            console.log(chalk.yellow('\nAvailable categories:'));
            this.categories.forEach(cat => console.log(`  - ${this.formatCategory(cat)}`));
            console.log();
            break;
          case 'Exit':
            console.log(chalk.green('\nThanks for using the Quantum Quip Generator! Stay quantum! \\U0001F913'));
            return;
        }

        // Ask if user wants to continue
        const continueAnswer = await inquirer.prompt([
          {
            type: 'confirm',
            name: 'continue',
            message: 'Generate another joke?',
            default: true
          }
        ]);

        if (!continueAnswer.continue) {
          console.log(chalk.green('\nThanks for using the Quantum Quip Generator! Stay quantum! \\U0001F913'));
          return;
        }

      } catch (error) {
        if (error.isTtyError) {
          console.log(chalk.red('Prompt couldn\'t be rendered in this environment'));
        } else {
          console.log(chalk.red(`Error: ${error.message}`));
        }
      }
    }
  }

  /**
   * Display joke with appropriate formatting
   * @param {Object} joke - Joke object
   */
  displayJoke(joke) {
    console.log(chalk.blue('\n' + '='.repeat(50)));
    console.log(chalk.yellow(`Category: ${this.formatCategory(joke.category)}`));
    console.log(chalk.blue('='.repeat(50)));
    console.log(chalk.white(joke.text));
    
    if (joke.explanation) {
      console.log(chalk.gray('\n' + '-'.repeat(30)));
      console.log(chalk.gray(`Explanation: ${joke.explanation}`));
    }
    console.log(chalk.blue('='.repeat(50)) + '\n');
  }
}

/**
 * CLI Interface
 */
function createCLI() {
  const program = new Command();
  const generator = new QuantumQuipGenerator();

  program
    .name('quantum-quip')
    .description('Generate whimsical quantum computing jokes and explanations')
    .version('1.0.0');

  program
    .command('generate')
    .description('Generate a quantum computing joke')
    .option('-c, --category <category>', 'Filter jokes by category')
    .option('-e, --explain', 'Include explanation with the joke')
    .option('-f, --format <format>', 'Output format (text, json, markdown)', 'text')
    .action((options) => {
      try {
        const joke = generator.generateJoke(options);
        const output = generator.formatOutput(joke, options.format);
        console.log(output);
      } catch (error) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exit(1);
      }
    });

  program
    .command('list-categories')
    .description('List all available joke categories')
    .action(() => {
      console.log(chalk.yellow('\nAvailable categories:'));
      generator.categories.forEach(cat => {
        console.log(`  - ${generator.formatCategory(cat)}`);
      });
      console.log();
    });

  program
    .command('interactive')
    .description('Run in interactive mode')
    .action(async () => {
      try {
        await generator.interactiveMode();
      } catch (error) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exit(1);
      }
    });

  // Default command (generate)
  program
    .argument('[category]', 'Optional category filter')
    .option('-e, --explain', 'Include explanation')
    .option('-f, --format <format>', 'Output format', 'text')
    .action((category, options) => {
      try {
        const jokeOptions = {
          category: category || options.category,
          explain: options.explain,
          format: options.format
        };
        const joke = generator.generateJoke(jokeOptions);
        const output = generator.formatOutput(joke, jokeOptions.format);
        console.log(output);
      } catch (error) {
        console.error(chalk.red(`Error: ${error.message}`));
        process.exit(1);
      }
    });

  return program;
}

// Export for programmatic use
module.exports = {
  QuantumQuipGenerator,
  createCLI
};

// Run CLI if called directly
if (require.main === module) {
  const program = createCLI();
  program.parse();
}
