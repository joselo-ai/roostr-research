#!/usr/bin/env python3

import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from datetime import datetime

def post_afternoon_tweet():
    # w2-8: Position sizing methodology
    tweet_content = """Position sizing = conviction scoring:

Portfolio: $100k

$ALL (10/10): $20k (20%) — Highest conviction
$PGR (9/10): $15k (15%) — Second highest
$KTB (7.5/10): $10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: $3.8k (3.8%).

Risk-adjusted by score."""
    
    # Reply to the latest tweet in thread
    previous_tweet_url = "https://x.com/roostrcapital/status/2022053449681314006"
    
    # Set up Chrome with existing profile
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/Users/agentjoselo/Library/Application Support/Google/Chrome")
    options.add_argument("profile-directory=Default")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"[{datetime.now()}] Opening previous tweet: {previous_tweet_url}")
        driver.get(previous_tweet_url)
        time.sleep(5)
        
        print(f"[{datetime.now()}] Clicking reply button...")
        reply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="reply"]'))
        )
        reply_button.click()
        time.sleep(3)
        
        print(f"[{datetime.now()}] Typing tweet content...")
        tweet_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
        )
        tweet_box.send_keys(tweet_content)
        time.sleep(2)
        
        print(f"[{datetime.now()}] Clicking post button...")
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]'))
        )
        post_button.click()
        time.sleep(5)
        
        # Try to extract tweet URL
        try:
            tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            if tweets:
                last_tweet = tweets[-1]
                time_element = last_tweet.find_element(By.TAG_NAME, 'time')
                tweet_link = time_element.find_element(By.XPATH, './ancestor::a')
                tweet_url = tweet_link.get_attribute('href')
                print(f"[{datetime.now()}] SUCCESS: {tweet_url}")
                return tweet_url
        except Exception as e:
            print(f"[{datetime.now()}] Could not extract URL: {e}")
            return driver.current_url
            
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {e}")
        raise
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    try:
        url = post_afternoon_tweet()
        print(f"TWEET_URL={url}")
        sys.exit(0)
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)
