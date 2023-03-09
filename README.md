# DiscordMusicBot

1. Requirement
- pip install discord.py
- pip install yt_dlp
- must include ffempeg.exe
- Write token at requirements.py
- It can only play music on youtube
- It is made for one's own use, commands from multiple channel or user can make error.

2. Commands (Any prefix required)
- p https://www.youtube.com/_______
   : Play instantly music. After end of music, bot gets a related music url and play.
     Repeat until the user exits. This command can cancel the original order.
- pp
   : Play instantly music that are written on url_List.txt. After end of music, bot gets a next index and play.
   Repeat until the user exits. If bot play all musics in list, index will return to 0. This command can cancel the original order.
- ffpp
   : Play instantly music that are in LocalMusicFile folder. After end of music, bot gets a next music and play.
   Repeat until the user exits. If bot play all musics in list, index will return to 0. This command can cancel the original order.
- sf
   : It is valid when bot is executing 'pp' command. Shuffle list of text file's url.
- ffsf
   : It is valid when bot is executing 'ffpp' command. Shuffle list of music files.
- ind
   : It is valid when bot is executing 'pp' command. Set index, apply to the following music.
- ffind
   : It is valid when bot is executing 'ffpp' command. Set index, apply to the following music.
- s
   : Instantly end the music, end get next music.
- q
   : Disconnect bot from voice channel.
