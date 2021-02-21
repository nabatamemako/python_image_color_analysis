import twitter
import time
import urllib
import os
from utils import util

TWEET_MODE = 'extended'


def get_image_urls_from_twitter_timelines(twitter_auth_file_path: str, user_id: str, seach_max_count: int):
    """指定ユーザーのタイムラインから画像URLを取得する

    Args:
        twitter_auth_file_path (str): Twitter認証情報が格納されたJSONファイルパス
        user_id (str): 検索対象のユーザーID
        seach_max_count (int): 検索結果の最大数
    Returns:
        list: 取得した画像URLのリスト
    """
    # Twitter認証情報をJSONファイルから読み取り
    twitter_auth_info = util.read_json_file(twitter_auth_file_path)

    # Twitter認証処理
    twitter_api = twitter.Api(
        twitter_auth_info['consumer_key'], twitter_auth_info['consumer_secret'],
        twitter_auth_info['access_token_key'], twitter_auth_info['access_token_secret'], tweet_mode=TWEET_MODE
    )

    # 指定されたユーザーIDのタイムラインから画像URLを取得する
    return get_timeline_image_urls(twitter_api, user_id, seach_max_count)


def get_timeline_image_urls(twitter_api, user_id: str, seach_max_count: int):
    """タイムラインから画像URLを取得する

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

    return image_urls
