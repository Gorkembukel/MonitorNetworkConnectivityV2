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
## How to Use<img width="1526" height="783" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient ping" src="https://github.com/user-attachments/assets/0cbfdf02-c086-41f2-8297-bb7049628668" />
<img width="1120" height="798" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient liveshell" src="https://github.com/user-attachments/assets/867a4b34-6cf5-4444-868f-d22544eb7e09" />
<img width="1709" height="812" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient iperfClient graph server" src="https://github.com/user-attachments/assets/cd7db84f-6b9a-430c-94c4-8c099eb2a800" />
<img width="1723" height="750" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient iperfClient graph" src="https://github.com/user-attachments/assets/78507474-2536-4dea-afd4-d90c2bbfffdf" />
<img width="1474" height="792" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient iperfClient" src="https://github.com/user-attachments/assets/fe142d8e-22a2-4aee-9eaa-8626a87d6fd4" />
<img width="1145" height="783" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient" src="https://github.com/user-attachments/assets/4a556d43-5e16-4a96-aab7-a0b9b599d060" />
<img width="1459" height="768" alt="nmc-ssh giriş  ssh account managment open connect summary widget" src="https://github.com/user-attachments/assets/81ef75a7-9c0a-4e86-a93a-3e9baafb127e" />
<img width="1363" height="797" alt="nmc-ssh giriş  ssh account managment open connect" src="https://github.com/user-attachments/assets/d4c3abfe-c6e6-4139-a7b6-56b1f9044bd9" />
<img width="1366" height="801" alt="nmc-ssh giriş  ssh account managment open" src="https://github.com/user-attachments/assets/2951d7d5-8e1c-43bc-9aaa-1d2e8d58b25b" />
<img width="1112" height="778" alt="nmc-ssh giriş" src="https://github.com/user-attachments/assets/663a357b-1a21-4236-8a2c-9246f74ff54c" />
<img width="1256" height="808" alt="nmc-ping-menu open add-pings start_all rightClick menu  open graph" src="https://github.com/user-attachments/assets/82e9d4cd-a38f-44af-8327-bbedd7dfef98" />
<img width="1836" height="1046" alt="nmc-ping-menu open add-pings start_all rightClick menu  graph reset zoom" src="https://github.com/user-attachments/assets/a518ad55-7baa-49e8-8de8-b9ec2b3a2674" />
<img width="1001" height="703" alt="nmc-ping-menu open add-pings start_all rightClick menu" src="https://github.com/user-attachments/assets/614382c8-09c9-4c4a-8d8d-84272eff39d6" />
<img width="1101" height="761" alt="nmc-ping-menu open add-pings start_all leftClick" src="https://github.com/user-attachments/assets/e74f1fcb-c9e9-46d0-b32b-2005cc5dfb2a" />
<img width="1105" height="789" alt="nmc-ping-menu open add-pings start_all" src="https://github.com/user-attachments/assets/2badea9c-f67f-471c-95d8-eed9d5402ea4" />
<img width="1110" height="773" alt="nmc-ping-menu open add-pings" src="https://github.com/user-attachments/assets/252010cf-a6b1-4a30-a16a-7b66272e9a0f" />
<img width="1104" height="778" alt="nmc-ping-menu open" src="https://github.com/user-attachments/assets/1975fdea-0455-41b8-8300-7a83da49b2d5" />
<img width="1113" height="785" alt="nmc-ping-menu" src="https://github.com/user-attachments/assets/11d521bd-b4ef-4abd-ba70-aec7e6166047" />
<img width="1827" height="1020" alt="nmc-iperf-menu add_iperfClient run grafik grafik içi" src="https://github.com/user-attachments/assets/04de6fdf-b92d-47d9-89e7-d3b853fa6197" />
<img width="1616" height="755" alt="nmc-iperf-menu add_iperfClient run grafik" src="https://github.com/user-attachments/assets/92e75bec-11b2-4c99-ad53-f7db18b54838" />
<img width="1096" height="771" alt="nmc-iperf-menu add_iperfClient run" src="https://github.com/user-attachments/assets/8a3f652e-9c90-4058-9cae-a96c0f4c2869" />
<img width="1129" height="778" alt="nmc-iperf-menu add_iperfClient" src="https://github.com/user-attachments/assets/52ada895-1930-414b-b5b8-bc285b9b3678" />
<img width="1113" height="773" alt="nmc-iperf-menu" src="https://github.com/user-attachments/assets/dcc68446-54e2-477b-9cf2-e657e696ad99" />

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

