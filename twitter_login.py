from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint
import asyncio
import os

Minimum_Tweets=100
query=["misinformation","fake news","disinformation"]

async def perform_login(client):
    print("Performing login with credentials...")
    config = ConfigParser()
    config.read('config.ini')

    email = config.get('X', 'email')
    username = config.get('X', 'username')
    password = config.get('X', 'password')

    await client.login(
        auth_info_2=email,
        auth_info_1=username,
        password=password
    )
    print("Logged in successfully!")

async def main():
    config = ConfigParser()
    config.read('config.ini')
    username = config.get('X', 'username') # Still need username for potential future use

    client = Client(language='en-us')
    cookies_file = 'cookies.json'

    if os.path.exists(cookies_file) and os.path.getsize(cookies_file) > 0:
        try:
            client.load_cookies(cookies_file)
            print("Loaded cookies from session file.")
            print("Cookies loaded. Assuming session is valid for now.")
        except Exception as e:
            print(f"Could not load cookies or session is invalid: {e}")
            # Fallback to login
            await perform_login(client)
    else:
        await perform_login(client)

    # Save cookies after any successful login/session validation
    client.save_cookies(cookies_file)
    print("Session cookies saved.")

# Run asyncio loop
if __name__ == "__main__":
    asyncio.run(main())
