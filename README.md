# csvlens-py

A terminal-based CSV explorer with fuzzy filtering and column statistics built on [rich](https://github.com/Textualize/rich).

---

## Installation

```bash
pip install csvlens-py
```

Or install from source:

```bash
git clone https://github.com/yourname/csvlens-py.git && cd csvlens-py && pip install .
```

---

## Usage

Launch the interactive explorer by pointing it at any CSV file:

```bash
csvlens data.csv
```

**Key bindings:**

| Key | Action |
|-----------|--------------------------|
| `/` | Fuzzy filter rows |
| `Tab` | Cycle through columns |
| `s` | Show column statistics |
| `q` | Quit |

**Example — inspect a dataset and filter on the fly:**

```bash
csvlens sales_2024.csv
# Press / and type "west" to fuzzy-filter rows containing "west"
# Press s to view mean, min, max for the selected column
```

You can also pipe data directly:

```bash
cat data.csv | csvlens -
```

---

## Requirements

- Python 3.8+
- [rich](https://pypi.org/project/rich/) >= 13.0

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss any major changes.

---

## License

This project is licensed under the [MIT License](LICENSE).