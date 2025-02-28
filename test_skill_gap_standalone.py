#!/usr/bin/env python3
"""スキルギャップタブ単体テスト用スクリプト"""

import sys
import os
import traceback

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# デバッグ用ロガー
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

logger.info("====== スタンドアロンテスト開始 ======")

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
    # 絶対パスでインポート
    from src.skill_matrix_manager.ui.components.skill_gap_tab_impl import SkillGapTab
    
    app = QApplication(sys.argv)
    
    # シンプルなテストウィンドウ
    window = QMainWindow()
    window.setWindowTitle("スキルギャップタブ単体テスト")
    window.setGeometry(100, 100, 800, 600)
    
    # 中央ウィジェット
    central = QWidget()
    layout = QVBoxLayout(central)
    
    # スキルギャップタブを表示
    skill_gap_tab = SkillGapTab()
    skill_gap_tab.set_member("test1", "テストユーザー", "テストグループ")
    layout.addWidget(skill_gap_tab)
    
    window.setCentralWidget(central)
    window.show()
    
    sys.exit(app.exec_())
except ImportError as e:
    logger.error(f"インポートエラー: {e}")
    logger.error(traceback.format_exc())
    print(f"モジュールインポートエラー: {e}")
except Exception as e:
    logger.error(f"予期しない例外: {e}")
    logger.error(traceback.format_exc())
    print(f"エラー: {e}")
