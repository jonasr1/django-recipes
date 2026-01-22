import contextlib
import itertools
import os
from collections import defaultdict

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from PIL import Image

from tag.models import Tag


class Category(models.Model):
    name = models.CharField(max_length=65)

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

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
    title = models.CharField(max_length=65, verbose_name=_("Title"))
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
    tags = models.ManyToManyField(Tag, blank=True, default="")

    class Meta:
        verbose_name = _("Recipe")
        verbose_name_plural = _("Recipes")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            for i in itertools.count(1):
                if not Recipe.objects.filter(slug=slug).exists():
                    break
                slug = f"{base_slug}-{i}"
            self.slug = slug
        saved = super().save(*args, **kwargs)
        if self.cover:
            with contextlib.suppress(FileNotFoundError):
                self.resize_image(self.cover, 840)
        return saved

    def get_absolute_url(self) -> str:
        return reverse("recipes:recipe", kwargs={"pk": self.pk})

    def resize_image(self, image: Image.Image, new_width: int = 840) -> None:
        imagem_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        imagem_pillow = Image.open(imagem_full_path)
        original_width, original_height = imagem_pillow.size
        if original_width <= new_width:
            imagem_pillow.close()
            return
        new_height = round((original_height * new_width) / original_width)
        new_image = imagem_pillow.resize((new_width, new_height), Image.LANCZOS)
        new_image.save(imagem_full_path, optimize=True, quality=50)

    def clean(self, *args, **kwargs) -> None:
        error_messages = defaultdict(list)
        recipe_from_db = Recipe.objects.filter(title__iexact=self.title).first()
        if recipe_from_db and recipe_from_db.pk != self.pk:
            error_messages["title"].append("Found recipes with the same title")
        if error_messages:
            raise ValidationError(error_messages)
