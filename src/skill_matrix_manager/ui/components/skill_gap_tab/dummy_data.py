def get_dummy_data():
    """スキルギャップタブ用のダミーデータを生成"""
    # 5段階のスキル評価データ
    dummy_data = {
        'stage_1': {  # 現在
            'Python': 3,
            'Java': 2,
            'JavaScript': 4,
            'SQL': 3,
            'Git': 3
        },
        'stage_2': {  # 3ヶ月後
            'Python': 4,
            'Java': 2,
            'JavaScript': 4,
            'SQL': 4,
            'Git': 3
        },
        'stage_3': {  # 6ヶ月後
            'Python': 4,
            'Java': 3,
            'JavaScript': 5,
            'SQL': 4,
            'Git': 4
        },
        'stage_4': {  # 9ヶ月後
            'Python': 5,
            'Java': 3,
            'JavaScript': 5,
            'SQL': 5,
            'Git': 4
        },
        'stage_5': {  # 目標
            'Python': 5,
            'Java': 4,
            'JavaScript': 5,
            'SQL': 5,
            'Git': 5
        }
    }
    
    return dummy_data
