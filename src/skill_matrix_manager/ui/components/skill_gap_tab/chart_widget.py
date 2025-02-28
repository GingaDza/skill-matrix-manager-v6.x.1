import logging
import logging
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict
from ....utils.debug_logger import DebugLogger

logger = logging.getLogger(__name__)

class RadarChartWidget(QWidget):
    def __init__(self, title: str = "", parent=None):
        super().__init__(parent)
        self.title = title
        self._setup_ui()
        logger.debug(f"RadarChartWidget initialized with title: {title}")

    def _setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)  # マージンを削除
        
        # Matplotlibのfigureを作成
        self.figure = Figure(figsize=(10, 6))  # サイズを固定
        self.figure.set_dpi(100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # ウィジェットサイズを固定
        self.setMinimumSize(QSize(800, 500))
        self.setMaximumSize(QSize(800, 500))
        
        self.setLayout(layout)

    def update_progressive_chart(self, categories: List[str], current_values: List[float], stages: List[Dict]):
        """段階的な目標値をレーダーチャートで表示"""
        logger.debug(f"Updating chart with: categories={categories}, current_values={current_values}, stages={stages}")
        
        self.figure.clear()
        
        # グリッドのサイズを調整（タイトル用のスペースを確保）
        gs = self.figure.add_gridspec(2, 2, height_ratios=[0.1, 0.9], width_ratios=[1, 2])
        
        # タイトルを追加（左上）
        title_ax = self.figure.add_subplot(gs[0, 0])
        title_ax.axis('off')
        title_ax.text(0.5, 0.5, self.title,
                     horizontalalignment='center',
                     verticalalignment='center',
                     fontsize=12,
                     fontweight='bold')
        
        # 凡例用のスペース（左下）
        ax_legend = self.figure.add_subplot(gs[1, 0])
        ax_legend.axis('off')
        
        # チャート用のスペース（右側全体）
        ax = self.figure.add_subplot(gs[:, 1], projection='polar')
        
        # データの準備
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]  # 閉じた図形にするため最初の点を最後にも追加
        
        # プロットの設定
        ax.set_theta_offset(np.pi / 2)  # 最初の要素を上部に配置
        ax.set_theta_direction(-1)  # 時計回り
        
        # 目盛りの設定
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        
        # グリッドの設定
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # 色の設定
        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(stages) + 1))
        legend_handles = []
        
        # 現在値を1に設定してプロット
        current_values = [1] * len(categories)  # すべての現在値を1に設定
        current_values_plot = current_values + [current_values[0]]
        ax.fill(angles, current_values_plot, alpha=0.25, color=colors[0])
        current_line = ax.plot(angles, current_values_plot, 'o-', 
                             linewidth=2, color=colors[0], markersize=8)[0]
        legend_handles.append((current_line, '現在'))
        
        # ステージを時間順にソート
        sorted_stages = sorted(stages, 
                             key=lambda x: self._convert_to_hours(x['time'], x['unit']))
        
        # 各ステージのプロット
        for i, stage in enumerate(sorted_stages, 1):
            # 各カテゴリーの値を取得
            stage_values = [stage['targets'].get(cat, 1) for cat in categories]
            stage_values += [stage_values[0]]  # 閉じた図形にする
            
            color = colors[i]
            ax.fill(angles, stage_values, alpha=0.25, color=color)
            line = ax.plot(angles, stage_values, 'o-', 
                         linewidth=1.5, color=color, markersize=6)[0]
            legend_handles.append((line, f"{stage['time']}{stage['unit']}後"))
            
            logger.debug(f"Plotted stage {stage['time']}{stage['unit']} with values: {stage_values}")
        
        # 凡例の表示位置を調整
        for line, label in legend_handles:
            ax_legend.plot([], [], color=line.get_color(), 
                         linewidth=line.get_linewidth(),
                         marker='o', markersize=8, label=label)
        
        legend = ax_legend.legend(loc='center',
                                bbox_to_anchor=(0.5, 0.5),
                                fontsize=10,
                                frameon=True,
                                edgecolor='gray',
                                fancybox=True,
                                shadow=True)
        
        # レイアウトの調整
        self.figure.tight_layout()
        self.canvas.draw()
        
        logger.debug("Chart update completed")

    def _convert_to_hours(self, time: int, unit: str) -> int:
        """時間単位を時間に変換"""
        multipliers = {
            "時間": 1,
            "日": 24,
            "月": 24 * 30,
            "年": 24 * 365
        }
        return time * multipliers.get(unit, 1)

