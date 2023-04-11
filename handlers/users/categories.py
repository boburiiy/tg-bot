from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import *

error_p = 'https://cdn.mos.cms.futurecdn.net/VmSUXc6MrUABpm5a4tH8KK-320-80.jpg'


@dp.message_handler(state=ShopState.categories)
async def cat(message: types.Message, state: FSMContext):
    if not message.text == 'Главное меню':
        try:
            cat_id = db.select_cat(text=message.text)[0]
            if cat_id:
                items = db.select_prod(cat_id=cat_id)
                await state.update_data({"cat_id": cat_id})
                await message.answer('Tanlang:', reply_markup=product_mark(items))
                await ShopState.products.set()
            else:
                await message.answer_photo(photo=error_p, caption='<b><i>Xato qandaydir xatolik qaytadan urinib ko`ring</i></b>', reply_markup=restart)
        except Exception as e:
            await message.answer_photo(photo=error_p)
            await message.answer(text=f"Xatolik: {e}", reply_markup=restart)
    elif message.text == '📥 Корзина':
        items = db.select_all_from_cart(message.from_user.id)
        if items:
            await message.answer(f'Sizning savatcgangiz:\n<b>pasda🔽</b>', reply_markup=cart_markup(items))
            for i in items:
                await message.answer(f"{i[1]} x {i[-2]}")
            await ShopState.cart.set()
        else:
            await message.answer('Sizning savatchangiz bo`m bo`sh')
    else:
        await state.finish()
        await message.answer('Nimadir tanlang', reply_markup=main_menu)
        await ShopState.main.set()
