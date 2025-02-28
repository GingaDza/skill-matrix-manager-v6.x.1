#!/usr/bin/env python3
"""スキルギャップタブの実装"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QGroupBox,
    QLabel, QPushButton, QSizePolicy, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal

from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

# スキルギャップタブ関連コンポーネントをインポート
try:
    from src.skill_matrix_manager.ui.components.skill_gap_tab.staged_target_tab import StagedTargetTab
    from src.skill_matrix_manager.ui.components.skill_gap_tab.radar_chart_dialog import RadarChartDialog
    logger.info("スキルギャップタブ関連コンポーネントのインポートに成功しました")
except ImportError as e:
    logger.error(f"スキルギャップタブ関連コンポーネントのインポートに失敗: {e}")

class SkillGapTab(QWidget):
    """スキルギャップ分析タブ - スキル目標設定と成長計画機能を提供"""
    
    # スキル成長計画作成シグナル
    skill_plan_created = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        """初期化"""
        super().__init__(parent)
        
        # メンバー情報
        self.current_member_id = None
        self.current_member_name = None
        self.current_group_name = None
        
        # UI初期化
        self.setup_ui()
        logger.info("スキルギャップタブを初期化しました")
    
    def setup_ui(self):
        """UI要素のセットアップ"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # メンバー情報表示部
        member_group = QGroupBox("メンバー情報")
        member_layout = QFormLayout()
        
        self.member_name_label = QLabel("選択されていません")
        self.member_group_label = QLabel("-")
        
        member_layout.addRow("名前:", self.member_name_label)
        member_layout.addRow("グループ:", self.member_group_label)
        
        member_group.setLayout(member_layout)
        main_layout.addWidget(member_group)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        
        try:
            # 段階別目標設定タブ
            self.staged_target_tab = StagedTargetTab(parent=self)
            self.staged_target_tab.data_changed.connect(self.on_data_changed)
            self.tab_widget.addTab(self.staged_target_tab, "段階別目標設定")
            logger.info("段階別目標設定タブを追加しました")
        except Exception as e:
            logger.error(f"段階別目標設定タブの作成に失敗: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
            # エラー表示用のダミータブ
            error_widget = QWidget()
            error_layout = QVBoxLayout()
            error_layout.addWidget(QLabel(f"コンポーネントの読み込みに失敗: {e}"))
            error_widget.setLayout(error_layout)
            self.tab_widget.addTab(error_widget, "エラー")
        
        main_layout.addWidget(self.tab_widget)
        
        # ボタンエリア
        button_layout = QHBoxLayout()
        
        # レーダーチャート表示ボタン
        self.chart_btn = QPushButton("レーダーチャート表示")
        self.chart_btn.setEnabled(False)  # 初期状態は無効
        self.chart_btn.clicked.connect(self.show_radar_chart)
        
        button_layout.addStretch(1)
        button_layout.addWidget(self.chart_btn)
        
        main_layout.addLayout(button_layout)
    
    def set_member(self, member_id, member_name=None, group_name=None):
        """メンバーを設定"""
        try:
            self.current_member_id = member_id
            self.current_member_name = member_name or member_id
            self.current_group_name = group_name or ""
            
            # メンバー情報の表示を更新
            self.member_name_label.setText(self.current_member_name)
            self.member_group_label.setText(self.current_group_name)
            
            # ボタン有効化
            self.chart_btn.setEnabled(True)
            
            # 段階別目標設定タブにもメンバー情報を設定
            if hasattr(self, 'staged_target_tab'):
                self.staged_target_tab.set_member(
                    self.current_member_id,
                    self.current_member_name,
                    self.current_group_name
                )
            
            logger.info(f"メンバー設定: {self.current_member_name}")
        except Exception as e:
            logger.error(f"メンバー設定エラー: {e}")
    
    def on_data_changed(self):
        """データ変更イベント処理"""
        # 将来の拡張用
        logger.debug("スキルギャップデータが変更されました")
    
    def show_radar_chart(self):
        """レーダーチャート表示"""
        try:
            if not hasattr(self, 'staged_target_tab'):
                logger.error("段階別目標設定タブが初期化されていません")
                return
            
            # 段階別目標設定タブからチャートデータを取得
            stages_data = self.staged_target_tab.get_chart_data()
            
            if not stages_data:
                logger.warning("表示可能なデータがありません")
                return
                
            # データの確認
            logger.debug(f"レーダーチャートデータ: {len(stages_data)}ステージ")
            
            # レーダーチャートダイアログ表示
            try:
                dialog = RadarChartDialog(self, stages_data)
                dialog.exec_()
            except Exception as e:
                logger.error(f"レーダーチャートダイアログ表示エラー: {e}")
                import traceback
                logger.error(traceback.format_exc())
                
        except Exception as e:
            logger.error(f"レーダーチャート表示エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
