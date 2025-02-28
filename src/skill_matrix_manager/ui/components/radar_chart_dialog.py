#!/usr/bin/env python3
"""レーダーチャートダイアログ"""

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
from src.skill_matrix_manager.ui.components.charts.radar_chart import RadarChart
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class RadarChartDialog(QDialog):
    """レーダーチャート表示ダイアログ"""
    
    def __init__(self, parent=None, categories=None, current_values=None, target_values=None, title=None):
        super().__init__(parent)
        
        # ウィンドウ設定
        self.setWindowTitle("スキルレーダーチャート")
        self.setMinimumSize(600, 500)
        
        # レイアウト
        layout = QVBoxLayout(self)
        
        # タイトル
        if title:
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(title_label)
        
        # レーダーチャート
        self.radar_chart = RadarChart(self, width=6, height=5)
        layout.addWidget(self.radar_chart)
        
        # 閉じるボタン
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # データを設定
        if categories and current_values:
            self.update_chart(categories, current_values, target_values, title)
    
    def update_chart(self, categories, current_values, target_values=None, title=None):
        """チャートデータの更新"""
        self.radar_chart.update_chart(categories, current_values, target_values, title)
