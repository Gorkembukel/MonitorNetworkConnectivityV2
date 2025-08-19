import sys

from source.GUI.Windows import MainWindow

from PyQt5.QtWidgets import QApplication 



#projenin kendi modülleri

#Iperf ile alakalı
from source.Iperf.subproces_for_iperf import valid_fields
from source.Iperf.iperf_controller import Iperf_controller
#Ping ile alakalı
from source.ping import PingStatistic
from source.ping.PingStatistic import get_data_keys

from source.ping import PingController
from source.ping.PingController import PingController
# SSH ile alakalı
from source.ssH.Client_Controller import Client_Controller as SSH_Client_Controller

class Applicaton:
    """Bazı verileri pencerelerden bağımsız tutmak için kullanılacak, 
    her hangi bir veriyi istenilen yere göndermek için çatı görevi görecek class
    """
    def __init__(self):
            # buradaki objeler projenin işlevlerinin tamamını yönetir, her obje singeltondır
            self.pingController = None
            self.iperfController = None
            self.sshController = None

                 

            self.ping_tableHeaders = []
            self.iperf_tableHeaders = []
            self.set_tablewidget_ip_header()#uygulama başında table için headerların ne olduğunu öğrenir
                                            # bu işlem bir kez yapılacağı için init aşamasında gerçekleştiriliyor
            self.set_tablewidget_iperf_header()

             #ana pencerenin başlatılması #en sonda olması daha sağlıklı olur
            self.app = QApplication(sys.argv)
            self.mainWindow = MainWindow(applicaton=self)    
            self.mainWindow.show()      
            sys.exit(self.app.exec())# bu en sonda olmalı
    
    #ping için header bilgilerini get set
    def set_tablewidget_ip_header(self):
        self.ping_tableHeaders = get_data_keys()
    def get_tablewidget_ip_header(self):
         return self.ping_tableHeaders
    #iperf için header bilgilerini get set
    def set_tablewidget_iperf_header(self):
         
         self.iperf_tableHeaders = valid_fields
         
    def get_tablewidget_iperf_header(self):
         return self.iperf_tableHeaders

    def init_PingController(self):
        self.pingController = PingController()
        return self.pingController

    def init_IperfController(self):
        self.iperfController = Iperf_controller()
        return self.iperfController
    
    
    def init_SSHController(self):
         self.sshController = SSH_Client_Controller()


if __name__ == "__main__":
    Applicaton()