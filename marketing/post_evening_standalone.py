#!/usr/bin/env python3

import time
import json
import sys
import tempfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def post_evening_tweet():
    tweet_content = """Why social arbitrage works:

Chris Camillo's Dorel Industries play (2020):

• March: COVID lockdowns begin
• Social media: Parents panic-buying bikes for kids
• Dorel: Major bike manufacturer
• Entry: $3.50
• Exit: $22
• Return: 629%

Wall Street saw it 3 months later.

Edge = speed of information."""
    
    # Use a temporary profile to avoid conflicts
    temp_dir = tempfile.mkdtemp()
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={temp_dir}")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"[{datetime.now()}] Opening X login...")
        driver.get("https://x.com/login")
        time.sleep(3)
        
        print(f"[{datetime.now()}] MANUAL LOGIN REQUIRED")
        print(f"Please log in to @roostrcapital in the browser window")
        print(f"After logging in, press ENTER to continue...")
        input()
        
        print(f"[{datetime.now()}] Navigating to home...")
        driver.get("https://x.com/home")
        time.sleep(5)
        
        print(f"[{datetime.now()}] Clicking compose box...")
        compose_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
        )
        compose_box.click()
        time.sleep(2)
        
        print(f"[{datetime.now()}] Typing content...")
        compose_box.send_keys(tweet_content)
        time.sleep(2)
        
        print(f"[{datetime.now()}] Clicking post...")
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]'))
        )
        post_button.click()
        time.sleep(5)
        
        print(f"[{datetime.now()}] Navigating to profile...")
        driver.get("https://x.com/roostrcapital")
        time.sleep(5)
        
        tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
        if tweets:
            first_tweet = tweets[0]
            time_element = first_tweet.find_element(By.TAG_NAME, 'time')
            tweet_link = time_element.find_element(By.XPATH, './ancestor::a')
            tweet_url = tweet_link.get_attribute('href')
            print(f"[{datetime.now()}] SUCCESS: {tweet_url}")
            return tweet_url
            
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    try:
        url = post_evening_tweet()
        print(f"TWEET_URL={url}")
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)
