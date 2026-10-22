const fs = require('fs').promises;
const path = require('path');

async function getFileStats(filePath) {
    try {
        return await fs.stat(filePath);
    } catch (error) {
        // File might have been deleted between scan and stat, or permissions issue
        console.warn(`Could not get stats for ${filePath}: ${error.message}`);
        return null;
    }
}

function isFileOld(stats, thresholdDays) {
    if (!stats || !stats.isFile()) {
        return false;
    }
    const now = new Date();
    const mtime = stats.mtime; // Modification time
    const ageMs = now.getTime() - mtime.getTime();
    const ageDays = ageMs / (1000 * 60 * 60 * 24);
    return ageDays > thresholdDays;
}

async function findDigitalEchoes(directory, thresholdDays) {
    let echoes = [];
    try {
        const entries = await fs.readdir(directory, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(directory, entry.name);
            if (entry.isDirectory()) {
                echoes = echoes.concat(await findDigitalEchoes(fullPath, thresholdDays));
            } else if (entry.isFile()) {
                const stats = await getFileStats(fullPath);
                if (isFileOld(stats, thresholdDays)) {
                    echoes.push(fullPath);
                }
            }
        }
    } catch (error) {
        console.error(`Error scanning directory ${directory}: ${error.message}`);
    }
    return echoes;
}

async function archiveEcho(filePath, archiveDir, baseDirForRelativePath) {
    // baseDirForRelativePath is the directory from which the relative path should be calculated.
    // This ensures the archive structure mirrors the scanned directory's structure.
    const relativePath = path.relative(baseDirForRelativePath, filePath);
    const destPath = path.join(archiveDir, relativePath);
    const destDir = path.dirname(destPath);

    try {
        await fs.mkdir(destDir, { recursive: true });
        await fs.rename(filePath, destPath);
        return true;
    } catch (error) {
        console.error(`Failed to archive ${filePath}: ${error.message}`);
        return false;
    }
}

module.exports = {
    findDigitalEchoes,
    archiveEcho,
    isFileOld,
    getFileStats
};
