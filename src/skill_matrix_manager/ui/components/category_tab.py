#!/usr/bin/env python3
"""カテゴリータブの実装"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QComboBox, QGroupBox, QFormLayout, QScrollArea)
from PyQt5.QtCore import Qt, pyqtSignal
from src.skill_matrix_manager.ui.components.charts.radar_chart import RadarChart
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class CategoryTab(QWidget):
    """カテゴリー別スキル入力タブ"""
    
    # スキルレベル変更シグナル
    skill_level_changed = pyqtSignal(str, str, int)  # カテゴリー名、スキル名、レベル
    
    def __init__(self, category_name, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.current_member = None
        self.current_group = None
        self.skill_combos = {}  # スキルコンボボックス
        self.setup_ui()
    
    def setup_ui(self):
        """UI要素のセットアップ"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # メンバー情報表示
        self.member_info_group = QGroupBox("メンバー情報")
        member_layout = QFormLayout()
        self.member_name_label = QLabel("選択されていません")
        self.member_group_label = QLabel("-")
        member_layout.addRow("名前:", self.member_name_label)
        member_layout.addRow("グループ:", self.member_group_label)
        self.member_info_group.setLayout(member_layout)
        main_layout.addWidget(self.member_info_group)
        
        # メインコンテンツ部分（左右分割）
        content_layout = QHBoxLayout()
        
        # 左側: スキル入力部分
        skill_group = QGroupBox("スキル評価")
        skill_layout = QVBoxLayout()
        
        # スクロールエリア
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_content = QWidget()
        self.form_layout = QFormLayout(scroll_content)
        
        # サンプルスキル（実際はカテゴリーに応じたスキルをロード）
        sample_skills = ["Python", "JavaScript", "Java", "データベース", "UI/UX"]
        
        for skill in sample_skills:
            combo = QComboBox()
            combo.addItems(["1", "2", "3", "4", "5"])
            combo.setCurrentIndex(0)
            combo.currentIndexChanged.connect(
                lambda idx, s=skill: self.on_skill_level_changed(s, idx+1)
            )
            self.form_layout.addRow(f"{skill}:", combo)
            self.skill_combos[skill] = combo
        
        scroll_area.setWidget(scroll_content)
        skill_layout.addWidget(scroll_area)
        skill_group.setLayout(skill_layout)
        content_layout.addWidget(skill_group)
        
        # 右側: レーダーチャート
        chart_group = QGroupBox("スキルチャート")
        chart_layout = QVBoxLayout()
        self.radar_chart = RadarChart()
        
        # サンプルデータでチャートを初期化
        categories = list(self.skill_combos.keys())
        values = [1] * len(categories)  # すべて1に初期化
        self.radar_chart.update_chart(categories, values)
        
        chart_layout.addWidget(self.radar_chart)
        chart_group.setLayout(chart_layout)
        content_layout.addWidget(chart_group)
        
        main_layout.addLayout(content_layout)
    
    def set_member(self, member_id, member_name=None, group_name=None):
        """メンバーを設定"""
        try:
            self.current_member = member_name or member_id
            self.current_group = group_name or ""
            
            # メンバー情報の表示更新
            self.member_name_label.setText(self.current_member)
            self.member_group_label.setText(self.current_group)
            
            # TODO: メンバーのスキルデータをロード
            
            logger.info(f"カテゴリータブ({self.category_name}): メンバー設定 - {self.current_member}")
        except Exception as e:
            logger.error(f"カテゴリータブ({self.category_name}): メンバー設定エラー - {e}")
    
    def on_skill_level_changed(self, skill, level):
        """スキルレベル変更時の処理"""
        try:
            # レーダーチャート更新
            categories = list(self.skill_combos.keys())
            values = [self.skill_combos[skill].currentIndex() + 1 for skill in categories]
            self.radar_chart.update_chart(categories, values)
            
            # シグナル発行
            self.skill_level_changed.emit(self.category_name, skill, level)
            
            logger.info(f"スキルレベル変更: {skill}={level}")
        except Exception as e:
            logger.error(f"スキルレベル変更エラー: {e}")
