# Wasteland Whisperer Decoder Ring

## Summary
This utility provides a type-safe command-line interface (CLI) for decoding messages that have been encrypted using simple, configurable ciphers. It serves as the essential counterpart to the Wasteland Whisperer Encoder, allowing survivors to decipher crucial communications in the post-apocalyptic landscape.

## Features
- Supports Caesar cipher with configurable shift.
- Supports Atbash cipher.
- Type-safe implementation using TypeScript.
- Easy-to-use CLI.

## Installation
1.  Ensure you have Node.js (v14 or higher) and npm installed.
2.  Navigate to the `nightly-wasteland-whisperer-decoder` directory.
3.  Install dependencies:
    ```bash
    npm install
    ```

## Usage
Run the decoder using `ts-node` or by building the project first.

### Decoding with Caesar Cipher
To decode a message encrypted with a Caesar cipher, specify `caesar` as the cipher type and provide the `shift` value used for encryption.

```bash
npm start -- --cipher caesar --shift 3 --message "khoor zruog"
# Expected Output: hello world

npm start -- --cipher caesar --shift -3 --message "hello world"
# Expected Output: khoor zruog (decoding with negative shift is equivalent to encoding with positive)
```

### Decoding with Atbash Cipher
To decode a message encrypted with an Atbash cipher, specify `atbash` as the cipher type. Atbash does not require a shift or key.

```bash
npm start -- --cipher atbash --message "zyxw"
# Expected Output: abcb

npm start -- --cipher atbash --message "svool dliow"
# Expected Output: hello world
```

### Help
```bash
npm start -- --help
```

## Development
To run tests:
```bash
npm test
```

To build the project:
```bash
npm run build
```
Then you can run the compiled JavaScript:
```bash
node dist/index.js --cipher caesar --shift 3 --message "khoor zruog"
```
