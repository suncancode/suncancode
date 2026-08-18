# HDFS Interfaces

> English notes for long-term storage/exam revision. 🇻🇳 *Vietnamese callouts mark points that caused real confusion in our discussion — read those twice.*

---

## 1. Big Picture

HDFS provides **four different interfaces** to read, write, interrogate, and manage the filesystem:

1. `hadoop fs` / `hdfs dfs` — the **shell (CLI)** interface
2. Hadoop Filesystem **Java API**
3. Hadoop **Web User Interface**
4. **Snakebite** — a pure-Python HDFS client library

> 🇻🇳 Đây là 4 "cửa" khác nhau để chạm vào **cùng một** hệ thống file HDFS — không phải 4 hệ thống file riêng biệt. Task 1 dùng cửa số 1, Task 2 dùng cửa số 4.

---

## 2. Hadoop Cluster vs. Pseudo-Distributed Hadoop

| | Real Cluster | Pseudo-Distributed Mode |
|---|---|---|
| Deployment | Multiple physical nodes | A **single machine** |
| JVMs | Spread across nodes | All Hadoop-service JVMs run on **one** machine |
| Our setup | — | The course VM: Ubuntu 22.04 |

Because Hadoop is written in Java, every Hadoop service (NameNode, DataNode, ResourceManager, NodeManager...) is its own **JVM process**. In pseudo-distributed mode, all of these JVMs happen to run on the same physical/virtual machine — but they are still **separate processes**, behaving exactly as they would on a real multi-node cluster.

> 🇻🇳 Đây chính là lý do khi chạy `jps` trên VM của bạn (chỉ 1 máy), bạn vẫn thấy nhiều tiến trình riêng biệt (NameNode, DataNode, ResourceManager, NodeManager...) — mỗi cái là một JVM độc lập, "giả lập" đúng vai trò như trên cluster thật. Mọi lệnh, mọi API bạn học đều dùng **y hệt** trên cả 2 chế độ — chỉ khác về quy mô vật lý.

---

## 3. Shell Interface to HDFS

### 3.1 Starting Hadoop and checking processes

```bash
$ cd $HADOOP_HOME
$ ./sbin/start-all.sh
$ jps
```

Expected healthy output:
```
28530 SecondaryNameNode
11188 NodeManager
28133 NameNode
28311 DataNode
10845 ResourceManager
3542 Jps
```

These 5 processes map onto the two layers you learned in Lecture 3:
- **HDFS layer**: NameNode, SecondaryNameNode, DataNode
- **YARN layer**: ResourceManager, NodeManager

> 🇻🇳 Có một tiến trình thứ 6 chỉ xuất hiện **tạm thời**, không nằm trong danh sách checklist cố định này: **`MRAppMaster`**. Nó chỉ xuất hiện khi một MapReduce job đang thực sự chạy, và biến mất ngay khi job kết thúc. Nếu bạn chạy `jps` lúc "rảnh rỗi" (không có job nào), bạn sẽ không bao giờ thấy nó — đừng nhầm nó là một service phải luôn chạy như 5 process trên.

### 3.2 Core commands (used directly in Task 1)

```bash
$ bin/hdfs dfs -mkdir -p /user/bigdata   # create user home dir
$ hdfs dfs -mkdir input                  # relative path → /user/<username>/input
$ hdfs dfs -ls                           # list current home dir
$ hdfs dfs -ls /user/bigdata             # same result, absolute path
$ hdfs dfs -put README.txt input         # upload local file to HDFS
$ hdfs dfs -cat input/README.txt         # print file contents
$ hdfs dfs -help                         # full command list
```

> 🇻🇳 Quy ước quan trọng: đường dẫn **tương đối** (`input`, không có `/` đầu) luôn được hiểu là `/user/<username>/input`. Đây là lý do `hdfs dfs -ls` và `hdfs dfs -ls /user/bigdata` cho ra cùng kết quả.

### 3.3 Common command reference table

| Command | Description |
|---|---|
| `-put` | Upload a file (or files) from local filesystem to HDFS |
| `-mkdir` | Create a directory in HDFS |
| `-ls` | List the files in a directory in HDFS |
| `-cat` | Read the content of a file (or files) |
| `-copyFromLocal` | Copy a file from local filesystem to HDFS (like `-put`) |
| `-copyToLocal` | Copy a file (or files) from HDFS to local filesystem |
| `-rm` | Delete a file (or files) in HDFS |
| `-rm -r` | Delete a directory in HDFS (recursive) |

---

## 4. Web Interface to HDFS

A built-in web UI (typically on the NameNode's web port) shows:
- **Overview**: version, start time, Cluster ID, Block Pool ID
- **Summary**: security on/off, Safemode on/off, total files/directories/blocks, heap memory usage
- A **file browser** view: Permission, Owner, Group, Size, Last Modified, Replication, Block Size, Name

**Safemode** = a read-only startup state HDFS enters automatically to verify data integrity before allowing writes.

> 🇻🇳 Web UI hữu ích để kiểm tra nhanh trạng thái cluster (đặc biệt Safemode) mà không cần gõ lệnh — dùng để đối chiếu (double-check) với kết quả các lệnh shell khi làm Task 1.

---

## 5. Python Interface to HDFS — Snakebite

### 5.1 What it is

Snakebite is a Python package (created by **Spotify**) that lets you access HDFS **programmatically**. Unlike the shell interface, it talks **directly to the NameNode** using **Protocol Buffer** messages over RPC — it does not shell out to `hdfs dfs` commands.

> 🇻🇳 Điểm hay nhầm: Snakebite **không gọi lệnh shell bên dưới** — nó tự giao tiếp trực tiếp với NameNode qua giao thức RPC riêng của nó. Đây là lý do nó nhanh hơn khi nhúng vào ứng dụng Python.

### 5.2 Connecting and listing

```python
#!/usr/bin/env python3
from snakebite.client import Client
client = Client('localhost', 9000)
for x in client.ls(['/user']):
    print(x)
```

- `Client('localhost', 9000)` — connects to the NameNode's **RPC port** (9000 by default; different from the Web UI port).
- `client.ls([...])` — takes a **list of paths** (always wrap in `[...]`, even for one path) and returns a **generator of dicts**, one dict per file/directory:

```python
{'file_type': 'd', 'permission': 493, 'path': '/user/bigdata', 'length': 0,
 'owner': 'bigdata', 'group': 'supergroup', 'block_replication': 0,
 'modification_time': 1711847570566, 'access_time': 0, 'blocksize': 0}
```

`file_type`: `'d'` = directory, `'f'` = file.

### 5.3 Filtering and reading content

```python
# Extract just path + type
for x in client.ls(['/user/NOTICE.txt']):
    print(x['path'], x['file_type'])

# Copy a file from HDFS to local disk
for x in client.copyToLocal(['/user/NOTICE.txt'], '.'):
    print(x)   # {'path': '...', 'result': True, 'error': '', 'source_path': '...'}

# Read file content directly (returns bytes, nested generators)
for file in client.cat(['/user/NOTICE.txt']):
    for y in file:
        print(y)   # b"Apache Hadoop\n..."
```

> 🇻🇳 `cat()` trả về dữ liệu dạng `bytes` (có prefix `b"..."`), không phải `str` — nếu cần xử lý text (tách dòng, đếm từ cho Task 2/3/4), phải `.decode('utf-8')` trước.

### 5.4 The important combined pattern (list → filter → read)

```python
#!/usr/bin/env python3
from snakebite.client import Client
client = Client('localhost', 9000)
files = []
for x in client.ls(['/user/bigdata/NOTICE.txt']):
    if x['file_type'] == 'f':
        files.append(x['path'])
for cat in client.text(files):
    print(cat)
```

> 🇻🇳 Đây là khuôn mẫu tư duy quan trọng nhất của cả lecture cho Task 2: **liệt kê → lọc theo điều kiện → xử lý từng phần tử hợp lệ**. `client.text()` khác `client.cat()` ở chỗ nó trả về nội dung đã decode sẵn, dễ đọc hơn.

---

## 6. Internals of HDFS — Read/Write Pipeline

### Read pipeline
1. Client opens file → `DistributedFileSystem`
2. Contacts **NameNode** → gets **block locations** (metadata only)
3. Returns `FSDataInputStream`
4. Client reads data **directly from DataNodes** (block by block)
5. Closes stream

### Write pipeline
1. Client creates file → `DistributedFileSystem`
2. Contacts **NameNode** → creates file entry
3. Returns `FSDataOutputStream`
4. Client writes data as **packets**, forwarded through a **pipeline of DataNodes** (DN1 → DN2 → DN3, per replication factor)
5. Each DataNode sends an **ack packet** back down the pipeline
6. Stream closes → NameNode marks the file complete

> 🇻🇳 **Điểm dễ nhầm nhất:** NameNode **không** truyền dữ liệu thật — nó chỉ trả lời "block này ở DataNode nào" (giống danh bạ/metadata server). Dữ liệu thật đi **thẳng** giữa Client và DataNode, không qua NameNode → đây là lý do NameNode không bị nghẽn băng thông dù có hàng nghìn client đọc cùng lúc.
>
> **Cơ chế ghi (pipeline):** Client chỉ gửi dữ liệu **1 lần duy nhất** tới DataNode đầu tiên; DataNode đó tự "chuyền tay" (forward) sang DataNode thứ 2, rồi thứ 3 — không phải Client tự gửi 3 lần riêng biệt tới 3 bản sao. Ack đi ngược chiều dữ liệu.

---

## 7. Direct link to Assignment 1

| Task | Technique from this lecture |
|---|---|
| Task 1 (Shell HDFS) | Section 3: `-mkdir`, `-put`, `-ls`, `-cat` |
| Task 2 (Snakebite) | Section 5: `Client(...)`, `.ls()`, `.copyToLocal()`, `.cat()`/`.text()`, list→filter→read pattern |

---

## 8. Self-Check Questions

1. Name the four interfaces to HDFS. Which two are used in Assignment 1?
2. Distinguish a real Hadoop cluster from pseudo-distributed mode. Why does the pseudo-distributed VM still teach correct skills?
3. List the 5 daemon processes you should see in `jps` when Hadoop is healthy, and their layer (HDFS vs YARN). Why might a 6th process (`MRAppMaster`) sometimes appear, and when does it disappear?
4. Explain HDFS's home-directory convention with a relative path example.
5. List at least 6 shell HDFS commands and their function.
6. How does Snakebite communicate with HDFS? Does it call `hdfs dfs` under the hood?
7. What data type does `client.ls()` return per element? Name 5 fields.
8. Compare `client.cat()` and `client.text()`.
9. Write Snakebite code that lists files in `/user/bigdata`, filters only files, then prints each file's content.
10. In the HDFS read pipeline, why doesn't the NameNode become a bandwidth bottleneck?
11. In the write pipeline with replication=3, describe the pipelining mechanism — why does the client only send data once?
12. What is an `ack packet` for, and which direction does it travel relative to the data?
