import disnake
from disnake.ext import commands
import asyncio
from time import sleep
import datetime

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):    
        if isinstance(error, disnake.ext.commands.errors.MissingPermissions):
            emb = disnake.Embed(title="Ошибка", description="У вас недостаточно прав <:MarkNo2:1055609056343113955>", color=disnake.Color.red())
            await inter.send(embed = emb, delete_after=3600, ephemeral=True)
        elif isinstance(error, disnake.ext.commands.errors.CommandOnCooldown):
            emb = disnake.Embed(title="Ошибка", description="Повторите попытку позже <:MarkNo2:1055609056343113955>", color=disnake.Color.red())
            await inter.send(embed =emb, ephemeral=True, delete_after=3600)
        elif isinstance(error, disnake.ext.commands.errors.MissingAnyRole):
            emb = disnake.Embed(title="Ошибка", description="У вас недостаточно прав <:MarkNo2:1055609056343113955>", color=disnake.Color.red())
            await inter.send(embed = emb, delete_after=3600, ephemeral=True)
        elif isinstance(error, disnake.ext.commands.errors.MissingRole):
            emb = disnake.Embed(title="Ошибка", description="У вас недостаточно прав <:MarkNo2:1055609056343113955>", color=disnake.Color.red())
            await inter.send(embed = emb, delete_after=3600, ephemeral=True)
        else:
            embed = disnake.Embed(title='Ошибка Бота',description=f'```py\n{error}\n```', color=0xff0000)
            embed.timestamp=datetime.datetime.now()
            embed.set_thumbnail(url='https://i.imgur.com/FBmMzb5.png')
            channel = self.bot.get_channel(1119005714933891153)
            await channel.send(embed=embed)

@commands.Cog.listener()
async def on_member_join(self, member):
        try:
            await member.send(f"Хай, {member.name}\n**Я Ягодка - твоя персональная помощница.**\n**Ты всегда сможешь найти меня тут! -** https://discord.gg/baaeQRRxbr\n\n**<:interesting:1072938409158512750>**" )
        except:
            pass
        emb1 = disnake.Embed(title="Вход", description=f"<:1046539988608757800:1072938433867165798> На сервер `{member.guild.name}` зашел(-а) \n{member}", color=0xffe600)
        emb1.set_thumbnail(url=member.display_avatar.url)
        channel =  self.bot.get_channel(1084894848680726578)
        await channel.send(embed=emb1)
        
@commands.Cog.listener()
async def on_guild_channel_create(self, channel):
        if isinstance(channel, disnake.VoiceChannel): # проверяем, является ли канал голосовым
            emb1 = disnake.Embed(title="Комната создана", description=f"<:1046539988608757800:1072938433867165798> Имя канала: {channel.name}", color=0xb1ff00)
            emb1.set_thumbnail(url="https://media.discordapp.net/attachments/992105125453775003/1053477465248497787/docsSection-a2860.png")
            channel = self.bot.get_channel(989528055657664622)
            await channel.send(embed=emb1)

def setup(bot):
    bot.add_cog(Events(bot))