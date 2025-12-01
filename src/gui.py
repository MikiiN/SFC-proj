#############################################################################
#
#   file: gui.py
#   author: Michal Zatecka
#   date: 01.12.2025
#
#############################################################################


import collections
from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QPushButton, QSlider, 
                            QGroupBox, QFrame)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from src.fuzzy import fuzzification, defuzzification
from src.simulation import Simulator


class ShowerWindow(QMainWindow):
    def __init__(self, rules):
        super().__init__()
        self.setWindowTitle("Fuzzy Sprcha - Vizualizace")
        self.resize(1000, 800)

        self.sim = Simulator()
        self.hot_valve = 0.5
        self.cold_valve = 0.5
        self.target_temp = 38.0
        self.target_flow = 0.6
        self.rules = rules
        self.running = True
        self.maxlen = 200
        self.data_t = collections.deque([20]*self.maxlen, maxlen=self.maxlen)
        self.data_target_t = collections.deque([38]*self.maxlen, maxlen=self.maxlen)
        self.data_target_f = collections.deque([0.6]*self.maxlen, maxlen=self.maxlen)
        self.data_flow = collections.deque([0]*self.maxlen, maxlen=self.maxlen)
        self.time = 0

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_loop)
        self.timer.start(30)


    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # left panel
        panel = QFrame()
        panel.setFixedWidth(280)
        panel.setStyleSheet("background-color: #f5f5f5; border-right: 1px solid #ddd;")
        vbox = QVBoxLayout(panel)

        lbl = QLabel("OVLÁDÁNÍ")
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setAlignment(Qt.AlignCenter)
        vbox.addWidget(lbl)
        vbox.addSpacing(20)

        # Temperature Control
        gb_temp = QGroupBox("Požadovaná Teplota")
        v_temp = QVBoxLayout()
        self.lbl_val_t = QLabel("38.0 °C")
        self.lbl_val_t.setFont(QFont("Arial", 24, QFont.Bold))
        self.lbl_val_t.setStyleSheet("color: #d32f2f;")
        self.lbl_val_t.setAlignment(Qt.AlignCenter)
        
        slider = QSlider(Qt.Horizontal)
        slider.setRange(20, 60)
        slider.setValue(38)
        slider.valueChanged.connect(self.update_target_temp)
        
        v_temp.addWidget(self.lbl_val_t)
        v_temp.addWidget(slider)
        gb_temp.setLayout(v_temp)
        vbox.addWidget(gb_temp)

        # Flow control
        gb_flow = QGroupBox("Požadovaný Průtok")
        gb_flow.setStyleSheet("QGroupBox { font-weight: bold; border: 1px solid gray; border-radius: 5px; margin-top: 10px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }")
        v_flow = QVBoxLayout()
        
        self.lbl_val_f = QLabel("0.6 l/min")
        self.lbl_val_f.setFont(QFont("Arial", 22, QFont.Bold))
        self.lbl_val_f.setStyleSheet("color: #1976D2;")
        self.lbl_val_f.setAlignment(Qt.AlignCenter)
        
        # flow * 10
        slider_f = QSlider(Qt.Horizontal)
        slider_f.setRange(5, 20)
        slider_f.setValue(6)
        slider_f.valueChanged.connect(self.update_target_flow)
        
        v_flow.addWidget(self.lbl_val_f)
        v_flow.addWidget(slider_f)
        gb_flow.setLayout(v_flow)
        vbox.addWidget(gb_flow)

        vbox.addSpacing(10)

        # 3. Flush (System fault)
        btn_flush = QPushButton("SPLÁCHNOUT")
        btn_flush.setMinimumHeight(50)
        btn_flush.setStyleSheet("background-color: #0048ff; color: white; font-weight: bold; font-size: 14px;")
        btn_flush.clicked.connect(self.sim.init_fault)
        vbox.addWidget(btn_flush)

        vbox.addSpacing(20)
        
        # Reset simulation
        btn_reset = QPushButton("RESET SIMULACE")
        btn_reset.clicked.connect(self.reset_sim)
        vbox.addWidget(btn_reset)

        layout.addWidget(panel)

        # right panel with graphs
        self.canvas = FigureCanvas(Figure(figsize=(5, 5)))
        self.ax1 = self.canvas.figure.add_subplot(211)
        self.ax2 = self.canvas.figure.add_subplot(212)
        # temperature graph
        self.ax1.set_title("Teplota vody (°C)")
        self.ax1.set_ylim(10, 80)
        self.ax1.grid(True, linestyle='--', alpha=0.6)
        self.line_t, = self.ax1.plot([], [], 'r-', lw=2, label="Aktuální")
        self.line_target_t, = self.ax1.plot([], [], 'g--', lw=1.5, label="Cíl")
        self.ax1.legend(loc="upper right")

        # flow graph
        self.ax2.set_title("Průtok (l/min)")
        self.ax2.set_ylim(-0.5, 2.5)
        self.ax2.grid(True, linestyle='--', alpha=0.6)
        self.line_f, = self.ax2.plot([], [], 'b-', lw=2, label="Aktuální")
        self.line_target_f, = self.ax2.plot([], [], 'g--', lw=1.5, label="Cíl")
        self.ax2.legend(loc="upper right")
        
        self.canvas.figure.tight_layout()
        layout.addWidget(self.canvas)


    def update_target_temp(self, value):
        self.target_temp = float(value)
        self.lbl_val_t.setText(f"{value:.1f} °C")

    
    def update_target_flow(self, value):
        real_val = value / 10.0
        self.target_flow = real_val
        self.lbl_val_f.setText(f"{real_val:.1f} l/min")


    def reset_sim(self):
        self.sim = Simulator()
        self.time = 0
        self.hot_valve = 0.5
        self.cold_valve = 0.5


    def update_loop(self):
        if not self.running: return

        current_flow, current_temp = self.sim.step(self.time, self.hot_valve, self.cold_valve)
        
        # Fuzzy control
        err_temp = current_temp - self.target_temp
        err_flow = current_flow - self.target_flow
        hot_change, cold_change = fuzzification(err_temp, err_flow, rules=self.rules)
        
        self.hot_valve += defuzzification(hot_change)
        self.cold_valve += defuzzification(cold_change)
        self.time += 1
        
        # Data update
        self.data_t.append(current_temp)
        self.data_target_t.append(self.target_temp)
        self.data_flow.append(current_flow)
        self.data_target_f.append(self.target_flow)
        
        # plot
        x = range(len(self.data_t))
        
        self.line_t.set_data(x, self.data_t)
        self.line_target_t.set_data(x, self.data_target_t)
        
        self.line_f.set_data(x, self.data_flow)
        self.line_target_f.set_data(x, self.data_target_f)
        
        self.ax1.set_xlim(0, len(self.data_t))
        self.ax2.set_xlim(0, len(self.data_t))
        self.canvas.draw_idle()