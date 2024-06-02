import requests
from api import UserApi
import urls
import data
import allure


class TestUserLogin:

    @allure.title("Проверка успешной авторизации существующим курьеров")
    @allure.description(
        "Тест проверяет, что можно авторизоваться уже существующим курьером")
    def test_user_can_login_with_existing_credentials(self):
        with allure.step("Формируем payload используя данные о существующем курьере из data"):
            payload = data.TestRegisteredUserCredentials.REGISTERED_USER

        with allure.step("Вызываем ручку авторизации со сформированным payload"):
            response = requests.post(
                urls.BASE_URL + urls.USER_LOGIN, json=payload)

        with allure.step("Проверяем код ответа и наличие в ответе id"):
            assert response.status_code == 200 and response.json()['accessToken'] is not None

    @allure.title('Проверка авторизации без регистрации')
    @allure.description('Тест проверяет, что нельзя авторизоваться с незарегистрированными данными')
    def test_user_cant_login_without_registered_credentials(self):
        with allure.step("Формируем payload используя случайные данные"):
            payload = UserApi.generate_random_user_credentials_without_registration()

        with allure.step("Вызываем ручку логина со сформированным payload"):
            response = requests.post(
                urls.BASE_URL + urls.USER_LOGIN, json=payload)

        with allure.step("Проверяем код ответа и наличие в ответе id"):
            assert response.status_code == 401 and response.json()['message'] == "email or password are incorrect"