"""スキルギャップのデータモデル"""

class SkillDataModel:
    """スキルと目標値のデータモデル"""
    
    def __init__(self):
        self.hierarchy = {}
        self.staged_targets = {}
    
    def load_test_data(self):
        """テスト用データの読み込み"""
        # グループ、カテゴリ、スキルの階層データ
        self.hierarchy = {
            "prog": {
                "name": "プログラミング",
                "categories": {
                    "lang": {
                        "name": "言語",
                        "skills": {
                            "python": {"name": "Python", "current": 3, "target": 5},
                            "java": {"name": "Java", "current": 2, "target": 4},
                            "js": {"name": "JavaScript", "current": 4, "target": 5}
                        }
                    },
                    "db": {
                        "name": "データベース",
                        "skills": {
                            "mysql": {"name": "MySQL", "current": 4, "target": 5},
                            "mongodb": {"name": "MongoDB", "current": 2, "target": 4}
                        }
                    },
                    "frame": {
                        "name": "フレームワーク",
                        "skills": {
                            "django": {"name": "Django", "current": 3, "target": 5},
                            "react": {"name": "React", "current": 2, "target": 4},
                            "vue": {"name": "Vue.js", "current": 1, "target": 3}
                        }
                    }
                }
            },
            "design": {
                "name": "デザイン",
                "categories": {
                    "ui": {
                        "name": "UI/UX",
                        "skills": {
                            "figma": {"name": "Figma", "current": 3, "target": 5},
                            "xd": {"name": "Adobe XD", "current": 2, "target": 4}
                        }
                    },
                    "graphic": {
                        "name": "グラフィック",
                        "skills": {
                            "ps": {"name": "Photoshop", "current": 4, "target": 5},
                            "ai": {"name": "Illustrator", "current": 3, "target": 4}
                        }
                    }
                }
            },
            "business": {
                "name": "ビジネススキル",
                "categories": {
                    "mgmt": {
                        "name": "マネジメント",
                        "skills": {
                            "project": {"name": "プロジェクト管理", "current": 3, "target": 5},
                            "team": {"name": "チームリーダーシップ", "current": 2, "target": 4}
                        }
                    },
                    "comm": {
                        "name": "コミュニケーション",
                        "skills": {
                            "presentation": {"name": "プレゼンテーション", "current": 4, "target": 5},
                            "writing": {"name": "文書作成", "current": 3, "target": 4}
                        }
                    }
                }
            }
        }
        
        # 段階的目標のテストデータ
        self.staged_targets = {
            "prog": {
                "lang": [
                    {"time": 10, "unit": "時間", "level": 1, "skills": {"python": 2, "java": 1, "js": 2}},
                    {"time": 30, "unit": "時間", "level": 2, "skills": {"python": 3, "java": 2, "js": 3}},
                    {"time": 60, "unit": "時間", "level": 3, "skills": {"python": 4, "java": 3, "js": 4}}
                ]
            }
        }
