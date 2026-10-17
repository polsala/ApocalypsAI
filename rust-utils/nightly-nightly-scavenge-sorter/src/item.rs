use std::fmt;
use std::str::FromStr;

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Rarity {
    Common,
    Uncommon,
    Rare,
    Legendary,
}

impl Rarity {
    pub fn multiplier(&self) -> f64 {
        match self {
            Rarity::Common => 1.0,
            Rarity::Uncommon => 1.5,
            Rarity::Rare => 2.5,
            Rarity::Legendary => 5.0,
        }
    }
}

impl FromStr for Rarity {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "common" => Ok(Rarity::Common),
            "uncommon" => Ok(Rarity::Uncommon),
            "rare" => Ok(Rarity::Rare),
            "legendary" => Ok(Rarity::Legendary),
            _ => Err(format!("Unknown rarity: {}", s)),
        }
    }
}

#[derive(Debug, PartialEq, Clone, Copy)]
pub enum Condition {
    Pristine,
    Worn,
    Damaged,
    Broken,
}

impl Condition {
    pub fn multiplier(&self) -> f64 {
        match self {
            Condition::Pristine => 1.2,
            Condition::Worn => 1.0,
            Condition::Damaged => 0.7,
            Condition::Broken => 0.3,
        }
    }
}

impl FromStr for Condition {
    type Err = String;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {
            "pristine" => Ok(Condition::Pristine),
            "worn" => Ok(Condition::Worn),
            "damaged" => Ok(Condition::Damaged),
            "broken" => Ok(Condition::Broken),
            _ => Err(format!("Unknown condition: {}", s)),
        }
    }
}

#[derive(Debug, PartialEq)]
pub struct Item {
    pub name: String,
    pub base_utility: u32,
    pub rarity: Rarity,
    pub condition: Condition,
}

impl Item {
    pub fn from_str(s: &str) -> Result<Self, String> {
        let parts: Vec<&str> = s.split(',').map(|p| p.trim()).collect();
        if parts.len() != 4 {
            return Err(format!("Invalid item format: expected 4 parts, got {}", parts.len()));
        }

        let name = parts[0].to_string();
        let base_utility = parts[1].parse::<u32>()
            .map_err(|e| format!("Invalid base utility '{}': {}", parts[1], e))?;
        let rarity = Rarity::from_str(parts[2])?;
        let condition = Condition::from_str(parts[3])?;

        Ok(Item { name, base_utility, rarity, condition })
    }

    pub fn survival_score(&self) -> f64 {
        self.base_utility as f64 * self.rarity.multiplier() * self.condition.multiplier()
    }
}

impl fmt::Display for Item {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "[{:.2}] {} (Utility: {}, Rarity: {:?}, Condition: {:?})",
            self.survival_score(),
            self.name,
            self.base_utility,
            self.rarity,
            self.condition
        )
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rarity_multiplier() {
        assert_eq!(Rarity::Common.multiplier(), 1.0);
        assert_eq!(Rarity::Uncommon.multiplier(), 1.5);
        assert_eq!(Rarity::Rare.multiplier(), 2.5);
        assert_eq!(Rarity::Legendary.multiplier(), 5.0);
    }

    #[test]
    fn test_condition_multiplier() {
        assert_eq!(Condition::Pristine.multiplier(), 1.2);
        assert_eq!(Condition::Worn.multiplier(), 1.0);
        assert_eq!(Condition::Damaged.multiplier(), 0.7);
        assert_eq!(Condition::Broken.multiplier(), 0.3);
    }

    #[test]
    fn test_item_from_str_valid() {
        let item_str = "Water Bottle,5,Common,Worn";
        let item = Item::from_str(item_str).unwrap();
        assert_eq!(item.name, "Water Bottle");
        assert_eq!(item.base_utility, 5);
        assert_eq!(item.rarity, Rarity::Common);
        assert_eq!(item.condition, Condition::Worn);
    }

    #[test]
    fn test_item_from_str_invalid_parts_count() {
        let item_str = "Water Bottle,5,Common";
        assert!(Item::from_str(item_str).is_err());
    }

    #[test]
    fn test_item_from_str_invalid_utility() {
        let item_str = "Water Bottle,abc,Common,Worn";
        assert!(Item::from_str(item_str).is_err());
    }

    #[test]
    fn test_item_from_str_invalid_rarity() {
        let item_str = "Water Bottle,5,Mythical,Worn";
        assert!(Item::from_str(item_str).is_err());
    }

    #[test]
    fn test_item_from_str_invalid_condition() {
        let item_str = "Water Bottle,5,Common,Destroyed";
        assert!(Item::from_str(item_str).is_err());
    }

    #[test]
    fn test_survival_score_calculation() {
        // Water Bottle,5,Common,Worn -> 5 * 1.0 * 1.0 = 5.0
        let item1 = Item {
            name: "Water Bottle".to_string(),
            base_utility: 5,
            rarity: Rarity::Common,
            condition: Condition::Worn,
        };
        assert_eq!(item1.survival_score(), 5.0);

        // Ancient AI Core,20,Legendary,Pristine -> 20 * 5.0 * 1.2 = 120.0
        let item2 = Item {
            name: "Ancient AI Core".to_string(),
            base_utility: 20,
            rarity: Rarity::Legendary,
            condition: Condition::Pristine,
        };
        assert_eq!(item2.survival_score(), 120.0);

        // Rusty Spoon,1,Common,Broken -> 1 * 1.0 * 0.3 = 0.3
        let item3 = Item {
            name: "Rusty Spoon".to_string(),
            base_utility: 1,
            rarity: Rarity::Common,
            condition: Condition::Broken,
        };
        assert_eq!(item3.survival_score(), 0.3);
    }
}
