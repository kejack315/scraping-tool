import json
import requests
import pandas as pd
import datetime

API_URL = "https://api.producthunt.com/v2/api/graphql"

# Specify API token
MY_API_TOKEN = "a5BOcd-z0WSB8-D0R1AkKCuzUWHjHPoJFLr5zxdSLZM"

# Specify query
query = {
    "query": "query todayPosts($cursor: String) { posts(after: $cursor) { edges { node { id name tagline createdAt votesCount } } pageInfo { endCursor hasNextPage } } }",
    "variables": {"cursor": None}
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + MY_API_TOKEN,
    'Host': 'api.producthunt.com'
}

posts = []
has_next_page = True

# Get arbitrary number of records in the 'posts' list (I chose 500)
while has_next_page and len(posts) < 500:
    # today's posts data from Product Hunt API
    today_posts = requests.post(API_URL, headers=headers, data=json.dumps(query))
    today_posts = today_posts.json()

    # Extract the edges (posts) from the response
    edges = today_posts['data']['posts']['edges']
    if not edges:
        break  # No more data, exit the loop

    # Add the current set of posts to the list
    posts.extend(edges)

    # Check if there is more data available for pagination
    page_info = today_posts['data']['posts']['pageInfo']
    has_next_page = page_info['hasNextPage']

    # Get the next cursor for pagination, I tried next page for pagination but not work
    cursor = page_info['endCursor']
    query['variables']['cursor'] = cursor


# Convert it to a DataFrame
df = pd.json_normalize(posts)

# Save 500 data if needed, just remove the "#" next line
# data_csv = df.to_csv(path_or_buf='c:/python/recent_data.csv', encoding='utf_8_sig', index=False)
# To select by datetime, must convert the "createdAt" column to datetime type first

df['node.createdAt'] = pd.to_datetime(df['node.createdAt'])

# Calculate the date range for the last 7 days in UTC timezone because I'm in Perth
end_date = datetime.datetime.now(datetime.timezone.utc)
start_date = end_date - datetime.timedelta(days=7)

# Use conditional filtering to select data for the last 7 days
recent_data = df[(df['node.createdAt'] >= start_date) & (df['node.createdAt'] <= end_date)]

# Save to recent_data contains data for the last 7 days
recent_data_csv = recent_data.to_csv(path_or_buf='c:/python/recent_data.csv', encoding='utf_8_sig', index=False)
print("Recent 7 days' data saved successfully as 'recent_data.csv'")
