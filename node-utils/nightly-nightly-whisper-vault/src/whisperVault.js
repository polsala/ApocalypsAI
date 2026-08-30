const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class WhisperVault {
    constructor(vaultFilePath, encryptionKey) {
        this.vaultFilePath = vaultFilePath;
        this.encryptionKey = this._deriveKey(encryptionKey);
        this.algorithm = 'aes-256-cbc';
        this.vault = { whispers: [] };
        this._loadVault();
    }

    _deriveKey(key) {
        // Ensure key is 32 bytes for AES-256. Hash if necessary.
        if (key.length === 32) {
            return key;
        }
        return crypto.createHash('sha256').update(key).digest();
    }

    _encrypt(text) {
        const iv = crypto.randomBytes(16); // Initialization vector
        const cipher = crypto.createCipheriv(this.algorithm, this.encryptionKey, iv);
        let encrypted = cipher.update(text, 'utf8', 'hex');
        encrypted += cipher.final('hex');
        return { iv: iv.toString('hex'), encryptedData: encrypted };
    }

    _decrypt(encryptedData, ivHex) {
        const iv = Buffer.from(ivHex, 'hex');
        const decipher = crypto.createDecipheriv(this.algorithm, this.encryptionKey, iv);
        let decrypted = decipher.update(encryptedData, 'hex', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    }

    _loadVault() {
        if (fs.existsSync(this.vaultFilePath)) {
            try {
                const encryptedVault = fs.readFileSync(this.vaultFilePath, 'utf8');
                if (encryptedVault) {
                    const { iv, encryptedData } = JSON.parse(encryptedVault);
                    const decryptedContent = this._decrypt(encryptedData, iv);
                    this.vault = JSON.parse(decryptedContent);
                }
            } catch (error) {
                console.error("Error loading or decrypting vault. It might be corrupted or the key is wrong.", error.message);
                // Initialize with empty vault if decryption fails
                this.vault = { whispers: [] };
            }
        }
    }

    _saveVault() {
        const contentToEncrypt = JSON.stringify(this.vault);
        const { iv, encryptedData } = this._encrypt(contentToEncrypt);
        fs.writeFileSync(this.vaultFilePath, JSON.stringify({ iv, encryptedData }), 'utf8');
    }

    addWhisper(message, ttlHours = null) {
        const now = Date.now();
        const expiresAt = ttlHours ? now + ttlHours * 60 * 60 * 1000 : null;
        const id = crypto.randomUUID();
        const { iv, encryptedData } = this._encrypt(message);

        this.vault.whispers.push({
            id,
            encryptedContent: encryptedData,
            createdAt: now,
            expiresAt,
            iv
        });
        this._saveVault();
        return id;
    }

    listWhispers() {
        const now = Date.now();
        return this.vault.whispers
            .filter(w => !w.expiresAt || w.expiresAt > now)
            .map(w => ({
                id: w.id,
                createdAt: new Date(w.createdAt).toLocaleString(),
                expiresAt: w.expiresAt ? new Date(w.expiresAt).toLocaleString() : 'Never'
            }));
    }

    revealWhisper(id) {
        const now = Date.now();
        const whisper = this.vault.whispers.find(w => w.id === id);

        if (!whisper) {
            return null;
        }

        if (whisper.expiresAt && whisper.expiresAt <= now) {
            // Whisper has expired, remove it and return null
            this.vault.whispers = this.vault.whispers.filter(w => w.id !== id);
            this._saveVault();
            return null;
        }

        try {
            return this._decrypt(whisper.encryptedContent, whisper.iv);
        } catch (error) {
            console.error("Error decrypting whisper. Key might be wrong or data corrupted.", error.message);
            return null;
        }
    }

    purgeExpired() {
        const now = Date.now();
        const initialCount = this.vault.whispers.length;
        this.vault.whispers = this.vault.whispers.filter(w => !w.expiresAt || w.expiresAt > now);
        const purgedCount = initialCount - this.vault.whispers.length;
        if (purgedCount > 0) {
            this._saveVault();
        }
        return purgedCount;
    }
}

module.exports = WhisperVault;
