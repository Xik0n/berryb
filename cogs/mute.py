import disnake
from disnake.ext import commands
from datetime import timedelta

def format_duration(total_seconds):
    days, remainder = divmod(total_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    duration_str = ""
    if days > 0:
        duration_str += f"{days}д "
    if hours > 0:
        duration_str += f"{hours}ч "
    if minutes > 0:
        duration_str += f"{minutes}м "
    if seconds > 0:
        duration_str += f"{seconds}с "
    return duration_str.strip()

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='мьют', description='Отправить участника подумать о своём поведении.')
    @commands.has_any_role(989527981565304872, 989929544704196618, 989527990239100938)
    @commands.cooldown(1, 30)
    async def mute(self, inter, 
                member: disnake.Member = commands.Param(name='участник', description='выберите участника'),
                duration: str = commands.Param(None, name='время', description='Время мута (Пример: 10м 1ч 5с 9д, если не указано то мут бессрочен)'),
                reason: str = commands.Param(None, name='причина', description='причина мута', min_length=5, max_length=250)):
        if member == inter.author:
            return await inter.send("Вы не можете замутить себя.", ephemeral=True)
        if member.current_timeout is not None:
            return await inter.send("Вы не можете замутить участника так как он уже в муте", ephemeral=True)
        if member.top_role >= inter.author.top_role:
            return await inter.send("Вы не можете замутить того у кого есть роль равная вашей или выше вашей.", ephemeral=True)
        if member.bot:
            return await inter.send("Вы не можете замутить Бота.", ephemeral=True)
        time_args = duration.split()
        duration_dict = {'с': 1, 'м': 60, 'ч': 3600, 'д': 86400}
        total_seconds = 0
        for arg in time_args:
            time_num = int(arg[:-1])
            time_unit = arg[-1]
            total_seconds += time_num * duration_dict[time_unit]
        duration_str = format_duration(total_seconds)
        embed=disnake.Embed(description=f'**<:1046540000344408115:1072938130199552030> Участник {member.mention} был замучен!**', color=0x9DFF00)
        embed.add_field(name='**Замутил:**', value=f'{inter.author.mention}', inline=True)
        embed.add_field(name='**Длительность:**', value=f'**{duration_str}**', inline=True)
        embed.add_field(name='**Причина:**', value=f'{reason}' if reason else '**Не указана**', inline=False)
        await inter.response.defer()
        await member.timeout(duration=total_seconds, reason=reason)
        await inter.send(embed=embed, delete_after=30)
        channel =  self.bot.get_channel(1084894848680726578)
        await channel.send(embed=embed)

    @commands.slash_command(name='размьют', description='Снять наказание с участника')
    @commands.has_any_role(989527981565304872, 989929544704196618, 989527990239100938)
    @commands.cooldown(1, 30)
    async def unmute(self, inter, 
                     member: disnake.Member = commands.Param(name='участник', description='укажите участника'),
                     reason: str = commands.Param(None, name='причина', description='укажи причину размута', min_length=5, max_length=250)):
        if member == inter.author:
            return await inter.send("Вы не можете замутить себя.", ephemeral=True)
        if member.current_timeout is None:
            return await inter.send("Вы не можете замутить участника т.к. он не в муте", ephemeral=True)
        if member.top_role >= inter.author.top_role:
            return await inter.send("Вы не можете замутить того у кого есть роль равная вашей или выше вашей.", ephemeral=True)
        if member.bot:
            return await inter.send("Вы не можете замутить Бота.", ephemeral=True)
        embed = disnake.Embed(description=f"**<:1046540000344408115:1072938130199552030> Участник {member.mention} был размучен**", color=0x9DFF00)
        embed.add_field(name='**Размутил:**', value=f'{inter.author.mention}', inline=True)
        embed.add_field(name='**Причина:**', value=f'{reason}' if reason else '**Не указана**', inline=True)
        await inter.response.defer()
        await member.edit(timeout=None)
        await inter.send(embed=embed, delete_after=30)
        channel =  self.bot.get_channel(1084894848680726578)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Mute(bot))