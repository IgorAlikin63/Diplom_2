import requests
import urls
import pytest
import data
import allure


class TestNewUserCreation:

    @allure.title('Создание уникального пользователя')
    @allure.description('Тест проверяет возможность создания нового уникального пользователя')
    def test_create_unique_user(self, new_user_creation):
        user_data, access_token = new_user_creation
        assert 'email' in user_data, "В словаре отсутствует email"
        assert 'password' in user_data, "В словаре отсутствует password"

    @allure.title('Попытка создания существующего пользователя')
    @allure.description('Тест проверяет, что нельзя создать пользователя с уже существующими данными')
    def test_create_existing_user(self):
        existing_user_data = data.TestRegisteredUserCredentials.REGISTERED_USER
        response = requests.post(urls.BASE_URL + urls.USER_REGISTRATION, json=existing_user_data)
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
        with allure.step(
                "В payload сохранили заготовленный шаблон создания курьера из data, содержащий все необходимые поля"):
            payload = data.TestUserBody.USER_BODY

        with allure.step("В payload удаляем одно из полей"):
            del payload[missing_field]

        with allure.step("Отправляем payload с отсутствующим полем на ручку создания .pthf"):
            response_without_required_fields = requests.post(
                urls.BASE_URL + urls.USER_REGISTRATION, json=payload)

        with allure.step("Проверяем код из ответа ручки"):
            assert response_without_required_fields.status_code == 403

        with allure.step("Проверяем соответствие сообщения об ошибке"):
            assert response_without_required_fields.json()[
                       'message'] == "Email, password and name are required fields"