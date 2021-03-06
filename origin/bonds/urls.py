from . import views
from django.urls import path
from bonds.views import HelloWorld, UserCreate
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', UserCreate.as_view(), name='create-user'),
    path('bonds/', HelloWorld.as_view(), name='bonds'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]