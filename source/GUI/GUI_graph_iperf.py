from PyQt5.QtWidgets import QDialog, QVBoxLayout,QMainWindow,QSizePolicy
from PyQt5.QtCore import QTimer
from pyqtgraph import PlotWidget, BarGraphItem
import pyqtgraph as pg
import re
from QTDesigns.iperf_result import Ui_MainWindow

from source.Iperf.iperf_TestResult_Wrapper import TestResult_Wrapper_sub

class GraphWindow_iperf(QMainWindow):
    def __init__(self, testResultWrapper_sub:TestResult_Wrapper_sub, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.testResult = testResultWrapper_sub
        self.setWindowTitle(f"Iperf Result for {self.testResult.hostName}")

        self.plot_widget = PlotWidget(self.ui.widget_graph)
        self.plot_widget.setMinimumWidth(700)
        #self.plot_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        #self.ui.dockWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.setup_graph_area()

        # Tek eğrileri sakla
        self.curve_all = None
        self.curve_sender = None
        self.curve_receiver = None

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_graph_live)
        self.timer.start()

    def setup_graph_area(self):
        if not self.ui.widget_graph.layout():
            layout = QVBoxLayout(self.ui.widget_graph)
        else:
            layout = self.ui.widget_graph.layout()
            for i in reversed(range(layout.count())):
                w = layout.itemAt(i).widget()
                if w:
                    w.setParent(None)

        self.plot_widget.setLabel('bottom', 'Stream #')
        self.plot_widget.setLabel('left', 'Bitrate (Mbps)')
        self.plot_widget.setTitle(f"Bitrate per Stream: {self.testResult.hostName}")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.addLegend(offset=(10, 10))
        layout.addWidget(self.plot_widget)

    def _bps_from_bitrate(self, bitrate: str) -> float:
        # "26.6 Gbits/sec" -> bps
        m = re.search(r'([\d\.]+)\s+([KMG]?bits)/sec', bitrate or '')
        if not m:
            return 0.0
        val, unit = m.groups()
        mult = {'bits': 1, 'Kbits': 1e3, 'Mbits': 1e6, 'Gbits': 1e9}
        return float(val) * mult.get(unit, 1)

    def _to_mbps(self, bps: float) -> float:
        return bps / 1e6

    def update_graph_live(self):
        # üstteki text kutularını doldur
        
        self.ui.lineEdit_localip.setText(self.testResult.local_ip or "")
        self.ui.lineEdit_localport.setText(self.testResult.local_port or "")
        self.ui.lineEdit_remoteip.setText(self.testResult.remote_ip or "")
        self.ui.lineEdit_remoteport.setText(self.testResult.remote_port or "")

        streams = self.testResult.streams
        if not streams:
            self.plot_widget.setTitle(f"Bitrate per Stream: {self.testResult.hostName} (waiting for data...)")
            return

        # X: 1..N  Y: Mbps
        xs_all, ys_all = [], []
        xs_sender, ys_sender = [], []
        xs_receiver, ys_receiver = [], []

        for idx, s in enumerate(streams, start=1):
            mbps = self._to_mbps(self._bps_from_bitrate(s.bitrate))
            xs_all.append(idx)
            ys_all.append(mbps)

            # cpu metinleri (varsa) güncelle
            if s.local_cpu_percent:
                self.ui.lineEdit_localCpu.setText(s.local_cpu_percent or "")
                self.ui.lineEdit_remotecpu.setText(s.remote_cpu_percent or "")

            if s.stream_type == 'sender':
                xs_sender.append(idx); ys_sender.append(mbps)
            elif s.stream_type == 'receiver':
                xs_receiver.append(idx); ys_receiver.append(mbps)

        # ---- Hepsi (gri çizgi + nokta)
        if self.curve_all is None:
            self.curve_all = self.plot_widget.plot(
                xs_all, ys_all,
                pen=pg.mkPen('gray', width=2),
                symbol='o', symbolSize=6, symbolBrush='gray',
                name='all'
            )
        else:
            self.curve_all.setData(xs_all, ys_all)

        # ---- Sender (yeşil noktalar)
        if self.curve_sender is None:
            self.curve_sender = self.plot_widget.plot(
                xs_sender, ys_sender,
                pen=None,  # sadece scatter
                symbol='o', symbolSize=7, symbolBrush='green',
                name='sender'
            )
        else:
            self.curve_sender.setData(xs_sender, ys_sender)

        # ---- Receiver (mavi noktalar)
        if self.curve_receiver is None:
            self.curve_receiver = self.plot_widget.plot(
                xs_receiver, ys_receiver,
                pen=None,
                symbol='o', symbolSize=7, symbolBrush='blue',
                name='receiver'
            )
        else:
            self.curve_receiver.setData(xs_receiver, ys_receiver)

        # X aralığını 1..N’e oturt
        n = len(streams)
        self.plot_widget.setXRange(1, max(2, n))  # en az 2’ye kadar aç
    def closeEvent(self, event):
        """Pencere kapanırken arka planda hiçbir şey kalmaması için temiz kapatma."""
        self.testResult.stop()

        print(f"[GUI_graph_iperf Close event] kapatılmaya çalışlıyor")
        # 1) Timer'ı durdur ve bağlantıyı kes
        try:
            if hasattr(self, "timer") and self.timer:
                if self.timer.isActive():
                    self.timer.stop()
                try:
                    self.timer.timeout.disconnect(self.update_graph_live)
                except TypeError:
                    pass  # zaten kopuk olabilir
                self.timer.deleteLater()
        except Exception:
            pass

        # 2) Plot'u temizle ve serbest bırak
        try:
            if hasattr(self, "plot_widget") and self.plot_widget:
                try:
                    self.plot_widget.clear()
                except Exception:
                    pass
                # Layout'tan çıkar ve imha et
                self.plot_widget.setParent(None)
                self.plot_widget.deleteLater()
        except Exception:
            pass

        # 3) widget_graph içindeki tüm çocukları sök
        try:
            lay = getattr(self.ui, "widget_graph", None)
            lay = lay.layout() if lay else None
            if lay:
                while lay.count():
                    item = lay.takeAt(0)
                    w = item.widget()
                    if w:
                        w.setParent(None)
                        w.deleteLater()
        except Exception:
            pass

        # 4) (Opsiyonel) UI içindeki lineEdit vb. widget’ları da serbest bırakmak istersen:
        # self.ui = None

        # 5) Üst sınıfın closeEvent'ini çağır
        print(f"[GUI_graph_iperf Close event] kapatıldı")
        super().closeEvent(event)