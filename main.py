import requests
import csv
from bs4 import BeautifulSoup
from datetime import datetime

no_quote_url = 'https://twitter.com/gabriel_TheCode/status/1413841963569328132'
tweet_url = 'https://twitter.com/CaroleDanwe/status/1413537284029308930'
GOOGLE_BOT_UA = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
BROWSER_UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
headers = {'User-Agent': GOOGLE_BOT_UA}

tweet_data = []

# all possible header
csv_headers = set()

# history of visited tweet to avoid double scrapping
visited_tweets = []



def merge_column():
    """
    Use levein
    """
    pass


def extract_lines(content:str, origin: str) -> dict:
    """
    Extract date from a tweet text and make a dict with
    """
    cleaned_data = {'origin': origin}
    _lines = content.split('\n')
    for line in _lines:
        kv = line.split(':')
        cleaned_data.update({
            kv[0].strip(): kv[1].strip().replace('https', '')
        })
    
    return cleaned_data


def build_csv_row(tweet_dict: dict) -> list:
    """
    Build a list out of data in a dict and map it to the headers available
    """
    row = []
    for key in csv_headers:
        row.append(tweet_dict.get(key, ''))

    return row


def save_tweets(tweets: list[dict]):
    """
    Save the tweets to a csv
    """
    file = open(f"tweets_{datetime.now()}.csv", 'w+')
    _rows = []
    for tweet in tweets:
        _rows.append(build_csv_row(tweet))

    writer = csv.writer(file)
    # write the csv headers
    writer.writerow(list(csv_headers))
    writer.writerows(_rows)
    file.close()
    return True


def get_quoted_tweet(tweet_content):
    """
    Will use search to get quoted tweets....
    - search a tweet url
    - all result containing that URL are the Quoted one
    """
    pass


def get_tweet_content(url: str):
    
    response = requests.get(url, headers=headers)
    if response.ok:
        soup = BeautifulSoup(response.text, "html.parser")
        content_soup = soup.find('p', class_='TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text')
        
        rs = extract_lines(content_soup.text, url)
        for k in rs.keys():
            csv_headers.add(k)
        csv_headers.add('origin')
        tweet_data.append(rs)
        quote_tweet_soup = content_soup.find('a', class_='twitter-timeline-link u-hidden')
        print(url, "<=== Extracted")
        visited_tweets.append(url)
        if quote_tweet_soup is not None:
            next_url = quote_tweet_soup.get('data-expanded-url')
            get_tweet_content(next_url)
        

    else:
        print('an issue')
        quit(1)

get_tweet_content(url=tweet_url)
# print(csv_headers, ' headers \n ', len(tweet_data) )
save_tweets(tweet_data)
print("Visited {} links".format(len(visited_tweets)))