#!/usr/bin/env python3

import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

def post_to_x():
    # Tweet content
    tweet_content = """Position sizing = conviction scoring:

Portfolio: $100k

$ALL (10/10): $20k (20%) — Highest conviction
$PGR (9/10): $15k (15%) — Second highest
$KTB (7.5/10): $10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: $3.8k (3.8%).

Risk-adjusted by score."""
    
    previous_tweet_url = "https://x.com/roostrcapital/status/2022053449681314006"
    
    # Set up Chrome with existing profile to use logged-in session
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=/Users/agentjoselo/Library/Application Support/Google/Chrome")
    options.add_argument("profile-directory=Default")
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # Navigate to the previous tweet
        print(f"Opening previous tweet: {previous_tweet_url}")
        driver.get(previous_tweet_url)
        time.sleep(5)
        
        # Find and click reply button
        print("Clicking reply button...")
        reply_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="reply"]'))
        )
        reply_button.click()
        time.sleep(3)
        
        # Type the tweet
        print("Typing tweet content...")
        tweet_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]'))
        )
        tweet_box.send_keys(tweet_content)
        time.sleep(2)
        
        # Click the post button
        print("Clicking post button...")
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]'))
        )
        post_button.click()
        time.sleep(5)
        
        # Get the current URL (should be the new tweet)
        current_url = driver.current_url
        print(f"Tweet posted! URL: {current_url}")
        
        # Wait a bit more to ensure the tweet is fully posted
        time.sleep(3)
        
        # Try to get the actual tweet URL from the page
        # After posting a reply, X usually shows the conversation
        # We need to find the new tweet's URL
        try:
            # Look for the latest tweet in the conversation
            tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            if tweets:
                # The last tweet should be ours
                last_tweet = tweets[-1]
                time_element = last_tweet.find_element(By.TAG_NAME, 'time')
                tweet_link = time_element.find_element(By.XPATH, './ancestor::a')
                tweet_url = tweet_link.get_attribute('href')
                print(f"New tweet URL: {tweet_url}")
                return tweet_url
        except Exception as e:
            print(f"Could not extract tweet URL: {e}")
            return current_url
            
    except Exception as e:
        print(f"Error posting tweet: {e}")
        raise
    finally:
        time.sleep(3)
        driver.quit()

if __name__ == "__main__":
    try:
        url = post_to_x()
        print(f"SUCCESS: {url}")
    except Exception as e:
        print(f"FAILED: {e}")
        exit(1)
