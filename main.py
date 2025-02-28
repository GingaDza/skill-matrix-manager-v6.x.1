#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from src.skill_matrix_manager.ui.main_window import MainWindow

# デバッグ用ロガー
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

def main():
    try:
        logger.info("アプリケーション起動")
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        logger.info("メインウィンドウ表示")
        sys.exit(app.exec_())
    except Exception as e:
        logger.error(f"アプリケーション実行中にエラー: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()
