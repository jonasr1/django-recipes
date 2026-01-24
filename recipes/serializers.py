from rest_framework import serializers

from recipes.models import Recipe


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    slug = serializers.SlugField()


class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source="is_published")
    preparation = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()
    author = serializers.StringRelatedField()
    tags = TagSerializer(many=True)
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source="tags",
        read_only=True,
        view_name="recipes:tag-api-detail",
    )

    def get_preparation(self, recipe: Recipe) -> str:
        return f"{recipe.preparation_time} {recipe.preparation_time_unit}"
