"""デバッグ情報を記録するためのロガー"""
import logging
import os
import sys
from datetime import datetime

class DebugLogger:
    """デバッグロガークラス"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls):
        """ロガーインスタンスを取得"""
        if cls._logger is None:
            # ロガーを初期化
            logger = logging.getLogger('skill_matrix_manager')
            logger.setLevel(logging.DEBUG)
            
            # コンソールハンドラの設定
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(console_format)
            logger.addHandler(console_handler)
            
            cls._logger = logger
        
        return cls._logger
