const { Command } = require('commander');
const { addDebt, repayDebt, listDebts, getTemporalBalance } = require('./ledger');

const program = new Command();

program
    .name('temporal-debt')
    .description('CLI to manage your whimsical temporal debts (borrowed time).')
    .version('1.0.0');

program
    .command('add <task> <hours> <repaymentDate>')
    .description('Add a new temporal debt. <repaymentDate> should be YYYY-MM-DD.')
    .action((task, hours, repaymentDate) => {
        try {
            const debt = addDebt(task, parseFloat(hours), repaymentDate);
            console.log(`Temporal debt "${debt.task}" of ${debt.borrowedHours} hours added. Repay by ${new Date(debt.repaymentTargetDate).toLocaleDateString()}. ID: ${debt.id}`);
        } catch (e) {
            console.error('Error adding debt:', e.message);
        }
    });

program
    .command('repay <id>')
    .description('Mark a temporal debt as repaid.')
    .action((id) => {
        const debt = repayDebt(id);
        if (debt) {
            console.log(`Temporal debt "${debt.task}" (ID: ${debt.id}) marked as repaid.`);
        } else {
            console.error(`Debt with ID "${id}" not found.`);
        }
    });

program
    .command('list')
    .description('List all temporal debts.')
    .action(() => {
        const debts = listDebts();
        if (debts.length === 0) {
            console.log('No temporal debts recorded. Your timeline is clear!');
            return;
        }
        console.log('--- Temporal Debt Ledger ---');
        debts.forEach(debt => {
            const status = debt.repaid ? 'REPAID' : 'OUTSTANDING';
            const repayDate = new Date(debt.repaymentTargetDate).toLocaleDateString();
            const borrowedDate = new Date(debt.borrowDate).toLocaleDateString();
            const repaidOn = debt.repaidDate ? ` (on ${new Date(debt.repaidDate).toLocaleDateString()})` : '';
            console.log(`ID: ${debt.id}`);
            console.log(`  Task: ${debt.task}`);
            console.log(`  Borrowed: ${debt.borrowedHours} hours (on ${borrowedDate})`);
            console.log(`  Repay by: ${repayDate}`);
            console.log(`  Status: ${status}${repaidOn}`);
            console.log('---');
        });
    });

program
    .command('balance')
    .description('Show your current temporal balance.')
    .action(() => {
        const balance = getTemporalBalance();
        console.log('--- Temporal Balance ---');
        console.log(`Total Hours Borrowed: ${balance.totalBorrowed}`);
        console.log(`Total Hours Repaid:   ${balance.totalRepaid}`);
        console.log(`Current Temporal Debt: ${balance.currentDebt} hours`);
        if (balance.currentDebt > 0) {
            console.log('You have outstanding temporal debts! Better start repaying...');
        } else if (balance.currentDebt < 0) {
            console.log('You have a temporal surplus! Perhaps you can lend some time?');
        } else {
            console.log('Your temporal ledger is perfectly balanced. As all things should be.');
        }
    });

program.parse(process.argv);
