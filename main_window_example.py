#!/usr/bin/env python3
"""
メインウィンドウ実装例

このコードは既存のメインウィンドウに変更を統合するための
参考例として提供されています。
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
    QHBoxLayout, QWidget, QComboBox, QLabel, QPushButton
)

from src.skill_matrix_manager.utils.coordinator import AppCoordinator
from src.skill_matrix_manager.ui.components.skill_gap_tab_impl import SkillGapTab
from src.skill_matrix_manager.services import SkillService
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

# 初期設定タブのモック
class SettingsTab(QWidget):
    """初期設定タブのモック"""
    from PyQt5.QtCore import pyqtSignal
    
    # シグナル定義
    groupAdded = pyqtSignal()
    groupEdited = pyqtSignal()
    groupDeleted = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # モック用ボタン
        add_btn = QPushButton("グループ追加（テスト）")
        add_btn.clicked.connect(self.add_group)
        layout.addWidget(add_btn)
    
    def add_group(self):
        """グループ追加のモックメソッド"""
        print("グループ追加シミュレーション")
        self.groupAdded.emit()

# メンバー選択コンポーネントのモック
class MemberSelector(QWidget):
    """メンバー選択コンポーネントのモック"""
    from PyQt5.QtCore import pyqtSignal
    
    # シグナル定義
    memberSelected = pyqtSignal(int)
    
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        layout = QVBoxLayout(self)
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        group_layout.addWidget(self.group_combo)
        layout.addLayout(group_layout)
        
        # メンバー選択
        member_layout = QHBoxLayout()
        member_layout.addWidget(QLabel("メンバー:"))
        self.member_combo = QComboBox()
        self.member_combo.currentIndexChanged.connect(self.on_member_changed)
        member_layout.addWidget(self.member_combo)
        layout.addLayout(member_layout)
        
        # 初期データ読み込み
        self.reload_groups()
    
    def reload_groups(self):
        """グループリストを再読み込み"""
        print("グループリスト再読み込み")
        groups = self.service.get_groups()
        self.group_combo.clear()
        self.group_combo.addItem("すべて", None)
        for group in groups:
            self.group_combo.addItem(group, group)
        
        # メンバーも再読み込み
        self.reload_members()
    
    def reload_members(self):
        """メンバーリストを再読み込み"""
        self.member_combo.clear()
        members = self.service.get_members()
        for member in members:
            display = f"{member['name']} ({member['group_name'] or '未所属'})"
            self.member_combo.addItem(display, member['id'])
    
    def on_member_changed(self, index):
        """メンバー選択時"""
        if index >= 0:
            member_id = self.member_combo.itemData(index)
            if member_id:
                print(f"メンバー選択: ID={member_id}")
                self.memberSelected.emit(member_id)

# メインウィンドウ実装例
class MainWindow(QMainWindow):
    """メインウィンドウ実装例"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("スキルマトリックスマネージャー")
        self.resize(900, 700)
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QHBoxLayout(central_widget)
        
        # サービス初期化
        self.service = SkillService()
        
        # 左サイドパネル（メンバー選択など）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.member_selector = MemberSelector(self.service)
        left_layout.addWidget(self.member_selector)
        left_layout.addStretch()
        main_layout.addWidget(left_panel, 1)
        
        # 右側タブウィジェット
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 3)
        
        # コーディネーター
        self.coordinator = AppCoordinator(self)
        
        # タブの追加
        self.init_tabs()
        
        # コンポーネント間の連携設定
        self.setup_connections()
        
        logger.info("メインウィンドウ初期化完了")
    
    def init_tabs(self):
        """タブの初期化"""
        # 初期設定タブ
        self.settings_tab = SettingsTab()
        self.tabs.addTab(self.settings_tab, "初期設定")
        
        # スキルギャップタブ（コーディネーターを渡す）
        self.skill_gap_tab = SkillGapTab(self.coordinator)
        self.tabs.addTab(self.skill_gap_tab, "スキルギャップ")
    
    def setup_connections(self):
        """コンポーネント間の連携設定"""
        # 初期設定タブのシグナル接続
        self.settings_tab.groupAdded.connect(self.coordinator.notify_groups_changed)
        self.settings_tab.groupEdited.connect(self.coordinator.notify_groups_changed)
        self.settings_tab.groupDeleted.connect(self.coordinator.notify_groups_changed)
        
        # メンバー選択コンポーネントのシグナル接続
        self.coordinator.groupsChanged.connect(self.member_selector.reload_groups)
        self.member_selector.memberSelected.connect(self.coordinator.select_member)

# アプリケーション実行
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
