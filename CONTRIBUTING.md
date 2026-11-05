# Contributing

Most of Cairo's microbus routes aren't on any app. They live in people's heads. This project exists to write them down, so the most useful contribution is **a route you have actually ridden**.

## Add a route

1. Fork the repo and open `routes.json`.
2. Add a new line to the `routes` list:

   ```json
   {
     "name": "Line 5",
     "stops": ["First Stop", "Middle Stop", "Last Stop"]
   }
   ```

   Stops go in order along the route. Routes are treated as running both ways.
3. **Reuse the exact same spelling** for a stop that already exists. Transfers only work when the names match exactly, so "Arabella Plaza" and "Arabella Plaza Mall" would count as two different places. Run `python route.py stops` to see the names already in use.
4. Run the checks:

   ```
   python route.py check
   python -m unittest
   ```
5. Open a pull request. In the description, say which neighborhood the route covers and roughly when you last rode it.

## Rules for routes

- Only add routes you have ridden yourself, or that someone you trust has confirmed.
- Don't guess. A missing route is better than a wrong one.
- Routes change. If one has changed or disappeared, open an issue or a pull request.

## Other ways to help

- Test the finder on your own trips and report wrong results.
- Suggest improvements through issues (see the roadmap in the README).
- Fix typos or improve the docs.
