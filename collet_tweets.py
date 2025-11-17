import asyncio
from twikit import Client, TooManyRequests
import csv
import os
from datetime import datetime

query_terms = [
    "(election OR vote OR ballot OR democracy) (fake news OR propaganda OR disinformation OR influence network)",
    "(coordinated campaign OR bot network OR paid trolls OR influence operation)",
    "(war OR conflict OR attack OR deepfake) (misinformation OR disinformation OR propaganda)",
    "(telegram OR whatsapp OR youtube OR reddit) (fake OR leak OR exposed OR hoax)",
    "(deepfake OR AI-generated OR bot farm) (fake news OR propaganda OR misinformation)"
]
max_tweets = 1000  # change depending on how big your dataset should be


async def collect_tweets(client):
    dataset = []
    print("\nSearching tweets...\n")

    for q in query_terms:
        print(f"Searching for: {q}")

        retries = 0
        max_retries = 5
        tweets = [] # Initialize tweets to an empty list
        while retries < max_retries:
            try:
                tweets = await client.search_tweet(q, product='Latest', count=100)   # first batch
                break # If successful, break out of the retry loop
            except TooManyRequests:
                retries += 1
                print(f"Rate limit hit on initial search (attempt {retries}/{max_retries}). Waiting 60 seconds...")
                await asyncio.sleep(60)
            except Exception as e:
                print(f"An unexpected error occurred during initial search: {e}")
                break # Break on other errors

        if retries == max_retries:
            print(f"Max retries reached for query: {q}. Skipping this query.")
            continue # Skip to the next query_term if max retries reached

        for tw in tweets:
            dataset.append([
                tw.id,
                tw.user.name,
                tw.user.location,
                tw.created_at,
                tw.text.replace("\n", " ")  # remove line breaks
            ])

        # Keep scrolling (pagination)
        while len(dataset) < max_tweets:
            try:
                tweets = await tweets.next()
                for tw in tweets:
                    dataset.append([
                        tw.id,
                        tw.user.name,
                        tw.user.location,
                        tw.created_at,
                        tw.text.replace("\n", " ")
                    ])
            except TooManyRequests:
                print("Rate limit hit. Waiting 30 seconds...")
                await asyncio.sleep(30)
            except:
                break

    print(f"\nCollected {len(dataset)} tweets.")
    return dataset


async def main():
    client = Client("en-US")

    # Load cookies saved from previous login
    client.load_cookies("cookies.json")
    print("Cookies Loaded. Fetching tweets...")

    tweets = await collect_tweets(client)

    # Save CSV
    filename = f"tweets_dataset_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tweet_id", "username", "location", "timestamp", "text"])
        writer.writerows(tweets)

    print(f"\nCSV Saved Successfully -> {filename}")


if __name__ == "__main__":
    asyncio.run(main())
