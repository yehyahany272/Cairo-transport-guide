import unittest

import route

ROUTES = [
    {"name": "A", "stops": ["S1", "S2", "S3"]},
    {"name": "B", "stops": ["S3", "S4", "S5"]},
    {"name": "C", "stops": ["S1", "S5"]},
    {"name": "D", "stops": ["X", "Y"]},
]


class FindRouteTests(unittest.TestCase):
    def test_direct_route(self):
        self.assertEqual(route.find_route(ROUTES, "S1", "S3"), [("A", "S1", "S3", 2)])

    def test_route_with_one_transfer(self):
        self.assertEqual(
            route.find_route(ROUTES, "S2", "S4"),
            [("A", "S2", "S3", 1), ("B", "S3", "S4", 1)],
        )

    def test_prefers_fewer_transfers_over_fewer_stops(self):
        # S1 -> S5 is one ride on C, even though A + B would also work.
        self.assertEqual(route.find_route(ROUTES, "S1", "S5"), [("C", "S1", "S5", 1)])

    def test_routes_work_in_both_directions(self):
        self.assertEqual(route.find_route(ROUTES, "S3", "S1"), [("A", "S3", "S1", 2)])

    def test_unconnected_stops_return_none(self):
        self.assertIsNone(route.find_route(ROUTES, "S1", "X"))


class MatchStopTests(unittest.TestCase):
    STOPS = ["3rd District", "Nasr City", "Tahrir"]

    def test_ignores_case(self):
        self.assertEqual(route.match_stop("nasr city", self.STOPS), "Nasr City")

    def test_fixes_small_typos(self):
        self.assertEqual(route.match_stop("3rd distict", self.STOPS), "3rd District")

    def test_unknown_stop_returns_none(self):
        self.assertIsNone(route.match_stop("Atlantis", self.STOPS))


class ValidateTests(unittest.TestCase):
    def test_clean_data_has_no_problems(self):
        self.assertEqual(route.validate(ROUTES), [])

    def test_catches_near_duplicate_stop_names(self):
        bad = [
            {"name": "L1", "stops": ["A Start", "Arabella Plaza Mall"]},
            {"name": "L2", "stops": ["Arabella Plaza", "B End"]},
        ]
        self.assertTrue(any("same place" in p for p in route.validate(bad)))

    def test_catches_duplicate_line_names(self):
        bad = [{"name": "L1", "stops": ["P", "Q"]}, {"name": "L1", "stops": ["R", "S"]}]
        self.assertTrue(any("more than once" in p for p in route.validate(bad)))

    def test_catches_short_routes(self):
        bad = [{"name": "L1", "stops": ["Only One"]}]
        self.assertTrue(any("fewer than 2" in p for p in route.validate(bad)))


class RealDataTests(unittest.TestCase):
    def test_routes_json_has_no_problems(self):
        self.assertEqual(route.validate(route.load_data()["routes"]), [])


if __name__ == "__main__":
    unittest.main()
