import tweepy
import time
import csv

# Insert bearer token
BEARER_TOKEN = "INSERT BEARER TOKEN"

START_TIME = '2017-06-01T00:00:00Z'
END_TIME = '2022-06-01T00:00:00Z'

users = {
    "jimcramer": "14216123",
    "barackobama": "813286",
    "elonmusk": "44196397",
}


def write_tweets_to_csv(tweets, name):
    with open(f'{name}.csv', 'w', newline='') as file:
        w = csv.DictWriter(file, fieldnames=['name', 'date', 'text'], delimiter=',')
        w.writeheader()
        w.writerows(tweets)


def get_all_tweets_from_page(page):
    tweets = []
    for tweet in page:
        tweets.append({"name": str(44196397), "text": tweet.get("text"), "date": str(tweet.get("created_at"))[0:10], })

    # do not abuse twitter api
    time.sleep(1)
    return tweets


def fetch_and_save_user_tweets(username):
    tweet_fields = ['created_at', 'text']
    token = None
    all_tweets = []

    try:
        for page in tweepy.Paginator(client.search_all_tweets, query=f"from:{users.get(username)}", end_time=END_TIME,
                                     start_time=START_TIME, next_token=token, tweet_fields=tweet_fields,
                                     max_results=100):
            # save tweets
            all_tweets += get_all_tweets_from_page(page[0])

            # check token and repeat or exit
            token = page.meta.get("next_token")
            print(f"Total tweets: {len(all_tweets)}")
            if not token:
                break

    except Exception as e:
        print(f"Twitter threw an exception with reason {e.response.reason}")
        print(f"Saving tweets fetched so far for {username}")
        print(f"Last tweet saved is from {all_tweets[-1].get('date')}")

    write_tweets_to_csv(all_tweets, username)


if __name__ == "__main__":
    print("Starting ...")
    client = tweepy.Client(bearer_token=BEARER_TOKEN)
    for user in users:
        print(f"Fetching tweets for {user}")
        fetch_and_save_user_tweets(user)
    print("Tweets have been saved")
