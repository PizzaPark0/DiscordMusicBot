from discord.ext import commands

import random

import playerParent


class TxtReader(commands.Cog, playerParent.MusicPlayer): #txt파일에 리스트를 미리 준비해놓고 순서대로 재생(셔플가능)
    def __init__(self, bot) -> None:
        self.bot = bot
        self.nowUrl = None

        self.chn = None

        self.indx = 0
        self.urls = []
        with open('url_List.txt', 'r', encoding='utf-8') as txts:
            self.urls = txts.readlines()
            self.urls = [ i.rstrip('\n') for i in self.urls ]        

    @commands.command(name='pp')
    async def playFirst(self, ctx): #pp받으면 텍스트 순서대로 재생, 스킵과 비슷하게 작동하기도 함
        if self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
            self.bot.voice_clients[0].pause()

        self.chn = await self.enterVoiceChannel(ctx)
        self.playMusic(self.urls[self.indx], self.playQueue2)
        self.indx += 1
        if self.indx>=len(self.urls):
            self.indx = 0
    
    @commands.command(name='sf') #목록을 섞음
    async def shuffleUrls(self, ctx):
        random.shuffle(self.urls)
        await ctx.send("Shuffed!!")
    
    @commands.command(name='ind') #몇번째로 이동할지 바로 지정
    async def setIndex(self, ctx):
        self.indx = int(ctx.message.content.split(' ')[1])
        await ctx.send(f"Next Song Index is {self.indx}")

    def playQueue2(self, ctx):#음악 하나 끝나면 큐를 새로 넘겨서 다시 재생
        self.playMusic(self.urls[self.indx], self.playQueue2)
        self.indx += 1
        if self.indx>=len(self.urls):
            self.indx = 0


async def setup(bot):
    await bot.add_cog(TxtReader(bot))