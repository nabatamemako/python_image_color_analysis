import json


def read_json_file(json_file_path: str):
    """Jsonファイル内データの読み込み

    Args:
        json_file_path (str): Jsonファイルのパス

    Returns:
        dict: ファイルの辞書型データ
    """
    json_open = open(json_file_path, 'r')
    return json.load(json_open)
