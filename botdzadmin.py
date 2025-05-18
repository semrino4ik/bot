import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.client.default import DefaultBotProperties

TOKEN = "7853159809:AAGsR7juazkDv1SR412sIiAKZciYUZtN-AQ"

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# Стан для отримання ДЗ
class HomeworkStates(StatesGroup):
    waiting_for_homework = State()

# Стан для вибору предмета перед фото
class NoteStates(StatesGroup):
    choosing_subject = State()
    waiting_for_photo = State()

# Список предметів
subjects = [
    "Укр мова", "Алгебра", "Геометрія", "Українська літ",
    "Історія Укр", "Фізика", "Зарубіжна", "Географія"
]

# Меню
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Додати домашнє завдання")],
        [KeyboardButton(text="🖼 Додати фото конспектів")]
    ],
    resize_keyboard=True
)

# Клавіатура предметів
subject_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=subj)] for subj in subjects] + [[KeyboardButton(text="🔙 Назад")]],
    resize_keyboard=True
)

# /start
@dp.message(F.text == "/start")
async def start(message: types.Message):
    await message.answer("Привіт, адміне! Обери дію:", reply_markup=main_menu)

# Натискання "Додати домашнє завдання"
@dp.message(F.text == "📘 Додати домашнє завдання")
async def get_homework(message: types.Message, state: FSMContext):
    await message.answer("Надішли текст домашнього завдання:")
    await state.set_state(HomeworkStates.waiting_for_homework)

# Збереження ДЗ
@dp.message(HomeworkStates.waiting_for_homework, F.text)
async def save_homework(message: types.Message, state: FSMContext):
    dz_text = message.text
    os.makedirs(".venv", exist_ok=True)
    with open("C:/Users/Микола Кмицяк/PythonProject1/.venv/dz.txt", "w", encoding="utf-8") as f:
        f.write(dz_text)
    await message.answer("✅ Домашнє завдання збережено!", reply_markup=main_menu)
    await state.clear()

# Натискання "Додати фото конспектів"
@dp.message(F.text == "🖼 Додати фото конспектів")
async def choose_subject(message: types.Message, state: FSMContext):
    await message.answer("Оберіть предмет:", reply_markup=subject_kb)
    await state.set_state(NoteStates.choosing_subject)

# Обробка вибору предмета
@dp.message(NoteStates.choosing_subject, F.text.in_(subjects))
async def subject_chosen(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await message.answer(f"Надішліть фото конспекту для «{message.text}»")
    await state.set_state(NoteStates.waiting_for_photo)

# Обробка фото
@dp.message(NoteStates.waiting_for_photo, F.photo)
async def handle_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject = data.get("subject")

    # Створюємо директорію для предмета
    dir_name = os.path.join("notes", subject.replace(" ", "_"))
    os.makedirs(dir_name, exist_ok=True)

    # Отримання фото
    photo = message.photo[-1]
    photo_id = photo.file_id
    file = await bot.get_file(photo_id)
    file_path = file.file_path

    photo_name = f"{message.from_user.id}_{photo_id}.jpg"
    destination = os.path.join(dir_name, photo_name)
    await bot.download(file, destination)

    await message.answer(f"✅ Фото для «{subject}» збережено!", reply_markup=main_menu)
    await state.clear()

# Назад
@dp.message(NoteStates.choosing_subject, F.text == "🔙 Назад")
async def go_back(message: types.Message, state: FSMContext):
    await message.answer("Повертаємось до головного меню.", reply_markup=main_menu)
    await state.clear()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__== "__main__":
    async def main():
    await dp.start_polling(bot)
