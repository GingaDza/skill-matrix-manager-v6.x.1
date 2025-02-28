#!/usr/bin/env python3
import sys
import os

# デバッグロガーの設定
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

def main():
    """テストウィンドウを表示して複数段階のレーダーチャートをテスト"""
    logger.info("移植版 StagedTargetTab テスト開始")
    
    try:
        # StagedTargetTab クラスのインポート
        from src.skill_matrix_manager.ui.components.skill_gap_tab.staged_target_tab import StagedTargetTab
        logger.info("StagedTargetTab クラスのインポート成功")
        
        # PyQt5のインポート
        from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
        
        # アプリケーションの作成
        app = QApplication(sys.argv)
        
        # メインウィンドウの作成
        window = QMainWindow()
        window.setWindowTitle("段階別レーダーチャートテスト")
        window.setGeometry(100, 100, 800, 600)
        
        # メインウィジェット
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # StagedTargetTab インスタンスの作成
        tab = StagedTargetTab()
        layout.addWidget(tab)
        
        # メインウィンドウに設定
        window.setCentralWidget(central_widget)
        
        # ウィンドウを表示
        logger.info("テストウィンドウを表示")
        window.show()
        
        # アプリケーションの実行
        sys.exit(app.exec_())
    
    except Exception as e:
        logger.error(f"テストエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
