from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import product_mark, restart

error_p = 'https://cdn.mos.cms.futurecdn.net/VmSUXc6MrUABpm5a4tH8KK-320-80.jpg'


@dp.message_handler(state=ShopState.menu)
async def cat(message: types.Message, state: FSMContext):
    try:
        cat_id = db.select_cat(text=message.text)[0]
        if cat_id:
            items = db.select_prod(cat_id=cat_id)
            await state.update_data(
                {"cat_id": cat_id}
            )
            await message.answer('Tanlang:', reply_markup=product_mark(items))
            await ShopState.products.set()
        else:
            await message.answer_photo(photo=error_p, caption='<b><i>Xato qandaydir xatolik qaytadan urinib ko`ring</i></b>', reply_markup=restart)
    except Exception as e:
        await message.answer_photo(photo=error_p)
        await message.answer(text=f"Xatolik: {e}", reply_markup=restart)
