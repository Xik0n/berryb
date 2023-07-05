import disnake
from disnake.ext import commands
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://xikon:joker12340000@cluster0.bvfeu4r.mongodb.net/?retryWrites=true&w=majority")
productDB = cluster['product']
DBtype = productDB['hands']
DBproduct = productDB['product']
DBprice = productDB['price']

serverDB = cluster['server']
dbcode = productDB['code']
active_threads= serverDB['threads']
synced_threads = serverDB['synced_threads']
servers = serverDB['servers']

qiwiDB = cluster['qiwi']
qiwi_base = qiwiDB['qiwi']

paintersDB = cluster['painters']
stars = paintersDB['rating']
orders = paintersDB['orders']
painter = paintersDB['paintersinfo']

class Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.persistent_views_added = False
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.persistent_views_added:
            self.persistent_views_added = True
        print(f"Бот {self.bot.user} запущен")

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == 'reload':
            await inter.message.delete()
            await inter.response.defer()
            total_members = 0
            for guild in self.bot.guilds:
                total_members += guild.member_count
            zakazov_all = servers.find_one({"_id": "count"})['zakaz']
            morwyy = self.bot.get_user(609737656363909151)
            essciz = self.bot.get_user(937410314100703243)
            mourt1n = self.bot.get_user(870550116887564348)
            gulava = self.bot.get_user(987793657723752468)
            kiborgtv = self.bot.get_user(617052770293252109)
            p1oko = self.bot.get_user(728648509334487102)
            nest = self.bot.get_user(986815186629455902)
            p1 = painter.find_one({"_id": 609737656363909151})
            p2 = painter.find_one({"_id": 937410314100703243})
            p3 = painter.find_one({"_id": 870550116887564348})
            p4 = painter.find_one({"_id": 987793657723752468})
            p5 = painter.find_one({"_id": 617052770293252109})
            p6 = painter.find_one({"_id": 728648509334487102})
            p7 = painter.find_one({"_id": 986815186629455902})

            threads_doc = active_threads.find_one({"_id": "count"})
            if threads_doc is not None:
                threads = str(threads_doc['threads'])
            else:
                threads = 0
            stars_doc1 = stars.find_one({"_id": int(609737656363909151)})
            stars_doc2 = stars.find_one({"_id": int(937410314100703243)})
            stars_doc3 = stars.find_one({"_id": int(870550116887564348)})
            stars_doc4 = stars.find_one({"_id": int(987793657723752468)})
            stars_doc5 = stars.find_one({"_id": int(617052770293252109)})
            stars_doc6 = stars.find_one({"_id": int(728648509334487102)})
            stars_doc7 = stars.find_one({"_id": int(986815186629455902)})

            if stars_doc1 is not None:
                rating_find1 = stars_doc1['rating']
            else:
                stars.insert_one({"_id": int(609737656363909151), "marks": [5], "rating": 5})
            
            if stars_doc2 is not None:
                rating_find2 = stars_doc2['rating']
            else:
                stars.insert_one({"_id": int(937410314100703243), "marks": [5], "rating": 5})
            
            if stars_doc3 is not None:
                rating_find3 = stars_doc3['rating']
            else:
                stars.insert_one({"_id": int(870550116887564348), "marks": [5], "rating": 5})
            if stars_doc4 is not None:
                rating_find4 = stars_doc4['rating']
            else:
                stars.insert_one({"_id": int(987793657723752468), "marks": [5], "rating": 5})
            if stars_doc5 is not None:
                rating_find5 = stars_doc5['rating']
            else:
                stars.insert_one({"_id": int(617052770293252109), "marks": [5], "rating": 5})
            if stars_doc6 is not None:
                rating_find6 = stars_doc6['rating']
            else:
                stars.insert_one({"_id": int(728648509334487102), "marks": [5], "rating": 5})
            if stars_doc7 is not None:
                rating_find7 = stars_doc7['rating']
            else:
                stars.insert_one({"_id": int(986815186629455902), "marks": [5], "rating": 5})

            await inter.send(embed=disnake.Embed(title='Статистика использования бота:', description=f'Сервера: `{len(self.bot.guilds)}`\nПользователи: `{total_members}`\nПинг: `{round(self.bot.latency*1000)}мс ({round(self.bot.latency*10)} сек)`\n\n**Статистика Skins:**\nЗаказов: `{zakazov_all}`\nАктивных заказов: `{threads}`').add_field(name='Статистика художников:', value=f"{morwyy.mention}⠀`{int(rating_find1)}⭐`⠀`{p1['getprice']} RUB`⠀`({p1['zakazs']} заказов)`\n{essciz.mention}⠀`{int(rating_find2)}⭐`⠀`{p2['getprice']} RUB`⠀`({p2['zakazs']} заказов)`\n{mourt1n.mention}⠀`{rating_find3}⭐`⠀`{p3['getprice']} RUB`⠀`({p3['zakazs']} заказов)`\n{gulava.mention}⠀`{rating_find4}⭐`⠀`{p4['getprice']} RUB`⠀`({p4['zakazs']} заказов)`\n{kiborgtv.mention}⠀`{rating_find5}⭐`⠀`{p5['getprice']} RUB`⠀`({p5['zakazs']} заказов)`\n{p1oko.mention}⠀`{rating_find6}⭐`⠀`{p6['getprice']} RUB`⠀`({p6['zakazs']} заказов)`\n{nest.mention}⠀`{rating_find7}⭐`⠀`{p7['getprice']} RUB`⠀`({p7['zakazs']} заказов)`", inline=False).set_thumbnail(url='https://media.discordapp.net/attachments/991705191978115132/1125071609661759560/1072938433867165798.png?width=120&height=120'), ephemeral=True, components=[disnake.ui.Button(label='Обновить', custom_id='reload')])

        if inter.component.custom_id == 'zakazss':
            orders_doc = orders.find_one({"_id": inter.author.id})
            if orders_doc is not None:
                order_list = orders_doc['orders']
                formatted_orders = '\n'.join(order_list)
                orders_user = f'{formatted_orders}'
                await inter.send(orders_user, ephemeral=True)
            else:
                await inter.send('Все заказы выполнены!\n🧺 Ожидайте новые.', ephemeral=True)

        if inter.component.custom_id == 'balance':
            price_doc = painter.find_one({"_id": inter.author.id})
            if price_doc is not None:
                price_find = price_doc['getprice']
                await inter.send(f'Ваш баланс 🏷️: {str(price_find)} RUB', ephemeral=True)
            else:
                await inter.send(f'Ваш баланс 🏷️: 0 RUB', ephemeral=True) 
        
        if inter.component.custom_id == 'rating':
            stars_doc = stars.find_one({"_id": inter.author.id})
            if stars_doc is not None:
                rating_find = stars_doc['rating']
                await inter.send(f'Ваш рейтинг 📈: {str(rating_find)}', ephemeral=True)
            else:
                await inter.send(f'Ваш рейтинг 📈: 5.0', ephemeral=True)

    @commands.slash_command(name='включение-навигации', description='включение навигации с кнопками')
    @commands.has_any_role(989929544704196618, 989527988959842345, 1061266758180286514, 1124021579702079588, 1124021498097704972)
    async def test(self, inter, nav: str = commands.Param(name='выберите-вид-навигации', choices=["Skins", "Главная"])):
        if nav == "Skins":
            emb1 = disnake.Embed(title="Теперь мы создаем дизайн! <:BBERRYnew1:1055609515371929751><:BBERRYnew2:1055609516676362341>", description="Выбери и оплати покупку за пару кликов, а \nнаша умная помощница « Ягодка » поможет \nоформить заказ!", color=0xffc000,)
            emb1.set_image(url="https://media.discordapp.net/attachments/992105125453775003/1120850210717958174/Frame_787.png?width=671&height=671")
            await inter.channel.send(embed=emb1, components=[disnake.ui.Button(label="Оформить заказ", style=disnake.ButtonStyle.success, custom_id="zkbt"), disnake.ui.Button(label='Отзывы', style=disnake.ButtonStyle.url, url='https://discord.com/channels/989526750813909034/1126112940903366707', emoji='<:chat:1063849144843763753>')])
            await inter.send('готово', ephemeral=True)
        if nav == 'Главная':
            c1 = self.bot.get_channel(1126113258970042428)
            c2 = self.bot.get_channel(1126113100928663562)
            c3 = self.bot.get_channel(989528054441328720)
            embed = disnake.Embed(title='Что такое BERRY?', description=f'⚠️ Мы объединяем любителей известной кубической игры в одно сообщество. Создаем сервера, проекты и творим интересный контент!\n\n{c1.mention}⁠ - Начало! Ознакомьтесь с нашими товарами.\n{c2.mention} - Оформите и оплатите свой заказ, в этом вам поможет наша умная помощница «Ягодка».\n⁠{c3.mention} - Знакомьтесь и общайтесь!', color=0x520014).set_image(url='https://media.discordapp.net/attachments/991705191978115132/1125946130857996298/Frame_878_1.png?width=852&height=528')
            await inter.send('Готово', ephemeral=True)
            await inter.channel.send(embed=embed)
    
    @commands.slash_command(name='оштрафовать', description='оштрафовать участника')
    @commands.has_any_role(989527988959842345, 1061266758180286514, 1124021498097704972)
    async def shtarf(self, inter, summa: int = commands.Param(name='сумма', description='выберите сумму'),user: disnake.Member = commands.Param(name='участник', description='выберите участника')):
        doc = painter.find_one({"_id": user.id})
        if doc is not None:
            painter.update_one({"_id": user.id}, {"$inc": {'getprice': -summa}})
            await inter.send(embed=disnake.Embed(title='Штраф', description=f'Уастник {user.mention} был оштрафован на {summa} RUB'), ephemeral=True)
        else:
            await inter.send('Ошибка', ephemeral=True)

    @commands.slash_command(name='премия', description='выдать премию')
    @commands.has_any_role(989527988959842345, 1061266758180286514, 1124021498097704972)
    async def premia(self, inter, summa: int = commands.Param(name='сумма', description='выберите сумму'),user: disnake.Member = commands.Param(name='участник', description='выберите участника')):
        doc = painter.find_one({"_id": user.id})
        if doc is not None:
            painter.update_one({"_id": user.id}, {"$inc": {'getprice': summa}})
            await inter.send(embed=disnake.Embed(title='Премия', description=f'Уастник {user.mention} получил премию в размере {summa} RUB'), ephemeral=True)
        else:
            await inter.send('Ошибка', ephemeral=True)

    @commands.slash_command(name='удалить-ветку', description='удаление ветки')
    @commands.has_any_role(989929544704196618, 989527988959842345, 1061266758180286514, 1124021579702079588, 1124021498097704972)
    async def delt(self, inter, channel: disnake.Thread = commands.Param(name='ветка', description='выберите ветку для удаления')):
        await inter.send('Готово!', ephemeral=True) 
        await channel.delete()

    @commands.slash_command(name='статистика', description='посмотреть статистику')
    @commands.has_any_role(989929544704196618, 989527988959842345, 1061266758180286514, 1124021579702079588, 1124021498097704972)
    async def stat(self, inter):
        await inter.response.defer()
        total_members = 0
        for guild in self.bot.guilds:
            total_members += guild.member_count
        zakazov_all = servers.find_one({"_id": "count"})['zakaz']
        morwyy = self.bot.get_user(609737656363909151)
        essciz = self.bot.get_user(937410314100703243)
        mourt1n = self.bot.get_user(870550116887564348)
        gulava = self.bot.get_user(987793657723752468)
        kiborgtv = self.bot.get_user(617052770293252109)
        p1oko = self.bot.get_user(728648509334487102)
        nest = self.bot.get_user(986815186629455902)
        p1 = painter.find_one({"_id": 609737656363909151})
        p2 = painter.find_one({"_id": 937410314100703243})
        p3 = painter.find_one({"_id": 870550116887564348})
        p4 = painter.find_one({"_id": 987793657723752468})
        p5 = painter.find_one({"_id": 617052770293252109})
        p6 = painter.find_one({"_id": 728648509334487102})
        p7 = painter.find_one({"_id": 986815186629455902})

        threads_doc = active_threads.find_one({"_id": "count"})
        if threads_doc is not None:
            threads = str(threads_doc['threads'])
        else:
            threads = 0
        stars_doc1 = stars.find_one({"_id": int(609737656363909151)})
        stars_doc2 = stars.find_one({"_id": int(937410314100703243)})
        stars_doc3 = stars.find_one({"_id": int(870550116887564348)})
        stars_doc4 = stars.find_one({"_id": int(987793657723752468)})
        stars_doc5 = stars.find_one({"_id": int(617052770293252109)})
        stars_doc6 = stars.find_one({"_id": int(728648509334487102)})
        stars_doc7 = stars.find_one({"_id": int(986815186629455902)})

        if stars_doc1 is not None:
            rating_find1 = stars_doc1['rating']
        else:
            stars.insert_one({"_id": int(609737656363909151), "marks": [5], "rating": 5})
        
        if stars_doc2 is not None:
            rating_find2 = stars_doc2['rating']
        else:
            stars.insert_one({"_id": int(937410314100703243), "marks": [5], "rating": 5})
        
        if stars_doc3 is not None:
            rating_find3 = stars_doc3['rating']
        else:
            stars.insert_one({"_id": int(870550116887564348), "marks": [5], "rating": 5})
        if stars_doc4 is not None:
            rating_find4 = stars_doc4['rating']
        else:
            stars.insert_one({"_id": int(987793657723752468), "marks": [5], "rating": 5})
        if stars_doc5 is not None:
            rating_find5 = stars_doc5['rating']
        else:
            stars.insert_one({"_id": int(617052770293252109), "marks": [5], "rating": 5})
        if stars_doc6 is not None:
            rating_find6 = stars_doc6['rating']
        else:
            stars.insert_one({"_id": int(728648509334487102), "marks": [5], "rating": 5})
        if stars_doc7 is not None:
            rating_find7 = stars_doc7['rating']
        else:
            stars.insert_one({"_id": int(986815186629455902), "marks": [5], "rating": 5})

        await inter.send(embed=disnake.Embed(title='Статистика использования бота:', description=f'Сервера: `{len(self.bot.guilds)}`\nПользователи: `{total_members}`\nПинг: `{round(self.bot.latency*1000)}мс ({round(self.bot.latency*10)} сек)`\n\n**Статистика Skins:**\nЗаказов: `{zakazov_all}`\nАктивных заказов: `{threads}`').add_field(name='Статистика художников:', value=f"{morwyy.mention}⠀`{int(rating_find1)}⭐`⠀`{p1['getprice']} RUB`⠀`({p1['zakazs']} заказов)`\n{essciz.mention}⠀`{int(rating_find2)}⭐`⠀`{p2['getprice']} RUB`⠀`({p2['zakazs']} заказов)`\n{mourt1n.mention}⠀`{rating_find3}⭐`⠀`{p3['getprice']} RUB`⠀`({p3['zakazs']} заказов)`\n{gulava.mention}⠀`{rating_find4}⭐`⠀`{p4['getprice']} RUB`⠀`({p4['zakazs']} заказов)`\n{kiborgtv.mention}⠀`{rating_find5}⭐`⠀`{p5['getprice']} RUB`⠀`({p5['zakazs']} заказов)`\n{p1oko.mention}⠀`{rating_find6}⭐`⠀`{p6['getprice']} RUB`⠀`({p6['zakazs']} заказов)`\n{nest.mention}⠀`{rating_find7}⭐`⠀`{p7['getprice']} RUB`⠀`({p7['zakazs']} заказов)`", inline=False).set_thumbnail(url='https://media.discordapp.net/attachments/991705191978115132/1125071609661759560/1072938433867165798.png?width=120&height=120'), ephemeral=True, components=[disnake.ui.Button(label='Обновить', custom_id='reload')])
    
    @commands.slash_command(name='закрыть-заказ', description='завершить оплату')
    @commands.has_any_role(989929544704196618, 989527988959842345, 1061266758180286514, 1061266758180286514, 1125528249708056597, 1124021579702079588, 1124021498097704972, 1124021670424875109)
    async def closeorder(self, inter, image: disnake.Attachment = commands.Param(name='изображение', description='приккрепите изображение'), product: str = commands.Param(name='товар', description='выберите товар который вы выполнили', choices=['Скин', 'Тотем', 'Аватар', 'GIF-Аватар', 'Плащ'])):
        stars_doc = stars.find_one({"_id": inter.author.id})
        if stars_doc is not None:
            rating_find = stars_doc['rating']
        else:
            stars.insert_one({"_id": inter.author.id, "marks": [5], "rating": 5})
            rating_find = stars_doc['rating']
        embed = disnake.Embed(title='🧺 Спасибо за покупку!', description=f'Просим вас написать отзыв о товаре, а так-же вы можете оставить чаевые или закрыть заказ.')
        await inter.send('Готово!', ephemeral=True)
        synced_thread_doc = synced_threads.find_one({"target_thread_id": inter.channel.id}) 
        if synced_thread_doc:
            source_thread_id = synced_thread_doc["source_thread_id"]
            source_thread = self.bot.get_channel(int(source_thread_id))
            await source_thread.send(embed=embed, components=[disnake.ui.Button(label='Закрыть заказ', style=disnake.ButtonStyle.red, emoji='<:basket:1072938090647277698>', custom_id=f'closeorder:{inter.author.id}')])
            channel = self.bot.get_channel(1126112940903366707)
            ch = self.bot.get_channel(1126113100928663562)
            embed=disnake.Embed(description=f'**🎯 Заказ выполнил: {inter.author.mention} `(Рейтинг: {rating_find}⭐)`**\n\nЗаказать `{product}` можно тут — {ch.mention}')
            embed.set_image(url=image.url)
            message = await channel.send(embed=embed)
            await message.create_thread(name='Выполненный заказ')
    
    @commands.slash_command(name='панель-skins', description='настроить панель skins')
    @commands.has_any_role(1124021579702079588, 1124021498097704972)
    async def forhud(self, inter):
        embed = disnake.Embed(title='Твоя панель исполнителя!', description='Узнай свой рейтинг, баланс и количество заказов.')
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/992105125453775003/1124911089759555635/1072938423230410762.webp')

        view = disnake.ui.View()
        view.add_item(disnake.ui.Button(label='Заказы', custom_id='zakazss'))
        view.add_item(disnake.ui.Button(label='Баланс', style=disnake.ButtonStyle.green, custom_id='balance'))
        view.add_item(disnake.ui.Button(label='Рейтинг', custom_id='rating'))

        await inter.send('Готово!', ephemeral=True)
        await inter.channel.send(embed=embed, view=view)



def setup(bot):
    bot.add_cog(Commands(bot))