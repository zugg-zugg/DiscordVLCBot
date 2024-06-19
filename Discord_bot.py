import discord
import requests
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot

# VLC web interface credentials
VLC_IP = '127.0.0.1'
VLC_PORT = '8080'
VLC_PASSWORD = 'your_password'

# Discord bot token
DISCORD_TOKEN = 'your_discord_bot_token'

# Base URL for VLC web interface
BASE_URL = f'http://{VLC_IP}:{VLC_PORT}'

# Basic authentication
auth = ('', VLC_PASSWORD)

# Define the necessary intents
intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

# Create bot instance with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

def send_vlc_command(command):
    """Send command to VLC web interface."""
    try:
        url = f"{BASE_URL}/requests/status.json?command={command}"
        response = requests.get(url, auth=auth)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error sending command to VLC: {e}")
        return None

def get_vlc_status():
    """Get the current status from VLC."""
    try:
        url = f"{BASE_URL}/requests/status.json"
        response = requests.get(url, auth=auth)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error getting VLC status: {e}")
        return None

def load_playlists():
    """Load playlists from the local JSON file."""
    try:
        with open('playlists.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading playlists: {e}")
        return None

def play_playlist(file_path):
    """Play the specified playlist file."""
    command = f"in_play&input=file:///{file_path.replace('\\', '/')}"
    return send_vlc_command(command) is not None

def set_shuffle(state):
    """Set shuffle state."""
    command = 'pl_random'
    send_vlc_command(command)
    return send_vlc_command(f"pl_random&val={'1' if state else '0'}")

def get_random_response(responses):
    """Return a random response from a list of responses."""
    return random.choice(responses)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command()
async def play(ctx):
    responses = ['Playback started.', 'Playing now!', 'Let the music begin!']
    if send_vlc_command('pl_play'):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to start playback.')

@bot.command()
async def pause(ctx):
    responses = ['Playback paused.', 'Music on hold.', 'Paused!']
    if send_vlc_command('pl_pause'):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to pause playback.')

@bot.command()
async def stop(ctx):
    responses = ['Playback stopped.', 'Music stopped.', 'Stopped playing!']
    if send_vlc_command('pl_stop'):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to stop playback.')

@bot.command()
async def next(ctx):
    responses = ['Skipped to next track.', 'Next song coming up!', 'Moving to the next track!']
    if send_vlc_command('pl_next'):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to skip to next track.')

@bot.command()
async def previous(ctx):
    responses = ['Playing previous track.', 'Going back to the last song.', 'Rewinding to the previous track.']
    if send_vlc_command('pl_previous'):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to play previous track.')

@bot.command()
async def playlists(ctx):
    playlists = load_playlists()
    if playlists:
        playlist_message = "Available Playlists:\n"
        for playlist in playlists['playlists']:
            playlist_message += f"{playlist['id']}: {playlist['name']} - {playlist['description']}\n"
        await ctx.send(playlist_message)
    else:
        await ctx.send('Failed to load playlists.')

@bot.command()
async def select(ctx, playlist_id: int):
    playlists = load_playlists()
    if playlists:
        selected_playlist = next((p for p in playlists['playlists'] if p['id'] == playlist_id), None)
        if selected_playlist:
            if play_playlist(selected_playlist['file']):
                await ctx.send(f'Playlist "{selected_playlist["name"]}" selected and playing.')
            else:
                await ctx.send(f'Failed to select playlist "{selected_playlist["name"]}".')
        else:
            await ctx.send(f'Playlist ID {playlist_id} not found.')
    else:
        await ctx.send('Failed to load playlists.')

@bot.command()
async def disable_shuffle(ctx):
    responses = ['Shuffle disabled.', 'No more shuffling.', 'Shuffle mode turned off.']
    if set_shuffle(False):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to disable shuffle.')

@bot.command()
async def enable_shuffle(ctx):
    responses = ['Shuffle enabled.', 'Shuffle mode is on!', 'Shuffling the playlist now.']
    if set_shuffle(True):
        await ctx.send(get_random_response(responses))
    else:
        await ctx.send('Failed to enable shuffle.')

@bot.command()
async def current(ctx):
    status = get_vlc_status()
    if status and 'information' in status and 'category' in status['information']:
        meta = status['information']['category'].get('meta', {})
        filename = meta.get('filename', 'Unknown')
        await ctx.send(f'Currently playing: {filename}')
    else:
        await ctx.send('Failed to retrieve the current track.')

@bot.command()
async def broken(ctx):
    status = get_vlc_status()
    if status and 'information' in status and 'category' in status['information']:
        meta = status['information']['category'].get('meta', {})
        filename = meta.get('filename', 'Unknown')
        await ctx.send(f'Reporting broken file: {filename}. Please enter the reason:')
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        try:
            reason = await bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            await ctx.send('You took too long to respond. Please try again.')
            return
        
        with open('broken_files.txt', 'a') as f:
            f.write(f'File: {filename}, Reason: {reason.content}\n')
        
        await ctx.send(f'Reported broken file: {filename} with reason: {reason.content}')
    else:
        await ctx.send('Failed to retrieve the current track.')

# Handle invalid commands with random responses
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        responses = [
            "Oops, I don't recognize that command.",
            "Sorry, that's not a valid command.",
            "I didn't understand that. Try another command.",
            "That command doesn't exist. Please try again."
        ]
        await ctx.send(get_random_response(responses))
    else:
        raise error

# Run the bot
bot.run(DISCORD_TOKEN)
