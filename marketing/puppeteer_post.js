const puppeteer = require('puppeteer');
const fs = require('fs');

const TWEET_CONTENT = `Position sizing = conviction scoring:

Portfolio: $100k

$ALL (10/10): $20k (20%) — Highest conviction
$PGR (9/10): $15k (15%) — Second highest
$KTB (7.5/10): $10k (10%) — Diversification

Size follows conviction.
Stops at -8% to -10%.
Max loss if all hit stops: $3.8k (3.8%).

Risk-adjusted by score.`;

const PREVIOUS_TWEET_URL = 'https://x.com/roostrcapital/status/2022053449681314006';

async function postTweet() {
    const browser = await puppeteer.launch({
        headless: false,
        userDataDir: '/Users/agentjoselo/.openclaw/browser/openclaw/user-data'
    });

    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });

        console.log('Navigating to previous tweet...');
        await page.goto(PREVIOUS_TWEET_URL, { waitUntil: 'networkidle2' });
        await new Promise(r => setTimeout(r, 3000));

        console.log('Looking for reply button...');
        // Wait for and click reply button
        await page.waitForSelector('[data-testid="reply"]', { timeout: 10000 });
        await page.click('[data-testid="reply"]');
        await new Promise(r => setTimeout(r, 2000));

        console.log('Typing tweet content...');
        // Wait for compose box and type
        await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
        await page.type('[data-testid="tweetTextarea_0"]', TWEET_CONTENT);
        await new Promise(r => setTimeout(r, 2000));

        console.log('Clicking post button...');
        // Click the post/reply button
        await page.waitForSelector('[data-testid="tweetButton"]', { timeout: 10000 });
        await page.click('[data-testid="tweetButton"]');
        await new Promise(r => setTimeout(r, 5000));

        // Get the new tweet URL
        // After posting, X might redirect or stay on the same page
        // We need to find the new tweet's URL
        const currentUrl = page.url();
        console.log(`Current URL after posting: ${currentUrl}`);

        // Try to find the new tweet link
        try {
            await new Promise(r => setTimeout(r, 3000));
            const tweets = await page.$$('article[data-testid="tweet"]');
            console.log(`Found ${tweets.length} tweets on page`);
            
            if (tweets.length > 0) {
                // Get the last tweet (should be our new one)
                const lastTweet = tweets[tweets.length - 1];
                const timeLink = await lastTweet.$('time');
                if (timeLink) {
                    const parent = await timeLink.$('xpath/..');
                    const href = await parent.evaluate(el => el.getAttribute('href'));
                    const fullUrl = `https://x.com${href}`;
                    console.log(`New tweet URL: ${fullUrl}`);
                    return fullUrl;
                }
            }
        } catch (e) {
            console.log(`Could not extract specific tweet URL: ${e.message}`);
        }

        return currentUrl;

    } catch (error) {
        console.error('Error posting tweet:', error);
        throw error;
    } finally {
        await new Promise(r => setTimeout(r, 3000));
        await browser.close();
    }
}

postTweet()
    .then(url => {
        console.log(`SUCCESS: Tweet posted at ${url}`);
        fs.writeFileSync('/Users/agentjoselo/.openclaw/workspace/marketing/tweet_url.txt', url);
        process.exit(0);
    })
    .catch(error => {
        console.error(`FAILED: ${error.message}`);
        process.exit(1);
    });
