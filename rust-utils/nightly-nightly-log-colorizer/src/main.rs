use std::env;
use std::fs::File;
use std::io::{self, BufRead, BufReader, Write};
use termcolor::{Color, ColorChoice, ColorSpec, StandardStream, WriteColor};

fn main() -> io::Result<()> {
    let args: Vec<String> = env::args().collect();
    let reader: Box<dyn BufRead> = if args.len() > 1 {
        Box::new(BufReader::new(File::open(&args[1])?))
    } else {
        Box::new(BufReader::new(io::stdin()))
    };

    let mut stdout = StandardStream::stdout(ColorChoice::Always);
    for line_res in reader.lines() {
        let line = line_res?;
        let mut spec = ColorSpec::new();
        if line.contains("ERROR") {
            spec.set_fg(Some(Color::Red)).set_bold(true);
        } else if line.contains("WARN") {
            spec.set_fg(Some(Color::Yellow)).set_bold(true);
        } else if line.contains("INFO") {
            spec.set_fg(Some(Color::Green)).set_bold(true);
        } else {
            spec.set_fg(None);
        }
        stdout.set_color(&spec)?;
        writeln!(&mut stdout, "{}", line)?;
        stdout.reset()?;
    }
    Ok(())
}
