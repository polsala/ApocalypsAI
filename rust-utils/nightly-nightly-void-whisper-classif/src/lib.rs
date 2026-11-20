use std::collections::HashMap;

#[derive(Debug, PartialEq, Eq, Clone)]
pub enum Category {
    ResourceAlert,
    TemporalAnomaly,
    SocialChatter,
    ExistentialDread,
    Unknown,
}

impl std::fmt::Display for Category {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Category::ResourceAlert => write!(f, "Resource Alert"),
            Category::TemporalAnomaly => write!(f, "Temporal Anomaly"),
            Category::SocialChatter => write!(f, "Social Chatter"),
            Category::ExistentialDread => write!(f, "Existential Dread"),
            Category::Unknown => write!(f, "Unknown"),
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum Urgency {
    Low,
    Medium,
    High,
}

impl std::fmt::Display for Urgency {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Urgency::Low => write!(f, "Low"),
            Urgency::Medium => write!(f, "Medium"),
            Urgency::High => write!(f, "High"),
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
pub struct ClassificationResult {
    pub category: Category,
    pub urgency: Urgency,
}

/// Classifies a given whisper into a category and assigns an urgency level.
pub fn classify_whisper(whisper: &str) -> ClassificationResult {
    let lower_whisper = whisper.to_lowercase();

    let mut category = Category::Unknown;
    let mut urgency = Urgency::Low;

    // Ordered keyword mappings for categories (priority from top to bottom)
    let ordered_categories = vec![
        (Category::ResourceAlert, vec!["food", "water", "supply", "cache", "scavenge", "resource"]),
        (Category::TemporalAnomaly, vec!["time", "rift", "loop", "echo", "past", "future", "glitch", "temporal"]),
        (Category::SocialChatter, vec!["hello", "friend", "foe", "group", "message", "signal", "speak", "contact"]),
        (Category::ExistentialDread, vec!["void", "end", "hopeless", "meaningless", "fate", "doom", "despair", "nothing"]),
    ];

    for (cat, keywords) in &ordered_categories {
        if keywords.iter().any(|k| lower_whisper.contains(k)) {
            category = cat.clone();
            break;
        }
    }

    // Ordered keyword mappings for urgency (priority from High to Low)
    let ordered_urgencies = vec![
        (Urgency::High, vec!["danger", "urgent", "immediate", "critical", "emergency", "now"]),
        (Urgency::Medium, vec!["alert", "warning", "soon", "watch", "monitor"]),
    ];

    for (urg, keywords) in &ordered_urgencies {
        if keywords.iter().any(|k| lower_whisper.contains(k)) {
            urgency = *urg;
            break;
        }
    }
    
    // Special handling for "danger" keyword to ensure it always sets high urgency
    // and potentially influences category if no other strong category keyword is present.
    if lower_whisper.contains("danger") {
        urgency = Urgency::High;
        if category == Category::Unknown {
            category = Category::ResourceAlert;
        }
    }

    ClassificationResult { category, urgency }
}
