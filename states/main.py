from aiogram.dispatcher.filters.state import State, StatesGroup


class ShopState(StatesGroup):
    main = State()
    categories = State()
    products = State()
    nums = State()
    cart = State()
    phone = State()
    check = State()
