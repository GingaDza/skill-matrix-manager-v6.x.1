#!/usr/bin/env python3
"""レーダーチャートウィジェット"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QSizePolicy
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class RadarChart(FigureCanvas):
    """レーダーチャートを描画するウィジェット"""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        """初期化"""
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111, polar=True)
        
        # キャンバス初期化
        super().__init__(self.fig)
        self.setParent(parent)
        
        # サイズポリシー設定
        FigureCanvas.setSizePolicy(self,
                                  QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        # データ初期化
        self.categories = []
        self.current_values = []
        self.target_values = []
        self.max_value = 5  # スキルレベルの最大値
        
        self._setup_chart()
    
    def _setup_chart(self):
        """チャートの基本設定"""
        self.axes.clear()
        self.axes.set_theta_zero_location('N')  # 上部から開始
        self.axes.set_theta_direction(-1)  # 時計回り
        self.axes.set_ylim(0, self.max_value)
        self.axes.grid(True)
    
    def update_chart(self, categories, current_values, target_values=None, title=None):
        """チャートのデータを更新して描画"""
        if not categories or not current_values:
            logger.warning("レーダーチャート更新: データが空です")
            return
            
        if len(categories) != len(current_values):
            logger.error("レーダーチャート更新: カテゴリとデータの長さが一致しません")
            return
        
        # データ保存
        self.categories = categories
        self.current_values = current_values
        self.target_values = target_values or []
        
        # チャート描画
        self._draw_chart(title)
    
    def _draw_chart(self, title=None):
        """チャートを描画"""
        try:
            # 設定をリセット
            self._setup_chart()
            
            # カテゴリ数に応じた角度を計算
            N = len(self.categories)
            if N < 3:
                logger.warning("レーダーチャート描画: カテゴリが3つ未満です")
                return
                
            angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
            
            # 閉じた形にするため、最初の点を最後にも追加
            values = self.current_values + [self.current_values[0]]
            angles = angles + [angles[0]]
            
            # 現在値のプロット
            self.axes.plot(angles, values, 'o-', linewidth=2, label='現在')
            self.axes.fill(angles, values, alpha=0.25)
            
            # 目標値がある場合は描画
            if self.target_values and len(self.target_values) == N:
                target_values = self.target_values + [self.target_values[0]]
                self.axes.plot(angles, target_values, 'o--', linewidth=2, label='目標')
            
            # カテゴリラベル設定
            self.axes.set_xticks(angles[:-1])
            self.axes.set_xticklabels(self.categories)
            
            # タイトル設定
            if title:
                self.axes.set_title(title)
            
            # 凡例表示
            if self.target_values:
                self.axes.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            
            self.draw()
            logger.info(f"レーダーチャート描画: {N}項目")
            
        except Exception as e:
            logger.error(f"レーダーチャート描画エラー: {e}")
