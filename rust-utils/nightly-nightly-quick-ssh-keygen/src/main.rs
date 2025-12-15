use std::fs::File;
use std::io::Write;
use std::path::PathBuf;

use rsa::{RsaPrivateKey, RsaPublicKey, pkcs1::EncodeRsaPrivateKey, pkcs1::EncodeRsaPublicKey};
use rand::rngs::OsRng;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let out_dir = if args.len() > 1 {
        PathBuf::from(&args[1])
    } else {
        std::env::current_dir().expect("cannot determine current directory")
    };
    let key_name = if args.len() > 2 { &args[2] } else { "id_rsa" };

    let private_path = out_dir.join(key_name);
    let public_path = out_dir.join(format!("{}.pub", key_name));

    // Generate a 2048‑bit RSA key pair
    let mut rng = OsRng;
    let bits = 2048;
    let private_key = RsaPrivateKey::new(&mut rng, bits).expect("failed to generate key");
    let public_key = RsaPublicKey::from(&private_key);

    // Encode keys
    let private_pem = private_key.to_pkcs1_pem().expect("failed to encode private key");
    let public_ssh = public_key.to_public_key_openssh().expect("failed to encode public key");

    // Ensure output directory exists
    std::fs::create_dir_all(&out_dir).expect("failed to create output directory");

    // Write private key
    let mut priv_file = File::create(&private_path).expect("failed to create private key file");
    priv_file.write_all(private_pem.as_bytes()).expect("failed to write private key");

    // Write public key
    let mut pub_file = File::create(&public_path).expect("failed to create public key file");
    pub_file.write_all(public_ssh.as_bytes()).expect("failed to write public key");

    // Print public key to stdout
    println!("{}", public_ssh);
    println!("Key pair generated: {} and {}", private_path.display(), public_path.display());
}
