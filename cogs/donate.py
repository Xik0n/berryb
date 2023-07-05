import disnake
from disnake.ext import commands

class Donate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="донат", description="Поможем вам поддержать нас!")
    async def donate(self, inter):
        donate = disnake.ui.Button(label="Кинуть деньги в лицо Несту", style=disnake.ButtonStyle.url, url="https://www.donationalerts.com/r/nestd", emoji='<:1046539985437864007:1072938102617800774>')
        await inter.send("**<:inlove:1072938318070816878> Донатить сюда (Желательно много)**\nhttps://www.donationalerts.com/r/nestd", components=[donate])

def setup(bot):
    bot.add_cog(Donate(bot))