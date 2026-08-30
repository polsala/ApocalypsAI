# nightly-scarcity-tracker

A whimsical CLI tool to track scarce resources in a post‑apocalyptic setting. It lets you add, remove, and list items in a simple text‑based inventory.

## Usage

```sh
./main.sh add <item> <amount>
./main.sh remove <item> <amount>
./main.sh list
```

The inventory is stored in `inventory.txt` next to the script.

## Example

```sh
$ ./main.sh add water 10
Added 10 of water
$ ./main.sh add food 5
Added 5 of food
$ ./main.sh list
water: 10
food: 5
$ ./main.sh remove water 3
Removed 3 of water
$ ./main.sh list
water: 7
food: 5
```

## Tests

Run `bash tests/test_main.sh` to execute the test suite.
