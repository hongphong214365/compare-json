# JSON Checker & Key Comparator (compare-json)

> **Công cụ so sánh key và kiểm tra cú pháp JSON mạnh mẽ, hỗ trợ CLI và chế độ nhập liệu tương tác.**

---

##  Tính Năng Nổi Bật

1. **Làm sạch dữ liệu đầu vào thông minh (`clean_path_input`)**:
   - Tự động loại bỏ khoảng trắng thừa ở hai đầu đường dẫn (`strip`).
   - Tự động gỡ bỏ các dấu ngoặc kép `"` hoặc dấu nháy đơn `'` bao quanh (thường phát sinh khi kéo thả file trực tiếp vào Terminal).

2. **Kiểm tra cú pháp JSON (`validate_json_file`)**:
   - Kiểm tra đường dẫn có tồn tại và đúng định dạng `.json`.
   - Phân tích cú pháp (`json.load`), báo rõ vị trí lỗi (dòng, cột, ký tự) nếu file JSON bị sai cú pháp.
   - Chỉ hiển thị thông báo hợp lệ (`Chúc mừng, bạn đã vượt qua, đường dẫn: ... là hợp lệ`) khi file và cú pháp đều hoàn toàn chính xác.

3. **Chế độ kiểm tra cú pháp nhanh (`--check` / `-c`)**:
   - Dùng để kiểm tra nhanh 2 file JSON có chuẩn cú pháp hay không mà không cần so sánh key.

4. **Hỗ trợ tham số dòng lệnh (CLI Direct Path)**:
   - Truyền trực tiếp đường dẫn file mà không cần chờ câu hỏi nhập liệu:
     - Nguồn: `-s`, `--source-file`, `--sof`
     - Đích: `-d`, `--destination-file`, `--def`
     - Hoặc gõ tắt: `compare-json file1.json file2.json`

5. **Xuất kết quả ra file & Cơ chế ngưỡng (`--threshold` / `-t`)**:
   - Chỉ định file lưu kết quả bằng `-o` hoặc `--output`.
   - Cấu hình ngưỡng key bị thiếu qua `-t` hoặc `--threshold` (mặc định: 5 key; có thể chỉnh thành 10, 15...).
   - Nếu số key thiếu vượt ngưỡng:
     - Ở chế độ tương tác: hỏi xác nhận người dùng và cho phép đặt tên file xuất.
     - Ở chế độ CLI tự động: tự động xuất ra file `missing_keys.txt`.

6. **Đóng gói file thực thi `.exe` độc lập (PyInstaller One-File)**:
   - Chạy trực tiếp trên Windows mà không cần cài đặt Python. Có thể thêm file `.exe` vào biến môi trường `PATH`.

---

## 📂 Cấu Trúc Repository

```text
tool/
├── .gitignore               # Tệp cấu hình bỏ qua git
├── pyproject.toml           # Cấu hình project, metadata và entrypoint
├── README.md                # Tài liệu hướng dẫn sử dụng chi tiết
├── compareJsonFiles.py      # Entrypoint chính (tương thích ngược)
├── src/
│   └── json_checker/
│       ├── __init__.py      # Khai báo package và version
│       ├── validator.py     # Làm sạch input, kiểm tra file và cú pháp JSON
│       ├── comparator.py    # Thuật toán làm phẳng key đa tầng (dict/list) & so sánh
│       ├── reporter.py      # Hiển thị console & xuất báo cáo ra file
│       └── cli.py           # Bộ phân tích CLI (argparse) và điều hướng luồng
├── tests/
│   ├── data/                # Dữ liệu JSON mẫu (hợp lệ & lỗi cú pháp)
│   ├── test_validator.py    # Test module validator
│   ├── test_comparator.py   # Test module so sánh
│   └── test_cli.py          # Test luồng CLI
└── dist/
    └── compare-json.exe     # File thực thi one-file (sau khi build)
```

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Sử dụng trực tiếp bằng Python

#### Chế độ nhập tương tác (Interactive):
```powershell
python compareJsonFiles.py
```
*Chương trình sẽ hỏi từng đường dẫn, kiểm tra cú pháp và chỉ in thông báo chúc mừng khi file hoàn toàn hợp lệ.*

#### Chế độ truyền trực tiếp tham số (CLI):
```powershell
# Truyền cờ chuẩn
python compareJsonFiles.py -s en.json -d vi.json

# Dùng alias --sof và --def
python compareJsonFiles.py --sof en.json --def vi.json

# Xuất ra file kết quả
python compareJsonFiles.py -s en.json -d vi.json -o result.txt

# Đặt ngưỡng phát hiện key thiếu là 10 (mặc định là 5)
python compareJsonFiles.py -s en.json -d vi.json -t 10
```

#### Chế độ chỉ kiểm tra cú pháp (`--check`):
```powershell
# Kiểm tra cú pháp 2 file trực tiếp
python compareJsonFiles.py --check -s en.json -d vi.json

# Hoặc chạy kiểm tra cú pháp dạng hỏi đáp
python compareJsonFiles.py --check
```

---

##  Quản Lý Bằng `uv` (Khuyên dùng)

### Cài đặt môi trường & dependencies:
```powershell
uv venv
uv pip install -e .
```

Sau khi cài đặt gói ở chế độ editable (`-e`), bạn có thể gọi trực tiếp lệnh:
```powershell
compare-json -s en.json -d vi.json
```

---

## 🧪 Chạy Kiểm Thử (Unit Tests)

Dự án đi kèm bộ unit test toàn diện:
```powershell
python -m unittest discover tests
```

---

## 📦 Build File `.exe` Độc Lập Bằng PyInstaller

Để tạo một file thực thi duy nhất (`.exe`) không phụ thuộc môi trường:

### Cách 1: Sử dụng `uv`
```powershell
uv run --with pyinstaller pyinstaller --onefile --name compare-json compareJsonFiles.py
```

### Cách 2: Sử dụng `pyinstaller` trực tiếp
```powershell
pip install pyinstaller
pyinstaller --onefile --name compare-json compareJsonFiles.py
```

Sau khi hoàn tất, file thực thi sẽ nằm tại:
```text
dist/compare-json.exe
```
Bạn chỉ cần copy file `compare-json.exe` vào một thư mục có trong biến môi trường `PATH` (ví dụ `C:\Windows\System32` hoặc thư mục `bin` cá nhân của bạn) để gọi `compare-json` từ bất kỳ đâu trong Command Prompt hoặc PowerShell.
