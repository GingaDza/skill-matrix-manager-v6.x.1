import os
import numpy as np
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QFormLayout, 
    QLabel, QGridLayout, QComboBox, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtGui import QFont
import tempfile
from datetime import datetime

# Matplotlibのインポート
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class SkillEvaluationTab(QWidget):
    skill_updated = pyqtSignal(str, str, int)  # member_id, skill_id, score

    def __init__(self, category_name, skills, parent=None):
        super().__init__(parent)
        self.category_name = category_name
        self.skills = skills
        self.current_values = [1] * len(skills)
        self.target_values = [5] * len(skills)
        self.skill_combos = []
        self.target_combos = []
        self.temp_files = []
        self.is_dark_mode = True
        self.current_member_id = None
        self.current_member_name = None
        self.current_member_group = None
        self.evaluations = {}  # {member_id: {skill_id: score}}
        self.last_update_time = "2025-02-21 13:34:46"
        self.current_user = "GingaDza"
        
        # 既存の色設定はそのまま維持
        self.dark_colors = {
            'current': {
                'line': 'rgb(189, 147, 249)',
                'fill': 'rgba(189, 147, 249, 0.3)',
                'text': '現在のスキル (1-5)'
            },
            'target': {
                'line': 'rgb(255, 184, 108)',
                'fill': 'rgba(255, 184, 108, 0.1)',
                'text': '目標スキル (1-5)'
            },
            'background': 'rgb(40, 42, 54)',
            'grid': 'rgb(68, 71, 90)',
            'text': 'rgb(248, 248, 242)',
            'paper_bg': 'rgb(40, 42, 54)',
            'plot_bg': 'rgb(40, 42, 54)'
        }

        self.light_colors = {
            'current': {
                'line': 'rgb(147, 112, 219)',
                'fill': 'rgba(147, 112, 219, 0.3)',
                'text': '現在のスキル (1-5)'
            },
            'target': {
                'line': 'rgb(251, 140, 0)',
                'fill': 'rgba(251, 140, 0, 0.1)',
                'text': '目標スキル (1-5)'
            },
            'background': 'rgb(255, 255, 255)',
            'grid': 'rgb(238, 238, 238)',
            'text': 'rgb(60, 64, 67)',
            'paper_bg': 'rgb(255, 255, 255)',
            'plot_bg': 'rgb(255, 255, 255)'
        }
        
        self.colors = self.dark_colors if self.is_dark_mode else self.light_colors
        
        # スタイルシートは既存のものを維持
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(40, 42, 54);
                color: rgb(248, 248, 242);
            }
            QGroupBox {
                margin-top: 1.2em;
                border: 1px solid rgb(68, 71, 90);
                border-radius: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0 5px;
                background-color: rgb(40, 42, 54);
                color: rgb(248, 248, 242);
            }
            QComboBox {
                background-color: rgb(68, 71, 90);
                border: 1px solid rgb(98, 114, 164);
                border-radius: 4px;
                padding: 2px;
                color: rgb(248, 248, 242);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        
        self._setup_ui()

    def _setup_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        
        # 上部コンテナ
        top_container = QWidget()
        top_layout = QHBoxLayout(top_container)
        top_layout.setSpacing(10)
        
        # ユーザー情報セクション
        self.user_info_group = QGroupBox("評価対象: 未選択")
        user_layout = QFormLayout()
        user_layout.setSpacing(10)
        user_layout.setContentsMargins(10, 15, 10, 10)
        
        self.user_name_label = QLabel("メンバー: 未選択")
        self.date_label = QLabel(f"最終更新: {self.last_update_time}")
        self.evaluator_label = QLabel(f"評価者: {self.current_user}")
        
        user_layout.addRow(self.user_name_label)
        user_layout.addRow(self.date_label)
        user_layout.addRow(self.evaluator_label)
        self.user_info_group.setLayout(user_layout)
        
        self.user_info_group.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        top_layout.addWidget(self.user_info_group)
        
        # スキル評価セクション
        skill_group = QGroupBox("スキル評価")
        skill_layout = QGridLayout()
        skill_layout.setSpacing(10)
        skill_layout.setContentsMargins(10, 15, 10, 10)
        
        # ヘッダー
        skill_layout.addWidget(QLabel("スキル"), 0, 0)
        current_label = QLabel("現在値")
        current_label.setStyleSheet(f"color: {self.colors['current']['line']}")
        target_label = QLabel("目標値")
        target_label.setStyleSheet(f"color: {self.colors['target']['line']}")
        skill_layout.addWidget(current_label, 0, 1)
        skill_layout.addWidget(target_label, 0, 2)
        
        skill_layout.setColumnStretch(0, 2)
        skill_layout.setColumnStretch(1, 1)
        skill_layout.setColumnStretch(2, 1)
        
        for i, skill in enumerate(self.skills, 1):
            skill_label = QLabel(skill)
            skill_layout.addWidget(skill_label, i, 0)
            
            current_combo = QComboBox()
            current_combo.addItems([str(x) for x in range(1, 6)])
            current_combo.setCurrentText("1")
            current_combo.currentTextChanged.connect(
                lambda value, idx=i-1: self.on_skill_level_changed(idx, value)
            )
            current_combo.setStyleSheet(f"color: {self.colors['current']['line']}")
            self.skill_combos.append(current_combo)
            skill_layout.addWidget(current_combo, i, 1)
            
            target_combo = QComboBox()
            target_combo.addItems([str(x) for x in range(1, 6)])
            target_combo.setCurrentText("5")
            target_combo.currentTextChanged.connect(
                lambda value, idx=i-1: self.on_target_level_changed(idx, value)
            )
            target_combo.setStyleSheet(f"color: {self.colors['target']['line']}")
            self.target_combos.append(target_combo)
            skill_layout.addWidget(target_combo, i, 2)
        
        skill_group.setLayout(skill_layout)
        skill_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_layout.addWidget(skill_group)
        
        main_layout.addWidget(top_container)
        
        # チャートコンテナの部分だけ変更
        chart_container = QWidget()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        
        chart_group = QGroupBox("スキルレーダーチャート")
        chart_group_layout = QVBoxLayout()
        chart_group_layout.setContentsMargins(10, 15, 10, 10)
        
        # WebEngineViewの代わりにMatplotlibのFigureCanvasを使用
        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumSize(400, 400)
        
        chart_group_layout.addWidget(self.canvas)
        chart_group.setLayout(chart_group_layout)
        
        chart_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        chart_layout.addWidget(chart_group)
        
        chart_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(chart_container)
        
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)
        
        self.setLayout(main_layout)
        self.update_chart()

    def create_radar_chart(self):
        """Matplotlibを使ったレーダーチャートを作成"""
        # 図をクリア
        self.figure.clear()
        
        # 極座標のサブプロットを追加
        ax = self.figure.add_subplot(111, polar=True)
        
        # データ準備
        categories = self.skills
        num_vars = len(categories)
        
        # 角度の計算 (時計回り、最初のカテゴリを上部に)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        
        # 閉じた図形にするため、最初の値を最後にも追加
        current_values = self.current_values + [self.current_values[0]]
        target_values = self.target_values + [self.target_values[0]]
        categories = categories + [categories[0]]
        angles = angles + [angles[0]]
        
        # 背景色の設定
        if self.is_dark_mode:
            # RGB文字列をタプルに変換
            bg_color = tuple(int(x) for x in self.colors['paper_bg'].replace('rgb(', '').replace(')', '').split(','))
            bg_color = (bg_color[0]/255, bg_color[1]/255, bg_color[2]/255)
            self.figure.patch.set_facecolor(bg_color)
            ax.set_facecolor(bg_color)
        
        # Y軸の範囲を設定
        ax.set_ylim(0, 5)
        
        # 目標値のプロット (点線)
        # RGB文字列をタプルに変換
        target_color = tuple(int(x) for x in self.colors['target']['line'].replace('rgb(', '').replace(')', '').split(','))
        target_color = (target_color[0]/255, target_color[1]/255, target_color[2]/255)
        
        ax.plot(angles, target_values, 'o-', linewidth=1, 
                linestyle='dashed', color=target_color, 
                label=self.colors['target']['text'])
        ax.fill(angles, target_values, alpha=0.1, color=target_color)
        
        # 現在値のプロット (実線)
        # RGB文字列をタプルに変換
        current_color = tuple(int(x) for x in self.colors['current']['line'].replace('rgb(', '').replace(')', '').split(','))
        current_color = (current_color[0]/255, current_color[1]/255, current_color[2]/255)
        
        ax.plot(angles, current_values, 'o-', linewidth=1.5,
                color=current_color, 
                label=self.colors['current']['text'])
        ax.fill(angles, current_values, alpha=0.25, color=current_color)
        
        # 目盛りの設定
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories[:-1])
        
        # テキスト色の設定
        text_color = tuple(int(x) for x in self.colors['text'].replace('rgb(', '').replace(')', '').split(','))
        text_color = (text_color[0]/255, text_color[1]/255, text_color[2]/255)
        
        for label in ax.get_xticklabels():
            label.set_color(text_color)
        
        # Y軸の目盛りを設定
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'])
        
        for label in ax.get_yticklabels():
            label.set_color(text_color)
        
        # グリッドの色を設定
        grid_color = tuple(int(x) for x in self.colors['grid'].replace('rgb(', '').replace(')', '').split(','))
        grid_color = (grid_color[0]/255, grid_color[1]/255, grid_color[2]/255, 0.5)
        ax.grid(True, color=grid_color)
        
        # タイトルを追加
        ax.set_title(f"{self.category_name}のスキル評価", 
                    color=text_color,
                    fontsize=14, pad=20)
        
        # 凡例を追加
        legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                          fancybox=True, shadow=True, ncol=2)
        
        # 凡例のテキスト色を設定
        for text in legend.get_texts():
            text.set_color(text_color)
        
        # レイアウトの調整
        self.figure.tight_layout()
        self.canvas.draw()
        
        return None  # HTMLファイルを返す必要はなくなった

    def update_chart(self):
        """チャートを更新"""
        try:
            self.create_radar_chart()  # HTMLファイル生成ではなく直接描画
        except Exception as e:
            print(f"Error updating chart: {e}")
            import traceback
            traceback.print_exc()

    def set_member(self, member_id, member_name, member_group):
        """メンバーが選択された時の処理"""
        self.current_member_id = member_id
        self.current_member_name = member_name
        self.current_member_group = member_group
        
        # ユーザー情報の更新
        self.user_info_group.setTitle(f"評価対象: {member_name}")
        self.user_name_label.setText(f"メンバー: {member_name} ({member_group})")
        self.date_label.setText(f"最終更新: {self.last_update_time}")
        
        # 保存済みの評価を読み込む
        self.load_member_evaluations()

    def load_member_evaluations(self):
        """メンバーの評価データを読み込む"""
        if not self.current_member_id:
            return

        member_evals = self.evaluations.get(self.current_member_id, {})
        for i, skill in enumerate(self.skills):
            score = member_evals.get(skill, 1)
            self.current_values[i] = score
            self.skill_combos[i].setCurrentText(str(score))

        self.update_chart()

    def on_skill_level_changed(self, index, value):
        """スキルレベルが変更された時の処理（自動保存含む）"""
        try:
            self.current_values[index] = int(value)
            
            # 自動保存の処理
            if self.current_member_id:
                skill_id = self.skills[index]
                score = int(value)
                
                if self.current_member_id not in self.evaluations:
                    self.evaluations[self.current_member_id] = {}
                
                self.evaluations[self.current_member_id][skill_id] = score
                
                # 保存時刻の更新
                self.last_update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.date_label.setText(f"最終更新: {self.last_update_time}")
                
                # シグナル発信
                self.skill_updated.emit(self.current_member_id, skill_id, score)
            
            self.update_chart()
            
        except (ValueError, IndexError) as e:
            print(f"Error updating skill level: {e}")

    def on_target_level_changed(self, index, value):
        """目標レベルが変更された時の処理"""
        try:
            self.target_values[index] = int(value)
            self.update_chart()
        except (ValueError, IndexError) as e:
            print(f"Error updating target level: {e}")

    def closeEvent(self, event):
        """ウィンドウが閉じられる時の処理"""
        # 一時ファイルの削除（不要になった）
        super().closeEvent(event)
        
    def update_color_mode(self):
        """カラーモードの更新"""
        self.colors = self.dark_colors if self.is_dark_mode else self.light_colors
        
        # スタイルシートの更新
        dark_style = """
            QWidget {
                background-color: rgb(40, 42, 54);
                color: rgb(248, 248, 242);
            }
            QGroupBox {
                margin-top: 1.2em;
                border: 1px solid rgb(68, 71, 90);
                border-radius: 4px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 7px;
                padding: 0 5px;
                background-color: rgb(40, 42, 54);
                color: rgb(248, 248, 242);
            }
            QComboBox {
                background-color: rgb(68, 71, 90);
                border: 1px solid rgb(98, 114, 164);
                border-radius: 4px;
                padding: 2px;
                color: rgb(248, 248, 242);
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """
        
        light_style = ""
        
        self.setStyleSheet(dark_style if self.is_dark_mode else light_style)
        self.update_chart()