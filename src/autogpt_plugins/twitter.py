"""This module contains functions for interacting with the Twitter API."""
from __future__ import annotations
from . import AutoGPTTwitter
import json

plugin = AutoGPTTwitter()


def get_my_tweets(number_of_tweets: int, exclude_retweets: bool) -> str:
    user_id = plugin.client.get_me(user_auth=True)["data"]["id"]
    return _get_tweets_for_user(user_id, number_of_tweets, exclude_retweets)


def get_user_tweets(target_username: str, number_of_tweets: int, exclude_retweets: bool) -> str:
    """Searches a user's tweets given a number of items to retrive and returns a dataframe.

    Args:
        target_username (str): The user to search.
        num_of_items (int): The number of items to retrieve.

    Returns:
        str: The dataframe containing the tweets.
    """

    user_id = plugin.client.get_user(
        username=target_username, user_auth=True)["data"]["id"]
    return _get_tweets_for_user(user_id, number_of_tweets, exclude_retweets)


def _get_tweets_for_user(user_id: str, number_of_tweets: int, exclude_retweets: bool) -> str:
    if (number_of_tweets < 5):
        number_of_tweets = 5
    elif (number_of_tweets > 100):
        number_of_tweets = 100
    tweets = plugin.client.get_users_tweets(
        user_id, expansions=["author_id"], tweet_fields=["created_at", "public_metrics", "author_id"], user_fields=["username"], max_results=number_of_tweets, exclude="retweets" if exclude_retweets else None, user_auth=True)

    # Create a dictionary to map user IDs to usernames
    user_id_to_username = {}
    for user in tweets["includes"]["users"]:
        user_id_to_username[user["id"]] = user["username"]

    data = []

    for tweet in tweets["data"]:
        author_username = user_id_to_username[tweet["author_id"]]
        data.append(
            {
                "text": tweet["text"],
                "author_username": author_username,
                "like_count": tweet["public_metrics"]["like_count"],
                "retweet_count": tweet["public_metrics"]["retweet_count"],
                "reply_count": tweet["public_metrics"]["reply_count"],
                "quote_count": tweet["public_metrics"]["quote_count"],
                "impression_count": tweet["public_metrics"]["impression_count"],
                "created_at": tweet["created_at"],
                "author_id": tweet["author_id"],
                "tweet_id": tweet["id"],
            }
        )

    # return data in json format
    df = json.dumps(data)

    return df
