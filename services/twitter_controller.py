import twitter
import time
import urllib
import os
from utils import util

TWEET_MODE = 'extended'


def auth_twitter_api(twitter_auth_file_path: str):
    """TwitterAPI認証処理

    Args:
        twitter_auth_file_path (str): Twitter認証情報が格納されたJSONファイルパス
    """
    # Twitter認証情報をJSONファイルから読み取り
    twitter_auth_info = util.read_json_file(twitter_auth_file_path)

    # Twitter認証処理
    return twitter.Api(
        twitter_auth_info['consumer_key'], twitter_auth_info['consumer_secret'],
        twitter_auth_info['access_token_key'], twitter_auth_info['access_token_secret'], tweet_mode=TWEET_MODE)


def get_image_urls_from_twitter_timelines(twitter_api, user_id: str, seach_max_count: int):
    """指定ユーザーのタイムラインから画像URLを取得する

    Args:
        twitter_api (twitter.api.API): 認証済みのTwitterAPI
        user_id (str): 検索対象のユーザーID
        seach_max_count (int): 検索結果の最大数
    Returns:
        list: 取得した画像URLのリスト
    """
    # タイムラインを取得
    search_results = twitter_api.GetUserTimeline(
        screen_name=user_id,
        count=seach_max_count,
    )

    image_urls = []
    # タイムラインに画像がある場合はurlを取得する
    for content in search_results:
        if content.media:
            image_urls.append(content.media[0].media_url)

    # 指定されたユーザーIDのタイムラインから画像URLを取得する
    return image_urls


def tweet_analysis_result(twitter_api, image_path, user_id):
    """色画像を対象ユーザーへメンション付きでタイムラインに投稿する

    Args:
        twitter_api (twitter.api.API): 認証済みのTwitterAPI
        image_path (str): 作成した色画像のファイルパス
        user_id (str): 検索対象のユーザーID
    """
    message = f'色解析結果を投稿します。' if image_path is not None else 'タイムラインから画像を取得できませんでした。'

    twitter_api.PostUpdates(f'@{user_id}さんの{message}', media=image_path)

    return
