import disnake
from disnake.ext import commands

class Report(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="репорт", description="Жалоба на участнинка")
    @commands.cooldown(1, 300)
    async def report(inter, member: disnake.User = commands.Param(name="выберите-участника", description="упомяните его тут")):
        await inter.response.send_message(f"<@&989527990239100938>, найдено возможное нарушение правил!\n\nЖалоба на {member.mention} <:berrybot5:1089331656185364491>", 
            allowed_mentions = disnake.AllowedMentions(roles = True))

def setup(bot):
    bot.add_cog(Report(bot))