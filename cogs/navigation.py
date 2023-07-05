import disnake
from disnake.ext import commands
from pymongo import MongoClient
from disnake.ext.commands.cooldowns import BucketType
import random
import asyncio
from glQiwiApi import QiwiP2PClient
import datetime
from datetime import timedelta

cluster = MongoClient("mongodb+srv://xikon:joker12340000@cluster0.bvfeu4r.mongodb.net/?retryWrites=true&w=majority")
productDB = cluster['product']
DBtype = productDB['hands']
DBproduct = productDB['product']
DBprice = productDB['price']
DBdates = productDB['dates']

serverBD = cluster['server']
dbcode = productDB['code']
active_threads= serverBD['threads']
synced_threads = serverBD['synced_threads']
servers = serverBD['servers']

qiwiDB = cluster['qiwi']
qiwi_base = qiwiDB['qiwi']

paintersDB = cluster['painters']
stars = paintersDB['rating']
orders = paintersDB['orders']
painter = paintersDB['paintersinfo']


listsdb = cluster['lists']
thread_messages_coll = listsdb['thread_messages']
send_to_target_coll = listsdb['send_to_target']

SECRET_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InE0M3NiZC0wMCIsInVzZXJfaWQiOiI3OTE2Nzc1NTk3MCIsInNlY3JldCI6ImIzMDRmMzBiMWE1YjgwOGVkYTM1YzJiNmEyNjhjOWZjNjM4MjZkNmVlYjgxMTk5ZDU4NjAwNzhjMGNmNWZjMzgifX0="
p2p = QiwiP2PClient(secret_p2p=SECRET_KEY, shim_server_url="http://bretail.space/proxy/p2p/")

class SteveOrAlexHands(disnake.ui.View): #Три кнопки: Назад, Широкие, Тонкие
    def __init__(self):
        super().__init__()
    
    @disnake.ui.button(label='Назад', style=disnake.ButtonStyle.red, emoji='<:1046539994682097754:1072938078617993247>')
    async def _backbutton_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.message.delete()
        await inter.send(embed = disnake.Embed(title='Выбор услуги', description='Пожалуйста выберите услугу.'), view=Products())
    
    @disnake.ui.button(label='Широкие', style=disnake.ButtonStyle.gray)
    async def wide(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        DBtype.update_one({'_id': inter.author.id}, {'$set': {'руки': "Широкие"}}, upsert=True)
        embed = disnake.Embed(title='Давай определимся с выбором стиля 🌈')
        await inter.message.delete()
        await inter.send(embed=embed, view=SkinStyles())
    
    @disnake.ui.button(label='Тонкие', style=disnake.ButtonStyle.gray)
    async def _alex_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        DBtype.update_one({'_id': inter.author.id}, {'$set': {'руки': "Тонкие"}}, upsert=True)
        embed = disnake.Embed(title='Давай определимся с выбором стиля 🌈')
        await inter.message.delete()
        await inter.send(embed=embed, view=SkinStyles())

class Ordering(disnake.ui.View): #Две кнопки: Назад, Оформить заказ
    def __init__(self):
        super().__init__()

    @disnake.ui.button(label='Назад', style=disnake.ButtonStyle.red, emoji='<:1046539994682097754:1072938078617993247>')
    async def _backbutton_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.message.delete()
        await inter.send(embed = disnake.Embed(title='Выбор услуги', description='Пожалуйста выберите услугу.'), view=Products())


    @disnake.ui.button(label='Оформить заказ', style=disnake.ButtonStyle.green, custom_id='makebuy', emoji='<:yes:1072938130199552030>')
    async def __ofromzakaz__(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        product = DBproduct.find_one({"_id": inter.author.id})['товар']
        description=f'Товар — `{product}`\n\nОтправь описание в чат, так же ты можешь прикрепить до десяти изображений в формате png, jpg, jpeg, webp, gif.'
        if product == 'Скин « Classic »' or product == "Скин « Modern »":
            hands = DBtype.find_one({"_id": inter.author.id})['руки']
            description = f'Товар — `{product}`\nРуки — `{hands}`\n\nОтправь описание в чат, также ты можешь прикрепить до десяти изображений в формате png, jpg, jpeg, webp, gif.'
        embed = disnake.Embed(title='💭 Теперь расскажи о том, как ты видишь свой будущий заказ.', description=description)
        await inter.message.delete()
        await inter.send(embed=embed, view=Cancel())
        thread_messages_coll.update_one({'_id': inter.channel.id}, {"$set": {"value": 1}}, upsert=True)

class OrderingForSkins(disnake.ui.View): #Две кнопки: Назад, Оформить заказ
    def __init__(self):
        super().__init__()

    @disnake.ui.button(label='Назад', style=disnake.ButtonStyle.red, emoji='<:1046539994682097754:1072938078617993247>')
    async def _backbutton_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Давай определимся с выбором стиля 🌈')
        await inter.message.delete()
        await inter.send(embed=embed, view=SkinStyles())


    @disnake.ui.button(label='Оформить заказ', style=disnake.ButtonStyle.green, custom_id='makebuy', emoji='<:yes:1072938130199552030>')
    async def __ofromzakaz__(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        product = DBproduct.find_one({"_id": inter.author.id})['товар']
        description=f'Товар — `{product}`\n\nОтправь описание в чат, так же ты можешь прикрепить до десяти изображений в формате png, jpg, jpeg, webp, gif.'
        if product == 'Скин « Classic »' or product == "Скин « Modern »" or product == 'Скин « Future »':
            hands = DBtype.find_one({"_id": inter.author.id})['руки']
            description = f'Товар — `{product}`\nРуки — `{hands}`\n\nОтправь описание в чат, также ты можешь прикрепить до десяти изображений в формате png, jpg, jpeg, webp, gif.'
        embed = disnake.Embed(title='💭 Теперь расскажи о том, как ты видишь свой будущий заказ.', description=description)
        await inter.message.delete()
        await inter.send(embed=embed, view=Cancel())
        thread_messages_coll.update_one({'_id': inter.channel.id}, {"$set": {"value": 1}}, upsert=True)

class Cancel(disnake.ui.View): #Две кнопки: Modern и Classic
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label='Отмена', style=disnake.ButtonStyle.red, emoji='<:1046539994682097754:1072938078617993247>')
    async def _backbutton_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.message.delete()
        await inter.send(embed = disnake.Embed(title='Выбор услуги', description='Пожалуйста выберите услугу.'), view=Products())
        try: 
            thread_messages_coll.delete_one({"_id": inter.channel.id})
        except:
            pass

class SkinStyles(disnake.ui.View): #Две кнопки: Future и Classic и Modern
    def __init__(self):
        super().__init__(timeout=None)
    
    @disnake.ui.button(label='Назад', style=disnake.ButtonStyle.red, emoji='<:1046539994682097754:1072938078617993247>')
    async def _backbutton_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Теперь выбери вид рук 👋', description='Какие руки ты хочешь? Стандартные как на первом примере, или на пару пикселей меньше, как на втором?', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1125973610302017568/Frame_770_2.png?width=852&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=SteveOrAlexHands())

    @disnake.ui.button(label='Classic', style=disnake.ButtonStyle.green, custom_id='classic')
    async def classic(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Скин « Classic »', description='Классика от нашей студии — скин, исполненный в стандартном разрешении, который выделит вас из толпы других игроков и добавит красок в игру.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108839754866698/Frame_871_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=OrderingForSkins()) 
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "Скин « Classic »"}}, upsert=True)
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "155"}}, upsert=True)

    @disnake.ui.button(label='Future', style=disnake.ButtonStyle.green, custom_id='future')
    async def future(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Скин « Future »', description='Скин будущего, исполняется в сочных и контрастных цветах. Такой стиль отлично подходит для медийных личностей и запоминается с первого взгляда.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108838983127102/Frame_873_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=OrderingForSkins()) 
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "Скин « Future »"}}, upsert=True)
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "155"}}, upsert=True)

    @disnake.ui.button(label='Modern', style=disnake.ButtonStyle.green, custom_id='modern')
    async def modern(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Скин « Modern »', description='Современный и яркий — это про этот стиль. Уникальный скин, который наполнен деталями, будет сделан по вашему референсу или описанию.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108839364792330/Frame_872_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=OrderingForSkins()) 
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "Скин « Modern »"}}, upsert=True)
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "155"}}, upsert=True)

class Products(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)   

    @disnake.ui.button(label='Скин', style=disnake.ButtonStyle.green, emoji='<:Frame7833:1121710630047596665>', row=1, custom_id='skin', disabled=False)
    async def _skin_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Теперь выбери вид рук 👋', description='Какие руки ты хочешь? Стандартные как на первом примере, или на пару пикселей меньше, как на втором?', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1125973610302017568/Frame_770_2.png?width=852&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=SteveOrAlexHands())

    @disnake.ui.button(label='Тотем', style=disnake.ButtonStyle.green, emoji='<:Frame7863:1121710640998928424>', row=1, custom_id='totem')
    async def _totem_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction): 
        embed = disnake.Embed(title='Тотем 3D', description='Модель, выполненная в хайповом стиле,\nкоторой можно заменить обычный тотем в\nMinecraft и добавить стиля игре.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108841789104178/Frame_874_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=Ordering())
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "25"}}, upsert=True)
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "Тотем"}}, upsert=True)  
    
    @disnake.ui.button(label='Плащ', style=disnake.ButtonStyle.green, emoji='<:Frame7823:1121710634002808873>', row=1, custom_id='oformleinie')
    async def _oformelie_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Плащ', description='Привлекательный плащ, который создается отдельно для каждого заказчика и является уникальным атрибутом.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108840165920818/Frame_870_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=Ordering())
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "50"}}, upsert=True)
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "Плащ"}}, upsert=True)

    @disnake.ui.button(label='GIF-Аватар', style=disnake.ButtonStyle.green, row=2, emoji='<:Frame7813:1121710637572161617>', custom_id='gifavatar')
    async def _gifavatar_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='GIF Аватар Minecraft', description='Анимированный аватар покажет ваш скин со всех сторон. Доступен только с Discord нитро или Telegram Premium*.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108840606306304/Frame_869_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=Ordering())
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "110"}}, upsert=True)
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "GIF-Аватар"}}, upsert=True)  
    
    @disnake.ui.button(label='Аватар', style=disnake.ButtonStyle.green, emoji='<:Frame7803:1121710646552186931>', row=2, custom_id='avatar')
    async def _avatar_(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        embed = disnake.Embed(title='Аватар Minecraft', description='Уникальный аватар в стиле Minecraft для вашего аккаунта Discord, Вконтакте, Ютуб и любых страниц, который будет притягивать внимание.', color=0xFFC200)
        embed.set_image(url='https://media.discordapp.net/attachments/991705191978115132/1126108842267267082/Frame_868_1.png?width=528&height=528')
        await inter.message.delete()
        await inter.send(embed=embed, view=Ordering())
        DBprice.update_one({'_id': inter.author.id}, {'$set': {'цена': "40"}}, upsert=True)
        DBproduct.update_one({'_id': inter.author.id}, {'$set': {'товар': "Аватар"}}, upsert=True)

class Navigation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.cd_map = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)
        self.rating = {}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, disnake.Thread) and message.channel.parent_id == 1126113100928663562:
            if not message.author.bot:
                message_channel_find = thread_messages_coll.find_one({"_id": message.channel.id})
                if message_channel_find is None:
                    return
                else:
                    value = message_channel_find['value']
                    if not message.author.bot and int(value) == 1:
                        product = DBproduct.find_one({"_id": message.author.id})['товар']
                        summa = DBprice.find_one({'_id': message.author.id})['цена']
                        old_url_find = qiwi_base.find_one({"_id": message.author.id})
                        if old_url_find is not None:
                            bill_find = old_url_find['bill_id']
                            try:
                                await p2p.reject_p2p_bill(bill_id=bill_find)
                            except:
                                pass
                        new_bill = await p2p.create_p2p_bill(bill_id=random.randint(10000000, 9999999999), amount=int(summa), comment=f'Новая покупка —\nКлиент: {message.author}\nТовар: {product}', theme_code="Egor-TsD9p1Nh-7j")
                        shim_url = p2p.create_shim_url(new_bill)
                        qiwi_base.update_many({'_id': message.author.id}, {'$set': {'bill_id': str(new_bill.id), 'pay_url': str(shim_url)}}, upsert=True)
                        embed = disnake.Embed(description=f'Отлично, заказ почти оформлен, осталось только оплатить!\nС Вас ``{summa}`` рублей, после оплаты мы сразу начнем выполнять ваш заказ.')
                        await message.reply(embed=embed, components=[
                            disnake.ui.Button(label='Оплатить', style=disnake.ButtonStyle.url, url=f'{shim_url}'),
                            disnake.ui.Button(label='Проверить оплату', style=disnake.ButtonStyle.blurple, custom_id='check')
                        ], mention_author=False)
                        thread_messages_coll.update_one({"_id": message.channel.id}, {"$set": {'value': 0}})
        
        if not message.author.bot:
            product_doc = DBproduct.find_one({"_id": message.author.id})
            if product_doc:
                source_channel_id = 1126113100928663562
                target_channel_id = 1124389034131730492
                source_channel = self.bot.get_channel(source_channel_id)
                target_channel = self.bot.get_channel(target_channel_id)
                source_thread = next((t for t in source_channel.threads if t.id == message.channel.id), None)
                target_thread = next((t for t in target_channel.threads if t.id == message.channel.id), None)
                if source_thread:
                    synced_thread = synced_threads.find_one({"source_thread_id": source_thread.id})
                    if synced_thread:
                        target_thread_id = synced_thread["target_thread_id"]
                        target_thread = target_channel.get_thread(target_thread_id)
                        if target_thread:
                            if message.content:
                                vl = send_to_target_coll.find_one({"msg": message.channel.id})['value']
                                if int(vl) == 0:
                                    product = DBproduct.find_one({"_id": message.author.id})['товар']
                                    hands_doc = DBtype.find_one({"_id": message.author.id})
                                    if hands_doc:
                                        hands = hands_doc['руки']                                      
                                        current_date = datetime.datetime.now()
                                        due_date = current_date + datetime.timedelta(days=5)
                                        formatted_date = f"{due_date.day}.{due_date.month:02d}.{due_date.year} {due_date.hour:02d}:{due_date.minute:02d}"
                                        if product in ['Тотем', 'Аватар', 'Плащ', 'GIF-Аватар']:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        else:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n{hands} руки\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        await target_thread.send(msg)
                                        DBdates.update_one({"_id": message.author.id}, {"$set": {'date': str(formatted_date)}}, upsert=True)
                                        send_to_target_coll.update_one({"msg": message.channel.id}, {"$set": {'value': 1}}, upsert=True)
                                        for attachment in message.attachments:
                                            file = await attachment.to_file()
                                            await target_thread.send(file=file)
                                    else:
                                        current_date = datetime.datetime.now()
                                        due_date = current_date + datetime.timedelta(days=5)
                                        formatted_date = f"{due_date.day}.{due_date.month:02d}.{due_date.year} {due_date.hour:02d}:{due_date.minute:02d}"
                                        if product in ['Тотем', 'Аватар', 'Плащ', 'GIF-Аватар']:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        else:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n{hands} руки\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        await target_thread.send(msg)
                                        DBdates.update_one({"_id": message.author.id}, {"$set": {'date': str(formatted_date)}}, upsert=True)
                                        send_to_target_coll.update_one({"msg": message.channel.id}, {"$set": {'value': 1}}, upsert=True)
                                        for attachment in message.attachments:
                                            file = await attachment.to_file()
                                            await target_thread.send(file=file)
                                else:
                                    await target_thread.send(f"{message.content}")
                                    for attachment in message.attachments:
                                        file = await attachment.to_file()
                                        await target_thread.send(file=file)
                            
                            else:
                                vl = send_to_target_coll.find_one({"msg": message.channel.id})['value']
                                if int(vl) == 0:
                                    product = DBproduct.find_one({"_id": message.author.id})['товар']
                                    hands_doc = DBtype.find_one({"_id": message.author.id})
                                    if hands_doc:
                                        hands = hands_doc['руки']  
                                        current_date = datetime.datetime.now()
                                        due_date = current_date + datetime.timedelta(days=5)
                                        formatted_date = f"{due_date.day}.{due_date.month:02d}.{due_date.year} {due_date.hour:02d}:{due_date.minute:02d}"
                                        if product in ['Тотем', 'Аватар', 'Плащ', 'GIF-Аватар']:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        else:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n{hands} руки\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        await target_thread.send(msg)
                                        DBdates.update_one({"_id": message.author.id}, {"$set": {'date': str(formatted_date)}}, upsert=True)
                                        send_to_target_coll.update_one({"msg": message.channel.id}, {"$set": {'value': 1}}, upsert=True)
                                        for attachment in message.attachments:
                                            file = await attachment.to_file()
                                            await target_thread.send(file=file)
                                    else:
                                        current_date = datetime.datetime.now()
                                        due_date = current_date + datetime.timedelta(days=5)
                                        formatted_date = f"{due_date.day}.{due_date.month:02d}.{due_date.year} {due_date.hour:02d}:{due_date.minute:02d}"
                                        if product in ['Тотем', 'Аватар', 'Плащ', 'GIF-Аватар']:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        else:
                                            msg = f"🛒 Новый заказ:\n\n{product}\n{hands} руки\n\nОписание товара: {message.content}\n\nСдать до {formatted_date}"
                                        await target_thread.send(msg)
                                        DBdates.update_one({"_id": message.author.id}, {"$set": {'date': str(formatted_date)}}, upsert=True)
                                        send_to_target_coll.update_one({"msg": message.channel.id}, {"$set": {'value': 1}}, upsert=True)
                                        for attachment in message.attachments:
                                            file = await attachment.to_file()
                                            await target_thread.send(file=file)
                                else:
                                    for attachment in message.attachments:
                                        file = await attachment.to_file()
                                        await target_thread.send(file=file)

                elif target_thread:
                    synced_thread = synced_threads.find_one({"target_thread_id": target_thread.id})
                    if synced_thread:
                        source_thread_id = synced_thread["source_thread_id"]
                        source_thread = source_channel.get_thread(source_thread_id)
                        if source_thread:
                            if message.content:
                                await source_thread.send(f"{message.content}")
                            for attachment in message.attachments:
                                file = await attachment.to_file()
                                await source_thread.send(file=file)

    @commands.Cog.listener()
    async def on_thread_create(self, thread):
        if thread.parent_id == 1126113100928663562:
            target_channel_id = 1124389034131730492
            target_channel = self.bot.get_channel(target_channel_id)
            channel = self.bot.get_channel(1124389034131730492)
            existing_thread = disnake.utils.get(channel.threads, name=thread.name)
            if existing_thread is not None:
                await existing_thread.delete()
            created_thread = await target_channel.create_thread(name=thread.name, type=disnake.ChannelType.private_thread)
            synced_threads.update_one({"source_thread_id": thread.id}, {"$set": {"target_thread_id": created_thread.id}}, upsert=True)
            send_to_target_coll.update_one({"msg": thread.id}, {"$set": {'value': 0}}, upsert=True)
    
    @commands.slash_command(name='оплатить', description='оплатить покупку')
    @commands.has_any_role(989929544704196618, 989527988959842345, 1061266758180286514, 1124021579702079588, 1124021498097704972)
    async def paid(self, inter, user: disnake.Member = commands.Param(name='участник', description='выберите участника')):
        base_doc = qiwi_base.find_one({"_id": user.id})
        if base_doc is not None:
            try:
                await inter.author.add_roles(inter.author.guild.get_role(989527992109789218))
                await inter.author.send("Привет! Мы уже работаем над твоим заказом 🥳\n👉 А что бы ожидание не казалось долгим — предлагаем заглянуть в чат (<#989528054441328720>)!")
            except:
                pass
            await inter.send('Готово!', ephemeral=True)
            
            await inter.channel.send(embed=disnake.Embed(description='Оплата прошла успешно!\nМы приняли ваш заказ и передали исполнителю.', color=0x52FF00))
            else_artist = self.bot.get_user(986815186629455902)
            skin = DBproduct.find_one({"_id": inter.author.id})['товар']
            code_find = dbcode.find_one({"_id": "code"})
            code = code_find['number']
            dbcode.update_one({"_id": "code"}, {"$inc": {"number": 1}})
            current_date = datetime.datetime.now()
            due_date = current_date + datetime.timedelta(days=5)
            formatted_date = f"{due_date.day}.{due_date.month:02d}.{due_date.year} {due_date.hour:02d}:{due_date.minute:02d}"
            await inter.channel.edit(name=f'Заказ {code}')
            if skin == 'Скин « Classic »':
                classic_artist1 = self.bot.get_user(609737656363909151)
                classic_artist2 = self.bot.get_user(937410314100703243)
                random_select_classic = random.choice([classic_artist1, classic_artist2])
                if random_select_classic == classic_artist1:
                    classic = 'Максим'
                    stars_doc = stars.find_one({"_id": 609737656363909151})
                    rating_find_classic = stars_doc['rating']
                else:
                    classic = 'Михаил'
                    stars_doc = stars.find_one({"_id": 937410314100703243})
                    rating_find_classic = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет {classic} `{rating_find_classic}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(random_select_classic.mentio, else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": random_select_classic.id}, {"$push": {'orders': f'#{code}: • Стиль: Classic сдать до {formatted_date}'}}, upsert=True)
            if skin == 'Скин « Future »':
                future_artist1 = self.bot.get_user(870550116887564348)
                future_artist2 = self.bot.get_user(987793657723752468)
                random_select_future = random.choice([future_artist1, future_artist2])
                if random_select_future == future_artist1:
                    future = 'Елнур'
                    stars_doc = stars.find_one({"_id": 870550116887564348})
                    rating_find_future = stars_doc['rating']
                else:
                    future = 'Андрей'
                    stars_doc = stars.find_one({"_id": 987793657723752468})
                    rating_find_future = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет {future} `{rating_find_future}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(random_select_future.mention, else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": random_select_future.id}, {"$push": {'orders': f'#{code}: • Стиль: Future сдать до {formatted_date}'}}, upsert=True)
            if skin == 'Скин « Modern »':
                modern_artist1 = self.bot.get_user(617052770293252109)
                modern_artist2 = self.bot.get_user(728648509334487102)
                random_select_modern = random.choice([modern_artist1, modern_artist2])
                if random_select_modern == modern_artist1:
                    modern = 'Глеб'
                    stars_doc = stars.find_one({"_id": 617052770293252109})
                    rating_find_modern = stars_doc['rating']
                else:
                    modern = 'Александр'
                    stars_doc = stars.find_one({"_id": 728648509334487102})
                    rating_find_modern = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет {modern} `{rating_find_modern}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(random_select_modern.mention, else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": random_select_modern.id}, {"$push": {'orders': f'#{code}: • Стиль: Modern сдать до {formatted_date}'}}, upsert=True)
            if skin == 'Аватар':
                else_artist = self.bot.get_user(986815186629455902)
                stars_doc = stars.find_one({"_id": 986815186629455902})
                rating_nest = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: Аватар сдать до {formatted_date}'}}, upsert=True)
            if skin == 'Тотем':
                else_artist = self.bot.get_user(986815186629455902)
                stars_doc = stars.find_one({"_id": 986815186629455902})
                rating_nest = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: Тотем сдать до {formatted_date}'}}, upsert=True)
            if skin == 'GIF-Аватар':
                else_artist = self.bot.get_user(986815186629455902)
                stars_doc = stars.find_one({"_id": 986815186629455902})
                rating_nest = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: GIF-Аватар сдать до {formatted_date}'}}, upsert=True)
            if skin == 'Плащ':
                else_artist = self.bot.get_user(986815186629455902)
                stars_doc = stars.find_one({"_id": 986815186629455902})
                rating_nest = stars_doc['rating']
                await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                if synced_thread_doc:
                    source_thread_id = synced_thread_doc["target_thread_id"]
                th = self.bot.get_channel(int(source_thread_id))
                msg = await th.send(else_artist.mention)
                await msg.delete()
                date = DBdates.find_one({"_id": user.id})
                if date:
                    formatted_date = date['date']
                orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: Плащ сдать до {formatted_date}'}}, upsert=True)
            

    @commands.Cog.listener()
    async def on_button_click(self, inter):
        if inter.component.custom_id == 'check':
            base_doc = qiwi_base.find_one({"_id": inter.author.id})
            if base_doc is not None:
                bill_id = base_doc['bill_id']
                check_p2p = await p2p.get_bill_status(bill_id=bill_id)
                if check_p2p == 'PAID':
                    try:
                        await inter.author.add_roles(inter.author.guild.get_role(989527992109789218))
                        await inter.author.send("Привет! Мы уже работаем над твоим заказом 🥳\n👉 А что бы ожидание не казалось долгим — предлагаем заглянуть в чат (<#989528054441328720>)!")
                    except:
                        pass
                    await inter.response.defer()
                    await inter.channel.send(embed=disnake.Embed(description='Оплата прошла успешно!\nМы приняли ваш заказ и передали исполнителю.', color=0x52FF00))
                    skin = DBproduct.find_one({"_id": inter.author.id})['товар']
                    code_find = dbcode.find_one({"_id": "code"})
                    code = code_find['number']
                    dbcode.update_one({"_id": "code"}, {"$inc": {"number": 1}})
                    current_date = datetime.datetime.now()
                    due_date = current_date + datetime.timedelta(days=5)
                    formatted_date = f"{due_date.day}.{due_date.month:02d}.{due_date.year} {due_date.hour:02d}:{due_date.minute:02d}"
                    await inter.channel.edit(name=f'Заказ {code}')
                    if skin == 'Скин « Classic »':
                        classic_artist1 = self.bot.get_user(609737656363909151)
                        classic_artist2 = self.bot.get_user(937410314100703243)
                        random_select_classic = random.choice([classic_artist1, classic_artist2])
                        if random_select_classic == classic_artist1:
                            classic = 'Максим'
                            stars_doc = stars.find_one({"_id": 609737656363909151})
                            rating_find_classic = stars_doc['rating']
                        else:
                            classic = 'Михаил'
                            stars_doc = stars.find_one({"_id": 937410314100703243})
                            rating_find_classic = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет {classic} `{rating_find_classic}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(random_select_classic.mention, else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": random_select_classic.id}, {"$push": {'orders': f'#{code}: • Стиль: Classic сдать до {formatted_date}'}}, upsert=True)
                    if skin == 'Скин « Future »':
                        future_artist1 = self.bot.get_user(870550116887564348)
                        future_artist2 = self.bot.get_user(987793657723752468)
                        random_select_future = random.choice([future_artist1, future_artist2])
                        if random_select_future == future_artist1:
                            future = 'Елнур'
                            stars_doc = stars.find_one({"_id": 870550116887564348})
                            rating_find_future = stars_doc['rating']
                        else:
                            future = 'Андрей'
                            stars_doc = stars.find_one({"_id": 987793657723752468})
                            rating_find_future = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет {future} `{rating_find_future}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(random_select_future.mention, else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": random_select_future.id}, {"$push": {'orders': f'#{code}: • Стиль: Future сдать до {formatted_date}'}}, upsert=True)
                    if skin == 'Скин « Modern »':
                        modern_artist1 = self.bot.get_user(617052770293252109)
                        modern_artist2 = self.bot.get_user(728648509334487102)
                        random_select_modern = random.choice([modern_artist1, modern_artist2])
                        if random_select_modern == modern_artist1:
                            modern = 'Глеб'
                            stars_doc = stars.find_one({"_id": 617052770293252109})
                            rating_find_modern = stars_doc['rating']
                        else:
                            modern = 'Александр'
                            stars_doc = stars.find_one({"_id": 728648509334487102})
                            rating_find_modern = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет {modern} `{rating_find_modern}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(random_select_modern.mention, else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": random_select_modern.id}, {"$push": {'orders': f'#{code}: • Стиль: Modern сдать до {formatted_date}'}}, upsert=True)
                    if skin == 'Аватар':
                        else_artist = self.bot.get_user(986815186629455902)
                        stars_doc = stars.find_one({"_id": 986815186629455902})
                        rating_nest = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: Аватар сдать до {formatted_date}'}}, upsert=True)
                    if skin == 'Тотем':
                        else_artist = self.bot.get_user(986815186629455902)
                        stars_doc = stars.find_one({"_id": 986815186629455902})
                        rating_nest = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: Тотем сдать до {formatted_date}'}}, upsert=True)
                    if skin == 'GIF-Аватар':
                        else_artist = self.bot.get_user(986815186629455902)
                        stars_doc = stars.find_one({"_id": 986815186629455902})
                        rating_nest = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: GIF-Аватар сдать до {formatted_date}'}}, upsert=True)
                    if skin == 'Плащ':
                        else_artist = self.bot.get_user(986815186629455902)
                        stars_doc = stars.find_one({"_id": 986815186629455902})
                        rating_nest = stars_doc['rating']
                        await inter.channel.send(f'Ваш заказ выполняет Нест `{rating_nest}⭐`')
                        synced_thread_doc = synced_threads.find_one({"source_thread_id": inter.channel.id}) 
                        if synced_thread_doc:
                            source_thread_id = synced_thread_doc["target_thread_id"]
                        th = self.bot.get_channel(int(source_thread_id))
                        msg = await th.send(else_artist.mention)
                        await msg.delete()
                        date = DBdates.find_one({"_id": inter.author.id})
                        if date:
                            formatted_date = date['date']
                        orders.update_one({"_id": else_artist.id}, {"$push": {'orders': f'#{code}: • Товар: Плащ сдать до {formatted_date}'}}, upsert=True)

                    try: 
                        await p2p.reject_p2p_bill(bill_id=bill_id)
                    except:
                        print('i cant')
                    qiwi_base.delete_one({"_id": inter.author.id})
                if check_p2p == 'WAITING':
                    await inter.send('Упс! Оплата еще не найдена. Если Вы оплатили заказ — попробуйте нажать через минуту.', ephemeral=True)
                if check_p2p == 'REJECTED':
                    await inter.send('Ваш заказ отменен или произошла ошибка!', ephemeral=True)
            else:
                await inter.send('У вас нет активных платежей.', ephemeral=True)

        if inter.component.custom_id.startswith('closeorder:'):
            user_id = inter.component.custom_id.split(':')[1]
            channel = inter.guild.get_channel(1126112940903366707)
            if inter.author.id in [609737656363909151,937410314100703243,870550116887564348,987793657723752468,617052770293252109,728648509334487102]:
                await inter.send(embed=disnake.Embed(title="Ошибка", description='Вы не можете закрыть этот заказ  <:MarkNo2:1055609056343113955>', color=disnake.Color.red()), ephemeral=True)
            else:
                await inter.send(f'Просим оставить рейтинг нашему художнику!', components=[disnake.ui.Button(label='1', emoji='⭐', custom_id=f'star1:{user_id}'),
                                                                                           disnake.ui.Button(label='2', emoji='⭐', custom_id=f'star2:{user_id}'), 
                                                                                           disnake.ui.Button(label='3', emoji='⭐', custom_id=f'star3:{user_id}'), 
                                                                                           disnake.ui.Button(label='4', emoji='⭐', custom_id=f'star4:{user_id}'), 
                                                                                           disnake.ui.Button(label='5', emoji='⭐', custom_id=f'star5:{user_id}')])

        if inter.component.custom_id == 'zkbt':
            cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, BucketType.user)
            bucket = cd_mapping.get_bucket(inter)
            retry_after = bucket.update_rate_limit()
            if retry_after:
                await inter.response.send_message(embed=disnake.Embed(title='Ошибка', description = f"**Нажмите через {int(retry_after)} секунд!**", color=disnake.Color.red()), ephemeral=True)
                return
            await inter.response.defer()        
            channel = inter.guild.get_channel(1126113100928663562)
            existing_thread = disnake.utils.get(channel.threads, name=f'Оформление заказа ({inter.author.name})')
            if existing_thread is not None:
                await existing_thread.delete()
            thread = await channel.create_thread(name=f'Оформление заказа ({inter.author.name})', type=disnake.ChannelType.private_thread)
            embed = disnake.Embed(title='Выбор услуги', description='Пожалуйста выберите услугу.')
            nest = inter.bot.get_user(986815186629455902) 
            xikon = inter.bot.get_user(768075509480292383)
            await thread.send(embed=embed, view=Products())
            msg = await thread.send(f"{inter.author.mention} {nest.mention} {xikon.mention} ")
            await msg.delete()
            active_threads.update_one({'_id': 'count'}, {'$inc': {'threads': 1}}, upsert=True)
            await inter.send(f'👉 Ваш заказ тут — **{thread.mention}**', ephemeral=True)


        if inter.component.custom_id.startswith('star'):
            if int(inter.author.id) in self.rating:
                await inter.send('Вы уже оставили рейтинг этому художнику!', ephemeral=True)
            else:
                if inter.author.id not in [609737656363909151,937410314100703243,870550116887564348,987793657723752468,617052770293252109,728648509334487102]:
                    user_id = inter.component.custom_id.split(':')[1]
                    stars_doc = stars.find_one({"_id": int(user_id)})
                    if stars_doc is not None:
                        stars_marks = list(stars_doc['marks'])
                    else:
                        stars.insert_one({"_id": int(user_id), "marks": [5], "rating": 5})
                    chan = self.bot.get_channel(1126112940903366707)
                    self.rating[int(inter.author.id)] = True
                    if inter.component.custom_id.startswith('star1'):
                        await inter.message.edit(components=[disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True)])
                        await inter.send(f'Спасибо за вашу оценку, теперь вы можете оставить отзыв в канале - {chan.mention}', ephemeral=True)
                        stars_marks.append(1)
                    if inter.component.custom_id.startswith('star2'):
                        await inter.message.edit(components=[disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True)])
                        await inter.send(f'Спасибо за вашу оценку, теперь вы можете оставить отзыв в канале - {chan.mention}', ephemeral=True)
                        stars_marks.append(2)
                    if inter.component.custom_id.startswith('star3'):
                        await inter.message.edit(components=[disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True)])
                        await inter.send(f'Спасибо за вашу оценку, теперь вы можете оставить отзыв в канале - {chan.mention}', ephemeral=True)
                        stars_marks.append(3)
                    if inter.component.custom_id.startswith('star4'):
                        await inter.message.edit(components=[disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True)])
                        await inter.send(f'Спасибо за вашу оценку, теперь вы можете оставить отзыв в канале - {chan.mention}', ephemeral=True)
                        stars_marks.append(4)
                    if inter.component.custom_id.startswith('star5'):
                        await inter.message.edit(components=[disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True), disnake.ui.Button(emoji='⭐', disabled=True)])
                        await inter.send(f'Спасибо за вашу оценку, теперь вы можете оставить отзыв в канале - {chan.mention}', ephemeral=True)
                        stars_marks.append(5)
                    updated_rating = round(sum(stars_marks) / len(stars_marks), 1)
                    stars.update_many({"_id": int(user_id)}, {"$set": {"marks": stars_marks, "rating": updated_rating}}, upsert=True)
                    active_threads.update_one({"_id": "count"}, {"$inc": {"threads": -1}}, upsert=True)
                    await asyncio.sleep(10)
                    await inter.channel.delete()
                    del self.rating[int(inter.author.id)]
                    if int(user_id) == 986815186629455902:
                        product_find = DBproduct.find_one({"_id": inter.author.id})['товар']
                        if product_find == 'Плащ':
                            painter.update_many({"_id": 986815186629455902}, {"$inc": {"getprice": 50, "zakazs": 1}}, upsert=True)
                        if product_find == 'Тотем':
                            painter.update_many({"_id": 986815186629455902}, {"$inc": {"getprice": 25, "zakazs": 1}}, upsert=True)
                        if product_find == 'Аватар':
                            painter.update_many({"_id": 986815186629455902}, {"$inc": {"getprice": 40, "zakazs": 1}}, upsert=True)
                        if product_find == 'GIF-Аватар':
                            painter.update_many({"_id": 986815186629455902}, {"$inc": {"getprice": 110, "zakazs": 1}}, upsert=True)
                    else:
                        painter.update_many({"_id": int(user_id)}, {"$inc": {"getprice": 70, "zakazs": 1}}, upsert=True)
                    servers.update_one({"_id": "count"}, {"$inc": {"zakaz": 1}}, upsert=True)
                    synced_thread = synced_threads.find_one({"source_thread_id": inter.channel.id})
                    if synced_thread:
                        target_id = synced_thread['target_thread_id']
                        th = self.bot.get_channel(int(target_id))
                        await th.delete()
                        synced_threads.delete_one({"source_thread_id": inter.channel.id})
                else:
                    await inter.send(embed=disnake.Embed(title="Ошибка", description='Вы не можете поставить оценку самому себе!  <:MarkNo2:1055609056343113955>', color=disnake.Color.red()), ephemeral=True)

def setup(bot):
    bot.add_cog(Navigation(bot))
