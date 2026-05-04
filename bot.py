import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardRemove


TOKEN = "8665400161:AAFqIt_ZemWkyADWrOYmoCppKU96TlCHCGk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

sizes = {
    "Круглая труба": ["Ø20 мм", "Ø25 мм", "Ø32 мм", "Ø40 мм"],
    "Квадратная труба": ["20x20", "40×40", "60×60", "80×80"],
    "Прямоугольная труба": ["20×40", "40×60", "50×100", "60×120"],

    # УЗБЕКСКИЕ КЛЮЧИ 👇
    "Dumaloq quvur": ["Ø20 mm", "Ø25 mm", "Ø32 mm", "Ø40 mm"],
    "Kvadrat quvur": ["20x20", "40×40", "60×60", "80×80"],
    "To‘rtburchak quvur": ["20×40", "40×60", "50×100", "60×120"]
}

# ---------------- СОСТОЯНИЯ ----------------
class Order(StatesGroup):
    language = State()
    product = State()
    size = State()
    thickness = State()
    volume = State()
    city = State()
    phone = State()

# ---------------- КНОПКИ ----------------
def lang_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🇷🇺 Русский"), KeyboardButton(text="🇺🇿 O‘zbekcha")]
        ],
        resize_keyboard=True
    )


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Прайс"), KeyboardButton(text="🧮 Расчет")],
            [KeyboardButton(text="🌐 Веб-сайт"), KeyboardButton(text="📍 Локация")],
            [KeyboardButton(text="📞 Контакты")]
        ],
        resize_keyboard=True
    )

def main_menu_uz():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💰 Narxlar"), KeyboardButton(text="🧮 Hisoblash")],
            [KeyboardButton(text="🌐 Veb-sayt"), KeyboardButton(text="📍 Lokatsiya")],
            [KeyboardButton(text="📞 Aloqa")]
        ],
        resize_keyboard=True
    )

def size_menu(product, lang="ru"):
    buttons = sizes.get(product, [])
    keyboard = []

    for i in range(0, len(buttons), 2):
        row = [KeyboardButton(text=btn) for btn in buttons[i:i+2]]
        keyboard.append(row)

    if lang == "ru":
        keyboard.append([KeyboardButton(text="✍️ Свой размер")])
        keyboard.append([KeyboardButton(text="⬅️ Назад")])
    else:
        keyboard.append([KeyboardButton(text="✍️ O‘z o‘lchami")])
        keyboard.append([KeyboardButton(text="⬅️ Orqaga")])

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def product_menu(lang="ru"):
    if lang == "ru":
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Круглая труба"),
                    KeyboardButton(text="Квадратная труба"),
                    KeyboardButton(text="Прямоугольная труба")
                ],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Dumaloq quvur"),
                    KeyboardButton(text="Kvadrat quvur"),
                    KeyboardButton(text="To‘rtburchak quvur")
                ],
                [KeyboardButton(text="⬅️ Orqaga")]
            ],
            resize_keyboard=True
        )

def thickness_menu(lang="ru"):
    if lang == "ru":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="1 мм"), KeyboardButton(text="1,5 мм")],
                [KeyboardButton(text="2 мм"), KeyboardButton(text="2,5 мм")],
                [KeyboardButton(text="✍️ Своя толщина")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="1 mm"), KeyboardButton(text="1,5 mm")],
                [KeyboardButton(text="2 mm"), KeyboardButton(text="2,5 mm")],
                [KeyboardButton(text="✍️ O‘z qalinligi")],
                [KeyboardButton(text="⬅️ Orqaga")]
            ],
            resize_keyboard=True
        )

def volume_menu(lang="ru"):
    if lang == "ru":
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="1 тонна"), KeyboardButton(text="3 тонны")],
                [KeyboardButton(text="5 тонн"), KeyboardButton(text="10+ тонн")],
                [KeyboardButton(text="✍️ Свой объем")],
                [KeyboardButton(text="⬅️ Назад")]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="1 tonna"), KeyboardButton(text="3 tonna")],
                [KeyboardButton(text="5 tonna"), KeyboardButton(text="10+ tonna")],
                [KeyboardButton(text="✍️ O‘z hajmi")],
                [KeyboardButton(text="⬅️ Orqaga")]
            ],
            resize_keyboard=True
        )

def price_menu_ru():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Труба"), KeyboardButton(text="Профиль")],
            [KeyboardButton(text="⬅️ Назад")]
        ],
        resize_keyboard=True
    )

def price_menu_uz():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Quvur"), KeyboardButton(text="Profil")],
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

def route_kb(lat, lon, lang="ru"):
    if lang == "ru":
        text = "🚗 Проложить маршрут"
    else:
        text = "🚗 Yo‘nalish qurish"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=text,
                    url=f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}"
                )
            ],
        ]
    )

# ---------------- СТАРТ ----------------

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(Order.language)
    await message.answer("Выберите удобный язык: / O‘zingizga qulay tilni tanlang:", reply_markup=lang_menu())

# ---------------- МЕНЮ ----------------

@dp.message(F.text.in_(["💰 Прайс", "💰 Narxlar"]))
async def price(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "ru")

    if lang == "ru":
        text = "Выберите продукцию:"
        menu = price_menu_ru()
    else:
        text = "Mahsulotni tanlang:"
        menu = price_menu_uz()

    await message.answer(text, reply_markup=menu)
    

@dp.message(F.text.in_(["📞 Контакты", "📞 Aloqa"]))
async def contacts(message: Message):
    await message.answer(
        "📞 +998 71 502-00-90\n📞 +998 90 326-08-08\n📧 atmz_steel@mail.ru"
    )

@dp.message(F.text.in_(["📍 Локация", "📍 Lokatsiya"]))
async def location(message: Message, state: FSMContext):

    lat = 40.916406
    lon = 69.661493

    await message.answer_location(latitude=lat, longitude=lon)

    data = await state.get_data()
    lang = data.get("lang", "ru")

    if lang == "ru":
        text = (
            "📍 Ахангаранский трубный металлургический завод,\n"
            "Ташкентская область, г. Ахангаран, промзона-2\n\n"
            "Нажмите кнопку ниже, чтобы построить маршрут 👇"
        )
    else:
        text = (
            "📍 Ohangaron quvur metallurgiya zavodi,\n"
            "Toshkent viloyati, Ohangaron shahri, promzona-2\n\n"
            "Yo‘nalish qurish uchun quyidagi tugmani bosing 👇"
        )

    await message.answer(text, reply_markup=route_kb(lat, lon, lang))

@dp.message(F.text.in_(["🌐 Веб-сайт", "🌐 Veb-sayt"]))
async def site(message: Message):
    await message.answer("https://atmz.uz/")


# ---------------- ВЫБОР ЯЗЫКА ----------------

@dp.message(Order.language)
async def set_language(message: Message, state: FSMContext):

    if "Русский" in message.text:
        lang = "ru"
        text = "Главное меню:"
        menu = main_menu()
    else:
        lang = "uz"
        text = "Asosiy menyu:"
        menu = main_menu_uz()

    await state.clear()
    await state.update_data(lang=lang)

    await message.answer(text, reply_markup=menu)

# ---------------- ПРАЙС ----------------

@dp.message(F.text.in_(["Труба", "Quvur"]))
async def pipe_price(message: Message):
    file = FSInputFile("atmz_price_pipes.pdf")
    await message.answer_document(file)

@dp.message(F.text.in_(["Профиль", "Profil"]))
async def pipe_price(message: Message):
    file = FSInputFile("atmz_price_profile.pdf")
    await message.answer_document(file)

# ---------------- КНОПКА НАЗАД ----------------

@dp.message(F.text.in_(["⬅️ Назад", "⬅️ Orqaga"]))
async def back_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()

    # если НЕ в процессе — просто меню
    if current_state is None:
        data = await state.get_data()
        lang = data.get("lang", "ru")

        if lang == "ru":
            return await message.answer("Главное меню", reply_markup=main_menu())
        else:
            return await message.answer("Asosiy menyu", reply_markup=main_menu_uz())

    # шаг назад по FSM
    if current_state == Order.product.state:
        data = await state.get_data()
        lang = data.get("lang")

        await state.clear()
        await state.update_data(lang=lang)

        data = await state.get_data()
        lang = data.get("lang", "ru")

        if lang == "ru":
            return await message.answer("Главное меню", reply_markup=main_menu())
        else:
            return await message.answer("Asosiy menyu", reply_markup=main_menu_uz())

    elif current_state == Order.size.state:
        await state.set_state(Order.product)
        data = await state.get_data()
        lang = data.get("lang", "ru")

        text = "Выберите продукцию:" if lang == "ru" else "Mahsulotni tanlang:"

        return await message.answer(text, reply_markup=product_menu(lang))

    elif current_state == Order.volume.state:
        await state.set_state(Order.size)
        data = await state.get_data()
        product = data.get("product")

        return await message.answer(
            "Выберите размер:",
            reply_markup=size_menu(product)
        )

    elif current_state == Order.city.state:
        await state.set_state(Order.volume)
        return await message.answer("Выберите объем:", reply_markup=volume_menu())
    

    elif current_state == Order.phone.state:
        await state.set_state(Order.city)
        return await message.answer("Из какого вы города?", reply_markup=ReplyKeyboardRemove())


    elif current_state == Order.thickness.state:
        await state.set_state(Order.size)
        data = await state.get_data()
        product = data.get("product")

    return await message.answer(
        "Выберите размер:",
        reply_markup=size_menu(product)
    )

# ---------------- РАСЧЕТ ----------------

@dp.message(F.text.in_(["🧮 Расчет", "🧮 Hisoblash"]))
async def calc_start(message: Message, state: FSMContext):

    data = await state.get_data()
    lang = data.get("lang", "ru")

    await state.set_state(Order.product)

    text = "Выберите продукцию:" if lang == "ru" else "Mahsulotni tanlang:"

    return await message.answer(text, reply_markup=product_menu(lang))


@dp.message(Order.product)
async def calc_product(message: Message, state: FSMContext):

    data = await state.get_data()
    lang = data.get("lang", "ru")

    # сохраняем продукт
    await state.update_data(product=message.text)
    await state.set_state(Order.size)

    if lang == "ru":
        texts = {
            "Круглая труба": "Диаметр: 15–377 мм\n\n✔️ В наличии\n✔️ Быстрая отгрузка\n\nВыберите размер:",
            "Квадратная труба": "Размер: 15×15–300×300 мм\n\n✔️ В наличии\n✔️ Прямые поставки\n\nВыберите размер:",
            "Прямоугольная труба": "Размер: 30×20–250×150 мм\n\n✔️ В наличии\n✔️ Гибкие условия\n\nВыберите размер:",
        }
    else:
        texts = {
            "Dumaloq quvur": "Diametr: 15–377 mm\n\n✔️ Mavjud\n✔️ Tez yuklash\n\nO‘lchamni tanlang yoki o‘zingiz yozing:",
            "Kvadrat quvur": "O‘lcham: 15×15–300×300 mm\n\n✔️ Mavjud\n✔️ Qulay shartlar\n\nO‘lchamni tanlang yoki o‘zingiz yozing:",
            "To‘rtburchak quvur": "O‘lcham: 30×20–250×150 mm\n\n✔️ Mavjud\n✔️ Moslashuvchan shartlar\n\nO‘lchamni tanlang yoki o‘zingiz yozing:",
        }

    return await message.answer(
        texts.get(message.text, "Выберите размер:"),
        reply_markup=size_menu(message.text, lang)
    )


@dp.message(Order.size)
async def calc_size(message: Message, state: FSMContext):

    if message.text in ["✍️ Свой размер", "✍️ O‘z o‘lchami"]:
        data = await state.get_data()
        lang = data.get("lang", "ru")

        text = "Введите размер:" if lang == "ru" else "O‘lchamni kiriting:"
        return await message.answer(text)

    await state.update_data(size=message.text)
    await state.set_state(Order.thickness)

    data = await state.get_data()
    lang = data.get("lang", "ru")

    text = "Выберите толщину:" if lang == "ru" else "Qalinlikni tanlang:"

    await message.answer(text, reply_markup=thickness_menu(lang))


@dp.message(Order.thickness)
async def calc_thickness(message: Message, state: FSMContext):

    if message.text in ["✍️ Своя толщина", "✍️ O‘z qalinligi"]:
        data = await state.get_data()
        lang = data.get("lang", "ru")

        text = "Введите толщину:" if lang == "ru" else "Qalinlikni kiriting:"
        return await message.answer(text)

    await state.update_data(thickness=message.text)
    await state.set_state(Order.volume)

    data = await state.get_data()
    lang = data.get("lang", "ru")

    await message.answer(
        "Выберите объем:" if lang == "ru" else "Hajmni tanlang:",
        reply_markup=volume_menu(lang)
    )


@dp.message(Order.volume)
async def calc_volume(message: Message, state: FSMContext):

    if message.text in ["✍️ Свой объем", "✍️ O‘z hajmi"]:
        data = await state.get_data()
        lang = data.get("lang", "ru")

        text = "Введите объем:" if lang == "ru" else "Hajmni kiriting:"
        return await message.answer(text)

    await state.update_data(volume=message.text)
    await state.set_state(Order.city)

    data = await state.get_data()
    lang = data.get("lang", "ru")

    text = "Из какого вы города?" if lang == "ru" else "Qaysi shahardansiz?"

    await message.answer(text, reply_markup=ReplyKeyboardRemove())


@dp.message(Order.city)
async def calc_city(message: Message, state: FSMContext):

    await state.update_data(city=message.text)
    await state.set_state(Order.phone)

    data = await state.get_data()
    lang = data.get("lang", "ru")

    text = "Введите телефон:" if lang == "ru" else "Telefon raqamingizni kiriting:"

    await message.answer(text)


@dp.message(Order.phone)
async def calc_phone(message: Message, state: FSMContext):

    data = await state.get_data()

    text = (
        f"🆕 Новая заявка:\n\n"
        f"📦 Продукт: {data['product']}\n"
        f"📏 Размер: {data['size']}\n"
        f"📐 Толщина: {data.get('thickness','не указана')}\n"
        f"⚖️ Объем: {data['volume']}\n"
        f"🏙 Город: {data['city']}\n"
        f"📞 Телефон: {message.text}"
    )

    data = await state.get_data()
    lang = data.get("lang", "ru")

    if lang == "ru":
        confirm_text = (
            "✅ Заявка отправлена!\n\n"
            "📞 Наш менеджер свяжется с вами в течение 10–15 минут "
            "и уточнит детали заказа."
        )
    else:
        confirm_text = (
            "✅ Buyurtma yuborildi!\n\n"
            "📞 Menejerimiz 10–15 daqiqa ichida siz bilan bog‘lanadi "
            "va buyurtma tafsilotlarini aniqlashtiradi."
        )

    await message.answer(confirm_text)
    
    await bot.send_message(chat_id=8005203449, text=text)

    data = await state.get_data()
    lang = data.get("lang")

    await state.clear()
    await state.update_data(lang=lang)

# ---------------- ЗАПУСК ----------------

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())