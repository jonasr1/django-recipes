from rest_framework import serializers

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]  # noqa: RUF012


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [  # noqa: RUF012
            "id", "title", "description", "author",
            "category", "tags", "public", "preparation",
            "tag_links",
            "preparation_time", "preparation_time_unit", "servings",
            "servings_unit",
            "preparation_steps", "cover",
        ]

    public = serializers.BooleanField(source="is_published", read_only=True)
    preparation = serializers.SerializerMethodField(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True, read_only=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source="tags",
        read_only=True,
        view_name="recipes:tag-api-detail",
    )

    def get_preparation(self, recipe: Recipe) -> str:
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"

    def validate(self, attrs: dict) -> dict:
        data = attrs.copy()
        if self.instance:
            for field in ("servings", "preparation_time", "title", "description"):
                if field not in data:
                    data[field] = getattr(self.instance, field)
        AuthorRecipeValidator(data=data, error_class=serializers.ValidationError)
        return attrs
