import pytest
from api import UserApi
import allure

@allure.step("Создать пользователя для теста с последующим удалением")
@pytest.fixture(scope='function')
def new_user(auth_required=True):
    user_body = UserApi.generate_user_data()
    user_response = UserApi.register_user(user_body)
    access_token = UserApi.get_access_token(user_response)
    yield user_response, access_token
    UserApi.delete_user(access_token)


