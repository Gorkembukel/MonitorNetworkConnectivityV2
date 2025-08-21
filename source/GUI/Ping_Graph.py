from PyQt5.QtWidgets import QDialog, QVBoxLayout,QWidget
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from QTDesigns.graph_window import Ui_Dialog_graphWindow
import time
from pyqtgraph import DateAxisItem  


class GraphWindow(QDialog):
    def __init__(self, stat_obj, parent=None):
        super().__init__(parent)
        self.ui = Ui_Dialog_graphWindow()
        self.ui.setupUi(self)
        self.stat_obj = stat_obj

        self.plot_refs = {}  # güncelleme için sakla

        self.setup_tabs()

        # Timer ile canlı güncelleme
        from PyQt5.QtCore import QTimer
        self.timer = QTimer(self)
        self.timer.setInterval(100)#60fps için 17 ms
        self.timer.timeout.connect(self.update_plots)
        self.timer.start()


        #grafik optimizasyonu için 
        self._last_len = -1

    def setup_tabs(self):
        # 1️⃣ RTT → tab
        
        """axis = DateAxisItem(orientation='bottom',utcOffset=3)
        rtt_plot = PlotWidget(axisItems={'bottom': axis})  # 
        rtt_plot.setTitle(f"RTT for {self.stat_obj.target}")  # ⬅ stat_obj çünkü GraphWindow sınıfındasın

        curve = self.stat_obj.get_rtt_curve()
        rtt_plot.addItem(curve)
        """
        axis = DateAxisItem(orientation='bottom', utcOffset=3)
        rtt_plot = PlotWidget(axisItems={'bottom': axis})
        rtt_plot.setTitle(f"RTT for {self.stat_obj.target}")

        curve = pg.PlotDataItem(pen='b', symbol='o', symbolSize=8)
        rtt_plot.setClipToView(True)
        rtt_plot.addItem(curve)

        
        layout1 = QVBoxLayout()
        layout1.addWidget(rtt_plot)
        self.ui.tab.setLayout(layout1)
        self.plot_refs['rtt'] = curve

      

       
      

    def update_plots(self):
        """if 'rtt' in self.plot_refs:        
            data = self.stat_obj.get_time_series_data()  # (timestamp, rtt) listesi
            if data:
                x, y = zip(*data)
                
                self.plot_refs['rtt'].setData(x, y)"""
        if 'rtt' in self.plot_refs:
            cur_len = self.stat_obj.get_plot_len()
            if cur_len != self._last_len:  # sadece yeni veri varsa çiz
                x, y, brushes, pens = self.stat_obj.get_plot_arrays()
                self.plot_refs['rtt'].setData(
                    x=x, y=y,
                    symbolBrush=brushes,
                    symbolPen=pens
                )
            self._last_len = cur_len
    def closeEvent(self, e):
        # Timer güvenli kapatma
        if self.timer and self.timer.isActive():
            self.timer.stop()
            try:
                self.timer.timeout.disconnect(self.update_plots)
            except TypeError:
                pass  # zaten kopuk olabilir

        # Plot referanslarını da bırak (GC’ye yardım)
        for k, it in getattr(self, "plot_refs", {}).items():
            try:
                it.clear()
            except Exception:
                pass
        self.plot_refs.clear()

      

        self.deleteLater()  # gerçekten yok et
        return super().closeEvent(e)