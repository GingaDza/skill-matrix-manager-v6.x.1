import logging
from PyQt5.QtWidgets import (QWidget, QFormLayout, QComboBox, QGroupBox, 
                           QVBoxLayout, QLabel, QScrollArea)
from typing import Dict, Callable
import logging

logger = logging.getLogger(__name__)

class TargetWidget(QGroupBox):
    def __init__(self, parent: QWidget = None):
        super().__init__("目標レベル設定", parent)
        self.skill_targets: Dict[str, QComboBox] = {}
        self._setup_ui()
        logger.debug("TargetWidget initialized")

    def _setup_ui(self) -> None:
        """UIの初期設定"""
        main_layout = QVBoxLayout()
        
        # 説明ラベル
        description = QLabel("各スキルの目標レベルを設定してください（1: 基礎レベル ～ 5: エキスパートレベル）")
        description.setWordWrap(True)
        main_layout.addWidget(description)

        # スクロール可能なエリアを作成
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.target_layout = QFormLayout(scroll_content)
        
        # スキル目標値のフォーム
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        self.setLayout(main_layout)

    def update_skills(self, skills: Dict[str, str],
                     get_target: Callable[[str], int],
                     on_target_changed: Callable[[str, int], None]) -> None:
        """スキル一覧を更新し、目標値設定用のUIを構築"""
        logger.debug(f"Updating skills in TargetWidget: {skills}")
        
        # 既存のウィジェットをクリア
        while self.target_layout.count():
            child = self.target_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.skill_targets.clear()
        
        if not skills:
            logger.warning("No skills to update UI")
            return

        # スキルごとのコンボボックスを作成
        for skill_name, skill_desc in skills.items():
            combo = QComboBox()
            combo.addItems(["1 (基礎レベル)", "2 (初級レベル)", 
                          "3 (中級レベル)", "4 (上級レベル)", 
                          "5 (エキスパートレベル)"])
            
            # 現在の目標値を設定
            current_value = get_target(skill_name)
            combo.setCurrentIndex(current_value - 1)
            
            # 値変更時のコールバックを設定
            combo.currentIndexChanged.connect(
                lambda value, skill=skill_name: 
                on_target_changed(skill, value + 1)
            )
            
            self.skill_targets[skill_name] = combo
            # スキル名と説明を組み合わせたラベル
            label = QLabel(f"{skill_name}\n({skill_desc})")
            label.setWordWrap(True)
            
            self.target_layout.addRow(label, combo)
            logger.debug(f"Added UI for skill: {skill_name}")

    def update_target(self, skill_name: str, value: int) -> None:
        """特定のスキルの目標値を更新"""
        if skill_name in self.skill_targets:
            combo = self.skill_targets[skill_name]
            if value != combo.currentIndex() + 1:
                combo.setCurrentIndex(value - 1)
                logger.debug(f"Updated target for {skill_name}: {value}")

    def get_all_targets(self) -> Dict[str, int]:
        """全てのスキルの目標値を取得"""
        return {
            skill: combo.currentIndex() + 1
            for skill, combo in self.skill_targets.items()
        }
