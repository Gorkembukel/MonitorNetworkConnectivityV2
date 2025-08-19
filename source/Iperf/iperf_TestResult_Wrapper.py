from dataclasses import dataclass
import io
from subprocess import Popen
import threading
import time
from typing import List
import iperf3,re

from iperf3 import TestResult

from PyQt5.QtCore import QObject, pyqtSignal,pyqtSlot


class TestResult_Wrapper(QObject):
    update_table_for_result_signal = pyqtSignal(object)
    def __init__(self, hostName ):
        super().__init__()
        
        

        
        self.hostName = hostName

        self.TestResult:TestResult = None


    def setResult(self,result:TestResult):
        self.TestResult = result
        self.update_table_for_result_signal.emit(self)






@dataclass
class StreamInfo:
    id: str = None
    interval: str = None
    transfer: str = None
    bitrate: str = None
    retr: str = None
    cwnd: str = None
    stream_type: str = None
    omitted: bool = False

    local_cpu_percent: str = None
    local_cpu_user_sys: str = None
    remote_cpu_percent: str = None
    remote_cpu_user_sys: str = None

    
class TestResult_Wrapper_sub(QObject):
    update_table_for_result_signal = pyqtSignal(object)
    def __init__(self, hostName ):
        super().__init__()
        
        self.streams: List[StreamInfo] = []
        self.hostName = hostName
        self.Client_subproces:Popen = None

        self._stop = threading.Event()


        self.stdout = None
        self.stderr = None

        self.local_ip = None
        self.local_port =None
        self.remote_ip = None
        self.remote_port = None

        #regez birkez komplie edilir
          # ---- REGEX KALIPLARI ----
        # [  5]  10.00-10.04 sec   135 MBytes  26.6 Gbits/sec   0   123 KBytes  (örnek)
        self.interval_re = re.compile(
            r'\[\s*(\d+)\s*\]\s+'                      # stream id
            r'(\d+(?:\.\d+)?-\d+(?:\.\d+)?\s+sec)\s+'  # "10.00-10.04 sec"
            r'([\d\.]+\s+[KMG]?Bytes)\s+'              # "135 MBytes"
            r'([\d\.]+\s+[KMG]?bits/sec)'              # "26.6 Gbits/sec"
            r'(?:\s+(\d+))?'                           # opsiyonel "retr"
            r'(?:\s+([\d\.]+\s+\w+Bytes))?'            # opsiyonel "cwnd" vb.
        )

        # CPU Utilization: local/sender 2.0% (1.0%u/1.0%s), remote/receiver 3.0% (2.0%u/1.0%s)
        self.cpu_re = re.compile(
            r'CPU Utilization:\s*local/sender\s*([\d\.]+%)\s*\(([^)]+)\),\s*'
            r'remote/receiver\s*([\d\.]+%)\s*\(([^)]+)\)'
        )

        # local 192.168.1.2 port 12345 connected to 192.168.1.10 port 5201
        self.connection_re = re.compile(
            r'local\s+([\d\.]+)\s+port\s+(\d+)\s+connected\s+to\s+([\d\.]+)\s+port\s+(\d+)'
        )
    def set_subproces(self,popen:Popen):# Client_subproces bu metot ile popen'i buraya aktarır
        self.Client_subproces = popen
        t = threading.Thread(target=self.task)#BUG
        t.start()
    def set_std_outERR(self,stdout:io.StringIO,stderr):# Client_subproces bu metot ile popen'i buraya aktarır
        self.stdout = stdout
        self.stderr = stderr
        t = threading.Thread(target=self.task_withStdoutErr)#BUG thread hep açık kalıyor olabilir
        t.start()
        
    
    def task_withStdoutErr(self):  # ssh bunu kullanıyor #BUG metot içindeki while hiç kapanmıyor
        pos = 0
        while not self._stop.is_set():
            buf = self.stdout.getvalue()
            if len(buf) > pos:
                chunk = buf[pos:]
                pos = len(buf)
                for line in chunk.splitlines():
                    print(f"buradayız >>> {line}")
                    self.parse_iperf3_line(line)
    
            time.sleep(0.5)
    def start(self):
        self._stop.clear()
    def stop(self):
        """Dışarıdan çağrıldığında döngüyü kırar"""
        print(f"[iperf_testresult_wrapper_sub    stop içi]    döngü durduruldu")
        self._stop.set()
    def task(self):#iperf bunu kullanıyor
        for line in self.Client_subproces.stdout:
            self.parse_iperf3_line(line)
    
    def parse_iperf3_line(self, line: str):
        line = line.strip()
        if not line:
            return
        # CPU bilgisi
        cpu_match = self.cpu_re.search(line)
        if cpu_match and self.streams:
            last = self.streams[-1]
            last.local_cpu_percent   = cpu_match.group(1)
            last.local_cpu_user_sys  = f"({cpu_match.group(2)})"
            last.remote_cpu_percent  = cpu_match.group(3)
            last.remote_cpu_user_sys = f"({cpu_match.group(4)})"
            return

        # bağlantı bilgisi
        conn_match = re.search(r"local ([\d\.]+) port (\d+) connected to ([\d\.]+) port (\d+)", line)
        if conn_match:
            self.local_ip   = conn_match.group(1)
            self.local_port = conn_match.group(2)
            self.remote_ip  = conn_match.group(3)
            self.remote_port= conn_match.group(4)
            return

        omitted = '(omitted)' in line
        clean = line.replace('(omitted)', '').replace('sender', '').replace('receiver', '').strip()

        m = self.interval_re.search(clean)
        if not m:
            return

        stream = StreamInfo(
            id=m.group(1),
            interval=m.group(2),
            transfer=m.group(3),
            bitrate=m.group(4),
            retr=m.group(5) or '',
            cwnd=m.group(6) or '',
            stream_type=('sender' if 'sender' in line else 'receiver' if 'receiver' in line else None),
            omitted=omitted
        )
        self.streams.append(stream)
        # debug:
        self.print_stream(stream)
        


    def print_all_stream(self):
        for stream in self.streams:
            self.print_stream(stream=stream)
    def print_stream(self, stream: StreamInfo):
        print("---- Yeni Stream Bilgisi ----")
        print(f"ID        : {stream.id}")
        print(f"Interval  : {stream.interval}")
        print(f"Transfer  : {stream.transfer}")
        print(f"Bitrate   : {stream.bitrate}")
        print(f"Retr      : {stream.retr}")
        print(f"CWND      : {stream.cwnd}")
        print(f"Stream    : {stream.stream_type}")
        print(f"Omitted   : {stream.omitted}")
        print(f"local cpu   : {stream.local_cpu_percent}")
        print(f"remote  cpu   : {stream.remote_cpu_percent}")
        print("-----------------------------\n")
    def __del__(self):
        print(f"❌ TestResult_Wrapper_sub siliniyor: {self.hostName}")