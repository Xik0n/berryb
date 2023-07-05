import disnake
from disnake.ext import commands
import random
required_roles = [1061266758180286514, 989963292065812500, 989527988959842345, 989929544704196618]

class buster(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name='бустерам', description='для бустеров')
    @commands.has_any_role(989929544704196618, 989527988959842345, 1061266758180286514)
    async def buster(self, inter):
        embed = disnake.Embed(title='⚡ Функции только для бустеров:', description='**</привет:1117123991203762269>** - отправляет случайную гифку с приветствием.\n**</пока:1117135196177842278>** - отправляет случайную гифку с прощанием.\n**</поцеловать:1117135196177842279>** - отправляет случайную гифку с поцелуем.\n**</обнять:1117135196177842280>** - отправляет случайную гифку с обниманием.', color=0x8000FF)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1117147459550982184/Frame_715.png?width=621&height=621')
        await inter.send('Готово', ephemeral=True)
        await inter.channel.send(embed=embed)

    @commands.slash_command(name='привет', description='отправить гифку')
    async def hello(self, inter, user: disnake.Member = commands.Param(None, name='участник', description='укажите пользователя')):
        server = self.bot.get_guild(992105124900130816)
        channel = server.get_channel(1117120251407106068)
        messages = await channel.history(limit=None).flatten()
        random_message = random.choice(messages)
        author_roles = [role.id for role in inter.author.roles]
        if any(role in author_roles for role in required_roles):
            if random_message.content.endswith('.gif'):
                if user is None:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} поприветствовал чатик').set_image(url=random_message.content))
                else:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} поприветствовал {user.mention}').set_image(url=random_message.content))
        else:
            await inter.send('Извините, Вы не давали буст этому серверу. Но... еще не поздно!', ephemeral=True)


    @commands.slash_command(name='пока', description='отправить гифку')
    async def bye(self, inter, user: disnake.Member = commands.Param(None, name='участник', description='укажите пользователя')):
        server = self.bot.get_guild(992105124900130816)
        channel = server.get_channel(1117120269610393761)
        messages = await channel.history(limit=None).flatten()
        random_message = random.choice(messages)
        author_roles = [role.id for role in inter.author.roles]
        if any(role in author_roles for role in required_roles):
            if random_message.content.endswith('.gif'):
                if user is None:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} попрощался с чатиком').set_image(url=random_message.content))
                else:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} попрощался с {user.mention}').set_image(url=random_message.content))
        else:
            await inter.send('Извините, Вы не давали буст этому серверу. Но... еще не поздно!', ephemeral=True)

    @commands.slash_command(name='поцеловать', description='отправить гифку')
    async def kiss(self, inter, user: disnake.Member = commands.Param(None, name='участник', description='укажите пользователя')):
        server = self.bot.get_guild(992105124900130816)
        channel = server.get_channel(1117120303294849105)
        messages = await channel.history(limit=None).flatten()
        random_message = random.choice(messages)
        author_roles = [role.id for role in inter.author.roles]
        if any(role in author_roles for role in required_roles):
            if random_message.content.endswith('.gif'):
                if user is None:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} поцеловал чатик').set_image(url=random_message.content))
                else:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} поцеловал {user.mention}').set_image(url=random_message.content))
        else:
            await inter.send('Извините, Вы не давали буст этому серверу. Но... еще не поздно!', ephemeral=True)

    @commands.slash_command(name='обнять', description='отправить гифку')
    async def hug(self, inter, user: disnake.Member = commands.Param(None, name='участник', description='укажите пользователя')):
        server = self.bot.get_guild(992105124900130816)
        channel = server.get_channel(1117120326334165092)
        messages = await channel.history(limit=None).flatten()
        random_message = random.choice(messages)
        author_roles = [role.id for role in inter.author.roles]
        if any(role in author_roles for role in required_roles):
            if random_message.content.endswith('.gif'):
                if user is None:
                    await inter.channel.send(description=f'{inter.author.mention} обнял чатик').set_image(url=random_message.content)
                else:
                    await inter.send(embed=disnake.Embed(description=f'{inter.author.mention} обнял {user.mention}').set_image(url=random_message.content))
                
        else:
            await inter.send('Извините, Вы не давали буст этому серверу. Но... еще не поздно!', ephemeral=True)
            
def setup(bot):
    bot.add_cog(buster(bot))