package cipher

var key = []byte("ApocalypsAI_Beacon_Key_123") // Whimsical fixed key

// Encrypts the given data using a simple XOR cipher with a fixed key.
func Encrypt(data []byte) []byte {
	encrypted := make([]byte, len(data))
	for i := 0; i < len(data); i++ {
		encrypted[i] = data[i] ^ key[i%len(key)]
	}
	return encrypted
}

// Decrypts the given data. Since XOR is symmetric, it uses the same Encrypt function.
func Decrypt(data []byte) []byte {
	return Encrypt(data)
}
