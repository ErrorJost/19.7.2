from api import PetFriends
from settings import valid_email, valid_password, not_valid_email, not_valid_password
import os

pf = PetFriends()

# Тест 1. Получение ключа API
def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

# Тест 2. Получаем список всех питомцев.
def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

 # Тест 3. Добавление питомца с корректными данными.
def test_add_new_pet_with_valid_data(name='Дымок', animal_type='кролик', age='1', pet_photo='images/rabbit.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

# Тест 4. Удаление питомца.
def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Дымок", "кролик", "1", "/rabbit.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()

# Тест 5. Обновление информации о питомце.
def test_successful_update_self_pet_info(name='Дымок', animal_type='кролик', age=2):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")

# Тест 6. Получение ключа с некорректной почтой, но корректным паролем.
def test_get_api_key_for_not_valid_email(email=not_valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# Тест 7. Получение ключа с некорректным паролем, но корректной почтой.
def test_get_api_key_for_not_valid_password(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# Тест 8. Добавление питомца без фото.
def test_add_new_pet_without_photo_valid_data (name='Рыжий', animal_type='кот', age='15'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

# Тест 9. Добавление питомца с пустыми значениями.
def test_add_new_pet_with_empty_value_in_variable_name(name='', animal_type='', age='', pet_photo=''):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 400
    # Баг. Код ответа сервера 200. Питомец создается с пустыми значениями.

# Тест 10. Добавление питомца с отрицательным возрастом.
def test_add_new_pet_negative_age(name='Дымок', animal_type='кролик', age='-1', pet_photo='images/rabbit.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    # Баг. Код ответа сервера 200. Питомец создается с отрицательным возрастом.

# Тест 11. Добавление питомца без фото с некорректными данными.
def test_add_new_pet_without_photo_invalid_data(name='!!!', animal_type='@@@', age='абв'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    # Баг. Код ответа сервера 200. Питомец создается c некорректными данными.

# Тест 12. Добавление фото питомца.
def test_post_add_new_photo_of_pet(pet_photo='images/tihon.jpeg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.post_add_new_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("There is no my pets")

# Тест 13. Создание питомца с длинным именем.
def test_add_new_pet_with_invalid_name(name='Дымоооооооооооооооооооооооооооооооок', animal_type='кролик',
                                       age='1', pet_photo='images/rabbit.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, api_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(api_key, name, animal_type, age, pet_photo)
    assert status == 400
    # Баг. Код ответа сервера 200. Создается питомец с длинным именем.

# Тест 14. Создание питомца, который уже существует.
def test_add_repeat_pet_with_valid_data(name='Дымок', animal_type='кролик', age='1', pet_photo='images/rabbit.jpeg'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400
    # Баг. Код ответа сервера 200. Создается питомец, который уже существует на сайте.
