import praw
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import logging
import time
from textblob import TextBlob
import csv
from dateutil.relativedelta import relativedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your own credentials
reddit = praw.Reddit(
    client_id='KMByENPnTSKvbG0porDggw',
    client_secret='noIyW9PDLKjl51Eok9kHd41UcrdaWA',
    user_agent='benicholson sentiment scraper'
)

# The subreddit and keywords we are interested in
subreddit_name = 'chicago'
keywords = ['immigration', 'migrants', 'migrant', 'immigrant', 'immigrants',
            'asylum', 'refugee', 'visa', 'naturalization', 'citizenship',
            'border', 'deportation', 'DACA', 'undocumented', 'resettlement',
            'green card']

# Function to perform sentiment analysis with caching
sentiment_cache = {}


def analyze_sentiment(text):
    if text in sentiment_cache:
        return sentiment_cache[text]
    analysis = TextBlob(text)
    sentiment = 'neutral'
    if analysis.sentiment.polarity > 0:
        sentiment = 'positive'
    elif analysis.sentiment.polarity < 0:
        sentiment = 'negative'
    sentiment_cache[text] = sentiment
    return sentiment


def fetch_submissions_in_batches(reddit, subreddit_name, query, start, end):
    """Fetch submissions from the specified subreddit within a given time frame and handle pagination."""
    all_submissions = []
    for submission in reddit.subreddit(subreddit_name).search(query=query, sort='new', time_filter='all'):
        submission_date = datetime.fromtimestamp(submission.created_utc)
        if start <= submission_date <= end:
            all_submissions.append(submission)
    return all_submissions


def process_comments_batch(comments, year, result_data):
    comments_to_process = [comment for comment in comments if datetime.fromtimestamp(comment.created_utc).year == year]
    result_data['comments_count_by_month'].update(
        datetime.fromtimestamp(comment.created_utc).strftime("%Y-%m") for comment in comments_to_process)

    for comment in comments_to_process:
        comment_created_date = datetime.fromtimestamp(comment.created_utc)
        sentiment = analyze_sentiment(comment.body)
        result_data['comment_sentiment'][comment_created_date.strftime("%Y-%m")][sentiment] += 1


def process_submission(submission, year, result_data):
    created_date = datetime.fromtimestamp(submission.created_utc)
    if created_date.year == year:
        result_data['posts_count_by_month'][created_date.strftime("%Y-%m")] += 1
        sentiment = analyze_sentiment(submission.title + " " + submission.selftext)
        result_data['post_sentiment'][created_date.strftime("%Y-%m")][sentiment] += 1
        submission.comments.replace_more(limit=0)
        process_comments_batch(submission.comments.list(), year, result_data)


def save_to_csv(year, result_data):
    filename = f'chungularmentions{year}.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year-Month', 'Total Posts', 'Positive Posts', 'Negative Posts', 'Neutral Posts',
                         'Total Comments', 'Positive Comments', 'Negative Comments', 'Neutral Comments'])
        for month in sorted(result_data['posts_count_by_month'].keys()):
            writer.writerow([
                month,
                result_data['posts_count_by_month'][month],
                result_data['post_sentiment'][month]['positive'],
                result_data['post_sentiment'][month]['negative'],
                result_data['post_sentiment'][month]['neutral'],
                result_data['comments_count_by_month'][month],
                result_data['comment_sentiment'][month]['positive'],
                result_data['comment_sentiment'][month]['negative'],
                result_data['comment_sentiment'][month]['neutral']
            ])
    logging.info(f"CSV file {filename} created successfully.")


def fetch_and_process_year(year):
    result_data = {
        "posts_count_by_month": Counter(),
        "comments_count_by_month": Counter(),
        "post_sentiment": defaultdict(Counter),
        "comment_sentiment": defaultdict(Counter)
    }

    logging.info(f"Fetching data for the year {year}")

    try:
        for keyword in keywords:
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            submissions = fetch_submissions_in_batches(reddit, subreddit_name, keyword, start_date, end_date)
            for submission in submissions:
                process_submission(submission, year, result_data)
            requestor = reddit.auth.limits
            if requestor['remaining'] < 10:
                sleep_time = max(60, requestor['reset'] - int(time.time()) + 5)
                logging.info(f"Rate limit imminent. Sleeping for {sleep_time} seconds.")
                time.sleep(sleep_time)
            else:
                time.sleep(1)
    except Exception as e:
        logging.error(f"Error while processing year {year}: {e}")

    save_to_csv(year, result_data)


start_time = time.time()

years_to_process = range(2012, 2019)

for year in years_to_process:
    fetch_and_process_year(year)

end_time = time.time()

logging.info(f"Elapsed time: {end_time - start_time} seconds")