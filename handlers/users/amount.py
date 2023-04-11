from aiogram import types
from states.main import ShopState
from loader import dp, db
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import *
from utils.db_api.sqlite import *


@dp.message_handler(state=ShopState.nums)
async def get_products(message: types.Message, state: FSMContext):
    data = await state.get_data()
    id = message.from_user.id
    count = int(message.text)
    if count > 0:
        try:
            item = data["product_name"]
            price = int(data["price"])
            total_price = price*count
            maybe = db.selected_select(item=item, user=id)
            summary = f'{item} {count}ta \nnarxi: {total_price}\n1 donasi:{price}'
            print(message.text)
            if maybe:
                print(maybe)
                await message.answer(f'Savatga qo`shildi\n{summary}', reply_markup=menu)
                db.update_cart(
                    total_price+maybe[-3], count+maybe[-2], id, item)
                await ShopState.categories.set()
            else:
                await message.answer(f'Savatga yangi magsulot qo`shildi\n{summary}', reply_markup=menu)
                db.add_to_cart(
                    id, item, data['price']*int(count), count, price)
                await ShopState.categories.set()
        except Exception as e:
            pass
            # await message.send
