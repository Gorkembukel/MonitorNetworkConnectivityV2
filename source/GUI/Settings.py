import sys

from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QListView, QPushButton
)
from PyQt5.QtCore import Qt







# Bu python dosyasının bulunduğu dizin (root/source/gui/)
path_of_this_module = Path(__file__).resolve().parent

# Oradan iki klasör yukarı çık (root'a gel) ve config/ip_list.txt yolunu oluştur
path_of_target_folder = path_of_this_module.parent.parent / "config" / "settings.txt"
class ReOrderPingTAbleHeaders(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)#parent burada Windows olacak
        self.parent = parent  # Windows örneğini sakla
        self.setWindowTitle("Reordering Ping Table Headers ")
        self.setGeometry(200, 200, 1450, 75)

        self.neworder = None
        # Ana layout
        main_layout = QVBoxLayout(self)

        # Yatay liste
        self.list_widget = QListWidget()
        self.list_widget.setFlow(QListView.LeftToRight)
        self.list_widget.setWrapping(False)
        self.list_widget.setDragDropMode(QListWidget.InternalMove)

        # ilk baştaki headerı buradan okuyacak
        for text in parent.ping_headers:
            item = QListWidgetItem( "| " + text + " |")
            
            self.list_widget.addItem(item)

        # Save butonu
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_order)

        # Layoutlara ekle
        main_layout.addWidget(self.list_widget)
        h_layout = QHBoxLayout()
        h_layout.addStretch()
        h_layout.addWidget(self.save_button)
        main_layout.addLayout(h_layout)

        # Enter tuşunu Save'e bağla
        self.save_button.setDefault(True)
        self.save_button.setAutoDefault(True)
    #pingheaders'ı ve config'i buradan güncelleyecek
    def save_order(self):
        # Önce QListWidget'tan sıralı header'ları al
        order = [self.list_widget.item(i).text().strip('| ').strip() for i in range(self.list_widget.count())]

        #  parent.ping_headers güncelle
        if self.parent:
            if isinstance(self.parent.ping_headers, dict):
                # dict ise key sırasını order'a göre yeniden oluştur
                new_dict = {k: self.parent.ping_headers[k] for k in order if k in self.parent.ping_headers}
                self.neworder = new_dict
                self.parent.ping_headers = new_dict
            else:
                # list ise direkt at
                self.parent.ping_headers = order

        #  Dosyaya yazılacak format
        line = 'pingHeaders: ' + ';'.join(f'"{h}"' for h in order) + '\n'

        try:
            with open(path_of_target_folder, 'w', encoding='utf-8') as f:
                f.write(line)
           
        except Exception as e:
            print("Dosyaya yazarken hata oluştu:", e)

        self.accept()  # Dialog'u kapat

    def get_new_order(self):
        """Liste widget’taki sıralı header’ları döndürür"""
        return self.neworder

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = ReOrderPingTAbleHeaders()
    dialog.exec_()
