


import ipaddress
import socket
from source.ping.PingThread import PingThread
from source.ping.PingStatistic import PingStats
from typing import Dict


def is_valid_ip(ip_str: str) -> bool:
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        pass
    try:
        socket.gethostbyname(ip_str)
        return True
    except socket.error:
        return False

def filter_kwargs_for_PingThread(kwargs: dict) -> dict:
    VALID_KWARGS = {
        "payload",
        "payload_size",
        "ttl",
        "traffic_class",
        "count",
        "interval",
        "timeout",
        "id",
        "source",
        "family",
        "privileged",        
        "isInfinte"
    }

    filtered = {}
    for k, v in kwargs.items():
        if k in VALID_KWARGS:
            filtered[k] = v
        else:
            print(f"⚠️ '{k}' geçersiz ping parametresi, atlandı.")
    return filtered

class PingTask:
    def __init__(self ,stat_list:Dict,address: str, duration: int, interval_ms: int, isInfinite: bool,isKill_Mod =False, **kwargs ):
        print(f"[Ping TASK için]  oluşturuldu")
        self.isKill_Mod = isKill_Mod
        self.address = address
        self.duration = duration
        self.interval_ms = interval_ms
        self.isInfinite = isInfinite
        self.stats = PingStats(address)

        self.kwargs = kwargs

        stat_list[self.address] = self.stats

        self.thread = None  # PingThread bu

    def start(self):#isKill_Mod=self.isKill_Mod behivor için
        self.thread = PingThread(address= self.address,duration= self.duration,interval_ms= self.interval_ms,stats= self.stats, isInfinite=self.isInfinite,**self.kwargs)
        
        self.thread.start()
        
    def stop(self,**kargs):
        print("stop_address kargs:", kargs)#FIXME geçici
        if self.thread:
            self.thread.stop(**kargs)
    def is_alive(self):
        return self.thread.is_alive() if self.thread else False

    def summary(self):
        return self.stats.summary()
    def toggleBeep(self):
        self.thread.toggleBeep()# burada thread thead değil behivor adlı bi class olabilir
    def wait(self):
        if self.thread:
            self.thread.join()
    
    def update_thread_parameters(self):
        if self.thread:
            self.thread.update_parameters(
                interval_ms=self.interval_ms,
                isInfinite=self.isInfinite,
                duration=self.duration,
                **self.kwargs
            )
    def join(self):
        if self.thread:
            self.thread.join()






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

class PingController(metaclass=SingletonMeta):
    
    def __init__(self):
        print(f"[PingController init]  deneme")#BUG test için
        self.tasks: Dict[str, PingTask] = {}  # key = address, value = PingTask
        self.address_dict = {}#her ip key olup istenen çalışma parametreleri value olacak
        self.stats_list: Dict[str, PingStats] = {}# FIXME normalde liste burası
        
    def add_task(self, address: str,isInfinite: bool, duration: int ,interval_ms: int,isKill_Mod = False, **kwargs  ):
        if not is_valid_ip(address):
            print(f"🚫 Invalid address skipped: {address}")
            return False  
    

        if address in self.tasks:#TODO bu kaldırılabilir belki
            print(f"⚠️ address already exists: {address}")
            return False

        task = PingTask(address=address,stat_list= self.stats_list, duration=duration,interval_ms= interval_ms, isKill_Mod=isKill_Mod,isInfinite=isInfinite,**kwargs )
        self.tasks[address] = task
        return True
    def address_dict_to_add_task(self):
        for address, config in self.address_dict.items():
            kwargs = config.get('kwargs', {})  # kwargs'ı al
            self.add_task(
                address=address,
                duration=config['duration'],
                interval_ms=config['interval_ms'],
                isKill_Mod=config['isKill_Mod'],
                isInfinite=config['isInfinite'],
                **kwargs  # kwargs'ı geçir
            )


    def add_addressList(self, addresses: list, interval_ms: int, duration: int, isInfinite: bool,isKill_Mod = False, **kwargs):
        filteredKwarg = filter_kwargs_for_PingThread(kwargs=kwargs)
        for address in addresses:
            self.address_dict[address] = {
                'interval_ms': interval_ms,
                'duration': duration,                
                'isInfinite': isInfinite,
                'isKill_Mod': isKill_Mod,
                'kwargs': filteredKwarg  
            }
        self.address_dict_to_add_task()


    def start_all(self):
        for task in self.tasks.values():
            if not task.is_alive():
                task.start()

    def wait_for_all(self):
        for task in self.tasks.values():
            task.wait()

    def get_active_count(self):
        return sum(task.is_alive() for task in self.tasks.values())

    """def get_stats_map(self):
        return {address: task.stats for address, task in self.tasks.items()}"""

    def get_task(self, address):
        return self.tasks.get(address)

    def add_and_start(self, address: str, duration: int = 10, interval_ms: int = 1000):
        if self.task(address, duration, interval_ms):
            self.tasks[address].start()

    def find_all_stats(self): #FIXME adı gui kodunda ve vurada değişmeli
       
        return self.stats_list

    
    def delete_stats(self, address):

        if address in self.stats_list:
            self.stop_address(address=address,isKill=True)
            del self.stats_list[address]
            del self.tasks[address]
            del self.address_dict[address]
    def show_all_updated(self):        
        self.find_all_stats()          
    
        for stat in self.stats_list:#FIXME keyvalu lara dikkat eğer hala dictonary ise stat_list
            stat.all_graph(True)
    def stop_address(self, address: str = "", **kargs):

        if address in self.tasks:
            self.tasks[address].stop(**kargs)
        else:
            print(f"PingThreadController Stop_address metodu__Adres bulunamadı: {address}")

    def stop_All(self):
        for task in self.tasks.values():  #  sadece value'larla ilgileniyoruz
            task.stop(isKill=True)
            task.join()

    def toggleBeep_by_address(self, address:str):
        task = self.get_task(address=address)
        task.toggleBeep()
    def is_alive_ping(self,address:str):
        task = self.get_task(address=address)
        return task.is_alive()
    def start_task(self,address:str):
        task = self.get_task(address=address)
        if not task.thread:
            task.start()
        else:
            print(f"{task} zaten başlatılmış")
    def restart_task(self,address:str):
        task = self.get_task(address=address)
        if task.thread:
            task.thread = None            
            task.stats = PingStats(task.address)
            self.stats_list[address] = task.stats
            task.start()
            
        else:
            print(f"{task} başlatılmamış")