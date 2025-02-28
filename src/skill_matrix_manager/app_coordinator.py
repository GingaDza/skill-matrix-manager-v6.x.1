#!/usr/bin/env python3
"""アプリケーション全体のタブ間連携を管理するコーディネーター"""

from PyQt5.QtCore import QObject, pyqtSignal
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class AppCoordinator(QObject):
    """
    アプリケーションコーディネーター
    
    タブ間の連携、グローバルイベントの管理を行う
    """
    
    # シグナル定義
    groupsUpdated = pyqtSignal()  # グループリスト更新
    membersUpdated = pyqtSignal()  # メンバーリスト更新
    skillsUpdated = pyqtSignal()   # スキルリスト更新
    
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("アプリケーションコーディネーター初期化")
    
    def notify_groups_updated(self):
        """グループリストが更新されたことを通知"""
        logger.info("グループリスト更新をブロードキャスト")
        self.groupsUpdated.emit()
    
    def notify_members_updated(self):
        """メンバーリストが更新されたことを通知"""
        logger.info("メンバーリスト更新をブロードキャスト")
        self.membersUpdated.emit()
    
    def notify_skills_updated(self):
        """スキルリストが更新されたことを通知"""
        logger.info("スキルリスト更新をブロードキャスト")
        self.skillsUpdated.emit()
