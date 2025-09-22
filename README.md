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
     sudo ./TEST.run
     ```
   - <img width="1632" height="327" alt="distro" src="https://github.com/user-attachments/assets/71d4efdb-8d40-42df-bd99-d76e93671a74" />
   - <img width="475" height="269" alt="distro" src="https://github.com/user-attachments/assets/e3a92653-043e-4fa1-bdd3-f77600fe0a52" />

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
## How to Use

**Ping**
  - <img width="1113" height="785" alt="nmc-ping-menu" src="https://github.com/user-attachments/assets/c8c9f3ce-03e6-4702-b1cd-8a12b546e8b8" />
  - You can use Open Menu button to adding/deleting pings.
  - Application will save your last added pings if list is not empy while closing it self.
  - <img width="1104" height="778" alt="nmc-ping-menu open" src="https://github.com/user-attachments/assets/811beeaa-06a9-4a97-a9cb-7b9e0187bba5" />
  - You can add or delete ip's to ip section.For sending pings with out a time constrain you can use loop button. Change will applies to table at left side.
  - <img width="1110" height="773" alt="2-nmc-ping-menu open add-pings" src="https://github.com/user-attachments/assets/c2829491-47cf-42a1-b02d-53d40aeb1eeb" />  
  - <img width="1105" height="789" alt="nmc-ping-menu open add-pings start_all" src="https://github.com/user-attachments/assets/94f09c8b-4da8-484b-82e8-0c3502a76a57" />
  - Use start all button to start all.
  - <img width="1101" height="761" alt="nmc-ping-menu open add-pings start_all leftClick" src="https://github.com/user-attachments/assets/4d417917-2b26-45e8-9e77-e660d4b248b5" />
  - You can click with left and right mouse buttons to rows in table for acces to vital options
  - You can configur parameters without stoping sending pings
  - If you right click you can acces those options
  - <img width="1001" height="703" alt="nmc-ping-menu open add-pings start_all rightClick menu" src="https://github.com/user-attachments/assets/d1162c0f-37a0-4f59-9882-44d94a884bc3" />
  - The beep will only work if the terminal permits it to "\a".
  - <img width="1256" height="808" alt="nmc-ping-menu open add-pings start_all rightClick menu  open graph" src="https://github.com/user-attachments/assets/4026bf16-a835-4436-bd4a-2b8f05c4fe53" />
  - <img width="1836" height="1046" alt="nmc-ping-menu open add-pings start_all rightClick menu  graph reset zoom" src="https://github.com/user-attachments/assets/85e596e1-1c2e-4abd-ae16-ffaba0b987eb" />
  - You can use left click to zoom selected area or rigth click to changing scale.
## Iperf3
---
  - <img width="1113" height="773" alt="nmc-iperf-menu" src="https://github.com/user-attachments/assets/9922488f-a8d5-4812-a15e-2c5432b8e872" />
  - You can use toolbar CTRL + F or you can select iperf tab at the bottom and Open menu button.
---
  - <img width="1129" height="778" alt="nmc-iperf-menu add_iperfClient" src="https://github.com/user-attachments/assets/39a6aba4-e13d-4787-9cbf-b261eb3ea730" />
  - You can use iperf3 -c with this section. If you need to open iperf3 server at remote you can use ssh with this applicaton. More at this later
---
  - <img width="1096" height="771" alt="nmc-iperf-menu add_iperfClient run" src="https://github.com/user-attachments/assets/8857ed9e-1167-4e51-9778-60418897fa74" />
  -  First right click desired client's row, user can start iperf client individually or start all button
---
  - <img width="1616" height="755" alt="nmc-iperf-menu add_iperfClient run grafik" src="https://github.com/user-attachments/assets/04d841fa-56ef-4685-a4df-06c4740cb85a" />
  - You can use Grafik button to open graph window
---
  - <img width="1827" height="1020" alt="nmc-iperf-menu add_iperfClient run grafik grafik içi" src="https://github.com/user-attachments/assets/8571dcb8-8c99-440d-b587-5c9c0e3ea385" />
  -  At number one, you can see white dash lines, it implies packet sending start with there. If you use same client more than once, every attempt drawer white line.
  - Two and three are self explanatory
---
## SSH
  - <img width="1112" height="778" alt="nmc-ssh giriş" src="https://github.com/user-attachments/assets/b4a10ca5-36e9-415d-bd9f-04e334c06620" />
  - If you want to connect a ssh server just for one, you can use number two (CTRL + S). If other wise, Number one will (CTRL + M) open window that you can saves ip's for later.
---
  - <img width="1366" height="801" alt="nmc-ssh giriş  ssh account managment open" src="https://github.com/user-attachments/assets/243cff7c-eac2-41af-a394-2bbefe12e600" />
  - Ass you can see, saved ip's in config/ip_list.txt will shows up.
  - You can click open menu button for acces more option
  - You can delete existing ip or star a connection to ssh server with those parameters
---
  - <img width="1363" height="797" alt="nmc-ssh giriş  ssh account managment open connect" src="https://github.com/user-attachments/assets/e70a6230-c04a-4982-ab12-cd652ab357ec" />
  - If you want to see connected ssh server, you can click view, and made visible that area.
---
  - <img width="1459" height="768" alt="nmc-ssh giriş  ssh account managment open connect summary widget" src="https://github.com/user-attachments/assets/ad610d95-f6ce-4a46-b33b-8e19a058d858" />
  - Connected servers will be listed up like that
  - X is you know, More menu will you will learn
---
  - <img width="1145" height="783" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient" src="https://github.com/user-attachments/assets/9b32cd4b-5795-4863-862f-5ae5f28a8c43" />
  - More menu will open this window. With this, you can use iperf3,ping or live shell in remote ssh server
---
 - <img width="1474" height="792" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient iperfClient" src="https://github.com/user-attachments/assets/10e926e1-f7d8-41e3-9f09-6c28afc19aac" />
 - Iperf parameters lies like that. Client role and server role will open diffrent tabs for ssh servers terminal output.
---
 - <img width="1723" height="750" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient iperfClient graph" src="https://github.com/user-attachments/assets/0940909d-891a-43d1-aec8-a985a434dc10" />
 - If you create iperf client, it will looks like this, you can use Open graph button for that clients iperf data
---
  - <img width="1709" height="812" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient iperfClient graph server" src="https://github.com/user-attachments/assets/a25bfa08-ad16-496e-9200-2e58258f6b1f" />
  - Iperf server 
---
 - <img width="1120" height="798" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient liveshell" src="https://github.com/user-attachments/assets/e0c835d8-5125-4fcd-ba24-bcc05c43e102" />
 - First, open live shell, write your command at the bottom and send it. I don't recommend to use nano command with this.
---
  - <img width="1526" height="783" alt="nmc-ssh giriş  ssh account managment open connect summary widget sshclient ping" src="https://github.com/user-attachments/assets/491b73cc-fa1f-4e50-abd5-b66aad182c91" />
  
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

