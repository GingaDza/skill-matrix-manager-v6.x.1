#!/usr/bin/env python3
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QComboBox, QFormLayout, QMessageBox, QDialogButtonBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from src.skill_matrix_manager.utils.debug_logger import DebugLogger

logger = DebugLogger.get_logger()

class MemberDialog(QDialog):
    """メンバー追加・編集ダイアログ"""
    
    # メンバー変更シグナル (id, name, email, group)
    memberChanged = pyqtSignal(int, str, str, str)
    
    def __init__(self, service, member_id=None, parent=None):
        """
        初期化
        
        Args:
            service: SkillServiceインスタンス
            member_id: 編集するメンバーID (Noneの場合は新規追加)
            parent: 親ウィジェット
        """
        super().__init__(parent)
        self.service = service
        self.member_id = member_id
        self.is_edit_mode = member_id is not None
        
        # ウィンドウタイトル
        self.setWindowTitle("メンバー編集" if self.is_edit_mode else "メンバー追加")
        
        # UI初期化
        self.setup_ui()
        
        # 編集モードの場合はメンバー情報を読み込み
        if self.is_edit_mode:
            self.load_member_data()
    
    def setup_ui(self):
        """UI初期化"""
        layout = QVBoxLayout(self)
        
        # フォームレイアウト
        form_layout = QFormLayout()
        
        # 名前入力
        self.name_edit = QLineEdit()
        form_layout.addRow("名前:", self.name_edit)
        
        # メールアドレス入力
        self.email_edit = QLineEdit()
        form_layout.addRow("メール:", self.email_edit)
        
        # グループ選択
        self.group_combo = QComboBox()
        self.group_combo.setEditable(True)
        self.load_groups()
        form_layout.addRow("グループ:", self.group_combo)
        
        layout.addLayout(form_layout)
        
        # ボタン
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        # サイズ設定
        self.resize(400, 200)
    
    def load_groups(self):
        """グループ一覧を読み込み"""
        try:
            groups = self.service.get_groups()
            self.group_combo.clear()
            self.group_combo.addItem("", "")  # 空の選択肢
            for group in groups:
                self.group_combo.addItem(group, group)
        except Exception as e:
            logger.error(f"グループ読み込みエラー: {e}")
    
    def load_member_data(self):
        """メンバー情報を読み込み"""
        try:
            member = self.service.get_member(self.member_id)
            if member:
                self.name_edit.setText(member['name'])
                self.email_edit.setText(member['email'] or "")
                
                # グループ設定
                if member['group_name']:
                    index = self.group_combo.findData(member['group_name'])
                    if index >= 0:
                        self.group_combo.setCurrentIndex(index)
                    else:
                        self.group_combo.setCurrentText(member['group_name'])
        except Exception as e:
            logger.error(f"メンバー情報読み込みエラー: {e}")
            QMessageBox.warning(self, "エラー", f"メンバー情報の読み込みに失敗しました: {e}")
    
    def accept(self):
        """OKボタンが押された時の処理"""
        # 入力値の取得
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        group = self.group_combo.currentText().strip()
        
        # バリデーション
        if not name:
            QMessageBox.warning(self, "入力エラー", "名前は必須項目です")
            return
        
        try:
            if self.is_edit_mode:
                # メンバー更新
                result = self.service.update_member(self.member_id, name, email, group)
                if result:
                    logger.info(f"メンバー更新成功: ID={self.member_id}, 名前={name}")
                    # シグナル発行
                    self.memberChanged.emit(self.member_id, name, email, group)
                    super().accept()
                else:
                    QMessageBox.critical(self, "エラー", "メンバーの更新に失敗しました")
            else:
                # メンバー追加
                member_id = self.service.add_member(name, email, group)
                if member_id:
                    logger.info(f"メンバー追加成功: ID={member_id}, 名前={name}")
                    # シグナル発行
                    self.memberChanged.emit(member_id, name, email, group)
                    super().accept()
                else:
                    QMessageBox.critical(self, "エラー", "メンバーの追加に失敗しました")
                    
        except Exception as e:
            logger.error(f"メンバー保存エラー: {e}")
            QMessageBox.critical(self, "エラー", f"メンバー情報の保存に失敗しました: {e}")


class MemberManagementDialog(QDialog):
    """メンバー管理ダイアログ"""
    
    # メンバーリスト変更シグナル
    membersChanged = pyqtSignal()
    
    def __init__(self, service, parent=None):
        super().__init__(parent)
        self.service = service
        
        self.setWindowTitle("メンバー管理")
        self.setup_ui()
        self.load_members()
    
    def setup_ui(self):
        """UI初期化"""
        layout = QVBoxLayout(self)
        
        # グループフィルタ
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("グループ:"))
        
        self.group_filter = QComboBox()
        self.group_filter.addItem("すべて", None)
        filter_layout.addWidget(self.group_filter)
        self.group_filter.currentIndexChanged.connect(self.on_filter_changed)
        
        layout.addLayout(filter_layout)
        
        # メンバーリスト
        self.member_list = QComboBox()
        self.member_list.setMinimumWidth(300)
        layout.addWidget(self.member_list)
        
        # ボタンレイアウト
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("追加")
        self.add_btn.clicked.connect(self.on_add)
        button_layout.addWidget(self.add_btn)
        
        self.edit_btn = QPushButton("編集")
        self.edit_btn.clicked.connect(self.on_edit)
        button_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QPushButton("削除")
        self.delete_btn.clicked.connect(self.on_delete)
        button_layout.addWidget(self.delete_btn)
        
        layout.addLayout(button_layout)
        
        # 閉じるボタン
        close_btn = QPushButton("閉じる")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        # サイズ設定
        self.resize(500, 300)
    
    def load_groups(self):
        """グループリスト読み込み"""
        try:
            current_filter = self.group_filter.currentData()
            
            groups = self.service.get_groups()
            self.group_filter.clear()
            self.group_filter.addItem("すべて", None)
            
            for group in groups:
                self.group_filter.addItem(group, group)
            
            # 以前の選択を復元
            if current_filter:
                index = self.group_filter.findData(current_filter)
                if index >= 0:
                    self.group_filter.setCurrentIndex(index)
            
        except Exception as e:
            logger.error(f"グループ読み込みエラー: {e}")
    
    def load_members(self):
        """メンバーリスト読み込み"""
        try:
            group_filter = self.group_filter.currentData()
            members = self.service.get_members(group_filter)
            
            self.member_list.clear()
            for member in members:
                display_text = f"{member['name']} ({member['group_name'] or '未所属'})"
                self.member_list.addItem(display_text, member['id'])
                
            # ボタン状態更新
            self.update_buttons()
            
        except Exception as e:
            logger.error(f"メンバー読み込みエラー: {e}")
    
    def update_buttons(self):
        """ボタン状態の更新"""
        has_members = self.member_list.count() > 0
        self.edit_btn.setEnabled(has_members)
        self.delete_btn.setEnabled(has_members)
    
    def on_filter_changed(self):
        """フィルタ変更時の処理"""
        self.load_members()
    
    def on_add(self):
        """メンバー追加"""
        dialog = MemberDialog(self.service, parent=self)
        dialog.memberChanged.connect(self.on_member_changed)
        dialog.exec_()
    
    def on_edit(self):
        """メンバー編集"""
        if self.member_list.count() == 0:
            return
            
        member_id = self.member_list.currentData()
        if not member_id:
            return
            
        dialog = MemberDialog(self.service, member_id, parent=self)
        dialog.memberChanged.connect(self.on_member_changed)
        dialog.exec_()
    
    def on_delete(self):
        """メンバー削除"""
        if self.member_list.count() == 0:
            return
            
        member_id = self.member_list.currentData()
        if not member_id:
            return
            
        # 確認ダイアログ
        member_name = self.member_list.currentText()
        reply = QMessageBox.question(
            self, "確認", 
            f"{member_name} を削除しますか？\nこの操作は元に戻せません。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                result = self.service.delete_member(member_id)
                if result:
                    logger.info(f"メンバー削除: ID={member_id}")
                    self.on_member_changed(member_id, "", "", "")
                else:
                    QMessageBox.critical(self, "エラー", "メンバーの削除に失敗しました")
            except Exception as e:
                logger.error(f"メンバー削除エラー: {e}")
                QMessageBox.critical(self, "エラー", f"メンバー削除でエラーが発生しました: {e}")
    
    def on_member_changed(self, member_id, name, email, group):
        """メンバー情報変更時の処理"""
        # メンバーリスト更新
        self.load_members()
        # グループリスト更新
        self.load_groups()
        # シグナル発行
        self.membersChanged.emit()
