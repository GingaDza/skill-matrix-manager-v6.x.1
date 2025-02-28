#!/usr/bin/env python3
"""レーダーチャートダイアログ"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTableWidget, 
                           QPushButton, QLabel, QTabWidget, QWidget, QTableWidgetItem)
from PyQt5.QtCore import Qt

from .radar_chart import RadarChart
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class RadarChartDialog(QDialog):
    """レーダーチャート表示ダイアログ"""
    
    def __init__(self, parent=None, stages_data=None):
        """初期化"""
        super().__init__(parent, Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle("スキルレーダーチャート")
        self.setMinimumSize(700, 500)
        
        # データ
        self.stages_data = stages_data or []
        
        # UI
        self.setup_ui()
        
        # データ表示
        if self.stages_data:
            self.display_stages_data()
        
        logger.info("レーダーチャートダイアログを初期化しました")
    
    def setup_ui(self):
        """UI設定"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 閉じるボタン
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        
        close_btn = QPushButton("閉じる")
        close_btn.setFixedWidth(120)
        close_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
    
    def display_stages_data(self):
        """ステージデータを表示"""
        try:
            # タブをクリア
            self.tab_widget.clear()
            
            # 各ステージごとにタブを作成
            for i, stage_data in enumerate(self.stages_data):
                stage_name = stage_data.get("name", f"第{i+1}段階")
                stage_tab = QWidget()
                
                tab_layout = QHBoxLayout()
                stage_tab.setLayout(tab_layout)
                
                # 左側: レーダーチャート
                radar_chart = RadarChart()
                categories = stage_data.get("categories", [])
                current_values = stage_data.get("current_values", [])
                target_values = stage_data.get("target_values", [])
                
                radar_chart.update_chart(
                    categories, current_values, target_values, 
                    f"スキルギャップ分析 - {stage_name}"
                )
                
                tab_layout.addWidget(radar_chart)
                
                # 右側: データテーブル
                table = QTableWidget()
                table.setColumnCount(3)
                table.setHorizontalHeaderLabels(["スキル", "現在", "目標"])
                
                # データ追加
                row_count = len(categories)
                table.setRowCount(row_count)
                
                for row, (cat, curr, targ) in enumerate(zip(
                    categories, current_values, target_values if target_values else [0]*row_count
                )):
                    # スキル名
                    item = QTableWidgetItem(cat)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, 0, item)
                    
                    # 現在値
                    item = QTableWidgetItem(str(curr))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, 1, item)
                    
                    # 目標値
                    item = QTableWidgetItem(str(targ))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    table.setItem(row, 2, item)
                
                table.resizeColumnsToContents()
                table.resizeRowsToContents()
                
                tab_layout.addWidget(table)
                
                # タブ追加
                self.tab_widget.addTab(stage_tab, stage_name)
            
            logger.info(f"レーダーチャート: {len(self.stages_data)}ステージを表示")
            
        except Exception as e:
            logger.error(f"ステージデータ表示エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
