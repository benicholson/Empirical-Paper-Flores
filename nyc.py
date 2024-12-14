import praw
from datetime import datetime, timedelta
from collections import Counter
import logging
import time
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Replace with your own credentials
reddit = praw.Reddit(
    client_id='KMByENPnTSKvbG0porDggw',
    client_secret='noIyW9PDLKjl51Eok9kHd41UcrdaWA',
    user_agent='benicholson sentiment scraper'
)
# The subreddit we are interested in
subreddit_name = 'denver'

def fetch_submissions_by_interval(reddit, subreddit_name, start, end):
    """Fetch submissions from the specified subreddit for the given date range in smaller intervals using PRAW's search_submissions method."""
    all_submissions = []
    interval_days = 30  # Fetching data in 30-day intervals
    interval_start = start

    while interval_start < end:
        interval_end = min(interval_start + timedelta(days=interval_days), end)
        logging.debug(f"Fetching submissions from {interval_start} to {interval_end}")
        submissions = reddit.subreddit(subreddit_name).search(
            "",
            sort="new",
            time_filter="all",
            params={"after": int(interval_start.timestamp()), "before": int(interval_end.timestamp())}
        )
        submissions_list = list(submissions)
        logging.debug(f"Fetched {len(submissions_list)} submissions in this interval")
        all_submissions.extend(submissions_list)
        interval_start = interval_end

    logging.debug(f"Total fetched submissions: {len(all_submissions)}")
    return all_submissions

def process_comments_batch(comments, year, result_data):
    for comment in comments:
        created_date = datetime.fromtimestamp(comment.created_utc)
        if created_date.year == year:
            result_data['comments_count_by_month'].update(
                created_date.strftime("%Y-%m")
            )

def process_submission(submission, year, result_data):
    created_date = datetime.fromtimestamp(submission.created_utc)
    if created_date.year == year:
        result_data['posts_count_by_month'][created_date.strftime("%Y-%m")] += 1
        submission.comments.replace_more(limit=0)
        process_comments_batch(submission.comments.list(), year, result_data)

def save_to_csv(year, result_data):
    filename = f'denver_total_mentions_{year}.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Year-Month', 'Total Posts', 'Total Comments'])
        for month in sorted(result_data['posts_count_by_month'].keys()):
            writer.writerow([
                month,
                result_data['posts_count_by_month'][month],
                result_data['comments_count_by_month'][month]
            ])
    logging.info(f"CSV file {filename} created successfully.")

def fetch_and_process_year(year):
    result_data = {
        "posts_count_by_month": Counter(),
        "comments_count_by_month": Counter()
    }

    logging.info(f"Fetching data for the year {year}")

    try:
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        submissions = fetch_submissions_by_interval(reddit, subreddit_name, start_date, end_date)
        logging.debug(f"Processing {len(submissions)} submissions for the year {year}")
        for submission in submissions:
            process_submission(submission, year, result_data)

    except Exception as e:
        logging.error(f"Error while processing year {year}: {e}")

    save_to_csv(year, result_data)
    return year

start_time = time.time()

years_to_process = range(2012, 2025)
max_threads = 5  # Adjust the number of threads based on your system's capabilities

with ThreadPoolExecutor(max_threads) as executor:
    futures = {executor.submit(fetch_and_process_year, year): year for year in years_to_process}

    for future in as_completed(futures):
        year = futures[future]
        try:
            result = future.result()
            logging.info(f"Completed processing for year {result}")
        except Exception as exc:
            logging.error(f"Year {year} generated an exception: {exc}")

end_time = time.time()

logging.info(f"Elapsed time: {end_time - start_time} seconds")