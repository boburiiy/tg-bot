from aiogram.dispatcher.storage import FSMContext
from loader import db, dp
from keyboards.default.main import cart_markup
from states.main import ShopState
from aiogram import types


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