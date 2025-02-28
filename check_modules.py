#!/usr/bin/env python3
"""モジュール構造の診断"""

import os
import importlib
import sys

def check_file(filepath):
    """ファイルの存在確認"""
    if os.path.exists(filepath):
        print(f"✓ {filepath} が存在します")
        return True
    else:
        print(f"✗ {filepath} が見つかりません")
        return False

def check_module(module_name):
    """モジュールのインポート確認"""
    try:
        module = importlib.import_module(module_name)
        print(f"✓ {module_name} をインポートできます")
        return True, module
    except ImportError as e:
        print(f"✗ {module_name} をインポートできません: {e}")
        return False, None

if __name__ == "__main__":
    print("=== ファイル構造の確認 ===")
    
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"プロジェクトルート: {root_dir}")
    
    # main_window.py
    main_window_path = os.path.join(root_dir, "src", "skill_matrix_manager", "ui", "main_window.py")
    check_file(main_window_path)
    
    # settings_tab.py の場所を検索
    print("\n=== settings_tab.py の検索 ===")
    for root, dirs, files in os.walk(root_dir):
        if "settings_tab.py" in files:
            settings_tab_path = os.path.join(root, "settings_tab.py")
            print(f"➤ settings_tab.py を見つけました: {settings_tab_path}")
    
    # データベースクラス
    print("\n=== データベースモジュールの確認 ===")
    db_path = os.path.join(root_dir, "src", "skill_matrix_manager", "database", "__init__.py")
    if check_file(db_path):
        with open(db_path, "r") as f:
            content = f.read()
            if "get_member_by_name" in content:
                print("✓ get_member_by_name メソッドが存在します")
            else:
                print("✗ get_member_by_name メソッドが見つかりません")
    
    # skill_gap_tab_impl.py
    print("\n=== skill_gap_tab_impl.py の検索 ===")
    for root, dirs, files in os.walk(root_dir):
        if "skill_gap_tab_impl.py" in files:
            skill_gap_path = os.path.join(root, "skill_gap_tab_impl.py")
            print(f"➤ skill_gap_tab_impl.py を見つけました: {skill_gap_path}")
            
            with open(skill_gap_path, "r") as f:
                content = f.read()
                if "def set_member(self, member_id, member_name=None, group_name=None)" in content:
                    print("✓ set_member メソッドの引数が正しいです")
                else:
                    print("✗ set_member メソッドの引数が間違っています")
