# MapReduce Data Processing Model

> English notes for long-term storage/exam revision. 🇻🇳 *Vietnamese callouts flag the exact misconceptions we ran into while discussing this lecture — these are the highest-value parts of the file for exam prep.*

---

## 1. Big Picture

This lecture answers: *"Inside one MapReduce job, exactly how does data move and transform, stage by stage — and which machine does each stage actually run on?"*

Five roles appear across this lecture — do not conflate them:

| Role | What it does | Aggregates data? |
|---|---|---|
| **Map** | Transforms/filters *one record at a time*, independently | **No** |
| **Combiner** | Optional local mini-Reduce, on the *same* node right after Map | **Yes — locally only** |
| **Partitioner** | Decides *which Reducer* a key should go to | **No — routing only** |
| **Shuffle-and-Sort** | Copies data across the network to the right Reducer, sorts by key | Groups data, doesn't compute |
| **Reduce** | Aggregates *all* values of a key, from *every* node | **Yes — globally, final** |

> 🇻🇳 **Đây là điểm nhầm lẫn lớn nhất của cả buổi học:** Map **KHÔNG** gộp các key giống nhau lại. Map chỉ biến đổi/lọc từng bản ghi độc lập, không biết và không thể biết các bản ghi khác (kể cả trên cùng node) có cùng key hay không, trừ khi có Combiner chạy sau nó. Việc "gộp key cùng loại trong 1 node" chính là việc của **Combiner** — một bước riêng biệt, tùy chọn, chạy *sau* Map.

---

## 2. Key-Value Pairs — the basic data model

All input, output, and intermediate records in MapReduce are key-value pairs. Critically: **a key is not required to be unique**.

> 🇻🇳 Khác hẳn "key" trong SQL/relational database (phải unique) — ở đây key chỉ là "nhãn để gom nhóm", một triệu bản ghi có thể cùng chung một key (ví dụ cùng tuổi 25) và điều đó hoàn toàn bình thường.

---

## 3. Map Phase

### 3.1 Signature and behaviour

```
map(in_key, in_value) → list(intermediate_key, intermediate_value)
```

Each call processes **one** input pair and emits **0 or more** output pairs. Mappers **never communicate with each other** — this independence is what makes MapReduce embarrassingly parallel.

- **0 outputs** → filtering (SQL `WHERE` equivalent). `Map(k,v) = if (ERROR in v) then emit(k,v)` → **used for Task 3**.
- **1 output** → 1-to-1 transform.
- **Many outputs** → splitting/duplicating (e.g. WordCount: one line → many `(word, 1)` pairs).

### 3.2 Where Map physically runs — data locality

Hadoop tries to run each Map task **on the very node that already stores the input block** (a DataNode), rather than moving the data to a compute node. This is called **data locality**, first introduced in Lecture 2.

> 🇻🇳 Ví dụ: 10 node, mỗi node có 1 block dữ liệu → 10 Map task được giao chạy **ngay tại chỗ**, không có dữ liệu nào truyền qua mạng ở bước này (trừ khi máy đó quá tải, phải chuyển task sang máy khác — đây là ngoại lệ, không phải quy tắc).

### 3.3 Partitioner — routing, not aggregation

```
Reducer_target = hash(key) % number_of_reducers
```

Ensures every key + its values are sent to **one and only one** Reducer. Runs per-record, immediately after Map (or after the Combiner if present).

> 🇻🇳 Partitioner **không tính toán gì cả**, nó chỉ "dán nhãn địa chỉ" cho mỗi bản ghi — giống nhân viên phân loại thư theo địa chỉ, không đọc/gộp nội dung thư. Số lượng Reducer là **con số cấu hình trước khi job chạy**, hoàn toàn độc lập với số node hay số Mapper — không cần "thêm node mới" để có thêm Reducer.

---

## 4. Combiner Phase — optional local aggregation

If the Reduce function is **commutative and associative**, it can run early — right after Map, on the *same node*, on *only the data that node produced* — as a **Combiner**.

```
Node A after Map:      (20,(10,1))  (20,(15,1))  (30,(20,1))
Node A after Combiner: (20,(25,2))  (30,(20,1))
```

- **SUM, COUNT**: commutative + associative → safe to combine.
- **AVG**: **not** safe to combine directly (see Section 6 — this is the critical gotcha of the lecture).

> 🇻🇳 Combiner = "mini-Reduce cục bộ" — dùng đúng logic hàm Reduce nhưng chỉ nhìn thấy dữ liệu **trên node đó**, chưa thấy dữ liệu từ các node khác. Là **tùy chọn** (job vẫn đúng nếu bỏ qua Combiner, chỉ chậm hơn/tốn băng thông hơn khi Shuffle). Ngược lại, Mapper và Reducer là **bắt buộc**.

**Map-Only jobs**: an application can have **0 Reduce tasks** when no grouping/aggregation is needed — e.g. ETL without summarization, file format conversion, image processing.

---

## 5. Shuffle-and-Sort — where grouping across nodes actually happens

This is the **automatic, framework-managed** stage between Map(+Combiner) and Reduce. It has two parts:

1. **Copy**: intermediate output, already split into per-partition files on each Mapper's **local disk**, is **physically transferred over the network** to the Reducer that owns that partition. The Reducer **pulls** the data (via HTTP fetch) from each completed Map task — it is not simply referenced/pointed to.
2. **Sort**: at each Reducer, the received data (arriving from many different Mappers) is **merge-sorted** by key so all values of the same key sit contiguously, ready for Reduce to process sequentially.

> 🇻🇳 **Điểm nhầm lẫn quan trọng thứ hai:** Dữ liệu được **copy thật sự** qua mạng, không phải dùng con trỏ/tham chiếu để Reducer "truy vấn từ xa" mỗi khi cần. Lý do: nếu dùng remote reference, mỗi lần đọc 1 giá trị sẽ tốn 1 lượt gọi mạng — với hàng triệu bản ghi sẽ cực kỳ chậm. Copy một lần rồi xử lý cục bộ hiệu quả hơn nhiều. (Dữ liệu gốc trên Map-node không bị xoá ngay — giữ lại để phục vụ fault tolerance, phòng khi Reduce task cần chạy lại.)
>
> Ví dụ minh hoạ toàn cảnh (2 node Map, 2 Reducer X/Y):
> ```
> Node A (Map):  (20,(10,1))   (30,(20,1))
> Node B (Map):  (20,(15,1))   (30,(25,1))
>       ↓ Copy qua mạng theo Partitioner ↓
> Reducer X (nhận mọi bản ghi key=20, từ CẢ A và B):
>    → S=10+15=25, C=2 → output (20,(25,2))
> Reducer Y (nhận mọi bản ghi key=30, từ CẢ A và B):
>    → output (30,(45,2))
> ```
> Lưu ý: kết quả `(20,(25,2))` **không** nằm lại trên Node A — nó nằm trên node chạy Reducer X, vì Node A chỉ từng giữ **một nửa** dữ liệu của key 20.

---

## 6. Why AVG cannot be a Combiner — the central gotcha

Averaging is **not commutative + associative** when group sizes differ:

```
Group A = [10]        → avg_A = 10
Group B = [2, 2, 2]    → avg_B = 2
avg(avg_A, avg_B) = (10+2)/2 = 6      ← WRONG
true avg([10,2,2,2]) = 16/4 = 4        ← CORRECT
```

**Fix**: never compute AVG at Map/Combiner time. Instead emit `(key, (value, 1))`; accumulate SUM (S) and COUNT (C) across all nodes at Reduce time; divide **exactly once**, at the very end.

> 🇻🇳 Đây là "bẫy toán học" quan trọng nhất của cả lecture, và là công thức trực tiếp cho **Task 4** (GROUP BY + AVG). Không tính trung bình cục bộ rồi lấy trung bình của các trung bình — luôn tách thành SUM + COUNT, chỉ chia một lần duy nhất ở bước Reduce cuối cùng.

### Worked example — average contacts by age

Equivalent SQL: `SELECT age, AVG(contacts) FROM social.person GROUP BY age`

```
function Map is
    for each person record:
        let Y = age, N = number of contacts
        emit (Y, (N, 1))
end function

function Reduce is
    input: age Y, with a stream of (N, C) pairs
    accumulate S = sum of all N
    accumulate C_new = sum of all C
    let A = S / C_new
    emit (Y, (A, C_new))
end function
```

### Streaming code (Python, Hadoop Streaming — used in Task 3/4)

```python
# mapper.py
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    age, contacts = line.split(',')
    contacts = int(contacts)
    print(f"{age}\t{contacts}\t1")
```

```python
# reducer.py
#!/usr/bin/env python3
import sys
current_age = None
sum_contacts = 0
count = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    age, contacts, one = line.split('\t')
    contacts, one = int(contacts), int(one)
    if current_age == age:
        sum_contacts += contacts
        count += one
    else:
        if current_age is not None:
            avg = sum_contacts / count
            print(f"{current_age}\t{avg}\t{count}")
        current_age, sum_contacts, count = age, contacts, one
if current_age is not None:
    avg = sum_contacts / count
    print(f"{current_age}\t{avg}\t{count}")
```

> 🇻🇳 **Khác biệt quan trọng giữa Hadoop Streaming và Java API:** Trong Java API, Hadoop tự gom sẵn "toàn bộ value của 1 key" thành 1 iterator đưa cho hàm reduce. Nhưng trong Streaming, dữ liệu tới reducer **từng dòng một, đã sort theo key** — bạn phải **tự viết logic phát hiện khi nào key đổi** (biến `current_age` + so sánh) để biết lúc nào một nhóm kết thúc. Đừng quên đoạn code "chốt sổ" nhóm cuối cùng **sau vòng lặp** — lỗi rất hay bị bỏ sót vì nhóm cuối không có dòng tiếp theo để kích hoạt việc flush.

---

## 7. Physical execution across the cluster — who runs where

| Component | What it is | Where it runs | Lifetime |
|---|---|---|---|
| **ResourceManager** | Cluster-wide resource allocator | **One fixed master node** | Permanent (starts with Hadoop, runs forever) |
| **NodeManager** | Per-machine resource manager, creates containers | **Every worker node** (one each) | Permanent |
| **MRAppMaster** | Per-**job** coordinator — requests containers for that job's Map/Reduce tasks | **Any node** the ResourceManager assigns a free container to, decided at job submission time | **Temporary** — exists only while that job runs |

> 🇻🇳 Bảng này trả lời trực tiếp thắc mắc "container Reduce chạy ở node nào" — **không cố định trước**. `MRAppMaster` mới là "người quyết định" xin ResourceManager cấp container ở node nào đang rảnh, tại thời điểm job cần — hoàn toàn không cần "tạo thêm node mới" để có chỗ chạy Reduce. Vì MRAppMaster là tiến trình tạm thời, nó **không xuất hiện trong `jps`** khi không có job nào đang chạy — chỉ xuất hiện trong lúc job thực thi rồi biến mất.

### Job lifecycle (11-step submission flow)

1. Client runs job (`MapReduce program` → `Job`)
2. Job asks ResourceManager for a new Application ID
3. Job copies resources (jar, config) to the **Shared Filesystem (HDFS)**
4. Job submits the application to ResourceManager
5. ResourceManager starts a container on a free NodeManager (5a), which launches **MRAppMaster** inside it (5b)
6. MRAppMaster initializes the job
7. MRAppMaster retrieves input splits from the Shared Filesystem
8. MRAppMaster requests more containers from ResourceManager for Map/Reduce tasks
9. ResourceManager starts containers on (possibly different) NodeManagers (9a), which launch task JVMs (`YarnChild`) (9b)
10. Each `YarnChild` retrieves job resources from the Shared Filesystem
11. The actual `MapTask` or `ReduceTask` runs

> 🇻🇳 Chú ý: `Shared Filesystem (HDFS)` là điểm mà **mọi thành phần đều quay lại lấy dữ liệu** (bước 3, 7, 10) — không phải một node "trỏ" dữ liệu sang node khác. Sơ đồ 11 bước này dừng lại ở bước 11 (task bắt đầu chạy); luồng Copy/Shuffle giữa các MapTask/ReduceTask (Section 5 ở trên) là một luồng riêng, xảy ra **sau** khi MapTask đã ghi xong output cục bộ.

---

## 8. WordCount Counters — reading real job output

```
Map input records       = 124,787
Map output records      = 904,061
Combine input records   = 904,061
Combine output records  =  67,779   ← Combiner shrank data ~13x before network transfer
Reduce input records    =  67,779
Reduce shuffle bytes    = 983,187   ← actual data volume that crossed the network
```

> 🇻🇳 Đây là bằng chứng số liệu thật cho việc Combiner hiệu quả thế nào: gần 1 triệu bản ghi giảm còn 67,779 trước khi truyền qua mạng. "Reduce shuffle bytes" chính là con số duy nhất đại diện cho network I/O thật sự trong toàn bộ job — Map input/output hoàn toàn là công việc cục bộ (local I/O), không tốn băng thông mạng.

---

## 9. Code ownership — what you write vs. what Hadoop handles

| Component | Who writes/implements it |
|---|---|
| `map()` logic | **You** (e.g. `mapper.py`) |
| `reduce()` logic | **You** (e.g. `reducer.py`) |
| Partitioner (hash routing) | Hadoop by default (overridable, advanced) |
| Copying data over the network | Hadoop entirely |
| Sorting/merging intermediate data | Hadoop entirely |
| Container scheduling (YARN) | Hadoop/YARN entirely |
| Fault tolerance / task retry | Hadoop entirely |

> 🇻🇳 Bạn chỉ viết "công thức xử lý 1 bản ghi" (map) và "công thức gộp 1 nhóm" (reduce) — toàn bộ phần hạ tầng phân tán (định tuyến, di chuyển dữ liệu, sắp xếp, điều phối, chịu lỗi) là Hadoop lo, đúng nguyên lý "separation of programming logic and scheduling/management" đã học ở Lecture 2.

---

## 10. Self-Check Questions

1. Correct this statement: "The Map phase gathers all key-value pairs of the same key together." What is actually true, and which stage does the gathering?
2. Distinguish Combiner from Partitioner — one line each on what they do and whether they aggregate data.
3. Why must a Combiner's operation be commutative and associative? Give a numeric counter-example showing why AVG breaks this rule.
4. Write the Map and Reduce pseudocode for "average contacts by age." Explain the role of each variable (Y, N, S, C, A).
5. In Hadoop Streaming, why must the reducer manually track a "current key" variable, unlike the Java API? What happens if you forget to flush the last group after the loop?
6. Is data physically copied during Shuffle, or accessed by reference across nodes? Justify with a reasoning about network cost.
7. Where does data locality apply to Map, and why does it minimize network usage?
8. Name the three YARN-related components discussed and, for each: how many instances exist in a cluster, where each runs, and its lifetime.
9. Why does `MRAppMaster` not show up in `jps` when no job is running?
10. Walk through the 11-step job submission flow, noting every point where a component contacts the Shared Filesystem.
11. From the WordCount Counters, explain why "Combine output records" is far smaller than "Map output records," and how that number relates to network transfer cost.
12. Directly connect this lecture to Assignment 1: what Map-phase technique does Task 3 need? What does Task 4 need at both Map and Reduce?
