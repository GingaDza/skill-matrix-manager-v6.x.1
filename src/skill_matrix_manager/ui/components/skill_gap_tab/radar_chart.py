"""レーダーチャートウィジェット"""
import numpy as np
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class RadarChartWidget(QWidget):
    """Matplotlibを使用したレーダーチャートウィジェット"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """UIの初期設定"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Matplotlibの図を作成
        self.figure = Figure(figsize=(6, 6), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # 初期チャート表示
        self.display_empty_chart()
    
    def display_empty_chart(self):
        """空のレーダーチャートを表示"""
        self.figure.clear()
        ax = self.figure.add_subplot(111, polar=True)
        ax.set_title('スキルギャップ分析', size=14)
        ax.text(0, 0, "データがありません", 
                ha='center', va='center', fontsize=12, color='gray')
        self.canvas.draw()
    
    def update_chart(self, labels, current_values, target_values):
        """チャートを更新
        
        Args:
            labels (list): スキル名のリスト
            current_values (list): 現在のスキルレベル値のリスト
            target_values (list): 目標のスキルレベル値のリスト
        """
        # データが空の場合
        if not labels or not current_values or not target_values:
            self.display_empty_chart()
            return
        
        # 図をクリア
        self.figure.clear()
        
        # 極座標のサブプロットを追加
        ax = self.figure.add_subplot(111, polar=True)
        
        # 角度の計算（各スキルが均等に配置されるように）
        N = len(labels)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]  # 閉じた形にするために最初の点を追加
        
        # 現在値と目標値を角度に合わせて調整
        current = current_values + [current_values[0]]
        target = target_values + [target_values[0]]
        
        # レーダーチャートの描画
        ax.plot(angles, target, 'r-', linewidth=2, label='目標値')
        ax.fill(angles, target, 'r', alpha=0.1)
        
        ax.plot(angles, current, 'b-', linewidth=2, label='現在値')
        ax.fill(angles, current, 'b', alpha=0.1)
        
        # 目盛りの設定
        ax.set_thetagrids(np.degrees(angles[:-1]), labels)
        ax.set_ylim(0, 5)  # スキルレベルの範囲
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1', '2', '3', '4', '5'])
        ax.set_theta_zero_location('N')  # 0度を北に設定
        
        # タイトルと凡例
        ax.set_title('スキルギャップ分析', size=14)
        ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
        
        # キャンバスの更新
        self.canvas.draw()
