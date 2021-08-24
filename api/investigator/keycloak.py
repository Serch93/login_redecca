from django.conf import settings
from keycloak import KeycloakOpenID, KeycloakAdmin

from api.investigator.constants import *


class ConnectKeycloak:

    @classmethod
    def connect_keycloak(cls):
        keycloak_openid = KeycloakOpenID(
            server_url=KEYCLOAK_URL,
            client_id=KEYCLOAK_CLIENT_ID,
            realm_name="miic",
            client_secret_key=KEYCLOAK_CLIENT_SECRET,
            verify=True)
        config_well_know = keycloak_openid.well_know()
        return keycloak_openid

    @classmethod
    def login_keycloak(cls, email: str = '', password: str = ''):
        keycloak_openid = cls.connect_keycloak()

        if settings.DEBUG:
            email = KEYCLOAK_USER_TEST
            password = KEYCLOAK_USER_PASSWORD_TEST

        tokens = keycloak_openid.token(
            username=email, password=password, grant_type='password')
        return tokens

    @classmethod
    def get_user_info(cls, token_access: str = ''):
        keycloak_openid = cls.connect_keycloak()
        return keycloak_openid.userinfo(token=token_access)

    @classmethod
    def logout_keycloak(cls, token_refresh: str = ''):
        keycloak_openid = cls.connect_keycloak()
        logout = keycloak_openid.logout(refresh_token=token_refresh)
        return logout



