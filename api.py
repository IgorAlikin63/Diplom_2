import requests
import data
import urls
import allure
from faker import Faker

class UserApi:

    @staticmethod
    @allure.title("Генерируем пользовательские данные, возвращаем словарь с его именем, почтой, паролем")
    def generate_user_data():
        fake = Faker()
        email = fake.email()
        password = fake.password()
        name = fake.name()
        user_data = {
            "email": email,
            "password": password,
            "name": name
        }
        return user_data


    @staticmethod
    @allure.step("Зарегистрировать пользователя")
    def register_user(user_data):
        user_response = requests.post(urls.BASE_URL + urls.USER_REGISTRATION, json=user_data)
        return user_response

    @staticmethod
    @allure.step("Получить access token созданного пользователя")
    def get_access_token(user_response):
        access_token = user_response.json().get("accessToken")
        return access_token

    @staticmethod
    @allure.title("Авторизуем пользователя")
    def login_user(login_data):
        response_login = requests.post(urls.BASE_URL + urls.USER_LOGIN, json=login_data)
        return response_login


    @staticmethod
    @allure.title("Удаляем пользователя по токену")
    def delete_user(access_token):
        headers = {
            "Authorization": access_token
        }
        response_delete = requests.delete(urls.BASE_URL + urls.DELETE_USER, headers=headers)
        return response_delete

    @staticmethod
    @allure.step("Изменить данные пользователя: email, password, name")
    def change_user_data(access_token, new_data):
        headers = {"Authorization": access_token}
        change_data_response = requests.patch(urls.BASE_URL + urls.USER_INFO, headers=headers, json=new_data)
        return change_data_response

    @staticmethod
    @allure.step("Получить все заказы конкретного пользователя")
    def get_users_orders(headers):
        response = requests.get(urls.BASE_URL + urls.ORDERS_USER, headers=headers)
        return response


    @staticmethod
    @allure.title('Авторизуемся зарегистрированным пользователем')
    def login_registered_user():
        user_data = data.TestRegisteredUserCredentials.REGISTERED_USER
        response = requests.post(urls.BASE_URL + urls.USER_LOGIN, json=user_data)
        access_token = response.json()['accessToken']
        return access_token

    @staticmethod
    @allure.step("Создать заказ")
    def create_new_order(headers, ingredients):
        response = requests.post(urls.BASE_URL + urls.ORDER_CREATION, headers=headers, json=ingredients)
        return response
