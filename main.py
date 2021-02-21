from services import twitter_controller
from opencv_module import color_controller

# Twitter認証情報を格納したJSONファイルパス
TWITTER_AUTH_INFO_FILE_PATH = 'auth_keys/twitter_auth_info.json'
# Google認証情報を格納したJSONファイルパス
GOOGLE_AUTH_INFO_FILE_PATH = ''

# 検索対象のユーザー名
USER_ID = '27_kmmr'
# 検索結果の最大数
SEARCH_MAX_COUNT = 100


def main():
    """対象ユーザーのTwitterタイムラインから画像を取得.
        取得した画像で使用されている色の代表色を抽出し、画像として出力.
        出力した画像を対象ユーザーのメンション付きでツイートをする.
    """
    # Twitterのタイムラインから画像を取得する
    twitter_image_urls = twitter_controller.get_image_urls_from_twitter_timelines(
        TWITTER_AUTH_INFO_FILE_PATH, USER_ID, SEARCH_MAX_COUNT)

    # 取得した画像で使われている代表色を抽出し、画像を作成
    typical_color_image = color_controller.get_color_image(twitter_image_urls)


if __name__ == "__main__":
    main()
