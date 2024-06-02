import requests
import urls
import pytest
import data
import allure

class TestOrderCreation:

    @pytest.mark.parametrize("auth, ingredients, expected_status, expected_success", [
        (True, data.TestDataValidIngredientsForBurger.VALID_INGREDIENTS_FOR_BURGER, 200, True),
        (False, data.TestDataValidIngredientsForBurger.VALID_INGREDIENTS_FOR_BURGER, 200, True),
        (True, data.TestEmptyIngredientsForBurger.EMPTY_INGREDIENTS_FOR_BURGER, 400, False)
    ])
    @allure.title('Тестирование создания заказа с валидными и невалидными ингредиентами')
    @allure.description('Тест проверяет создание заказа с различными комбинациями авторизации и ингредиентов')
    def test_order_creation(self, new_user_creation, auth, ingredients, expected_status, expected_success):
        user_data, access_token = new_user_creation
        headers = {"Authorization": access_token} if auth else {}
        response = requests.post(urls.BASE_URL + urls.ORDER_CREATION, headers=headers, json=ingredients)
        assert response.status_code == expected_status
        assert response.json()['success'] == expected_success

    @allure.title('Тестирование создания заказа с невалидными ингредиентами')
    @allure.description('Тест проверяет, что заказ с невалидными ингредиентами не создается')
    def test_order_creation_with_unvalid_ingredients(self, new_user_creation):
        user_data, access_token = new_user_creation
        headers = {"Authorization": access_token}
        ingredients = data.TestDataUnValidIngredientsForBurger.UNVALID_INGREDIENTS_FOR_BURGER
        response = requests.post(urls.BASE_URL + urls.ORDER_CREATION, headers=headers, json=ingredients)
        assert response.status_code == 500
