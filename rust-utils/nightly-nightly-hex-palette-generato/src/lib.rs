pub type Rgb = (f64, f64, f64);
pub type Hsl = (f64, f64, f64);

/// Convert a hex string ("#RRGGBB" or "RRGGBB") to an RGB tuple.
pub fn hex_to_rgb(hex: &str) -> Option<Rgb> {
    let hex = hex.trim_start_matches('#');
    if hex.len() != 6 {
        return None;
    }
    let r = u8::from_str_radix(&hex[0..2], 16).ok()? as f64;
    let g = u8::from_str_radix(&hex[2..4], 16).ok()? as f64;
    let b = u8::from_str_radix(&hex[4..6], 16).ok()? as f64;
    Some((r, g, b))
}

/// Convert an RGB tuple (0..255) to HSL (h in 0..360, s,l in 0..1).
pub fn rgb_to_hsl(rgb: Rgb) -> Hsl {
    let (r, g, b) = (rgb.0 / 255.0, rgb.1 / 255.0, rgb.2 / 255.0);
    let max = r.max(g.max(b));
    let min = r.min(g.min(b));
    let delta = max - min;

    // Lightness
    let l = (max + min) / 2.0;

    // Saturation
    let s = if delta == 0.0 {
        0.0
    } else {
        delta / (1.0 - (2.0 * l - 1.0).abs())
    };

    // Hue
    let h = if delta == 0.0 {
        0.0
    } else if max == r {
        60.0 * (((g - b) / delta) % 6.0)
    } else if max == g {
        60.0 * (((b - r) / delta) + 2.0)
    } else {
        60.0 * (((r - g) / delta) + 4.0)
    };
    let h = if h < 0.0 { h + 360.0 } else { h };
    (h, s, l)
}

/// Convert HSL back to an RGB tuple (0..255).
pub fn hsl_to_rgb(hsl: Hsl) -> Rgb {
    let (h, s, l) = hsl;
    let c = (1.0 - (2.0 * l - 1.0).abs()) * s;
    let x = c * (1.0 - ((h / 60.0) % 2.0 - 1.0).abs());
    let m = l - c / 2.0;

    let (r1, g1, b1) = if (0.0..60.0).contains(&h) {
        (c, x, 0.0)
    } else if (60.0..120.0).contains(&h) {
        (x, c, 0.0)
    } else if (120.0..180.0).contains(&h) {
        (0.0, c, x)
    } else if (180.0..240.0).contains(&h) {
        (0.0, x, c)
    } else if (240.0..300.0).contains(&h) {
        (x, 0.0, c)
    } else {
        (c, 0.0, x)
    };
    let r = ((r1 + m) * 255.0).round() as u8;
    let g = ((g1 + m) * 255.0).round() as u8;
    let b = ((b1 + m) * 255.0).round() as u8;
    (r as f64, g as f64, b as f64)
}

/// Convert an RGB tuple to a hex string "#RRGGBB".
pub fn rgb_to_hex(rgb: Rgb) -> String {
    format!("#{{:02X}}{{:02X}}{{:02X}}", rgb.0 as u8, rgb.1 as u8, rgb.2 as u8)
}

/// Generate a palette by rotating the hue evenly around the color wheel.
pub fn generate_palette(base: Hsl, count: usize) -> Vec<Rgb> {
    let step = 360.0 / count as f64;
    (0..count)
        .map(|i| {
            let h = (base.0 + step * i as f64) % 360.0;
            hsl_to_rgb((h, base.1, base.2))
        })
        .collect()
}
