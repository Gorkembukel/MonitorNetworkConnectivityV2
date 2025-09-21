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

        self.setWindowTitle("Ping RTT vs Time")
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
        self.timer.start(10)  #TODO settingsen değiştirilebilir belki 1 saniyede bir güncelle

        self.update_plot()  # İlk çizim

    def update_plot(self):
        # Sadece yeni veri eklendiyse güncelle
        if len(self.rttlist) != self.last_data_length or self.last_timeout_value != self.stat_obj.timeOut:
            self.last_data_length = len(self.rttlist)
            self.last_timeout_value = self.stat_obj.timeOut
            
            # Tüm verileri işle
            times = []
            values = []
            colors = []
            
            for i in range(len(self.rttlist)):
                times.append(self.timeStamp[i])
                
                if self.rttlist[i] is not None:
                    values.append(self.rttlist[i])
                    colors.append('b')  # Mavi - geçerli RTT
                else:
                    values.append(self.stat_obj.timeOut)
                    colors.append('r')  # Kırmızı - timeout
            
            # Numpy array'lere dönüştür
            times = np.array(times)
            values = np.array(values)
            colors = np.array(colors)
            
            # Sadece veri değiştiyse grafiği güncelle
            if (len(times) != len(self.cached_times) or 
                not np.array_equal(values, self.cached_values) or
                not np.array_equal(colors, self.cached_colors)):
                
                self.cached_times = times
                self.cached_values = values
                self.cached_colors = colors
                
                # Çizgiyi güncelle (tüm noktaları birleştiren)
                self.line_plot.setData(times, values)
                
                # Noktaları güncelle (renkli noktalar)
                self.points_plot.setData(times, values, symbolBrush=colors)

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