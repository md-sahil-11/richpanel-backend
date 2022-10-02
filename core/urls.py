from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path("users/", include("user.api.urls")),
    path("subs/", include("subscription.api.urls", namespace="subscription")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
