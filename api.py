import requests
import data
import urls
import allure
from faker import Faker


@allure.step('Создание экземпляра UserSession')
class UserSession:
    def __init__(self):
        self.accessToken = None

user_session = UserSession()

class UserApi:

    @staticmethod
    @allure.title('Регистрируем нового юзера со случайными данными, возвращаем словарь с его именем, почтой, паролем')
    def register_new_user_and_return_email_password():
        # генерируем почту, пароль и имя курьера
        fake = Faker()
        email = fake.email()
        password = fake.password()
        name = fake.name()

        # собираем тело запроса
        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(urls.BASE_URL + urls.USER_REGISTRATION, json=payload)

        # если регистрация прошла успешно (код ответа 200), добавляем в список логин и пароль курьера
        if response.status_code == 200:
            user_data = {
                "email": email,
                "password": password,
                "name": name
            }
            return user_data  # Возвращаем словарь данных пользователя

            # если возникла ошибка, возвращаем пустой словарь
        else:
            return {}

    @staticmethod
    @allure.title('Генерируем случайные пользовательские данные без регистрации')
    def generate_random_user_credentials_without_registration():
        fake = Faker()
        email = fake.email()
        password = fake.password()
        name = fake.name()

        # собираем тело запроса
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        return payload

    @staticmethod
    @allure.title('Авторизуем юзера и получаем его accessToken')
    def login_user(user_session, email, password):
        login_payload = {
            "email": email,
            "password": password
       }
        response_login = requests.post(urls.BASE_URL + urls.USER_LOGIN, json=login_payload)
        if response_login.status_code == 200:
            user_session.accessToken = response_login.json()['accessToken']
            return user_session
        else:
            print(f"Ошибка: {response_login.status_code}")
            print(response_login.json())
            return None


    @staticmethod
    @allure.title('Удаляем пользователя по токену')
    def delete_user(user_session):
        headers = {
            "Authorization": user_session.accessToken
        }
        response = requests.delete(urls.BASE_URL + urls.DELETE_USER, headers=headers)
        if response.status_code == 202:
            return {"success": True , "message": "User successfully removed"}
        else:
            print(f"Ошибка при удалении пользователя: {response.status_code}")
            print(f"Тело ответа: {response.json()}")
            return {'success': False, 'message': 'Failed to delete user', 'error': response.json()}

    @staticmethod
    @allure.title('Авторизуемся зарегистрированным пользователем')
    def login_registered_user():
        user_data = data.TestRegisteredUserCredentials.REGISTERED_USER
        response = requests.post(urls.BASE_URL + urls.USER_LOGIN, data=user_data)
        if response.status_code == 200:
            access_token = response.json()['accessToken']
            return access_token
