from api import UserApi
import allure
import pytest
import data

class TestNewUserCreation:

    @allure.title('Создание уникального пользователя')
    @allure.description('Тест проверяет возможность создания нового уникального пользователя')
    def test_create_unique_user(self):
        new_user_data = UserApi.generate_user_data()
        user_response = UserApi.register_user(new_user_data)
        assert user_response.status_code == 200, "Не удалось зарегистрировать нового пользователя"
        assert user_response.json()['user']['email'] == new_user_data['email'], "Email пользователя не соответствует"
        assert user_response.json()['user']['name'] == new_user_data['name'], "Имя пользователя не соответствует"
        access_token = UserApi.get_access_token(user_response)
        UserApi.delete_user(access_token)

    @allure.title('Попытка создания существующего пользователя')
    @allure.description('Тест проверяет, что нельзя создать пользователя с уже существующими данными')
    def test_create_existing_user(self):
        existing_user_data = data.TestRegisteredUserCredentials.REGISTERED_USER
        response = UserApi.register_user(existing_user_data)
        assert response.status_code == 403 and response.json()["message"] == "User already exists"

    @pytest.mark.parametrize('missing_field, '
                             'error_message', [
                                 ('email', 'Email, password and name are required fields'),
                                 ('password', 'Email, password and name are required fields'),
                                 ('name', 'Email, password and name are required fields')
                             ])
    @allure.title("Проверка, что нельзя создать юзера без обязательных полей")
    @allure.description(
        "Тест проверяет, что нельзя создать юзера без обязательных полей, будет ошибка")
    def test_cant_create_user_without_required_fields_and_get_error(self, missing_field, error_message):
        payload = data.TestUserBody.USER_BODY.copy()
        del payload[missing_field]
        response_without_required_fields = UserApi.register_user(payload)
        assert response_without_required_fields.status_code == 403
        assert response_without_required_fields.json()[
                       'message'] == "Email, password and name are required fields"