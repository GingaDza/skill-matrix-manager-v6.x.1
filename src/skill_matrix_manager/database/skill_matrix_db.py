#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
スキルマトリックスデータベース管理クラス
SQLiteを使用してデータを管理する
"""

import os
import sqlite3
import datetime
import json
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class SkillMatrixDatabase:
    """スキルマトリックスのデータベース管理クラス"""
    
    def __init__(self, db_path=None):
        """
        初期化
        
        Args:
            db_path (str, optional): データベースファイルのパス
        """
        # データベースファイルのパスを設定
        if db_path is None:
            # デフォルトのパスを設定
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            db_path = os.path.join(base_dir, "data", "skill_matrix.db")
            
            # dataディレクトリの存在確認と作成
            data_dir = os.path.dirname(db_path)
            if not os.path.exists(data_dir):
                os.makedirs(data_dir)
        
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        logger.info(f"データベースパス設定: {self.db_path}")
        
    def __enter__(self):
        """コンテキストマネージャーの開始処理"""
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャーの終了処理"""
        self.close()
        
    def connect(self):
        """データベース接続を確立"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            # ローカライズされた文字列を適切に処理
            self.connection.text_factory = str
            # 結果を辞書形式で取得
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            logger.info("データベースに接続しました")
            return True
        except sqlite3.Error as e:
            logger.error(f"データベース接続エラー: {e}")
            return False
            
    def close(self):
        """データベース接続を閉じる"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            logger.info("データベース接続を閉じました")
            
    def commit(self):
        """変更をコミットする"""
        if self.connection:
            self.connection.commit()
            
    def rollback(self):
        """変更を元に戻す"""
        if self.connection:
            self.connection.rollback()

    def create_tables(self):
        """必要なテーブルを作成"""
        try:
            logger.info("データベーステーブル作成中...")
            
            # メンバーテーブル
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT,
                    group_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # スキルカテゴリテーブル
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS skill_categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # スキルテーブル
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id INTEGER,
                    name TEXT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES skill_categories(id)
                )
            """)
            
            # ステージテーブル
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS stages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    time_unit TEXT,
                    time_value INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # メンバースキルテーブル
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS member_skills (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    member_id INTEGER NOT NULL,
                    skill_id INTEGER NOT NULL,
                    stage_id INTEGER NOT NULL,
                    level INTEGER NOT NULL DEFAULT 0,
                    target_level INTEGER,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (member_id) REFERENCES members(id),
                    FOREIGN KEY (skill_id) REFERENCES skills(id),
                    FOREIGN KEY (stage_id) REFERENCES stages(id),
                    UNIQUE(member_id, skill_id, stage_id)
                )
            """)
            
            self.commit()
            logger.info("データベーステーブル作成完了")
            return True
            
        except sqlite3.Error as e:
            logger.error(f"テーブル作成エラー: {e}")
            self.rollback()
            return False

    #--------------------------------------------------
    # メンバー関連メソッド
    #--------------------------------------------------
    
    def add_member(self, name, email=None, group_name=None):
        """メンバーを追加"""
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                INSERT INTO members (name, email, group_name, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
            """, (name, email, group_name, current_time, current_time))
            self.commit()
            member_id = self.cursor.lastrowid
            logger.info(f"メンバーを追加しました: ID={member_id}, 名前={name}")
            return member_id
        except sqlite3.Error as e:
            logger.error(f"メンバー追加エラー: {e}")
            self.rollback()
            return None
    
    def update_member(self, member_id, name=None, email=None, group_name=None):
        """メンバー情報を更新"""
        try:
            # 現在の値を取得
            current = self.get_member(member_id)
            if not current:
                logger.error(f"更新対象メンバーが見つかりません: ID={member_id}")
                return False
                
            # Noneでなければパラメータを更新
            name = name if name is not None else current['name']
            email = email if email is not None else current['email']
            group_name = group_name if group_name is not None else current['group_name']
            
            # 更新
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                UPDATE members 
                SET name = ?, email = ?, group_name = ?, updated_at = ?
                WHERE id = ?
            """, (name, email, group_name, current_time, member_id))
            self.commit()
            logger.info(f"メンバー情報を更新しました: ID={member_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"メンバー更新エラー: {e}")
            self.rollback()
            return False
    
    def delete_member(self, member_id):
        """メンバーを削除"""
        try:
            # 関連するスキルデータも削除
            self.cursor.execute("DELETE FROM member_skills WHERE member_id = ?", (member_id,))
            
            # メンバーを削除
            self.cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
            
            self.commit()
            logger.info(f"メンバーを削除しました: ID={member_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"メンバー削除エラー: {e}")
            self.rollback()
            return False
    
    def get_member(self, member_id):
        """メンバー情報を取得"""
        try:
            self.cursor.execute("SELECT * FROM members WHERE id = ?", (member_id,))
            result = self.cursor.fetchone()
            if result:
                return dict(result)
            return None
        except sqlite3.Error as e:
            logger.error(f"メンバー取得エラー: {e}")
            return None
    
    def get_all_members(self):
        """すべてのメンバーを取得"""
        try:
            self.cursor.execute("SELECT * FROM members ORDER BY name")
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"メンバー一覧取得エラー: {e}")
            return []
    
    def search_members(self, keyword):
        """メンバーを検索"""
        try:
            # 名前かグループ名で検索
            search_term = f"%{keyword}%"
            self.cursor.execute("""
                SELECT * FROM members 
                WHERE name LIKE ? OR group_name LIKE ? OR email LIKE ?
                ORDER BY name
            """, (search_term, search_term, search_term))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"メンバー検索エラー: {e}")
            return []

    #--------------------------------------------------
    # スキルカテゴリ関連メソッド
    #--------------------------------------------------
    
    def add_skill_category(self, name, description=None):
        """スキルカテゴリを追加"""
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                INSERT INTO skill_categories (name, description, created_at)
                VALUES (?, ?, ?)
            """, (name, description, current_time))
            self.commit()
            category_id = self.cursor.lastrowid
            logger.info(f"スキルカテゴリを追加しました: ID={category_id}, 名前={name}")
            return category_id
        except sqlite3.Error as e:
            logger.error(f"スキルカテゴリ追加エラー: {e}")
            self.rollback()
            return None
    
    def update_skill_category(self, category_id, name=None, description=None):
        """スキルカテゴリを更新"""
        try:
            # 現在の値を取得
            current = self.get_skill_category(category_id)
            if not current:
                logger.error(f"更新対象カテゴリが見つかりません: ID={category_id}")
                return False
                
            # Noneでなければパラメータを更新
            name = name if name is not None else current['name']
            description = description if description is not None else current['description']
            
            # 更新
            self.cursor.execute("""
                UPDATE skill_categories 
                SET name = ?, description = ?
                WHERE id = ?
            """, (name, description, category_id))
            self.commit()
            logger.info(f"スキルカテゴリを更新しました: ID={category_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"スキルカテゴリ更新エラー: {e}")
            self.rollback()
            return False
    
    def delete_skill_category(self, category_id):
        """スキルカテゴリを削除"""
        try:
            # このカテゴリに属するスキルを取得
            skills = self.get_skills_by_category(category_id)
            
            # トランザクション開始
            with self.connection:
                # 関連スキルのカテゴリをNULLに設定
                self.cursor.execute("UPDATE skills SET category_id = NULL WHERE category_id = ?", (category_id,))
                
                # カテゴリを削除
                self.cursor.execute("DELETE FROM skill_categories WHERE id = ?", (category_id,))
            
            logger.info(f"スキルカテゴリを削除しました: ID={category_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"スキルカテゴリ削除エラー: {e}")
            return False
    
    def get_skill_category(self, category_id):
        """スキルカテゴリを取得"""
        try:
            self.cursor.execute("SELECT * FROM skill_categories WHERE id = ?", (category_id,))
            result = self.cursor.fetchone()
            if result:
                return dict(result)
            return None
        except sqlite3.Error as e:
            logger.error(f"スキルカテゴリ取得エラー: {e}")
            return None
    
    def get_all_skill_categories(self):
        """すべてのスキルカテゴリを取得"""
        try:
            self.cursor.execute("SELECT * FROM skill_categories ORDER BY name")
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"スキルカテゴリ一覧取得エラー: {e}")
            return []

    #--------------------------------------------------
    # スキル関連メソッド
    #--------------------------------------------------
    
    def add_skill(self, name, category_id=None, description=None):
        """スキルを追加"""
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                INSERT INTO skills (name, category_id, description, created_at)
                VALUES (?, ?, ?, ?)
            """, (name, category_id, description, current_time))
            self.commit()
            skill_id = self.cursor.lastrowid
            logger.info(f"スキルを追加しました: ID={skill_id}, 名前={name}")
            return skill_id
        except sqlite3.Error as e:
            logger.error(f"スキル追加エラー: {e}")
            self.rollback()
            return None
    
    def update_skill(self, skill_id, name=None, category_id=None, description=None):
        """スキルを更新"""
        try:
            # 現在の値を取得
            current = self.get_skill(skill_id)
            if not current:
                logger.error(f"更新対象スキルが見つかりません: ID={skill_id}")
                return False
                
            # Noneでなければパラメータを更新
            name = name if name is not None else current['name']
            category_id = category_id if category_id is not None else current['category_id']
            description = description if description is not None else current['description']
            
            # 更新
            self.cursor.execute("""
                UPDATE skills 
                SET name = ?, category_id = ?, description = ?
                WHERE id = ?
            """, (name, category_id, description, skill_id))
            self.commit()
            logger.info(f"スキルを更新しました: ID={skill_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"スキル更新エラー: {e}")
            self.rollback()
            return False
    
    def delete_skill(self, skill_id):
        """スキルを削除"""
        try:
            # 関連するスキルデータも削除
            self.cursor.execute("DELETE FROM member_skills WHERE skill_id = ?", (skill_id,))
            
            # スキルを削除
            self.cursor.execute("DELETE FROM skills WHERE id = ?", (skill_id,))
            
            self.commit()
            logger.info(f"スキルを削除しました: ID={skill_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"スキル削除エラー: {e}")
            self.rollback()
            return False
    
    def get_skill(self, skill_id):
        """スキルを取得"""
        try:
            self.cursor.execute("""
                SELECT s.*, c.name as category_name
                FROM skills s 
                LEFT JOIN skill_categories c ON s.category_id = c.id
                WHERE s.id = ?
            """, (skill_id,))
            result = self.cursor.fetchone()
            if result:
                return dict(result)
            return None
        except sqlite3.Error as e:
            logger.error(f"スキル取得エラー: {e}")
            return None
    
    def get_all_skills(self):
        """すべてのスキルを取得"""
        try:
            self.cursor.execute("""
                SELECT s.*, c.name as category_name
                FROM skills s 
                LEFT JOIN skill_categories c ON s.category_id = c.id
                ORDER BY c.name, s.name
            """)
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"スキル一覧取得エラー: {e}")
            return []
    
    def get_skills_by_category(self, category_id):
        """カテゴリ別にスキルを取得"""
        try:
            self.cursor.execute("""
                SELECT * FROM skills 
                WHERE category_id = ?
                ORDER BY name
            """, (category_id,))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"カテゴリ別スキル取得エラー: {e}")
            return []
    
    def search_skills(self, keyword):
        """スキルを検索"""
        try:
            search_term = f"%{keyword}%"
            self.cursor.execute("""
                SELECT s.*, c.name as category_name
                FROM skills s
                LEFT JOIN skill_categories c ON s.category_id = c.id
                WHERE s.name LIKE ? OR s.description LIKE ?
                ORDER BY s.name
            """, (search_term, search_term))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"スキル検索エラー: {e}")
            return []

    #--------------------------------------------------
    # ステージ関連メソッド
    #--------------------------------------------------
    
    def add_stage(self, name, time_unit=None, time_value=None):
        """ステージを追加"""
        try:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.cursor.execute("""
                INSERT INTO stages (name, time_unit, time_value, created_at)
                VALUES (?, ?, ?, ?)
            """, (name, time_unit, time_value, current_time))
            self.commit()
            stage_id = self.cursor.lastrowid
            logger.info(f"ステージを追加しました: ID={stage_id}, 名前={name}")
            return stage_id
        except sqlite3.Error as e:
            logger.error(f"ステージ追加エラー: {e}")
            self.rollback()
            return None
    
    def update_stage(self, stage_id, name=None, time_unit=None, time_value=None):
        """ステージを更新"""
        try:
            # 現在の値を取得
            current = self.get_stage(stage_id)
            if not current:
                logger.error(f"更新対象ステージが見つかりません: ID={stage_id}")
                return False
                
            # Noneでなければパラメータを更新
            name = name if name is not None else current['name']
            time_unit = time_unit if time_unit is not None else current['time_unit']
            time_value = time_value if time_value is not None else current['time_value']
            
            # 更新
            self.cursor.execute("""
                UPDATE stages 
                SET name = ?, time_unit = ?, time_value = ?
                WHERE id = ?
            """, (name, time_unit, time_value, stage_id))
            self.commit()
            logger.info(f"ステージを更新しました: ID={stage_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"ステージ更新エラー: {e}")
            self.rollback()
            return False
    
    def delete_stage(self, stage_id):
        """ステージを削除"""
        try:
            # 関連するスキルデータも削除
            self.cursor.execute("DELETE FROM member_skills WHERE stage_id = ?", (stage_id,))
            
            # ステージを削除
            self.cursor.execute("DELETE FROM stages WHERE id = ?", (stage_id,))
            
            self.commit()
            logger.info(f"ステージを削除しました: ID={stage_id}")
            return True
        except sqlite3.Error as e:
            logger.error(f"ステージ削除エラー: {e}")
            self.rollback()
            return False
    
    def get_stage(self, stage_id):
        """ステージを取得"""
        try:
            self.cursor.execute("SELECT * FROM stages WHERE id = ?", (stage_id,))
            result = self.cursor.fetchone()
            if result:
                return dict(result)
            return None
        except sqlite3.Error as e:
            logger.error(f"ステージ取得エラー: {e}")
            return None
    
    def get_all_stages(self):
        """すべてのステージを取得"""
        try:
            self.cursor.execute("SELECT * FROM stages ORDER BY time_value, name")
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"ステージ一覧取得エラー: {e}")
            return []
