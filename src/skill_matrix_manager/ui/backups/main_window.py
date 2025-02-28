    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QComboBox,
    QPushButton,
    QMessageBox
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tab_widget = self.create_tab_widget()
        self.tab_handlers = TabHandlers(self.tab_widget)
        self.init_ui()
        self.setup_group_sync()
        
        # タイムスタンプとユーザー名を設定
        self.timestamp = "2025-02-21 22:31:05"
        self.username = "GingaDza"

    def init_ui(self):
        self.setWindowTitle('スキルマトリクスマネージャー')
        self.setGeometry(100, 100, 1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # 左側のパネル（3:7の分割）
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # グループ選択コンボボックス
        self.group_combo = QComboBox()
        self.group_combo.currentIndexChanged.connect(self.on_group_selected)
        left_layout.addWidget(self.group_combo)
        
        # ユーザーリスト
        self.user_list = QListWidget()
        self.user_list.itemSelectionChanged.connect(self.on_user_selection_changed)
        left_layout.addWidget(self.user_list)
        
        # ユーザー操作ボタン
        button_layout = QHBoxLayout()
        self.add_user_btn = QPushButton("追加")
        self.edit_user_btn = QPushButton("編集")
        self.delete_user_btn = QPushButton("削除")
        
        self.add_user_btn.clicked.connect(self.on_add_user_clicked)
        self.edit_user_btn.clicked.connect(self.on_edit_user_clicked)
        self.delete_user_btn.clicked.connect(self.on_delete_user_clicked)
        
        button_layout.addWidget(self.add_user_btn)
        button_layout.addWidget(self.edit_user_btn)
        button_layout.addWidget(self.delete_user_btn)
        left_layout.addLayout(button_layout)
        
        main_layout.addWidget(left_panel, stretch=3)
        main_layout.addWidget(self.tab_widget, stretch=7)

        # 初期データのロード
        self.load_initial_data()
        
        self.show()

    def create_tab_widget(self):
        tab_widget = QTabWidget()
        
        # システム管理タブの作成
        system_tab = QTabWidget()
        self.initial_setup_tab = InitialSetupTab(self)
        system_tab.addTab(self.initial_setup_tab, "初期設定")
        system_tab.addTab(QWidget(), "データ入出力")
        system_tab.addTab(QWidget(), "システム情報")
        
        # スキル分析タブの作成
        analysis_tab = QTabWidget()
        analysis_tab.addTab(QWidget(), "総合評価")
        
        # スキルギャップタブを初期化して追加
        self.skill_gap_tab = SkillGapTab(self)
        analysis_tab.addTab(self.skill_gap_tab, "スキルギャップ")

        # メインタブに追加
        tab_widget.addTab(system_tab, "システム管理")
        tab_widget.addTab(analysis_tab, "スキル分析")
        
        return tab_widget

    def setup_group_sync(self):
        """グループリストとコンボボックスの同期設定"""
        self.initial_setup_tab.group_list.itemSelectionChanged.connect(self.sync_group_selection)
        QTimer.singleShot(100, self.update_group_combo)

    def update_group_combo(self):
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


    def sync_group_selection(self):
        """グループリストの選択をコンボボックスに反映"""
        current_item = self.initial_setup_tab.group_list.currentItem()
        if current_item:
            index = self.group_combo.findText(current_item.text())
            if index >= 0:
                self.group_combo.setCurrentIndex(index)
                self.update_user_list(current_item.text())

    def on_group_selected(self, index):
        """グループが選択されたときの処理"""
        if index >= 0:
            group_name = self.group_combo.currentText()
            # InitialSetupTabのグループ選択を更新
            for i in range(self.initial_setup_tab.group_list.count()):
                if self.initial_setup_tab.group_list.item(i).text() == group_name:
                    self.initial_setup_tab.group_list.setCurrentRow(i)
                    self.update_user_list(group_name)
                    break

    def on_user_selection_changed(self):
        """ユーザー選択が変更されたときの処理"""
        current_user = self.user_list.currentItem()
        if current_user:
            user_name = current_user.text()
            group_name = self.group_combo.currentText()
            # ユーザー情報を全てのタブに反映
            self.tab_handlers.on_member_selected(user_name, user_name, group_name)
            
            # スキルギャップタブにメンバー情報を設定
            if hasattr(self, 'skill_gap_tab'):
                self.skill_gap_tab.set_member(user_name, user_name, group_name)

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


    def on_add_tab_clicked(self):
        """新規タブ追加ボタンがクリックされたときの処理"""
        current_item = self.initial_setup_tab.category_tree.currentItem()
        if not current_item:
            QMessageBox.warning(self, "警告", "カテゴリーを選択してください。")
            return

        # カテゴリー名とスキルを取得
        if current_item.parent():  # スキルが選択されている場合
            category_name = current_item.parent().text(0)
            skills = [current_item.text(0)]
        else:  # カテゴリーが選択されている場合
            category_name = current_item.text(0)
            skills = []
            for i in range(current_item.childCount()):
                skills.append(current_item.child(i).text(0))

        if not skills:
            QMessageBox.warning(self, "警告", "スキルが見つかりません。")
            return

        # 選択されているユーザーを取得
        current_user = self.user_list.currentItem()
        if not current_user:
            QMessageBox.warning(self, "警告", "ユーザーを選択してください。")
            return

        # タブを追加し、ユーザー情報を設定
        evaluation_tab = self.tab_handlers.add_new_tab(category_name, skills)
        
        # ユーザー情報をタブに設定
        user_name = current_user.text()
        group_name = self.group_combo.currentText()
        self.tab_handlers.on_member_selected(user_name, user_name, group_name)

    def load_initial_data(self):
        """初期データのロード"""
        QTimer.singleShot(0, self.update_group_combo)

    def on_add_user_clicked(self):
        """ユーザー追加ボタンのクリックハンドラ"""
        if self.group_combo.currentIndex() < 0:
            QMessageBox.warning(self, "警告", "グループを選択してください。")
            return
        # TODO: ユーザー追加の実装

    def on_edit_user_clicked(self):
        """ユーザー編集ボタンのクリックハンドラ"""
        if not self.user_list.currentItem():
            QMessageBox.warning(self, "警告", "編集するユーザーを選択してください。")
            return
        # TODO: ユーザー編集の実装

    def on_delete_user_clicked(self):
        """ユーザー削除ボタンのクリックハンドラ"""
        if not self.user_list.currentItem():
            QMessageBox.warning(self, "警告", "削除するユーザーを選択してください。")
            return
        # TODO: ユーザー削除の実装
