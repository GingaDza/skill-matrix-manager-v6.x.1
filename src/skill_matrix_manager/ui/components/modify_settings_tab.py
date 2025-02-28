#!/usr/bin/env python3
# 設定タブのグループ連携を修正するスクリプト

import os
import sys
import re

# ディレクトリパスの設定
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../../.."))
sys.path.insert(0, project_root)

# 設定タブファイルを開く
settings_tab_path = os.path.join(current_dir, "settings_tab.py")

# バックアップ作成
backup_path = settings_tab_path + ".bak"
if os.path.exists(settings_tab_path):
    with open(settings_tab_path, "r") as src:
        content = src.read()
        with open(backup_path, "w") as dst:
            dst.write(content)
    print(f"バックアップ作成: {backup_path}")

    # デバッグロガーのインポートを追加
    import_added = False
    if "from src.skill_matrix_manager.utils.debug_logger import DebugLogger" not in content:
        content = content.replace("import sys", "import sys\nfrom src.skill_matrix_manager.utils.debug_logger import DebugLogger")
        content = content.replace("class SettingsTab(", "\nlogger = DebugLogger.get_logger()\n\nclass SettingsTab(")
        import_added = True
        print("デバッグロガーのインポートを追加しました")

    # update_main_windowメソッドを追加
    if "def update_main_window(self)" not in content:
        # クラスの終わりを探す
        class_end = content.rfind("\n\n")
        if class_end > 0:
            # メソッドを追加
            new_method = "\n    def update_main_window(self):\n"
            new_method += "        # メインウィンドウに変更を通知\n"
            new_method += "        try:\n"
            new_method += "            # ルートウィンドウを取得\n"
            new_method += "            root = self.parent()\n"
            new_method += "            while root.parent():\n"
            new_method += "                root = root.parent()\n\n"
            new_method += "            # グループコンボボックス更新\n"
            new_method += "            if hasattr(root, \"update_group_combo\"):\n"
            new_method += "                logger.info(\"メインウィンドウのグループコンボボックス更新を呼び出し\")\n"
            new_method += "                root.update_group_combo()\n"
            new_method += "        except Exception as e:\n"
            new_method += "            logger.error(f\"メインウィンドウ更新エラー: {e}\")\n"
            
            content = content[:class_end] + new_method + content[class_end:]
            print("update_main_windowメソッドを追加しました")
    
    # グループ追加メソッドを修正
    if "def add_group" in content:
        add_group_match = re.search(r"(self\.group_list\.addItem\(group_name\))", content)
        if add_group_match and "self.update_main_window()" not in content[add_group_match.end():add_group_match.end()+100]:
            pos = add_group_match.end()
            indent = re.search(r"\n(\s+)self\.group_list\.addItem", content).group(1)
            new_code = f"\n{indent}logger.info(f\"グループ {{group_name}} を追加しました\")\n{indent}# メインウィンドウ更新\n{indent}self.update_main_window()"
            content = content[:pos] + new_code + content[pos:]
            print("add_groupメソッドを修正しました")
    
    # グループ編集メソッドを修正
    if "def edit_group" in content:
        edit_group_match = re.search(r"(self\.group_list\.currentItem\(\)\.setText\(new_name\))", content)
        if edit_group_match and "self.update_main_window()" not in content[edit_group_match.end():edit_group_match.end()+100]:
            pos = edit_group_match.end()
            indent = re.search(r"\n(\s+)self\.group_list\.currentItem", content).group(1)
            new_code = f"\n{indent}logger.info(f\"グループ名を {{new_name}} に変更しました\")\n{indent}# メインウィンドウ更新\n{indent}self.update_main_window()"
            content = content[:pos] + new_code + content[pos:]
            print("edit_groupメソッドを修正しました")
    
    # グループ削除メソッドを修正
    if "def delete_group" in content:
        delete_group_match = re.search(r"(self\.group_list\.takeItem\(row\))", content)
        if delete_group_match and "self.update_main_window()" not in content[delete_group_match.end():delete_group_match.end()+100]:
            pos = delete_group_match.end()
            indent = re.search(r"\n(\s+)self\.group_list\.takeItem", content).group(1)
            new_code = f"\n{indent}logger.info(\"グループを削除しました\")\n{indent}# メインウィンドウ更新\n{indent}self.update_main_window()"
            content = content[:pos] + new_code + content[pos:]
            print("delete_groupメソッドを修正しました")
    
    # 変更を保存
    with open(settings_tab_path, "w") as f:
        f.write(content)
        print("設定タブを修正しました")
else:
    print(f"ファイルが見つかりません: {settings_tab_path}")
