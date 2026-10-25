"""
Module xử lý làm sạch dữ liệu đầu vào và kiểm tra hợp lệ của file/cú pháp JSON.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Tuple


def clean_path_input(raw_input: str) -> str:
    """Loại bỏ khoảng trắng thừa ở hai đầu và các dấu nháy kép/đơn (thường gặp khi kéo thả file trong terminal)."""
    if raw_input is None:
        return ""
    cleaned = raw_input.strip()
    # Loại bỏ dấu ngoặc kép hoặc dấu nháy đơn bao bọc đường dẫn
    if (cleaned.startswith('"') and cleaned.endswith('"')) or (
        cleaned.startswith("'") and cleaned.endswith("'")
    ):
        cleaned = cleaned[1:-1].strip()
    return cleaned


def validate_json_file(file_path_str: str | Path) -> Tuple[bool, Any, str, Path | None]:
    """Kiểm tra đường dẫn file tồn tại, đúng định dạng và cú pháp JSON hợp lệ.

    Returns:
        (is_valid, parsed_data, message, path_obj)
    """
    if isinstance(file_path_str, Path):
        path = file_path_str
    else:
        cleaned_path = clean_path_input(file_path_str)
        if not cleaned_path:
            return False, None, "Lỗi: Đường dẫn không được để trống.", None
        path = Path(cleaned_path)

    if not path.exists():
        return False, None, f"Lỗi: Đường dẫn không tồn tại: {path}", path

    if not path.is_file():
        return False, None, f"Lỗi: Đường dẫn không phải là một tập tin: {path}", path

    if not path.name.lower().endswith(".json"):
        return False, None, f"Lỗi: File bạn nhập không phải là file json. Vui lòng nhập lại: {path}", path

    # Kiểm tra cú pháp JSON
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
        return (
            True,
            data,
            f"Chúc mừng, bạn đã vượt qua, đường dẫn: {path} là hợp lệ",
            path,
        )
    except UnicodeDecodeError as e:
        return (
            False,
            None,
            f"Lỗi mã hóa file '{path}' (không thể đọc chuẩn UTF-8): {e}",
            path,
        )
    except json.JSONDecodeError as e:
        return (
            False,
            None,
            f"Lỗi cú pháp JSON trong file '{path}': Dòng {e.lineno}, Cột {e.colno} (Ký tự {e.pos}) - {e.msg}",
            path,
        )
    except Exception as e:
        return False, None, f"Lỗi không xác định khi đọc file '{path}': {e}", path


def prompt_for_valid_json_file(prompt_message: str) -> Tuple[Path, Any]:
    """Hỏi người dùng đường dẫn file trong vòng lặp cho đến khi hợp lệ cả đường dẫn và cú pháp."""
    while True:
        user_input = input(f"{prompt_message}: ")
        cleaned = clean_path_input(user_input)

        if cleaned.lower() in ("exit", "quit", "q"):
            print("Đã hủy thao tác theo yêu cầu.")
            raise SystemExit(0)

        is_valid, data, message, path_obj = validate_json_file(cleaned)
        print(message)

        if is_valid and path_obj is not None:
            return path_obj, data

        print("Vui lòng thử lại hoặc gõ 'q' để thoát.\n")
