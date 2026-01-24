from recipes.urls.api import urlpatterns as api_urlpatterns
from recipes.urls.web import urlpatterns as web_urlpatterns

app_name = "recipes"

urlpatterns = web_urlpatterns + api_urlpatterns
