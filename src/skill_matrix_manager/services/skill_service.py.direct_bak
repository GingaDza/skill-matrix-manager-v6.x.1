#!/usr/bin/env python3
"""スキルマトリックス関連のサービス層"""

from PyQt5.QtCore import QObject, pyqtSignal
from src.skill_matrix_manager.database import SkillMatrixDatabase
from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class SkillService(QObject):
    """スキルマトリックスサービス - UIとデータベース間の中間層"""
    
    # シグナル定義 - データ更新時に発火
    groups_updated = pyqtSignal()  # グループリスト更新シグナル
    members_updated = pyqtSignal()  # メンバーリスト更新シグナル
    
    def __init__(self):
        """サービスの初期化"""
        super().__init__()
        self.db = SkillMatrixDatabase()
        self.db.connect()
        self.db.create_tables()
        self._ensure_sample_data()
        
        # 現在選択中のメンバー
        self.current_member_id = None
        
    def _ensure_sample_data(self):
        """サンプルデータが存在することを確認"""
        # メンバーが存在するか確認
        self.db.execute("SELECT COUNT(*) as count FROM members")
        row = self.db.cursor.fetchone()
        if row and row['count'] == 0:
            # サンプルデータがない場合は初期化
            logger.info("初期サンプルデータを作成します")
            self.db.initialize_sample_data()
    
    # ------ グループ管理 ------
    
    def get_groups(self):
        """グループ一覧の取得"""
        return self.db.get_groups()
    
    def add_group(self, group_name):
        """新しいグループを追加（空のメンバーを作成）"""
        if not group_name or group_name.strip() == "":
            logger.error("グループ名が空です")
            return False
            
        # グループ名が既に存在するか確認
        groups = self.get_groups()
        if group_name in groups:
            logger.info(f"グループ '{group_name}' は既に存在します")
            return False
            
        # 空のメンバーを作成してグループを追加
        temp_name = f"__GROUP__{group_name}"
        member_id = self.db.add_member(temp_name, None, group_name)
        
        # シグナル発火 - グループリスト更新通知
        self.groups_updated.emit()
        return member_id is not None
    
    # ------ メンバー管理 ------
    
    def get_members(self, group=None):
        """メンバー一覧の取得"""
        members = self.db.get_members(group)
        # 一時的なグループプレースホルダーを除外
        return [m for m in members if not m['name'].startswith('__GROUP__')]
    
    def add_member(self, name, email=None, group_name=None):
        """メンバーを追加"""
        if not name or name.strip() == "":
            logger.error("メンバー名が空です")
            return None
            
        member_id = self.db.add_member(name, email, group_name)
        if member_id:
            # シグナル発火 - メンバーリスト更新通知
            self.members_updated.emit()
        return member_id
    
    def update_member(self, member_id, name=None, email=None, group_name=None):
        """メンバー情報を更新"""
        success = self.db.update_member(member_id, name, email, group_name)
        if success:
            # シグナル発火 - メンバーリスト更新通知
            self.members_updated.emit()
            # グループが変更された可能性があるため、グループリストも更新
            self.groups_updated.emit()
        return success
    
    def delete_member(self, member_id):
        """メンバーを削除"""
        success = self.db.delete_member(member_id)
        if success:
            # シグナル発火 - メンバーリスト更新通知
            self.members_updated.emit()
            # グループ構成が変わった可能性があるため、グループリストも更新
            self.groups_updated.emit()
        return success
    
    def get_member(self, member_id):
        """メンバー情報の取得"""
        return self.db.get_member(member_id)
    
    # ------ スキルマトリックス管理 ------
    
    def get_skill_matrix(self, member_id):
        """スキルマトリックスを取得"""
        return self.db.get_skill_matrix(member_id)
    
    def get_skill_data_for_radar_chart(self, member_id):
        """レーダーチャート用のデータ形式に変換"""
        matrix = self.db.get_skill_matrix(member_id)
        if not matrix:
            return None, None
            
        # RadarChartDialogが期待する形式に変換
        stages = []
        stage_data = []
        
        # ステージ情報を抽出
        for stage in matrix['stages']:
            stages.append(stage['name'])
            # 各ステージのスキルデータを取得
            skills_dict = {}
            for skill_id, skill_info in matrix['skills'].items():
                if stage['id'] in skill_info['levels']:
                    level = skill_info['levels'][stage['id']]['level']
                    skills_dict[skill_info['name']] = level
            stage_data.append(skills_dict)
            
        return stages, stage_data
    
    def set_member(self, member_id):
        """現在のメンバーを設定"""
        self.current_member_id = member_id
        return self.db.get_member(member_id)
    
    def update_skill_level(self, skill_name, stage_idx, level):
        """スキルレベルを更新"""
        if not self.current_member_id:
            logger.error("メンバーが選択されていません")
            return False
            
        # スキルIDとステージIDを取得
        skill_id = self._get_skill_id_by_name(skill_name)
        stage_id = self._get_stage_id_by_index(stage_idx)
        
        if skill_id is None or stage_id is None:
            return False
            
        # スキルレベルを更新
        return self.db.set_skill_level(self.current_member_id, skill_id, stage_id, level)
    
    def _get_skill_id_by_name(self, skill_name):
        """スキル名からスキルIDを取得"""
        self.db.execute("SELECT id FROM skills WHERE name = ?", (skill_name,))
        row = self.db.cursor.fetchone()
        return row['id'] if row else None
    
    def _get_stage_id_by_index(self, stage_idx):
        """ステージインデックスからステージIDを取得"""
        self.db.execute("SELECT id FROM stages ORDER BY time_value, name LIMIT 1 OFFSET ?", (stage_idx,))
        row = self.db.cursor.fetchone()
        return row['id'] if row else None
    
    def __del__(self):
        """デストラクタ - データベース接続のクローズ"""
        if hasattr(self, 'db') and self.db.conn:
            self.db.close()
