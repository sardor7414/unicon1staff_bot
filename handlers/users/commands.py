import asyncio
import json
from aiogram.dispatcher import FSMContext
from aiogram.types import ChatActions
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.builtin import Text, CallbackQuery
from keyboards.inline.inline_buttons import generate_regions, generate_district, generate_members, \
    generate_task_buttons
from keyboards.default.default_buttons import button_send_location
from data.config import ADMINS
from states.states import AppealState
from api import check_member_data, update_member, create_task, todo_by_telegramID


# Vazifa qo'shish, registratsiya
@dp.message_handler(Text(equals="📝Vazifa qo'shish"))
async def reaction_to_start(message: types.Message, state:  FSMContext):
    await message.delete()
    check_tg_id = check_member_data(message.from_user.id)
    if not check_tg_id:
        await message.answer(
            f"Hurmatli, <b>{message.from_user.full_name}</b>,Siz vazifa qo'shish uchun Xodimlar ro'yxatidan "
            f"o'z ism-sharifingizni topib ma'lumotlaringizni yangilashingiz kerak "
            f"Ma'lumotlarni yangilash uchun o'z viloyatingizni  tanlang ⬇️", reply_markup=generate_regions(),
            parse_mode='html'
        )
    else:
        member_id = check_member_data(message.from_user.id)
        await state.update_data({
            'member_id': member_id
        })
        await message.answer("Tashrif buyurgan tashkilotingizni kiriting: ")
        await AppealState.organization.set()


@dp.callback_query_handler(Text(startswith="⭕"))
async def reaction_to_region(call: CallbackQuery, state: FSMContext):
    region_id = call.data[1:]
    await state.update_data({
        'region_id': region_id
    })
    await call.message.answer("Tumanni tanlang ⬇️", reply_markup=generate_district(region_id))
    await AppealState.district_id.set()


@dp.callback_query_handler(state=AppealState.district_id)
async def reaction_to_district(call: CallbackQuery, state: FSMContext):
    district_id = call.data[1:]
    await state.update_data({
        'district_id': district_id
    })
    await call.message.answer("Xodimni tanlang ⬇️", reply_markup=generate_members(district_id))
    await AppealState.member_id.set()


@dp.callback_query_handler(state=AppealState.member_id)
async def reaction_to_member(call: CallbackQuery, state: FSMContext):
    member_id = call.data[1:]
    await state.update_data({
        'member_id': member_id
    })
    data = await state.get_data()
    region_id = data['region_id']
    district_id = data['district_id']
    member_id = data['member_id']
    new_data = update_member(
        member_id=member_id,
        data={"telegram_id": call.from_user.id}
    )
    await state.finish()
    await call.message.answer("✅ Ma'lumotlar yangilandi")


# Tashkilotni ushlash
@dp.message_handler(state=AppealState.organization,content_types='text')
async def reaction_to_organization(message: types.Message, state: FSMContext):
    organization = message.text
    if organization=='Back':
        pass
    else:
        await state.update_data({
            'organization': organization
        })
        await message.answer("Bajarilgan ishni tanlang ⬇️", reply_markup=generate_task_buttons())
        await AppealState.task_id.set()

@dp.callback_query_handler(state=AppealState.task_id)
async def reaction_to_task(call: CallbackQuery, state: FSMContext):
    task_id = call.data[1:]
    await state.update_data({
        "task_id": task_id
    })
    await call.message.answer("Hudud joylashuvini yuboring ⬇️", reply_markup=button_send_location())
    await AppealState.location.set()


@dp.message_handler(content_types=types.ContentType.LOCATION, state=AppealState.location)
async def reaction_to_location(message: types.Message, state: FSMContext):
    location = message.location
    await state.update_data({
        "latitude": location.latitude,
        'longitude':location.longitude
    })
    await message.answer("✅Joylashuv qabul qilindi! "
                         "Jarayondan fotolavha yuklang ⏏️", reply_markup=types.ReplyKeyboardRemove())
    await AppealState.image.set()

# Photo URL
@dp.message_handler(content_types=types.ContentType.PHOTO, state=AppealState.image)
async def handle_photo(message: types.Message, state: FSMContext):
    # Foydalanuvchidan kelgan rasmni saqlash
    photo_id = message.photo[-1].file_id
    photo_file = await bot.get_file(photo_id)
    photo_url = bot.get_file_url(file_path=photo_file.file_path)
    file_name = photo_file.file_path.split('/')[-1]
    await state.update_data(image=photo_url)
    await message.answer("✅Rasm qabul qilindi. Ma'lumotlaringiz rahbariyatga yuborildi! "
                         "Yangi vazifalarni qo'shishni unutmang")

    data = await state.get_data()
    member_id = data['member_id']
    organization = data['organization']
    task_id = data['task_id']
    # photo = data['image']

    await state.finish()
    create_task(
        member=member_id,
        organization=organization,
        task=task_id,
        latitude=data['latitude'],
        longitude=data['longitude'],
        photo=photo_url)


@dp.message_handler(Text(equals="📊Mening ishlarim"))
async def reaction_to_mytodo(message: types.Message):
    todos = todo_by_telegramID(message.from_user.id)
    for todo in todos:
        await message.answer(f"""
        <b>👤Xodim: {message.from_user.full_name}, ID: {todo['member']}</b>
        ◾️Vazifa ID: {todo['id']}
        ◾️Tashkilot nomi: {todo['organization']}
        ◾️Bajarilgan ish: {todo['task']}
""")