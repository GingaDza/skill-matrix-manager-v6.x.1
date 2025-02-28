from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout,
                           QHBoxLayout, QComboBox, QListWidget, QPushButton,
                           QLabel, QListWidgetItem)
from PyQt5.QtCore import Qt
from datetime import datetime, UTC
import sys
import traceback

# デバッグ用ロガー
from .utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

logger.info("===== メインウィンドウモジュールの読み込み開始 =====")

# コンポーネントをインポート
logger.info("システム管理タブのコンポーネントをインポート")
from .ui.components.initial_setup_tab import InitialSetupTab
from .ui.components.data_io_tab import DataIOTab
from .ui.components.system_info_tab import SystemInfoTab

logger.info("総合評価タブをインポート")
from .ui.components.overall_evaluation_tab import OverallEvaluationTab

logger.info("スキルギャップタブをインポート試行")
try:
    from .ui.components.skill_gap_tab_impl import SkillGapTab
    logger.info("SkillGapTab インポート成功")
except ImportError as e:
    logger.error(f"SkillGapTab インポートエラー: {e}")
    traceback.print_exc()
    # ダミークラスを定義
    class SkillGapTab(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            layout = QVBoxLayout(self)
            label = QLabel("スキルギャップタブの読み込みに失敗しました")
            layout.addWidget(label)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        logger.info("メインウィンドウの初期化開始")
        self._current_time = datetime(2025, 2, 19, 22, 21, 6, tzinfo=UTC)
        self._current_user = "GingaDza"
        try:
            self.initUI()
            self.load_test_data()
            logger.info("メインウィンドウの初期化完了")
        except Exception as e:
            logger.error(f"メインウィンドウ初期化中にエラー: {e}")
            traceback.print_exc()

    def initUI(self):
        """UIの初期化"""
        logger.info("メインウィンドウUIの初期化開始")
        self.setWindowTitle("Skill Matrix Manager")
        self.setGeometry(100, 100, 1200, 800)

        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # 左パネル (3:7の左側)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # グループ選択コンボボックスとラベル
        group_label = QLabel("グループ選択:")
        left_layout.addWidget(group_label)
        self.group_combo = QComboBox()
        left_layout.addWidget(self.group_combo)
        
        # ユーザーリストとラベル
        user_label = QLabel("ユーザーリスト:")
        left_layout.addWidget(user_label)
        self.user_list = QListWidget()
        left_layout.addWidget(self.user_list)
        
        # ユーザー操作ボタン
        button_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("追加")
        self.edit_user_btn = QPushButton("編集")
        self.delete_user_btn = QPushButton("削除")
        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(button_layout)
        
        main_layout.addWidget(left_panel, 3)

        # 右パネル (3:7の右側)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        self.tab_widget = QTabWidget()

        # システム管理タブ（デフォルト）
        logger.info("システム管理タブを初期化")
        self.system_tab = QTabWidget()
        self.initial_setup_tab = InitialSetupTab()
        self.data_io_tab = DataIOTab()
        self.system_info_tab = SystemInfoTab()
        self.system_tab.addTab(self.initial_setup_tab, "初期設定")
        self.system_tab.addTab(self.data_io_tab, "データ入出力")
        self.system_tab.addTab(self.system_info_tab, "システム情報")
        self.tab_widget.addTab(self.system_tab, "システム管理")

        # スキル分析タブ
        logger.info("スキル分析タブを初期化")
        self.skill_analysis_tab = QTabWidget()
        self.overall_evaluation_tab = OverallEvaluationTab()
        
        logger.info("スキルギャップタブを初期化")
        try:
            self.skill_gap_tab = SkillGapTab()
            logger.info("スキルギャップタブ初期化成功")
        except Exception as e:
            logger.error(f"スキルギャップタブ初期化エラー: {e}")
            traceback.print_exc()
            # エラー時にはダミーウィジェットを使用
            self.skill_gap_tab = QWidget()
            error_layout = QVBoxLayout(self.skill_gap_tab)
            error_label = QLabel("スキルギャップタブの初期化に失敗しました")
            error_layout.addWidget(error_label)
        
        self.skill_analysis_tab.addTab(self.overall_evaluation_tab, "総合評価")
        self.skill_analysis_tab.addTab(self.skill_gap_tab, "スキルギャップ")
        self.tab_widget.addTab(self.skill_analysis_tab, "スキル分析")

        right_layout.addWidget(self.tab_widget)
        main_layout.addWidget(right_panel, 7)
        
        logger.info("メインウィンドウUIの初期化完了")
    
    def load_test_data(self):
        """テスト用のデータをロード"""
        logger.info("テストデータのロード開始")
        # グループの追加
        groups = ["開発チーム", "デザインチーム", "マーケティングチーム", "営業チーム", "人事チーム"]
        for group in groups:
            self.group_combo.addItem(group)
        
        # ユーザー情報を追加（実際はDBから取得）
        self.users = {
            "開発チーム": [
                {"id": "dev1", "name": "佐藤太郎"},
                {"id": "dev2", "name": "鈴木一郎"},
                {"id": "dev3", "name": "田中花子"}
            ],
            "デザインチーム": [
                {"id": "des1", "name": "山本和子"},
                {"id": "des2", "name": "伊藤真司"}
            ],
            "マーケティングチーム": [
                {"id": "mkt1", "name": "渡辺健太"},
                {"id": "mkt2", "name": "小林直人"},
                {"id": "mkt3", "name": "加藤恵"}
            ],
            "営業チーム": [
                {"id": "sls1", "name": "吉田拓也"},
                {"id": "sls2", "name": "佐々木美咲"}
            ],
            "人事チーム": [
                {"id": "hr1", "name": "中村優子"}
            ]
        }
        
        # 初期グループのユーザーをロード
        self.update_user_list()
        
        # イベントハンドラを接続
        logger.info("イベントハンドラを接続")
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        self.user_list.itemSelectionChanged.connect(self.on_user_selected)
        
        logger.info("テストデータのロード完了")
    
    def update_user_list(self):
        """選択されたグループに基づいてユーザーリストを更新"""
        self.user_list.clear()
        current_group = self.group_combo.currentText()
        
        logger.info(f"ユーザーリストを更新: グループ={current_group}")
        
        if current_group in self.users:
            for user in self.users[current_group]:
                item = QListWidgetItem(user["name"])
                item.setData(Qt.UserRole, user["id"])
                self.user_list.addItem(item)
    
    def on_group_changed(self):
        """グループ選択変更時の処理"""
        logger.info("グループ選択変更")
        self.update_user_list()
    
    def on_user_selected(self):
        """ユーザー選択時の処理"""
        selected_items = self.user_list.selectedItems()
        if selected_items:
            selected_user = selected_items[0]
            user_id = selected_user.data(Qt.UserRole)
            user_name = selected_user.text()
            
            # 選択されたグループを取得
            group_name = self.group_combo.currentText()
            
            logger.info(f"ユーザー選択: id={user_id}, name={user_name}, group={group_name}")
            
            # スキルギャップタブにユーザー情報を設定
            try:
                if hasattr(self.skill_gap_tab, 'set_member'):
                    logger.info(f"スキルギャップタブにメンバー情報を設定: {user_name}")
                    self.skill_gap_tab.set_member(user_id, user_name, group_name)
                else:
                    logger.error("スキルギャップタブにset_memberメソッドがありません")
            except Exception as e:
                logger.error(f"スキルギャップタブへのメンバー設定中にエラー: {e}")
                traceback.print_exc()
            
            # スキル分析タブに切り替える
            logger.info("スキル分析タブ -> スキルギャップタブに切り替え")
            self.tab_widget.setCurrentIndex(1)  # "スキル分析"タブ
            self.skill_analysis_tab.setCurrentIndex(1)  # "スキルギャップ"タブ

logger.info("===== メインウィンドウモジュールの読み込み完了 =====")
