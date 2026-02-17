const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    userDataDir: '/Users/agentjoselo/.openclaw/browser/openclaw/user-data'
  });
  
  const page = await browser.newPage();
  
  // Navigate to the latest tweet
  await page.goto('https://x.com/roostrcapital/status/2022053449681314006', {
    waitUntil: 'networkidle2'
  });
  
  // Wait a bit for page to fully load
  await new Promise(resolve => setTimeout(resolve, 3000));
  
  // Click reply button
  const replyButton = await page.waitForSelector('[data-testid="reply"]', { timeout: 10000 });
  await replyButton.click();
  
  // Wait for compose box
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Type the tweet content
  const tweetContent = `Why social arbitrage works:

Chris Camillo's Dorel Industries play (2020):

• March: COVID lockdowns begin
• Social media: Parents panic-buying bikes for kids
• Dorel: Major bike manufacturer
• Entry: $3.50
• Exit: $22
• Return: 629%

Wall Street saw it 3 months later.

Edge = speed of information.`;
  
  const composeBox = await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 5000 });
  await composeBox.type(tweetContent);
  
  // Wait a bit before posting
  await new Promise(resolve => setTimeout(resolve, 2000));
  
  // Click tweet button
  const tweetButton = await page.waitForSelector('[data-testid="tweetButton"]', { timeout: 5000 });
  await tweetButton.click();
  
  // Wait for tweet to post and get URL
  await new Promise(resolve => setTimeout(resolve, 5000));
  
  const currentUrl = page.url();
  console.log('TWEET_URL:', currentUrl);
  
  await browser.close();
})();
