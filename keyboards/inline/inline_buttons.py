from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api import get_regions, get_district, get_member, get_tasks

# Murojaat yuborish ichki tugmalari
def generate_regions():
    markup = InlineKeyboardMarkup()
    regions = get_regions()
    for region in regions:
        markup.insert(InlineKeyboardButton(text=region['name'], callback_data=f"⭕{region['id']}"))
    return markup

def generate_district(region_id):
    markup = InlineKeyboardMarkup()
    districts = get_district(region_id)
    for district in districts:
        markup.insert(InlineKeyboardButton(text=district['name'], callback_data=f"➖{district['id']}"))
    return markup

def generate_members(district_id):
    markup = InlineKeyboardMarkup()
    members = get_member(district_id)
    for member in members:
        markup.insert(InlineKeyboardButton(text=member['full_name'], callback_data=f"➖{member['id']}"))
    return markup

def generate_task_buttons():
    markup = InlineKeyboardMarkup()
    tasks = get_tasks()
    for task in tasks:
        markup.insert(InlineKeyboardButton(text=task['name'], callback_data=f"➖{task['id']}"))
    return markup
