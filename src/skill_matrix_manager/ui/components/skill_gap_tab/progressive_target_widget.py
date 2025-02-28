import logging
from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout,
                           QLabel, QComboBox, QPushButton, QSpinBox,
                           QTabWidget, QMessageBox, QWidget)
from PyQt5.QtCore import Qt
from typing import Dict, List, Callable
import logging
from .skill_input_dialog import SkillInputDialog

logger = logging.getLogger(__name__)

class ProgressiveTargetWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("段階的目標値設定", parent)
        self.on_stage_changed = None
        self.on_stage_removed = None
        self._stages = {}  # 期間ごとのスキルレベルを保持
        self._skills = {}  # スキル一覧
        self._setup_ui()
        logger.debug("ProgressiveTargetWidget initialized")

    def _setup_ui(self) -> None:
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        
        # 目標時間設定グループ
        time_group = QGroupBox("目標時間設定")
        time_layout = QHBoxLayout()
        
        # 時間単位選択
        time_layout.addWidget(QLabel("時間単位:"))
        self.time_unit_combo = QComboBox()
        self.time_unit_combo.addItems(["時間", "日", "月", "年"])
        self.time_unit_combo.setCurrentText("月")  # デフォルトを月に設定
        time_layout.addWidget(self.time_unit_combo)
        
        # 目標時間
        time_layout.addWidget(QLabel("目標時間:"))
        self.time_value = QSpinBox()
        self.time_value.setRange(1, 9999)
        self.time_value.setValue(3)  # デフォルトを3に設定
        time_layout.addWidget(self.time_value)
        
        # 追加ボタン
        add_button = QPushButton("目標期間を追加")
        add_button.clicked.connect(self._add_time_period)
        time_layout.addWidget(add_button)
        
        time_layout.addStretch()
        time_group.setLayout(time_layout)
        main_layout.addWidget(time_group)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        main_layout.addWidget(self.tab_widget)
        
        self.setLayout(main_layout)
        logger.debug("UI setup completed")

    def set_skills(self, skills: Dict[str, str]) -> None:
        """スキル一覧を設定"""
        logger.debug(f"Setting skills in ProgressiveTargetWidget: {skills}")
        self._skills = skills
        if self.on_stage_changed:
            self.on_stage_changed(self.get_current_stage())

    def _add_time_period(self) -> None:
        """新しい目標期間を追加"""
        time_value = self.time_value.value()
        time_unit = self.time_unit_combo.currentText()
        
        # 重複チェック
        period_key = f"{time_value}{time_unit}"
        if period_key in self._stages:
            QMessageBox.warning(
                self,
                "警告",
                f"同じ期間（{period_key}）の目標が既に存在します。"
            )
            return
        
        logger.debug(f"Adding new time period with skills: {self._skills}")
        
        # スキル入力ダイアログを表示
        dialog = SkillInputDialog(time_value, time_unit, self._skills, self)
        if dialog.exec_():
            skill_levels = dialog.get_skill_levels()
            self._stages[period_key] = {
                'time': time_value,
                'unit': time_unit,
                'targets': skill_levels
            }
            
            logger.debug(f"Added new stage: {self._stages[period_key]}")
            
            # タブの更新
            self._update_tabs()
            
            # 値の変更を通知
            if self.on_stage_changed:
                self.on_stage_changed(self.get_current_stage())

    def _update_tabs(self) -> None:
        """タブの更新"""
        # 既存のタブをクリア
        self.tab_widget.clear()
        
        # ステージをソート
        sorted_stages = sorted(
            self._stages.items(),
            key=lambda x: self._convert_to_hours(x[1]['time'], x[1]['unit'])
        )
        
        # タブを追加
        for period_key, stage in sorted_stages:
            # タブの内容を作成
            tab_content = QWidget()
            tab_layout = QVBoxLayout(tab_content)
            
            # スキルレベル一覧を表示
            for skill_name in self._skills.keys():
                level = stage['targets'].get(skill_name, 1)
                skill_label = QLabel(f"{skill_name}: レベル{level}")
                tab_layout.addWidget(skill_label)
            
            # 編集・削除ボタン
            button_layout = QHBoxLayout()
            
            edit_button = QPushButton("編集")
            edit_button.clicked.connect(
                lambda checked, p=period_key: self._edit_time_period(p)
            )
            button_layout.addWidget(edit_button)
            
            delete_button = QPushButton("削除")
            delete_button.clicked.connect(
                lambda checked, p=period_key: self._delete_time_period(p)
            )
            button_layout.addWidget(delete_button)
            
            tab_layout.addLayout(button_layout)
            tab_layout.addStretch()
            
            # タブを追加
            self.tab_widget.addTab(tab_content, period_key)

    def _edit_time_period(self, period_key: str) -> None:
        """期間の編集"""
        stage = self._stages[period_key]
        dialog = SkillInputDialog(stage['time'], stage['unit'], self._skills, self)
        if dialog.exec_():
            skill_levels = dialog.get_skill_levels()
            stage['targets'] = skill_levels
            self._update_tabs()
            if self.on_stage_changed:
                self.on_stage_changed(self.get_current_stage())

    def _delete_time_period(self, period_key: str) -> None:
        """期間の削除"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setText(f"期間「{period_key}」の目標を削除しますか？")
        msg.setWindowTitle("目標期間の削除")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        
        if msg.exec_() == QMessageBox.Yes:
            self._stages.pop(period_key, None)
            self._update_tabs()
            if self.on_stage_changed:
                self.on_stage_changed(self.get_current_stage())

    def get_current_stage(self) -> List[Dict]:
        """現在のステージデータを取得"""
        return list(self._stages.values())

    def _convert_to_hours(self, time: int, unit: str) -> int:
        """時間単位を時間に変換"""
        multipliers = {
            "時間": 1,
            "日": 24,
            "月": 24 * 30,
            "年": 24 * 365
        }
        return time * multipliers.get(unit, 1)

