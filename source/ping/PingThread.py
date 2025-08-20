# ping_thread.py


import time
import threading
from datetime import datetime
from icmplib import ping as icmp_ping

class PingThread(threading.Thread):
    

    def __init__(self, address, stats,duration,isInfinite =False ,end_datetime = None,count=1, interval_ms=100, timeout=1000, id=None, source=None,
        family=None, privileged=True, **kwargs):
        super().__init__()
        self._stop_event = threading.Event()

        self.address = address
        self.stats = stats
        self.duration = duration
        self.isInfinite = isInfinite
        self.end_datetime = end_datetime
        self.count = count
        self.interval_ms = interval_ms / 1000
        self.timeout = timeout 
        self.id = id
        self.source = source
        self.startTime = time.time()
        self.stop_time = self.startTime + duration if duration else None
        self.family = family
        self.privileged = privileged
        self.kwargs = kwargs
        self.isBeep = False
        self._pause_start_time = 0
        stats.setAddress(address)

        self.stats.set_timeout(self.timeout)
        self.isKill=False #threadi komple kapatır
    def _should_continue(self):#FIXME burada is kill tanımlı o yüzden diğer yerlerden kadlırabiliriz gibi
        
        if self.isKill:
            return False

        now = datetime.now()
        
        # Öncelik: end_datetime varsa ve geçilmişse dur
        if self.end_datetime:  # 🔴 Bitiş zamanı varsa onu esas al
            return now < self.end_datetime
        
        if self.isInfinite:
            return True

        return time.time() < self.stop_time  # duration süresi dolmadıysa devam

    def run(self):
        
        while not self.isKill:#TODO bu while hep dönecek, kill komutu gelene kadar threadi uykuda tutacak
            while self._should_continue() and not self._stop_event.is_set():#TODO burada sürekli metot çağırılıyor performans için değiştirilebilir
                # icmplib yöntemi
                try:
                    send_time = time.time()
                    
                    result = icmp_ping(address=self.address, count=self.count,interval=self.interval_ms, timeout=self.timeout/1000, id=self.id, source=self.source,
            family=self.family, privileged=self.privileged, **self.kwargs)
                    if result.is_alive:
                        #rtt = result.avg_rtt
                        
                        rtt = result.avg_rtt 
                        
                        self.stats.add_result(rtt, time.time() + 10800, payloadSize = self.kwargs["payload_size"] +42) #    istanbula göre UTC 3.    +42 header için
                        
                        #ses için
           
                        if self.isBeep:
                            print('\a')
                        
                    else:
                        self.stats.add_result(None, time.time() + 10800) #timeout burada saniyeden ms'ye çevirilir
                        
                    
                except Exception as e:
                    
                    self.stats.add_result(None, time.time() + 10800)
                
                
                sleep_time = self.interval_ms# threadin tam olarak interval kadar uyuması için ping atma süresi kadar çıkartıyorum çünkü zaten o kadar zaman geçiyo             
                if sleep_time > 0:
                    time.sleep(sleep_time) 
                endOf_while = time.time()
                pulse = endOf_while - send_time
                self.stats.update_rate(pulse)
            if not self._should_continue() :# thread işlemini bitirip durdu ise threadi kapatır, kullanıcı tarafından durduruldu ise uykuya dalar
                self.isKill = True
                break
                #TODO durduktan sonra zaman kaybı sorunu, stop metodu içinde çözülmüştür
            
            #thread durduruldu geri uyandırlımayı bekliyor


            time.sleep(2)#FIXME uzun time sleep
       
    def getStats(self):
        return self.stats
    def setWhileCondition(self, isInfinite: bool):
        self.isInfinite = isInfinite
        

    def getWhileCondition(self):
        return self.whileCondition
    def stop(self,isToggle=False, isKill=False):
        if isToggle:
            if self._stop_event.is_set():
                paused_duration = time.time() - self._pause_start_time
                self.stop_time += paused_duration
                self._stop_event.clear()
            else:
                self._pause_start_time = time.time()
                self._stop_event.set()
        
        if isKill:
            self.isKill = isKill
    def getEnd_datetime(self):
        return self.end_datetime
    def update_parameters(self, interval_ms=None, duration = None,end_datetime=None, timeout=None, count=None, isInfinite=None, **kwargs):
        if interval_ms is not None:
            self.interval_ms = interval_ms / 1000
        if end_datetime is not None:
            self.end_datetime = end_datetime
        if timeout is not None:
            self.timeout = timeout
        if count is not None:
            self.count = count
        if isInfinite is not None:
            self.isInfinite = isInfinite
        if duration is not None:
            
            if self.duration is not None:
                self.duration = duration
                self.startTime = time.time() 
                self.stop_time = self.startTime + self.duration
                self.isInfinite = False
            else:
                self.stop_time = time.time() + duration


        if kwargs:
            self.kwargs.update(kwargs)

        print(f"[{self.address}] 🔁 Thread parametreleri güncellendi.")
    def toggleBeep(self):
        if self.isBeep:
            self.isBeep=False
        else:self.isBeep=True

        
