"""
File entrypoint chạy công cụ so sánh và kiểm tra cú pháp JSON.
Hỗ trợ cả chế độ CLI và chế độ nhập liệu tương tác.
"""

import sys
from pathlib import Path

# Thêm thư mục 'src' vào sys.path để có thể chạy trực tiếp tập tin này từ mọi nơi
current_dir = Path(__file__).resolve().parent
src_dir = current_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from json_checker.cli import main

if __name__ == "__main__":
    sys.exit(main())
