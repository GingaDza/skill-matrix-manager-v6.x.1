#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import QApplication
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
from src.skill_matrix_manager.ui.components.skill_gap_tab.staged_target_tab import StagedTargetTab

logger = DebugLogger.get_logger()

def inspect():
    logger.info("StagedTargetTab構造調査を開始")
    
    try:
        # QApplicationのインスタンス化が必要
        app = QApplication(sys.argv)
        
        tab = StagedTargetTab()
        # 属性の確認
        attrs = [attr for attr in dir(tab) if not attr.startswith('__')]
        logger.info(f"StagedTargetTabの主な属性: {attrs}")
        
        # 主要属性の型確認
        for attr in attrs:
            if hasattr(tab, attr) and not callable(getattr(tab, attr)):
                try:
                    logger.info(f"属性 {attr} の型: {type(getattr(tab, attr))}")
                    # 配列や辞書の場合は内容も表示
                    value = getattr(tab, attr)
                    if isinstance(value, (list, dict)):
                        logger.info(f"属性 {attr} の内容: {value}")
                except:
                    logger.info(f"属性 {attr} の内容取得に失敗")
        
        # メソッドの確認
        methods = [attr for attr in dir(tab) if callable(getattr(tab, attr)) and not attr.startswith('__')]
        logger.info(f"StagedTargetTabのメソッド: {methods}")
        
        # RadarChartDialogの調査
        logger.info("RadarChartDialogの調査")
        from src.skill_matrix_manager.ui.components.skill_gap_tab.radar_chart_dialog import RadarChartDialog
        chart_methods = [attr for attr in dir(RadarChartDialog) if callable(getattr(RadarChartDialog, attr)) and not attr.startswith('__')]
        logger.info(f"RadarChartDialogのメソッド: {chart_methods}")
        
    except Exception as e:
        logger.error(f"調査中にエラー発生: {e}")
        import traceback
        traceback.print_exc()
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(inspect())
