from keyboards.default.main import cart_markup
from loader import db, dp
from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import *


@dp.message_handler(text="📥 Корзина", state='*')
async def cart_use(message: types.Message):
    items = db.select_all_from_cart(message.from_user.id)
    if items:
        await message.answer(f'Sizning savatcgangiz:\n<b>pasda🔽</b>\n<strong>O`chirmoqchi bo`lgan narsangiz ustiga bosing</strong>', reply_markup=cart_markup(items))
        for i in items:
            await message.answer(f"{i[1]} x {i[-2]}")
        await ShopState.cart.set()
    else:
        await message.answer('Sizning savatchangiz bo`m bo`sh')


@dp.message_handler(text="Clear", state='*')
async def cart_c(message: types.Message):
    user = message.from_user.id
    db.delete_all(user=user)
    await message.answer('O`chirilmoqda')
    await message.answer(f"Muvaffaqiyatli tozalandi", reply_markup=cart_markup(db.select_all_from_cart(user)))


@dp.message_handler(state=ShopState.cart)
async def cart_use(message: types.Message):
    user = message.from_user.id
    items = db.select_all_from_cart(user)
    await message.answer("o'chirmoqchi bo`lgan narsani ustiga bosing", reply_markup=cart_markup(items))
    if items:
        txts = (message.text.split())
        item = ''
        for i in txts:
            if not "x" in i:
                item += i+' '
                print(i)
            else:
                break
        item = item.replace(' ', '')
        db.delete_pro(user=user, item=item)
        await message.answer(f"{item} muvaffaqiyatli o`chirildi", reply_markup=cart_markup(db.select_all_from_cart(user)))
    else:
        await message.answer('Bo`sh')
