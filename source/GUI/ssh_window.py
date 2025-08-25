
import sys,time

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal , pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QTableWidgetItem,QSizePolicy
from PyQt5.QtGui import QTextCursor, QPixmap
import paramiko

from QTDesigns.sshController import Ui_MainWindow_ssh
from QTDesigns.sshClient_summaryi import Ui_Dialog as ui_sshClient_summry
from QTDesigns.sshClient import Ui_MainWindow as ui_SSClientWindow



from source.Iperf.iperf_TestResult_Wrapper import TestResult_Wrapper_sub
from source.ssH.Client_Controller import Client_Controller, ClientWrapper
from source.GUI.GUI_graph_iperf import GraphWindow_iperf

class SSHClient(QMainWindow):
    def __init__(self,testResultWrapper:TestResult_Wrapper_sub,hostname,clientWrapper:ClientWrapper,user,parent =None ):
        super().__init__(parent)
        self.ui = ui_SSClientWindow()
        self.ui.setupUi(self)
        self.hostname = hostname
        self.testResultWrapper = testResultWrapper
        
        self.clientWrapper = clientWrapper
       
        if self.clientWrapper.os_type == "windows":
            self.ui.label_image.setPixmap(QPixmap(":/images/windowslogo.png"))
        
        self.ui.lineEdit_username.setText(user)
        self.ui.lineEdit_hostname.setText(hostname)
        if self.clientWrapper.os_type == "windows":
            self.ui.pushButton_iperf.setDisabled(True)
            self.ui.tabWidget.setTabVisible(1,False)

        self.ui.pushButton_openGraph.clicked.connect(self.open_graph_menu)
        self.ui.tabWidget.setTabVisible(0,False)
        self.ui.pushButton_liveShell.setDisabled(True)
        self.ui.pushButton_iperf.clicked.connect(self.open_iperf_menu)
        self.ui.pushButton_ping.clicked.connect(self.open_ping_menu)

        """self.stats_timer = QTimer(self)
        self.stats_timer.setInterval(100)  # 1000ms = 1 saniye#60fps için girilen değr
        self.stats_timer.timeout.connect(self.update_plaintext)
        self.stats_timer.start()"""

    def open_graph_menu(self):
        """
        'Grafikler' için küçük bir açılır menü (QMenu) gösterir.
        Butona basıldığında, butonun hemen altında iki seçenek sunulur:
        'iPerf Graph' ve 'Ping Graph'.
        """
        menu = QtWidgets.QMenu(self)

        act_iperf = menu.addAction("iPerf Graph")
        

        # OS 'windows' ise iPerf'i devre dışı bırak (senin mevcut mantığına uygun)
        if getattr(self.clientWrapper, "os_type", "").lower() == "windows":
            act_iperf.setEnabled(False)

        act_iperf.triggered.connect(self.show_iperf_graph)
        

        btn = self.ui.pushButton_openGraph
        pos = btn.mapToGlobal(btn.rect().bottomLeft())
        menu.exec_(pos)
    def show_iperf_graph(self):
        self.testResultWrapper.start()
        print(f"[ssh_window show iperf içi] {self.testResultWrapper.local_ip}   ")        
        self.window = GraphWindow_iperf(self.testResultWrapper)
        
        self.window.setWindowFlags(Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        self.window.show()
    def open_ping_menu(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(f"Ping Ayarları - {self.hostname}")
        dialog.setFixedSize(420, 360)

        layout = QtWidgets.QVBoxLayout(dialog)

        form = QtWidgets.QFormLayout()

        # Hedef
        self.ping_target_input = QtWidgets.QLineEdit()
        self.ping_target_input.setPlaceholderText("örn: 8.8.8.8 veya example.com")
        form.addRow("Hedef:", self.ping_target_input)

        # Sayım (count)
        self.ping_count_input = QtWidgets.QSpinBox()
        self.ping_count_input.setRange(0, 10_000)  # 0 => None olarak geçer (süresiz)
        self.ping_count_input.setValue(4)
        form.addRow("Paket sayısı (-c):", self.ping_count_input)

        # Aralık (interval, float)
        self.ping_interval_input = QtWidgets.QSpinBox()
        #self.ping_interval_input.setDecimals(2)
        self.ping_interval_input.setRange(1, 100)
        self.ping_interval_input.setSingleStep(1)
        self.ping_interval_input.setValue(1)
        form.addRow("Aralık sn (-i):", self.ping_interval_input)

        # Zaman aşımı (timeout)
        self.ping_timeout_input = QtWidgets.QSpinBox()
        self.ping_timeout_input.setRange(0, 86_400)
        self.ping_timeout_input.setValue(5)
        form.addRow("Zaman aşımı sn (-w):", self.ping_timeout_input)

        # Boyut (size)
        self.ping_size_input = QtWidgets.QSpinBox()
        self.ping_size_input.setRange(0, 65_507)
        self.ping_size_input.setValue(0)  # 0 => None olarak geçer
        form.addRow("Boyut bayt (-s):", self.ping_size_input)

        # TTL
        self.ping_ttl_input = QtWidgets.QSpinBox()
        self.ping_ttl_input.setRange(0, 255)  # 0 => None olarak geçer
        self.ping_ttl_input.setValue(0)
        form.addRow("TTL (-t):", self.ping_ttl_input)

        # IPv6 / DF / extra
        self.ping_ipv6_chk = QtWidgets.QCheckBox("IPv6 ile (ping6)")
        self.ping_df_chk = QtWidgets.QCheckBox("DF (do not fragment) (-M do)")
        self.ping_extra_input = QtWidgets.QLineEdit()
        self.ping_extra_input.setPlaceholderText("Ek parametreler (opsiyonel)")

        form.addRow(self.ping_ipv6_chk)
        form.addRow(self.ping_df_chk)
        form.addRow("Ek parametre:", self.ping_extra_input)

        layout.addLayout(form)

        # Butonlar
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(lambda: self.run_ping(dialog))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.setLayout(layout)
        dialog.exec_()

    def run_ping(self, dialog: QtWidgets.QDialog):
        
            target = self.ping_target_input.text().strip()
            if not target:
                QtWidgets.QMessageBox.warning(self, "Uyarı", "Hedef (target) boş olamaz.")
                return

            # 0 veya boş değerleri None'a çeviren yardımcılar
            def none_if_zero(v): return None if (v is None or int(v) == 0) else int(v)
            def none_if_empty(s): 
                s = (s or "").strip()
                return s if s else None
            def float_none_if_zero(v):
                v = float(v)
                return None if v == 0.0 else v

            params = {
                "target": target,
                "count": none_if_zero(self.ping_count_input.value()),
                "interval": int(self.ping_interval_input.value()),
                "timeout": none_if_zero(self.ping_timeout_input.value()),
                "size": none_if_zero(self.ping_size_input.value()),
                "ipv6": self.ping_ipv6_chk.isChecked(),
                "do_not_fragment": self.ping_df_chk.isChecked(),
                "ttl": none_if_zero(self.ping_ttl_input.value()),
                "extra": none_if_empty(self.ping_extra_input.text()),
            }

            # Burada setPing'i çağırıyoruz (senin sağladığın metoda göre)
            # Örn: self.clientWrapper.commandBuilder.setPing(**params) gibi
            # Ben doğrudan self.setPing’i çağırıyorum; projende neredeyse orayı kullan.
            if not self.clientWrapper:
                print("SSH bağlantısı bulunamadı")

            stdobject = self.clientWrapper.ping_on_remote(**params)
            stdobject.stdout_chunk.connect(self.openPingTab)
           
            
        

            

        
    @pyqtSlot(str,str)
    def openPingTab(self,name,data):
        if name !="ping":
            return
        
        tab_widget = self.ui.tabWidget  

        # Daha önce "Ping" sekmesi eklenmiş mi kontrol et
        existing_index = None
        for i in range(tab_widget.count()):
            if tab_widget.tabText(i).lower() == "ping":
                existing_index = i
                break

        if existing_index is not None:# varsa
           
            self.ping_target_plain.appendPlainText(data)

            # İmleci sona taşı ve görünür kıl (otomatik alt kaydırma)
            cursor = self.ping_target_plain.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.ping_target_plain.setTextCursor(cursor)
            self.ping_target_plain.ensureCursorVisible()
            return
        else:#yoksa
            # Yeni sekme oluştur
            ping_tab = QtWidgets.QWidget()
            main_layout = QtWidgets.QVBoxLayout(ping_tab)

            # Üst kısım: parametre formu
            form_layout = QtWidgets.QFormLayout()

            # Hedef giriş alanı (PlainText)
            self.ping_target_plain = QtWidgets.QPlainTextEdit()
            
            self.ping_target_plain.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.ping_target_plain.appendPlainText(data)

            # Layout’a ekle
            
            main_layout.addWidget(self.ping_target_plain)
            main_layout.addLayout(form_layout)           
            
            

            # Sekmeyi ekle ve göster
            tab_widget.addTab(ping_tab, "Ping")
            tab_widget.setCurrentWidget(ping_tab)


            

            # İmleci sona taşı ve görünür kıl (otomatik alt kaydırma)
                
    def open_iperf_menu(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle(f"iPerf Ayarları - {self.hostname}")
        dialog.setFixedSize(400, 300)

        layout = QtWidgets.QVBoxLayout()

        # Rol seçimi
        role_group = QtWidgets.QGroupBox("Rol")
        role_layout = QtWidgets.QHBoxLayout()
        self.role_client = QtWidgets.QRadioButton("Client")
        self.role_server = QtWidgets.QRadioButton("Server")
        self.role_client.setChecked(True)
        role_layout.addWidget(self.role_client)
        role_layout.addWidget(self.role_server)
        role_group.setLayout(role_layout)

        # Parametre inputları
        form_layout = QtWidgets.QFormLayout()

        # Satır oluşturucu (Label + Input birlikte)
        def make_row(label_text, widget):
            container = QtWidgets.QWidget()
            hbox = QtWidgets.QHBoxLayout(container)
            hbox.setContentsMargins(0, 0, 0, 0)

            label = QtWidgets.QLabel(label_text)
            hbox.addWidget(label)
            hbox.addWidget(widget)
            hbox.addStretch()

            form_layout.addRow(container)
            return container

        self.target_server_input = QtWidgets.QLineEdit()
        self.target_server_input.setPlaceholderText("Hedef Sunucu (client modu için)")
        self.port_input = QtWidgets.QLineEdit("5201")
        self.duration_input = QtWidgets.QLineEdit("10")
        self.protocol_combo = QtWidgets.QComboBox()
        self.protocol_combo.addItems(["tcp", "udp"])
        self.parallel_streams_input = QtWidgets.QLineEdit("1")
        self.bandwidth_input = QtWidgets.QLineEdit("1M")
        self.reverse_checkbox = QtWidgets.QCheckBox("Ters Yönde Test (Server->Client)")

        # Satır konteynerleri
        row_target = make_row("Hedef Sunucu:", self.target_server_input)
        row_port = make_row("Port:", self.port_input)
        row_duration = make_row("Süre (sn):", self.duration_input)
        row_proto = make_row("Protokol:", self.protocol_combo)
        row_parallel = make_row("Paralel Akış:", self.parallel_streams_input)
        row_bw = make_row("Bant Genişliği:", self.bandwidth_input)
        row_reverse = make_row("", self.reverse_checkbox)

        # Sadece client modunda görünenler
        self.client_rows = [row_target, row_duration, row_proto, row_parallel, row_bw, row_reverse]

        # Client/Server seçimine göre göster/gizle
        def toggle_client_widgets():
            is_client = self.role_client.isChecked()
            for row in self.client_rows:
                row.setVisible(is_client)

        self.role_client.toggled.connect(toggle_client_widgets)
        self.role_server.toggled.connect(toggle_client_widgets)
        toggle_client_widgets()

        # Butonlar
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.run_iperf(dialog))
        button_box.rejected.connect(dialog.reject)

        layout.addWidget(role_group)
        layout.addLayout(form_layout)
        layout.addWidget(button_box)
        dialog.setLayout(layout)

        dialog.exec_()
    def run_iperf(self, dialog):
        try:
       
            # Parametreleri topla
            role = "server" if self.role_server.isChecked() else "client"
            
            params = {
                'role': role,
                'server': self.target_server_input.text().strip() if role == "client" else None,
                'port': int(self.port_input.text()) if self.port_input.text() else None,
                'duration': int(self.duration_input.text()) if self.duration_input.text() else None,
                'parallel': int(self.parallel_streams_input.text()) if self.parallel_streams_input.text() else None,
                'reverse': self.reverse_checkbox.isChecked(),
                'udp': self.protocol_combo.currentText() == "udp",
                'bandwidth': self.bandwidth_input.text().strip() if self.bandwidth_input.text() else None
            }
            
            
            # ClientWrapper'dan CommandExecutor'ı al
            if not self.clientWrapper:
                print("SSH bağlantısı bulunamadı")
            print(f"[STDOUT öncesi ]     --------------")
            self.clientWrapper.open_iperf3(**params).stdout_chunk.connect(self.update_plaintext)
            stdout,stderr = self.clientWrapper.stdobject.get_sdt_outErr("iperf")

            print(f"[ssh_window    run_iperf içi]     {stdout.getvalue()}")
            self.testResultWrapper.set_std_outERR(stdout=stdout,stderr=stderr)
            
        except Exception as e:
             QtWidgets.QMessageBox.warning(self, "Uyarı", str(e))

    @pyqtSlot(str,str)
    def update_plaintext(self,name:str , data:str):
        if name !="iperf":# stdout_chunk sinyallerinden sadece iperf olan gelsin
            return
        
        
        self.ui.plainTextEdit_iperf.appendPlainText(data)

        # İmleci sona taşı ve görünür kıl (otomatik alt kaydırma)
        cursor = self.ui.plainTextEdit_iperf.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.ui.plainTextEdit_iperf.setTextCursor(cursor)
        self.ui.plainTextEdit_iperf.ensureCursorVisible()
        
        
            
class StatusWorker(QtCore.QObject):# her client_widget summary'nin client bağlantısını kontrol eden qthread
    tick = pyqtSignal()
    def __init__(self):
        super().__init__()
        self._running = True
    def start(self):
        while self._running:
            self.tick.emit()           # UI slot’u tetikler
            QtCore.QThread.sleep(2)
    def stop(self):
        self._running = False       

# bu SSH_client window içindeki scroll area da gösterilecek olan widget
class ClientWidget_summary(QtWidgets.QWidget):
    delete_requested = pyqtSignal(str)  # Signal to emit when deletion is requested
    def __init__(self, hostname, username, port, parent=None,clientWrapper:ClientWrapper=None):
        super().__init__(parent)
        self.hostname = hostname
        self.username = username
        self.clientWrapper = clientWrapper
        self.testResultWrapper = TestResult_Wrapper_sub(self.hostname)

        print(f"[client summary] clientwrapper { self.clientWrapper}")
        self.port = port
        self.ui = ui_sshClient_summry()
        self.ui.setupUi(self)

        if self.clientWrapper.os_type == "windows":           
            self.ui.label.setPixmap(QPixmap(":icons/windowslogo.png"))

        self.ui.lineEdit_hostname.setText(self.hostname)
        self.ui.lineEdit_username.setText(self.username)

        self.ui.label_status = QtWidgets.QLabel("🔴 Bağlı Değil")
        self.ui.horizontalLayout.addWidget(self.ui.label_status)

        self.ui.pushButton_more.clicked.connect(self.open_sshClient)
        self.ui.pushButton_close.clicked.connect(self.delete)
        self.update_connection_status()
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,  # Yatayda genişleyebilir
            QtWidgets.QSizePolicy.Fixed       # Dikeyde sabit boyut
        )
        
        #self.setMinimumHeight()  # Sabit bir yükseklik belirle
        self._thread = QtCore.QThread(self)
        self._worker = StatusWorker()
        self._worker.moveToThread(self._thread)
        self._worker.tick.connect(self.update_connection_status)
        self._thread.started.connect(self._worker.start)
        self._thread.start()
        self.destroyed.connect(self._cleanup_thread)
        
    def _cleanup_thread(self):
        try:
            self._worker.stop()
            self._thread.quit()
            self._thread.wait()
        except Exception:
            pass

    def delete(self):
        self._cleanup_thread()
        self.testResultWrapper.stop()
        self.delete_requested.emit(self.hostname)  # Emit signal before actual deletion
        client_controller.remove_client(self.hostname)
        self.deleteLater()  # Schedule widget for deletion
    def _status_loop(self):
        while self.clientWrapper:
            self.update_connection_status()

            time.sleep(2)  # ✅ burada kullanmak güvenli
    def update_connection_status(self):
        try:
            client = self.clientWrapper
            if client.is_connected():
                self.ui.label_status.setText("🟢 Bağlı")
                self.ui.label_status.setStyleSheet("color: green;")
            else:
                self.ui.label_status.setText("🔴 Bağlı Değil")
        except:
            if self.clientWrapper:
                self.ui.label_status.setText("⚪ Client Yok")
    def open_sshClient(self):
        self.window = SSHClient(self.testResultWrapper,hostname=self.hostname, user=self.username, clientWrapper=self.clientWrapper)
        self.window.show()

        
client_controller = Client_Controller()
class SSH_Client_Window(QMainWindow):
    

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        print(f"[SSH_Client_window]    init edildi")
        global client_controller
        self.mainwindow = parent
        self.ui = Ui_MainWindow_ssh()
        self.ui.setupUi(self)  
        self.setWindowFlags((Qt.Window | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint))
        self.clientWidgets = []
         # Scroll Area için layout oluştur
        self.scroll_layout = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)
        self.ui.scrollAreaWidgetContents.setLayout(self.scroll_layout)

        self.ui.pushButton_add.clicked.connect(self.createClient)


        client_controller = Client_Controller(self.mainwindow)

        
    def createClient(self):
        hostName = self.ui.lineEdit_ip.text().strip()
        username = self.ui.lineEdit_username.text().strip()
        password = self.ui.lineEdit_password.text().strip()
        port = int(self.ui.lineEdit_port.text().strip())

        # Aynı hostname ile client var mı kontrol et
        if hostName in client_controller.list_clients():
            QtWidgets.QMessageBox.warning(self, "Uyarı", 
                f"{hostName} zaten eklenmiş!")
            return

        #try:
        client_controller.add_client(hostname=hostName, username=username, 
                                password=password, port=port)
        client_wrapper = client_controller.get_client(hostName)
        print(f"[createClient] client_wrapper  {client_wrapper}")
        # Bağlantı thread'i oluştur
        self.connection_thread = self.ConnectionThread(client_wrapper)
        self.connection_thread.connection_result.connect(self.handle_connection_result)
        self.connection_thread.start()
        
        QtWidgets.QMessageBox.information(self, "Bilgi", 
            f"{hostName} için bağlantı deneniyor...")
            
        """except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Hata", 
                f"İstemci oluşturulamadı: {str(e)}")
            if hostName in client_controller.list_clients():
                client_controller.remove_client(hostName)"""

    def handle_connection_result(self,clientWrapper:ClientWrapper ,success, hostname, username, error_msg):
        print(f"[handle connection thread] client_wrapper  {clientWrapper}")
        if success:
            # Başarılıysa widget ekle
            self.add_client_widget(hostname, username, clientWrapper=clientWrapper)
            QtWidgets.QMessageBox.information(self, "Başarılı", 
                f"{hostname} bağlantısı kuruldu. OS: {clientWrapper.os_type}")
        else:
            # Başarısızsa client'ı temizle
            client_controller.remove_client(hostname)
            QtWidgets.QMessageBox.critical(self, "Hata", 
                f"{hostname} bağlantısı başarısız: {error_msg}")
    def remove_client_widget(self, hostname):
        # Find and remove the widget with matching hostname
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget and hasattr(widget, 'hostname') and widget.hostname == hostname:
                widget.setParent(None)  # Remove from layout
                widget.deleteLater()  # Schedule for deletion
                break
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

    def add_client_widget(self ,hostname, username, port=22,clientWrapper:ClientWrapper=None):
        # Yeni bir ClientWidget oluştur
        client_widget = ClientWidget_summary(hostname, username, port,clientWrapper=clientWrapper)
        self.clientWidgets.append(client_widget)
        # Scroll Area'nın layout'una ekle
        self.scroll_layout.addWidget(client_widget)
        
        # Eğer scroll alanı dolduysa kaydırma çubuğunu otomatik aşağı kaydır
        self.ui.scrollArea.verticalScrollBar().setValue(
            self.ui.scrollArea.verticalScrollBar().maximum()
        )

    def update_scrollArea(self):
        pass
    def pass_scrollLayout(self, clientWindgets):
        if not clientWindgets:
            return

        for w in clientWindgets:
            if w is None:
                continue

            # ScrollArea içeriğine bağla
            if w.parent() is not self.ui.scrollAreaWidgetContents:
                w.setParent(self.ui.scrollAreaWidgetContents)

            # Layout'a ekle
            self.scroll_layout.addWidget(w)

            # İç listeye ekle (tekrar eklememek için basit kontrol)
            if w not in self.clientWidgets:
                self.clientWidgets.append(w)

            # Silme sinyali varsa bağla
            if hasattr(w, "delete_requested"):
                try:
                    w.delete_requested.connect(self.remove_client_widget)
                except TypeError:
                    pass

        # Scroll'u alta indir
        self.ui.scrollArea.verticalScrollBar().setValue(
            self.ui.scrollArea.verticalScrollBar().maximum()
        )
    def get_clientController(self):# şimdilik scroll layout döndürür
        global client_controller
        return self.clientWidgets
def main():
    app = QApplication(sys.argv)
    window = SSH_Client_Window()
    window.show()
    sys.exit(app.exec())
if __name__ =="__main__":
    main()