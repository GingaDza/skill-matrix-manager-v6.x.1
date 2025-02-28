#!/usr/bin/env python3
"""メインウィンドウ拡張ヘルパー"""

from src.skill_matrix_manager.utils.coordinator import AppCoordinator
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

def extend_main_window(main_window):
    """
    既存のメインウィンドウにコーディネーター機能を追加
    
    Args:
        main_window: 拡張するMainWindowインスタンス
        
    Returns:
        coordinator: 作成したAppCoordinatorインスタンス
    """
    # コーディネーターをメインウィンドウに追加
    coordinator = AppCoordinator(main_window)
    main_window.coordinator = coordinator
    
    # 既存のメンバー選択機能とコーディネーターを接続
    if hasattr(main_window, 'on_member_selected'):
        # 既存のメンバー選択メソッドをラップ
        original_on_member_selected = main_window.on_member_selected
        
        def wrapped_on_member_selected(member_id):
            result = original_on_member_selected(member_id)
            # メンバー選択イベントを発火
            coordinator.memberSelected.emit(member_id)
            return result
            
        main_window.on_member_selected = wrapped_on_member_selected
        
    # メイン画面で選択されているメンバーIDを取得するメソッドを追加
    if not hasattr(main_window, 'get_selected_member_id'):
        def get_selected_member_id():
            # 実装は既存コードに依存するため、適切に調整が必要
            try:
                # 一般的なパターンとして、member_id属性をチェック
                if hasattr(main_window, 'current_member_id'):
                    return main_window.current_member_id
                # または左側のメンバーリストから取得
                if hasattr(main_window, 'member_list'):
                    return main_window.member_list.currentData()
            except:
                return None
            return None
            
        main_window.get_selected_member_id = get_selected_member_id
        
    # グループ変更通知メソッドを追加
    if not hasattr(main_window, 'notify_groups_changed'):
        def notify_groups_changed():
            coordinator.groupsChanged.emit()
        main_window.notify_groups_changed = notify_groups_changed
    
    logger.info("メインウィンドウ拡張完了")
    return coordinator
