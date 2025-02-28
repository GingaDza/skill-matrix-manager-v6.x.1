"""デバッグユーティリティ - 問題の診断と原因特定を支援"""
import sys
import os
import inspect
import traceback
import importlib

from .debug_logger import DebugLogger
logger = DebugLogger.get_logger()

def print_system_info():
    """システム情報を出力"""
    logger.info("=== システム情報 ===")
    logger.info(f"Python バージョン: {sys.version}")
    logger.info(f"実行ファイル: {sys.executable}")
    logger.info(f"作業ディレクトリ: {os.getcwd()}")
    logger.info(f"sys.path: {sys.path}")

def check_module_path(module_name):
    """モジュールのパスを確認"""
    try:
        module = importlib.import_module(module_name)
        logger.info(f"モジュール {module_name} のパス: {module.__file__}")
        return module.__file__
    except ImportError as e:
        logger.error(f"モジュール {module_name} のインポートエラー: {e}")
        return None
    except Exception as e:
        logger.error(f"モジュール {module_name} の確認中にエラー: {e}")
        return None

def inspect_object(obj, name="オブジェクト"):
    """オブジェクトの情報を表示"""
    logger.info(f"=== {name} の情報 ===")
    logger.info(f"タイプ: {type(obj)}")
    logger.info(f"ID: {id(obj)}")
    logger.info(f"__dict__: {obj.__dict__ if hasattr(obj, '__dict__') else 'なし'}")
    logger.info(f"dir(): {dir(obj)}")

def debug_import(module_path):
    """インポートの問題をデバッグ"""
    logger.info(f"=== モジュール {module_path} のインポートデバッグ ===")
    
    # インポートの試行
    try:
        module = importlib.import_module(module_path)
        logger.info(f"インポート成功: {module}")
        return module
    except ImportError as e:
        logger.error(f"インポートエラー: {e}")
        logger.error(f"スタックトレース:\n{traceback.format_exc()}")
        
        # モジュールパスの各部分を確認
        parts = module_path.split('.')
        for i in range(1, len(parts) + 1):
            partial_path = '.'.join(parts[:i])
            try:
                partial_module = importlib.import_module(partial_path)
                logger.info(f"部分パス {partial_path} はインポート可能: {partial_module.__file__}")
            except ImportError as inner_e:
                logger.error(f"部分パス {partial_path} はインポート不可: {inner_e}")
        
        return None
    except Exception as e:
        logger.error(f"予期せぬエラー: {e}")
        logger.error(f"スタックトレース:\n{traceback.format_exc()}")
        return None

def debug_traceback(message="例外発生"):
    """現在のスタックトレースを出力"""
    stack = traceback.format_stack()
    logger.debug(f"{message}\nスタックトレース:\n{''.join(stack)}")
