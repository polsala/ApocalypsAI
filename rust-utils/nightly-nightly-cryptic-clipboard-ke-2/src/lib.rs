/// Performs a repeating‑key XOR on `data` using `key`.
///
/// The operation is symmetric: applying it twice with the same key
/// restores the original data.
pub fn xor(data: &[u8], key: &[u8]) -> Vec<u8> {
    let key_len = key.len();
    data.iter()
        .enumerate()
        .map(|(i, &b)| b ^ key[i % key_len])
        .collect()
}
