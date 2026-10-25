import io
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from json_checker.cli import main

TESTS_DIR = Path(__file__).parent / "data"

class TestCLI(unittest.TestCase):
    def test_cli_help(self):
        saved_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            with self.assertRaises(SystemExit) as cm:
                main(["--help"])
            self.assertEqual(cm.exception.code, 0)
        finally:
            sys.stdout = saved_stdout

    def test_cli_check_valid_files(self):
        en = str(TESTS_DIR / "en.json")
        vi = str(TESTS_DIR / "vi_missing.json")

        saved_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            code = main(["--check", "-s", en, "-d", vi])
            output = sys.stdout.getvalue()
            self.assertEqual(code, 0)
            self.assertIn("Toàn bộ file đã kiểm tra đều có cú pháp JSON chuẩn xác", output)
        finally:
            sys.stdout = saved_stdout

    def test_cli_check_invalid_syntax(self):
        en = str(TESTS_DIR / "en.json")
        broken = str(TESTS_DIR / "invalid_syntax.json")

        saved_stdout = sys.stdout
        try:
            sys.stdout = io.StringIO()
            code = main(["--check", "-s", en, "-d", broken])
            output = sys.stdout.getvalue()
            self.assertEqual(code, 1)
            self.assertIn("Lỗi cú pháp JSON", output)
        finally:
            sys.stdout = saved_stdout

    def test_cli_compare_with_output_flag(self):
        en = str(TESTS_DIR / "en.json")
        vi = str(TESTS_DIR / "vi_missing.json")
        with tempfile.TemporaryDirectory() as tmp_dir:
            out_file = Path(tmp_dir) / "output_result.txt"
            saved_stdout = sys.stdout
            try:
                sys.stdout = io.StringIO()
                code = main(["--sof", en, "--def", vi, "-o", str(out_file)])
                self.assertEqual(code, 0)
                self.assertTrue(out_file.exists())
                content = out_file.read_text(encoding="utf-8")
                self.assertIn("BÁO CÁO SO SÁNH FILE JSON", content)
                self.assertIn("app.settings", content)
            finally:
                sys.stdout = saved_stdout

if __name__ == "__main__":
    unittest.main()
