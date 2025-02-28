#!/usr/bin/env python3
"""データベース管理クラス"""

import sqlite3
import os
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class SkillMatrixDatabase:
    """スキルマトリックスデータベース管理クラス"""
    
    def __init__(self):
        self.conn = None
        self.cursor = None
        db_dir = os.path.join(os.path.dirname(__file__), '../../../database')
        os.makedirs(db_dir, exist_ok=True)
        self.db_path = os.path.join(db_dir, 'skill_matrix.db')
    
    def connect(self):
        """データベースに接続"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            self.create_tables()
            return True
        except Exception as e:
            logger.error(f"データベース接続エラー: {e}")
            return False
    
    def close(self):
        """データベース接続を閉じる"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def execute(self, query, params=()):
        """クエリを実行"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except Exception as e:
            logger.error(f"クエリ実行エラー: {query} - {e}")
            return False
    
    def create_tables(self):
        """必要なテーブルを作成"""
        # メンバーテーブル
        self.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            group_name TEXT
        )
        ''')
        
        # スキルテーブル
        self.execute('''
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT
        )
        ''')
        
        # メンバースキルテーブル（関連）
        self.execute('''
        CREATE TABLE IF NOT EXISTS member_skills (
            id INTEGER PRIMARY KEY,
            member_id INTEGER,
            skill_id INTEGER,
            current_level INTEGER,
            target_level INTEGER,
            FOREIGN KEY (member_id) REFERENCES members(id),
            FOREIGN KEY (skill_id) REFERENCES skills(id)
        )
        ''')
    
    def add_member(self, name, email="", group_name=""):
        """メンバーを追加"""
        self.execute(
            "INSERT INTO members (name, email, group_name) VALUES (?, ?, ?)",
            (name, email, group_name)
        )
        return self.cursor.lastrowid
    
    def update_member_name(self, current_name, new_name):
        """メンバー名を更新"""
        self.execute(
            "UPDATE members SET name = ? WHERE name = ?",
            (new_name, current_name)
        )
        return self.cursor.rowcount > 0
    
    def delete_member(self, name):
        """メンバーを削除"""
        self.execute("DELETE FROM members WHERE name = ?", (name,))
        return self.cursor.rowcount > 0
    
    def get_members(self, group_name=None):
        """メンバーリストを取得（グループでフィルタ可能）"""
        if group_name:
            self.execute(
                "SELECT id, name, email, group_name FROM members WHERE group_name = ? ORDER BY name",
                (group_name,)
            )
        else:
            self.execute(
                "SELECT id, name, email, group_name FROM members ORDER BY name"
            )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_member(self, member_id):
        """メンバー情報を取得"""
        self.execute(
            "SELECT id, name, email, group_name FROM members WHERE id = ?",
            (member_id,)
        )
        return self.cursor.fetchone()
    
    def get_member_by_name(self, name):
        """名前からメンバー情報を取得"""
        self.execute(
            "SELECT id, name, email, group_name FROM members WHERE name = ?",
            (name,)
        )
        return self.cursor.fetchone()
    
    def get_groups(self):
        """グループリストを取得"""
        self.execute(
            "SELECT DISTINCT group_name FROM members WHERE group_name IS NOT NULL AND group_name != ''"
        )
        return [row['group_name'] for row in self.cursor.fetchall()]
    
    def add_group_if_not_exists(self, group_name):
        """グループが存在しない場合は追加（ダミーメンバー作成）"""
        if not group_name:
            return False
            
        # グループ存在確認
        self.execute(
            "SELECT COUNT(*) as count FROM members WHERE group_name = ?",
            (group_name,)
        )
        result = self.cursor.fetchone()
        
        if result and result['count'] == 0:
            # ダミーメンバー作成
            dummy_name = f"_dummy_{group_name}"
            self.add_member(dummy_name, "", group_name)
            logger.info(f"グループ追加: {group_name}")
            return True
        return False
