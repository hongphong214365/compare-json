"""
Module xử lý hiển thị kết quả và xuất kết quả ra file.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from json_checker.comparator import ComparisonResult


def display_comparison_summary(
    result: ComparisonResult,
    source_path: Path | str,
    dest_path: Path | str,
) -> None:
    """In tóm tắt kết quả so sánh ra màn hình console."""
    print("\n" + "=" * 60)
    print(" KẾT QUẢ SO SÁNH JSON")
    print("=" * 60)
    print(f"File nguồn (Source)     : {source_path}")
    print(f"File so sánh (Dest)     : {dest_path}")
    print("-" * 60)
    print(f"Tổng số key nguồn       : {result.total_source}")
    print(f"Tổng số key đích        : {result.total_dest}")
    print(f"Số key bị thiếu ở đích  : {result.missing_count}")
    print(f"Số key thừa ở đích      : {result.extra_count}")
    print("=" * 60)

    if result.missing_count > 0:
        print(f"\nDanh sách {result.missing_count} key bị thiếu:")
        for key in result.missing_in_dest:
            print(f"  [-] {key}")
    else:
        print("\n Tuyệt vời! Không có key nào bị thiếu.")

    if result.extra_count > 0:
        print(f"\nDanh sách {result.extra_count} key thừa ở file đích:")
        for key in result.extra_in_dest:
            print(f"  [+] {key}")


def export_result_to_file(
    result: ComparisonResult,
    output_path: Path | str,
    source_path: Path | str,
    dest_path: Path | str,
) -> Optional[Path]:
    """Xuất báo cáo so sánh chi tiết ra tập tin văn bản."""
    target_path = Path(output_path)
    try:
        target_path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"\n[!] Không thể tạo thư mục cho file xuất '{target_path.parent}': {e}")
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "============================================================",
        " BÁO CÁO SO SÁNH FILE JSON",
        f" Thời gian tạo: {timestamp}",
        "============================================================",
        f"File nguồn (Source): {source_path}",
        f"File đích  (Dest)  : {dest_path}",
        "------------------------------------------------------------",
        f"Tổng số key nguồn      : {result.total_source}",
        f"Tổng số key đích       : {result.total_dest}",
        f"Số lượng key bị thiếu  : {result.missing_count}",
        f"Số lượng key thừa      : {result.extra_count}",
        "============================================================",
        "",
        f"--- DANH SÁCH KEY BỊ THIẾU ({result.missing_count} key) ---",
    ]

    if result.missing_in_dest:
        for key in result.missing_in_dest:
            lines.append(f"- {key}")
    else:
        lines.append("(Không có key nào bị thiếu)")

    if result.extra_in_dest:
        lines.append("")
        lines.append(f"--- DANH SÁCH KEY THỪA ({result.extra_count} key) ---")
        for key in result.extra_in_dest:
            lines.append(f"+ {key}")

    lines.append("")
    lines.append("============================================================")

    try:
        target_path.write_text("\n".join(lines), encoding="utf-8")
        return target_path
    except Exception as e:
        print(f"\n[!] Cảnh báo: Không thể ghi file kết quả ra '{target_path}': {e}")
        return None


def handle_export_workflow(
    result: ComparisonResult,
    source_path: Path | str,
    dest_path: Path | str,
    output_arg: Optional[str | Path] = None,
    threshold: int = 5,
    interactive: bool = True,
) -> Optional[Path]:
    """Xử lý điều kiện và ghi file kết quả:
    - Nếu có output_arg được chỉ định: ghi ngay ra file đó.
    - Nếu thiếu từ threshold key trở lên:
        + Trong chế độ tương tác (interactive): hỏi người dùng và cho phép nhập đường dẫn/dùng mặc định.
        + Trong chế độ CLI không tương tác: tự động xuất ra file 'missing_keys.txt'.
    """
    default_output = Path("missing_keys.txt")

    # Trường hợp 1: Người dùng đã chỉ định file output qua tham số CLI
    if output_arg:
        out_path = Path(output_arg)
        saved = export_result_to_file(result, out_path, source_path, dest_path)
        if saved:
            print(f"\n[+] Đã xuất kết quả so sánh ra file: {saved.resolve()}")
        return saved

    # Trường hợp 2: Số key thiếu vượt ngưỡng quy định (mặc định 5 hoặc tùy chỉnh qua --threshold)
    if result.missing_count >= threshold:
        if interactive:
            print(
                f"\n[!] Chú ý: Phát hiện {result.missing_count} key bị thiếu (đạt ngưỡng >= {threshold} key)."
            )
            confirm = input(
                f"Bạn có muốn xuất danh sách ra file không? [Y/n] (mặc định: '{default_output.name}'): "
            ).strip().lower()

            if confirm in ("", "y", "yes"):
                custom_name = input(
                    f"Nhập tên file xuất (nhấn Enter để dùng '{default_output.name}'): "
                ).strip()
                target = Path(custom_name) if custom_name else default_output
                saved = export_result_to_file(result, target, source_path, dest_path)
                if saved:
                    print(f"[+] Đã lưu thành công ra file: {saved.resolve()}")
                return saved
            else:
                print("[-] Bỏ qua việc xuất file theo yêu cầu.")
        else:
            # Chế độ non-interactive nhưng thiếu nhiều key >= threshold
            saved = export_result_to_file(result, default_output, source_path, dest_path)
            if saved:
                print(
                    f"\n[!] Số key thiếu ({result.missing_count}) >= ngưỡng ({threshold}). "
                    f"Tự động xuất kết quả ra: {saved.resolve()}"
                )
            return saved

    return None
