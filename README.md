# Cairo Route Finder

A small Python tool that finds a microbus route between two places in Cairo, using as few transfers as possible.

## Why this exists

Recently I needed to get from the 3rd District to Nasr City and spent 40 minutes asking strangers which microbus to take. Most of Cairo's microbus routes aren't on any app, they live in people's heads. This project is a first step toward writing them down in one open, searchable place.

## How it works

Routes are stored as simple lists of stops in `routes.json`. When you ask for a trip, the program searches for the path with the **fewest transfers**, and among those, the fewest stops. It tells you which line to take and where to switch.

It only uses the Python standard library, so there is nothing to install.

## Usage

```
python route.py find "3rd District" "Nasr City"
```

Example output:

```
3rd District  ->  Nasr City
  1. Take Line 1: 3rd District -> Arabella Plaza  (2 stops)
  2. Take Line 2: Arabella Plaza -> Nasr City  (2 stops)
  Transfers: 1
```

Other commands:

| Command | What it does |
|---|---|
| `python route.py stops` | Lists every stop the program knows |
| `python route.py add "Line name" "Stop 1" "Stop 2" ...` | Adds a new route to `routes.json` |
| `python route.py check` | Looks for mistakes in `routes.json` (for example, one place spelled two ways) |
| `python route.py` | Interactive mode: it asks for "From" and "To" |

Small typos in what you type are handled, so `3rd distict` still finds `3rd District`.

## Data

`routes.json` looks like this:

```json
{
  "routes": [
    { "name": "Line 1", "stops": ["3rd District", "Arabella Square", "Arabella Plaza"] },
    { "name": "Line 2", "stops": ["Arabella Plaza", "ElHuda Market", "Nasr City"] }
  ]
}
```

The current routes come from my own trips. They only cover a small part of Cairo so far, and routes change over time, so **double-check before relying on them**. Two lines connect only where they share a stop with exactly the same name.

## Tests

```
python -m unittest -v
```

Tests also run automatically on every push through GitHub Actions.

## Roadmap

These are plans, not features that exist yet:

- [ ] Collect many more routes from riders across Cairo
- [ ] A searchable website on top of the same data
- [ ] Arabic stop names and search
- [ ] Fares and approximate travel times
- [ ] A map view

## Contributing

Know a route? Please add it. See [CONTRIBUTING.md](CONTRIBUTING.md) for how.

## About

Built by Yehya, a Computer Science student at Cairo University, while learning Python with CS50.

## License

[MIT](LICENSE)
