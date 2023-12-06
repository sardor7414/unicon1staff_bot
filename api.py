import requests
import json
from environs import Env

env = Env()
env.read_env()

BASE_URL = env.str("URL")

def get_regions():
    url = f"{BASE_URL}/api/regions/"
    res = requests.get(url=url)
    data = res.json()
    return data


def get_district(region_id):
    url = f"{BASE_URL}/api/district/"
    params = {
        'region_id': region_id
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    return data


def get_member(district_id):
    url = f"{BASE_URL}/api/member"
    params = {
        'district_id': district_id
    }
    response = requests.get(url=url, params=params)
    data = response.json()
    return data


def update_member(member_id, data):
    url = f'{BASE_URL}/api/member/{member_id}/'

    # Foydalanuvchidan kelgan ma'lumotlar
    payload = {
        # 'full_name': data.get('full_name', ''),
        # 'phone': data.get('phone', ''),
        'telegram_id': data.get('telegram_id', None),
        # 'district': data.get('district', None)
    }
    # API so'rovni bajarish
    response = requests.patch(url, data=payload)
    return response


def check_member_data(telegram_id):
    url = f"{BASE_URL}/api/checkMember/{telegram_id}/"
    res = requests.get(url=url)
    data = res.json()
    if data['is_registered']:
        return data['member_id']
    else:
        return False


def get_tasks():
    url = f"{BASE_URL}/api/task/"
    res = requests.get(url=url)
    data = res.json()
    return data


def create_task(member, organization, task, location, photo, file_name):
    url = f"{BASE_URL}/api/todo/"
    data = {
        "member": member,
        "organization": organization,
        'location': location,
        'task': task
    }
    response = requests.post(url=url, data=data, files={'photo': (file_name, photo)})
    return response.json()


def todo_by_telegramID(telegram_id):
    url = f"{BASE_URL}/api/getTodo/{telegram_id}/"
    res = requests.get(url=url)
    data = res.json()
    return data




