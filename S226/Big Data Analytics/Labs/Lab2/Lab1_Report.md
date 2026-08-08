# CSCI446/946 Big Data Analytics — Lab 1 Report
## Working with Different Data Types

---

## Task 1 — Structured Data: Yearly Sales (CSV)

**Kết quả chạy:**
- Shape: (12 rows, 4 columns) — cột: `cust_id`, `sales_total`, `num_of_orders`, `gender`
- `sales_total`: min = 74.58, mean = 1027.65, max = 3175.80

**Câu hỏi & trả lời:**

**1. How many rows and columns are in the dataset?**
Dataset có **12 dòng và 4 cột**: `cust_id`, `sales_total`, `num_of_orders`, `gender`.

**2. What are the minimum, mean and maximum values of sales_total?**
- Min: **74.58**
- Mean: **1027.65**
- Max: **3175.80**

**3. What does the plot suggest about the relationship between the number of orders and total sales?**
Biểu đồ cho thấy xu hướng **tương quan thuận (positive correlation)** giữa số đơn hàng (`num_of_orders`) và tổng doanh số (`sales_total`) — khách hàng đặt nhiều đơn hơn thì tổng chi tiêu có xu hướng cao hơn. Tuy nhiên quan hệ không hoàn toàn tuyến tính (độ lệch chuẩn của `sales_total` khá lớn so với mean), nên có một số khách hàng lệch khỏi xu hướng chung — ví dụ đặt ít đơn nhưng giá trị mỗi đơn cao.

---

## Task 2 — Semi-structured Data: XML Student Records

**Kết quả chạy:**
- Root tag: `students`
- Số học sinh: 5

| student_id | name | program | year | mark |
|---|---|---|---|---|
| S001 | Alice | Computer Science | 1 | 78 |
| S002 | Ben | Data Science | 2 | 85 |
| S003 | Chen | Computer Science | 1 | 72 |
| S004 | Divya | Information Technology | 3 | 91 |
| S005 | Emma | Data Science | 2 | 81 |

**Câu hỏi & trả lời:**

**1. What is the root tag of the XML document?**
Root tag là **`students`**.

**2. What is the difference between the student id attribute and the name element?**
- `id` là **attribute** — nằm ngay trong thẻ mở `<student id="S001">`, dùng để định danh nhanh, dữ liệu ngắn gọn, không lồng thêm cấp con.
- `name` là **element (child tag)** — là thẻ con độc lập `<name>Alice</name>` nằm bên trong `<student>`, có thể chứa văn bản hoặc lồng thêm các thẻ con khác nếu cần.

Tóm lại: attribute mô tả *thuộc tính/metadata* của thẻ cha; element là *nội dung/dữ liệu con* theo cấu trúc cây.

**3. Which student has the highest mark?**
**Divya** (student_id `S004`, chương trình Information Technology, năm 3) với **mark = 91**.

---

## Task 3 — Quasi-structured Data: Web Clickstream

**Kết quả chạy:**
- Tổng số request: 8
- Methods: GET (7), POST (1)
- Status codes: 200 (5), 302 (1), 404 (1), 500 (1)
- URL nhiều nhất: `/products/leather-jacket` (2), `/checkout` (2)

**Câu hỏi & trả lời:**

**1. How many requests are recorded in the log?**
**8 request**.

**2. Which HTTP methods appear in the log?**
**GET** (7 lần) và **POST** (1 lần).

**3. Which URL is requested most frequently?**
Có 2 URL đồng hạng cao nhất, mỗi URL xuất hiện 2 lần:
- `/products/leather-jacket`
- `/checkout`

**4. How many successful (200) responses are recorded?**
**5 response** có status code 200.

**5. Which status code indicates an error?**
- **404** (Not Found) — lỗi phía client, tài nguyên không tồn tại (ảnh `jacket.jpg`)
- **500** (Internal Server Error) — lỗi phía server

(Riêng **302** là redirect — chuyển hướng sau khi thêm vào giỏ hàng — không phải lỗi.)

**6. Why is this file considered quasi-structured rather than structured?**
Log có **định dạng lặp lại, có thể đoán trước** (IP, timestamp, method, URL, status...) giống dữ liệu có cấu trúc, nhưng **không được lưu sẵn dưới dạng bảng với schema cố định** như CSV/database — mỗi dòng chỉ là một chuỗi văn bản thuần túy. Phải dùng **regex để tự bóc tách** các trường mới chuyển được thành dạng bảng (DataFrame). Đây chính là điểm khác biệt giữa structured (đã có sẵn cột) và quasi-structured (có pattern nhưng cần "diễn giải" để lấy ra cấu trúc).

---

## Task 4 — Unstructured Data: Image

**Kết quả chạy:**
- Shape: (336, 594, 3)
- Data type: `float32`
- Top-left pixel: `[0.698, 0.8196, 0.8]`
- Cropped shape: (160, 270, 3)
- Mean red value: 0.4284

**Câu hỏi & trả lời:**

**1. What do the three values in image.shape represent?**
- `336` → **chiều cao ảnh** (số hàng pixel)
- `594` → **chiều rộng ảnh** (số cột pixel)
- `3` → **số kênh màu** (Red, Green, Blue — ảnh RGB)

**2. What information is stored in one pixel of this colour image?**
Mỗi pixel là một mảng gồm **3 giá trị cường độ màu** (Red, Green, Blue). Ví dụ pixel góc trên-trái: `[0.698, 0.8196, 0.8]`, kiểu dữ liệu `float32`, giá trị được chuẩn hóa trong khoảng 0–1 (thay vì 0–255 như thông thường).

**3. How does the cropped image differ from the original image?**
Ảnh gốc có shape `(336, 594, 3)`; sau khi crop vùng `[160:320, 300:570]`, shape còn `(160, 270, 3)` — chỉ giữ lại một vùng nhỏ hơn của ảnh gốc (160 hàng × 270 cột), số kênh màu (3) không đổi.

**4. Why can an image be called unstructured data even though Python stores it as an array?**
Mảng số (array) chỉ là **cách kỹ thuật để lưu trữ giá trị pixel**, chứ **không có field/record mang ý nghĩa được định nghĩa sẵn** như dữ liệu có cấu trúc (không có cột kiểu "đây là tòa nhà", "đây là cái cây"...). Ý nghĩa thực sự của nội dung ảnh phải được **suy luận thêm** (qua con người nhìn hoặc thuật toán computer vision), chứ không nằm sẵn trong dữ liệu như một bản ghi CSV có cột được đặt tên rõ ràng.

---

## Tóm tắt so sánh 4 loại dữ liệu

| Loại dữ liệu | File | Đặc điểm chính |
|---|---|---|
| Structured | `yearly_sales.csv` | Dạng bảng, schema cố định, dễ xử lý trực tiếp |
| Semi-structured | `students.xml` | Có cấu trúc rõ ràng nhưng dạng cây (nested tags/attributes) |
| Quasi-structured | `clickstream.log` | Có pattern lặp lại nhưng không có schema chính thức, cần regex để trích xuất |
| Unstructured | `campus.png` | Không có field/record định nghĩa sẵn, chỉ là mảng dữ liệu thô (pixel) |
