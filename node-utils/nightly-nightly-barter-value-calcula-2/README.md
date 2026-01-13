# Nightly Barter Value Calculator

## Overview

Utility to compute barter points for items in a postâapocalyptic setting. Each item has a base rarity/utility score; total value = score * quantity.

## Installation

```sh
npm install
node src/main.js <item> <quantity>
```

## Usage

```sh
node src/main.js water 3
# => 3 units of water are worth 30 barter points.
```

## Adding Items

Edit the `ITEMS` map in `src/main.js` to add or adjust item scores.

## Tests

```sh
node tests/test_main.js
```

The test suite runs offline using Node's builtâin `assert` module.
