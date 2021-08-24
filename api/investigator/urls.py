from django.urls import path

from .views.investigator import (
    LoginUserKeycloak, GetInfoUser, LogOutUserKeycloak, SendCodeResetPassword
)


urlpatterns = [
    path('login', LoginUserKeycloak.as_view(), name='login'),
    path('logout', LogOutUserKeycloak.as_view(), name='logout'),
    path('me/<str:access_token>', GetInfoUser.as_view(), name='get_user'),
    path('reset/password', SendCodeResetPassword.as_view(), name='send_code'),
]
