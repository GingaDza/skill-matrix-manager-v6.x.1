import logging
from typing import Dict

class SkillGapModel:
    def __init__(self):
        self._skills: Dict[str, str] = {}  # skill_name: category
        self._target_values: Dict[str, int] = {}  # skill_name: target_value
        self._user_values: Dict[str, int] = {}  # skill_name: user_value
        self._progressive_targets: Dict[str, Dict[str, int]] = {}  # time_key: {skill_name: target_value}
        self._time_unit: str = "時間"

    @property
    def skills(self) -> Dict[str, str]:
        return self._skills.copy()

    @property
    def target_values(self) -> Dict[str, int]:
        return self._target_values.copy()

    @property
    def user_values(self) -> Dict[str, int]:
        return self._user_values.copy()

    @property
    def progressive_targets(self) -> Dict[str, Dict[str, int]]:
        return {k: v.copy() for k, v in self._progressive_targets.items()}

    @property
    def time_unit(self) -> str:
        return self._time_unit

    def set_skills(self, skills: Dict[str, str]) -> None:
        self._skills = skills.copy()

    def set_target(self, skill_name: str, value: int) -> None:
        if not 1 <= value <= 5:
            raise ValueError("Target value must be between 1 and 5")
        self._target_values[skill_name] = value

    def set_user_value(self, skill_name: str, value: int) -> None:
        if not 1 <= value <= 5:
            raise ValueError("User value must be between 1 and 5")
        self._user_values[skill_name] = value

    def get_target(self, skill_name: str) -> int:
        return self._target_values.get(skill_name, 1)

    def get_user_value(self, skill_name: str) -> int:
        return self._user_values.get(skill_name, 1)

    def set_time_unit(self, unit: str) -> None:
        if unit not in ["時間", "日", "月", "年"]:
            raise ValueError("Invalid time unit")
        self._time_unit = unit

    def set_progressive_target(self, time_key: str, targets: Dict[str, int]) -> None:
        self._progressive_targets[time_key] = targets.copy()
