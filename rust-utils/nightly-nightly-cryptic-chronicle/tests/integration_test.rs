#[cfg(test)]
mod tests {
    use cryptic_chronicle::lib::{encrypt, decrypt};

    #[test]
    fn round_trip() {
        let key = "secret";
        let msg = "Hello, wasteland!";
        let ct = encrypt(msg, key);
        let (dec_msg, _ts) = decrypt(&ct, key).expect("decryption failed");
        assert_eq!(dec_msg, msg);
    }

    #[test]
    fn wrong_key_fails() {
        let key = "secret";
        let wrong = "wrongkey";
        let msg = "Test";
        let ct = encrypt(msg, key);
        let res = decrypt(&ct, wrong);
        assert!(res.is_err(), "Decryption with wrong key should error");
    }
}
