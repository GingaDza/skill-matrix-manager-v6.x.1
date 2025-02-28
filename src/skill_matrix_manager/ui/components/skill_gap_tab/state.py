import logging
from PyQt5.QtCore import QObject, pyqtSignal
from typing import Dict

class SkillGapState(QObject):
    skill_target_changed = pyqtSignal(str, int)
    progressive_target_changed = pyqtSignal(str, dict)
    skills_changed = pyqtSignal(dict)
    time_unit_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self._skills = {}
        self._targets = {}
        self._progressive_targets = {}
        self._time_unit = "時間"

    def get_skills(self) -> Dict[str, str]:
        """スキル一覧を取得"""
        return self._skills.copy()

    def update_skills(self, skills: Dict[str, str]) -> None:
        """スキル一覧を更新"""
        self._skills = skills.copy()
        self.skills_changed.emit(self._skills)

    def update_target(self, skill: str, value: int) -> None:
        """目標値を更新"""
        if not 1 <= value <= 5:
            raise ValueError("Target value must be between 1 and 5")
        self._targets[skill] = value
        self.skill_target_changed.emit(skill, value)

    def get_target(self, skill: str) -> int:
        """スキルの目標値を取得"""
        return self._targets.get(skill, 1)

    @property
    def time_unit(self) -> str:
        """時間単位を取得"""
        return self._time_unit

    def update_time_unit(self, unit: str) -> None:
        """時間単位を更新"""
        if unit not in ["時間", "日", "月", "年"]:
            raise ValueError("Invalid time unit")
        self._time_unit = unit
        self.time_unit_changed.emit(unit)

    def update_progressive_target(self, time_key: str, targets: Dict[str, int]) -> None:
        """段階的目標値を更新"""
        self._progressive_targets[time_key] = targets.copy()
        self.progressive_target_changed.emit(time_key, targets)

    def get_progressive_targets(self) -> Dict[str, Dict[str, int]]:
        """段階的目標値を取得"""
        return self._progressive_targets.copy()
