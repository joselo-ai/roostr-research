-- AppleScript to post tweet reply
delay 2

tell application "System Events"
	-- Click reply button (using keyboard shortcut if available)
	keystroke "r" -- X shortcut for reply
	delay 2
	
	-- Paste the tweet content
	set the clipboard to "Why social arbitrage works:

Chris Camillo's Dorel Industries play (2020):

• March: COVID lockdowns begin
• Social media: Parents panic-buying bikes for kids
• Dorel: Major bike manufacturer
• Entry: $3.50
• Exit: $22
• Return: 629%

Wall Street saw it 3 months later.

Edge = speed of information."
	
	keystroke "v" using command down
	delay 2
	
	-- Post tweet (Cmd+Return on X)
	keystroke return using command down
	delay 3
end tell
