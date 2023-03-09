import requests
import re

from discord.ext import commands

import playerParent


class Croller(commands.Cog, playerParent.MusicPlayer): #추천 영상 받아서 가장 첫번째 재생
    def __init__(self, bot) -> None:
        self.bot = bot
        self.nowResponse = None
        self.nowUrl = None

        self.chn = None

    @commands.command(name='p')
    async def playInstant(self, ctx): #p+링크 받으면 그 음악 일단 재생
        if self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
            self.bot.voice_clients[0].pause()
        
        self.nowUrl = ctx.message.content.split(' ')[1]
        self.sendUrl(self.nowUrl)

        self.chn = await self.enterVoiceChannel(ctx)
        self.playMusic(self.nowUrl, self.playQueue)
    
    @commands.command(name='s') #s누르면 다음으로 넘어감
    async def passMusic(self, ctx):
        '''다른 클래스와 명령어를 공유하지는 않으나,
            stop만 하면 나머지는 각자가 알아서 하기 때문에 다른 클래스의 스킵에도 사용할 수 있다.'''
        if self.bot.voice_clients and self.bot.voice_clients[0].is_playing():
            self.bot.voice_clients[0].stop()

    @commands.command(name='q') #q누르면 퇴장
    async def quit(self, ctx):
        '''다른 클래스와 명령어를 공유하지는 않으나,
            stop만 하면 나머지는 각자가 알아서 하기 때문에 다른 클래스의 종료에도 사용할 수 있다.'''
        await self.quitVoiceChannel()

    def playQueue(self, ctx):#음악 하나 끝나면 새 링크 받아서 다시 재생
        url = self.getRecommandedUrl(self.nowResponse)
        self.sendUrl(url)
        self.playMusic(self.nowUrl, self.playQueue)

    def sendUrl(self, url): #입력받은 url 유튜브에 쏴서 response 반환
        self.nowResponse = requests.get(url=url).content.decode()

    def getRecommandedUrl(self, res): #현재 받은 response에서 추천 영상들 링크 찾아 반환
        temp = re.findall('/watch\?v=[a-zA-Z0-9-_]{1,}',res)
        boolTarget = self.nowUrl.split('=')[1]
        temp = list(set(list(filter(lambda x: x.split('=')[1] != boolTarget, temp))))
        self.nowUrl = 'https://www.youtube.com/' + temp[0]
        return self.nowUrl
    

async def setup(bot):
    await bot.add_cog(Croller(bot))
