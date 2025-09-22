

from datetime import datetime
from icmplib import ping


import PyQt5 
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QTimer,Qt,QDateTime,QThread
from PyQt5.QtWidgets import QMainWindow, QDockWidget,QAction,QTableWidgetItem,QDialog,QMessageBox

#projenin kendi modülleri
#Setting için
from source.GUI.Settings import ReOrderPingTAbleHeaders

#ip list penceresi
from source.GUI.ip_list_menu import Accounts_list_window

#Iperf ile alakalı
from source.Iperf.subproces_for_iperf import valid_fields
from source.Iperf.iperf_controller import Iperf_controller
from source.GUI.GUI_graph_iperf import GraphWindow_iperf
#SSH ile alakalı
from source.GUI.little_menus import SSH_login
from source.GUI.ssh_window import ClientWidget_summary,SSH_Client_Window
from source.ssH.Client_Controller import Client_Controller,ClientWrapper

#QTDesign
from QTDesigns.MainMenu import Ui_MainWindow
from QTDesigns.Change_parameters import Ui_Dialog_changeParameter

#Ping ile alakalı
from source.ping.PingStatistic import get_data_keys
from source.ping.PingController import PingController,PingTask
from source.GUI.Ping_Graph import GraphWindow
class LeftClickMenu(QtWidgets.QMenu):
    def mouseReleaseEvent(self, event):
        # sadece sol tıkla çalışsın
        if event.button() == Qt.LeftButton:
            super().mouseReleaseEvent(event)
        else:
            event.ignore()
class ChangeParameterWindow(QDialog):
    def __init__(self, parent= None, task:PingTask = None):
        super().__init__(parent)
        self.ui = Ui_Dialog_changeParameter()
        self.ui.setupUi(self)
        self.task = task
        self.setWindowTitle(task.address)
        self.isInfinite = task.isInfinite
        self.timeOut = str(int(task.kwargs['timeout']))
        self.ui.checkBox_infinite.setCheckState(self.isInfinite)
        
        
        #task değerlerini okuyup gösterir
        self.ui.lineEdit_ip.setText(task.address)
        self.ui.spinBox_interval.setValue(task.interval_ms)
        self.ui.spinBox_payloadsize.setValue(int(task.kwargs['payload_size']))
        self.ui.spinBox_timeout.setValue(int(self.timeOut))
    
        

        self.ui.pushButton_settChages.clicked.connect(self.applyChange) 

        

        
    def applyChange(self):
        try:
            interval_val = self.ui.spinBox_interval.value()
            timeout_val = self.ui.spinBox_timeout.value()
            payload_val = self.ui.spinBox_payloadsize.value()
            isInfinite_val = self.ui.checkBox_infinite.isChecked()

            # Task parametrelerini güncelle
            self.task.interval_ms = interval_val
            self.task.kwargs["timeout"] = timeout_val
            self.task.kwargs["payload_size"] = payload_val
            self.task.isInfinite = isInfinite_val

            # Thread parametrelerini güncelle
            self.task.update_thread_parameters()
            self.close()  # pencereyi kapat
        except ValueError as e:
            print(f"❗ Hatalı giriş: {e}")
            QtWidgets.QMessageBox.warning(self, "Geçersiz Girdi", "Lütfen tüm değerleri sayısal ve doğru formatta girin.")
    def __del__(self):
        print(f"Change appley penceresinin objesi silindi")








class MainWindow(QMainWindow):
    
    def __init__(self,applicaton, parent= None):
        super().__init__(parent)
        #QTdesignda tasarlanan pencere burada yüklenir
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #MainWindow ile alakalı kurulumlar
        self.setWindowTitle("Network Connectivity Monitor Window")
        self._build_view_menu()#View menu'u doldurur

        
        self.ui.tableWidget_ping.resizeColumnsToContents()
        #Sistem kurulumu
        self.application = applicaton # bu application pyqt ile alakalı değil. veri aktarımını proje içinde kolaylaştırmak için çatı class

        #action bağlama
        self.ui.actionAdd_iperf_Client.triggered.connect(self.change_tabTo_iperf)
        self.ui.actionAdd_ping.triggered.connect(self.change_tabTo_ping)
        self.ui.actionAdd_SSH_Client.triggered.connect(self.open_ssh_loginMenu)
        self.ui.actionIP_List.triggered.connect(self.open_ip_list)
            #Iperf için önemli
        self.iperf_headers = self.application.get_tablewidget_iperf_header()
        self.valid_fields = valid_fields
        self.iperfController:Iperf_controller = self.application.init_IperfController()
        self.set_table_headers_iperf()   
        
            #ping için önemli
        self.pingController:PingController = self.application.init_PingController()
        self.statList = self.pingController.stats_list
        self.ping_headers = self.application.get_tablewidget_ip_header()
        self.set_table_headers()#tableWidget_ping headersını ayarlar
            #SSH için önemli
        self.SSH_Client_Controller:Client_Controller = self.application.init_SSHController()
        #button bağlama
            #ping için
        self.ui.pushButton_addPing.clicked.connect(self.extract_addresses)
        self.ui.frame_rigthPingsetting.setHidden(True)# sağdaki menü görünmez hale getirilir başlangıç için
        self.ui.pushButton_startAll.clicked.connect(self.startAll)
        self.ui.pushButton_stopAll.clicked.connect(self.stopAll)

            #iperf için
        #    self.ui.pushButton_iperfStartAll.setHidden(True)
        #    self.ui.pushButton_iperfStopall.setHidden(True)
        self.ui.pushButton_iperfStartAll.clicked.connect(self.iperfController.start_all)
        self.ui.pushButton_iperfStopall.clicked.connect(self.iperfController.stop_all)
            #ssh için
        self.ui.pushButton_loginmenu.clicked.connect(self.open_ssh_loginMenu)

        #evetfilter bağlama
            #ping için
        self.ui.tableWidget_ping.viewport().installEventFilter(self)
        self.ui.tableWidget_ping.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            #iperf için        
        self.ui.tableWidget_iperfClient.viewport().installEventFilter(self)
        
        #SSH için değişkenler
        self.clientWidgets = []
        self.scroll_layout = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.ui.scrollAreaWidgetContents.setLayout(self.scroll_layout)
        #Iperf için değişkenler
        self.ui.iperf_rigth_menu.setHidden(True)
        self.ui.pushButton_apply.clicked.connect(self.add_iperfClient)
        self.iperf_target_to_row = {}

        self.ui.label_bulksize.setHidden(True)
        self.ui.lineEdit_bulksize.setHidden(True)
        #ping için değişkenler
        self.target_to_row = {}
        self.isInfinite= False
        
            #ip addreslerini program başında ip.txt^den oku
        try:
            with open('ip.txt', 'r', encoding='utf-8') as output:
                self.last_ip_list = [line.strip() for line in output if line.strip()]
        except FileNotFoundError:
            self.last_ip_list = []
        if self.last_ip_list and not self.statList:            
            for line in self.last_ip_list:
                self.ui.plainTextEdit_iplist.insertPlainText(f"{line}\n")
        #Genel arayüz işlemleri.
        self.ui.Rightdock_LoginSSH.setHidden(True)# başlangıçta sağ docker görünmez olur
        #QTimer
        self.ping_tableTimer = QTimer(self)
        self.ping_tableTimer.setInterval(1000)  # 1000ms = 1 saniye#60fps için girilen değr
        self.ping_tableTimer.timeout.connect(self.update_ping_table)
        self.ping_tableTimer.timeout.connect(self.iperf_update_clientTable)
        self.ping_tableTimer.start()

    #Action metotları
    def change_tabTo_ping(self):
        self.ui.MainBody.setCurrentWidget(self.ui.tab_ping)#0 ping için
        if self.ui.frame_rigthPingsetting.isHidden():
            self.ui.pushButton_pingSetting.click()
    def change_tabTo_iperf(self):
        self.ui.MainBody.setCurrentWidget(self.ui.tab_iperf)#0 ping için
        if self.ui.iperf_rigth_menu.isHidden():
            self.ui.pushButton_iperfSetting.click()
    #Iperf için #############################################################################
    class QThread_ping(QThread):# iperfde client eklemeden önce o client'a ping atar sonra clienti ekler. Şu an çalışmıyor
        def __init__(self,server_hostname:str, parent = None,params = None):
            super().__init__(parent)
            self.server_hostname = server_hostname
            self.params = params
        def add_iperfClient(self):
            self.iperfController.add(**self.params)

        def run(self):
            timeOut = 2
            result = ping(self.server_hostname,1,1,timeOut)#TODO Settings gibi bir yerden burası değiştirilebilinir
            if not result.is_alive:
                QMessageBox.information(
                    None,
                    "Ping Sonucu",
                    f"{self.server_hostname} adresine bağlanılamadı. Timeout: {timeOut}s"
                )
            else:
                QMessageBox.information(
                    None,
                    "Ping Sonucu",
                    f"{self.server_hostname} bağlantı gerçekleşti."
                )
                self.add_iperfClient()
        def __delete__(self):
            print(f"[QThread_ping içi]    bu thread kapandı")

    def open_ip_list(self):
        
        # 1) Eğer daha önce oluşturulmamışsa oluştur
        if not hasattr(self, 'accounts_window') or self.accounts_window is None:
            
            self.accounts_window = Accounts_list_window(parent=self)

        # 2) Pencereyi gizlemek yerine sadece göster
        if not self.accounts_window.isVisible():
            self.accounts_window.show()
        self.accounts_window.raise_()
        self.accounts_window.activateWindow()

    def start_iperf(self,hostName):
        self.iperfController.start(hostName)

    def open_graph_iperf(self,hostName):

        testResult = self.iperfController.get_testResultWrapper(hostName)

        self.window = GraphWindow_iperf(testResult)
        self.window.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.window.show()

    def delete_client(self, address):
        self.pingController.delete_stats(address=address)

        row = self.iperf_target_to_row.pop(address, None)  # yoksa None döner, KeyError vermez
        self.iperf_update_target_to_row(row)
        self.ui.tableWidget_iperfClient.removeRow(row)
        self.iperfController.delete_client(address)
        


    def add_iperfClient(self):
        server_hostname = self.ui.lineEdit_serverhostname.text() or None
        port            = self.ui.lineEdit_port.text() or None
        num_streams     = self.ui.lineEdit_numstreams.text() or None
        zerocopy        = self.ui.checkBox_zerocopy.isChecked()
        reversed        = self.ui.checkBox_reversed.isChecked()
        omit            = self.ui.lineEdit_omit.text() or None
        duration        = self.ui.lineEdit_duration.text() or None
        bandwidth       = self.ui.lineEdit_bandwidth.text() or None
        protocol        = self.ui.lineEdit_protocol.text() or None
        bulksize        = self.ui.lineEdit_bulksize.text() or None


        #self.QThread_ping(server_hostname=server_hostname).run()#sadece bir kez çalışır
        params = {#buradaki keywordler iperf_clientWrapper da parameter_for_table_headers'a göre girilmeli
            "hostName":  server_hostname,
            "_server_hostname":  server_hostname,
            "_port":      port,
            "_num_streams": num_streams,
            "_zerocopy":  zerocopy,
            "_reversed":   reversed,   
            "_omit":      omit,
            "_duration":  duration,
            "_bandwidth": bandwidth,
            "_protocol":  protocol,
            "_blksize":  bulksize,
        }

        # Metoda geçir
        self.iperfController.add(**params)
        self.iperf_update_clientTable()
        

    def iperf_update_target_to_row(self,deleted_row):#iperf için bu method bir ip listeden çıkartılınca tablonun kaymasını engellemek için
                                    #target_to_row dictonry'si içinde ki gerekli value'ları bir değer küçültür 
        new_map = {}
        for target, row in self.iperf_target_to_row.items():
            if row > deleted_row:
                new_map[target] = row - 1
            elif row < deleted_row:
                new_map[target] = row
            # eşitse (row == deleted_row) zaten silinmiş olmalı → atlanır
        self.iperf_target_to_row = new_map

    
    def iperf_update_clientTable(self):        
        self.ui.tableWidget_iperfClient.clearContents()

        for client in self.iperfController.clientSubproceses.values():
            # Satır anahtarı: hostname (gerekirse ":port" ekleyebilirsin)
            
            target = client.server_hostname
            
            
            
            if target in self.iperf_target_to_row:#target ip için target_to_row içinde varsa
                row = self.iperf_target_to_row[target]
            else:#yeni ip tabloya eklenecekse

                #tablodaki bütün satırları tek tek boş mu diye dener
                for row in range(self.ui.tableWidget_iperfClient.rowCount()):
                    
                    it = self.ui.tableWidget_iperfClient.item(row, 0)#satırların sadece başındaki columa bakar o yüzden 0
                    if it is None:  #hali hazırda olan satırlardan boşluğa denk gelirse oraya koyar
                        self.target_to_riperf_target_to_rowow[target] = row
                        break
                if target not in self.iperf_target_to_row:#eğer döngü bittiğinde hala boşluk yoksa en sona yeni bir satır oluşturup koyar
                    row = len(self.iperf_target_to_row.keys()) 
                    self.ui.tableWidget_iperfClient.insertRow(row)
                    self.iperf_target_to_row[target] = row
                    
                    self.iperf_target_to_row[target] = row


            # Kolonları, header sırasına göre doldur
            for col, key in enumerate(self.iperf_headers):
                value = getattr(client, key, key)
                item = QTableWidgetItem(str(value if value is not None else ""))
                self.ui.tableWidget_iperfClient.setItem(row, col, item)

        self.ui.tableWidget_iperfClient.resizeColumnsToContents()

        
    def set_table_headers_iperf(self):        
        self.ui.tableWidget_iperfClient.setColumnCount(len(self.iperf_headers))
        self.ui.tableWidget_iperfClient.setHorizontalHeaderLabels(self.iperf_headers)

    #SSH için ###############################################################################

    def open_ssh_loginMenu(self):
        self.ui.Rightdock_LoginSSH.setVisible(True)
    # Eğer pencere zaten oluşturulmamışsa, oluştur
        if not hasattr(self, 'loginMenu') or self.loginMenu is None:
            self.loginMenu = SSH_login(self)
        
        

        # Pencereyi göster ve öne getir
        self.loginMenu.show()
        self.loginMenu.raise_()
        self.loginMenu.activateWindow()
    
    def add_client_widget(self ,hostname, username, port=22,clientWrapper:ClientWrapper=None):
        # Yeni bir ClientWidget oluştur
        client_widget = ClientWidget_summary(hostname, username, port,clientWrapper=clientWrapper)
        client_widget.delete_requested.connect(self.remove_client_widget)
        self.clientWidgets.append(client_widget)
        # Scroll Area'nın layout'una ekle
        self.scroll_layout.addWidget(client_widget)
        
        # Eğer scroll alanı dolduysa kaydırma çubuğunu otomatik aşağı kaydır
        self.ui.scrollArea.verticalScrollBar().setValue(
            self.ui.scrollArea.verticalScrollBar().maximum()
        )
        return  client_widget
    
    #Ping için ##########################################################################3333
    def startAll(self):
        self.pingController.start_all()
    def stopAll(self):
        self.pingController.stop_All()
    def update_ping_table(self):
        self.ui.tableWidget_ping.clearContents()        
        for stat in self.statList.values():# FIXME burada stat_list dictonrydir
            summary = stat.summary()
            target = summary["target"]

            if target in self.target_to_row:#target ip için target_to_row içinde varsa
                row = self.target_to_row[target]
            else:#yeni ip tabloya eklenecekse

                #tablodaki bütün satırları tek tek boş mu diye dener
                for row in range(self.ui.tableWidget_ping.rowCount()):
                    
                    it = self.ui.tableWidget_ping.item(row, 0)#satırların sadece başındaki columa bakar o yüzden 0
                    if it is None:  #hali hazırda olan satırlardan boşluğa denk gelirse oraya koyar
                        self.target_to_row[target] = row
                        break
                if target not in self.target_to_row:#eğer döngü bittiğinde hala boşluk yoksa en sona yeni bir satır oluşturup koyar
                    row = len(self.target_to_row.keys()) 
                    self.ui.tableWidget_ping.insertRow(row)
                    self.target_to_row[target] = row
                    
                    self.target_to_row[target] = row

            # ✅ Renk sadece bir kere belirleniyor
            last_result = summary.get("last result", "")
            color = QColor(200, 255, 200) if last_result == "Success" else QColor(255, 200, 200)

            # 🔁 Hem hücreyi doldur, hem rengini ver
            for col, key in enumerate(self.ping_headers):                
                 
                    value = summary.get(key, "")
                    item = QTableWidgetItem(str(value))
                    item.setBackground(color)
                    self.ui.tableWidget_ping.setItem(row, col, item)       
        
        self.ui.tableWidget_ping.resizeColumnsToContents()
        
     #burada rowdaki veriler alınıp açılan pencereye aktarılmalı böylece rowdaki ip kontrol edilmiş olunur# bir tane eventfilter olacağından iperf ile ortak
    def eventFilter(self, source, event):
            # 1) PING TABLOSU
        if (event.type() == QtCore.QEvent.MouseButtonPress and
            source is self.ui.tableWidget_ping.viewport()):

            if event.buttons() == QtCore.Qt.RightButton:
                row = self.ui.tableWidget_ping.rowAt(event.pos().y())
                col = self.ui.tableWidget_ping.columnAt(event.pos().x())
                if row == -1 or col == -1:
                    return super(MainWindow, self).eventFilter(source, event)

                header_item = self.ui.tableWidget_ping.item(row, 0)
                address = header_item.text() if header_item else None

                menu = LeftClickMenu()
                if self.pingController.is_alive_ping(address=address):
                    menu.addAction("Yeniden Başlat", lambda: self.restart_ping(address=address))
                else:
                    menu.addAction("Ping Başlat", lambda: self.start_ping(address=address))
                menu.addAction("Grafik Aç", lambda: self.open_graph(address=address))
                menu.addAction("Beep", lambda: self.toggleBeep_by_address(address))
                menu.addAction("Durdur", lambda: self.ip_stop(address=address, isToggle=True, isKill=True))
                menu.addAction("Sil", lambda: self.deleteRowFromTable_ping(address=address))
                menu.exec(self.ui.tableWidget_ping.mapToGlobal(event.pos()))
                return True  # olayı tükettik

            if event.buttons() == QtCore.Qt.LeftButton:
                row = self.ui.tableWidget_ping.rowAt(event.pos().y())
                if row != -1:
                    header_item = self.ui.tableWidget_ping.item(row, 0)
                    if header_item:
                        address = header_item.text()
                        self.open_changeSettingsWindow(task=self.pingController.get_task(address=address))
                return True

        # 2) IPERF TABLOSU
        if (event.type() == QtCore.QEvent.MouseButtonPress and
            source is self.ui.tableWidget_iperfClient.viewport()):

            if event.buttons() == QtCore.Qt.RightButton:
                row = self.ui.tableWidget_iperfClient.rowAt(event.pos().y())
                col = self.ui.tableWidget_iperfClient.columnAt(event.pos().x())
                if row == -1 or col == -1:
                    return super(MainWindow, self).eventFilter(source, event)

                header_item = self.ui.tableWidget_iperfClient.item(row, 0)
                hostName = header_item.text() if header_item else None

                menu = LeftClickMenu()
                menu.addAction("Iperf başlat", lambda: self.start_iperf(hostName))
                menu.addAction("Grafik", lambda: self.open_graph_iperf(hostName))
                menu.addAction("Sil", lambda: self.delete_client(hostName))
                menu.exec(self.ui.tableWidget_iperfClient.mapToGlobal(event.pos()))
                return True

            # (İstersen sol tık davranışı da ekle)
            # if event.buttons() == QtCore.Qt.LeftButton:
            #     ...

        return super(MainWindow, self).eventFilter(source, event)
    
    def open_changeSettingsWindow(self, task:PingTask):
        if task:
            self.changeSetting = ChangeParameterWindow(task=task)
            
            self.changeSetting.show()
    def start_ping(self, address:str):
        self.pingController.start_task(address=address)
    def open_graph(self,address):
        task = self.pingController.get_task(address=address)
        statObject = task.stats
        
        self.graphWindow = GraphWindow(stat_obj=statObject,parent=self)
        self.graphWindow.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.graphWindow.show()
    def ip_stop(self, address:str, **kargs):
        print("stop_address kargs:", kargs)#BUG geçici
        
        self.pingController.stop_address(address=address, **kargs)
    def restart_ping(self, address:str):
        self.pingController.restart_task(address=address)
    def deleteRowFromTable_ping(self,address:str):
        
        self.pingController.delete_stats(address=address)
        row = self.target_to_row.pop(address, None)  # yoksa None döner, KeyError vermez
        self.update_target_to_row(row)
        self.ui.tableWidget_ping.removeRow(row)



    def update_target_to_row(self,deleted_row):#bu method bir ip listeden çıkartılınca tablonun kaymasını engellemek için
                                    #target_to_row dictonry'si içinde ki gerekli value'ları bir değer küçültür 
        new_map = {}
        for target, row in self.target_to_row.items():
            if row > deleted_row:
                new_map[target] = row - 1
            elif row < deleted_row:
                new_map[target] = row
            # eşitse (row == deleted_row) zaten silinmiş olmalı → atlanır
        self.target_to_row = new_map

    def toggleBeep_by_address(self,address:str):#
          
        self.pingController.toggleBeep_by_address(address=address)

    def extract_addresses(self):
        # 1) UI'dan adresleri oku
        text = self.ui.plainTextEdit_iplist.toPlainText()
        addresses = [line.strip() for line in text.splitlines() if line.strip()]

        # 2) Parametreleri topla (UI default'lar doğruysa ek korumaya gerek kalmaz)
        payload_size = self.ui.spinBox_packetSize.value() or 56
        interval_ms  = self.ui.spinBox_pingInterval.value()
        isInfinite   = self.ui.pushButton_infinitePing.isChecked()
        duration     = self.ui.spinBox_duration.value() if self.ui.spinBox_duration.isEnabled() else None
        timeout      = self.ui.spinBox_timeOut.value() 
        # 3) Mevcut çalışan hedefler ve yeni hedefler arasında fark al
        current_set = set(self.statList.keys()) if isinstance(self.statList, dict) else set()
        new_set     = set(addresses)

        to_add    = list(new_set - current_set)
        to_remove = list(current_set - new_set)

        # 4) Eklenmesi gerekenleri tek seferde ekle
        if to_add:
            self.pingController.add_addressList(
                timeout=timeout,
                addresses=to_add,                
                interval_ms=interval_ms,
                duration=duration,
                isInfinite=isInfinite,
                payload_size=payload_size
                
            )

        # 5) Listeden çıkarılanları durdur ve sil
        for ip in to_remove:
            self.pingController.stop_address(address=ip, isKill=True)
            self.pingController.delete_stats(address=ip)
            row = self.target_to_row.pop(ip, None)
            self.update_target_to_row(row)
            self.ui.tableWidget_ping.removeRow(row)


         # 6) Snapshot'ı güncelle (bir sonraki karşılaştırma için)
        self.textInBegining = "\n".join(addresses)#TODO buraya bakılmalı
        self.update_ping_table()
        
    def setIsInfinite(self):    
        if self.isInfinite:
            self.isInfinite =False
        else:
            self.isInfinite = True
    ##############################3
    def set_table_headers(self):        
        self.ui.tableWidget_ping.setColumnCount(len(self.ping_headers))
        self.ui.tableWidget_ping.setHorizontalHeaderLabels(self.ping_headers)

    def _build_view_menu(self):# View için dock widgetları bulup show, hide özelliklerini gösterir
        """Var olan tüm dock'ları View menüsüne ekler + toplu göster/gizle."""
        self.ui.menuView.clear()

        docks = self.findChildren(QDockWidget)

        # Her dock için toggle action ekle
        for d in docks:
            self.ui.menuView.addAction(d.toggleViewAction())

        # Ayırıcı + Hepsini Göster/Gizle
        self.ui.menuView.addSeparator()

        show_all = QAction("Show All Docks", self)
        show_all.triggered.connect(lambda: self._show_all(docks))
        self.ui.menuView.addAction(show_all)

        hide_all = QAction("Hide All Docks", self)
        hide_all.triggered.connect(lambda: self._hide_all(docks))
        self.ui.menuView.addAction(hide_all)
        self.ui.menuView.addSeparator()
        reorder_ping_header = QAction("Reorder Ping Table Header", self)
        reorder_ping_header.triggered.connect(self._reorder_ping_table_header)
        self.ui.menuView.addAction(reorder_ping_header)
        
    def _reorder_ping_table_header(self):
        reorder_window = ReOrderPingTAbleHeaders(parent=self)
        reorder_window.exec_()  # Modal olarak göster
        # Eğer kullanıcı değişiklik yaptıysa, yeni header'ları al ve uygula
        if reorder_window.result() == QDialog.Accepted:
            self.set_table_headers()        # Header’ları güncelle
            
            self.update_ping_table() 
    @pyqtSlot(str)
    def remove_client_widget(self, hostname):
        print(f"[remove_client_widget]   sinyal geldi")
        # Find and remove the widget with matching hostname
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'hostname') and widget.hostname == hostname:
                widget.setParent(None)  # Remove from layout
                widget.deleteLater()  # Schedule for deletion
                break
    def _show_all(self, docks):
        for d in docks:
            d.show()
            # İsteğe bağlı: tab'li dock'larda üste getir
            try:
                d.raise_()
            except Exception:
                pass
    def _hide_all(self, docks):
        for d in docks:
            d.hide()
    def close_all_summaryWidget(self):
        
        """Scroll layout içindeki tüm client widget'ları siler"""
        # Layout'taki tüm widget'ları al
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            print(f"widget: {widget}")
            if widget:
                # Widget'ın deleteLater metodunu çağır
                widget.deleteLater()
    def closeEvent(self, event):
        print("Uygulama kapanıyor, en son ki ip'ler txt'e aktarılıyor...")
          # ip.txt'ye kaydet
        if self.statList:  
            try:
                if isinstance(self.statList, dict):
                    ips_to_save = list(self.statList.keys())
                else:
                    ips_to_save = []

                with open('ip.txt', 'w', encoding='utf-8') as f:
                    f.write("\n".join(ips_to_save))

                print(f"ip.txt kaydedildi ({len(ips_to_save)} IP).")
            except Exception as e:
                print("ip.txt kaydedilemedi:", e)

        print("Uygulama kapanıyor, threadlerin kapanması bekleniyor")
        print("client summary widgetlar kapanıyor")
        self.close_all_summaryWidget()

        # Thread nesnelerini döngüyle durdur
        self.pingController.stop_All()
        self.SSH_Client_Controller.close_all()
         # thread kapanmasını bekle

        event.accept()  # pencerenin kapanmasına izin ver
