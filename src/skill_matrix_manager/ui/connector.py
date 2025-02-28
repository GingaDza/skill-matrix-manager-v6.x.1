#!/usr/bin/env python3
"""既存メインウィンドウへのコネクター機能"""

from src.skill_matrix_manager.utils.coordinator import AppCoordinator
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

def connect_components(main_window, settings_tab, skill_gap_tab, member_selector):
    """
    既存コンポーネント間の連携を設定
    
    Args:
        main_window: メインウィンドウインスタンス
        settings_tab: 初期設定タブインスタンス
        skill_gap_tab: スキルギャップタブインスタンス
        member_selector: メンバー選択コンポーネントインスタンス
    
    Returns:
        AppCoordinator: 作成したコーディネーターインスタンス
    """
    # コーディネーター作成
    coordinator = AppCoordinator(main_window)
    
    # 初期設定タブの連携
    # グループ変更があればコーディネーターに通知
    try:
        settings_tab.groupAdded.connect(coordinator.notify_groups_changed)
        settings_tab.groupEdited.connect(coordinator.notify_groups_changed)
        settings_tab.groupDeleted.connect(coordinator.notify_groups_changed)
        logger.info("初期設定タブとコーディネーターの連携設定完了")
    except (AttributeError, TypeError) as e:
        logger.warning(f"初期設定タブとの連携に一部失敗: {e}")
    
    # メンバー選択コンポーネントの連携
    try:
        # グループ変更通知を受け取る
        coordinator.groupsChanged.connect(member_selector.reload_groups)
        
        # メンバー選択をコーディネーターに通知
        member_selector.memberSelected.connect(coordinator.select_member)
        
        logger.info("メンバー選択コンポーネントとコーディネーターの連携設定完了")
    except (AttributeError, TypeError) as e:
        logger.warning(f"メンバー選択コンポーネントとの連携に一部失敗: {e}")
    
    # スキルギャップタブのインスタンスにコーディネーターを設定
    if hasattr(skill_gap_tab, 'coordinator') and skill_gap_tab.coordinator is None:
        skill_gap_tab.coordinator = coordinator
    
    logger.info("コンポーネント間の連携設定完了")
    return coordinator
