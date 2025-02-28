#!/usr/bin/env python3
# データベースにget_member_by_nameメソッドを追加するスクリプト

import os
import sys
import re

# ディレクトリパスの設定
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../../.."))
sys.path.insert(0, project_root)

# データベースファイルを開く
db_file_path = os.path.join(current_dir, "__init__.py")

# バックアップ作成
backup_path = db_file_path + ".bak"
if os.path.exists(db_file_path):
    with open(db_file_path, "r") as src:
        content = src.read()
        with open(backup_path, "w") as dst:
            dst.write(content)
    print(f"バックアップ作成: {backup_path}")

    # get_member_by_nameメソッドが存在するか確認
    if "def get_member_by_name" not in content:
        # メソッドの挿入場所を見つける
        match = re.search(r"def get_member\(self.*?\).*?\n(\s+)def", content, re.DOTALL)
        if match:
            indent = match.group(1)
            insert_pos = match.end(0) - len("def")
            
            # 新しいメソッドを作成
            new_method = f"\n{indent}def get_member_by_name(self, name):\n"
            new_method += f"{indent}    # 名前からメンバー情報を取得\n"
            new_method += f"{indent}    self.execute(\n"
            new_method += f"{indent}        \"SELECT id, name, email, group_name FROM members WHERE name = ?\",\n"
            new_method += f"{indent}        (name,)\n"
            new_method += f"{indent}    )\n"
            new_method += f"{indent}    return self.cursor.fetchone()\n\n{indent}"
            
            # メソッドを挿入
            new_content = content[:insert_pos] + new_method + content[insert_pos:]
            
            # ファイルに書き戻す
            with open(db_file_path, "w") as f:
                f.write(new_content)
            print("get_member_by_nameメソッドを追加しました")
        else:
            print("get_memberメソッドが見つかりません")
    else:
        print("get_member_by_nameメソッドは既に存在します")
else:
    print(f"ファイルが見つかりません: {db_file_path}")
