from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from .db_setup import create_user, select_users, create_product

router = Router()


# Foydalanuvchini ro'yxatdan o'tkazish holatlari
class Register(StatesGroup):
    name = State()
    surname = State()


# Mahsulot qo'shish holatlari
class AddProduct(StatesGroup):
    name = State()
    price = State()


# Foydalanuvchini kutib olish va /start komandasi uchun handler
@router.message(CommandStart())
async def greet_user(message: Message):
    await message.answer("Assalomu alaykum! Botga xush kelibsiz! Men sizga yordam bera olishim mumkin.")


# `/ism` komandasi uchun handler
@router.message(Command(commands=["ism"]))
async def ask_name(message: Message, state: FSMContext):
    await message.answer("Iltimos, ismingizni kiriting:")
    await state.set_state(Register.name)


# Foydalanuvchidan ismni qabul qilish
@router.message(Register.name)
async def register_name(message: Message, state: FSMContext):
    user_name = message.text
    await message.answer(f"Salom, {user_name}!")
    await state.clear()


# Foydalanuvchilar ro'yxatini ko'rsatish uchun handler
@router.message(Command(commands=["show_users"]))
async def show_users(message: Message):
    users = await select_users()
    if users:
        result = "\n".join(
            [f"ID: {user[0]}, Ism: {user[1]}, Familiya: {user[2]}" for user in users]
        )
        await message.answer(f"Foydalanuvchilar ro'yxati:\n{result}")
    else:
        await message.answer("Hech qanday foydalanuvchi topilmadi.")


# Mahsulot qo'shishni boshlash uchun handler
@router.message(Command("create_product"))
async def start_adding_product(message: Message, state: FSMContext):
    await state.set_state(AddProduct.name)
    await message.answer("Mahsulot nomini kiriting:")


# Mahsulot nomini qabul qilish
@router.message(AddProduct.name)
async def add_product_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AddProduct.price)
    await message.answer("Mahsulot narxini kiriting:")


# Mahsulot narxini qabul qilish va ma'lumotlarni bazaga saqlash
@router.message(AddProduct.price)
async def add_product_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    # Mahsulotni bazaga qo'shish
    await create_product(name=data['name'], price=data['price'])
    await message.answer(f"Mahsulot qo'shildi!\nNomi: {data['name']}\nNarxi: {data['price']} so'm")

    # Holatni tugatish
    await state.clear()


# Noto'g'ri komanda yuborilganda handler
@router.message()
async def unknown_command(message: Message):
    await message.answer("Bu komanda topilmadi. Yordam uchun /help komandasini yuboring.")
