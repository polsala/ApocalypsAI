pub const FORTUNES: &[&str] = &[
    "The stars align in your favor today.",
    "A surprise awaits you at the corner.",
    "You will find what you seek in the unexpected.",
    "Patience is the key to unlocking mysteries.",
    "A new opportunity knocks on your door.",
];

pub fn hash_input(input: &str) -> usize {
    input.bytes().map(|b| b as usize).sum()
}
