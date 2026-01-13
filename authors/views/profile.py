from typing import Any

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from authors.models import Profile


class ProfileView(TemplateView):
    template_name = "authors/pages/profile.html"

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile_id = context.get("profile_id")
        queryset = Profile.objects.select_related("author")
        profile = get_object_or_404(queryset, pk=profile_id)
        context["profile"] = profile
        return context
