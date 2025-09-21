import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore

# Custom ViewBox
class CustomViewBox(pg.ViewBox):
    def __init__(self, *args, **kwds):
        kwds['enableMenu'] = False
        super().__init__(*args, **kwds)
        self.setMouseMode(self.RectMode)
    
    def mouseClickEvent(self, ev):
        if ev.button() == QtCore.Qt.MouseButton.RightButton:
            self.autoRange()
    
    def mouseDragEvent(self, ev, axis=None):
        if axis is not None and ev.button() == QtCore.Qt.MouseButton.RightButton:
            ev.ignore()
        else:
            super().mouseDragEvent(ev, axis=axis)

class GraphWindow(QDialog):
    def __init__(self, stat_obj, parent=None):
        super().__init__(parent)
        
        self.stat_obj = stat_obj
        self.rttlist = stat_obj._rttList
        self.timeStamp = stat_obj._timeStamp_for_rttList
        
        # Önceki durumu takip etmek için değişkenler
        self.last_data_length = 0
        self.last_timeout_value = stat_obj.timeOut

        self.setWindowTitle("RTT Graph for " + self.stat_obj.target)
        self.resize(800, 400)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Pyqtgraph plot widget
        axis = pg.DateAxisItem(orientation='bottom')
        vb = CustomViewBox()
        self.plot_widget = pg.PlotWidget(viewBox=vb, axisItems={'bottom': axis}, enableMenu=False)
        self.plot_widget.setLabel('left', 'RTT (ms)')
        self.plot_widget.setLabel('bottom', 'Time')
        layout.addWidget(self.plot_widget)

        # Çizgi için ayrı bir plot (tüm noktaları birleştiren)
        self.line_plot = self.plot_widget.plot([], [], pen='g', name="RTT Trend")
        
        # Noktalar için plot (renkli noktalar)
        self.points_plot = self.plot_widget.plot([], [], symbol='o', pen=None, symbolBrush=[], symbolSize=8)
        
        # Verileri önbellekleme
        self.cached_times = np.array([])
        self.cached_values = np.array([])
        self.cached_colors = np.array([])
        
        # QTimer ile otomatik güncelleme
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(2000)  #TODO settingsen değiştirilebilir belki 1 saniyede bir güncelle

        self.update_plot()  # İlk çizim

    def update_plot(self):
        # Sadece yeni veri eklendiyse güncelle
        if len(self.rttlist) != self.last_data_length or self.last_timeout_value != self.stat_obj.timeOut:
            self.last_data_length = len(self.rttlist)
            self.last_timeout_value = self.stat_obj.timeOut
            
            # Yalnızca yeni eklenen verileri işle
            start_idx = len(self.cached_times)
            
            # Eğer timeout değeri değiştiyse tüm renkleri yeniden hesapla
            if self.last_timeout_value != self.stat_obj.timeOut:
                start_idx = 0
            
            # Yeni verileri ekle
            new_times = []
            new_values = []
            new_colors = []
            
            for i in range(start_idx, len(self.rttlist)):
                new_times.append(self.timeStamp[i])
                
                if self.rttlist[i] is not None:
                    new_values.append(self.rttlist[i])
                    new_colors.append('b')  # Mavi - geçerli RTT
                else:
                    new_values.append(self.stat_obj.timeOut)
                    new_colors.append('r')  # Kırmızı - timeout
            
            if start_idx == 0:
                # Tüm verileri yeniden oluştur
                self.cached_times = np.array(new_times)
                self.cached_values = np.array(new_values)
                self.cached_colors = np.array(new_colors)
            else:
                # Yalnızca yeni verileri ekle
                self.cached_times = np.concatenate((self.cached_times, new_times))
                self.cached_values = np.concatenate((self.cached_values, new_values))
                self.cached_colors = np.concatenate((self.cached_colors, new_colors))
            
            # Grafiği güncelle
            self.line_plot.setData(self.cached_times, self.cached_values)
            self.points_plot.setData(self.cached_times, self.cached_values, symbolBrush=self.cached_colors)

    def closeEvent(self, e):
        # Timer güvenli kapatma
        if self.timer and self.timer.isActive():
            self.timer.stop()
            try:
                self.timer.timeout.disconnect(self.update_plot)
            except TypeError:
                pass  # zaten kopuk olabilir

        self.deleteLater()
        return super().closeEvent(e)