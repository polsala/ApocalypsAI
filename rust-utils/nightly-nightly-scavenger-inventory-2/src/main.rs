use scavenger_inventory::generate_inventory;\n\nfn main() {\n    let inventory = generate_inventory(12345);\n    for (item, qty) in inventory {\n        println!("{}x {}", qty, item);\n    }\n}\n
