import numpy as np
import cv2
import requests


def get_color_image(image_urls, local_file_path):
    """画像URLから画像データ取得し、画像の代表色を抽出.
        取得した代表色で画像を作成.

    Args:
        image_urls (list): 画像URLのリスト
        local_file_path (str): 画像の保存先

    Returns:
        Numpy: 代表色の画像
    """
    if not image_urls:
        return

    image_list = []
    # 画像URLから画像データを取得
    for url in image_urls:
        resp = requests.get(url, stream=True).raw
        image = np.asarray(bytearray(resp.read()), dtype='uint8')
        image_list.append(cv2.imdecode(image, cv2.IMREAD_COLOR))

    # 画像の色を抽出する
    color_list = extract_colors(image_list)

    # 抽出した色を基に1枚の画像を作成
    colors_image = image_generator(color_list, local_file_path)

    # 画像確認用
    # cv2.imshow('aaa', colors_image)
    # cv2.waitKey(0)

    return colors_image


def extract_colors(image_list, main_color_num=5):
    """画像の代表色を抽出する

    Args:
        image_list (list): 画像データのリスト
        main_color_num (int, optional): 抽出する代表色の数. Defaults to 5.

    Returns:
        NumPy: 代表色データのリスト
    """
    # 全画像のRGB値
    all_pixels = None

    for image in image_list:
        # 画像の色データ（RGB値）の並びを整形
        pixels = image.reshape((-1, 3))

        if all_pixels is None:
            all_pixels = pixels
        else:
            all_pixels = np.vstack((all_pixels, pixels))

    criteria = (cv2.TERM_CRITERIA_EPS +
                cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, _, center = cv2.kmeans(np.float32(all_pixels), main_color_num,
                              None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    typical_colors = np.array(center, np.int)

    return typical_colors


def image_generator(color_list, local_file_path, image_width=200, image_height=50):
    """抽出した代表色で画像を作成し、ローカルに保存する

    Args:
        color_list (NumPy): 代表色データのリスト
        local_file_path (str): 画像の保存先
        image_width (int, optional): 作成画像の横幅. Defaults to 100.
        image_height (int, optional): 作成画像の高さ. Defaults to 20.
    """
    image_width_per_color = int(image_width/len(color_list))
    image_width_mod = image_width_per_color * len(color_list)
    create_image = np.zeros((image_height, image_width_mod, 3), np.uint8)

    for color_indx, color in enumerate(color_list):
        startX = color_indx * image_width_per_color
        endX = (color_indx + 1) * image_width_per_color
        create_image[0:image_height, startX:endX] = color

    cv2.imwrite(local_file_path, create_image)

    return
