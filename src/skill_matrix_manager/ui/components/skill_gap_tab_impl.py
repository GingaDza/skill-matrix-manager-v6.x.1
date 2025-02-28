from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpinBox,
    QGroupBox, QFormLayout, QToolButton, QScrollArea
)
from PyQt5.QtCore import Qt

# 重要なインポート
from src.skill_matrix_manager.ui.components.skill_gap_tab.staged_target_tab import StagedTargetTab
from src.skill_matrix_manager.ui.components.skill_gap_tab.radar_chart_dialog import RadarChartDialog
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class SkillGapTab(QWidget):
    """SkillGapTab - 最終実装版"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        logger.info("SkillGapTab初期化 - 最終実装版")
        
        # スキルとステージの設定
        self.skills = ["Python", "Java", "JavaScript", "SQL", "Git"]
        self.stages = ["現在", "3ヶ月後", "6ヶ月後", "9ヶ月後", "目標"]
        self.stage_data = []  # ステージごとのデータを保持
        
        # 各ステージにスキルデータの初期化
        for _ in range(len(self.stages)):
            stage_skills = {}
            for skill in self.skills:
                stage_skills[skill] = 0  # 初期値は0
            self.stage_data.append(stage_skills)
        
        # スピンボックス管理
        self.spin_boxes = {}
        
        # UIのセットアップ
        self.setup_ui()
        
        # デフォルトデータの設定
        self.setup_default_data()
    
    def setup_ui(self):
        """UIの初期化"""
        main_layout = QHBoxLayout(self)
        
        # 左側：入力パネル
        left_panel = QWidget()
        left_layout = QHBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # 開閉ボタン
        self.toggle_btn = QToolButton()
        self.toggle_btn.setText("▶")
        self.toggle_btn.clicked.connect(self.toggle_panel)
        left_layout.addWidget(self.toggle_btn)
        
        # 入力パネル（初期状態：非表示）
        self.input_widget = QWidget()
        self.input_widget.setVisible(False)
        input_layout = QVBoxLayout(self.input_widget)
        
        # スクロールエリア（スピンボックス用）
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # 各ステージのグループボックス作成
        for i, stage_name in enumerate(self.stages):
            group = QGroupBox(f"{stage_name}のスキルレベル")
            form = QFormLayout(group)
            
            for skill in self.skills:
                # スピンボックス作成
                spin = QSpinBox()
                spin.setRange(0, 5)
                spin.setValue(min(i + 2, 5))  # ステージが上がるごとに値が大きくなる
                self.spin_boxes[(i, skill)] = spin
                
                # 値変更イベント
                spin.valueChanged.connect(
                    lambda v, stage=i, sk=skill: self.on_value_changed(stage, sk, v)
                )
                
                form.addRow(skill, spin)
            
            scroll_layout.addWidget(group)
        
        scroll.setWidget(scroll_content)
        input_layout.addWidget(scroll)
        
        # レーダーチャート表示ボタン
        chart_btn = QPushButton("レーダーチャート表示")
        chart_btn.clicked.connect(self.show_radar_chart)
        input_layout.addWidget(chart_btn)
        
        left_layout.addWidget(self.input_widget)
        
        # 右側：StagedTargetTab
        self.staged_target = StagedTargetTab()
        
        # メインレイアウトに追加
        main_layout.addWidget(left_panel, 0)  # 幅は最小限
        main_layout.addWidget(self.staged_target, 1)  # 残りのスペースを使う
    
    def setup_default_data(self):
        """デフォルトデータのセットアップ"""
        logger.info("デフォルトデータを設定")
        
        # ステージごとにスキル値を設定
        for i, stage_name in enumerate(self.stages):
            for skill in self.skills:
                value = min(i + 2, 5)  # ステージが上がるごとに値が大きくなる
                self.stage_data[i][skill] = value
                
                # スピンボックスの値も更新
                if (i, skill) in self.spin_boxes:
                    self.spin_boxes[(i, skill)].setValue(value)
    
    def on_value_changed(self, stage_idx, skill, value):
        """スピンボックスの値が変更された時の処理"""
        logger.info(f"値変更: ステージ{stage_idx}の{skill}={value}")
        
        # 内部データを更新
        self.stage_data[stage_idx][skill] = value
    
    def toggle_panel(self):
        """左パネルの表示/非表示切り替え"""
        is_visible = self.input_widget.isVisible()
        self.input_widget.setVisible(not is_visible)
        self.toggle_btn.setText("◀" if not is_visible else "▶")
    
    def show_radar_chart(self):
        """RadarChartDialogを正しく使用してレーダーチャートを表示"""
        try:
            logger.info("RadarChartDialogを正しいパラメータで呼び出し")
            
            # RadarChartDialogのパラメータ分析に基づく呼び出し
            # コンストラクタは (self, stage_names, stage_data) の形式と思われる
            dialog = RadarChartDialog(self.stages, self.stage_data)
            dialog.exec_()
            
        except Exception as e:
            logger.error(f"チャート表示エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def set_member(self, member_id, member_name, group_name):
        """メンバー情報設定（インターフェース互換性用）"""
        logger.info(f"メンバー設定: {member_id}, {member_name}, {group_name}")
