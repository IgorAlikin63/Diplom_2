import pytest
from api import UserApi, UserSession
import allure


@pytest.fixture(scope="function")
@allure.title('Фикстура для создания нового пользователя')
def new_user_creation(auth_required=True):
    #Создаем нового пользователя и получаем его данные
    user_data = UserApi.register_new_user_and_return_email_password()
    email = user_data.get('email')
    password = user_data.get('password')

    #Проверяем, что данные пользователя были успешно созданы
    assert email and password, "Не удалось создать пользователя"

    access_token = None
    if auth_required:
        user_session = UserSession()
        #Авторизуем пользователя и получаем accessToken
        user_session = UserApi.login_user(user_session, email, password)
        assert user_session.accessToken, "Не удалось авторизовать пользователя"
        access_token = user_session.accessToken

    #Предоставляем данные пользователя и accessToken для теста
    yield user_data, access_token

    #После завершения теста удаляем пользователя
    delete_response = UserApi.delete_user(user_session)
    assert delete_response['success'], "Не удалось удалить пользователя"