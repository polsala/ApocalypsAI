use clap::Parser;
use rand::seq::SliceRandom;
use rand::thread_rng;

#[derive(Parser)]
#[command(name = "nightly-emoji-echo")]
struct Args {
    /// Text to echo
    #[arg(required = true)]
    text: String,
}

fn main() {
    let args = Args::parse();
    let emojis = ["😀","😃","😄","😁","😆","😅","😂","🤣","😊","😇","🙂","🙃","😉","😌","😍","🥰","😘","😗","😙","😚","😋","😛","😝","😜","🤪","🤨","🧐","🤓","😎","🤩","🥳","😏","😒","😞","😔","😟","😕","🙁","☹️","😣","😖","😫","😩","🥺","😢","😭","😤","😠","😡","🤬","🤯","😳","🥵","🥶","😱","😨","😰","😥","😓","🤗","🤔","🤭","🤫","🤥","😶","😐","😑","😬","🙄","😯","😦","😧","😮","😲","🥱","😴","🤤","😪","😵","🤐","🥴","🤢","🤮","🤧","😷","🤒","🤕","🤑","🤠","😈","👿","👹","👺","🤡","💩","👻","💀","☠️","👽","🤖","🎃","😺","😸","😹","😻","😼","😽","🙀","😿","😾"]; 

    let mut rng = thread_rng();
    let emoji = emojis.choose(&mut rng).unwrap_or(&"");
    println!("{} {}", args.text, emoji);
}
