#!/usr/bin/env python3
"""グループとメンバー管理の問題を修正するスクリプト"""

import os
import sys
import re
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

def fix_settings_tab():
    """設定タブでのグループ管理関数を修正"""
    settings_tab_path = os.path.join("src", "skill_matrix_manager", "ui", "components", "settings_tab.py")
    if not os.path.exists(settings_tab_path):
        print(f"ファイルが見つかりません: {settings_tab_path}")
        return False
    
    # バックアップ作成
    backup_file(settings_tab_path)
    
    with open(settings_tab_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # デバッグ用のログを追加
    if 'from src.skill_matrix_manager.utils.debug_logger import DebugLogger' not in content:
        content = 'from src.skill_matrix_manager.utils.debug_logger import DebugLogger\n' + content
        content = content.replace('class SettingsTab(', 'logger = DebugLogger.get_logger()\n\nclass SettingsTab(')
    
    # グループ追加メソッドの修正
    if 'def add_group(' in content:
        add_group_pattern = r'(def add_group\(self.*?\):.*?if group_name:.*?)(\s+self\.group_list\.addItem\(group_name\))'
        
        replacement = r'\1\n            logger.info(f"グループ追加: {group_name}")\2'
        content = re.sub(add_group_pattern, replacement, content, flags=re.DOTALL)
        
        # グループ追加後に直接メインウィンドウの更新を呼び出す
        after_add_pattern = r'(self\.group_list\.addItem\(group_name\))'
        after_add_replacement = r'\1\n            # メインウィンドウのグループコンボボックスを更新\n            main_window = self\n            while main_window.parent():\n                main_window = main_window.parent()\n            \n            if hasattr(main_window, "update_group_combo"):\n                logger.info("メインウィンドウのグループコンボボックス更新を呼び出し")\n                main_window.update_group_combo()'
        content = re.sub(after_add_pattern, after_add_replacement, content)
    
    # グループ編集メソッドにも同様の更新処理を追加
    if 'def edit_group(' in content:
        after_edit_pattern = r'(self\.group_list\.currentItem\(\)\.setText\(new_name\))'
        after_edit_replacement = r'\1\n            logger.info(f"グループ編集: {new_name}")\n            # メインウィンドウのグループコンボボックスを更新\n            main_window = self\n            while main_window.parent():\n                main_window = main_window.parent()\n            \n            if hasattr(main_window, "update_group_combo"):\n                logger.info("メインウィンドウのグループコンボボックス更新を呼び出し")\n                main_window.update_group_combo()'
        content = re.sub(after_edit_pattern, after_edit_replacement, content)
    
    # グループ削除メソッドにも同様の更新処理を追加
    if 'def delete_group(' in content:
        after_delete_pattern = r'(self\.group_list\.takeItem\(row\))'
        after_delete_replacement = r'\1\n            logger.info("グループ削除完了")\n            # メインウィンドウのグループコンボボックスを更新\n            main_window = self\n            while main_window.parent():\n                main_window = main_window.parent()\n            \n            if hasattr(main_window, "update_group_combo"):\n                logger.info("メインウィンドウのグループコンボボックス更新を呼び出し")\n                main_window.update_group_combo()'
        content = re.sub(after_delete_pattern, after_delete_replacement, content)
    
    with open(settings_tab_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{settings_tab_path} を修正しました")
    return True

def fix_main_window():
    """メインウィンドウのグループコンボボックス更新関数を修正"""
    main_window_path = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(main_window_path):
        print(f"ファイルが見つかりません: {main_window_path}")
        return False
    
    # バックアップ作成
    backup_file(main_window_path)
    
    with open(main_window_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # update_group_combo メソッドの検索と修正
    update_method_exists = 'def update_group_combo' in content
    
    if update_method_exists:
        # 既存メソッドの修正
        update_pattern = r'(def update_group_combo.*?:.*?)(\s+(?:def|if __name__))'
        
        # 既存のメソッドを強化
        replacement = r'''def update_group_combo(self):
        """グループコンボボックス更新 - 修正版"""
        logger.info("グループコンボボックス更新開始")
        try:
            # 現在の選択を保存
            current_selection = self.group_combo.currentText()
            
            # グループリストをクリア
            self.group_combo.clear()
            
            # グループの読み込み
            db = SkillMatrixDatabase()
            db.connect()
            groups = db.get_groups()
            db.close()
            
            # 「すべて」の選択肢を追加
            self.group_combo.addItem("すべて")
            
            # グループを追加
            for group in groups:
                logger.info(f"グループ追加: {group}")
                self.group_combo.addItem(group)
            
            # 以前の選択を復元
            index = self.group_combo.findText(current_selection)
            if index >= 0:
                self.group_combo.setCurrentIndex(index)
            else:
                self.group_combo.setCurrentIndex(0)  # デフォルトは「すべて」
                
            logger.info("グループコンボボックス更新完了")
        except Exception as e:
            logger.error(f"グループコンボボックス更新エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
\2'''
        
        content = re.sub(update_pattern, replacement, content, flags=re.DOTALL)
    else:
        # メソッドが存在しない場合は追加
        class_end = content.rfind('\n\nif __name__')
        if class_end < 0:
            class_end = content.rfind('\n\n# アプリケーション実行')
        
        if class_end > 0:
            update_method = '''
    def update_group_combo(self):
        """グループコンボボックス更新"""
        logger.info("グループコンボボックス更新開始")
        try:
            # 現在の選択を保存
            current_selection = self.group_combo.currentText()
            
            # グループリストをクリア
            self.group_combo.clear()
            
            # グループの読み込み
            db = SkillMatrixDatabase()
            db.connect()
            groups = db.get_groups()
            db.close()
            
            # 「すべて」の選択肢を追加
            self.group_combo.addItem("すべて")
            
            # グループを追加
            for group in groups:
                logger.info(f"グループ追加: {group}")
                self.group_combo.addItem(group)
            
            # 以前の選択を復元
            index = self.group_combo.findText(current_selection)
            if index >= 0:
                self.group_combo.setCurrentIndex(index)
            else:
                self.group_combo.setCurrentIndex(0)  # デフォルトは「すべて」
                
            logger.info("グループコンボボックス更新完了")
        except Exception as e:
            logger.error(f"グループコンボボックス更新エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
            
'''
            content = content[:class_end] + update_method + content[class_end:]
    
    # SkillMatrixDatabaseのインポート確認
    if 'from src.skill_matrix_manager.database import SkillMatrixDatabase' not in content:
        import_pos = content.find('import')
        import_pos = content.find('\n', import_pos)
        content = content[:import_pos+1] + 'from src.skill_matrix_manager.database import SkillMatrixDatabase\n' + content[import_pos+1:]
    
    with open(main_window_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{main_window_path} を修正しました")
    return True

def fix_member_management():
    """メンバー管理機能を修正"""
    main_window_path = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(main_window_path):
        print(f"ファイルが見つかりません: {main_window_path}")
        return False
    
    # バックアップ作成
    backup_file(main_window_path)
    
    with open(main_window_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # add_user メソッドの検索と修正
    if 'def add_user' in content:
        add_user_pattern = r'(def add_user.*?:.*?)(\s+(?:def|if __name__))'
        
        # 既存のメソッドを強化
        replacement = r'''def add_user(self):
        """ユーザー追加"""
        logger.info("ユーザー追加ダイアログ表示")
        try:
            user_name, ok = QInputDialog.getText(self, "ユーザー追加", "ユーザー名:")
            if ok and user_name:
                # グループの取得
                group_name = self.group_combo.currentText()
                if group_name == "すべて":
                    group_name = ""  # グループなしとして扱う
                
                logger.info(f"ユーザー追加: {user_name}, グループ: {group_name}")
                
                # データベースに追加
                db = SkillMatrixDatabase()
                db.connect()
                db.add_member(user_name, "", group_name)
                db.close()
                
                # ユーザーリストを更新
                self.update_user_list()
        except Exception as e:
            logger.error(f"ユーザー追加エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
            QMessageBox.warning(self, "エラー", f"ユーザーの追加に失敗しました: {e}")
\2'''
        
        content = re.sub(add_user_pattern, replacement, content, flags=re.DOTALL)
    
    # update_user_list メソッドの検索と修正
    if 'def update_user_list' in content:
        update_users_pattern = r'(def update_user_list.*?:.*?)(\s+(?:def|if __name__))'
        
        # 既存のメソッドを強化
        replacement = r'''def update_user_list(self):
        """ユーザーリスト更新"""
        logger.info("ユーザーリスト更新開始")
        try:
            # 現在の選択を保存
            current_item = self.user_list.currentItem()
            current_user = current_item.text() if current_item else None
            
            # リストをクリア
            self.user_list.clear()
            
            # 選択されたグループを取得
            group = self.group_combo.currentText()
            filter_group = None if group == "すべて" else group
            
            # データベースからユーザー取得
            db = SkillMatrixDatabase()
            db.connect()
            members = db.get_members(filter_group)
            db.close()
            
            # ユーザーリストに追加
            for member in members:
                self.user_list.addItem(member['name'])
            
            # 以前の選択を復元
            if current_user:
                items = self.user_list.findItems(current_user, Qt.MatchExactly)
                if items:
                    self.user_list.setCurrentItem(items[0])
                    
            logger.info(f"ユーザーリスト更新完了: {len(members)}人")
        except Exception as e:
            logger.error(f"ユーザーリスト更新エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
\2'''
        
        content = re.sub(update_users_pattern, replacement, content, flags=re.DOTALL)
    
    # ユーザーリスト作成部分を確認し修正
    if 'self.user_list = QListWidget()' in content and 'self.user_list.itemSelectionChanged.connect(' not in content:
        user_list_pattern = r'(self\.user_list = QListWidget\(\).*?)(\s+[^\s])'
        
        # シグナルを接続
        replacement = r'\1\n        self.user_list.itemSelectionChanged.connect(self.on_user_selection_changed)\2'
        content = re.sub(user_list_pattern, replacement, content)
    
    # on_user_selection_changed メソッドの確認
    if 'def on_user_selection_changed(' not in content:
        # メソッドを追加する場所を探す
        insert_pos = content.find('def update_user_list(')
        if insert_pos > 0:
            # update_user_listの前に追加
            method_to_add = '''
    def on_user_selection_changed(self):
        """ユーザー選択変更時の処理"""
        try:
            # 選択されたユーザーを取得
            current_item = self.user_list.currentItem()
            if not current_item:
                return
                
            user_name = current_item.text()
            logger.info(f"ユーザー選択: {user_name}")
            
            # 選択されたグループを取得
            group_name = self.group_combo.currentText()
            if group_name == "すべて":
                # データベースから正確なグループを取得
                db = SkillMatrixDatabase()
                db.connect()
                member = db.get_member_by_name(user_name)
                db.close()
                if member:
                    group_name = member['group_name'] or ""
            
            # タブにユーザーを設定
            if hasattr(self, 'skill_gap_tab'):
                self.skill_gap_tab.set_member(user_name, user_name, group_name)
        except Exception as e:
            logger.error(f"ユーザー選択変更エラー: {e}")
            
'''
            content = content[:insert_pos] + method_to_add + content[insert_pos:]
    
    # get_member_by_nameメソッドをデータベースクラスに追加するためのパッチ
    db_patch_path = os.path.join("src", "skill_matrix_manager", "database", "__init__.py")
    if os.path.exists(db_patch_path):
        backup_file(db_patch_path)
        
        with open(db_patch_path, 'r', encoding='utf-8') as f:
            db_content = f.read()
        
        if 'def get_member_by_name(self, name)' not in db_content:
            # get_memberメソッドの後にget_member_by_nameを追加
            get_member_pos = db_content.find('def get_member(self')
            if get_member_pos > 0:
                next_method_pos = db_content.find('def ', get_member_pos + 10)
                if next_method_pos > 0:
                    method_to_add = '''
    def get_member_by_name(self, name):
        """メンバー情報をメンバー名から取得"""
        self.execute(
            "SELECT id, name, email, group_name FROM members WHERE name = ?",
            (name,)
        )
        return self.cursor.fetchone()
        
'''
                    db_content = db_content[:next_method_pos] + method_to_add + db_content[next_method_pos:]
                    
                    with open(db_patch_path, 'w', encoding='utf-8') as f:
                        f.write(db_content)
                    
                    print(f"{db_patch_path} にget_member_by_nameメソッドを追加しました")
    
    # メインウィンドウの変更を保存
    with open(main_window_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"{main_window_path} を修正しました")
    return True

if __name__ == "__main__":
    print("グループとメンバー管理の問題を修正します...")
    
    # 初期設定タブのグループ機能修正
    fix_settings_tab()
    
    # メインウィンドウのグループコンボボックス更新
    fix_main_window()
    
    # メンバー管理機能の修正
    fix_member_management()
    
    print("修正が完了しました。アプリケーションを再起動してください。")
