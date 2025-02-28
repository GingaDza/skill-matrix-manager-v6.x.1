#!/usr/bin/env python3
"""構文エラーを修正するスクリプト"""

import os
import sys
from datetime import datetime

def backup_file(filepath):
    """ファイルのバックアップを作成"""
    if os.path.exists(filepath):
        dir_name = os.path.dirname(filepath)
        backup_dir = os.path.join(dir_name, "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        base_name = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{base_name}.{timestamp}")
        
        with open(filepath, 'r', encoding='utf-8') as src:
            with open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
        
        print(f"バックアップを作成しました: {backup_path}")
        return True
    return False

def fix_main_window_imports():
    """main_window.pyのインポート構文エラーを修正"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 修正されたコンテンツを作成
    fixed_content = []
    
    # importセクションを修正
    imports_added = False
    for line in lines:
        if not imports_added and line.startswith('import '):
            # 最初のimport文の前に必要なインポート文を追加
            fixed_content.append('from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, QSplitter, QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QComboBox, QHBoxLayout, QMessageBox, QInputDialog\n')
            fixed_content.append('from PyQt5.QtCore import Qt\n')
            fixed_content.append('from src.skill_matrix_manager.database import SkillMatrixDatabase\n')
            fixed_content.append('from src.skill_matrix_manager.utils.debug_logger import DebugLogger\n\n')
            fixed_content.append('logger = DebugLogger.get_logger()\n\n')
            imports_added = True
            
        # 既存のimport行は除外、それ以外は保持
        if not line.startswith('from ') and not line.startswith('import '):
            fixed_content.append(line)
    
    # ファイルを上書き
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(fixed_content)
    
    print(f"{filepath} のインポート文を修正しました")
    return True

if __name__ == "__main__":
    fix_main_window_imports()
    print("構文エラーを修正しました。")
