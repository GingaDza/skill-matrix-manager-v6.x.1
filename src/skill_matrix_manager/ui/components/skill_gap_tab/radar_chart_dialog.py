"""レーダーチャートダイアログ - スキルギャップの視覚化用ダイアログ"""

import math
import traceback
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QComboBox, QCheckBox
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

class RadarChartDialog(QDialog):
    """スキルレベルをレーダーチャートで表示するダイアログ"""
    
    def __init__(self, parent, stages_data):
        super().__init__(parent)
        logger.info(f"RadarChartDialog初期化: {len(stages_data)}個のステージデータ")
        
        self.stages_data = stages_data
        self.selected_stages = [True] * len(stages_data)  # 初期状態ですべて選択
        
        self.setWindowTitle("スキルレーダーチャート")
        self.setMinimumSize(800, 600)
        
        self.setup_ui()
    
    def setup_ui(self):
        """UIの初期化"""
        main_layout = QVBoxLayout(self)
        
        # チャート表示エリア
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)
        
        # 表示制御エリア
        control_layout = QHBoxLayout()
        
        # ステージ選択チェックボックスエリア
        stage_layout = QHBoxLayout()
        stage_label = QLabel("表示ステージ:")
        stage_layout.addWidget(stage_label)
        
        # 各ステージのチェックボックス
        self.stage_checkboxes = []
        for i, stage in enumerate(self.stages_data):
            checkbox = QCheckBox(stage["name"])
            checkbox.setChecked(True)  # 初期状態で選択
            checkbox.stateChanged.connect(
                lambda state, idx=i: self.on_stage_checked(idx, state)
            )
            stage_layout.addWidget(checkbox)
            self.stage_checkboxes.append(checkbox)
        
        control_layout.addLayout(stage_layout)
        control_layout.addStretch(1)
        
        # ボタンエリア
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.accept)
        control_layout.addWidget(close_btn)
        
        main_layout.addLayout(control_layout)
        
        # 初期表示
        self.draw_radar_chart()
    
    def on_stage_checked(self, stage_index, state):
        """ステージの選択状態が変更されたときの処理"""
        self.selected_stages[stage_index] = (state == Qt.Checked)
        self.draw_radar_chart()
    
    def draw_radar_chart(self):
        """レーダーチャートの描画"""
        try:
            # 図をクリア
            self.figure.clear()
            
            # データの準備
            # スキル名のリスト (最初のステージから取得)
            if not self.stages_data or not self.stages_data[0]['targets']:
                logger.warning("チャートを描画するデータがありません")
                return
            
            # すべてのスキルIDを集める (どのステージにも存在するもの)
            all_skills = set()
            for stage in self.stages_data:
                all_skills.update(stage['targets'].keys())
            
            # サンプルスキル名 (実際のアプリではスキルIDからスキル名を取得)
            skill_names = {
                "python": "Python",
                "sql": "SQL",
                "ui_design": "UI/UX設計",
                "project_mgmt": "プロジェクト管理",
                "communication": "コミュニケーション"
            }
            
            # スキルのリスト (名前があるもののみ)
            skills = [skill_id for skill_id in all_skills if skill_id in skill_names]
            skill_labels = [skill_names.get(skill_id, skill_id) for skill_id in skills]
            
            # スキルの数を確認
            n_skills = len(skills)
            if n_skills == 0:
                logger.warning("表示するスキルがありません")
                return
            
            logger.info(f"レーダーチャート描画: {n_skills}個のスキル, {len(self.stages_data)}個のステージ")
            
            # 角度の計算
            angles = np.linspace(0, 2*math.pi, n_skills, endpoint=False).tolist()
            angles += angles[:1]  # 閉じたポリゴンにするため最初の点を最後にも追加
            
            # サブプロットの作成
            ax = self.figure.add_subplot(111, polar=True)
            
            # 色のリスト
            colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
            
            # 選択されたステージのデータをプロット
            for i, stage in enumerate(self.stages_data):
                if not self.selected_stages[i]:
                    continue  # 選択されていないステージはスキップ
                
                # このステージの各スキルのレベル値を取得
                values = []
                for skill_id in skills:
                    values.append(stage['targets'].get(skill_id, 0))
                
                # 閉じたポリゴンにするため最初の点を最後にも追加
                values += values[:1]
                
                # プロット
                logger.info(f"プロット: {stage['name']}, {len(values)}個の値")
                ax.plot(angles, values, linewidth=1, linestyle='solid', label=stage['name'], color=colors[i % len(colors)])
                ax.fill(angles, values, alpha=0.1, color=colors[i % len(colors)])
            
            # 角度ラベルの設定
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(skill_labels)
            
            # y軸の設定
            ax.set_yticks([1, 2, 3, 4, 5])
            ax.set_ylim(0, 5)
            
            # グリッドとレジェンドの設定
            ax.grid(True)
            ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
            
            # グラフのタイトル
            self.figure.suptitle("スキルレベルレーダーチャート", fontsize=14)
            
            # キャンバスを更新
            self.canvas.draw()
            
        except Exception as e:
            logger.error(f"レーダーチャート描画でエラー: {e}")
            logger.error(traceback.format_exc())
