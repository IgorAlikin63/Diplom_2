import requests
import urls
import allure


class TestChangeUserData:

    @allure.title("Проверка успешного обновления данных авторизованного пользователя")
    @allure.description(
        "Тест проверяет, что авторизованный пользователь может успешно обновить свои данные")
    def test_user_can_update_info_with_authorization(self, new_user_creation):
        user_data, access_token = new_user_creation
        new_email = "some_new_" + user_data['email']
        new_name = "some_new_" + user_data['name']
        update_payload = {
            "email": new_email,
            "name": new_name
        }
        headers = {
            "Authorization": access_token
        }
        response = requests.patch(urls.BASE_URL + urls.USER_INFO, json=update_payload, headers=headers)
        assert response.status_code == 200
        assert response.json()['user']['email'] == new_email
        assert response.json()['user']['name'] == new_name

    @allure.title("Проверка ошибки при попытке обновления данных неавторизованного пользователя")
    @allure.description(
        "Тест проверяет, что неавторизованный пользователь не может обновить данные и получает ошибку")
    def test_user_cant_update_info_without_authorization(self):
        update_payload = {
            "email": "new_email@mail.ru",
            "name": "New Name"
        }
        response = requests.patch(urls.BASE_URL + urls.USER_INFO, json=update_payload)
        assert response.status_code == 401 and response.json()['message'] == "You should be authorised"