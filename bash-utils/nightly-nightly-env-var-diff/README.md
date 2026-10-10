# nightly-env-var-diff

Utility to compare two `.env` files and report added, removed, and modified environment variables.

## Usage

```sh
./src/env_diff.sh path/to/.env.old path/to/.env.new
```

The script prints three optional sections (in this order):

* **Added** – variables present only in the *new* file.
* **Removed** – variables present only in the *old* file.
* **Modified** – variables present in both files but with different values.

If a section has no entries it is omitted from the output.

## Example

```sh
# old.env
FOO=apple
BAR=banana
BAZ=qux

# new.env
FOO=apple
BAR=blueberry
NEWVAR=hello

$ ./src/env_diff.sh old.env new.env
Added:
  NEWVAR=hello
Removed:
  BAZ=qux
Modified:
  BAR=banana -> blueberry
```

## License

MIT © ApocalypsAI Community
