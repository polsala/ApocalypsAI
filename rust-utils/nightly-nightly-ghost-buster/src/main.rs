use std::env;
use std::fs;
use std::path::Path;

fn print_usage() {
    eprintln!("Usage: ghost-buster --path <directory> [--delete]");
}

fn find_hidden_files(dir: &Path, ghosts: &mut Vec<std::path::PathBuf>) {
    if let Ok(entries) = fs::read_dir(dir) {
        for entry in entries.filter_map(|e| e.ok()) {
            let path = entry.path();
            if path.is_dir() {
                find_hidden_files(&path, ghosts);
            } else if path.is_file() {
                if let Some(name) = path.file_name().and_then(|n| n.to_str()) {
                    if name.starts_with('.') {
                        ghosts.push(path);
                    }
                }
            }
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 3 {
        print_usage();
        std::process::exit(1);
    }

    let mut path = "";
    let mut delete = false;
    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "--path" => {
                if i + 1 < args.len() {
                    path = &args[i + 1];
                    i += 1;
                } else {
                    eprintln!("--path requires a value");
                    std::process::exit(1);
                }
            }
            "--delete" => delete = true,
            _ => {
                eprintln!("Unknown argument: {}", args[i]);
                std::process::exit(1);
            }
        }
        i += 1;
    }

    let dir = Path::new(path);
    if !dir.is_dir() {
        eprintln!("{} is not a directory", path);
        std::process::exit(1);
    }

    let mut ghosts = Vec::new();
    find_hidden_files(dir, &mut ghosts);

    if ghosts.is_empty() {
        println!("No ghosts found.");
    } else {
        for ghost in &ghosts {
            println!("👻 Found ghost: {}", ghost.display());
        }
        if delete {
            for ghost in &ghosts {
                if let Err(e) = fs::remove_file(ghost) {
                    eprintln!("Failed to delete {}: {}", ghost.display(), e);
                } else {
                    println!("🗑️ Deleted ghost: {}", ghost.display());
                }
            }
        }
    }
}
