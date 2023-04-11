from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import producds_markup


@dp.message_handler(state=ShopState.category)
async def get_products(message: types.Message, state: FSMContext):
    id = message.from_user.id
    cat = db.select_cat(text=message.text)
    await message.answer(message.text)
    if cat:
        await message.answer(cat[0])
        product = db.select_prod(int(*cat))
        await message.answer(product)
    await message.answer('categoriya yo`q')
