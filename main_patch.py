#!/usr/bin/env python3
"""メインアプリケーション修正用パッチ"""

import sys
from PyQt5.QtWidgets import QApplication

from src.skill_matrix_manager.ui.main_window import MainWindow
from src.skill_matrix_manager.ui.main_window_helper import extend_main_window
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

def main():
    """メイン関数"""
    logger.info("アプリケーション起動")
    
    app = QApplication(sys.argv)
    
    # メインウィンドウの作成 - 初期化前にヘルパーをモンキーパッチ
    from src.skill_matrix_manager.ui import main_window
    original_init = main_window.MainWindow.__init__
    
    def patched_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        # メインウィンドウの拡張
        extend_main_window(self)
        
    main_window.MainWindow.__init__ = patched_init
    
    try:
        window = MainWindow()
        window.show()
        return app.exec_()
    except Exception as e:
        logger.error(f"アプリケーション実行中にエラー: {e}")
        logger.error(traceback.format_exc())
    finally:
        # データベース接続のクローズなど
        if 'window' in locals() and hasattr(window, 'cleanup'):
            window.cleanup()

if __name__ == "__main__":
    sys.exit(main())
