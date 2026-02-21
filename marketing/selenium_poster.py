#!/usr/bin/env python3
"""
Post tweet via Selenium automation
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import sys

def post_tweet(tweet_text):
    """Post tweet via Selenium"""
    
    # Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--user-data-dir=/Users/agentjoselo/Library/Application Support/Google/Chrome')
    chrome_options.add_argument('--profile-directory=Default')
    
    driver = None
    try:
        # Initialize driver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to compose page
        driver.get('https://x.com/compose/post')
        time.sleep(3)
        
        # Find the tweet compose box
        # Try multiple selectors
        selectors = [
            '[data-testid="tweetTextarea_0"]',
            'div[contenteditable="true"]',
            'div[role="textbox"]'
        ]
        
        tweet_box = None
        for selector in selectors:
            try:
                tweet_box = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                break
            except:
                continue
        
        if not tweet_box:
            print("❌ Could not find tweet compose box")
            return None
        
        # Type the tweet
        tweet_box.click()
        time.sleep(0.5)
        tweet_box.send_keys(tweet_text)
        time.sleep(1)
        
        # Find and click the Post button
        post_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButton"]')
        post_button.click()
        
        # Wait for post to complete
        time.sleep(3)
        
        # Get the tweet URL from the current page
        current_url = driver.current_url
        
        # Close driver
        driver.quit()
        
        return current_url
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if driver:
            driver.quit()
        return None

if __name__ == "__main__":
    tweet_text = """Risk discipline in practice:

Every position has:
• Pre-defined stop loss (-15% to -20%)
• Position size based on conviction (2%-10%)
• Max portfolio risk: 10%

No exceptions. No "let me see what happens."

When stop hits → exit. No questions.

Discipline > hope."""
    
    print("🐓 Posting tweet via Selenium...")
    url = post_tweet(tweet_text)
    
    if url:
        print(f"✅ Posted: {url}")
        sys.exit(0)
    else:
        print("❌ Failed to post")
        sys.exit(1)
