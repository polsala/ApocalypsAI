use crate::fonts::{Font, FontType};

pub struct AsciiArt {
    text: String,
    font: FontType,
}

impl AsciiArt {
    pub fn new(text: String, font: FontType) -> Self {
        Self { text, font }
    }
    
    pub fn print(&self) {
        let font = self.font.get_font();
        let lines = self.generate_art(&font);
        
        for line in lines {
            println!("{}", line);
        }
    }
    
    fn generate_art(&self, font: &Font) -> Vec<String> {
        let mut result = vec![String::new(); 6]; // Most fonts have 6 lines
        
        for ch in self.text.chars() {
            let char_art = font.get_char(ch);
            
            for (i, line) in char_art.iter().enumerate() {
                if i < result.len() {
                    result[i].push_str(line);
                }
            }
        }
        
        result
    }
}
