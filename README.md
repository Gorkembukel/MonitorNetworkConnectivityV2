# MNCv2 – Network Measurement and Control v2

MNCv2 is a **network measurement and management tool** that integrates **Ping**, **iPerf3**, and **SSH** functionalities into a single **PyQt5-based graphical user interface**.  
It allows local and remote network testing, visualization, and client management.

---

## 🚀 Features

- **Ping Module**
  - Local ping measurements with detailed RTT, jitter, and packet loss statistics.
  - Live plotting of results using PyQtGraph.
  - Per-target statistics management (min/max/avg RTT, consecutive failures, etc.).

- **iPerf Module**
  - Bandwidth measurement using iPerf3.
  - Support for client/server mode, TCP/UDP, multiple streams, reverse mode, etc.
  - Live bitrate graph per stream.

- **SSH Module**
  - Remote execution of ping and iPerf tests.
  - OS-aware command generation using Strategy Pattern (Linux/Windows).
  - Paramiko-based secure SSH connections with multi-stream output management.

- **GUI**
  - Main window for managing Ping, iPerf, and SSH clients.
  - Real-time tables and graph windows for network tests.
  - Persistent storage of IP lists for quick re-use.



## 🛠️ Build Instructions

To build the project, run the provided `setup.sh` script:


    
     chmod +x setup.sh
     ./setup.sh
     

./setup.sh
This script will:
- Create a local virtual environment (.venv/)
- Install all required dependencies listed in requirements.txt
- Install PyInstaller (for packaging)
- Generate an executable build of the entire project

## ▶️ Running the Application

After building, you can run the application in one of two ways:

1. **Executable File**
   - Navigate to the `dist/` folder.
   - Run the generated executable:(you need to run this in sudo) 
     ```bash
     ./TEST.run
     ```

2. **Start Script (With Terminal Open)  (Recommended)**
   - From the main project directory, run:  
     ```bash
     chmod +x start.sh
     ./start.sh
     ```
    **ShortCuts**
   - CTRL + A for ping menu
   - CTRL + F for iper menu
   - CTRL + S for ssh login
   
---

## 📌 Notes

- When running the program using **`TEST.run`** (from the `dist/` folder), the application will create an `ip.txt` file **next to the `TEST.run` executable** to store your added ping targets.  
- When running the program using **`start.sh`** (from the project’s root directory), the `ip.txt` file will be created in the **main project folder**.  
- The `ip.txt` file is used to save and reload previously entered IP addresses automatically on startup.


---

## 🎨 UI Modifications

Most of the windows in this project were designed using **Qt Designer**.  
If you want to modify the interface elements:

1. Open the `.ui` files located in the **`QTDesigns/`** folder with the Qt Designer tool.
2. Apply your changes and save the `.ui` file.
3. Convert the updated `.ui` file into a Python file using the `pyuic5` command, for example:  
   ```bash
   pyuic5 -o output_file.py input_file.ui
 4. **(Recomenmded)** If you don’t want to handle this manually, you can use the **pyuic5-o.sh** script located in the project root directory.
 This script automatically scans the QTDesigns/ folder and converts all .ui files into their corresponding .py files.


---

## 🧩 Ping Controller Overview
<img width="2853" height="864" alt="classes_Ping" src="https://github.com/user-attachments/assets/bb7e2746-4617-4fda-b8ee-24fdfbadbc5b" />

The **PingController** class acts as the main bridge between the GUI and the ping logic.  
It manages multiple `PingThread` instances through `PingTask` objects and keeps track of them using dictionaries:

- **`tasks`**: A dictionary where each key is an IP address and each value is the corresponding `PingTask` object.  
- **`stat_list`**: A dictionary where each key is an IP address and each value is a `PingStats` object holding statistics such as RTT, packet loss, jitter, and failures.  

The GUI’s **Ping TableWidget** is populated dynamically by scanning the `stat_list` dictionary and displaying the statistics for each IP address.



## 📊 PingStats Class – Role and Data Flow

### 🔹 1. Purpose and Importance

The **PingStats** class is the central component for handling ping results.  
It is responsible for storing, analyzing, and preparing data for both tables and graphs.

- Keeps track of **RTT values**, **packet loss**, **consecutive failures**, **min/avg/max RTT**, and **jitter**.  
- Prepares **cached plot data** (`x`, `y`, brushes, pens) for efficient real-time graph updates.  
- Provides **summary dictionaries** for quick GUI table population.  
- In addition to statistical data, the **graph data** displayed in `GraphWindow (Ping_Graph.py)` is also **calculated and cached directly inside PingStats**.  
  - ✅ This means that PingStats is not only a statistics holder but also the main provider of **optimized graph-ready data**.  
- If **graph rendering performance optimizations** are required, both the `GraphWindow (Ping_Graph.py)` and the `PingStats` class should be considered together, since they work hand-in-hand.

**In short:**
- **PingThread** → generates raw ping results.  
- **PingStats** → processes, stores, and summarizes results + prepares cached graph data.  
- **GUI (Ping Table  (in MainMenu) & Graph)** → reads directly from PingStats for both statistics and real-time plotting.  


### 🔹 2. Where It Is Created
`PingStats` objects are created inside the **PingTask** class:  

```python
class PingTask:
    def __init__(..., address: str, ...):
        self.stats = PingStats(address)   # ✅ created here
        stat_list[self.address] = self.stats
```
## 🧩 iPerf Controller Overview
<img width="3678" height="544" alt="classes_iperf" src="https://github.com/user-attachments/assets/6500608b-3ef8-4189-8ded-c4ee845eb9c4" />

The **Iperf_controller** class acts as the main bridge between the GUI and the iPerf testing logic.  
It manages multiple iPerf client processes through `Client_subproces` objects and associates their results with `TestResult_Wrapper_sub` objects.  

It keeps track of them using dictionaries:

- **clientSubproceses**:  
  A dictionary where each key is a hostname (target server) and each value is a `Client_subproces` object.  
  - Each `Client_subproces` represents a running iPerf3 client process, started via `subprocess.Popen`.  

- **testResults**:  
  A dictionary where each key is a hostname and each value is a `TestResult_Wrapper_sub` object.  
  - These objects parse the raw iPerf3 output, extract **per-stream bitrate, interval, and CPU usage statistics**, and store them for the GUI.  

The GUI’s **iPerf TableWidget** is populated dynamically by scanning the `testResults` dictionary and displaying statistics for each active iPerf client.  

---
`
## 📊 TestResult_Wrapper_sub Class – Role and Data Flow  

### 🔹 1. Purpose and Importance
The **TestResult_Wrapper_sub** class is the central component for handling iPerf3 results.  
It is responsible for collecting, parsing, and preparing test results for both tables and graphs.  

- Tracks **streams**, each containing bitrate, transfer size, retransmits, cwnd, and optional CPU usage.  
- Uses compiled **regex patterns** to parse iPerf3 stdout in real time.  
- Stores **connection information** (local/remote IPs, ports).  
- Prepares **graph data** for the iPerf Graph window (`GraphWindow_iperf`).  
- Works in tandem with a background **thread** to continuously process new iPerf3 output lines.  

✅ This means that `TestResult_Wrapper_sub` is not only a statistics holder but also the main provider of **optimized graph-ready data** for iPerf tests.  

If graph rendering performance optimizations are required, both the `GraphWindow_iperf` and the `TestResult_Wrapper_sub` class should be considered together, since they work hand-in-hand.  

**In short:**  
- **Client_subproces** → runs iPerf3 as a subprocess and produces raw stdout/stderr.  
- **TestResult_Wrapper_sub** → parses, stores, and summarizes results + prepares graph data.  
- **GUI (iPerf Table & Graph)** → reads directly from `TestResult_Wrapper_sub` for both statistics and real-time plotting.  

---

### 🔹 2. Where It Is Created
`TestResult_Wrapper_sub` objects are created inside the **Iperf_controller.add()** method:  

```python
def add(self, *, hostName:str, overwrite: bool = False, **clientKwargs) -> str:
    testResultWrapper = TestResult_Wrapper_sub(hostName=hostName)   # ✅ created here
    self.testResults[hostName] = testResultWrapper
    client_sub = Client_Wrapper.build_client_kwargs(testResultWrapper=testResultWrapper, **clientKwargs)
    self.clientSubproceses[hostName] = client_sub
    return client_sub

```
## 🧩 SSH Controller Overview
<img width="3221" height="505" alt="classes_SSH" src="https://github.com/user-attachments/assets/0a09518b-4688-47e2-965a-c9db292cca6b" />

The **Client_Controller** class acts as the main bridge between the GUI and remote SSH clients.  
It manages multiple **ClientWrapper** objects, each representing one remote host, and keeps track of them in a dictionary:

- **_clients**:  
  A dictionary where each key is a hostname and each value is a `ClientWrapper`.  
  Each wrapper contains its own `paramiko`-based `Client` object and an `STD_object` for managing command I/O.  

The GUI’s **SSH Client Window** allows adding/removing remote hosts.  
Each new SSH connection spawns a corresponding `ClientWrapper`, which is displayed inside the GUI as a client widget.  

---

📊 ClientWrapper Class – Role and Data Flow  

### 🔹 1. Purpose and Importance
The **ClientWrapper** class represents a single remote SSH client.  
It is responsible for:  

- Establishing the **SSH connection** (via paramiko).  
- Running remote commands (`ping`, `iperf3`, or custom).  
- Wrapping input/output streams in `STD_object` so results can be handled in real time.  
- Detecting the remote **Operating System** and switching strategies (Linux vs Windows).  

✅ This makes `ClientWrapper` the key abstraction that hides OS differences and exposes a unified interface to the rest of the system.  

- **`paramiko_Client.py`**  
  Paramiko-based SSH client: connect, execute command (`exec_command`), SFTP, shutdown.  
  > Note: `execute_command(..., get_pty=True)` is enabled by default since it triggers **line-based flushing** for streaming outputs (e.g., iperf/ping), which is useful.

- **`osStragey.py`**  
  Uses the **Strategy Pattern** to generate commands depending on the OS.  
  - `Linux.setIperf3()`, `Windows.setIperf3()`  
  - `Linux.setPing()`, `Windows.setPing()`  
  Single interface: `CommandExecutor.comand_Iperf3(...)` and `CommandExecutor.command_Ping(...)`.

- **`std_control.py`**  
  Reads remote command **stdout/stderr** channels with separate **Reader** threads in a **non-blocking** way, writing to both **StringIO buffers** and emitting **Qt signals** in real time.  
  - Signals:  
    - `stdout_chunk(stream_name, chunk)`  
    - `stderr_chunk(stream_name, chunk)`  
    - `stdout_to_PingStat(clientWrapper, target, chunk)` *(ping-specific — currently optional/example)*

- **`Client_Controller.py`**  
  Manages multiple hosts (Singleton). Inside `ClientWrapper`:  
  - `Client` (SSH)  
  - `CommandExecutor` (Linux/Windows strategy)  
  - `STD_object` (stream handling)  
  Helpers:  
  - `open_iperf3(...)` → starts iperf, returns `STD_object`, registers the stream as `iperf`, starts the reader.  
  - `ping_on_remote(...)` → starts ping, registers the stream as `ping`, starts the reader.

- **`GUI_graph_iperf.py`**  
  `GraphWindow_iperf` window updates the **parsed** iperf stream data in `TestResult_Wrapper_sub` every **1 second**, rendering it on the graph and UI fields.

---

### 🔹 2. Where It Is Created
`ClientWrapper` objects are created inside the **Client_Controller.add_client()** method:  

```python
def add_client(self, hostname: str, username: str, password: str, port: int = 22, osType: str = "linux") -> None:
    self._clients[hostname] = ClientWrapper(hostname, username, password, port, osType=osType)   # ✅ created here

