# Zuggs DiscordVLCBot

Features
- Discord commands allow users to control vlc remotely utilizing the VLC web interface running locally on a machine.
- Integrates with a simple to configure DiscordBot that you setup to fit your Discord Server. This portion is all on the user to configure.
- Allows users to control both audio and video playback.
- Supports M3U and XSPF playlist types.
- Ability to Play, Pause, Stop and Skip content with simple commands.
- Enable or Disable Playlist Shuffling
- Command to output the currently playing track name.
- Ability to report broken tracks that prompt the user for a reason, saving these files to a text file for administrative review.

**Commands**
- !play - Start Playback
- !Pause - Pause Playback
- !Stop - Stop Playback
- !Next - Skips the current content
- !enable_shuffle - Enables the random shuffle
- !disable_shuffle - Disables the random shuffle
- !playlist - View Playlists
- !current - Lists the currently playing video/episode
- !broken - Reports a broken file then prompts user to enter a reason. This will save the reported files to a text document in the same directory as your bot files.
- !select [Playlist ID] - **BROKEN** Need to work on fixing the issues here

**Host Machine Requirements**
- Make sure you have discord.py and requests installed. You can install them using pip.
- Python - python.org
- VLC Must be installed on the host machine and the web interface must be enabled with a password.
- Discord Client

**VLC Requirements**
1. Enable VLC Web Interface
2. Open VLC media player.
3. Go to Tools > Preferences.
4. In the bottom left corner, click All to show all settings.
5. Under Interface, select Main interfaces.
6. Check the box for Web.
7. Under Main interfaces, click on Lua.
8. Set a password in the Password field.
9.. Restart VLC.

**Playlist Requirements**
- Create a local JSON file (e.g., playlists.json) that contains the list of playlists.
- Update the bot script to read from this JSON file and provide commands to list and select playlists.
- Included is a sample playlist you can reference for your own. In the near future I will fix the playlist selection capabilities.
