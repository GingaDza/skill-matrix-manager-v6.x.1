"""スキルギャップタブ - 現在のスキルと目標スキルのギャップを分析し、成長計画を設計するタブ"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QFormLayout, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from datetime import datetime

# 段階別目標設定タブとレーダーチャートダイアログのインポート
from src.skill_matrix_manager.ui.components.skill_gap_tab.staged_target_tab import StagedTargetTab
from src.skill_matrix_manager.ui.components.skill_gap_tab.radar_chart_dialog import RadarChartDialog

# デバッグ用ロガー
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

class SkillGapTab(QWidget):
    """スキルギャップ分析と段階的な成長プランを提供するタブ"""
    
    # スキルギャップタブからのシグナル
    data_changed = pyqtSignal()  # データ変更通知用シグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("スキルギャップタブの初期化")
        
        # メンバー情報
        self.current_member_id = None
        self.current_member_name = None
        self.current_member_group = None
        
        # スキル情報
        self.skill_data = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期設定"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        
        # ===== メンバー情報エリア =====
        self.member_info_group = QGroupBox("分析対象")
        member_info_layout = QFormLayout()
        self.member_name_label = QLabel("未選択")
        self.member_group_label = QLabel("未選択")
        self.last_update_label = QLabel(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        member_info_layout.addRow("メンバー:", self.member_name_label)
        member_info_layout.addRow("グループ:", self.member_group_label)
        member_info_layout.addRow("更新日時:", self.last_update_label)
        self.member_info_group.setLayout(member_info_layout)
        
        main_layout.addWidget(self.member_info_group)
        
        # ===== タブウィジェット =====
        self.tab_widget = QTabWidget()
        
        # 段階別目標設定タブ (テスト済みコンポーネント)
        self.staged_target_tab = StagedTargetTab(parent=self)
        self.staged_target_tab.data_changed.connect(self.on_data_changed)
        self.tab_widget.addTab(self.staged_target_tab, "段階別目標設定")
        
        main_layout.addWidget(self.tab_widget)
        
        # ===== ボタンエリア =====
        button_layout = QHBoxLayout()
        
        # レーダーチャートボタン
        self.radar_chart_btn = QPushButton("レーダーチャートで確認")
        self.radar_chart_btn.setEnabled(False)  # 初期状態は無効
        self.radar_chart_btn.clicked.connect(self.show_radar_chart)
        button_layout.addWidget(self.radar_chart_btn)
        
        button_layout.addStretch(1)
        
        # 成長プラン生成ボタン
        self.generate_btn = QPushButton("成長プラン生成")
        self.generate_btn.setEnabled(False)  # 初期状態は無効
        self.generate_btn.clicked.connect(self.generate_growth_plan)
        button_layout.addWidget(self.generate_btn)
        
        main_layout.addLayout(button_layout)
    
    def set_member(self, member_id, member_name, member_group):
        """メンバーの設定"""
        logger.info(f"スキルギャップタブ: メンバー設定 - {member_name} ({member_group})")
        
        # メンバー情報の更新
        self.current_member_id = member_id
        self.current_member_name = member_name
        self.current_member_group = member_group
        
        # UI表示の更新
        self.member_info_group.setTitle(f"分析対象: {member_name}")
        self.member_name_label.setText(member_name)
        self.member_group_label.setText(member_group)
        self.last_update_label.setText(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # 仮のスキルデータをロード
        self.load_test_skill_data()
        
        # 段階別目標設定タブにデータを渡す
        # ※実際のアプリではダミーデータではなく、DBから取得したデータを渡す
        
        # ボタンを有効化
        self.generate_btn.setEnabled(True)
    
    def load_test_skill_data(self):
        """テスト用のスキルデータ読み込み（実際のアプリではDBから取得）"""
        # テスト用のスキルデータを作成
        self.skill_data = {
            "prog": {
                "name": "プログラミング",
                "categories": {
                    "lang": {
                        "name": "言語",
                        "skills": {
                            "python": {"name": "Python", "current": 3, "target": 5},
                            "java": {"name": "Java", "current": 2, "target": 4},
                            "js": {"name": "JavaScript", "current": 4, "target": 5}
                        }
                    },
                    "db": {
                        "name": "データベース",
                        "skills": {
                            "mysql": {"name": "MySQL", "current": 4, "target": 5},
                            "mongodb": {"name": "MongoDB", "current": 2, "target": 4}
                        }
                    }
                }
            },
            "design": {
                "name": "デザイン",
                "categories": {
                    "ui": {
                        "name": "UI/UX",
                        "skills": {
                            "figma": {"name": "Figma", "current": 3, "target": 5},
                            "xd": {"name": "Adobe XD", "current": 2, "target": 4}
                        }
                    }
                }
            }
        }
    
    def on_data_changed(self):
        """データ変更時の処理"""
        logger.info("スキルギャップタブ: データ変更通知を受信")
        
        # レーダーチャートボタンを有効化
        self.radar_chart_btn.setEnabled(True)
        
        # 親へシグナルを伝播
        self.data_changed.emit()
    
    def generate_growth_plan(self):
        """成長プランの生成"""
        logger.info("スキルギャップタブ: 成長プラン生成")
        
        if not self.current_member_name:
            QMessageBox.warning(self, "エラー", "メンバーが選択されていません")
            return
        
        # 段階別目標設定タブのデータから成長プランを生成
        chart_data = self.staged_target_tab.get_chart_data()
        
        if chart_data:
            QMessageBox.information(self, "成長プラン生成完了", 
                                   f"{self.current_member_name}さんの成長プランを生成しました。\n\n"
                                   "「レーダーチャートで確認」ボタンで可視化結果を確認できます。")
            self.radar_chart_btn.setEnabled(True)
    
    def show_radar_chart(self):
        """レーダーチャートの表示"""
        logger.info("スキルギャップタブ: レーダーチャート表示")
        
        # 段階別目標設定タブからチャートデータを取得
        chart_data = self.staged_target_tab.get_chart_data()
        
        if chart_data:
            # レーダーチャートダイアログを表示
            dialog = RadarChartDialog(self, chart_data)
            dialog.exec_()
        else:
            QMessageBox.warning(self, "エラー", "表示できるチャートデータがありません")
