# Pinot's Clip Program

This program will help you create a bot that will listen for a !clip command and will run a native clip button on your stream PC

### Instructions 
1) Download latest [`PinotsClipScript.zip`](https://github.com/chukwumaokere/TwitchClipScript/releases/latest)
2) Unzip it to its own folder i.e., `PinotsClipScript/`
3) Run `PinotsClipScript.exe`
4) Get twitch tmi auth code 
5) Fill out info
6) Press Start/Restart :)

If it stops working or something crashes, press Start/Restart or re-run the program

### Dev Requirements
1) Python 3.6+
2) Pip installer (This comes standard with Python 3.4+)
3) `pynput` (Run: `pip install pynput` in cmd) 
[Image reference](https://i.gyazo.com/4d4a9d36df373192567c0bd69d862248.png)

### TODO
- Add a function to autorestart if something fails
- Add deeomjify python package to rpevent crashing on emoji chat
- Ignore most chat logs so the log doesnt get filled
- Add input box for command to track so users arent stuck with !clip
- Add timestamp to logging.
- Package as an .exe