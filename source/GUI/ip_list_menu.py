import sys
from typing import List
from pathlib import Path



#PyQT5 imports
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal , pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QTableWidgetItem,QSizePolicy


#QTdesign imports

from QTDesigns.Window_for_ip_control import Ui_MainWindow as Ui_window_for_ip_list  
from QTDesigns.ip_list_widget import Ui_Dialog as Ui_ssh_account

#projenin kendi modülleri
from source.GUI.little_menus import SSH_login

# Bu python dosyasının bulunduğu dizin (root/source/gui/)
path_of_this_module = Path(__file__).resolve().parent

# Oradan iki klasör yukarı çık (root'a gel) ve config/ip_list.txt yolunu oluştur
path_of_target_folder = path_of_this_module.parent.parent / "config" / "ip_list.txt"


def read_accounts():#TODO (ayrı threadde çalışması daha iyi olabilir) 
   accounts = []
   with open(path_of_target_folder, "r", encoding="utf-8") as f:
      for line in f:
         line = line.strip()
         if not line or line.startswith("#"):  # boş veya yorum satırlarını atla
               continue
         try:
               ip, username, password = line.split(";")
               accounts.append({
                  "ip": ip.strip(),
                  "username": username.strip(),
                  "password": password.strip()
               })
         except ValueError:
               print(f"Geçersiz satır atlandı: {line}")
            
   
   return accounts
#Qthreadler
# add acountda eklenen ip ve username zaten accounts da var mı
class DuplicateCheckThread(QThread):
   result = pyqtSignal(bool)  # True = duplicate bulundu, False = eklenebilir

   def __init__(self, new_account, accounts_list):
      super().__init__()
      self.new_account = new_account
      self.accounts_list = accounts_list

   def run(self):
      # Listeyi tara (O(n))
      is_duplicate = any(
         acc['ip'] == self.new_account['ip'] and acc['username'] == self.new_account['username']
         for acc in self.accounts_list
      )
      self.result.emit(is_duplicate)
   def __del__(self):
      print("[DuplicateCheckThread içi  silindi]")

#küçük menüler
class AddAccountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yeni Hesap Ekle")
        self.setModal(True)
        self.resize(300, 150)

        layout = QtWidgets.QFormLayout(self)

        self.ip_input = QtWidgets.QLineEdit()
        self.username_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        

        layout.addRow("IP Adresi:", self.ip_input)
        layout.addRow("Username:", self.username_input)
        layout.addRow("Password:", self.password_input)

        # Butonlar
        buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_data(self):
        return {
            "ip": self.ip_input.text().strip(),
            "username": self.username_input.text().strip(),
            "password": self.password_input.text().strip()
        }
    

class Item_Scrol_Area_widget(QDialog):
   instance_count = 0
   #sinyal
   connect_requested = pyqtSignal(dict)  # account bilgisi ile sinyal
   def __init__(self, account: dict, parent= None, mainWindow= None):
      super().__init__(parent)
      self.parent_window = mainWindow
      self.ui = Ui_ssh_account()
      self.ui.setupUi(self)
      self.account = account
      Item_Scrol_Area_widget.instance_count += 1  # sonraki instance için artır
       # Account dict'ten bilgileri al ve widget içine yerleştir
      self.ui.lineEdit_ipaddres.setText(account.get("ip", ""))
      self.ui.lineEdit_username.setText(account.get("username", ""))
      self.ui.lineEdit_password.setText(account.get("password", ""))

      #button bağlama
      self.ui.pushButton_del.clicked.connect(self.confirm_delete)
      self.ui.pushButton_connect.clicked.connect(self.connect_to_ssh)

      #self.ui.pushButton_connect
      # Rengini index'e göre belirle
      light_color = "#f0f0f0"  # açık gri
      dark_color  = "#dcdcdc"  # koyu gri
      bg_color = light_color if Item_Scrol_Area_widget.instance_count % 2 == 0 else dark_color
      #style sheet ayarları
      self.setStyleSheet(f"""
      QDialog {{
         background-color: {bg_color};   /* ana widget arka planı */
         border-radius: 8px;
      }}
              
         
      """)
   def connect_to_ssh(self):
      # Eğer pencere zaten oluşturulmamışsa, oluştur
      if not hasattr(self, 'loginMenu') or self.loginMenu is None:
         self.parent_window.loginMenu = SSH_login(parent=self.parent_window)
         
      self.parent_window.loginMenu.login_ssh_from_ip_list(
            ip=self.account['ip'],
            username=self.account['username'],
            password=self.account['password']
      )
       
   def confirm_delete(self):
        reply = QtWidgets.QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes and self.parent_window:
            # parent layout'tan kaldır
            self.parent_window.scroll_layout.removeWidget(self)
            self.setParent(None)
            self.deleteLater()

            # parent accounts listesinden sil
            if self.account in self.parent_window.accounts:
               self.parent_window.accounts.remove(self.account)
               
            # dosyayı tekrar yaz
            with open(path_of_target_folder, "w", encoding="utf-8") as f:
                for acc in self.parent_window.accounts:
                    f.write(f"{acc['ip']};{acc['username']};{acc['password']}\n")
   def __del__(self):      
      Item_Scrol_Area_widget.instance_count -= 1
      
class Accounts_list_window(QMainWindow):
   def __init__(self, parent= None):
      super().__init__(parent)
      self.parent_mainWindow = parent
      self.ui = Ui_window_for_ip_list()
      self.ui.setupUi(self)
      self.ui.rightFrame.hide()
      self.setWindowTitle("SSH Account Management")

      self.accounts = read_accounts()#ip_list.txt'ini okur

      # Scroll Area içinde bir widget container oluştur      
      self.scroll_layout = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)      
      self.scroll_layout.setContentsMargins(0, 0, 0, 0)
      self.scroll_layout.setSpacing(5)  # widgetlar arası boşluk            
      self.ui.scrollArea.setWidget(self.ui.scrollAreaWidgetContents)    
      self.list_to_widget()
      self.scroll_layout.addStretch()
      #scrol are içine eklenecek widgetların renk ayarı
      light_color = "#f0f0f0"  # açık gri
      dark_color  = "#dcdcdc"  # koyu gri
      #button bağlama
      self.ui.pushButton_addaccount.clicked.connect(self.add_account)


   def list_to_widget(self):#TODO (ayrı threadde çalışması daha iyi olabilir) aldığı listedeki bilgilere göre scrol areada gözükecek widgetları oluşturur.
      for account in self.accounts:
            item_widget = Item_Scrol_Area_widget(account=account, parent=self, mainWindow=self.parent_mainWindow)
            # Eğer widget içinde account bilgisi gösterecek bir alan varsa doldurabilirsin:
            # item_widget.ui.label_ip.setText(account['ip'])
            self.scroll_layout.addWidget(item_widget)
   def add_account(self):
        dialog = AddAccountDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_account = dialog.get_data()
            
             # 2️⃣ Thread ile kontrol başlat
            self.check_thread = DuplicateCheckThread(new_account, self.accounts)
            self.check_thread.result.connect(lambda is_dup: self.handle_duplicate_check(is_dup, new_account))
            self.check_thread.start()
            
          

   
   # 3️⃣ Thread sonucu geldiğinde işleme
   def handle_duplicate_check(self, is_duplicate, new_account):
      if is_duplicate:
         QtWidgets.QMessageBox.warning(
               self,
               "Duplicate Account",
               "An account with this IP and username already exists!"
         )
         return

      # Listeye ekle
      self.accounts.append(new_account)

      # Yeni widget oluştur ve scroll layouta ekle
      item_widget = Item_Scrol_Area_widget(new_account, self)
      self.scroll_layout.insertWidget(self.scroll_layout.count() - 1, item_widget)

      # Dosyaya kaydet
      with open(path_of_target_folder, "a", encoding="utf-8") as f:
         f.write(f"{new_account['ip']};{new_account['username']};{new_account['password']}\n")
if __name__ =='__main__':    
    
   app = QApplication(sys.argv)
   window = Accounts_list_window()
   window.show()
   sys.exit(app.exec_())









