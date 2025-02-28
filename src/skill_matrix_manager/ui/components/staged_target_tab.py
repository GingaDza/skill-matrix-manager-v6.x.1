#!/usr/bin/env python3
"""段階的目標設定タブ"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QComboBox, QMessageBox, QHeaderView)
from PyQt5.QtCore import Qt, pyqtSignal
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class StagedTargetTab(QWidget):
    """段階的目標設定タブ"""
    
    # 目標レベル変更シグナル
    data_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.current_member_id = None
        self.current_member_name = None
        self.current_group_name = None
        self.skill_data = []  # スキルデータのリスト
        
    def setup_ui(self):
        """UI要素のセットアップ"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # ステージ選択
        stage_layout = QHBoxLayout()
        stage_layout.addWidget(QLabel("ステージ:"))
        self.stage_combo = QComboBox()
        self.stage_combo.addItems(["第1段階", "第2段階", "第3段階"])
        self.stage_combo.currentIndexChanged.connect(self.on_stage_changed)
        stage_layout.addWidget(self.stage_combo)
        stage_layout.addStretch()
        layout.addLayout(stage_layout)
        
        # スキルギャップテーブル
        self.skill_table = QTableWidget()
        self.skill_table.setColumnCount(3)
        self.skill_table.setHorizontalHeaderLabels(["スキル", "現在レベル", "目標レベル"])
        self.skill_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.skill_table.itemChanged.connect(self.on_table_item_changed)
        layout.addWidget(self.skill_table)
    
    def set_member(self, member_id, member_name=None, group_name=None):
        """メンバーを設定"""
        try:
            self.current_member_id = member_id
            self.current_member_name = member_name or member_id
            self.current_group_name = group_name or ""
            
            # スキルデータを読み込み
            self.load_skill_data()
            
            # 現在のステージでデータを表示
            self.display_stage_data()
            
            logger.info(f"StagedTargetTab: メンバーを設定: {self.current_member_name}")
        except Exception as e:
            logger.error(f"StagedTargetTab: メンバー設定エラー: {e}")
    
    def load_skill_data(self):
        """スキルデータを読み込み"""
        try:
            # ダミーデータを使用（実際はデータベースから取得）
            self.skill_data = [
                {"name": "Python", "current": 3, "targets": [4, 4, 5]},
                {"name": "JavaScript", "current": 2, "targets": [3, 4, 5]},
                {"name": "データベース", "current": 1, "targets": [2, 3, 4]},
                {"name": "UI/UX", "current": 2, "targets": [3, 3, 4]},
                {"name": "プロジェクト管理", "current": 2, "targets": [3, 4, 5]}
            ]
            logger.info(f"StagedTargetTab: スキルデータ読み込み: {len(self.skill_data)}件")
        except Exception as e:
            logger.error(f"StagedTargetTab: スキルデータ読み込みエラー: {e}")
    
    def display_stage_data(self):
        """現在のステージでテーブルに表示"""
        try:
            # テーブルの変更シグナルを一時的に切断
            self.skill_table.blockSignals(True)
            
            # テーブル初期化
            self.skill_table.setRowCount(0)
            
            # 現在のステージを取得
            current_stage = self.stage_combo.currentIndex()
            
            # スキルデータを表示
            for skill in self.skill_data:
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
                target_item = QTableWidgetItem(str(skill["targets"][current_stage]))
                self.skill_table.setItem(row, 2, target_item)
            
            # シグナル再接続
            self.skill_table.blockSignals(False)
            
            self.skill_table.resizeColumnsToContents()
            logger.info(f"StagedTargetTab: ステージ{current_stage+1}のデータ表示")
        except Exception as e:
            logger.error(f"StagedTargetTab: ステージデータ表示エラー: {e}")
    
    def on_stage_changed(self, index):
        """ステージ変更時の処理"""
        try:
            self.display_stage_data()
            logger.info(f"StagedTargetTab: ステージ{index+1}に変更")
        except Exception as e:
            logger.error(f"StagedTargetTab: ステージ変更エラー: {e}")
    
    def on_table_item_changed(self, item):
        """テーブルアイテム変更時の処理"""
        try:
            # 目標レベル列の変更のみ処理
            if item.column() != 2:
                return
                
            row = item.row()
            skill_name = self.skill_table.item(row, 0).text()
            
            # 値の検証
            try:
                new_level = int(item.text())
                if new_level < 1 or new_level > 5:
                    raise ValueError("レベルは1から5の間で設定してください")
            except ValueError as e:
                QMessageBox.warning(self, "エラー", str(e))
                # 元の値に戻す
                current_stage = self.stage_combo.currentIndex()
                for skill in self.skill_data:
                    if skill["name"] == skill_name:
                        item.setText(str(skill["targets"][current_stage]))
                        break
                return
            
            # データ更新
            current_stage = self.stage_combo.currentIndex()
            for i, skill in enumerate(self.skill_data):
                if skill["name"] == skill_name:
                    self.skill_data[i]["targets"][current_stage] = new_level
                    # 変更シグナル発行
                    self.data_changed.emit()
                    break
        except Exception as e:
            logger.error(f"StagedTargetTab: テーブルアイテム変更エラー: {e}")
    
    def get_chart_data(self):
        """チャートデータを取得"""
        # 現在のステージのデータを返す
        try:
            current_stage = self.stage_combo.currentIndex()
            categories = []
            current_values = []
            target_values = []
            
            for skill in self.skill_data:
                categories.append(skill["name"])
                current_values.append(skill["current"])
                target_values.append(skill["targets"][current_stage])
            
            return {
                "categories": categories,
                "current_values": current_values,
                "target_values": target_values,
                "stage": self.stage_combo.currentText()
            }
        except Exception as e:
            logger.error(f"StagedTargetTab: チャートデータ取得エラー: {e}")
            return None
