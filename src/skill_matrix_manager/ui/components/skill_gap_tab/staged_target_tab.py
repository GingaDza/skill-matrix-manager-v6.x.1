#!/usr/bin/env python3
"""段階的目標設定タブ"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QTableWidget, QTableWidgetItem, QPushButton,
                           QComboBox, QMessageBox, QHeaderView, QFormLayout,
                           QGroupBox)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class StagedTargetTab(QWidget):
    """段階的目標設定タブ"""
    
    # データ変更シグナル
    data_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        """初期化"""
        super().__init__(parent)
        
        # メンバー情報
        self.current_member_id = None
        self.current_member_name = None
        self.current_group_name = None
        self.skill_data = []  # スキルデータリスト
        
        # UI初期化
        self.setup_ui()
    
    def setup_ui(self):
        """UI設定"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # ステージ選択エリア
        stage_group = QGroupBox("ステージ選択")
        stage_layout = QHBoxLayout()
        
        stage_layout.addWidget(QLabel("目標ステージ:"))
        self.stage_combo = QComboBox()
        self.stage_combo.addItems(["第1段階", "第2段階", "第3段階"])
        self.stage_combo.currentIndexChanged.connect(self.on_stage_changed)
        stage_layout.addWidget(self.stage_combo)
        
        stage_layout.addStretch()
        
        stage_group.setLayout(stage_layout)
        layout.addWidget(stage_group)
        
        # スキル目標値エリア
        self.skill_group = QGroupBox("スキル目標値設定")
        skill_layout = QVBoxLayout()
        
        # スキルテーブル
        self.skill_table = QTableWidget()
        self.skill_table.setColumnCount(4)
        self.skill_table.setHorizontalHeaderLabels(["スキル", "現在レベル", "目標レベル", "ギャップ"])
        self.skill_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.skill_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        self.skill_table.itemChanged.connect(self.on_item_changed)
        
        skill_layout.addWidget(self.skill_table)
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("保存")
        self.save_btn.setEnabled(False)  # 初期状態は無効
        self.save_btn.clicked.connect(self.save_data)
        
        button_layout.addStretch()
        button_layout.addWidget(self.save_btn)
        
        skill_layout.addLayout(button_layout)
        
        self.skill_group.setLayout(skill_layout)
        layout.addWidget(self.skill_group)
        
        # ステータス表示
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
    
    def set_member(self, member_id, member_name=None, group_name=None):
        """メンバーを設定"""
        try:
            self.current_member_id = member_id
            self.current_member_name = member_name or member_id
            self.current_group_name = group_name or ""
            
            # データ読み込み
            self.load_data()
            
            # 現在のステージでテーブル表示
            self.update_table()
            
            # 保存ボタン無効化（変更があるまで）
            self.save_btn.setEnabled(False)
            
            logger.info(f"StagedTargetTab: メンバー設定 - {self.current_member_name}")
            
        except Exception as e:
            logger.error(f"StagedTargetTab: メンバー設定エラー - {e}")
    
    def load_data(self):
        """メンバーのスキルデータを読み込み"""
        try:
            # ダミーデータ（実際はデータベースから取得）
            self.skill_data = [
                {"name": "Python", "current": 3, "targets": [4, 4, 5]},
                {"name": "JavaScript", "current": 2, "targets": [3, 4, 4]},
                {"name": "Java", "current": 1, "targets": [2, 3, 4]},
                {"name": "データベース", "current": 2, "targets": [3, 4, 5]},
                {"name": "UI/UX", "current": 3, "targets": [3, 4, 4]}
            ]
            
            logger.info(f"StagedTargetTab: スキルデータ読み込み - {len(self.skill_data)}件")
            
        except Exception as e:
            logger.error(f"StagedTargetTab: データ読み込みエラー - {e}")
            self.skill_data = []
    
    def update_table(self):
        """テーブル表示を更新"""
        try:
            # シグナルをブロック
            self.skill_table.blockSignals(True)
            
            # テーブルをクリア
            self.skill_table.setRowCount(0)
            
            # 現在のステージ
            current_stage = self.stage_combo.currentIndex()
            
            # 各スキルを表示
            for i, skill in enumerate(self.skill_data):
                row = self.skill_table.rowCount()
                self.skill_table.insertRow(row)
                
                # スキル名
                name_item = QTableWidgetItem(skill["name"])
                name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                self.skill_table.setItem(row, 0, name_item)
                
                # 現在レベル
                current_item = QTableWidgetItem(str(skill["current"]))
                current_item.setFlags(current_item.flags() & ~Qt.ItemIsEditable)
                self.skill_table.setItem(row, 1, current_item)
                
                # 目標レベル
                target_level = skill["targets"][current_stage]
                target_item = QTableWidgetItem(str(target_level))
                self.skill_table.setItem(row, 2, target_item)
                
                # ギャップ
                gap = target_level - skill["current"]
                gap_text = f"{gap:+d}" if gap != 0 else "0"
                gap_item = QTableWidgetItem(gap_text)
                gap_item.setFlags(gap_item.flags() & ~Qt.ItemIsEditable)
                
                # ギャップに応じたカラー設定
                if gap > 0:
                    gap_item.setForeground(Qt.darkGreen)
                elif gap < 0:
                    gap_item.setForeground(Qt.red)
                
                self.skill_table.setItem(row, 3, gap_item)
            
            # テーブル調整
            self.skill_table.resizeColumnsToContents()
            self.skill_table.resizeRowsToContents()
            
            # シグナル再開
            self.skill_table.blockSignals(False)
            
        except Exception as e:
            logger.error(f"StagedTargetTab: テーブル更新エラー - {e}")
    
    def on_stage_changed(self, index):
        """ステージ変更時の処理"""
        try:
            # テーブル表示更新
            self.update_table()
            logger.info(f"StagedTargetTab: ステージ{index+1}に変更")
        except Exception as e:
            logger.error(f"StagedTargetTab: ステージ変更エラー - {e}")
    
    def on_item_changed(self, item):
        """アイテム変更時の処理"""
        try:
            # 目標レベル列のみ処理
            if item.column() != 2:
                return
            
            row = item.row()
            if row >= len(self.skill_data):
                return
            
            try:
                # 値の検証
                new_level = int(item.text())
                if new_level < 1 or new_level > 5:
                    raise ValueError("レベルは1～5の範囲で指定してください")
                
                # データ更新
                current_stage = self.stage_combo.currentIndex()
                self.skill_data[row]["targets"][current_stage] = new_level
                
                # ギャップ再計算
                current_level = self.skill_data[row]["current"]
                gap = new_level - current_level
                gap_text = f"{gap:+d}" if gap != 0 else "0"
                
                # ギャップアイテム更新
                gap_item = QTableWidgetItem(gap_text)
                gap_item.setFlags(gap_item.flags() & ~Qt.ItemIsEditable)
                
                if gap > 0:
                    gap_item.setForeground(Qt.darkGreen)
                elif gap < 0:
                    gap_item.setForeground(Qt.red)
                
                self.skill_table.blockSignals(True)
                self.skill_table.setItem(row, 3, gap_item)
                self.skill_table.blockSignals(False)
                
                # 保存ボタン有効化
                self.save_btn.setEnabled(True)
                self.data_changed.emit()
                
            except ValueError as e:
                # 不正な値の場合は元に戻す
                QMessageBox.warning(self, "入力エラー", str(e))
                
                current_stage = self.stage_combo.currentIndex()
                original_value = str(self.skill_data[row]["targets"][current_stage])
                
                self.skill_table.blockSignals(True)
                item.setText(original_value)
                self.skill_table.blockSignals(False)
            
        except Exception as e:
            logger.error(f"StagedTargetTab: アイテム変更エラー - {e}")
    
    def save_data(self):
        """データ保存"""
        try:
            # 実際はここでデータベースに保存する処理
            
            # 保存完了メッセージ
            self.status_label.setText("保存しました")
            self.save_btn.setEnabled(False)
            
            # 3秒後にステータスメッセージをクリア
            QTimer.singleShot(3000, lambda: self.status_label.setText(""))
            
            logger.info("StagedTargetTab: データ保存")
            
        except Exception as e:
            logger.error(f"StagedTargetTab: データ保存エラー - {e}")
            self.status_label.setText("保存失敗")
    
    def get_chart_data(self):
        """チャート用データを取得"""
        try:
            # 各ステージごとにデータを用意
            stages_data = []
            
            for stage in range(3):  # 3段階
                categories = []
                current_values = []
                target_values = []
                
                for skill in self.skill_data:
                    categories.append(skill["name"])
                    current_values.append(skill["current"])
                    target_values.append(skill["targets"][stage])
                
                stages_data.append({
                    "name": f"第{stage+1}段階",
                    "categories": categories,
                    "current_values": current_values,
                    "target_values": target_values
                })
            
            return stages_data
            
        except Exception as e:
            logger.error(f"StagedTargetTab: チャートデータ取得エラー - {e}")
            return []
