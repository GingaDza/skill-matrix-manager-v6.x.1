"""スキルギャップタブ関連コンポーネント"""
import traceback
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
logger = DebugLogger.get_logger()

logger.info("===== skill_gap_tab パッケージの初期化開始 =====")

# 直接インポートできるようにパッケージ内のクラスをエクスポート
try:
    logger.info("StagedTargetTabのインポート試行")
    from .staged_target_tab import StagedTargetTab
    logger.info("StagedTargetTabインポート成功")
except ImportError as e:
    logger.error(f"StagedTargetTabのインポートエラー: {e}")
    logger.error(traceback.format_exc())

try:
    logger.info("RadarChartDialogのインポート試行")
    from .radar_chart_dialog import RadarChartDialog
    logger.info("RadarChartDialogインポート成功")
except ImportError as e:
    logger.error(f"RadarChartDialogのインポートエラー: {e}")
    logger.error(traceback.format_exc())

logger.info("===== skill_gap_tab パッケージの初期化完了 =====")
