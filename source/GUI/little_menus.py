from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal

import paramiko

from QTDesigns.SSH_login_dialog import Ui_Dialog



#ssh modülleri
from source.ssH.Client_Controller import Client_Controller,ClientWrapper



class ConnectionThread(QtCore.QThread):
        connection_result = pyqtSignal(object,bool, str, str, str)  # success, hostname, os_type, error
        
        def __init__(self, client_wrapper):
            super().__init__()
            self.client_wrapper = client_wrapper
            
            print(f"[ConnectionThread] client_wrapper  {self.client_wrapper}")
        def run(self):
            try:                
                self.client_wrapper.connect()
                os_type = self.client_wrapper.greet_and_set_strategy()
                self.connection_result.emit(self.client_wrapper,True, self.client_wrapper.hostname, self.client_wrapper.username, "")
            except paramiko.ssh_exception.AuthenticationException as e:
                self.connection_result.emit(None,False, self.client_wrapper.hostname, "", "Yanlış kullanıcı adı/şifre!")
            except Exception as e:
                self.connection_result.emit(None,False, self.client_wrapper.hostname, "", str(e))

        

class SSH_login(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        #buton conneciton
        self.ui.pushButton_addLogin.clicked.connect(self.login_ssh)  

        #parent(mainWindow) veri alma
        self.client_controller:Client_Controller = Client_Controller()
    def login_ssh(self):
        hostName = self.ui.lineEdit_ip.text().strip()
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        port = int(self.ui.lineEdit_port.text().strip())

        # Aynı hostname ile client var mı kontrol et
        if hostName in self.client_controller.list_clients():
            QtWidgets.QMessageBox.warning(self, "Uyarı", 
                f"{hostName} zaten eklenmiş!")
            return

        #try:
        self.client_controller.add_client(hostname=hostName, username=username, 
                                password=password, port=port)
        client_wrapper = self.client_controller.get_client(hostName)
        print(f"[createClient] client_wrapper  {client_wrapper}")
        # Bağlantı thread'i oluştur
        self.connection_thread = ConnectionThread(client_wrapper)
        self.connection_thread.connection_result.connect(self.handle_connection_result)
        self.connection_thread.start()
        
        self.info_box = QtWidgets.QMessageBox(self)
        self.info_box.setWindowTitle("Bilgi")
        self.info_box.setText(f"{hostName} için bağlantı deneniyor...")
        self.info_box.setIcon(QtWidgets.QMessageBox.Information)

        # Kapat butonu ekliyoruz
        close_button = self.info_box.addButton("Close", QtWidgets.QMessageBox.RejectRole)        
        close_button.clicked.connect(self.info_box.close)  # Buton tıklanınca pencere kapanır

        self.info_box.show()
       
        
        
        #TODO  bu commentten çıkartılabilir geliştirme süreci bitince. traceback edilmiyor exception açıldığında ama kullanıcılar için olması faydalı olur    
        """except Exception as e: 
            QtWidgets.QMessageBox.critical(self, "Hata", 
                f"İstemci oluşturulamadı: {str(e)}")
            if hostName in client_controller.list_clients():
                client_controller.remove_client(hostName)"""
        
        

    def handle_connection_result(self,clientWrapper:ClientWrapper ,success, hostname, username, error_msg):
        print(f"[handle connection thread] client_wrapper  {clientWrapper}")
        if success:
            # Başarılıysa widget ekle
            self.parent.add_client_widget(hostname, username, clientWrapper=clientWrapper)

            success_info_box = QtWidgets.QMessageBox(self)
            success_info_box.setWindowTitle("Bilgi")
            success_info_box.setText(f"{hostname} için Bağlantı başarılı")
            success_info_box.setIcon(QtWidgets.QMessageBox.Information)

            # Butonu doğru mesaja ekliyoruz
            close_button = success_info_box.addButton("Close", QtWidgets.QMessageBox.RejectRole)
            close_button.clicked.connect(success_info_box.close)  
            close_button.clicked.connect(self.close)

            success_info_box.show()
            
               
            
        else:
            # Başarısızsa client'ı temizle
            self.client_controller.remove_client(hostname)
            QtWidgets.QMessageBox.critical(self, "Hata", 
                f"{hostname} bağlantısı başarısız: {error_msg}")
        if hasattr(self, "info_box"):
            print("---------------------------------------------")
            self.info_box.close()