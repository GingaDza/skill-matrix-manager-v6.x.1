#!/usr/bin/env python3
"""デバッグログユーティリティ"""

import logging
import os
import getpass
from datetime import datetime

class DebugLogger:
    """デバッグロガークラス"""
    
    _logger = None
    
    @classmethod
    def get_logger(cls):
        """シングルトンロガーを取得"""
        if cls._logger is None:
            cls._logger = cls._create_logger()
        return cls._logger
    
    @staticmethod
    def _create_logger():
        """ロガーを作成"""
        # ルートディレクトリのパスを取得
        root_dir = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '../../../'
        ))
        
        # ロガーの設定
        logger = logging.getLogger('skill_matrix')
        logger.setLevel(logging.INFO)
        
        # 既存のハンドラがあれば削除
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # コンソールハンドラ
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
        
        # ファイルハンドラ
        log_file = os.path.join(root_dir, 'app_log.txt')
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        # アプリケーション起動を記録
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        username = getpass.getuser()
        
        # 起動情報をログファイルに直接書き込み
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"Application started at: {current_time}\n")
            f.write(f"User: {username}\n")
            f.write(f"Dark Mode: False\n")
            f.write("-" * 50 + "\n")
        
        return logger
