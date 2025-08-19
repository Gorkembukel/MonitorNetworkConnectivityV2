

from typing import Dict, Optional


#projenin kendi modülleri

from source.Iperf.iperf_Client_Wraper import Client_Wrapper
from source.Iperf.subproces_for_iperf import Client_subproces 
from source.Iperf.iperf_TestResult_Wrapper import TestResult_Wrapper_sub

class SingletonMeta(type):# pingcontrollerı sinfleton yapmak için
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
    

class Iperf_controller(metaclass=SingletonMeta):
    def __init__(self):
        self.clientSubproceses: Dict[str, Client_subproces] = {}  # key = address, value = clientSubproces    
        self.testResults: Dict[str, TestResult_Wrapper_sub] = {}# FIXME normalde liste burası


    
    
    def start(self, hostname: str) -> None:
        """Tek bir client’ı başlatır (zaten çalışıyorsa pas geçer)."""
        
        client_sub = self.clientSubproceses.get(hostname)
        if client_sub is None:
            raise KeyError(f"Böyle bir key yok: '{hostname}'")

        if client_sub.is_running():
            print(f"ℹ️  Zaten çalışıyor: {hostname}")
            return

        # Başlat
        client_sub.start_iperf()

    def add(self, *, hostName:str, overwrite: bool = False,**clientKwargs) -> str:
        """
        Yeni bir Client_subproces ekler.
        key verilmezse 'host[:port]' oluşturulur.
        overwrite=False iken aynı key varsa hata atar.
        Dönüş: kullanılan key (string)
        """
        
        
        if (not overwrite) and (hostName in self.clientSubproceses):#aynısı var mı, overwrite edilsin mi
            raise KeyError(f"Aynı key zaten mevcut: '{hostName}'")
        
        testResultWrapper =  TestResult_Wrapper_sub(hostName=hostName) #test result burada oluşturulur clientSubprocese aktarılır
        self.testResults[hostName] = testResultWrapper 

        client_sub = Client_Wrapper.build_client_kwargs(testResultWrapper=testResultWrapper,**clientKwargs)
        self.clientSubproceses[hostName] = client_sub
        return client_sub
    def get_testResultWrapper(self,hostname):        
        testResult = self.testResults[hostname]
        if testResult:
            return testResult
        else:
            raise 

    def delete_client(self,hostname):        
        # hostname key'ini kaldır
        
        self.testResults.pop(hostname, None)
        self.clientSubproceses.pop(hostname, None)

    
