import allure
from api import UserApi


class TestChangeUserData:

    @allure.title("Проверка успешного обновления email авторизованного пользователя")
    @allure.description(
        "Тест проверяет, что авторизованный пользователь может успешно обновить свой email")
    def test_user_can_update_email_with_authorization(self):
        user_data = UserApi.generate_user_data()
        user_response = UserApi.register_user(user_data)
        access_token = UserApi.get_access_token(user_response)
        new_email = "some_new_" + user_data['email']
        new_data = {"email": new_email}
        headers = access_token
        response = UserApi.change_user_data(headers, new_data)
        assert response.status_code == 200
        assert response.json()['user']['email'] == new_email
        UserApi.delete_user(access_token)

    @allure.title("Проверка успешного обновления имени авторизованного пользователя")
    @allure.description(
        "Тест проверяет, что авторизованный пользователь может успешно обновить свое имя")
    def test_user_can_update_name_with_authorization(self):
        user_data = UserApi.generate_user_data()
        user_response = UserApi.register_user(user_data)
        access_token = UserApi.get_access_token(user_response)
        new_name = "some_new_" + user_data['name']
        new_data = {"name": new_name}
        headers = access_token
        response = UserApi.change_user_data(headers, new_data)
        assert response.status_code == 200
        assert response.json()['user']['name'] == new_name
        UserApi.delete_user(access_token)

    @allure.title("Проверка ошибки при попытке обновления данных неавторизованного пользователя")
    @allure.description(
        "Тест проверяет, что неавторизованный пользователь не может обновить имя и получает ошибку")
    def test_user_cant_update_name_without_authorization(self):
        update_payload = {
            "name": "new_name_WoW"
        }
        response = UserApi.change_user_data('', update_payload)
        assert response.status_code == 401 and response.json()['message'] == "You should be authorised"

    @allure.title("Проверка ошибки при попытке обновления данных неавторизованного пользователя")
    @allure.description(
        "Тест проверяет, что неавторизованный пользователь не может обновить почту и получает ошибку")
    def test_user_cant_update_email_without_authorization(self):
        update_payload = {
            "email": "new_email1111@mail.ru"
        }
        response = UserApi.change_user_data('', update_payload)
        assert response.status_code == 401 and response.json()['message'] == "You should be authorised"