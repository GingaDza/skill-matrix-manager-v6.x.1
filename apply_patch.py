#!/usr/bin/env python3
"""パッチ適用スクリプト"""

import os
import sys
import shutil
from datetime import datetime

def backup_file(filepath):
    """ファイルのバックアップを作成"""
    if os.path.exists(filepath):
        backup_dir = os.path.join(os.path.dirname(filepath), "backups")
        os.makedirs(backup_dir, exist_ok=True)
        
        filename = os.path.basename(filepath)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(backup_dir, f"{filename}.{timestamp}")
        
        shutil.copy2(filepath, backup_path)
        print(f"バックアップ作成: {backup_path}")
        return True
    return False

def patch_main_window():
    """メインウィンドウの修正"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(filepath):
        print(f"エラー: {filepath} が見つかりません")
        return False
        
    # ファイルのバックアップ
    backup_file(filepath)
    
    # ファイル内容の読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # パッチの適用（例）
    # コンポーネントの初期化前にコーディネーター初期化を追加
    if "from src.skill_matrix_manager.utils.coordinator import AppCoordinator" not in content:
        imports = "from PyQt5.QtWidgets import QMainWindow, QTabWidget\n"
        new_imports = "from PyQt5.QtWidgets import QMainWindow, QTabWidget\nfrom src.skill_matrix_manager.utils.coordinator import AppCoordinator\n"
        content = content.replace(imports, new_imports)
    
    # コーディネーターの初期化を追加
    if "self.coordinator = AppCoordinator(self)" not in content:
        init_section = "def __init__(self):\n        super().__init__()\n"
        new_init_section = "def __init__(self):\n        super().__init__()\n        # コーディネーターの初期化\n        self.coordinator = AppCoordinator(self)\n"
        content = content.replace(init_section, new_init_section)
    
    # SkillGapTab初期化部分の修正
    if "self.skill_gap_tab = SkillGapTab(self)" in content:
        old_init = "self.skill_gap_tab = SkillGapTab(self)"
        new_init = "self.skill_gap_tab = SkillGapTab(self)"  # 変更なし
        content = content.replace(old_init, new_init)
    
    # ファイルに書き戻し
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{filepath} を修正しました")
    return True

def main():
    """パッチ適用メイン処理"""
    # 現在の作業ディレクトリ確認
    cwd = os.getcwd()
    print(f"現在の作業ディレクトリ: {cwd}")
    
    # パッチ適用
    if patch_main_window():
        print("パッチの適用が完了しました")
    else:
        print("パッチの適用に失敗しました")

if __name__ == "__main__":
    main()
