import disnake
from disnake.ext import commands

user_ids = [986815186629455902, 768075509480292383]

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="очистить", description="Удалить сообщения")
    @commands.has_any_role(989929544704196618, 989527988959842345)
    @commands.cooldown(1,60)
    async def purge(self, inter, amount: int = commands.Param(name="количество", description="Выберите количество")):
        if amount > 100:
            emb = disnake.Embed(title="Ошибка", description=f"Вы можете удалить только до 5 сообщений <:MarkNo2:1055609056343113955>", color=disnake.Color.red())
            await inter.send(embed=emb, ephemeral=True)
        else:
            embed = disnake.Embed(title="Очистка сообщений <:1046539991666405418:1072938090647277698>", description=f"Очищено {amount} сообщений", color=0x49656b)
            emb =  disnake.Embed(title="Очистка <:1046539991666405418:1072938090647277698>", description=f"Участник `{inter.author.name}`\nочистил: {amount} сообщений", color=0x49656b)
            nest = self.bot.get_user(986815186629455902)
            xikon = self.bot.get_user(768075509480292383)
            await inter.channel.purge(limit = amount)
            await inter.send(embed = embed, delete_after=20)
            await xikon.send(embed = emb)
            await nest.send(embed=emb)

def setup(bot):
    bot.add_cog(Purge(bot))
