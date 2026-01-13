use std::io::{self, BufRead, Write};

static EMOJIS: &[&str] = &[
    "ð", "ð", "ð¥", "ð¥", "ð", "â¨", "ð", "ð ï¸", "ð§", "ð§©",
];

pub fn process<R: BufRead, W: Write>(reader: R, mut writer: W) -> io::Result<()> {
    for (idx, line_res) in reader.lines().enumerate() {
        let line = line_res?;
        let emoji = EMOJIS[idx % EMOJIS.len()];
        writeln!(writer, "{} {}", emoji, line)?;
    }
    Ok(())
}

