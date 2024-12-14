import requests
import datetime
import csv
import time
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

PUSHSHIFT_BASE_URL = "https://api.pushshift.io/reddit/search/submission/"


def fetch_posts(subreddit, year, keywords):
    posts = []
    logging.info(f'Fetching posts for year: {year}')
    start_time = int(datetime.datetime(year, 1, 1).timestamp())
    end_time = int(datetime.datetime(year, 12, 31, 23, 59, 59).timestamp())
    query = ' OR '.join(keywords)

    params = {
        'subreddit': subreddit,
        'q': query,
        'after': start_time,
        'before': end_time,
        'sort': 'desc',
        'size': 500  # Requests max 500 posts per batch
    }

    while True:
        response = requests.get(PUSHSHIFT_BASE_URL, params=params)
        data = response.json()

        if 'data' not in data or len(data['data']) == 0:
            break

        submissions = data['data']

        for submission in submissions:
            post_date = datetime.datetime.fromtimestamp(submission['created_utc'])
            logging.debug(f'Fetched post: {submission["title"]} created on {post_date}')
            posts.append(submission)

        # Update 'before' parameter to fetch the next batch of posts
        params['before'] = submissions[-1]['created_utc']
        time.sleep(1)  # To handle rate limiting

    logging.info(f'Total posts fetched: {len(posts)}')
    return posts


def count_mentions_and_sentiments(posts, keywords):
    mention_counts = {'posts': 0, 'comments': 0, 'positive': 0, 'negative': 0, 'neutral': 0}
    analyzer = SentimentIntensityAnalyzer()

    logging.info(f'Analyzing posts for year: 2022, total submissions: {len(posts)}')
    try:
        for submission in posts:
            if any(keyword in submission['title'].lower() for keyword in keywords):
                logging.info(f'Keyword found in post: {submission["title"]}')
                mention_counts['posts'] += 1
                score = analyzer.polarity_scores(submission['title'])
                logging.info(f'Post sentiment scores: {score}')
                if score['compound'] >= 0.05:
                    mention_counts['positive'] += 1
                elif score['compound'] <= -0.05:
                    mention_counts['negative'] += 1
                else:
                    mention_counts['neutral'] += 1

    except Exception as e:
        logging.error(f'Error analyzing posts for year 2022: {e}')
    return mention_counts


def save_to_csv(mention_counts, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Post Mentions', 'Comment Mentions', 'Positive Sentiments', 'Negative Sentiments',
                         'Neutral Sentiments'])
        writer.writerow([2022, mention_counts['posts'], mention_counts['comments'], mention_counts['positive'],
                         mention_counts['negative'], mention_counts['neutral']])


keywords = ["immigration", "immigrant", "immigrants", "migrants", "migrant"]
year = 2022
posts = fetch_posts('chicago', year, keywords)
mention_counts = count_mentions_and_sentiments(posts, keywords)
save_to_csv(mention_counts, 'draft files/mentions2022.csv')