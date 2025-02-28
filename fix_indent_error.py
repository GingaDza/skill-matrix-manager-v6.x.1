#!/usr/bin/env python3
"""インデントエラーを修正するスクリプト"""

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

def restore_main_window():
    """main_window.pyを修復"""
    filepath = os.path.join("src", "skill_matrix_manager", "ui", "main_window.py")
    if not os.path.exists(filepath):
        print(f"ファイルが見つかりません: {filepath}")
        return False
    
    # バックアップ作成
    backup_file(filepath)
    
    # メインウィンドウファイルを適切な形式で書き直し
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("""from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, QSplitter, QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton, QComboBox, QHBoxLayout, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt
from src.skill_matrix_manager.database import SkillMatrixDatabase
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
from src.skill_matrix_manager.ui.components.settings_tab import SettingsTab
from src.skill_matrix_manager.ui.components.skill_gap_tab_impl import SkillGapTab
from src.skill_matrix_manager.ui.components.data_io_tab import DataIOTab

logger = DebugLogger.get_logger()

class MainWindow(QMainWindow):
    """アプリケーションのメインウィンドウ"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("スキルマトリックスマネージャー")
        self.resize(1000, 700)
        
        # メンバー選択状態の初期化
        self.current_user = None
        self.current_group = None
        
        # スプリッター（左右に分割）
        main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(main_splitter)
        
        # 左側のパネル（メンバー選択部分）
        self.left_panel = QWidget()
        left_layout = QVBoxLayout(self.left_panel)
        
        # グループ選択
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("グループ:"))
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_changed)
        group_layout.addWidget(self.group_combo)
        left_layout.addLayout(group_layout)
        
        # ユーザーリスト
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selection_changed)
        left_layout.addWidget(self.user_list)
        
        # ユーザー操作ボタン
        button_layout = QVBoxLayout()
        
        add_user_btn = QPushButton("ユーザー追加")
        add_user_btn.clicked.connect(self.add_user)
        button_layout.addWidget(add_user_btn)
        
        edit_user_btn = QPushButton("ユーザー編集")
        edit_user_btn.clicked.connect(self.edit_user)
        button_layout.addWidget(edit_user_btn)
        
        delete_user_btn = QPushButton("ユーザー削除")
        delete_user_btn.clicked.connect(self.delete_user)
        button_layout.addWidget(delete_user_btn)
        
        left_layout.addLayout(button_layout)
        
        # 左パネルをスプリッターに追加
        main_splitter.addWidget(self.left_panel)
        
        # 右側のタブウィジェット
        self.tab_widget = self.create_tab_widget()
        main_splitter.addWidget(self.tab_widget)
        
        # スプリッターの比率を設定（左:右 = 3:7）
        main_splitter.setSizes([300, 700])
        
        # グループコンボボックスを初期化
        self.update_group_combo()
        
        # ウィンドウを表示
        logger.info("メインウィンドウ表示")
        self.show()
    
    def create_tab_widget(self):
        """タブウィジェットの作成"""
        tab_widget = QTabWidget()
        
        # システム管理タブ
        system_tab = QTabWidget()
        tab_widget.addTab(system_tab, "システム管理")
        
        # システム管理の各サブタブ
        self.settings_tab = SettingsTab(self)
        system_tab.addTab(self.settings_tab, "初期設定")
        
        self.data_io_tab = DataIOTab(self)
        system_tab.addTab(self.data_io_tab, "データ入出力")
        
        # スキル分析タブ
        skill_tab = QTabWidget()
        tab_widget.addTab(skill_tab, "スキル分析")
        
        # スキル分析の各サブタブ
        skill_tab.addTab(QWidget(), "総合評価") 
        
        self.skill_gap_tab = SkillGapTab(self)
        skill_tab.addTab(self.skill_gap_tab, "スキルギャップ")
        
        return tab_widget
    
    def update_group_combo(self):
        """グループコンボボックスを更新"""
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
                logger.info(f"グループ追加: {group}")
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
    
    def on_group_changed(self, index):
        """グループ選択変更時のハンドラ"""
        group = self.group_combo.currentText()
        logger.info(f"グループ選択変更: {group}")
        self.current_group = None if group == "すべて" else group
        self.update_user_list()
    
    def update_user_list(self):
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
    
    def on_user_selection_changed(self):
        """ユーザー選択変更時の処理"""
        try:
            # 選択されたユーザーを取得
            current_item = self.user_list.currentItem()
            if not current_item:
                return
                
            user_name = current_item.text()
            logger.info(f"ユーザー選択: {user_name}")
            self.current_user = user_name
            
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
            import traceback
            logger.error(traceback.format_exc())
    
    def add_user(self):
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
    
    def edit_user(self):
        """ユーザー編集"""
        current_item = self.user_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するユーザーを選択してください")
            return
            
        current_name = current_item.text()
        
        new_name, ok = QInputDialog.getText(
            self, "ユーザー名編集", "新しいユーザー名:", text=current_name)
            
        if ok and new_name and new_name != current_name:
            try:
                # データベース更新
                db = SkillMatrixDatabase()
                db.connect()
                db.update_member_name(current_name, new_name)
                db.close()
                
                # リスト更新
                self.update_user_list()
            except Exception as e:
                logger.error(f"ユーザー編集エラー: {e}")
                QMessageBox.warning(self, "エラー", f"ユーザーの編集に失敗しました: {e}")
    
    def delete_user(self):
        """ユーザー削除"""
        current_item = self.user_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するユーザーを選択してください")
            return
            
        user_name = current_item.text()
        
        reply = QMessageBox.question(
            self, "確認", f"ユーザー '{user_name}' を削除してもよろしいですか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # データベース更新
                db = SkillMatrixDatabase()
                db.connect()
                db.delete_member(user_name)
                db.close()
                
                # リスト更新
                self.update_user_list()
            except Exception as e:
                logger.error(f"ユーザー削除エラー: {e}")
                QMessageBox.warning(self, "エラー", f"ユーザーの削除に失敗しました: {e}")
    
    def cleanup(self):
        """アプリケーション終了時のクリーンアップ"""
        # データベース接続を閉じるなど
        pass
""")
    
    print(f"{filepath} を修復しました")
    
    # データベースクラスにget_member_by_nameメソッドが存在するか確認し、なければ追加
    db_path = os.path.join("src", "skill_matrix_manager", "database", "__init__.py")
    if os.path.exists(db_path):
        with open(db_path, 'r', encoding='utf-8') as f:
            db_content = f.read()
        
        if "def get_member_by_name" not in db_content:
            # バックアップ作成
            backup_file(db_path)
            
            # get_memberメソッドの後に追加
            get_member_pos = db_content.find("def get_member(self")
            if get_member_pos > 0:
                next_def_pos = db_content.find("def ", get_member_pos + 10)
                if next_def_pos > 0:
                    method_to_add = """
    def get_member_by_name(self, name):
        \"\"\"名前からメンバー情報を取得\"\"\"
        self.execute(
            "SELECT m.id, m.name, m.email, m.group_name FROM members m WHERE m.name = ?",
            (name,)
        )
        return self.cursor.fetchone()
        
"""
                    db_content = db_content[:next_def_pos] + method_to_add + db_content[next_def_pos:]
                    
                    with open(db_path, 'w', encoding='utf-8') as f:
                        f.write(db_content)
                    
                    print(f"{db_path} にget_member_by_nameメソッドを追加しました")
    
    return True

if __name__ == "__main__":
    restore_main_window()
    print("インデントエラーを修正しました。アプリケーションを再起動してください。")
