from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import logging
from pymongo import MongoClient
from pyqiwip2p import QiwiP2P
import random
import aiogram

QIWI_PRIV_KEY = "eyJ2ZXJzaW9uIjoiUDJQIiwiZGF0YSI6eyJwYXlpbl9tZXJjaGFudF9zaXRlX3VpZCI6InE0M3NiZC0wMCIsInVzZXJfaWQiOiI3OTE2Nzc1NTk3MCIsInNlY3JldCI6ImIzMDRmMzBiMWE1YjgwOGVkYTM1YzJiNmEyNjhjOWZjNjM4MjZkNmVlYjgxMTk5ZDU4NjAwNzhjMGNmNWZjMzgifX0="
p2p = QiwiP2P(auth_key=QIWI_PRIV_KEY)

cluster = MongoClient("mongodb+srv://xikon:joker12340000@cluster0.bvfeu4r.mongodb.net/?retryWrites=true&w=majority")
db = cluster['keys']
qiwi_base = db['qiwi']

API_TOKEN = '6145433316:AAFoBcDUYNwTZeyT7_T8sFdfju61MvN0bkc'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    caption="Приветствуем тебя в Berry Shop, передовом магазине Minecraft-ключей и Discord Nitro. У нас одни из самых выгодных цен на рынке и наилучший сервис, потыкай кнопки внизу и убедись сам!"
    kb = [[types.KeyboardButton(text="Товары")]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите кнопку:")
    photo_file = open('./' + '1.png', 'rb')
    await bot.send_photo(photo=photo_file, chat_id=message.chat.id, caption=caption, parse_mode="HTML", reply_markup=keyboard)

@dp.message_handler(Text("Товары"))
async def list_things(message : types.Message):
    photo_file = open('./' + '2.png', 'rb')
    Tovar_variant = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(text="Minecraft", callback_data="minecraft"),types.InlineKeyboardButton(text="Discord", callback_data="discord"))
    await bot.send_photo(chat_id=message.chat.id, photo=photo_file, caption="Выберите категорию", reply_markup=Tovar_variant)

@dp.callback_query_handler(Text("tovari"))
async def tovari(callback: types.CallbackQuery):
    photo_file = open('./' + '2.png', 'rb')
    Tovari = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton(text="Minecraft", callback_data="minecraft"),types.InlineKeyboardButton(text="Discord", callback_data="discord"))
    await callback.message.delete()
    await bot.send_photo(chat_id=callback.message.chat.id, photo=photo_file, caption="Выберите категорию", reply_markup=Tovari)

@dp.callback_query_handler(Text("minecraft"))
async def get_minecraft_things(callback: types.CallbackQuery):
    photo_file = open('./' + '3.png', 'rb')
    Minecraft_things = types.InlineKeyboardMarkup()
    Minecraft_things.add(types.InlineKeyboardButton(text="Minecraft Java & Bedrock edition - 1390₽",callback_data="minecraft_general"))
    Minecraft_things.add(types.InlineKeyboardButton(text="Minecraft Dungeons - 790₽",callback_data="dungeons_general"))
    Minecraft_things.add(types.InlineKeyboardButton(text="Плащ Optifine - 180₽",callback_data="optifine_general"))
    Minecraft_things.add(types.InlineKeyboardButton(text="Назад",callback_data="tovari"))
    await callback.message.delete()
    await bot.send_photo(
    chat_id=callback.message.chat.id,
    photo=photo_file,
    caption="Выберите услугу:",
    parse_mode="HTML",
    reply_markup=Minecraft_things
    )

@dp.callback_query_handler(Text("nitro"))
async def get_minecraft_things(callback: types.CallbackQuery):
    photo_file = open('./' + '4.png', 'rb')
    Nitro_things = types.InlineKeyboardMarkup()
    Nitro_things.add(types.InlineKeyboardButton(text="Discord Nitro Full | 1 месяц | 449₽",callback_data="nitro_full"))
    Nitro_things.add(types.InlineKeyboardButton(text="Discord Nitro Basic | 1 месяц | 199₽",callback_data="nitro_basic"))
    Nitro_things.add(types.InlineKeyboardButton(text="Назад",callback_data="tovari"))
    await callback.message.delete()
    await bot.send_photo(
    chat_id=callback.message.chat.id,
    photo=photo_file,
    caption="Выберите нитро:",
    parse_mode="HTML",
    reply_markup=Nitro_things
    )

@dp.callback_query_handler(Text("discord"))
async def get_minecraft_things(callback: types.CallbackQuery):
    photo_file = open('./' + '4.png', 'rb')
    Nitro_things = types.InlineKeyboardMarkup()
    Nitro_things.add(types.InlineKeyboardButton(text="Discord Nitro Full | 1 месяц | 449₽",callback_data="nitro_full"))
    Nitro_things.add(types.InlineKeyboardButton(text="Discord Nitro Basic | 1 месяц | 199₽",callback_data="nitro_basic"))
    Nitro_things.add(types.InlineKeyboardButton(text="Назад",callback_data="tovari"))
    await callback.message.delete()
    await bot.send_photo(
    chat_id=callback.message.chat.id,
    photo=photo_file,
    caption="Выберите нитро:",
    parse_mode="HTML",
    reply_markup=Nitro_things
    )

@dp.callback_query_handler(Text("minecraft_general"))
async def do_shit_with_java(callback: types.CallbackQuery):
    user = callback.from_user.username
    user_id = callback.from_user.id 
    pay_doc = qiwi_base.find_one({"_id": user_id})
    if pay_doc is not None:
        bill_find = pay_doc['bill_id']
        p2p.reject(bill_id=bill_find)
    new_bill = p2p.bill(bill_id=random.randint(10000000, 9999999999), amount=1390, lifetime=2880, comment=f'Новая покупка —\nКлиент: @{user}\nТовар: Ключ Minecraft Java & Bedrock', fields={"themeCode": "Egor-TsD9p1Nh-7j"})
    qiwi_base.update_many({'_id': user_id}, {'$set': {'bill_id': str(new_bill.bill_id ), 'pay_url': str(new_bill.pay_url)}}, upsert=True)
    Oplata_Minecraft = types.InlineKeyboardMarkup()
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Оплатить", url=str(new_bill.pay_url)))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Проверить оплату",callback_data="gotovo"))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Назад",callback_data="minecraft"))
    await callback.message.delete()
    await callback.message.answer_photo(
    photo=open('./' + 'minecraft.png', 'rb'),
    caption="Товар: Minecraft Java & Bedrock\nЦена: 1390₽\n\nПосле оплаты нажмите на кнопку (Проверить оплату). После чего бот проверит платеж и выдаст вам выбранный товар.\n\nЕсли оплата прошла успешно, то вы получите ключ, который необходимо активировать в Microsoft аккаунте, после чего – игра полностью и навсегда ваша.",
    parse_mode="HTML",
    reply_markup=Oplata_Minecraft)

@dp.callback_query_handler(Text("dungeons_general"))
async def do_shit_with_java(callback: types.CallbackQuery):
    user = callback.from_user.username
    user_id = callback.from_user.id
    pay_doc = qiwi_base.find_one({"_id": user_id})
    if pay_doc is not None:
        bill_find = pay_doc['bill_id']
        p2p.reject(bill_id=bill_find)
    new_bill = p2p.bill(bill_id=random.randint(10000000, 9999999999), amount=790, lifetime=2880, comment=f'Новая покупка —\nКлиент: @{user}\nТовар: Ключ Minecraft Dungeons', fields={"themeCode": "Egor-TsD9p1Nh-7j"})
    qiwi_base.update_many({'_id': user_id}, {'$set': {'bill_id': str(new_bill.bill_id ), 'pay_url': str(new_bill.pay_url)}}, upsert=True)
    Oplata_Minecraft = types.InlineKeyboardMarkup()
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Оплатить",url=str(new_bill.pay_url)))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Проверить оплату",callback_data="gotovo"))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Назад",callback_data="minecraft"))
    await callback.message.delete()
    await callback.message.answer_photo(
    photo=open('./' + 'dungeons.png', 'rb'),
    caption="Товар: Minecraft Dungeons\nЦена: 790₽\n\nПосле оплаты нажмите на кнопку (Проверить оплату). После чего бот проверит платеж и выдаст вам выбранный товар.\n\nЕсли оплата прошла успешно, то вы получите активацию ключ, на вашем аккаунте! После чего вы получите игру, она полностью ваша. Навсегда.",
    parse_mode="HTML",
    reply_markup=Oplata_Minecraft
    )
    user_id = callback.from_user.id

@dp.callback_query_handler(Text("optifine_general"))
async def do_shit_with_java(callback: types.CallbackQuery):
    user = callback.from_user.username
    user_id = callback.from_user.id 
    pay_doc = qiwi_base.find_one({"_id": user_id})
    if pay_doc is not None:
        bill_find = pay_doc['bill_id']
        p2p.reject(bill_id=bill_find)
    new_bill = p2p.bill(bill_id=random.randint(10000000, 9999999999), amount=180, lifetime=2880, comment=f'Новая покупка —\nКлиент: @{user}\nТовар: Optifine Плащ', fields={"themeCode": "Egor-TsD9p1Nh-7j"})
    qiwi_base.update_many({'_id': user_id}, {'$set': {'bill_id': str(new_bill.bill_id ), 'pay_url': str(new_bill.pay_url)}}, upsert=True)
    Oplata_Minecraft = types.InlineKeyboardMarkup()
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Оплатить",url=str(new_bill.pay_url)))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Проверить оплату",callback_data="gotovo"))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Назад",callback_data="minecraft"))
    await callback.message.delete()
    await callback.message.answer_photo(
    photo=open('./' + 'optifine.png', 'rb'),
    caption="Товар: Плащ Optifine\nЦена: 180₽\n\nПосле оплаты нажмите на кнопку (Проверить оплату). После чего бот проверит платеж и выдаст вам выбранный товар.\n\nЕсли оплата прошла успешно, то вы получите крутой плащ Optifine на ваш лицензионный ник. Видят его все у кого есть мод Optifine",
    parse_mode="HTML",
    reply_markup=Oplata_Minecraft
    )
    user_id = callback.from_user.id 

@dp.callback_query_handler(Text("nitro_full"))
async def do_shit_with_java(callback: types.CallbackQuery):
    user = callback.from_user.username
    user_id = callback.from_user.id
    pay_doc = qiwi_base.find_one({"_id": user_id})
    if pay_doc is not None:
        bill_find = pay_doc['bill_id']
        p2p.reject(bill_id=bill_find)
    new_bill = p2p.bill(bill_id=random.randint(10000000, 9999999999), amount=449, lifetime=2880, comment=f'Новая покупка —\nКлиент: @{user}\nТовар: Nitro Full', fields={"themeCode": "Egor-TsD9p1Nh-7j"})
    qiwi_base.update_many({'_id': user_id}, {'$set': {'bill_id': str(new_bill.bill_id ), 'pay_url': str(new_bill.pay_url)}}, upsert=True)
    Oplata_Minecraft = types.InlineKeyboardMarkup()
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Оплатить",url=str(new_bill.pay_url)))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Проверить оплату",callback_data="gotovo"))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Назад",callback_data="nitro"))
    await callback.message.delete()
    await callback.message.answer_photo(
    photo=open('./' + 'full.png', 'rb'),
    caption="Товар: Discord Нитро Full\nЦена: 449₽\n\nНаш самый популярный план подписки, Nitro, открывает доступ ко всем предлагаемым нами привилегиям, включая персонализированные эмодзи и стикеры, которые можно использовать повсеместно, потоковую передачу HD-видео и 2 буста сервера, и это лишь некоторые из них.\n\nПосле оплаты нажмите на кнопку (Проверить оплату). После чего бот проверит платеж и выдаст вам выбранный товар. Если оплата прошла успешно, то пожалуйста ожидайте выдачи товара.",
    parse_mode="HTML",
    reply_markup=Oplata_Minecraft)


@dp.callback_query_handler(Text("nitro_basic"))
async def do_shit_with_java(callback: types.CallbackQuery):
    user = callback.from_user.username
    user_id = callback.from_user.id
    pay_doc = qiwi_base.find_one({"_id": user_id})
    if pay_doc is not None:
        bill_find = pay_doc['bill_id']
        p2p.reject(bill_id=bill_find)
    new_bill = p2p.bill(bill_id=random.randint(10000000, 9999999999), amount=199, lifetime=2880, comment=f'Новая покупка —\nКлиент: @{user}\nТовар: Nitro Basic', fields={"themeCode": "Egor-TsD9p1Nh-7j"})
    qiwi_base.update_many({'_id': user_id}, {'$set': {'bill_id': str(new_bill.bill_id ), 'pay_url': str(new_bill.pay_url)}}, upsert=True)
    Oplata_Minecraft = types.InlineKeyboardMarkup()
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Оплатить",url=str(new_bill.pay_url)))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Проверить оплату",callback_data="gotovo"))
    Oplata_Minecraft.add(types.InlineKeyboardButton(text="Назад",callback_data="nitro"))
    await callback.message.delete()
    await callback.message.answer_photo(
    photo=open('./' + 'basic.png', 'rb'),
    caption="Товар: Discord Нитро Basic\nЦена: 199₽\n\nПлан подписки Nitro Basic включает в себя самые излюбленные перки Nitro, которые помогут вам лучше выразить себя, заплатив меньше.\nПосле оплаты нажмите на кнопку (Проверить оплату). После чего бот проверит платеж и выдаст вам выбранный товар. Если оплата прошла успешно, то пожалуйста ожидайте выдачи товара.",
    parse_mode="HTML",
    reply_markup=Oplata_Minecraft
    )
    user_id = callback.from_user.id

@dp.callback_query_handler(Text("gotovo"))
async def do_shit_with_gotovo(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    base_doc = qiwi_base.find_one({"_id": user_id})
    if base_doc is not None:
        bill_id = base_doc['bill_id']
        check_p2p = p2p.check(bill_id=bill_id).status
        try:
            if check_p2p == 'PAID':
                await callback.message.delete()
                await callback.message.answer(text='Оплата прошла успешно!\nВ течении 2 дней мы выполним Ваш заказ.')
                qiwi_base.delete_one({"_id": user_id})
            elif check_p2p == 'WAITING':
                await bot.answer_callback_query(callback.id, 'Упс! Оплата еще не найдена. Если Вы оплатили заказ — попробуйте нажать через минуту.', show_alert=True)
            elif check_p2p == 'REJECTED':
                await bot.answer_callback_query(callback.id, 'Ваш заказ отменен или произошла ошибка!', show_alert=True)
        except aiogram.utils.exceptions.InvalidQueryID:
            pass
    else:
        await bot.answer_callback_query(callback.id, 'У вас нет активных платежей.', show_alert=True)
executor.start_polling(dp, skip_updates=True)