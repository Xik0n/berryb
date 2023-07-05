import disnake #импорт библиотек
from disnake.ext import commands

user_ids = [986815186629455902, 768075509480292383] #заносим айди пользователей в переменную user_ids

class Feedback(commands.Cog):#создание класса Feedback
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="отзыв", description="Если ты нашел баг бота или хочешь оставить отзыв, то напиши о нем тут")#создаем слеш-команду
    @commands.cooldown(1,15)#ставим кулдаун на команду 15 секунд
    async def feedback(self, inter, bug: str = commands.Param(name="напишите-отзыв", description="Опишите баг или дайте отзыв по поводу бота как можно подробнее")):
        embed = disnake.Embed(title="Отзыв", description=f"**{inter.author.name} оставил отзыв:**\n{bug}", color=disnake.Color.orange())
        await inter.send("Спасибо за ваш отзыв <:berrybot1:1089331590431248444>", ephemeral=True)#отправялем сообщение 'спасибо за отзыв'
        for users in user_ids:#перебираем айди из переменной user_ids и заносим в users
            logs = self.bot.get_user(users)
            await logs.send(embed=embed)#отправляем логи

#подгружаем ког к боту
def setup(bot):
    bot.add_cog(Feedback(bot))