#!/usr/bin/env node

const { chromium } = require('playwright');

async function postToX() {
  const browser = await chromium.launch({ 
    headless: false,
    channel: 'chrome'
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // Navigate to the previous tweet
    const previousTweetUrl = 'https://x.com/roostrcapital/status/2022053449681314006';
    await page.goto(previousTweetUrl);
    await page.waitForTimeout(3000);
    
    // Look for the reply button and click it
    const replyButton = page.locator('[data-testid="reply"]').first();
    await replyButton.click();
    await page.waitForTimeout(2000);
    
    // Type the tweet content
    const tweetContent = `Position sizing = conviction scoring:

Portfolio: $100k

$ALL (10/10): $20k (20%) — Highest conviction
$PGR (9/10): $15k (15%) — Second highest
$KTB (7.5/10): $10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: $3.8k (3.8%).

Risk-adjusted by score.`;
    
    const tweetBox = page.locator('[data-testid="tweetTextarea_0"]');
    await tweetBox.fill(tweetContent);
    await page.waitForTimeout(2000);
    
    // Click the Reply button to post
    const postButton = page.locator('[data-testid="tweetButton"]');
    await postButton.click();
    await page.waitForTimeout(5000);
    
    // Get the URL of the new tweet
    // After posting, X redirects or shows the new tweet
    // We need to get the URL from the page
    const currentUrl = page.url();
    console.log('TWEET_URL:', currentUrl);
    
    await page.waitForTimeout(3000);
    
  } catch (error) {
    console.error('Error posting tweet:', error);
    throw error;
  } finally {
    await browser.close();
  }
}

postToX();
