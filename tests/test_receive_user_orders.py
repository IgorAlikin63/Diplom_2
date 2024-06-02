import requests
from api import UserApi
import urls
import allure

class TestReceiveUserOrders:

    @allure.title("Получение заказов авторизованным пользователем")
    @allure.description(
        "Тест проверяет, что авторизованный пользователь может получить список своих заказов")
    def test_authorized_user_can_get_orders(self):
        access_token = UserApi.login_registered_user()
        headers = {
            "Authorization": access_token
        }
        response = requests.get(urls.BASE_URL + urls.ORDERS_USER, headers=headers)
        assert response.status_code == 200
        assert 'orders' in response.json()
        assert len(response.json()['orders']) <= 50  # Проверяем, что заказов не больше 50

    @allure.title("Получение заказов неавторизованным пользователем")
    @allure.description(
        "Тест проверяет, что неавторизованный пользователь не может получить список заказов и получает ошибку")
    def test_unauthorized_user_cannot_get_orders(self):
        response = requests.get(urls.BASE_URL + urls.ORDERS_USER)
        assert response.status_code == 401
        assert response.json()['message'] == "You should be authorised"