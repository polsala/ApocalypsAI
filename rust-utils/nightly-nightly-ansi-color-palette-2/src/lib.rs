/// Convert an ANSI 256 colour index to an (R, G, B) tuple.
///
/// The algorithm follows the xterm specification:
/// * 0‑15   – standard and bright colours
/// * 16‑231 – 6×6×6 colour cube
/// * 232‑255 – grayscale ramp
pub fn rgb_from_256(idx: u8) -> (u8, u8, u8) {
    match idx {
        0 => (0, 0, 0),
        1 => (128, 0, 0),
        2 => (0, 128, 0),
        3 => (128, 128, 0),
        4 => (0, 0, 128),
        5 => (128, 0, 128),
        6 => (0, 128, 128),
        7 => (192, 192, 192),
        8 => (128, 128, 128),
        9 => (255, 0, 0),
        10 => (0, 255, 0),
        11 => (255, 255, 0),
        12 => (0, 0, 255),
        13 => (255, 0, 255),
        14 => (0, 255, 255),
        15 => (255, 255, 255),
        16..=231 => {
            let i = idx as u16 - 16;
            let r = ((i / 36) % 6) as u8;
            let g = ((i / 6) % 6) as u8;
            let b = (i % 6) as u8;
            let conv = |c| if c == 0 { 0 } else { c * 40 + 55 };
            (conv(r), conv(g), conv(b))
        }
        232..=255 => {
            let gray = 8 + (idx - 232) * 10;
            (gray, gray, gray)
        }
        _ => (0, 0, 0), // unreachable for u8
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_standard_colors() {
        assert_eq!(rgb_from_256(0), (0, 0, 0));
        assert_eq!(rgb_from_256(9), (255, 0, 0));
        assert_eq!(rgb_from_256(15), (255, 255, 255));
    }

    #[test]
    fn test_color_cube() {
        // Index 16 is the first cube colour (0,0,0)
        assert_eq!(rgb_from_256(16), (0, 0, 0));
        // Index 21 should be pure blue (0,0,255)
        assert_eq!(rgb_from_256(21), (0, 0, 255));
        // Index 46 -> r=0,g=2,b=2 => (0,115,115)
        assert_eq!(rgb_from_256(46), (0, 115, 115));
    }

    #[test]
    fn test_grayscale() {
        assert_eq!(rgb_from_256(232), (8, 8, 8));
        assert_eq!(rgb_from_256(255), (238, 238, 238));
    }
}
