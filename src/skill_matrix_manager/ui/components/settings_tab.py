#!/usr/bin/env python3
"""初期設定タブの実装"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QListWidget, QInputDialog, 
                           QMessageBox, QTabWidget, QGroupBox, QFormLayout,
                           QTreeWidget, QTreeWidgetItem)
import sys
from src.skill_matrix_manager.utils.debug_logger import DebugLogger
from src.skill_matrix_manager.database import SkillMatrixDatabase

logger = DebugLogger.get_logger()

class SettingsTab(QWidget):
    """初期設定タブ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """UI要素のセットアップ"""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # 上部レイアウト - グループとカテゴリー管理
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)
        
        # グループ管理
        group_box = QGroupBox("グループ管理")
        group_layout = QVBoxLayout()
        group_box.setLayout(group_layout)
        
        # グループリスト
        self.group_list = QListWidget()
        group_layout.addWidget(self.group_list)
        
        # グループ操作ボタン
        group_btn_layout = QHBoxLayout()
        
        self.add_group_btn = QPushButton("追加")
        self.add_group_btn.clicked.connect(self.add_group)
        group_btn_layout.addWidget(self.add_group_btn)
        
        self.edit_group_btn = QPushButton("編集")
        self.edit_group_btn.clicked.connect(self.edit_group)
        group_btn_layout.addWidget(self.edit_group_btn)
        
        self.delete_group_btn = QPushButton("削除")
        self.delete_group_btn.clicked.connect(self.delete_group)
        group_btn_layout.addWidget(self.delete_group_btn)
        
        group_layout.addLayout(group_btn_layout)
        
        top_layout.addWidget(group_box)
        
        # カテゴリー/スキル管理 (ツリー表示)
        category_box = QGroupBox("カテゴリー/スキル管理")
        category_layout = QVBoxLayout()
        category_box.setLayout(category_layout)
        
        # カテゴリー/スキルツリー
        self.category_tree = QTreeWidget()
        self.category_tree.setHeaderLabels(["カテゴリー/スキル"])
        category_layout.addWidget(self.category_tree)
        
        # カテゴリー操作ボタン
        category_btn_layout = QHBoxLayout()
        
        self.add_category_btn = QPushButton("カテゴリー追加")
        self.add_category_btn.clicked.connect(self.add_category)
        category_btn_layout.addWidget(self.add_category_btn)
        
        self.add_skill_btn = QPushButton("スキル追加")
        self.add_skill_btn.clicked.connect(self.add_skill)
        category_btn_layout.addWidget(self.add_skill_btn)
        
        self.edit_item_btn = QPushButton("編集")
        self.edit_item_btn.clicked.connect(self.edit_selected_item)
        category_btn_layout.addWidget(self.edit_item_btn)
        
        self.delete_item_btn = QPushButton("削除")
        self.delete_item_btn.clicked.connect(self.delete_selected_item)
        category_btn_layout.addWidget(self.delete_item_btn)
        
        category_layout.addLayout(category_btn_layout)
        
        top_layout.addWidget(category_box)
        
        # 新規タブ追加ボタン (最下部)
        self.add_tab_btn = QPushButton("新規タブ追加")
        self.add_tab_btn.clicked.connect(self.add_new_tab)
        main_layout.addWidget(self.add_tab_btn)
        
        # データベースからグループとカテゴリー一覧を取得
        self.load_groups()
        self.load_categories()
    
    def load_groups(self):
        """グループ一覧をロード"""
        try:
            self.group_list.clear()
            db = SkillMatrixDatabase()
            db.connect()
            groups = db.get_groups()
            db.close()
            
            for group in groups:
                self.group_list.addItem(group)
                
        except Exception as e:
            logger.error(f"グループロードエラー: {e}")
    
    def load_categories(self):
        """カテゴリーとスキル一覧をロード"""
        try:
            self.category_tree.clear()
            
            # サンプルデータ (後で実際のデータベースから取得するように修正)
            sample_categories = [
                {"name": "プログラミング", "skills": ["Python", "JavaScript", "Java"]},
                {"name": "データベース", "skills": ["SQL", "MongoDB", "Redis"]},
                {"name": "デザイン", "skills": ["UI/UX", "グラフィック", "Web"]},
            ]
            
            for category in sample_categories:
                # 親カテゴリー作成
                parent = QTreeWidgetItem(self.category_tree, [category["name"]])
                
                # 子スキル追加
                for skill in category["skills"]:
                    QTreeWidgetItem(parent, [skill])
                
                # 親アイテムを展開
                parent.setExpanded(True)
                
        except Exception as e:
            logger.error(f"カテゴリーロードエラー: {e}")
    
    def add_group(self):
        """グループ追加"""
        group_name, ok = QInputDialog.getText(self, "グループ追加", "グループ名:")
        if ok and group_name:
            try:
                # データベースにグループを追加
                db = SkillMatrixDatabase()
                db.connect()
                db.add_group_if_not_exists(group_name)
                db.close()
                
                # リストに追加
                self.group_list.addItem(group_name)
                logger.info(f"グループ {group_name} を追加しました")
                
                # メインウィンドウ更新
                self.update_main_window()
                
            except Exception as e:
                logger.error(f"グループ追加エラー: {e}")
                QMessageBox.warning(self, "エラー", f"グループの追加に失敗しました: {e}")
    
    def edit_group(self):
        """グループ編集"""
        current_item = self.group_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "編集するグループを選択してください")
            return
            
        current_name = current_item.text()
        new_name, ok = QInputDialog.getText(
            self, "グループ名編集", "新しいグループ名:", text=current_name)
            
        if ok and new_name and new_name != current_name:
            try:
                # データベース更新
                db = SkillMatrixDatabase()
                db.connect()
                db.execute(
                    "UPDATE members SET group_name = ? WHERE group_name = ?",
                    (new_name, current_name)
                )
                db.close()
                
                # リストアイテム更新
                self.group_list.currentItem().setText(new_name)
                logger.info(f"グループ名を {new_name} に変更しました")
                
                # メインウィンドウ更新
                self.update_main_window()
                
            except Exception as e:
                logger.error(f"グループ編集エラー: {e}")
                QMessageBox.warning(self, "エラー", f"グループの編集に失敗しました: {e}")
    
    def delete_group(self):
        """グループ削除"""
        current_item = self.group_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "削除するグループを選択してください")
            return
            
        group_name = current_item.text()
        reply = QMessageBox.question(
            self, "確認", f"グループ '{group_name}' を削除してもよろしいですか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # データベース更新
                db = SkillMatrixDatabase()
                db.connect()
                db.execute(
                    "UPDATE members SET group_name = NULL WHERE group_name = ?",
                    (group_name,)
                )
                db.close()
                
                # リストから削除
                row = self.group_list.row(current_item)
                self.group_list.takeItem(row)
                logger.info("グループを削除しました")
                
                # メインウィンドウ更新
                self.update_main_window()
                
            except Exception as e:
                logger.error(f"グループ削除エラー: {e}")
                QMessageBox.warning(self, "エラー", f"グループの削除に失敗しました: {e}")
    
    def add_category(self):
        """カテゴリー追加"""
        category_name, ok = QInputDialog.getText(self, "カテゴリー追加", "カテゴリー名:")
        if ok and category_name:
            # カテゴリーをツリーに追加
            new_category = QTreeWidgetItem(self.category_tree, [category_name])
            new_category.setExpanded(True)
            logger.info(f"カテゴリー {category_name} を追加しました")
            # TODO: データベースに保存する機能を実装
    
    def add_skill(self):
        """スキル追加"""
        selected = self.category_tree.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "スキルを追加するカテゴリーを選択してください")
            return
        
        # 選択されたアイテムが親カテゴリーか確認
        if selected.parent() is None:
            parent = selected
        else:
            parent = selected.parent()
        
        skill_name, ok = QInputDialog.getText(self, "スキル追加", "スキル名:")
        if ok and skill_name:
            # スキルをカテゴリーに追加
            QTreeWidgetItem(parent, [skill_name])
            logger.info(f"スキル {skill_name} をカテゴリー {parent.text(0)} に追加しました")
            # TODO: データベースに保存する機能を実装
    
    def edit_selected_item(self):
        """選択されたカテゴリーまたはスキルを編集"""
        selected = self.category_tree.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "編集するアイテムを選択してください")
            return
        
        current_name = selected.text(0)
        new_name, ok = QInputDialog.getText(
            self, "アイテム編集", "新しい名前:", text=current_name)
            
        if ok and new_name and new_name != current_name:
            selected.setText(0, new_name)
            
            # 親カテゴリーか子スキルかを判定
            item_type = "カテゴリー" if selected.parent() is None else "スキル"
            logger.info(f"{item_type} {current_name} を {new_name} に変更しました")
            # TODO: データベースの更新を実装
    
    def delete_selected_item(self):
        """選択されたカテゴリーまたはスキルを削除"""
        selected = self.category_tree.currentItem()
        if not selected:
            QMessageBox.warning(self, "警告", "削除するアイテムを選択してください")
            return
        
        item_name = selected.text(0)
        item_type = "カテゴリー" if selected.parent() is None else "スキル"
        
        reply = QMessageBox.question(
            self, "確認", f"{item_type} '{item_name}' を削除してもよろしいですか？",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # 親アイテムを取得
            parent = selected.parent()
            
            if parent:
                # 子スキルの場合
                index = parent.indexOfChild(selected)
                parent.takeChild(index)
            else:
                # 親カテゴリーの場合
                index = self.category_tree.indexOfTopLevelItem(selected)
                self.category_tree.takeTopLevelItem(index)
            
            logger.info(f"{item_type} {item_name} を削除しました")
            # TODO: データベースの更新を実装
    
    def add_new_tab(self):
        """新規タブを追加"""
        # 選択されたカテゴリーの確認
        selected = self.category_tree.currentItem()
        if not selected or selected.parent() is not None:
            QMessageBox.warning(self, "警告", "新規タブとして追加するカテゴリーを選択してください")
            return
        
        category_name = selected.text(0)
        
        try:
            # メインウィンドウのタブに追加
            logger.info(f"カテゴリー {category_name} の新規タブを追加")
            
            # ルートウィンドウを取得
            root = self.parent()
            while root.parent():
                root = root.parent()
            
            # タブ追加メソッドを呼び出し
            if hasattr(root, "add_category_tab") and root.add_category_tab(category_name):
                QMessageBox.information(self, "タブ追加", f"カテゴリー「{category_name}」の新規タブが追加されました")
            else:
                QMessageBox.warning(self, "エラー", "タブの追加に失敗しました")
                
        except Exception as e:
            logger.error(f"タブ追加エラー: {e}")
            import traceback
            logger.error(traceback.format_exc())
            QMessageBox.warning(self, "エラー", f"タブの追加に失敗しました: {e}")
    def update_main_window(self):
        """メインウィンドウに変更を通知"""
        try:
            # ルートウィンドウを取得
            root = self.parent()
            while root.parent():
                root = root.parent()
            
            # グループコンボボックス更新
            if hasattr(root, "update_group_combo"):
                logger.info("メインウィンドウのグループコンボボックス更新を呼び出し")
                root.update_group_combo()
        except Exception as e:
            logger.error(f"メインウィンドウ更新エラー: {e}")
