#!/usr/bin/env python3

import time
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime

def post_evening_tweet():
    # w2-9: Social arbitrage case study
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
    
    # Set up Chrome with existing profile
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/Users/agentjoselo/Library/Application Support/Google/Chrome")
    options.add_argument("profile-directory=Default")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        print(f"[{datetime.now()}] Opening X home...")
        driver.get("https://x.com/home")
        time.sleep(5)
        
        print(f"[{datetime.now()}] Clicking compose tweet box...")
        # Click the main tweet compose box
        compose_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
        )
        compose_box.click()
        time.sleep(2)
        
        print(f"[{datetime.now()}] Typing tweet content...")
        compose_box.send_keys(tweet_content)
        time.sleep(2)
        
        print(f"[{datetime.now()}] Clicking post button...")
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButtonInline"]'))
        )
        post_button.click()
        time.sleep(5)
        
        # Wait for tweet to post and navigate to profile to find it
        print(f"[{datetime.now()}] Navigating to profile to find tweet...")
        driver.get("https://x.com/roostrcapital")
        time.sleep(5)
        
        # Try to extract the latest tweet URL
        try:
            tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            if tweets:
                first_tweet = tweets[0]  # Latest tweet should be first
                time_element = first_tweet.find_element(By.TAG_NAME, 'time')
                tweet_link = time_element.find_element(By.XPATH, './ancestor::a')
                tweet_url = tweet_link.get_attribute('href')
                print(f"[{datetime.now()}] SUCCESS: {tweet_url}")
                return tweet_url
        except Exception as e:
            print(f"[{datetime.now()}] Could not extract URL: {e}")
            return "https://x.com/roostrcapital"
            
    except Exception as e:
        print(f"[{datetime.now()}] ERROR: {e}")
        raise
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    try:
        url = post_evening_tweet()
        print(f"TWEET_URL={url}")
        sys.exit(0)
    except Exception as e:
        print(f"FAILED: {e}")
        sys.exit(1)
