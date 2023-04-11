from aiogram.dispatcher.storage import FSMContext
from loader import db, dp, bot
from states.main import ShopState
from aiogram import types
from keyboards.default.main import *


@dp.message_handler(text="⬅️ Назад", state=ShopState.category)
async def go_to_main_menu(message: types.Message):
    await message.reply_markup(main_menu)
    await ShopState.main.set()


@dp.message_handler(text="⬅️ Назад", state=ShopState.nums)
async def nums(message: types.Message, state: FSMContext):
    await message.answer('Tanlang', reply_markup=menu)
    await ShopState.category.set()
    # await ShopState.end.set()


@dp.message_handler(text="⬅️ Назад", state=ShopState.products)
async def pros(message: types.Message, state: FSMContext):
    await message.answer('Tanlang', reply_markup=menu)
    await ShopState.category.set()
    # await state.finish()


@dp.message_handler(text="⬅️ Назад", state=ShopState.cart)
async def cart(message: types.Message):
    await message.answer('Tanlang', reply_markup=main_menu)
    await ShopState.main.set()


@dp.message_handler(text="Главное меню", state='*')
async def main(message: types.Message, state=FSMContext):
    await state.finish()
    await message.answer('Nimadir tanlang', reply_markup=main_menu)
    await ShopState.main.set()


@dp.message_handler(text="Меню", state=ShopState.main)
async def a_menu(message: types.Message, state=FSMContext):
    await message.answer('Menu:', reply_markup=menu.add(home))
    await ShopState.category.set()


@dp.message_handler(text="🚖 Оформить заказ", state='*')
async def end(message: types.Message):
    if db.select_all_from_cart(message.from_user.id):
        await message.answer(
            "Itimos telefon raqamingizni qoldiring\nNamuna:+998998889988 - Iltimos shu bilan bir xil qilib yozing")
        await ShopState.end.set()
    else:
        await message.answer('savat bosh')


@dp.message_handler(state=ShopState.end)
async def a_menu(message: types.Message, state: FSMContext):
    if '+998' in message.text and int(message.text.replace("+", '')) > 0:
        await state.update_data({"Num": message.text})
        name = message.from_user.full_name
        id = message.from_user.id
        msg = f"{name} buyurtma qildi\ncart_id:{id}\n"
        items = db.select_all_from_cart(message.from_user.id)
        data = await state.get_data()
        phone_num = data.get('Num')
        if items:
            db.delete_all(id)
            await message.answer('Tekshirildi', reply_markup=menu)
            await ShopState.category.set()
            # await state.finish()
            for i in items:
                msg += f"Buyurtma:{i[1]}\nJami:{i[3]}\nQiymat:{i[2]}\nRaqami:{phone_num}"
        else:
            await message.answer('Sizning savatchangiz bo`m bo`sh')
        await bot.send_message(248549756, msg)
    else:
        await message.answer('Noto`gri raqam +998 yo`q yoki harf bor')


@dp.message_handler(text="📥 Корзина", state='*')
async def cart_use(message: types.Message):
    items = db.select_all_from_cart(message.from_user.id)
    if items:
        await message.answer(f'Sizning savatcgangiz:\n<b>pasda🔽</b>', reply_markup=cart_markup(items))
        for i in items:
            await message.answer(f"{i[1]} x {i[-2]}")
        await ShopState.cart.set()
    else:
        await message.answer('Sizning savatchangiz bo`m bo`sh')
