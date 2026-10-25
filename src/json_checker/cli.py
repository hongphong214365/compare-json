"""
Module CLI xử lý giao diện dòng lệnh, tham số đầu vào và điều phối chương trình.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional, Sequence

from json_checker import __version__
from json_checker.comparator import compare_json_data
from json_checker.reporter import display_comparison_summary, handle_export_workflow
from json_checker.validator import prompt_for_valid_json_file, validate_json_file


def build_parser() -> argparse.ArgumentParser:
    """Xây dựng bộ phân tích cú pháp dòng lệnh."""
    parser = argparse.ArgumentParser(
        prog="compare-json",
        description="Công cụ kiểm tra cú pháp và so sánh key giữa các file JSON chuyên nghiệp.",
        epilog=(
            "Ví dụ sử dụng:\n"
            "  compare-json (chạy chế độ nhập tay tương tác)\n"
            "  compare-json --source-file en.json --destination-file vi.json\n"
            "  compare-json -s en.json -d vi.json -o missing.txt --threshold 10\n"
            "  compare-json --check -s en.json -d vi.json (chỉ kiểm tra cú pháp JSON)\n"
            "  compare-json --check (kiểm tra cú pháp tương tác)\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Nhóm tham số nguồn / đích
    parser.add_argument(
        "-s",
        "--source-file",
        "--sof",
        dest="source_file",
        help="Đường dẫn tới file JSON gốc / nguồn (Source).",
    )
    parser.add_argument(
        "-d",
        "--destination-file",
        "--def",
        dest="destination_file",
        help="Đường dẫn tới file JSON cần đối chiếu / đích (Destination).",
    )

    # Positional arguments dự phòng khi gõ nhanh: tool file1.json file2.json
    parser.add_argument(
        "positional_files",
        nargs="*",
        metavar="FILE",
        help="Đường dẫn file (hỗ trợ nhập nhanh 1 hoặc 2 file trực tiếp không cần cờ).",
    )

    # Tham số kiểm tra cú pháp thuần túy
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="Chỉ kiểm tra cú pháp JSON của các file mà không tiến hành so sánh key.",
    )

    # Tham số xuất file
    parser.add_argument(
        "-o",
        "--output",
        help="Đường dẫn file để ghi kết quả key bị thiếu/thừa (ví dụ: result.txt).",
    )

    # Ngưỡng ghi file
    parser.add_argument(
        "-t",
        "--threshold",
        type=int,
        default=5,
        help="Ngưỡng số lượng key bị thiếu để kích hoạt gợi ý hoặc tự động ghi ra file (mặc định: 5, có thể đặt 10, 15...).",
    )

    # Phiên bản
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    return parser


def run_syntax_check_mode(
    source_arg: Optional[str],
    dest_arg: Optional[str],
) -> int:
    """Chế độ chỉ kiểm tra cú pháp file JSON (--check)."""
    print("\n--- CHẾ ĐỘ KIỂM TRA CÚ PHÁP JSON (--check) ---")

    # Xác định file 1
    if source_arg:
        valid1, _, msg1, path1 = validate_json_file(source_arg)
        print(f"[File 1] {msg1}")
    else:
        path1, _ = prompt_for_valid_json_file("Nhập đường dẫn tới file JSON thứ nhất cần kiểm tra")
        valid1 = True

    # Xác định file 2
    if dest_arg:
        valid2, _, msg2, path2 = validate_json_file(dest_arg)
        print(f"[File 2] {msg2}")
    else:
        path2, _ = prompt_for_valid_json_file("Nhập đường dẫn tới file JSON thứ hai cần kiểm tra")
        valid2 = True

    all_valid = valid1 and valid2
    if all_valid:
        print("\n[V] Toàn bộ file đã kiểm tra đều có cú pháp JSON chuẩn xác!")
        return 0
    else:
        print("\n[X] Có file không vượt qua kiểm tra cú pháp!")
        return 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Hàm chạy chính của chương trình."""
    parser = build_parser()
    args = parser.parse_args(argv)

    # Xử lý tham số nguồn và đích (ưu tiên cờ -s, -d, nếu không có thì lấy từ positional_files)
    source_path_input = args.source_file
    dest_path_input = args.destination_file

    if args.positional_files:
        if not source_path_input and len(args.positional_files) >= 1:
            source_path_input = args.positional_files[0]
        if not dest_path_input and len(args.positional_files) >= 2:
            dest_path_input = args.positional_files[1]

    # Kiểm tra cờ --check
    if args.check:
        return run_syntax_check_mode(source_path_input, dest_path_input)

    # Xác định tương tác hay CLI trực tiếp
    is_interactive = False

    # Lấy dữ liệu file nguồn
    if source_path_input:
        valid_src, source_data, msg_src, src_path = validate_json_file(source_path_input)
        print(msg_src)
        if not valid_src or src_path is None:
            return 1
    else:
        is_interactive = True
        src_path, source_data = prompt_for_valid_json_file(
            "Nhập đường dẫn tới file JSON thứ nhất của bạn (Source)"
        )

    # Lấy dữ liệu file đích
    if dest_path_input:
        valid_dst, dest_data, msg_dst, dst_path = validate_json_file(dest_path_input)
        print(msg_dst)
        if not valid_dst or dst_path is None:
            return 1
    else:
        is_interactive = True
        dst_path, dest_data = prompt_for_valid_json_file(
            "Nhập đường dẫn tới file JSON thứ hai của bạn (Destination)"
        )

    # Tiến hành so sánh key
    result = compare_json_data(source_data, dest_data)

    # Hiển thị kết quả ra console
    display_comparison_summary(result, src_path, dst_path)

    # Xử lý xuất file theo ngưỡng (--threshold, mặc định 5 hoặc 10/15 tùy chọn)
    handle_export_workflow(
        result=result,
        source_path=src_path,
        dest_path=dst_path,
        output_arg=args.output,
        threshold=args.threshold,
        interactive=is_interactive,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
