import requests
import json

ACCESS_TOKEN = 'fbc4d15dfbc4d15dfbc4d15d90f8e7b200ffbc4fbc4d15d9cf4e4335ed2494b10195ea5'
USER_ID = '190868'  # Новый user_id
VERSION = '5.131'


def get_user_info(user_id):
    try:
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params={
                'user_ids': user_id,
                'fields': 'followers_count',
                'access_token': ACCESS_TOKEN,
                'v': VERSION
            }
        )
        data = response.json()
        if 'response' in data:
            user = data['response'][0]
            user_info = {
                'id': user['id'],
                'full_name': f"{user['first_name']} {user['last_name']}",
                'followers_count': user.get('followers_count', 'Не указано')
            }
            print(f"ID: {user_info['id']}")
            print(f"ФИО: {user_info['full_name']}")
            print(f"Количество фолловеров: {user_info['followers_count']}")
            return user_info
        else:
            print(f"Ошибка получения информации о пользователе: {data['error']['error_msg']}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return None


def get_followers(user_id):
    try:
        response = requests.get(
            'https://api.vk.com/method/users.getFollowers',
            params={
                'user_id': user_id,
                'access_token': ACCESS_TOKEN,
                'v': VERSION
            }
        )
        data = response.json()
        if 'response' in data:
            followers_count = data['response']['count']
            print(f"Количество фолловеров: {followers_count}")
            return {'followers_count': followers_count}
        else:
            print(f"Ошибка получения фолловеров: {data['error']['error_msg']}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return None


def get_subscriptions(user_id):
    try:
        response = requests.get(
            'https://api.vk.com/method/users.getSubscriptions',
            params={
                'user_id': user_id,
                'access_token': ACCESS_TOKEN,
                'v': VERSION
            }
        )
        data = response.json()
        if 'response' in data:
            subscriptions_info = {}

            if 'users' in data['response']:
                users_count = data['response']['users']['count']
                subscriptions_info['users_count'] = users_count
                print(f"Количество подписок (пользователи): {users_count}")
            else:
                print(f"Ошибка: 'users.count' отсутствует в ответе")

            if 'groups' in data['response']:
                groups_count = data['response']['groups']['count']
                subscriptions_info['groups_count'] = groups_count
                print(f"Количество подписок (группы): {groups_count}")
            else:
                print(f"Ошибка: 'groups.count' отсутствует в ответе")

            return subscriptions_info
        else:
            print(f"Ошибка получения подписок: {data['error']['error_msg']}")
    except Exception as e:
        print(f"Ошибка: {e}")
    return None


def save_data_to_json(user_info, followers_info, subscriptions_info):
    # Сохраняем данные в JSON файл
    data = {
        'user_info': user_info,
        'followers_info': followers_info,
        'subscriptions_info': subscriptions_info
    }

    with open('vk_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("\nДанные успешно сохранены в vk_data.json")


def main():
    # Проверяем, является ли USER_ID числом или строкой
    user_id = USER_ID
    if isinstance(user_id, str) and user_id.isdigit():
        user_id = int(user_id)  # Если это строка с цифрами, преобразуем в int

    # Получаем информацию о пользователе
    user_info = get_user_info(user_id)
    if user_info:
        print("\n=== Фолловеры ===")
        followers_info = get_followers(user_id)

        print("\n=== Подписки ===")
        subscriptions_info = get_subscriptions(user_id)

        # Сохраняем все данные в JSON файл
        save_data_to_json(user_info, followers_info, subscriptions_info)


if __name__ == '__main__':
    main()