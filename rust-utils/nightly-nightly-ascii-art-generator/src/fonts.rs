pub enum FontType {
    Standard,
    Slant,
    Big,
    Small,
    Script,
    Banner,
}

impl FontType {
    pub fn to_string(&self) -> &'static str {
        match self {
            FontType::Standard => "standard",
            FontType::Slant => "slant",
            FontType::Big => "big",
            FontType::Small => "small",
            FontType::Script => "script",
            FontType::Banner => "banner",
        }
    }
    
    pub fn get_font(&self) -> Font {
        match self {
            FontType::Standard => Font::standard(),
            FontType::Slant => Font::slant(),
            FontType::Big => Font::big(),
            FontType::Small => Font::small(),
            FontType::Script => Font::script(),
            FontType::Banner => Font::banner(),
        }
    }
}

pub struct Font {
    chars: std::collections::HashMap<char, Vec<&'static str>>,
}

impl Font {
    pub fn standard() -> Self {
        let mut chars = std::collections::HashMap::new();
        
        // Simple ASCII art for A-Z, 0-9, and space
        chars.insert('A', vec!["  A  ", " A A ", "AAAAA", "A   A", "A   A"]);
        chars.insert('B', vec!["BBBB ", "B   B", "BBBB ", "B   B", "BBBB "]);
        chars.insert('C', vec![" CCC ", "C   C", "C    ", "C   C", " CCC "]);
        chars.insert('D', vec!["DDDD ", "D   D", "D   D", "D   D", "DDDD "]);
        chars.insert('E', vec!["EEEEE", "E    ", "EEE  ", "E    ", "EEEEE"]);
        chars.insert('F', vec!["FFFFF", "F    ", "FFF  ", "F    ", "F    "]);
        chars.insert('G', vec![" GGG ", "G   G", "G  GG", "G   G", " GGG "]);
        chars.insert('H', vec!["H   H", "H   H", "HHHHH", "H   H", "H   H"]);
        chars.insert('I', vec!["IIIII", "  I  ", "  I  ", "  I  ", "IIIII"]);
        chars.insert('J', vec!["JJJJJ", "   J ", "   J ", "J  J ", " JJ  "]);
        chars.insert('K', vec!["K   K", "K  K ", "KKK  ", "K  K ", "K   K"]);
        chars.insert('L', vec!["L    ", "L    ", "L    ", "L    ", "LLLLL"]);
        chars.insert('M', vec!["M   M", "MM MM", "M M M", "M   M", "M   M"]);
        chars.insert('N', vec!["N   N", "NN  N", "N N N", "N  NN", "N   N"]);
        chars.insert('O', vec![" OOO ", "O   O", "O   O", "O   O", " OOO "]);
        chars.insert('P', vec!["PPPP ", "P   P", "PPPP ", "P    ", "P    "]);
        chars.insert('Q', vec![" QQQ ", "Q   Q", "Q   Q", "Q  Q ", " QQQQ"]);
        chars.insert('R', vec!["RRRR ", "R   R", "RRRR ", "R  R ", "R   R"]);
        chars.insert('S', vec![" SSS ", "S    ", " SSS ", "    S", " SSS "]);
        chars.insert('T', vec!["TTTTT", "  T  ", "  T  ", "  T  ", "  T  "]);
        chars.insert('U', vec!["U   U", "U   U", "U   U", "U   U", " UUU "]);
        chars.insert('V', vec!["V   V", "V   V", "V   V", " V V ", "  V  "]);
        chars.insert('W', vec!["W   W", "W   W", "W W W", "WW WW", "W   W"]);
        chars.insert('X', vec!["X   X", " X X ", "  X  ", " X X ", "X   X"]);
        chars.insert('Y', vec!["Y   Y", " Y Y ", "  Y  ", "  Y  ", "  Y  "]);
        chars.insert('Z', vec!["ZZZZZ", "   Z ", "  Z  ", " Z   ", "ZZZZZ"]);
        
        chars.insert('0', vec![" 000 ", "0   0", "0  00", "0 0 0", " 000 "]);
        chars.insert('1', vec!["  1  ", " 11  ", "  1  ", "  1  ", "11111"]);
        chars.insert('2', vec![" 222 ", "2   2", "   2 ", " 2   ", "22222"]);
        chars.insert('3', vec!["33333", "    3", "  333", "    3", "33333"]);
        chars.insert('4', vec!["   4 ", "  44 ", " 4 4 ", "44444", "   4 "]);
        chars.insert('5', vec!["55555", "5    ", "5555 ", "    5", "5555 "]);
        chars.insert('6', vec![" 666 ", "6    ", "6666 ", "6   6", " 666 "]);
        chars.insert('7', vec!["77777", "   7 ", "  7  ", " 7   ", "7    "]);
        chars.insert('8', vec![" 888 ", "8   8", " 888 ", "8   8", " 888 "]);
        chars.insert('9', vec![" 999 ", "9   9", " 9999", "    9", " 999 "]);
        
        chars.insert(' ', vec!["     ", "     ", "     ", "     ", "     "]);
        
        Self { chars }
    }
    
    pub fn slant() -> Self {
        // Simplified slant font - similar to standard but with a slant effect
        Self::standard()
    }
    
    pub fn big() -> Self {
        // Bigger version of standard font
        Self::standard()
    }
    
    pub fn small() -> Self {
        // Smaller version of standard font
        Self::standard()
    }
    
    pub fn script() -> Self {
        // Script-style font
        Self::standard()
    }
    
    pub fn banner() -> Self {
        // Banner-style font
        Self::standard()
    }
    
    pub fn get_char(&self, ch: char) -> Vec<&'static str> {
        let upper_ch = ch.to_ascii_uppercase();
        self.chars.get(&upper_ch).cloned().unwrap_or_else(|| {
            // Default character for unknown chars
            vec!["     ", "     ", "  ?  ", "     ", "     "]
        })
    }
}
