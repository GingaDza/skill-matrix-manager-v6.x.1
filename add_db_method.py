#!/usr/bin/env python3
"""データベースクラスにget_member_by_nameメソッドを追加"""

import os
import re

def add_method():
    filepath = os.path.join("src", "skill_matrix_manager", "database", "__init__.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # ファイルを読み込み
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # メソッドが既に存在するか確認
    if "def get_member_by_name" not in content:
        # バックアップ作成
        backup_path = filepath + ".bak"
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"バックアップを作成しました: {backup_path}")
        
        # get_memberメソッドを探す
        get_member_pos = content.find("def get_member(self")
        if get_member_pos > 0:
            # メソッドの終わりを探す
            next_method_pos = content.find("\n    def ", get_member_pos + 1)
            if next_method_pos > 0:
                # 新しいメソッドを追加
                new_method = """
    def get_member_by_name(self, name):
        """名前からメンバー情報を取得"""
        self.execute(
            "SELECT id, name, email, group_name FROM members WHERE name = ?",
            (name,)
        )
        return self.cursor.fetchone()
        
"""
                # 新しいメソッドを挿入
                new_content = content[:next_method_pos] + new_method + content[next_method_pos:]
                
                # ファイルを保存
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"{filepath} にget_member_by_nameメソッドを追加しました")
                return True
            else:
                print("get_memberメソッドの終わりが見つかりませんでした")
        else:
            print("get_memberメソッドが見つかりませんでした")
    else:
        print("get_member_by_nameメソッドは既に存在します")
    
    return False

if __name__ == "__main__":
    add_method()
