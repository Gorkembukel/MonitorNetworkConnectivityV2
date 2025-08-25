
import subprocess

from source.Iperf.iperf_TestResult_Wrapper import TestResult_Wrapper_sub
from iperf3 import Client

valid_fields = {#Tablo buraya göre headerları çiziyor
            "server_hostname": "",
            "port" : "",
            "num_streams": "",
            "zerocopy": "",
            "omit": "",
            "duration": "",
            "bandwidth": "",
            "protocol": "",           
            
            "reversed": ""
        }
class Client_subproces():
    def __init__(self, testresultWrapper, **clientKwargs):
        super().__init__()
        
        self.clientKwargs = clientKwargs
        self.testresultWrapper = testresultWrapper
        self.proces = None
        #bu kısım geçici, tablonun burayı görmesi lazım ki arayüzde listelensin
        self.client = Client()
        for k, v in self.clientKwargs.items():
            if k in valid_fields:
                setattr(self.client, k, v)
            else:
                print(f"⚠️  Uyarı: iperf3.Client '{k}' parametresini tanımıyor, atlandı.")


        self.server_hostname = self.clientKwargs.get("server_hostname")
        self.port = self.clientKwargs.get("port")
        self.num_streams = self.clientKwargs.get("num_streams")
        self.zerocopy = self.clientKwargs.get("zerocopy")
        self.omit = self.clientKwargs.get("omit")
        self.duration = self.clientKwargs.get("duration")
        self.bandwidth = self.clientKwargs.get("bandwidth")
        self.protocol = self.clientKwargs.get("protocol")
        self.blksize = self.clientKwargs.get("blksize")
        self.bind_address = self.clientKwargs.get("bind_address")
        self.reversed = self.clientKwargs.get("reversed")
        
       


    def start_iperf(self):
        # Başlangıç komutu
        cmd = ["iperf3", "-c", self.clientKwargs.get("server_hostname")]

        # Optional parametreler
        if self.clientKwargs.get("port"):
            cmd += ["-p", str(self.clientKwargs["port"])]
        if self.clientKwargs.get("num_streams"):
            cmd += ["-P", str(self.clientKwargs["num_streams"])]
        if self.clientKwargs.get("zerocopy"):
            cmd += ["--zerocopy"]
        if self.clientKwargs.get("omit"):
            cmd += ["--omit", str(self.clientKwargs["omit"])]
        if self.clientKwargs.get("duration"):
            cmd += ["-t", str(self.clientKwargs["duration"])]
        if self.clientKwargs.get("bandwidth"):
            cmd += ["-b", f"{self.clientKwargs['bandwidth']}K"]
        if self.clientKwargs.get("protocol") == "UDP":
            cmd += ["-u"]
        if self.clientKwargs.get("blksize"):
            cmd += ["-l", str(self.clientKwargs["blksize"])]

        if self.clientKwargs.get("reversed"):
            if self.clientKwargs["reversed"]:
                cmd += ["-R"]
       

        # Force flush output
        cmd += ["-V"]# detailed info
        cmd += ["--forceflush"]

        # Komutu yazdırmak istersen (debug için)
        print("Running command:", " ".join(cmd))

        # subprocess başlat 
        self.proces = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        self.testresultWrapper.set_subproces(self.proces)
        return self
    
    def is_running(self):
        if not self.proces:
            return False

        poll = self.proces.poll()
        if poll is None:
            return True 
    def stop_iperf(self):
        if self.proces and self.is_running():
            print(f"Stopping iperf3 process for {self.server_hostname}")
            self.proces.terminate()  # Sürece SIGTERM gönderir
            try:
                self.proces.wait(timeout=5)  # 5 sn içinde kapanmazsa
            except subprocess.TimeoutExpired:
                print("Process did not exit, killing it forcefully.")
                self.proces.kill()  # SIGKILL ile zorla kapatır
            self.proces = None
        else:
            print("No running iperf3 process to stop.")
    def _del__(self):
        print(f"[🗑 Siliniyor:Client_Subproces] {self.clientKwargs.get('server_hostname')}")