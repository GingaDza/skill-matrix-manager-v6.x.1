#!/usr/bin/env python3
"""設定タブとメインウィンドウのグループ連携を修正"""

import os
import re

def fix_settings_tab():
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "components", "settings_tab.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # バックアップ作成
    backup_path = filepath + ".bak"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"バックアップを作成しました: {backup_path}")
    
    modified = False
    
    # デバッグログのインポートがなければ追加
    if "from src.skill_matrix_manager.utils.debug_logger import DebugLogger" not in content:
        import_pos = content.find("import ")
        if import_pos >= 0:
            content = content[:import_pos] + "from src.skill_matrix_manager.utils.debug_logger import DebugLogger\n" + content[import_pos:]
            content = content.replace("class SettingsTab(", "logger = DebugLogger.get_logger()\n\nclass SettingsTab(")
            modified = True
    
    # グループ追加後の処理を修正
    if "def add_group" in content:
        if "self.update_main_window()" not in content:
            # グループリストに追加した後にメインウィンドウ更新を呼び出す
            add_pattern = r'(self\.group_list\.addItem\(group_name\))'
            replacement = r'\1\n            logger.info(f"グループ {group_name} を追加しました")\n            # メインウィンドウ更新\n            self.update_main_window()'
            content = re.sub(add_pattern, replacement, content)
            modified = True
    
    # グループ編集後の処理を修正
    if "def edit_group" in content:
        if "self.update_main_window()" not in content:
            # グループ名を変更した後にメインウィンドウ更新を呼び出す
            edit_pattern = r'(self\.group_list\.currentItem\(\)\.setText\(new_name\))'
            replacement = r'\1\n            logger.info(f"グループ名を {new_name} に変更しました")\n            # メインウィンドウ更新\n            self.update_main_window()'
            content = re.sub(edit_pattern, replacement, content)
            modified = True
    
    # グループ削除後の処理を修正
    if "def delete_group" in content:
        if "self.update_main_window()" not in content:
            # グループを削除した後にメインウィンドウ更新を呼び出す
            delete_pattern = r'(self\.group_list\.takeItem\(row\))'
            replacement = r'\1\n            logger.info("グループを削除しました")\n            # メインウィンドウ更新\n            self.update_main_window()'
            content = re.sub(delete_pattern, replacement, content)
            modified = True
    
    # メインウィンドウ更新メソッドを追加
    if "def update_main_window" not in content:
        # クラスの最後にメソッドを追加
        update_method = """
    def update_main_window(self):
        """メインウィンドウに変更を通知"""
        try:
            # ルートウィンドウを取得
            root = self.parent()
            while root.parent():
                root = root.parent()
            
            # グループコンボボックス更新
            if hasattr(root, "update_group_combo"):
                logger.info("メインウィンドウのグループコンボボックス更新を呼び出し")
                root.update_group_combo()
        except Exception as e:
            logger.error(f"メインウィンドウ更新エラー: {e}")
"""
        content += update_method
        modified = True
    
    if modified:
        # 修正した内容を保存
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"{filepath} を修正しました")
        return True
    else:
        print(f"{filepath} は既に修正されています")
        return False

if __name__ == "__main__":
    fix_settings_tab()
