#!/usr/bin/env python3
"""メインアプリケーション修正のサンプル"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget
from src.skill_matrix_manager.app_coordinator import AppCoordinator
from src.skill_matrix_manager.ui.components.skill_gap_tab_impl import SkillGapTab
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

# ここでは初期設定タブのモックを作成
class SettingsTabMock:
    def __init__(self, coordinator):
        self.coordinator = coordinator
    
    def add_group(self, group_name):
        """グループ追加のモックメソッド"""
        # 実際には追加処理を行い、その後通知
        logger.info(f"グループ追加: {group_name}")
        self.coordinator.notify_groups_updated()

# メインアプリケーションのカスタマイズ方法例
def customize_main_app():
    """
    既存のメインアプリケーションを修正するためのガイド
    
    以下は実際に実行されるコードではなく、既存のコードに組み込むべき
    修正内容を示しています。
    """
    
    # 1. メインウィンドウクラスに AppCoordinator を追加
    #    class MainWindow:
    #        def __init__(self):
    #            # ... 既存の初期化コード ...
    #            
    #            # コーディネーターの追加
    #            self.coordinator = AppCoordinator(self)
    #            
    #            # ... 残りの初期化コード ...
    
    # 2. 初期設定タブのグループ変更時に通知を行う
    #    settings_tab.group_added.connect(self.coordinator.notify_groups_updated)
    #    settings_tab.group_edited.connect(self.coordinator.notify_groups_updated)
    #    settings_tab.group_deleted.connect(self.coordinator.notify_groups_updated)
    
    # 3. スキルギャップタブにグループ更新通知を接続
    #    self.coordinator.groupsUpdated.connect(skill_gap_tab.updateGroups)
    
    # 4. メンバー管理コンポーネントにもグループ更新通知を接続
    #    self.coordinator.groupsUpdated.connect(member_manager.updateGroups)
    
    # これらの変更により、初期設定タブでグループが変更された際に
    # 他のすべてのタブやコンポーネントに通知され、UIが最新の状態に保たれる
    
    print("メインアプリケーションの修正方法を出力しました。")
    print("実際のコードに上記の変更を適用してください。")

# 修正例のデモ
def demo_app():
    """修正後の動作をデモするシンプルなアプリケーション"""
    app = QApplication(sys.argv)
    
    main_window = QMainWindow()
    main_window.setWindowTitle("修正例デモ")
    main_window.resize(800, 600)
    
    # コーディネーター作成
    coordinator = AppCoordinator(main_window)
    
    # タブウィジェット
    tabs = QTabWidget()
    main_window.setCentralWidget(tabs)
    
    # スキルギャップタブ
    skill_gap_tab = SkillGapTab()
    tabs.addTab(skill_gap_tab, "スキルギャップ")
    
    # 連携設定
    coordinator.groupsUpdated.connect(skill_gap_tab.updateGroups)
    
    # 初期設定タブのモック
    settings_tab_mock = SettingsTabMock(coordinator)
    
    # ここで初期設定タブでグループ追加があった場合をシミュレート
    # 実際のアプリケーションでは、初期設定タブのUI操作に応じて実行される
    import threading
    def simulate_group_add():
        import time
        time.sleep(3)  # 3秒後にグループ追加
        settings_tab_mock.add_group("新規グループ")
        
    threading.Thread(target=simulate_group_add).start()
    
    main_window.show()
    return app.exec_()

if __name__ == "__main__":
    customize_main_app()
    # デモ実行
    # sys.exit(demo_app())
