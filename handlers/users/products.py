from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import *


@dp.message_handler(state=ShopState.products)
async def get_products(message: types.Message, state: FSMContext):
    id = message.from_user.id
    try:
        prod = db.select_prod(name=message.text)[0]
        price = prod[3]
        await message.answer_photo(photo=prod[-1], caption=f'<b>{prod[2]}</b>\n<strong>Narxi:{price}</strong>', reply_markup=keypad)
        await ShopState.nums.set()
        await state.update_data(
            {
                'product_name': message.text,
                'price': price
            }
        )
    except Exception as e:
        await message.answer(e)
