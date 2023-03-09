import discord
import yt_dlp
import requests

import requirments

class MusicPlayer:
    nowResponse = None

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist':'True',
        'outtmpl': 'song.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
    ydl = yt_dlp.YoutubeDL(ydl_opts)
        
    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'}

    async def quitVoiceChannel(self):
        if self.bot.voice_clients[0]:
            await self.bot.voice_clients[0].disconnect()

    async def enterVoiceChannel(self, ctx):
        if not self.bot.voice_clients:
            await ctx.author.voice.channel.connect()
        return ctx.channel.id

    def playMusic(self, url, nextMusic=None): #유튜브 링크 사용
        if self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
            return

        info = MusicPlayer.ydl.extract_info(url, download=False)

        if self.bot.voice_clients: #음악이 끝나면 인자로 받은 함수를 이어서 실행함, 그 함수들이 음악을 바꿔 playMusic을 다시 호출함
            self.bot.voice_clients[0].play(discord.FFmpegPCMAudio(info['url'], **self.ffmpeg_opts, executable="ffmpeg/bin/ffmpeg"), after = nextMusic)
            requests.post(f"https://discord.com/api/v9/channels/{self.chn}/messages",
                      json={'content':'', "embed": { 'title': f"{info['title']}", "description": f"\n{url}"}},
                      headers={'authorization': f"Bot {requirments.Setups.token}"}
                      )
        return

    def playMusic2(self, filename, nextMusic=None): #로컬 파일 사용
        if self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
            return

        if self.bot.voice_clients: #음악이 끝나면 인자로 받은 함수를 이어서 실행함, 그 함수들이 음악을 바꿔 playMusic을 다시 호출함
            self.bot.voice_clients[0].play(discord.FFmpegPCMAudio(f'localMusicFile/{filename}', executable="ffmpeg/bin/ffmpeg.exe"), after = nextMusic)
            requests.post(f"https://discord.com/api/v9/channels/{self.chn}/messages",
                      json={'content':'', "embed": { 'title': f"{''.join(filename.split('.')[:-1])}", "description": f"LocalFile"}},
                      headers={'authorization': f"Bot {requirments.Setups.token}"}
                      )
        return