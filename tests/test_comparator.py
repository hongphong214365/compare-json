from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from json_checker.comparator import compare_json_data, flatten_keys
from json_checker.validator import validate_json_file

TESTS_DIR = Path(__file__).parent / "data"

class TestComparator(unittest.TestCase):
    def test_flatten_keys(self):
        data = {
            "a": 1,
            "b": {
                "c": 2,
                "d": [10, {"e": 3}]
            }
        }
        keys = flatten_keys(data)
        expected = {"a", "b", "b.c", "b.d", "b.d[0]", "b.d[1]", "b.d[1].e"}
        self.assertEqual(keys, expected)

    def test_compare_json_data(self):
        _, source_data, _, _ = validate_json_file(str(TESTS_DIR / "en.json"))
        _, dest_data, _, _ = validate_json_file(str(TESTS_DIR / "vi_missing.json"))

        result = compare_json_data(source_data, dest_data)
        self.assertGreater(result.missing_count, 0)
        self.assertIn("app.settings", result.missing_in_dest)
        self.assertIn("app.settings.theme", result.missing_in_dest)
        self.assertIn("messages.goodbye", result.missing_in_dest)

if __name__ == "__main__":
    unittest.main()
