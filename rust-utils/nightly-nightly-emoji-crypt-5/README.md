nightly-emoji-crypt

Encode and decode strings to a whimsical emoji cipher.

Usage:

  Encode a phrase:
    nightly-emoji-crypt encode "hello world"

  Decode an emoji string:
    nightly-emoji-crypt decode "😉😄😄😅🟦😗😄😅😅"

The tool maps each lower‑case letter a‑z to a distinct emoji and maps a space to a blue square. Characters outside a‑z and space are passed through unchanged.

Mapping (letter → emoji):
  a → 😀   b → 😁   c → 😂   d → 😃   e → 😄   f → 😅   g → 😆   h → 😉   i → 😊   j → 😋
  k → 😎   l → 😍   m → 😘   n → 🥰   o → 😗   p → 😙   q → 😚   r → ☺️   s → 🤗   t → 🤩
  u → 🤔   v → 🤨   w → 😐   x → 😑   y → 😶   z → 🙄   space → 🟦

The binary is built with Cargo. Run `cargo build --release` and the executable will appear in `target/release/nightly-emoji-crypt`.
