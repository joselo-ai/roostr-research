const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const QUEUE_FILE = path.join(__dirname, 'content-queue.json');
const LOG_FILE = path.join(__dirname, 'posted-log.json');

async function findNextMorningPost() {
    const queue = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));
    
    // Find the next unposted "morning" slot post
    const nextPost = queue.posts.find(post => 
        post.slot === 'morning' && post.posted === false
    );
    
    if (!nextPost) {
        console.log('No unposted morning posts found in queue');
        return null;
    }
    
    console.log(`Found next morning post: ${nextPost.id}`);
    console.log(`Content preview: ${nextPost.content.substring(0, 50)}...`);
    
    return nextPost;
}

async function postToX(content, replyToUrl = null) {
    const browser = await puppeteer.launch({
        headless: false,
        executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        userDataDir: '/Users/agentjoselo/Library/Application Support/Google/Chrome',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--profile-directory=Default'
        ]
    });

    try {
        const page = await browser.newPage();
        await page.setViewport({ width: 1280, height: 800 });

        if (replyToUrl && replyToUrl !== 'previous') {
            // Reply to specific tweet
            console.log(`Navigating to previous tweet: ${replyToUrl}`);
            await page.goto(replyToUrl, { waitUntil: 'networkidle2' });
            await new Promise(r => setTimeout(r, 3000));

            console.log('Clicking reply button...');
            await page.waitForSelector('[data-testid="reply"]', { timeout: 10000 });
            await page.click('[data-testid="reply"]');
            await new Promise(r => setTimeout(r, 2000));
        } else {
            // Standalone tweet - use compose URL directly
            console.log('Navigating to compose page...');
            await page.goto('https://x.com/compose/tweet', { waitUntil: 'networkidle2' });
            await new Promise(r => setTimeout(r, 3000));
        }

        console.log('Typing tweet content...');
        await page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
        await page.type('[data-testid="tweetTextarea_0"]', content);
        await new Promise(r => setTimeout(r, 2000));

        console.log('Clicking post button...');
        await page.waitForSelector('[data-testid="tweetButton"]', { timeout: 10000 });
        await page.click('[data-testid="tweetButton"]');
        await new Promise(r => setTimeout(r, 5000));

        // Extract the new tweet URL
        console.log('Extracting tweet URL...');
        await new Promise(r => setTimeout(r, 3000));
        
        try {
            const tweets = await page.$$('article[data-testid="tweet"]');
            console.log(`Found ${tweets.length} tweets on page`);
            
            if (tweets.length > 0) {
                const lastTweet = tweets[tweets.length - 1];
                const timeLink = await lastTweet.$('time');
                if (timeLink) {
                    const parent = await timeLink.evaluateHandle(el => el.parentElement);
                    const href = await parent.evaluate(el => el.getAttribute('href'));
                    const fullUrl = `https://x.com${href}`;
                    console.log(`New tweet URL: ${fullUrl}`);
                    return fullUrl;
                }
            }
        } catch (e) {
            console.log(`Could not extract tweet URL: ${e.message}`);
        }

        return page.url();

    } catch (error) {
        console.error('Error posting tweet:', error);
        throw error;
    } finally {
        await new Promise(r => setTimeout(r, 3000));
        await browser.close();
    }
}

async function updateQueue(postId, tweetUrl) {
    const queue = JSON.parse(fs.readFileSync(QUEUE_FILE, 'utf8'));
    const post = queue.posts.find(p => p.id === postId);
    
    if (post) {
        post.posted = true;
        post.posted_at = new Date().toISOString();
        post.tweet_url = tweetUrl;
        
        // Update metadata
        queue.metadata.updated = new Date().toISOString();
        queue.metadata.latest_tweet = tweetUrl;
        
        fs.writeFileSync(QUEUE_FILE, JSON.stringify(queue, null, 2));
        console.log(`Updated content-queue.json for post ${postId}`);
    }
}

async function updateLog(post, tweetUrl) {
    const log = JSON.parse(fs.readFileSync(LOG_FILE, 'utf8'));
    
    log.posted.push({
        id: post.id,
        content: post.content,
        platforms: post.platforms,
        tweet_url: tweetUrl,
        reply_to: post.reply_to || null,
        posted_at: new Date().toISOString(),
        note: post.note || `Morning post ${post.id}`
    });
    
    fs.writeFileSync(LOG_FILE, JSON.stringify(log, null, 2));
    console.log(`Updated posted-log.json for post ${post.id}`);
}

async function main() {
    try {
        console.log('=== Morning Post Automation ===');
        console.log(`Time: ${new Date().toLocaleString('en-US', { timeZone: 'America/New_York' })} EST`);
        
        const post = await findNextMorningPost();
        if (!post) {
            console.log('No morning posts to publish. Exiting.');
            return;
        }
        
        console.log(`\nPosting tweet ${post.id}...`);
        console.log(`Type: ${post.type}`);
        console.log(`Slot: ${post.slot}`);
        
        const tweetUrl = await postToX(post.content, post.reply_to);
        
        console.log(`\n✅ Tweet posted successfully!`);
        console.log(`URL: ${tweetUrl}`);
        
        await updateQueue(post.id, tweetUrl);
        await updateLog(post, tweetUrl);
        
        console.log('\n✅ Files updated successfully!');
        console.log('=== Automation Complete ===');
        
    } catch (error) {
        console.error('\n❌ Automation failed:', error.message);
        process.exit(1);
    }
}

main();
