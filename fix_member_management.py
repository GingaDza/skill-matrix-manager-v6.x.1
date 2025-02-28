#!/usr/bin/env python3
"""メンバー管理とグループ同期の問題を修正するスクリプト - 再試行版"""

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

def add_update_group_combo():
    """update_group_comboメソッドがなければ追加"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # メソッドが既に存在するか確認
    if "def update_group_combo" not in content:
        # メソッドを追加する場所を見つける
        # クラス定義の終わり付近を探す
        insertion_point = content.rfind("    def ")
        if insertion_point > 0:
            # 最後のメソッドを見つけたら、そのメソッドの終わりを探す
            next_method = content.find("    def ", insertion_point + 1)
            if next_method < 0:  # 次のメソッドが見つからない場合
                # クラス定義の終わりを推測
                class_end = content.find("if __name__")
                if class_end < 0:
                    class_end = len(content)
                insertion_point = class_end
            else:
                insertion_point = next_method
            
            # メソッドを追加
            method_code = """
    def update_group_combo(self):
        \"\"\"グループコンボボックスを更新\"\"\"
        logger.info("グループコンボボックス更新開始")
        try:
            # 現在の選択を保存
            current_text = self.group_combo.currentText() if self.group_combo.count() > 0 else ""
            
            # コンボボックスをクリア
            self.group_combo.clear()
            
            # データベースからグループ一覧を取得
            db = SkillMatrixDatabase()
            db.connect()
            groups = db.get_groups()
            db.close()
            
            # 「すべて」オプションを追加
            self.group_combo.addItem("すべて")
            
            # グループを追加
            for group in groups:
                self.group_combo.addItem(group)
            
            # 以前の選択を復元
            if current_text:
                index = self.group_combo.findText(current_text)
                if index >= 0:
                    self.group_combo.setCurrentIndex(index)
                else:
                    self.group_combo.setCurrentIndex(0)  # デフォルトは「すべて」
                    
            logger.info(f"グループコンボボックス更新完了: {len(groups)}グループ")
            
            # ユーザーリストも更新
            self.update_user_list()
            
        except Exception as e:
            logger.error(f"グループコンボボックス更新エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
"""
            
            content = content[:insertion_point] + method_code + content[insertion_point:]
            
            # ファイルを上書き
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"{filepath} にupdate_group_comboメソッドを追加しました")
            return True
        else:
            print("メソッドの挿入ポイントが見つかりませんでした")
            return False
    else:
        print("update_group_comboメソッドは既に存在します")
        return True

def connect_settings_tab():
    """初期設定タブのグループ操作とメインウィンドウのグループ更新を連携"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "components", "settings_tab.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 各グループ操作メソッドに更新通知を追加
    modified = False
    
    # add_groupメソッドを修正
    if "def add_group" in content:
        # 追加処理の後にメインウィンドウ更新を呼び出す
        if "self.group_list.addItem(group_name)" in content and "# メインウィンドウ更新" not in content:
            content = content.replace(
                "self.group_list.addItem(group_name)",
                "self.group_list.addItem(group_name)\n            # メインウィンドウ更新\n            self.update_main_window()"
            )
            modified = True
    
    # edit_groupメソッドを修正
    if "def edit_group" in content:
        # 編集処理の後にメインウィンドウ更新を呼び出す
        if "self.group_list.currentItem().setText(new_name)" in content and "# メインウィンドウ更新" not in content:
            content = content.replace(
                "self.group_list.currentItem().setText(new_name)",
                "self.group_list.currentItem().setText(new_name)\n            # メインウィンドウ更新\n            self.update_main_window()"
            )
            modified = True
    
    # delete_groupメソッドを修正
    if "def delete_group" in content:
        # 削除処理の後にメインウィンドウ更新を呼び出す
        if "self.group_list.takeItem(row)" in content and "# メインウィンドウ更新" not in content:
            content = content.replace(
                "self.group_list.takeItem(row)",
                "self.group_list.takeItem(row)\n            # メインウィンドウ更新\n            self.update_main_window()"
            )
            modified = True
    
    # update_main_windowメソッドがなければ追加
    if "def update_main_window" not in content:
        # クラスの最後にメソッドを追加
        last_def = content.rfind("    def ")
        next_class = content.find("class ", last_def)
        
        if next_class < 0:  # 次のクラス定義がない場合
            next_class = len(content)
        
        # メソッドの終わりを推測
        method_end = content.find("\n\n", last_def)
        if method_end < 0 or method_end > next_class:
            method_end = next_class
        
        # メソッドを追加
        update_method = """
    def update_main_window(self):
        \"\"\"メインウィンドウに変更を通知\"\"\"
        try:
            # ルートウィンドウを取得
            main_window = self
            while main_window.parent():
                main_window = main_window.parent()
            
            # グループコンボボックス更新メソッドを呼び出し
            if hasattr(main_window, "update_group_combo"):
                main_window.update_group_combo()
        except Exception as e:
            # デバッグログのみ記録して続行
            try:
                from src.skill_matrix_manager.utils.debug_logger import DebugLogger
                logger = DebugLogger.get_logger()
                logger.error(f"メインウィンドウ更新エラー: {e}")
            except:
                pass
"""
        
        content = content[:method_end] + update_method + content[method_end:]
        modified = True
    
    if modified:
        # ファイルを上書き
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"{filepath} を修正しました")
        return True
    else:
        print(f"{filepath} は既に修正されています")
        return False

def add_database_method():
    """get_member_by_nameメソッドをデータベースクラスに追加"""
    filepath = os.path.join("src", "skill_matrix_manager", "database", "__init__.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # get_member_by_nameメソッドを追加
    if "def get_member_by_name" not in content:
        # get_memberメソッドの後に追加
        get_member_pos = content.find("def get_member(self")
        if get_member_pos > 0:
            # get_memberメソッドの終わりを見つける
            next_def_pos = content.find("def ", get_member_pos + 10)
            if next_def_pos > 0:
                # メソッドを追加
                method_code = """
    def get_member_by_name(self, name):
        \"\"\"名前からメンバー情報を取得\"\"\"
        self.execute(
            "SELECT m.id, m.name, m.email, m.group_name FROM members m WHERE m.name = ?",
            (name,)
        )
        return self.cursor.fetchone()
        
"""
                content = content[:next_def_pos] + method_code + content[next_def_pos:]
                
                # ファイルを上書き
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"{filepath} にget_member_by_nameメソッドを追加しました")
                return True
            else:
                print("get_memberメソッドの終わりが見つかりませんでした")
                return False
        else:
            print("get_memberメソッドが見つかりませんでした")
            return False
    else:
        print("get_member_by_nameメソッドは既に存在します")
        return True

def fix_main_window():
    """メインウィンドウクラスの修正"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # __init__メソッド内でupdate_group_comboを呼び出す箇所を追加
    if "def __init__" in content and "self.update_group_combo()" not in content:
        init_end = content.find("def ", content.find("def __init__") + 10)
        if init_end > 0:
            # 適切な場所を探す
            show_pos = content.rfind("self.show()", 0, init_end)
            if show_pos > 0:
                # self.show()の前に追加
                line_start = content.rfind("\n", 0, show_pos)
                content = content[:line_start] + "\n        # グループコンボボックスを初期化\n        self.update_group_combo()" + content[line_start:]
                
                # ファイルを上書き
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"{filepath} の__init__メソッドにupdate_group_combo呼び出しを追加しました")
                return True
            else:
                print("self.show()が見つかりませんでした")
        else:
            print("__init__メソッドの終わりが見つかりませんでした")
    else:
        print("既にupdate_group_comboが呼び出されているか、__init__メソッドが見つかりません")
    
    return False

if __name__ == "__main__":
    print("メンバー管理とグループ同期の問題を修正します...")
    
    # update_group_comboメソッドの追加
    add_update_group_combo()
    
    # 初期設定タブとメインウィンドウの連携
    connect_settings_tab()
    
    # データベースにget_member_by_nameメソッドを追加
    add_database_method()
    
    # メインウィンドウの初期化処理を修正
    fix_main_window()
    
    print("修正が完了しました。アプリケーションを再起動してください。")
