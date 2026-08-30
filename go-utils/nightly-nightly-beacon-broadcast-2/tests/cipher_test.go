package tests

import (
	"nightly-beacon-broadcast/src/cipher"
	"testing"
)

func TestCipher(t *testing.T) {
	original := "Hello, ApocalypsAI!"
	encrypted := cipher.Encrypt([]byte(original))
	decrypted := cipher.Decrypt(encrypted)

	if string(decrypted) != original {
		t.Errorf("Encryption/Decryption failed. Original: %s, Decrypted: %s", original, string(decrypted))
	}

	// Test with empty string
	empty := ""
	encryptedEmpty := cipher.Encrypt([]byte(empty))
	decryptedEmpty := cipher.Decrypt(encryptedEmpty)
	if string(decryptedEmpty) != empty {
		t.Errorf("Empty string encryption/decryption failed.")
	}

	// Test with different length, longer than the key
	longMsg := "This is a much longer message to test key wrapping and ensure it works correctly across different lengths. The key should cycle."
	encryptedLong := cipher.Encrypt([]byte(longMsg))
	decryptedLong := cipher.Decrypt(encryptedLong)
	if string(decryptedLong) != longMsg {
		t.Errorf("Long message encryption/decryption failed. Original: %s, Decrypted: %s", longMsg, string(decryptedLong))
	}
}
