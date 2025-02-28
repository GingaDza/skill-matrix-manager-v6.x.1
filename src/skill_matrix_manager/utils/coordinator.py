#!/usr/bin/env python3
"""アプリケーションコンポーネント間の連携を管理するコーディネーター"""

from PyQt5.QtCore import QObject, pyqtSignal
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class AppCoordinator(QObject):
    """アプリケーションコーディネーター"""
    
    # シグナル定義
    groupsChanged = pyqtSignal()      # グループリスト変更
    membersChanged = pyqtSignal(str)  # メンバーリスト変更(変更されたグループ名)
    skillsChanged = pyqtSignal()      # スキル一覧変更
    memberSelected = pyqtSignal(int)  # メンバー選択 (member_id)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("アプリケーションコーディネーター初期化")
