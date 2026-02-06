use ansi_palette_swatch::generate_palette;\nuse std::io::{self, Write};\n\nfn main() {\n    let palette = generate_palette();\n    print!("{}", palette);\n    io::stdout().flush().unwrap();\n}\n
