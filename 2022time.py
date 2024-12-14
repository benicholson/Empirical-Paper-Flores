import praw
from datetime import datetime
from collections import defaultdict
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

# Prepare a dictionary to count the results by month
posts_count_by_month = defaultdict(int)

# Function to check if text contains any of the keywords
def contains_keywords(text, keywords):
    text = text.lower()
    for keyword in keywords:
        if keyword in text:
            return True
    return False

# Fetching submissions
logging.info("Fetching posts...")
post_counter = 0

query = ' OR '.join(keywords)
for submission in reddit.subreddit(subreddit_name).search(query=query, time_filter='all', limit=None):
    created_date = datetime.fromtimestamp(submission.created_utc)
    if 2022 <= created_date.year <= 2024 and contains_keywords(submission.title + " " + submission.selftext, keywords):
        logging.debug(f"Post found: {submission.title} (Date: {created_date})")
        posts_count_by_month[created_date.strftime("%Y-%m")] += 1
        post_counter += 1
    time.sleep(1)  # Add delay to handle rate limiting

logging.info(f"Total posts fetched: {post_counter}")

# Print the monthly counts
logging.info("\nPosts count by month from 2022 to 2024:")
for month, count in sorted(posts_count_by_month.items()):
    logging.info(f"{month}: {count}")