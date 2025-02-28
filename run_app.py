#!/usr/bin/env python3
"""スキルマトリクスマネージャーアプリケーション起動スクリプト"""

import sys
import os
import traceback

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# デバッグ用ロガー
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

logger.info("====== アプリケーション起動スクリプト実行開始 ======")

try:
    from PyQt5.QtWidgets import QApplication
    from src.skill_matrix_manager.main_window import MainWindow
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # スタイルシートの適用
    try:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    except ImportError:
        logger.warning("qdarkstyleをインポートできません。デフォルトスタイルを使用します。")
    
    # メインウィンドウを作成
    logger.info("メインウィンドウの作成")
    main_window = MainWindow()
    main_window.show()
    
    # アプリケーションの実行
    logger.info("アプリケーション実行")
    sys.exit(app.exec_())
    
except ImportError as e:
    logger.error(f"インポートエラー: {e}")
    logger.error(traceback.format_exc())
    print(f"必要なモジュールをインポートできません: {e}")
    sys.exit(1)
except Exception as e:
    logger.error(f"予期しない例外: {e}")
    logger.error(traceback.format_exc())
    print(f"アプリケーションの起動中にエラーが発生しました: {e}")
    sys.exit(1)
