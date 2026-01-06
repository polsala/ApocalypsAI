const fs = require('fs').promises;
const path = require('path');

async function findDustBunnies(dirPath, maxSizeKB = 10) {
    const dustBunnies = [];
    const maxSize = maxSizeKB * 1024; // Convert KB to bytes

    async function traverse(currentPath) {
        let entries;
        try {
            entries = await fs.readdir(currentPath, { withFileTypes: true });
        } catch (error) {
            // console.warn(`Could not read directory ${currentPath}: ${error.message}`);
            return; // Skip unreadable directories
        }

        for (const entry of entries) {
            const fullPath = path.join(currentPath, entry.name);
            if (entry.isDirectory()) {
                if (entry.name !== 'node_modules' && entry.name !== '.git') { // Avoid common large dirs
                    await traverse(fullPath);
                }
            } else if (entry.isFile()) {
                let stats;
                try {
                    stats = await fs.stat(fullPath);
                } catch (error) {
                    // console.warn(`Could not stat file ${fullPath}: ${error.message}`);
                    continue; // Skip unreadable files
                }

                if (stats.size > 0 && stats.size <= maxSize) {
                    dustBunnies.push({
                        path: fullPath,
                        size: stats.size,
                        extension: path.extname(entry.name).toLowerCase(),
                        name: entry.name
                    });
                }
            }
        }
    }

    await traverse(dirPath);
    return dustBunnies;
}

function categorizeDustBunnies(dustBunnies) {
    const categories = {
        'logs': ['.log', '.txt', '.md'],
        'temp': ['.tmp', '.temp', '.bak', '.old', '.swp'],
        'images': ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico'],
        'code': ['.js', '.json', '.ts', '.jsx', '.tsx', '.py', '.java', '.c', '.cpp', '.h', '.html', '.css', '.scss', '.less', '.yml', '.yaml', '.xml', '.sh', '.bat'],
        'documents': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.rtf'],
        'archives': ['.zip', '.tar', '.gz', '.rar', '.7z'],
        'other': [] // Default category
    };

    const categorized = {};
    for (const categoryName in categories) {
        categorized[categoryName] = [];
    }

    for (const bunny of dustBunnies) {
        let assigned = false;
        for (const categoryName in categories) {
            if (categories[categoryName].includes(bunny.extension)) {
                categorized[categoryName].push(bunny);
                assigned = true;
                break;
            }
        }
        if (!assigned) {
            categorized['other'].push(bunny);
        }
    }
    return categorized;
}

function generateReport(categorizedBunnies, baseDir) {
    let report = `Digital Dust Bunny Report for: ${baseDir}\n`;
    report += `========================================\n\n`;

    let totalBunnies = 0;
    let totalSize = 0;

    for (const category in categorizedBunnies) {
        const bunnies = categorizedBunnies[category];
        if (bunnies.length > 0) {
            report += `Category: ${category.toUpperCase()} (${bunnies.length} files)\n`;
            const categorySize = bunnies.reduce((sum, b) => sum + b.size, 0);
            report += `  Total Size: ${(categorySize / 1024).toFixed(2)} KB\n`;
            report += `  Files:\n`;
            bunnies.forEach(bunny => {
                report += `    - ${path.relative(baseDir, bunny.path)} (${(bunny.size / 1024).toFixed(2)} KB)\n`;
            });
            report += '\n';
            totalBunnies += bunnies.length;
            totalSize += categorySize;
        }
    }

    report += `----------------------------------------\n`;
    report += `Summary:\n`;
    report += `  Total Dust Bunnies Found: ${totalBunnies}\n`;
    report += `  Total Size: ${(totalSize / 1024).toFixed(2)} KB\n`;
    report += `========================================\n`;

    return report;
}

async function run(dirPath, maxSizeKB) {
    const dustBunnies = await findDustBunnies(dirPath, maxSizeKB);
    const categorized = categorizeDustBunnies(dustBunnies);
    const report = generateReport(categorized, dirPath);
    console.log(report);
    return { dustBunnies, categorized, report }; // Return for testing
}

if (require.main === module) {
    const args = process.argv.slice(2);
    const targetDir = args[0] || process.cwd();
    const sizeArg = parseInt(args[1], 10);
    const maxSize = isNaN(sizeArg) || sizeArg <= 0 ? 10 : sizeArg; // Default 10KB

    console.log(`Scanning '${targetDir}' for files <= ${maxSize}KB...`);
    run(targetDir, maxSize).catch(console.error);
}

module.exports = { findDustBunnies, categorizeDustBunnies, generateReport, run };
