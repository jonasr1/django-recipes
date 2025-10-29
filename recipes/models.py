from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    SERVINGS_UNIT_CHOICES = (
        ("Porções", "Porções"),
        ("Pedaços", "Pedaços"),
        ("Pessoas", "Pessoas"),
    )

    PREPARATION_TIME_UNIT_CHOICES = (
        ("Minutos", "Minutos"),
        ("Horas", "Horas"),
    )
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(
        max_length=65, choices=PREPARATION_TIME_UNIT_CHOICES,
    )
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=65, choices=SERVINGS_UNIT_CHOICES)
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to="recipes/covers/%Y/%m/%d", blank=True, default="")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True, default=None,
    )
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None: # noqa
        if not self.slug:
            slug = f"{slugify}"
            self.slug = slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("recipes:recipe", kwargs={"pk": self.pk})
