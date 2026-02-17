#!/usr/bin/env python3
"""
Enhanced Discord Helper for Content Factory
Supports text, images, embeds, and file attachments
"""

import requests
import json
import os
from pathlib import Path
from typing import Optional, Dict, List

# Load channel mapping
CHANNELS_FILE = Path.home() / '.openclaw/workspace/.discord-channels.json'
with open(CHANNELS_FILE, 'r') as f:
    DISCORD_CONFIG = json.load(f)

# Load bot token
TOKEN_FILE = Path.home() / '.openclaw/workspace/.discord-bot-token'
with open(TOKEN_FILE, 'r') as f:
    BOT_TOKEN = f.read().strip()

CHANNELS = DISCORD_CONFIG['channels']
GUILD_ID = DISCORD_CONFIG['guild_id']


def post_message(channel_name: str, content: str = None, embed: Dict = None, 
                 file_path: str = None) -> Optional[Dict]:
    """
    Post message to Discord channel with optional embed or file attachment.
    
    Args:
        channel_name: Name of the channel (e.g., 'trending-stories')
        content: Text message content
        embed: Discord embed object
        file_path: Path to file to attach (image, etc.)
    
    Returns:
        Response JSON with message ID or None on failure
    """
    if channel_name not in CHANNELS:
        print(f"❌ Unknown channel: {channel_name}")
        return None
    
    channel_id = CHANNELS[channel_name]
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}"
    }
    
    # Build payload
    payload = {}
    if content:
        payload['content'] = content
    if embed:
        payload['embeds'] = [embed]
    
    # Handle file uploads
    if file_path and os.path.exists(file_path):
        files = {
            'file': (os.path.basename(file_path), open(file_path, 'rb'))
        }
        # Send payload as form data when uploading files
        data = {'payload_json': json.dumps(payload)}
        response = requests.post(url, headers=headers, data=data, files=files)
        files['file'][1].close()
    else:
        headers['Content-Type'] = 'application/json'
        response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        msg_data = response.json()
        msg_id = msg_data['id']
        print(f"✅ Posted to #{channel_name} (ID: {msg_id})")
        return msg_data
    else:
        print(f"❌ Failed to post to #{channel_name}: {response.status_code}")
        print(f"   {response.text}")
        return None


def fetch_recent_messages(channel_name: str, limit: int = 10) -> List[Dict]:
    """
    Fetch recent messages from a Discord channel.
    
    Args:
        channel_name: Name of the channel
        limit: Number of recent messages to fetch (max 100)
    
    Returns:
        List of message objects
    """
    if channel_name not in CHANNELS:
        print(f"❌ Unknown channel: {channel_name}")
        return []
    
    channel_id = CHANNELS[channel_name]
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages?limit={min(limit, 100)}"
    
    headers = {
        "Authorization": f"Bot {BOT_TOKEN}"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        messages = response.json()
        print(f"✅ Fetched {len(messages)} messages from #{channel_name}")
        return messages
    else:
        print(f"❌ Failed to fetch from #{channel_name}: {response.status_code}")
        return []


def create_embed(title: str, description: str = None, color: int = 0x5865F2,
                 fields: List[Dict] = None, thumbnail_url: str = None,
                 image_url: str = None, footer: str = None) -> Dict:
    """
    Create a Discord embed object.
    
    Args:
        title: Embed title
        description: Embed description
        color: Color as integer (default: Discord blurple)
        fields: List of field dicts with 'name', 'value', optional 'inline'
        thumbnail_url: URL for thumbnail image
        image_url: URL for main image
        footer: Footer text
    
    Returns:
        Discord embed dict
    """
    embed = {
        "title": title,
        "color": color
    }
    
    if description:
        embed['description'] = description
    if fields:
        embed['fields'] = fields
    if thumbnail_url:
        embed['thumbnail'] = {"url": thumbnail_url}
    if image_url:
        embed['image'] = {"url": image_url}
    if footer:
        embed['footer'] = {"text": footer}
    
    return embed


# Convenience functions for Content Factory channels
def post_trending_story(content: str, embed: Dict = None) -> Optional[Dict]:
    """Post to #trending-stories"""
    return post_message('trending-stories', content, embed)


def post_script(content: str, embed: Dict = None) -> Optional[Dict]:
    """Post to #scripts"""
    return post_message('scripts', content, embed)


def post_thumbnail(content: str, file_path: str = None, embed: Dict = None) -> Optional[Dict]:
    """Post to #thumbnails"""
    return post_message('thumbnails', content, embed, file_path)


def post_ready_to_publish(content: str, embed: Dict = None) -> Optional[Dict]:
    """Post to #ready-to-publish"""
    return post_message('ready-to-publish', content, embed)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: discord_helper.py <channel> <message>")
        print(f"Channels: {', '.join(CHANNELS.keys())}")
        sys.exit(1)
    
    channel = sys.argv[1]
    message = ' '.join(sys.argv[2:])
    post_message(channel, message)
