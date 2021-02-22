from services import twitter_controller
from opencv_module import color_controller

# Twitter認証情報を格納したJSONファイルパス
TWITTER_AUTH_INFO_FILE_PATH = 'auth_keys/twitter_auth_info.json'
# Google認証情報を格納したJSONファイルパス
GOOGLE_AUTH_INFO_FILE_PATH = ''

# 作成した画像の保存先ファイルパス
LOCAL_FILE_PATH = 'results/images/image.png'

# 検索対象のユーザー名
USER_ID = 'testusertw1'
# 検索結果の最大数
SEARCH_MAX_COUNT = 100


def main():
    """対象ユーザーのTwitterタイムラインから画像を取得.
        取得した画像で使用されている色の代表色を抽出し、画像として出力.
        出力した画像を対象ユーザーのメンション付きでツイートをする.
    """
    # TwitterAPIの認証
    twitter_api = twitter_controller.auth_twitter_api(
        TWITTER_AUTH_INFO_FILE_PATH)

    # Twitterのタイムラインから画像を取得する
    twitter_image_urls = twitter_controller.get_image_urls_from_twitter_timelines(
        twitter_api, USER_ID, SEARCH_MAX_COUNT)

    # 取得した画像で使われている代表色を抽出し、画像を作成、ローカルに保存
    color_controller.get_color_image(
        twitter_image_urls, LOCAL_FILE_PATH)

    # 作成した画像をTwitterタイムラインに投稿する
    twitter_controller.tweet_analysis_result(
        twitter_api, LOCAL_FILE_PATH, USER_ID)


if __name__ == "__main__":
    main()
