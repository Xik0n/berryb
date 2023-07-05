import disnake
from disnake.ext import commands
import random

list_of_random_words=["да", "нет", "точно да", "точно нет", "вероятно"]

class Random(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
          
    @commands.slash_command(name='рандом', description='бот ответит на любой ваш вопрос')
    async def rand(self, inter, text: str=commands.Param(name="вопрос", description='задайте вопрос чтобы бот на него мог ответить Да/Нет')):
        randansw = random.choice(list_of_random_words) 
        embed = disnake.Embed(description=f'**{inter.author.name} спросил:** `{text}`', color=0xffffff)
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embedbot = disnake.Embed(description=f'**Ответ:** `{randansw}`', color=0xffe600)
        embedbot.set_thumbnail(url="https://media.discordapp.net/attachments/992105125453775003/1089336374097891338/berrybot3.png")
        embs = [embed, embedbot]
        await inter.send(embeds=embs)
    
    @commands.slash_command(name='монетка', description='Подбросить монетку')
    async def mon(self, inter):
        list = ['орел', 'решка']
        rand = random.choice(list)
        if rand == 'орел':
            await inter.send(embed=disnake.Embed(title='Выпал орёл!', color=0xffffff))
        if rand == 'решка':
            await inter.send(embed=disnake.Embed(title='Выпала решка!', color=0xffffff))

def setup(bot):
    bot.add_cog(Random(bot))
