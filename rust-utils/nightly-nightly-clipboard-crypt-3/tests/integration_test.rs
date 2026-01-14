#[cfg(test)]
mod integration {
    use std::process::Command;
    use std::str;

    #[test]
    fn encrypt_then_decrypt_roundtrip() {
        let pass = "apocalypse";
        let plaintext = "SecretMessage123!";

        // Encrypt
        let encrypt_output = Command::new("cargo")
            .args(&["run", "--quiet", "--", "-e", "-p", pass])
            .input(plaintext)
            .output()
            .expect("Failed to execute encrypt command");
        assert!(encrypt_output.status.success());
        let encrypted = str::from_utf8(&encrypt_output.stdout).unwrap().trim();
        assert!(!encrypted.is_empty());

        // Decrypt
        let decrypt_output = Command::new("cargo")
            .args(&["run", "--quiet", "--", "-d", "-p", pass])
            .input(encrypted)
            .output()
            .expect("Failed to execute decrypt command");
        assert!(decrypt_output.status.success());
        let decrypted = str::from_utf8(&decrypt_output.stdout).unwrap().trim();
        assert_eq!(decrypted, plaintext);
    }
}
