#!/usr/bin/env python3
"""データベース操作のテストスクリプト"""

import os
import sys
from src.skill_matrix_manager.database import SkillMatrixDatabase
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

def test_database():
    """データベース操作をテスト"""
    logger.info("データベーステスト開始")
    
    # テスト用の一時データベースパス
    test_db_path = "/tmp/skill_matrix_test.db"
    
    # 前回のテストファイルが残っていれば削除
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    
    # データベースインスタンス作成
    db = SkillMatrixDatabase(test_db_path)
    
    # 接続
    if not db.connect():
        logger.error("データベース接続に失敗しました")
        return False
    
    # テーブル作成
    if not db.create_tables():
        logger.error("テーブル作成に失敗しました")
        return False
    
    # サンプルデータ追加
    if not db.initialize_sample_data():
        logger.error("サンプルデータ初期化に失敗しました")
        return False
    
    # データ取得テスト
    members = db.get_members()
    logger.info(f"メンバー一覧: {len(members)}件")
    for member in members:
        logger.info(f"  - {member['name']} ({member['group_name']})")
        
        # スキルマトリックス取得
        matrix = db.get_skill_matrix(member['id'])
        if matrix:
            logger.info(f"    スキル数: {len(matrix['skills'])}")
            logger.info(f"    ステージ数: {len(matrix['stages'])}")
    
    # データベースエクスポートテスト
    export_path = "/tmp/skill_matrix_export.sql"
    if db.export_database(export_path):
        logger.info(f"データベースエクスポート成功: {export_path}")
    
    # 接続を閉じる
    db.close()
    logger.info("データベーステスト完了")
    return True

if __name__ == "__main__":
    success = test_database()
    sys.exit(0 if success else 1)
