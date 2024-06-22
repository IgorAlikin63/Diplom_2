from api import UserApi
import allure
import data


class TestUserLogin:

    @allure.title("Проверка успешной авторизации существующим пользователем")
    @allure.description(
        "Тест проверяет, что можно авторизоваться уже существующим пользователем")
    def test_user_can_login_with_existing_credentials(self):
        login_data = data.TestRegisteredUserCredentials.REGISTERED_USER
        response = UserApi.login_user(login_data)
        assert response.status_code == 200 and response.json()['accessToken'] is not None

    @allure.title('Проверка авторизации без регистрации')
    @allure.description('Тест проверяет, что нельзя авторизоваться с незарегистрированными данными')
    def test_user_cant_login_without_registered_credentials(self):
        payload = UserApi.generate_user_data()
        response = UserApi.login_user(payload)
        assert response.status_code == 401 and response.json()['message'] == "email or password are incorrect"