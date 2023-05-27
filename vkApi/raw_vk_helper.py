import urllib.request
import json
import os


def get_token(filename: str):
    with open(filename, 'r') as json_file:
        file = json.load(json_file)
        return file["token"]


# Токен доступа VK API
access_token = get_token("token.json")


def get_friends(user_id):
    # URL для запроса списка друзей
    friends_url = f'https://api.vk.com/method/friends.get?user_id={user_id}&access_token={access_token}&v=5.131'

    # Выполняем запрос списка друзей
    friends_response = urllib.request.urlopen(friends_url)
    friends_data = json.loads(friends_response.read())

    # Проверяем, есть ли ошибка в ответе
    if 'error' in friends_data:
        print('Ошибка при выполнении запроса списка друзей:', friends_data['error']['error_msg'])
    else:
        # Получаем список друзей
        friends = friends_data['response']['items']

        # Формируем список идентификаторов друзей для запроса их информации
        friends_ids = ','.join(str(friend_id) for friend_id in friends)

        # URL для запроса информации о друзьях
        users_url = f'https://api.vk.com/method/users.get?user_ids={friends_ids}&access_token={access_token}&v=5.131'

        # Выполняем запрос информации о друзьях
        users_response = urllib.request.urlopen(users_url)
        users_data = json.loads(users_response.read())

        # Проверяем, есть ли ошибка в ответе
        if 'error' in users_data:
            print('Ошибка при выполнении запроса информации о друзьях:', users_data['error']['error_msg'])
        else:
            # Получаем список профилей друзей
            profiles = users_data['response']
            # Выводим имя и фамилию каждого друга
            print(f"Всего {len(profiles)} друзей:")
            for profile in profiles:
                friend_id = profile['id']
                first_name = profile['first_name']
                last_name = profile['last_name']
                print(f'ID: {friend_id}, {first_name} {last_name}')


def get_user_photos(user_id):
    # URL для запроса списка фотографий пользователя
    photos_url = f'https://api.vk.com/method/photos.get?owner_id={user_id}&album_id=profile&rev=1&extended=1' \
                 f'&photo_sizes=1&access_token={access_token}&v=5.131 '

    # Выполняем запрос списка фотографий пользователя
    photos_response = urllib.request.urlopen(photos_url)
    photos_data = json.loads(photos_response.read())

    # Проверяем, есть ли ошибка в ответе
    if 'error' in photos_data:
        print('Ошибка при выполнении запроса списка фотографий:', photos_data['error']['error_msg'])
    else:
        # Получаем список фотографий
        photos = photos_data['response']['items']

        # Создаем папку для сохранения фотографий
        folder_name = f'user_{user_id}_photos'
        os.makedirs(folder_name, exist_ok=True)

        # Скачиваем фотографии
        print(f"Всего {len(photos)} фотографий:")
        for photo in photos:
            photo_id = photo['id']
            photo_sizes = photo['sizes']
            # Выбираем фотографию максимального размера
            max_size = max(photo_sizes, key=lambda x: x['width'])
            photo_url = max_size['url']
            photo_filename = f'{photo_id}.jpg'
            photo_path = os.path.join(folder_name, photo_filename)
            urllib.request.urlretrieve(photo_url, photo_path)
            print(f'Скачана фотография: {photo_filename}')

        print(f'Фотографии сохранены в папку: {folder_name}')


def like_all_posts(user_id):
    # URL для запроса списка записей пользователя
    posts_url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&access_token={access_token}&v=5.131'

    # Выполняем запрос списка записей пользователя
    posts_response = urllib.request.urlopen(posts_url)
    posts_data = json.loads(posts_response.read())

    # Проверяем, есть ли ошибка в ответе
    if 'error' in posts_data:
        print('Ошибка при выполнении запроса списка записей:', posts_data['error']['error_msg'])
    else:
        # Получаем список записей
        posts = posts_data['response']['items']

        # Ставим лайки на записи
        print(f"Ставим лайки на все записи пользователя {user_id}:")
        for post in posts:
            post_id = post['id']

            # URL для запроса постановки лайка
            like_url = f'https://api.vk.com/method/likes.add?type=post&owner_id={user_id}&item_id={post_id}&access_token={access_token}&v=5.131'

            # Выполняем запрос постановки лайка
            like_response = urllib.request.urlopen(like_url)
            like_data = json.loads(like_response.read())

            # Проверяем, есть ли ошибка в ответе
            if 'error' in like_data:
                print(f'Ошибка при постановке лайка на запись {post_id}:', like_data['error']['error_msg'])
            else:
                print(f'Лайк поставлен на запись {post_id}')

        print('Постановка лайков завершена')


def unlike_all_posts(user_id):
    # URL для запроса списка записей пользователя
    posts_url = f'https://api.vk.com/method/wall.get?owner_id={user_id}&access_token={access_token}&v=5.131'

    # Выполняем запрос списка записей пользователя
    posts_response = urllib.request.urlopen(posts_url)
    posts_data = json.loads(posts_response.read())

    # Проверяем, есть ли ошибка в ответе
    if 'error' in posts_data:
        print('Ошибка при выполнении запроса списка записей:', posts_data['error']['error_msg'])
    else:
        # Получаем список записей
        posts = posts_data['response']['items']

        # Снимаем лайки со записей
        print(f"Снимаем лайки со всех записей пользователя {user_id}:")
        for post in posts:
            post_id = post['id']

            # URL для запроса снятия лайка
            unlike_url = f'https://api.vk.com/method/likes.delete?type=post&owner_id={user_id}&item_id={post_id}&access_token={access_token}&v=5.131'

            # Выполняем запрос снятия лайка
            unlike_response = urllib.request.urlopen(unlike_url)
            unlike_data = json.loads(unlike_response.read())

            # Проверяем, есть ли ошибка в ответе
            if 'error' in unlike_data:
                print(f'Ошибка при снятии лайка с записи {post_id}:', unlike_data['error']['error_msg'])
            else:
                print(f'Лайк снят с записи {post_id}')

        print('Снятие лайков завершено')


def get_friends_statuses(user_id):
    # URL для запроса списка друзей пользователя
    friends_url = f'https://api.vk.com/method/friends.get?user_id={user_id}&access_token={access_token}&v=5.131'

    # Выполняем запрос списка друзей пользователя
    friends_response = urllib.request.urlopen(friends_url)
    friends_data = json.loads(friends_response.read())

    # Проверяем, есть ли ошибка в ответе
    if 'error' in friends_data:
        print('Ошибка при выполнении запроса списка друзей:', friends_data['error']['error_msg'])
    else:
        # Получаем список друзей
        friends = friends_data['response']['items']

        # Формируем список идентификаторов друзей для запроса их статусов
        friends_ids = ','.join(str(friend_id) for friend_id in friends)

        # URL для запроса информации о друзьях
        users_url = f'https://api.vk.com/method/users.get?user_ids={friends_ids}&fields=status&access_token={access_token}&v=5.131'

        # Выполняем запрос информации о друзьях
        users_response = urllib.request.urlopen(users_url)
        users_data = json.loads(users_response.read())

        # Проверяем, есть ли ошибка в ответе
        if 'error' in users_data:
            print('Ошибка при выполнении запроса информации о друзьях:', users_data['error']['error_msg'])
        else:
            # Получаем список профилей друзей с их статусами
            profiles = users_data['response']

            # Выводим статус каждого друга
            print(f"Статусы друзей пользователя {user_id}:")
            for profile in profiles:
                friend_name = profile['first_name'] + " " + profile['last_name']
                friend_status = profile.get('status', '')
                if friend_status == "":
                    continue
                print(f'{friend_name}, Статус: {friend_status}')


def main():
    # ID пользователя, для которого нужно получить список друзей
    dmitry_akulin_id = 159945397
    sema_vaibik_id = 163901316
    # get_friends(dmitry_akulin_id)
    # get_user_photos(sema_vaibik_id)
    # like_all_posts(dmitry_akulin_id)
    # unlike_all_posts(dmitry_akulin_id)
    get_friends_statuses(dmitry_akulin_id)


if __name__ == '__main__':
    main()
