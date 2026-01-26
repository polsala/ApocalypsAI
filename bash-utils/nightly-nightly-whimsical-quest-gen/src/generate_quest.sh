#!/bin/bash

# Whimsical elements
QUEST_TEMPLATES=(
    "Retrieve the legendary {object} from the {location} before the {threat} arrives."
    "Scavenge for {resource} in the {area} to appease the {entity}."
    "Perform a {action} at the {landmark} to unlock the {secret}."
    "Decipher the {ancient_text} found near the {ruin} to reveal the {hidden_truth}."
    "Befriend the {creature} inhabiting the {habitat} by offering {offering}."
)

WHIMSICAL_OBJECTS=(
    "Glimmering Spork of Destiny"
    "Lost Sock of Infinite Comfort"
    "Rusty Can of Cosmic Beans"
    "Whispering Rubber Duck"
    "Singing Teacup of Serenity"
)

WHIMSICAL_LOCATIONS=(
    "Echoing Dustbowl"
    "Forgotten Fridge Dimension"
    "The Great Lint Sea"
    "Whisperwind Alley"
    "Giggling Gulch"
)

WHIMSICAL_THREATS=(
    "Grumpy Goblins of Glitch"
    "Temporal Tumbleweeds"
    "The Great Snack Thief"
    "Existential Dust Bunnies"
    "The Looming Laundry Day"
)

WHIMSICAL_RESOURCES=(
    "Sparkle-Dust"
    "Ambrosia of Forgotten Dreams"
    "Quantum Crumbs"
    "Echoing Silence"
    "Pure Imagination"
)

WHIMSICAL_AREAS=(
    "The Whispering Pantry"
    "The Land of Lost Remotes"
    "The Infinite Sock Drawer"
    "The Forgotten Corner of the Internet"
    "The Realm of Unread Books"
)

WHIMSICAL_ENTITIES=(
    "The Great Procrastinator"
    "The Dust Bunny King"
    "The Spirit of Unfinished Projects"
    "The Oracle of Lost Keys"
    "The Ancient Coffee Stain"
)

WHIMSICAL_ACTIONS=(
    "a ceremonial dance"
    "a dramatic monologue"
    "a silent meditation on lint"
    "a vigorous high-five"
    "a heartfelt apology to a houseplant"
)

WHIMSICAL_LANDMARKS=(
    "The Monument of Misplaced Pens"
    "The Tower of Toppled Tupperware"
    "The Shrine of Forgotten Passwords"
    "The Great Wall of Unsorted Mail"
    "The Fountain of Eternal 'Later'"
)

WHIMSICAL_SECRETS=(
    "the recipe for eternal youth (and toast)"
    "the true meaning of 'soon'"
    "the location of all missing socks"
    "the secret to perfectly folded fitted sheets"
    "the universal remote code"
)

WHIMSICAL_ANCIENT_TEXTS=(
    "The Scroll of Self-Correction"
    "The Ballad of the Broken Browser"
    "The Epic of the Empty Fridge"
    "The Codex of Cat Hair"
    "The Prophecy of the Pending Update"
)

WHIMSICAL_RUINS=(
    "The Ruins of the Last Wi-Fi Signal"
    "The Crumbling Remains of the Weekend"
    "The Desolate Desktop"
    "The Forgotten Folder of Fun"
    "The Sunken City of Unanswered Emails"
)

WHIMSICAL_HIDDEN_TRUTHS=(
    "that the universe is powered by static electricity"
    "the true identity of the 'who left this here?' culprit"
    "that all lost items are in a parallel dimension"
    "the secret language of squirrels"
    "that Mondays are actually Tuesdays in disguise"
)

WHIMSICAL_CREATURES=(
    "The Grumbling Gremlin of the Gutter"
    "The Fluffy Fuzzball of Forgetfulness"
    "The Chirping Chinchilla of Chaos"
    "The Sneezing Snorklewomp"
    "The Giggle-Puff"
)

WHIMSICAL_HABITATS=(
    "The Under-Couch Caverns"
    "The Back of the Bookshelf Bog"
    "The Laundry Basket Labyrinth"
    "The Desk Drawer Dungeon"
    "The Forbidden Zone Behind the Router"
)

WHIMSICAL_OFFERINGS=(
    "a single, perfectly peeled grape"
    "a freshly polished paperclip"
    "a whispered secret"
    "a moment of quiet contemplation"
    "a perfectly timed yawn"
)

# Function to pick a random element from an array using shuf
pick_random() {
    local -n arr=$1 # Use nameref for array
    printf "%s\n" "${arr[@]}" | shuf -n 1
}

# Generate a quest
generate_quest() {
    local template=$(pick_random QUEST_TEMPLATES)

    local object=$(pick_random WHIMSICAL_OBJECTS)
    local location=$(pick_random WHIMSICAL_LOCATIONS)
    local threat=$(pick_random WHIMSICAL_THREATS)
    local resource=$(pick_random WHIMSICAL_RESOURCES)
    local area=$(pick_random WHIMSICAL_AREAS)
    local entity=$(pick_random WHIMSICAL_ENTITIES)
    local action=$(pick_random WHIMSICAL_ACTIONS)
    local landmark=$(pick_random WHIMSICAL_LANDMARKS)
    local secret=$(pick_random WHIMSICAL_SECRETS)
    local ancient_text=$(pick_random WHIMSICAL_ANCIENT_TEXTS)
    local ruin=$(pick_random WHIMSICAL_RUINS)
    local hidden_truth=$(pick_random WHIMSICAL_HIDDEN_TRUTHS)
    local creature=$(pick_random WHIMSICAL_CREATURES)
    local habitat=$(pick_random WHIMSICAL_HABITATS)
    local offering=$(pick_random WHIMSICAL_OFFERINGS)

    # Replace placeholders
    template="${template//\{object\}/$object}"
    template="${template//\{location\}/$location}"
    template="${template//\{threat\}/$threat}"
    template="${template//\{resource\}/$resource}"
    template="${template//\{area\}/$area}"
    template="${template//\{entity\}/$entity}"
    template="${template//\{action\}/$action}"
    template="${template//\{landmark\}/$landmark}"
    template="${template//\{secret\}/$secret}"
    template="${template//\{ancient_text\}/$ancient_text}"
    template="${template//\{ruin\}/$ruin}"
    template="${template//\{hidden_truth\}/$hidden_truth}"
    template="${template//\{creature\}/$creature}"
    template="${template//\{habitat\}/$habitat}"
    template="${template//\{offering\}/$offering}"

    echo "Your Whimsical Quest for $(date +%A):"
    echo "-------------------------------------"
    echo "$template"
    echo "-------------------------------------"
    echo "Good luck, wanderer!"
}

generate_quest
