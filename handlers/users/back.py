from aiogram.dispatcher.storage import FSMContext
from loader import db, dp, bot
from states.main import ShopState
from aiogram import types
from keyboards.default.main import *


@dp.message_handler(text="⬅️ Назад", state=ShopState.products)
async def go_to_main_menu(message: types.Message):
    await message.answer('Menu', reply_markup=menu)
    await ShopState.categories.set()


@dp.message_handler(text="⬅️ Назад", state=ShopState.nums)
async def go_to_main_menu(message: types.Message):
    await message.answer('Menu', reply_markup=menu)
    await ShopState.categories.set()


@dp.message_handler(text="⬅️ Назад", state=ShopState.cart)
async def go_to_main_menu(message: types.Message):
    await message.answer('Bosh menu', reply_markup=main_menu)
    await ShopState.main.set()


@dp.message_handler(text="Главное меню", state='*')
async def main(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer('Nimadir tanlang', reply_markup=main_menu)
    await ShopState.main.set()


@dp.message_handler(text="Меню", state=ShopState.main)
async def main(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer('Nimadir tanlang', reply_markup=menu.add(home))
    await ShopState.categories.set()


@dp.message_handler(text="🚖 Оформить заказ", state='*')
async def end(message: types.Message):
    if db.select_all_from_cart(message.from_user.id):
        await message.answer("Itimos telefon raqamingizni qoldiring\nTugmani bosing", reply_markup=phone_num)
        await ShopState.phone.set()
    else:
        await message.answer('savat bosh')


@dp.message_handler(content_types=ContentType.CONTACT, state=ShopState.phone)
async def process_contact(message: Message):
    maybe = db.select_all_from_cart(message.from_user.id)
    phone_number = message.contact.phone_number
    msg = ''
    if maybe:
        for i in maybe:
            msg += f'Buyurtma: {i[1]}\nJami summa: {i[2]}\nMiqdori: {i[3]}\n1 donasi narxi {i[4]}\n----------------\n'
        await message.answer(f'Buyurtma qa`bul qilindi\n{msg}')
        await message.answer(f"Sizning telefon raqaming: {phone_number}", reply_markup=menu)
        user = message.from_user.id
        from data.config import ADMINS
        await bot.send_message(ADMINS[0], f'Buyurtma:\n{msg}\n\nTelefon raqami: {phone_number}')
        db.delete_all(user=user)
        await ShopState.categories.set()
    else:
        await message.answer('savat bosh')
