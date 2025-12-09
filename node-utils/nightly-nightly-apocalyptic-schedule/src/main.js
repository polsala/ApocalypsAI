const { Command } = require('commander');
const { generateSchedule } = require('./schedule');

function createCLI() {
  const program = new Command();

  program
    .name('apocalyptic-schedule-gen')
    .description('Generate a whimsical apocalyptic schedule')
    .version('1.0.0')
    .action(() => {
      const schedule = generateSchedule();
      console.log(schedule.asciiArt);
      schedule.times.forEach(time => {
        console.log(`${time.time} - ${time.task}`);
      });
    });

  return program;
}

if (require.main === module) {
  createCLI().parse(process.argv);
}

module.exports = { createCLI };
