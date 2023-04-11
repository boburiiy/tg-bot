from aiogram import types
from states.main import ShopState
from loader import dp, db
# from keyboards.default.main import _replymark
from keyboards.default.main import keypad
from aiogram.dispatcher.storage import FSMContext
from keyboards.default.main import restart, keypad, menu

error_p = 'https://cdn.mos.cms.futurecdn.net/VmSUXc6MrUABpm5a4tH8KK-320-80.jpg'
@dp.message_handler(state=ShopState.products)
async def cat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    cat_id = data.get('cat_id')
    try:
        item = db.select_prod(name=message.text)
        if item:
            price = item[0][3]
            await message.answer_photo(photo=item[0][-1], caption=f"<b>{message.text}</b>\n<b><i>Narxi:</i><code>{price}</code></b>")
            await message.answer('Qancha xohlaysiz', reply_markup=keypad)
            await state.update_data(
                {
                    'product_name': message.text,
                    'price': price
                }
            )
            await ShopState.nums.set()
        else:
            await message.answer_photo(photo=error_p)
            await message.answer('Xato qandaydir xatolik qaytadan urinib ko`ring', reply_markup=restart)
    except Exception as e:
        await message.answer(f"Xato:{e}", reply_markup=restart)


@dp.message_handler(state=ShopState.nums)
async def amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if int(message.text) > 0:
        try:
            item = data.get('product_name')
            amount = int(message.text)
            price = int(data.get("price"))
            total_amount = amount * price
            a = db.selected_select(item, message.from_user.id)
            if a:
                last_cua = int(a[-3])
                last_cou = int(a[-2])
                db.update_cart(
                    count=amount+last_cou, amount=total_amount+last_cua, user=message.from_user.id, item=item)
            else:
                db.add_to_cart(message.from_user.id, item,
                               total_amount, amount, price)
            await message.answer(f'Savatga qo`shildi:\n{message.text}ta {item}\nnarxi:{price}\njami:{total_amount}', reply_markup=menu)
            await ShopState.category.set()
        except Exception as e:
            await message.answer_photo(
                photo=error_p, caption=f'<b>Xatolik\nBad request:\n{e}</b>')
    # elif message.text in "⬅️ Назад":
    #     await message.answer_animation('Tanlang', reply_markup=menu)
    #     await ShopState.products.set()
    else:
        await message.answer_photo(photo="https://cdn.mos.cms.futurecdn.net/VmSUXc6MrUABpm5a4tH8KK-320-80.jpg", caption='Iltimos butun son kiriting')
