use nightly_cryptic_fortune::{hash_input, FORTUNES};

#[test]
fn test_hash_input() {
    assert_eq!(hash_input("hello"), 532); // h=104 e=101 l=108 l=108 o=111 => 532
    assert_eq!(hash_input("world"), 552); // w=119 o=111 r=114 l=108 d=100 => 552
}

#[test]
fn test_fortune_selection() {
    let index_hello = hash_input("hello") % FORTUNES.len();
    let index_world = hash_input("world") % FORTUNES.len();
    assert_ne!(index_hello, index_world);
}
