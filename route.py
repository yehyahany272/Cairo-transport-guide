"""Cairo Route Finder

Finds a microbus/bus route between two stops, using as few rides as possible.
Routes live in routes.json, so anyone can add a route without touching the code.

Usage:
    python route.py find "3rd District" "Nasr City"
    python route.py stops
    python route.py add "Line name" "Stop 1" "Stop 2" "Stop 3" ...
    python route.py check            (looks for mistakes in routes.json)
    python route.py                  (interactive mode)

Uses only the Python standard library.
"""

import difflib
import heapq
import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).with_name("routes.json")
BOARD_COST = 1000  # boarding a bus costs far more than one extra stop,
                   # so the search first minimizes transfers, then stops.
SIMILAR_NAME_CUTOFF = 0.8


def load_data():
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def all_stops(routes):
    return sorted({stop for r in routes for stop in r["stops"]})


def match_stop(name, stops):
    """Match what the user typed to a known stop (ignores case, fixes small typos)."""
    lookup = {s.lower(): s for s in stops}
    key = name.strip().lower()
    if key in lookup:
        return lookup[key]
    close = difflib.get_close_matches(key, lookup.keys(), n=1, cutoff=0.6)
    return lookup[close[0]] if close else None


def find_route(routes, start, end):
    """Return a list of legs [(line, from_stop, to_stop, stops_travelled)] or None."""
    lines = {r["name"]: r["stops"] for r in routes}
    by_stop = {}
    for r in routes:
        for s in r["stops"]:
            by_stop.setdefault(s, set()).add(r["name"])

    best, prev, queue = {}, {}, []

    def relax(state, cost, came_from):
        if cost < best.get(state, float("inf")):
            best[state] = cost
            prev[state] = came_from
            heapq.heappush(queue, (cost, state))

    for line in by_stop.get(start, ()):
        relax((start, line), BOARD_COST, None)

    while queue:
        cost, (stop, line) = heapq.heappop(queue)
        if cost > best.get((stop, line), float("inf")):
            continue
        if stop == end:
            return build_legs(prev, (stop, line))
        stops = lines[line]
        i = stops.index(stop)
        for j in (i - 1, i + 1):  # routes run both ways
            if 0 <= j < len(stops):
                relax((stops[j], line), cost + 1, (stop, line))
        for other in by_stop[stop]:  # transfer to another line here
            if other != line:
                relax((stop, other), cost + BOARD_COST, (stop, line))
    return None


def build_legs(prev, goal):
    path, state = [], goal
    while state is not None:
        path.append(state)
        state = prev[state]
    path.reverse()

    legs = []
    line, from_stop, last_stop, count = path[0][1], path[0][0], path[0][0], 0
    for stop, ln in path[1:]:
        if ln == line:
            count += 1
            last_stop = stop
        else:
            legs.append((line, from_stop, last_stop, count))
            line, from_stop, last_stop, count = ln, stop, stop, 0
    legs.append((line, from_stop, last_stop, count))
    return legs


def validate(routes):
    """Return a list of problems found in the route data (empty list = all good)."""
    problems = []

    names = [r["name"] for r in routes]
    for name in sorted(set(names)):
        if names.count(name) > 1:
            problems.append(f"Line name '{name}' is used more than once.")

    for r in routes:
        if len(r["stops"]) < 2:
            problems.append(f"'{r['name']}' has fewer than 2 stops.")
        lowered = [s.lower() for s in r["stops"]]
        if len(set(lowered)) != len(lowered):
            problems.append(f"'{r['name']}' lists the same stop more than once.")

    stops = all_stops(routes)
    for i, a in enumerate(stops):
        for b in stops[i + 1:]:
            if a.lower() == b.lower():
                problems.append(f"'{a}' and '{b}' differ only by capital letters.")
            elif difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio() >= SIMILAR_NAME_CUTOFF:
                problems.append(
                    f"'{a}' and '{b}' look like the same place spelled differently. "
                    "Transfers only work when the names match exactly."
                )
    return problems


def print_route(start, end, legs):
    print(f"\n{start}  ->  {end}")
    for n, (line, a, b, count) in enumerate(legs, 1):
        word = "stop" if count == 1 else "stops"
        print(f"  {n}. Take {line}: {a} -> {b}  ({count} {word})")
    print(f"  Transfers: {len(legs) - 1}\n")


def cmd_find(data, start_in, end_in):
    routes = data["routes"]
    stops = all_stops(routes)
    start, end = match_stop(start_in, stops), match_stop(end_in, stops)
    for typed, found in ((start_in, start), (end_in, end)):
        if found is None:
            print(f"I don't know a stop called '{typed}'. Run 'stops' to see known stops.")
            return
        if found.lower() != typed.strip().lower():
            print(f"(Using '{found}' for '{typed}')")
    if start == end:
        print("You are already there!")
        return
    legs = find_route(routes, start, end)
    if legs is None:
        print(f"No route found from {start} to {end}. The route may be missing from routes.json.")
    else:
        print_route(start, end, legs)


def cmd_stops(data):
    for s in all_stops(data["routes"]):
        print(" -", s)


def cmd_add(data, name, stops):
    if len(stops) < 2:
        print("A route needs at least 2 stops.")
        return
    data["routes"].append({"name": name, "stops": stops})
    save_data(data)
    print(f"Added '{name}' with {len(stops)} stops.")
    for problem in validate(data["routes"]):
        print("Warning:", problem)


def cmd_check(data):
    problems = validate(data["routes"])
    if not problems:
        print("routes.json looks good.")
        return 0
    for problem in problems:
        print("Problem:", problem)
    return 1


def interactive(data):
    print("Cairo Route Finder. Press Enter on an empty line to quit.")
    while True:
        start = input("From: ").strip()
        if not start:
            break
        end = input("To:   ").strip()
        if not end:
            break
        cmd_find(data, start, end)


def main(argv):
    data = load_data()
    if len(argv) == 1:
        interactive(data)
    elif argv[1] == "find" and len(argv) == 4:
        cmd_find(data, argv[2], argv[3])
    elif argv[1] == "stops":
        cmd_stops(data)
    elif argv[1] == "add" and len(argv) >= 5:
        cmd_add(data, argv[2], argv[3:])
    elif argv[1] == "check":
        sys.exit(cmd_check(data))
    else:
        print(__doc__)


if __name__ == "__main__":
    main(sys.argv)
