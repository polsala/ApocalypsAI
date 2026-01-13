pub struct GearItem {
    pub name: &'static str,
    pub rarity: &'static str,
    pub description: &'static str,
}

pub fn generate_item<R: rand::Rng + ?Sized>(rng: &mut R) -> GearItem {
    let names = [
        "Rusty Pipe Wrench",
        "Makeshift Gas Mask",
        "Scrap Metal Shield",
        "Improvised Flamethrower",
        "Salvaged Solar Panel",
        "Worn Leather Boots",
        "Radiation Detector",
        "JuryâRigged Drone",
        "Canned Food Stash",
        "Water Purifier Kit",
    ];
    let rarities = ["Common", "Uncommon", "Rare", "Legendary"];
    let descriptions = [
        "A battered item, still functional enough for survival.",
        "A piece of equipment cobbled together from scavenged parts.",
        "An essential tool for navigating the wastelands.",
        "A rare find that could turn the tide of any encounter.",
        "A legendary artifact whispered about in survivor tales.",
    ];

    let name = names.choose(rng).unwrap();
    let rarity = rarities.choose(rng).unwrap();
    let description = descriptions.choose(rng).unwrap();

    GearItem {
        name,
        rarity,
        description,
    }
}
