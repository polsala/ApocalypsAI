# nightly-emoji-calendar

**What it does**

`nightly-emoji-calendar` renders a month‑long calendar where every day is replaced by a cute emoji:

- 📚 Monday – Friday (workdays)
- 🌞 Saturday (weekend sunshine)
- 🌛 Sunday (relaxing night)

The output is plain text, making it easy to paste into Markdown files, commit messages, or terminal output.

**Installation**

The utility is self‑contained – just copy the `utils/nightly-emoji-calendar/` directory into your repository and run the script with Python 3.11.

```bash
python -m utils.nightly-emoji-calendar.src.calendar [--year <YYYY>] [--month <MM>]
```

If `--year` or `--month` are omitted, the current year and month are used.

**Example**

```text
$ python -m utils.nightly-emoji-calendar.src.calendar --year 2023 --month 2
    📚 📚 📚 🌞 🌛
📚 📚 📚 📚 📚 🌞 🌛
📚 📚 📚 📚 📚 🌞 🌛
📚 📚 📚 📚 📚 🌞 🌛
📚 📚               
```

**Testing**

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-calendar/tests
```

---

*Feel free to fork, tweak the emoji set, or embed the output in your project’s documentation!*
