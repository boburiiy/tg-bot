from aiogram.types import *
back = KeyboardButton("⬅️ Назад")
home = KeyboardButton('Главное меню')
restart = ReplyKeyboardMarkup(keyboard=[["/start"]])

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("Меню"), KeyboardButton("📥 Корзина")],
        [KeyboardButton("🚖 Оформить заказ")]
    ], resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🍔 Бургер"), KeyboardButton("🌭 Хот-Дог")],
        [KeyboardButton('🍗 Куриные крылышки(острые)')],
        [KeyboardButton("🍹 Напитки"), KeyboardButton("🍟 Дополнительно")]
    ], resize_keyboard=True
)

keypad = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(1), KeyboardButton(2), KeyboardButton(3)],
        [KeyboardButton(4), KeyboardButton(5), KeyboardButton(6)],
        [KeyboardButton(7), KeyboardButton(8), KeyboardButton(9)],
        [home, back]
    ], resize_keyboard=True
)

phone_num = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton('Tasdiqlash', request_contact=True)
]])


def cart_markup(items):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for i in items:
        markup.insert(KeyboardButton(f"{i[1]} x {i[-2]}"))
    markup.row(back, home)
    markup.add(KeyboardButton('Clear'))
    return markup


def product_mark(items):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        markup.add(KeyboardButton(item[2]))
    markup.row(back, home)
    return markup
