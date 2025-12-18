use rand::Rng;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum MeasurementOutcome {
    Zero,
    One,
}

impl MeasurementOutcome {
    pub fn to_i32(self) -> i32 {
        match self {
            MeasurementOutcome::Zero => 0,
            MeasurementOutcome::One => 1,
        }
    }
    
    pub fn to_f64(self) -> f64 {
        match self {
            MeasurementOutcome::Zero => -1.0,
            MeasurementOutcome::One => 1.0,
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub struct MeasurementBasis {
    angle: f64,
}

impl MeasurementBasis {
    pub fn new(angle: f64) -> Self {
        MeasurementBasis {
            angle: angle % (std::f64::consts::PI),
        }
    }
    
    pub fn random() -> Self {
        let mut rng = rand::thread_rng();
        let angle = rng.gen_range(0.0..std::f64::consts::PI);
        MeasurementBasis::new(angle)
    }
    
    pub fn angle_difference(&self, other: &MeasurementBasis) -> f64 {
        let diff = (self.angle - other.angle).abs();
        diff.min(std::f64::consts::PI - diff)
    }
}

impl Default for MeasurementBasis {
    fn default() -> Self {
        MeasurementBasis::new(0.0)
    }
}
