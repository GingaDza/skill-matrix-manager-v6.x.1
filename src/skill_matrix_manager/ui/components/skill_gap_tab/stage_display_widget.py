"""段階表示ウィジェット - 段階別目標値の視覚的表示"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGridLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class StageDisplayWidget(QWidget):
    """段階の目標表示用ウィジェット"""
    
    def __init__(self, stage_data, parent=None):
        super().__init__(parent)
        self.stage_data = stage_data
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # 期間表示
        period_text = f"{self.stage_data['time']}{self.stage_data['unit']}後の目標"
        period_label = QLabel(period_text)
        period_label.setAlignment(Qt.AlignCenter)
        period_label.setStyleSheet("font-weight: bold; color: #1976D2;")
        layout.addWidget(period_label)
        
        # スキルレベル表示
        skills_grid = QGridLayout()
        skills_grid.setColumnStretch(1, 1)  # レベル列を伸縮可能に
        
        # ヘッダー
        skills_grid.addWidget(QLabel("スキル"), 0, 0)
        skills_grid.addWidget(QLabel("レベル"), 0, 1)
        
        # スキルデータ
        if 'targets' in self.stage_data:
            for row, (skill, level) in enumerate(self.stage_data['targets'].items(), start=1):
                skills_grid.addWidget(QLabel(skill), row, 0)
                level_label = QLabel(str(level))
                level_label.setAlignment(Qt.AlignCenter)
                
                # レベルに応じた色設定
                if level >= 4:
                    level_label.setStyleSheet("color: #388E3C; font-weight: bold;")  # 緑
                elif level >= 3:
                    level_label.setStyleSheet("color: #1976D2; font-weight: bold;")  # 青
                elif level >= 2:
                    level_label.setStyleSheet("color: #FFA000;")  # オレンジ
                else:
                    level_label.setStyleSheet("color: #D32F2F;")  # 赤
                    
                skills_grid.addWidget(level_label, row, 1)
            
        layout.addLayout(skills_grid)
        self.setLayout(layout)
        
        # スタイル設定
        self.setStyleSheet("""
            QWidget {
                background-color: #F5F5F5;
                border: 1px solid #BDBDBD;
                border-radius: 5px;
                padding: 8px;
            }
        """)
        self.setMinimumWidth(180)
        self.setMaximumWidth(250)
