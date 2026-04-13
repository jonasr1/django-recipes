from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, ModelSerializer, ValidationError

User = get_user_model()


class AuthorSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]  # noqa: RUF012


class AuthorCreateSerializer(ModelSerializer):
    # password = CharField(write_only=True, required=True, validators=[strong_password])
    password = CharField(write_only=True, required=True)
    password2 = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [  # noqa: RUF012
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        ]
        extra_kwargs = {  # noqa: RUF012
            "username": {"min_length": 4},
            "email": {"required": True},
        }

    def validate_email(self, email: str) -> str:
        exists = User.objects.filter(email__iexact=email).exists()
        if exists:
            msg = "User e-mail is already in use"
            raise ValidationError(msg)
        return email

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        password = attrs.get("password", "")
        password2 = attrs.get("password2", "")
        if password != password2:
            msg = "Password and password2 must be equal"
            raise ValidationError({"password": [msg], "password2": [msg]})
        return attrs

    def create(self, validated_data: dict[str, str]) -> object:
        validated_data.pop("password2")
        password = validated_data.pop("password")
        return User.objects.create_user(password=password, **validated_data)
