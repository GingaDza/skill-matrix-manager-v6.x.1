from PyQt5.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QTreeWidgetItem
)

class UIComponents:
    def __init__(self, parent=None):
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.widget = QWidget()
        layout = QVBoxLayout(self.widget)
        
        self.add_tab_btn = QPushButton("新規タブ追加")
        self.add_tab_btn.clicked.connect(self.on_add_tab_clicked)
        
        layout.addWidget(self.add_tab_btn)

    def on_add_tab_clicked(self):
        """選択されたカテゴリーとスキルでタブを追加"""
        # 正しい参照経路でカテゴリーアイテムを取得 - MainWindowからinitial_setup_tabを経由する
        try:
            # 親ウィンドウから初期設定タブへの参照を取得
            if hasattr(self.parent, 'initial_setup_tab'):
                initial_setup_tab = self.parent.initial_setup_tab
                current_item = initial_setup_tab.category_tree.currentItem()
                
                if not current_item:
                    QMessageBox.warning(self.widget, "警告", "カテゴリーを選択してください。")
                    return

                # カテゴリー名とスキルを取得
                if current_item.parent():  # スキルが選択されている場合
                    category_name = current_item.parent().text(0)
                    skills = [current_item.text(0)]  # 選択されたスキルのみ
                else:  # カテゴリーが選択されている場合
                    category_name = current_item.text(0)
                    skills = []
                    # カテゴリー配下の全スキルを取得
                    for i in range(current_item.childCount()):
                        skill_item = current_item.child(i)
                        skills.append(skill_item.text(0))

                if not skills:
                    QMessageBox.warning(self.widget, "警告", "スキルが見つかりません。")
                    return

                # タブを追加
                self.parent.tab_handlers.add_new_tab(category_name, skills)
            else:
                QMessageBox.warning(self.widget, "エラー", "初期設定タブが見つかりません。")
        except Exception as e:
            QMessageBox.critical(self.widget, "エラー", f"処理中にエラーが発生しました: {str(e)}")
