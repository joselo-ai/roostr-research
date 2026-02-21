tell application "Google Chrome"
	activate
	set tweetURL to "https://x.com/roostrcapital/status/2024484515012628951"
	open location tweetURL
	delay 3
	
	-- Tweet content
	set tweetContent to "Why social arbitrage works:

Chris Camillo's Dorel Industries play (2020):

• March: COVID lockdowns begin
• Social media: Parents panic-buying bikes for kids
• Dorel: Major bike manufacturer
• Entry: $3.50
• Exit: $22
• Return: 629%

Wall Street saw it 3 months later.

Edge = speed of information."
	
	-- Instructions for manual posting
	display dialog "Ready to post tweet. 

Content:
" & tweetContent & "

Steps:
1. Click Reply button on the tweet
2. Paste the content (Cmd+V)
3. Click Post
4. Copy the new tweet URL

Press OK when ready." buttons {"OK"} default button "OK"
	
	-- Copy tweet content to clipboard
	set the clipboard to tweetContent
	
end tell
