# CSCI446/946 – Lab 1: Working with Different Data Types

## Cách setup

1. Copy toàn bộ folder này (`Lab1_code`) vào:
   `D:\sun\WOLLONGONG\suncancode\S226\Big Data Analytics\Labs\Lab2`

2. Đảm bảo 4 file dataset đã có sẵn ở:
   `D:\sun\WOLLONGONG\S226\CSCI946 - Big Data Analytics\Lab\W2\Lab1-Released\CSCI446_946_Week2_Lab_SP_2026_Datasets`
   - `yearly_sales.csv`
   - `students.xml`
   - `clickstream.log`
   - `campus.png`

   (Các script đã trỏ sẵn `DATA_DIR` tới đường dẫn này — không cần copy dataset qua folder code.)

3. Cài thư viện cần thiết (nếu chưa có):
   ```
   pip install pandas matplotlib
   ```

## Cách chạy

Mỗi task là 1 file riêng, chạy độc lập:

```
python task1_csv.py
python task2_xml.py
python task3_clickstream.py
python task4_image.py
```

Hoặc mở từng file trong VS Code / Jupyter và chạy từng cell.

## File trong folder này

| File | Nội dung |
|---|---|
| `task1_csv.py` | Task 1 – CSV (structured data) |
| `task2_xml.py` | Task 2 – XML (semi-structured data) |
| `task3_clickstream.py` | Task 3 – Log file (quasi-structured data) |
| `task4_image.py` | Task 4 – Image (unstructured data) |

Mỗi file đều in ra thêm các số liệu (shape, min/mean/max, value_counts, v.v.)
để bạn dễ trả lời các câu hỏi cuối mỗi task trong đề bài, không chỉ chạy code
mẫu suông.

## Lưu ý

- Nếu bạn di chuyển dataset sang chỗ khác, chỉ cần sửa biến `DATA_DIR`
  ở đầu mỗi file cho đúng đường dẫn mới.
- Đường dẫn dùng `r"..."` (raw string) để tránh lỗi với dấu `\` trên Windows.
