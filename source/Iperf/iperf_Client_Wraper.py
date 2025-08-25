import iperf3
from iperf3 import Client

import PyQt5
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5        import QtCore


from source.Iperf.subproces_for_iperf import Client_subproces


parameter_for_table_headers= {  "_server_hostname": "",# buradan tablo headerları oluşturuluyordu artık subproces_for_iperf içinde
                                "_blksize": "",                                 
                                "_port": "",
                                "_num_streams": "",
                                "_zerocopy": "",
                                "_omit": "",
                                "_duration": "",
                                "_bandwidth": "",
                                "_protocol": ""
                                
}
def beautify_key(key):
    # Başındaki "_" işaretini kaldır, alt çizgileri boşluk yap, kelimelerin ilk harfini büyük yap
    return key.lstrip('_').replace('_', ' ').title()

table_headers = [beautify_key(key) for key in parameter_for_table_headers.keys()]

def get_data_keys():
        return table_headers


class Client_Wrapper(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
     
    @staticmethod
    @pyqtSlot()
    def build_client_kwargs(testResultWrapper,
    _server_hostname=None, _port=None, _num_streams=None, _zerocopy=False,
    _omit=None, _duration=None, _bandwidth=None, _protocol=None, _blksize=None, _reversed = None
    ):
        raw = {
            "server_hostname": _server_hostname,
            "port": int(_port) if _port else None,
            "num_streams": int(_num_streams) if _num_streams else None,
            "zerocopy": _zerocopy,  # Checkbox olduğundan direkt atanır
            "omit": int(_omit) if _omit else None,
            "duration": int(_duration) if _duration else None,
            "bandwidth": int(_bandwidth)*1024 if _bandwidth else None,
            "protocol": _protocol,
            "blksize": int(_blksize) if _blksize else None,
            "reversed": _reversed
        }

        # None olanları filtrele
        kwargs = {k: v for k, v in raw.items() if v is not None}
        #return Client_Runner(iperWindow=iperWindow, **kwargs)
        return Client_subproces(testresultWrapper=testResultWrapper,**kwargs)
if __name__== "__main__":
    #classı test etmek için pencere oluşturmayı düşünüyorum
    pass