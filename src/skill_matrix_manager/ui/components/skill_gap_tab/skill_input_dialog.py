"""スキル入力ダイアログ"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QSpinBox
)
from PyQt5.QtCore import Qt
import logging

# 絶対インポートを使用
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent.parent))
from skill_matrix_manager.models.skill_data import SkillData

logger = logging.getLogger(__name__)

class SkillInputDialog(QDialog):
    """スキル入力ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.skill_data = SkillData()  # シングルトンインスタンスを取得
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期設定"""
        self.setWindowTitle("スキル目標レベル設定")
        self.setMinimumSize(600, 400)
        
        # メインレイアウト
        layout = QVBoxLayout(self)
        
        # 説明ラベル
        info_label = QLabel("各スキルの目標レベルを設定してください。")
        layout.addWidget(info_label)
        
        # スキルテーブル
        self.skill_table = QTableWidget()
        self.skill_table.setColumnCount(3)
        self.skill_table.setHorizontalHeaderLabels(["スキル名", "現在レベル", "目標レベル"])
        self.skill_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.skill_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.skill_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        layout.addWidget(self.skill_table)
        
        # ボタンエリア
        btn_layout = QHBoxLayout()
        self.cancel_btn = QPushButton("キャンセル")
        self.save_btn = QPushButton("保存")
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white;")
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.save_btn)
        layout.addLayout(btn_layout)
        
        # シグナル接続
        self.cancel_btn.clicked.connect(self.reject)
        self.save_btn.clicked.connect(self.save_and_close)
        
        # テーブル初期化
        self.populate_table()
    
    def populate_table(self):
        """テーブルにスキルデータを表示"""
        skills = self.skill_data.get_skills()
        self.skill_table.setRowCount(len(skills))
        
        for i, (skill_id, data) in enumerate(skills.items()):
            # スキル名
            self.skill_table.setItem(i, 0, QTableWidgetItem(data["name"]))
            
            # 現在レベル（編集不可）
            current_level_item = QTableWidgetItem(str(data["current"]))
            current_level_item.setFlags(current_level_item.flags() & ~Qt.ItemIsEditable)
            self.skill_table.setItem(i, 1, current_level_item)
            
            # 目標レベル（スピンボックス）
            target_spin = QSpinBox()
            target_spin.setMinimum(0)
            target_spin.setMaximum(5)  # 5段階評価と仮定
            target_spin.setValue(data["target"])
            target_spin.setProperty("skill_id", skill_id)  # カスタムプロパティでスキルIDを保持
            self.skill_table.setCellWidget(i, 2, target_spin)
    
    def save_and_close(self):
        """データを保存して閉じる"""
        # テーブルの各行からデータを取得して保存
        for row in range(self.skill_table.rowCount()):
            target_spin = self.skill_table.cellWidget(row, 2)
            if target_spin:
                skill_id = target_spin.property("skill_id")
                target_level = target_spin.value()
                self.skill_data.update_target_level(skill_id, target_level)
        
        # ダイアログを閉じる
        self.accept()
