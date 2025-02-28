#!/usr/bin/env python3
"""スキルギャップタブ機能テスト用スクリプト"""

import sys
import os
import traceback

# パスを追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# デバッグ用ロガー
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

logger.info("====== test_skill_gap.py 実行開始 ======")

try:
    from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTabWidget, QLabel, QMessageBox
    
    # スキルギャップタブを直接インポート（循環インポートを回避）
    logger.info("SkillGapTab のインポート開始")
    # ここでインポートエラーが発生する可能性があります
    from src.skill_matrix_manager.ui.components.skill_gap_tab_impl import SkillGapTab
    logger.info("SkillGapTab のインポート成功")

    class TestWindow(QMainWindow):
        """テスト用ウィンドウ"""
        
        def __init__(self):
            try:
                logger.info("TestWindow.__init__ 開始")
                super().__init__()
                self.setWindowTitle("スキルギャップタブテスト")
                self.setGeometry(100, 100, 1000, 700)
                
                # メインウィジェット
                central_widget = QWidget()
                self.setCentralWidget(central_widget)
                layout = QVBoxLayout(central_widget)
                
                # インポート検証ラベル
                status_label = QLabel("SkillGapTab がインポートされました")
                status_label.setStyleSheet("font-size: 14pt; color: green;")
                layout.addWidget(status_label)
                
                # スキルギャップタブ
                logger.info("SkillGapTab のインスタンス化")
                try:
                    self.skill_gap_tab = SkillGapTab()
                    logger.info("SkillGapTab のインスタンス化成功")
                    
                    # テスト用にダミーのメンバーデータを設定
                    logger.info("ダミーメンバーデータの設定")
                    self.skill_gap_tab.set_member(
                        "user1", 
                        "佐藤太郎", 
                        "開発チーム"
                    )
                    
                    layout.addWidget(self.skill_gap_tab)
                except Exception as e:
                    logger.error(f"SkillGapTab のインスタンス化でエラー: {e}")
                    logger.error(traceback.format_exc())
                    error_label = QLabel(f"SkillGapTabのロードに失敗しました:\n{str(e)}")
                    error_label.setStyleSheet("color: red;")
                    layout.addWidget(error_label)
                
                logger.info("TestWindow.__init__ 完了")
            except Exception as e:
                logger.error(f"TestWindow.__init__ でエラー: {e}")
                logger.error(traceback.format_exc())
                QMessageBox.critical(None, "初期化エラー", f"ウィンドウ初期化中にエラーが発生しました:\n{str(e)}")

    # メイン処理
    if __name__ == "__main__":
        logger.info("アプリケーション初期化")
        app = QApplication(sys.argv)
        app.setStyle("Fusion")
        
        try:
            logger.info("テストウィンドウ作成")
            window = TestWindow()
            logger.info("テストウィンドウ表示")
            window.show()
            logger.info("アプリケーション実行")
            sys.exit(app.exec_())
        except Exception as e:
            logger.error(f"アプリケーションの実行中にエラー: {e}")
            logger.error(traceback.format_exc())
            QMessageBox.critical(None, "実行エラー", f"アプリケーションの実行中にエラーが発生しました:\n{str(e)}")

except ImportError as e:
    logger.error(f"インポートエラー: {e}")
    logger.error(traceback.format_exc())
    
    # GUIがなくてもエラーメッセージを表示できるようにする
    print(f"エラー: {e}")
    print("必要なモジュールをインポートできませんでした。")
    print("詳細はログファイルを確認してください。")
    sys.exit(1)
except Exception as e:
    logger.error(f"予期しない例外: {e}")
    logger.error(traceback.format_exc())
    print(f"予期しないエラーが発生しました: {e}")
    sys.exit(1)