import praw
from datetime import datetime
from collections import defaultdict

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
comments_count_by_month = defaultdict(int)

# Function to check if text contains any of the keywords
def contains_keywords(text, keywords):
    text = text.lower()
    for keyword in keywords:
        if keyword in text:
            return True
    return False

# Fetching submissions and their comments
print("Fetching posts and comments...")
post_counter = 0
comment_counter = 0
matched_comment_counter = 0

for submission in reddit.subreddit(subreddit_name).search(query="|".join(keywords),
                                                          time_filter='year',
                                                          syntax='cloudsearch'):
    post_counter += 1
    created_date = datetime.fromtimestamp(submission.created_utc)
    if created_date.year == 2022 and contains_keywords(submission.title + " " + submission.selftext, keywords):
        print(f"Post found: {submission.title} (Date: {created_date})")
        posts_count_by_month[created_date.strftime("%Y-%m")] += 1
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comment_counter += 1
            comment_created_date = datetime.fromtimestamp(comment.created_utc)
            if comment_created_date.year == 2022 and contains_keywords(comment.body, keywords):
                print(f"Comment found: {comment.body[:30]}... (Date: {comment_created_date})")
                comments_count_by_month[comment_created_date.strftime("%Y-%m")] += 1
                matched_comment_counter += 1

print(f"Total posts fetched: {post_counter}")
print(f"Total comments fetched: {comment_counter}")
print(f"Total matched comments: {matched_comment_counter}")

# Print the monthly counts
print("\nPosts count by month in 2022:")
for month, count in sorted(posts_count_by_month.items()):
    print(f"{month}: {count}")

print("\nComments count by month in 2022:")
for month, count in sorted(comments_count_by_month.items()):
    print(f"{month}: {count}")