# Python MapReduce Application

> English notes for long-term storage/exam revision. 🇻🇳 *Vietnamese callouts flag the exact misconceptions we worked through — these are the highest-value parts of the file for exam prep.*

---

## 1. Big Picture

This lecture answers: *"Concretely, what do I write, what does Hadoop already provide, and what does running a real job actually look like on screen?"*

> 🇻🇳 Câu trả lời cốt lõi cho cả lecture: bạn chỉ viết **logic của 2 hàm** (`map`, `reduce`); Hadoop cung cấp **cơ chế vận hành** (chia dữ liệu, gọi script đúng lúc đúng chỗ, di chuyển dữ liệu, ghi kết quả). Hadoop **không** đóng gói sẵn Python interpreter — Python phải được cài sẵn độc lập trên mọi node; Hadoop chỉ biết "gọi file này như một chương trình ngoài", không quan tâm ngôn ngữ viết bằng gì.

---

## 2. Building Blocks of a MapReduce Program

Four classes implement the MapReduce **logic**; one component represents the **client**:

| Component | Role |
|---|---|
| **Mapper** | Contains `map()`, does most of the heavy lifting (reads the entire input) |
| **Reducer** | Contains `reduce()`, usually holds the main business logic (sum, count, average...) |
| **Combiner** | Optional local mini-Reduce (see Lecture 5) |
| **Partitioner** | Routes keys to reducers (see Lecture 5) |
| **Driver / ToolRunner** | The client program — sets up and submits the job |

### 2.1 Driver

- Runs **on the client**, contains `main()`.
- Submits the application to the **ResourceManager** along with its configuration.
- Can submit **asynchronously** (non-blocking) or **synchronously** (waits for completion) — the course uses synchronous.
- A single Driver instance can orchestrate a **workflow of multiple MapReduce jobs**.

> 🇻🇳 Với Hadoop Streaming, bạn **không tự viết code Driver bằng Java** — chính dòng lệnh `hadoop jar hadoop-streaming.jar -mapper ... -reducer ...` mà bạn gõ trên terminal **đóng vai trò Driver**: nó chính là thứ submit job kèm cấu hình.

### 2.2 Mapper — additional details beyond Lecture 5

- Iterates through input via `InputFormat` + `RecordReader` to call `map()`.
- **The number of HDFS blocks determines the number of input splits, which determines the number of Mapper objects (Map tasks).** Direct link to Lecture 3 (HDFS blocks) and Lecture 5 (data locality).
- Can include **`setup()`** (runs before `map()`) and **`cleanup()`** (runs after `map()`) — for one-time initialization/teardown (e.g. opening a connection) without repeating it on every call.

### 2.3 Reducer — additional details

- Runs against **one partition**; each key + its values go into `reduce()`.
- **Reducer's `InputFormat` matches Mapper's `OutputFormat`** — the data shapes must be compatible.
- While Mapper mostly *extracts*, **Reducer usually holds the main application logic** (sum, count, averaging).
- Reducer runtime is typically **faster** than Mapper — it processes already-reduced data, not the raw full input.

---

## 3. Hadoop Streaming — the mechanism

### 3.1 How the Mapper process actually works

1. When the Mapper initializes, it starts your executable (e.g. `mapper.py`) as a **separate subprocess**.
2. It converts input into lines and **feeds them into the process's standard input (stdin)**.
3. **Simultaneously**, it collects lines from the process's **standard output (stdout)** and converts each line into a key/value pair.
4. Split rule: **everything before the first tab character is the key; everything after is the value.**

### 3.2 How the Reducer process works — identical mechanism

1. Starts your executable (e.g. `reducer.py`) as a subprocess.
2. Converts its input key/value pairs into lines, feeds them into stdin.
3. Collects stdout lines, converts each into an output key/value pair (same tab rule).

> 🇻🇳 **Ẩn dụ để nhớ:** Hadoop giống một "người mù chữ" chỉ biết đẩy giấy (dòng text) qua khe vào (stdin), nhặt giấy ở khe ra (stdout), và cắt tại tab đầu tiên — nó **không đọc hiểu** nội dung Python/logic bên trong. Đây là lý do Streaming chạy được với **bất kỳ ngôn ngữ nào** biết đọc stdin/ghi stdout — không riêng gì Python.
>
> **Hệ quả quan trọng:** vì Hadoop chỉ đẩy dữ liệu **từng dòng, đã sort theo key** vào reducer — không có khái niệm "iterator gom sẵn theo nhóm" như Java API thật sự có — bạn **phải tự viết logic phát hiện khi nào key đổi** trong `reducer.py` (biến `current_key` + so sánh), đúng như đã thực hành ở bài toán AVG.
>
> **Hadoop không cung cấp môi trường Python có sẵn.** Dòng `#!/usr/bin/env python3` đầu file (shebang) chỉ báo cho **hệ điều hành của node đó** biết dùng `python3` để chạy — Python phải được cài đặt sẵn trên **mọi node**, độc lập với Hadoop.

### 3.3 Command syntax

```
mapred streaming [genericOptions] [streamingOptions]
```

**Generic command options** (apply broadly, not streaming-specific):

| Option | Description |
|---|---|
| `-conf configuration_file` | Specify an application configuration file |
| `-D property=value` | Set value for a given property |
| `-fs host:port` or `local` | Specify a NameNode |
| `-files` | Comma-separated files to copy to the Map/Reduce cluster |
| `-libjars` | Comma-separated jar files added to the classpath |
| `-archives` | Comma-separated archives to unarchive on compute machines |

**Streaming command options:**

| Option | Description |
|---|---|
| `-input directoryname/filename` | Input location for mapper |
| `-output directoryname` (**required**) | Output location for reducer |
| `-mapper` | Mapper executable (default: `IdentityMapper`) |
| `-reducer` | Reducer executable (default: `IdentityMapper`) |
| `-file filename` | Make mapper/reducer/combiner executable available locally on each node |
| `-inputformat` / `-outputformat` | Class for input/output format |
| `-partitioner` | Custom Partitioner class |
| `-combiner` | Combiner executable for map output |
| `-cmdenv name=value` | Pass an environment variable to streaming commands |
| `-numReduceTasks` | Number of reducers |
| `-mapdebug` / `-reducedebug` | Script to call when a map/reduce task fails |

> 🇻🇳 `-numReduceTasks` là nơi bạn cấu hình con số **N** trong công thức `hash(key) % N` đã học ở Lecture 5 — đây là con số bạn tự đặt, độc lập với số node.
>
> `IdentityMapper` (giá trị mặc định của `-mapper` khi không chỉ định) chính là "hàm map built-in" duy nhất Hadoop có — nó chỉ emit lại y hệt dữ liệu nhận vào, không biến đổi gì. Hadoop không thể built-in sẵn logic nghiệp vụ thật (WordCount, AVG...) vì mỗi bài toán cần công thức khác nhau — Hadoop chỉ built-in sẵn **cơ chế gọi hàm đúng lúc đúng chỗ**, còn nội dung 2 hàm `map()`/`reduce()` luôn phải do người dùng cung cấp.

### 3.4 Real command examples

**Using a Java class as mapper, packaging a Python reducer isn't shown here but the pattern generalizes:**
```bash
mapred streaming -input Input -output Output \
    -inputformat org.apache.hadoop.mapred.KeyValueTextInputFormat \
    -mapper org.apache.hadoop.mapred.lib.IdentityMapper \
    -reducer /usr/bin/wc
```

**Packaging a Python script (`-file`):**
```bash
mapred streaming -input Input -output Output \
    -mapper myPythonScript.py \
    -reducer /usr/bin/wc \
    -file myPythonScript.py
```

**A realistic Task 3/4-style command:**
```bash
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-3.4.0.jar \
    -input /user/bigdata/input \
    -output /user/bigdata/output_avg \
    -mapper mapper.py \
    -reducer reducer.py \
    -file mapper.py \
    -file reducer.py
```

> 🇻🇳 `-file` đảm bảo script được copy tới **mọi node** sẽ chạy task đó — vì mỗi node là một "người mù chữ" riêng biệt, nếu chưa từng nhận được bản sao script, nó không có gì để chạy. `-output` phải trỏ tới một thư mục HDFS **chưa tồn tại** — nếu đã có, Hadoop báo lỗi và không chạy (tránh vô tình ghi đè kết quả cũ).

### 3.5 What a real run looks like on screen

```
$ hadoop jar hadoop-streaming-3.4.0.jar -input ... -output ... -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py

INFO mapreduce.Job: Running job: job_1755500000000_0001
INFO mapreduce.Job: Job job_1755500000000_0001 running in uber mode : false
INFO mapreduce.Job:  map 0% reduce 0%
INFO mapreduce.Job:  map 100% reduce 0%
INFO mapreduce.Job:  map 100% reduce 100%
INFO mapreduce.Job: Job job_1755500000000_0001 completed successfully
Counters: 30
    Map-Reduce Framework
        Map input records=5
        Map output records=5
        Reduce input records=5
        Reduce output records=2
```

Result on HDFS:
```
$ hdfs dfs -ls /user/bigdata/output_avg
Found 2 items
-rw-r--r--  ... 0 .../output_avg/_SUCCESS
-rw-r--r--  ... 18 .../output_avg/part-00000

$ hdfs dfs -cat /user/bigdata/output_avg/part-00000
25    8.0    3
30    3.0    2
```

> 🇻🇳 `map 100%` luôn hoàn tất **trước** `reduce` bắt đầu tăng — đúng thứ tự pipeline Map → Shuffle-Sort → Reduce. `_SUCCESS` là file rỗng chỉ báo hiệu job hoàn tất, không chứa dữ liệu. `part-00000` là output thật — nếu có N Reducer sẽ có N file `part-XXXXX`, mỗi Reducer ghi file riêng của mình.

---

## 4. Word Count — the "Hello, World" of MapReduce

> 🇻🇳 Slide gốc chỉ có ảnh phần `reducer.py` (2 cách viết), phần `mapper.py` bị thiếu trong bản gốc — mình bổ sung mapper chuẩn tương ứng bên dưới để có bộ code hoàn chỉnh.

### Mapper (standard, supplemented)
```python
#!/usr/bin/env python3
import sys
for line in sys.stdin:
    words = line.strip().split()
    for word in words:
        print(f"{word}\t1")
```

### Reducer — Approach 1: manual "current key" tracking

```python
#!/usr/bin/env python3
import sys
current_word = None
current_count = 0
word = None
for line in sys.stdin:
    line = line.strip()
    word, count = line.split('\t', 1)
    try:
        count = int(count)
    except ValueError:
        continue
    if current_word == word:
        current_count += count
    else:
        if current_word:
            print('%s\t%s' % (current_word, current_count))
        current_count = count
        current_word = word
if current_word == word:
    print('%s\t%s' % (current_word, current_count))
```

> 🇻🇳 Đây chính là pattern "biến current_key + so sánh + flush nhóm cuối" đã dùng cho bài toán AVG ở Lecture 5 — WordCount chỉ là trường hợp đơn giản hơn (COUNT thay vì AVG).

### Reducer — Approach 2: `itertools.groupby` (more Pythonic)

```python
#!/usr/bin/env python3
from itertools import groupby
from operator import itemgetter
import sys

def read_mapper_output(file, separator='\t'):
    for line in file:
        yield line.rstrip().split(separator, 1)

def main(separator='\t'):
    data = read_mapper_output(sys.stdin, separator=separator)
    for current_word, group in groupby(data, itemgetter(0)):
        try:
            total_count = sum(int(count) for current_word, count in group)
            print("%s%s%d" % (current_word, separator, total_count))
        except ValueError:
            pass

if __name__ == "__main__":
    main()
```

> 🇻🇳 `itertools.groupby(data, itemgetter(0))` **tự động gom** các phần tử liên tiếp có cùng giá trị ở vị trí `itemgetter(0)` (key) lại thành từng nhóm — vì dữ liệu **đã được Hadoop sort theo key** trước khi tới Reducer, `groupby` hoạt động đúng y hệt logic gom nhóm bạn viết tay ở Approach 1, chỉ gọn hơn. Cả 2 cách cho **kết quả giống hệt nhau** — khác phong cách code, không khác thuật toán. Có thể dùng `groupby` để viết gọn lại Reducer AVG.

---

## 5. Miscellaneous — Compound (Chained) MapReduce Jobs

**Rule of thumb**: for complex data-processing problems, think about **adding more jobs**, rather than adding complexity to a single job.

**Example**: computing the mean of the maximum daily temperature per month, per station:
- **Job 1**: compute the max daily temperature per `(station, day)` key
- **Job 2**: take Job 1's output, compute the mean of those max values per `(station, month)` key

A library called **`ChainMapper`** supports developing chained MapReduce jobs (Java API — outside the scope of Hadoop Streaming used in this course, but useful to know conceptually).

> 🇻🇳 Bài toán 2 tầng (max rồi mới avg) không thể gộp vào 1 job duy nhất một cách tự nhiên — Reduce của job 1 (tính MAX theo ngày) phải hoàn tất **toàn bộ** trước khi job 2 mới có đủ dữ liệu đúng để tính AVG theo tháng. Đây là ví dụ thực tế cho nguyên tắc "thêm job, đừng thêm độ phức tạp vào 1 job" — hữu ích nếu Task 5 (thiết kế thuật toán) của Assignment cần một bài toán nhiều tầng.

---

## 6. Why can't Hadoop just have built-in map/reduce logic?

> 🇻🇳 Câu hỏi quan trọng đã thảo luận: logic map/reduce mang tính **nghiệp vụ** — khác nhau cho mỗi bài toán (WordCount, AVG, filter log ERROR...), nên không thể "đóng gói sẵn". Hadoop chỉ built-in được:
> - **Chữ ký hàm cố định** (`map(k,v) → list(k,v)`, `reduce(k, values) → list(k,v)`)
> - **Cơ chế gọi hàm đúng lúc, đúng node, đúng thứ tự dữ liệu**
>
> Còn **nội dung bên trong** 2 hàm đó bắt buộc là người dùng viết, vì chỉ người dùng biết bài toán của mình cần tính gì. Ẩn dụ: Hadoop = nhà bếp công nghiệp (băng chuyền, giám sát, backup đầu bếp tự động); bạn = người viết công thức món ăn. Nhà bếp không thể "built-in sẵn công thức" vì mỗi khách muốn món khác nhau — nhưng nhà bếp lo toàn bộ phần vận hành ở quy mô lớn, thứ khó hơn nhiều so với viết công thức.

### Hadoop ≠ HDFS — correcting a common mix-up

> 🇻🇳 HDFS **không phải** nền tảng chứa Hadoop — ngược lại, **Hadoop là tên gọi chung** cho một framework gồm 3 tầng, HDFS chỉ là một trong số đó:
>
> | Tầng | Vai trò | Thành phần |
> |---|---|---|
> | HDFS | Lưu trữ phân tán | NameNode, DataNode |
> | YARN | Quản lý tài nguyên | ResourceManager, NodeManager |
> | MapReduce | Mô hình lập trình xử lý | Mapper, Reducer, Driver |
>
> Khi `jps` liệt kê cả NameNode/DataNode (HDFS) lẫn ResourceManager/NodeManager (YARN) — đó là bằng chứng cả 2 hệ thống con cùng thuộc về "Hadoop", không phải Hadoop nằm bên trên HDFS.

---

## 7. Direct link to Assignment 1

| Task | Technique from this lecture |
|---|---|
| Task 3 (filter/WHERE) | Command syntax + subprocess/stdin-stdout mechanism from Section 3 |
| Task 4 (GROUP BY + AVG) | Reducer patterns from Section 4 (manual tracking or `groupby`), applied to SUM/COUNT accumulation from Lecture 5 |
| Both | Real command template in Section 3.4, reading real job output in Section 3.5 |

---

## 8. Self-Check Questions

1. What role does the Driver play, and who writes it when using Hadoop Streaming (vs. the Java API)?
2. Why does the number of HDFS blocks for a file determine the number of Mapper objects?
3. What are `setup()` and `cleanup()` in a Mapper used for?
4. Describe, step by step, how Hadoop Streaming runs a Mapper executable — what goes into stdin, what comes out of stdout, and how is the key/value split determined?
5. Why can Hadoop Streaming work with any programming language, not just Java or Python?
6. Why must the reducer script manually track a "current key" instead of relying on Hadoop to group values?
7. What does `-file` do, and why is it necessary when running on a real multi-node cluster?
8. What is `IdentityMapper`, and why doesn't Hadoop provide a more useful built-in map/reduce function?
9. Correct this statement: "Hadoop is a platform built on top of HDFS." What is actually true?
10. Compare the two WordCount reducer implementations (manual loop vs. `itertools.groupby`). Do they produce different results? What's different about them?
11. Give the rule of thumb for handling complex, multi-stage data processing problems in MapReduce, with the max-then-average temperature example.
12. Walk through what a real `hadoop jar ... streaming ...` command's terminal output shows, and where the final results end up on HDFS.
13. Does Hadoop provide a Python runtime/environment? What must already exist on every node for a Python-based Streaming job to work?
