from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from json_checker.validator import clean_path_input, validate_json_file

TESTS_DIR = Path(__file__).parent / "data"

class TestValidator(unittest.TestCase):
    def test_clean_path_input(self):
        # Trimming spaces
        self.assertEqual(clean_path_input("   myfile.json   "), "myfile.json")
        self.assertEqual(clean_path_input("\t\n  myfile.json \r "), "myfile.json")
        # Removing surrounding quotes (from drag-drop)
        self.assertEqual(clean_path_input('"C:\\path with spaces\\file.json"'), "C:\\path with spaces\\file.json")
        self.assertEqual(clean_path_input("'C:\\path with spaces\\file.json'"), "C:\\path with spaces\\file.json")
        # Empty input
        self.assertEqual(clean_path_input(""), "")
        self.assertEqual(clean_path_input("   "), "")

    def test_validate_valid_file(self):
        en_path = str(TESTS_DIR / "en.json")
        # Pass with extra spaces
        spaced_path = f"   {en_path}   "
        is_valid, data, msg, path_obj = validate_json_file(spaced_path)
        self.assertTrue(is_valid)
        self.assertIsNotNone(data)
        self.assertIn("Chúc mừng, bạn đã vượt qua, đường dẫn:", msg)
        self.assertIn("là hợp lệ", msg)
        self.assertEqual(data["app"]["name"], "My Tool")

    def test_validate_nonexistent_file(self):
        is_valid, data, msg, _ = validate_json_file("non_existent_file_xyz.json")
        self.assertFalse(is_valid)
        self.assertIn("không tồn tại", msg)

    def test_validate_non_json_extension(self):
        is_valid, data, msg, _ = validate_json_file("pyproject.toml")
        self.assertFalse(is_valid)
        self.assertIn("không phải là file json", msg)

    def test_validate_invalid_syntax(self):
        broken_path = str(TESTS_DIR / "invalid_syntax.json")
        is_valid, data, msg, _ = validate_json_file(broken_path)
        self.assertFalse(is_valid)
        self.assertIn("Lỗi cú pháp JSON", msg)
        self.assertIn("Dòng", msg)

if __name__ == "__main__":
    unittest.main()
