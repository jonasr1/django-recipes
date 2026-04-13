from typing import TypedDict

from django.urls import reverse

from recipes.models import User
from recipes.tests.test_recipe_base import RecipeMixin


class AuthData(TypedDict):
    jwt_access_token: str
    jtw_refresh_token: str
    user: User


class RecipeAPIMixin(RecipeMixin):
    def get_recipe_raw_data(self) -> dict[str, int | str]:
        return {
            "title": "This is the title",
            "description": "This is the description",
            "preparation_time": 1,
            "preparation_time_unit": "Minutos",
            "servings": "1",
            "servings_unit": "Pessoas",
            "preparation_steps": "This is the preparation steps.",
        }

    def get_recipe_list_reverse_url(self, reverse_result: str | None = None) -> str:
        return reverse_result or reverse("recipes:recipes-api-list")

    def get_recipe_api_list(self, reverse_result: str | None = None):  # noqa: ANN201
        api_url = self.get_recipe_list_reverse_url(reverse_result)
        return self.client.get(api_url)

    def build_jwt_user_data(self, username: str, password: str) -> dict[str, str]:
        return {
            "username": username,
            "password": password,
        }

    def create_jwt_user(self, userdata: dict[str, str]) -> User:
        return self.make_author(
            username=userdata.get("username"),
            password=userdata.get("password"),
        )

    def request_jwt_token(self, userdata: dict[str, str]):  # noqa: ANN201
        return self.client.post(
            reverse("recipes:token_obtain_pair"), data={**userdata},
        )

    def get_auth_data(self, username: str = "user", password: str = "pass") -> AuthData:  # noqa: S107
        userdata = self.build_jwt_user_data(username, password)
        user = self.create_jwt_user(userdata)
        response = self.request_jwt_token(userdata)
        return {
            "jwt_access_token": response.data["access"],
            "jtw_refresh_token": response.data["refresh"],
            "user": user,
        }
