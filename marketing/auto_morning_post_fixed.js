const puppeteer = require('puppeteer');
const fs = require('fs');

const QUEUE_FILE = '/Users/agentjoselo/.openclaw/workspace/marketing/content-queue.json';
const LOG_FILE = '/Users/agentjoselo/.openclaw/workspace/marketing/posted-log.json';

async function getNextMorningPost() {
    const queue = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));
    const unpostedMorning = queue.posts.find(p => p.slot === 'morning' && p.posted === false);
    
    if (!unpostedMorning) {
        throw new Error('No unposted morning posts found');
    }
    
    return unpostedMorning;
}

function updateQueues(postId, tweetUrl) {
    const timestamp = new Date().toISOString();
    
    // Update content-queue.json
    const queue = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));
    const post = queue.posts.find(p => p.id === postId);
    if (post) {
        post.posted = true;
        post.posted_at = timestamp;
        post.tweet_url = tweetUrl;
    }
    queue.metadata.updated = timestamp;
    queue.metadata.latest_tweet = tweetUrl;
    fs.writeFileSync(QUEUE_FILE, JSON.stringify(queue, null, 2));
    
    // Update posted-log.json
    const log = JSON.parse(fs.readFileSync(LOG_FILE, 'utf8'));
    log.posted.push({
        id: postId,
        content: post.content,
        platforms: post.platforms,
        tweet_url: tweetUrl,
        reply_to: post.reply_to || null,
        posted_at: timestamp,
        note: post.note || `Morning post ${postId}`
    });
    fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2));
}

async function postTweet() {
    const post = await getNextMorningPost();
    
    console.log('=== Morning Post Automation ===');
    console.log(`Time: ${new Date()}`);
    console.log(`Post ID: ${post.id}`);
    console.log(`Content preview: ${post.content.substring(0, 50)}...`);
    console.log(`Type: ${post.type}`);
    console.log(`Reply to: ${post.reply_to || 'standalone'}`);
    console.log('');

    const browser = await puppeteer.launch({
        headless: false,
        userDataDir: '/Users/agentjoselo/.openclaw/browser/openclaw/user-data',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });

    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });

        let finalUrl;

        if (post.type === 'standalone' || !post.reply_to || post.reply_to === 'previous') {
            // Standalone tweet
            console.log('Opening compose page...');
            await page.goto('https://x.com/compose/post', { waitUntil: 'networkidle2' });
            await new Promise(r => setTimeout(r, 3000));

            console.log('Typing tweet content...');
            await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 15000 });
            await page.click('[data-testid="tweetTextarea_0"]');
            await page.type('[data-testid="tweetTextarea_0"]', post.content, { delay: 30 });
            await new Promise(r => setTimeout(r, 2000));

            console.log('Clicking post button...');
            await page.waitForSelector('[data-testid="tweetButton"]', { timeout: 10000 });
            
            // Wait for button to be enabled
            await page.waitForFunction(
                () => {
                    const btn = document.querySelector('[data-testid="tweetButton"]');
                    return btn && !btn.disabled;
                },
                { timeout: 10000 }
            );
            
            await page.click('[data-testid="tweetButton"]');
            await new Promise(r => setTimeout(r, 7000));

            // Get the tweet URL from the current page
            finalUrl = page.url();
            
            // Try to extract specific tweet URL if we're redirected
            if (finalUrl.includes('/status/')) {
                console.log(`Tweet posted at: ${finalUrl}`);
            } else {
                // Try to find it from the timeline
                const tweets = await page.$$('article[data-testid="tweet"]');
                if (tweets.length > 0) {
                    const firstTweet = tweets[0];
                    const timeLink = await firstTweet.$('time');
                    if (timeLink) {
                        const parent = await timeLink.evaluateHandle(el => el.parentElement);
                        const href = await parent.evaluate(el => el.getAttribute('href'));
                        if (href) {
                            finalUrl = `https://x.com${href}`;
                        }
                    }
                }
            }

        } else {
            // Reply to previous tweet
            console.log(`Opening previous tweet: ${post.reply_to}`);
            await page.goto(post.reply_to, { waitUntil: 'networkidle2' });
            await new Promise(r => setTimeout(r, 3000));

            console.log('Clicking reply button...');
            await page.waitForSelector('[data-testid="reply"]', { timeout: 10000 });
            await page.click('[data-testid="reply"]');
            await new Promise(r => setTimeout(r, 2000));

            console.log('Typing reply content...');
            await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
            await page.click('[data-testid="tweetTextarea_0"]');
            await page.type('[data-testid="tweetTextarea_0"]', post.content, { delay: 30 });
            await new Promise(r => setTimeout(r, 2000));

            console.log('Clicking reply button...');
            await page.waitForSelector('[data-testid="tweetButton"]', { timeout: 10000 });
            
            await page.waitForFunction(
                () => {
                    const btn = document.querySelector('[data-testid="tweetButton"]');
                    return btn && !btn.disabled;
                },
                { timeout: 10000 }
            );
            
            await page.click('[data-testid="tweetButton"]');
            await new Promise(r => setTimeout(r, 7000));

            // Try to get the reply URL
            const currentUrl = page.url();
            if (currentUrl.includes('/status/') && currentUrl !== post.reply_to) {
                finalUrl = currentUrl;
            } else {
                // Navigate to home and find the tweet
                await page.goto('https://x.com/roostrcapital', { waitUntil: 'networkidle2' });
                await new Promise(r => setTimeout(r, 3000));
                
                const tweets = await page.$$('article[data-testid="tweet"]');
                if (tweets.length > 0) {
                    const firstTweet = tweets[0];
                    const timeLink = await firstTweet.$('time');
                    if (timeLink) {
                        const parent = await timeLink.evaluateHandle(el => el.parentElement);
                        const href = await parent.evaluate(el => el.getAttribute('href'));
                        if (href) {
                            finalUrl = `https://x.com${href}`;
                        }
                    }
                }
            }
        }

        console.log(`\n✅ Tweet posted successfully!`);
        console.log(`URL: ${finalUrl}`);
        
        // Update the queue files
        updateQueues(post.id, finalUrl);
        console.log('✅ Files updated successfully!');
        console.log('=== Automation Complete ===');
        
        return finalUrl;

    } catch (error) {
        console.error('Error posting tweet:', error);
        throw error;
    } finally {
        await new Promise(r => setTimeout(r, 2000));
        await browser.close();
    }
}

postTweet()
    .then(url => {
        console.log(`\nFINAL SUCCESS: ${url}`);
        process.exit(0);
    })
    .catch(error => {
        console.error(`\nFAILED: ${error.message}`);
        process.exit(1);
    });
