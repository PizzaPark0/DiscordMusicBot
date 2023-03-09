from discord.ext import commands

import random
import os

import playerParent


class LocalFileReader(commands.Cog, playerParent.MusicPlayer): #txt파일에 리스트를 미리 준비해놓고 순서대로 재생(셔플가능)
    def __init__(self, bot) -> None:
        self.bot = bot
        self.chn = None

        self.indx2 = 0
        self.names = list(filter(lambda x:x.split('.')[-1] in ['mp3', 'wav'], os.listdir('localMusicFile')))

    @commands.command(name='ffp')
    async def playFirst2(self, ctx): #pp받으면 텍스트 순서대로 재생, 스킵과 비슷하게 작동하기도 함
        if self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
            self.bot.voice_clients[0].pause()

        self.chn = await self.enterVoiceChannel(ctx)
        self.playMusic2(self.names[self.indx2], self.playQueue2)
        self.indx2 += 1
        if self.indx2>=len(self.names):
            self.indx2 = 0
    
    @commands.command(name='ffsf') #목록을 섞음
    async def shuffleNames(self, ctx):
        random.shuffle(self.names)
        await ctx.send("Shuffed!!")
    
    @commands.command(name='ffind') #몇번째로 이동할지 바로 지정
    async def setIndex2(self, ctx):
        self.indx = int(ctx.message.content.split(' ')[1])
        await ctx.send(f"Next Song Index is {self.indx2}")

    def playQueue2(self, ctx):#음악 하나 끝나면 큐를 새로 넘겨서 다시 재생
        self.playMusic2(self.names[self.indx2], self.playQueue2)
        self.indx2 += 1
        if self.indx2>=len(self.names):
            self.indx2 = 0


async def setup(bot):
    await bot.add_cog(LocalFileReader(bot))