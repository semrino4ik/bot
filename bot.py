from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types.input_file import FSInputFile
from aiogram.types import LabeledPrice, PreCheckoutQuery
import asyncio
import random
import os
import glob
import json
from datetime import datetime,timedelta
def is_subscription_active(user_id):
    date_str = paid_users.get(str(user_id))
    if not date_str:
        return False
    paid_date = datetime.fromisoformat(date_str)
    return datetime.now() < paid_date + timedelta(days=30)

PAID_USERS_FILE = "paid_users.json"
def load_paid_users():
    if os.path.exists(PAID_USERS_FILE):
        with open(PAID_USERS_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_paid_users():
    with open(PAID_USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(paid_users, f)

paid_users = load_paid_users()

TOKEN = '7892675445:AAF831rV9Wbs-GMyLeCwegyv3MxiaUoCuaY'
PROVIDER_TOKEN = '1725141586:TEST:b7bb9606f080d36b4d4db5c5714a0168d7fcacfb'  # Твій токен
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()
paid_users = {}

# Далі — твій код з обробниками
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📚Домашнє завдання"), KeyboardButton(text="📝Конспекти")],
        [KeyboardButton(text="📆 Розклад уроків"), KeyboardButton(text="🪙 Підкинути монетку")],
        [KeyboardButton(text="🗓 Коли вже вихідні"), KeyboardButton(text="Оновити д.з")],
        [KeyboardButton(text="Залишити відгук"), KeyboardButton(text="💳 Купити підписку")]
    ],
    resize_keyboard=True
)

@dp.message(F.text == "📚Домашнє завдання")
async def handle_dz(message: Message):
    if message.from_user.id not in paid_users:
        await message.answer("🔒 Щоб побачити домашнє завдання, купи підписку — 50 зірок. Натисни 💳 Купити підписку.")
        return

    if os.path.exists("C:/Users/Микола Кмицяк/PythonProject1/.venv/dz.txt"):
        with open("C:/Users/Микола Кмицяк/PythonProject1/.venv/dz.txt", "r", encoding="utf-8") as f:
            dz_text = f.read()
        await message.answer(f"<b>Домашнє завдання:</b>\n\n{dz_text}")


# Підменю предметів

subjects_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Укр мова"), KeyboardButton(text="Алгебра")],
        [KeyboardButton(text="Геометрія"), KeyboardButton(text="Українська літ")],
        [KeyboardButton(text="Історія Укр"), KeyboardButton(text="Фізика")],
        [KeyboardButton(text="Зарубіжна"), KeyboardButton(text="Географія")],
        [KeyboardButton(text=" 🔙Назад до меню")]
    ],
    resize_keyboard=True
)

class NoteStates(StatesGroup):
    choosing_subject = State()

# Кнопка " 📝Конспекти"


@dp.message(F.text == "📝Конспекти")
async def handle_notes(message: Message, state: FSMContext):
    if message.from_user.id not in paid_users:
        await message.answer("🔒 Щоб переглядати конспекти, купи підписку — 50 зірок. Натисни 💳 Купити підписку.")
        return

    await message.answer("Оберіть предмет:",reply_markup=subjects_keyboard)
    await state.set_state(NoteStates.choosing_subject)



@dp.message(NoteStates.choosing_subject)
async def show_notes_for_subject(message: Message, state: FSMContext):
    subject = message.text.strip()

    if subject == "🔙Назад до меню":
        await message.answer("Повертаємось до головного меню 👇", reply_markup=main_menu)
        await state.clear()
        return

    # Формуємо шлях до папки з фото
    subject_folder = subject.replace(" ", "_")
    folder_path = f"notes/{subject_folder}"

    if not os.path.exists(folder_path):
        await message.answer(f"❌ Для предмета <b>{subject}</b> ще немає конспектів.")
        return

    files = os.listdir(folder_path)
    image_files = [f for f in files if f.endswith(".jpg") or f.endswith(".png")]

    if not image_files:
        await message.answer(f"❌ Для предмета <b>{subject}</b> ще немає фото конспектів.")
        return

    for image_file in image_files:
        photo_path = os.path.join(folder_path, image_file)
        photo_inputfile = FSInputFile(photo_path)  # правильний клас
        await bot.send_photo(chat_id=message.chat.id, photo=photo_inputfile)

    await message.answer("📚 Ось усі доступні конспекти!", reply_markup=subjects_keyboard)

# Ініціалізація бота


# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привіт! Обери дію з меню нижче 👇", reply_markup=main_menu)

# Обробка кожної кнопки

@dp.message(F.text == "📆 Розклад уроків")
async def handle_schedule(message: Message):
    await message.answer("1.Урок 8:00–8:45 перерва 15хв            2.Урок 9:00–9:45 перерва 15хв                  3.Урок 10:00–10:45 перерва 15хв               4.Урок 11:00–11:45 перерва 15хв              5.Урок 12:00–12:45 перерва 15хв               6.Урок 13:00–13:45 перерва 15хв              7.Урок 13:50–14:35 перерва 5хв                  8.Урок 14:40–15:25 перерва 5хв")

@dp.message(F.text == "🪙 Підкинути монетку")
async def handle_coin(message: Message):
    result = random.choice(["Орёл 🦅", "Решка 💰"])
    await message.answer(f"Випало: {result}")

@dp.message(F.text == "🗓 Коли вже вихідні")
async def handle_weekend(message: Message):
    now = datetime.now()

    # Вихідні (субота)
    weekday = now.weekday()  # 0 — понеділок, 5 — субота
    if weekday < 5:
        weekend = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=(5 - weekday))
        time_to_weekend = weekend - now
        days = time_to_weekend.days
        hours, remainder = divmod(time_to_weekend.seconds, 3600)
        minutes = remainder // 60
        text_weekend = f"До вихідних залишилось {days} днів, {hours} годин і {minutes} хвилин!"
    else:
        text_weekend = "🎉 Вже вихідні! Насолоджуйся!"

    # Літні канікули — 6 червня (можеш змінити час)
    summer_date = datetime(now.year, 6, 6, 0, 0, 0)
    if now >= summer_date:
        text_summer = "☀️ Літні канікули вже розпочались! Ура!"
    else:
        time_to_summer = summer_date - now
        days = time_to_summer.days
        hours, remainder = divmod(time_to_summer.seconds, 3600)
        minutes = remainder // 60
        text_summer = f"До літніх канікул залишилось {days} днів, {hours} годин і {minutes} хвилин!"

    # Відповідь
    await message.answer(f"{text_weekend}\n\n{text_summer}")

@dp.message(F.text == "Оновити д.з")
async def handle_update_dz(message: Message, state: FSMContext):
    chat_id = message.chat.id

    # 1. Спроба очистити повідомлення (тільки якщо бот має права)
    try:
        # Видаляємо останні 20 повідомлень (можеш змінити)
        for i in range(message.message_id, message.message_id - 20, -1):
            try:
                await bot.delete_message(chat_id, i)
            except:
                continue  # Деякі повідомлення можуть бути недоступні для видалення
    except Exception as e:
        await message.answer("⚠️ Не вдалося очистити чат повністю.")

    # 2. Очистити FSM стан
    await state.clear()

    # 3. Надіслати повідомлення після "перезапуску"
    await bot.send_message(chat_id, "🔄 Бот оновлено! Обери дію:", reply_markup=main_menu)

@dp.message(F.text == "Залишити відгук")
async def handle_events(message: Message):
    await message.answer("у цьому каналі можете залишити відгук:https://t.me/+OwL1YBWfqatlYWQ6")
from aiogram.types import LabeledPrice, PreCheckoutQuery, ShippingOption, ShippingQuery, InlineKeyboardMarkup, InlineKeyboardButton

PROVIDER_TOKEN = '1725141586:TEST:b7bb9606f080d36b4d4db5c5714a0168d7fcacfb'  # Твій тестовий токен

@dp.message(F.text == "💳 Купити підписку")
async def pay_sub(message: Message):
    prices = [LabeledPrice(label="Місячна підписка", amount=5000)]  # 50 зірок = 50.00 * 100

    await bot.send_invoice(
        chat_id=message.chat.id,
        title="Підписка на бота",
        description="Доступ до домашнього завдання та конспектів на 1 місяць",
        payload="monthly_sub",
        provider_token=PROVIDER_TOKEN,
        currency="UAH",
        prices=prices,
        start_parameter="subscription"
    )

@dp.pre_checkout_query()
async def checkout(pre_checkout_q: PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)

@dp.message(F.successful_payment)
async def got_payment(message: Message):
    user_id = message.from_user.id
    paid_users.add(user_id)
    await message.answer("✅ Дякуємо за оплату! Доступ до конспектів і домашнього завдання відкрито.")
# Запуск
@dp.message(Command("status"))
async def status(message: Message):
    user_id = message.from_user.id
    if is_subscription_active(user_id):
        date_str = paid_users.get(str(user_id))
        paid_date = datetime.fromisoformat(date_str)
        expires = paid_date + timedelta(days=30)
        await message.answer(f"✅ Ваша підписка активна до <b>{expires.strftime('%d.%m.%Y %H:%M')}</b>")
    else:
        await message.answer("❌ У вас немає активної підписки.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
