/// Caesar cipher implementation
/// Shifts each alphabetic character by the specified amount
/// Preserves case and non-alphabetic characters
pub fn caesar_cipher(text: &str, shift: i32) -> String {
    text.chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let shifted = ((c as u8 - base + shift as u8) % 26 + 26) % 26 + base;
                shifted as char
            } else {
                c
            }
        })
        .collect()
}

/// Atbash cipher implementation
/// Reverses the alphabet (A->Z, B->Y, etc.)
/// Preserves case and non-alphabetic characters
pub fn atbash_cipher(text: &str) -> String {
    text.chars()
        .map(|c| {
            if c.is_ascii_alphabetic() {
                let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
                let offset = c as u8 - base;
                let reversed = 25 - offset;
                (base + reversed) as char
            } else {
                c
            }
        })
        .collect()
}

/// Vigenère cipher implementation
/// Uses a repeating key to shift characters
/// Preserves case and non-alphabetic characters
pub fn vigenere_cipher(text: &str, key: &str) -> String {
    if key.is_empty() {
        return text.to_string();
    }
    
    let key_chars: Vec<char> = key.to_lowercase().chars().collect();
    let mut result = String::with_capacity(text.len());
    let mut key_index = 0;
    
    for c in text.chars() {
        if c.is_ascii_alphabetic() {
            let base = if c.is_ascii_uppercase() { b'A' } else { b'a' };
            let key_char = key_chars[key_index % key_chars.len()];
            let key_shift = key_char as u8 - b'a';
            
            let shifted = ((c as u8 - base + key_shift) % 26) + base;
            result.push(shifted as char);
            
            key_index += 1;
        } else {
            result.push(c);
        }
    }
    
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_caesar_cipher_basic() {
        assert_eq!(caesar_cipher("abc", 1), "bcd");
        assert_eq!(caesar_cipher("xyz", 1), "yza");
        assert_eq!(caesar_cipher("ABC", 1), "BCD");
        assert_eq!(caesar_cipher("XYZ", 1), "YZA");
    }

    #[test]
    fn test_caesar_cipher_negative_shift() {
        assert_eq!(caesar_cipher("bcd", -1), "abc");
        assert_eq!(caesar_cipher("yza", -1), "xyz");
        assert_eq!(caesar_cipher("BCD", -1), "ABC");
        assert_eq!(caesar_cipher("YZA", -1), "XYZ");
    }

    #[test]
    fn test_caesar_cipher_wraparound() {
        assert_eq!(caesar_cipher("z", 1), "a");
        assert_eq!(caesar_cipher("Z", 1), "A");
        assert_eq!(caesar_cipher("a", -1), "z");
        assert_eq!(caesar_cipher("A", -1), "Z");
    }

    #[test]
    fn test_caesar_cipher_non_alpha() {
        assert_eq!(caesar_cipher("hello, world!", 3), "khoor, zruog!");
        assert_eq!(caesar_cipher("123", 5), "123");
        assert_eq!(caesar_cipher("!@#", 10), "!@#");
    }

    #[test]
    fn test_caesar_cipher_empty() {
        assert_eq!(caesar_cipher("", 5), "");
    }

    #[test]
    fn test_atbash_cipher_basic() {
        assert_eq!(atbash_cipher("abc"), "zyx");
        assert_eq!(atbash_cipher("ABC"), "ZYX");
        assert_eq!(atbash_cipher("xyz"), "cba");
        assert_eq!(atbash_cipher("XYZ"), "CBA");
    }

    #[test]
    fn test_atbash_cipher_mixed() {
        assert_eq!(atbash_cipher("Hello, World!"), "Svool, Dliow!");
        assert_eq!(atbash_cipher("123!@#"), "123!@#");
    }

    #[test]
    fn test_atbash_cipher_empty() {
        assert_eq!(atbash_cipher(""), "");
    }

    #[test]
    fn test_vigenere_cipher_basic() {
        assert_eq!(vigenere_cipher("abc", "a"), "abc");
        assert_eq!(vigenere_cipher("abc", "b"), "bcd");
        assert_eq!(vigenere_cipher("abc", "c"), "ace");
    }

    #[test]
    fn test_vigenere_cipher_keyword() {
        assert_eq!(vigenere_cipher("attackatdawn", "lemon"), "lxfopvefrnhr");
        assert_eq!(vigenere_cipher("ATTACKATDAWN", "LEMON"), "LXFOPVEFRNHR");
    }

    #[test]
    fn test_vigenere_cipher_mixed() {
        assert_eq!(vigenere_cipher("Hello, World!", "key"), "Rivvk, Xkxvb!");
    }

    #[test]
    fn test_vigenere_cipher_empty_key() {
        assert_eq!(vigenere_cipher("hello", ""), "hello");
    }

    #[test]
    fn test_vigenere_cipher_empty_text() {
        assert_eq!(vigenere_cipher("", "key"), "");
    }
}
