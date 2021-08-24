import uuid

from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.core.mail import send_mail
from django.conf import settings
from keycloak.exceptions import KeycloakAuthenticationError

from api.investigator.serializers import investigator
from api.investigator.keycloak import ConnectKeycloak
from api.investigator.logs import LogsConnection
from api.investigator.utils import load_data_user_in_data_keycloak
from api.investigator.constants import (
    ERROR_AUTHENTICATION_KEYCLOAK,
    ERROR_GET_INFO_KEYCLOAK,
    ERROR_AUTHENTICATION_TOKEN_KEYCLOAK,
    DETAIL_SUCCESS_SEND_EMAIL
)


class LoginUserKeycloak(generics.CreateAPIView):
    serializer_class = investigator.LoginUserKeycloakSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post']

    @staticmethod
    def format_id_keycloak(id_keycloak):
        list_letters = list()
        add = False

        for letter in id_keycloak:
            if add:
                list_letters.append(letter)

            if letter == ':':
                add = True if not add else False

        return "".join(list_letters[:len(list_letters)-1])

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            log, created, user = LogsConnection.create_log_of_connection(email, "LI")

            try:
                data = ConnectKeycloak.login_keycloak(email, password)

                if created:
                    data_user = ConnectKeycloak.get_user_info(data.get("access_token"))
                    user.id_keyclock = self.format_id_keycloak(data_user.get("sub"))
                    user.curp = data_user.get("curp")
                    user.save()

                data = load_data_user_in_data_keycloak(data, email)
                LogsConnection.update_log_of_connection(log, 202)
                return Response(
                    self.get_serializer(data).data, status=status.HTTP_202_ACCEPTED)

            except KeycloakAuthenticationError:
                LogsConnection.update_log_of_connection(log, 400)
                return Response(
                    ERROR_AUTHENTICATION_KEYCLOAK, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LogOutUserKeycloak(generics.CreateAPIView):
    serializer_class = investigator.LogoutKeycloakSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            refresh_token = serializer.data.get("refresh_token")
            log, created, user = LogsConnection.create_log_of_connection(email, 'LO')
            data = ConnectKeycloak.logout_keycloak(refresh_token)
            LogsConnection.update_log_of_connection(log, 204)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            ERROR_AUTHENTICATION_TOKEN_KEYCLOAK, status=status.HTTP_400_BAD_REQUEST)


class GetInfoUser(generics.GenericAPIView):
    serializer_class = investigator.GetInfoSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        access_token = self.kwargs["access_token"]
        if len(access_token) > 50:
            try:
                data = ConnectKeycloak.get_user_info(access_token)
                LogsConnection.create_log_complete(
                    email=data.get("email"), action="OIU", status=202)
                return Response(
                    self.get_serializer(data).data, status=status.HTTP_202_ACCEPTED)

            except KeycloakAuthenticationError:
                LogsConnection.create_log_complete(
                    email='Desconocido@gmail.com', action="OIU", status=404)
                return Response(
                    ERROR_AUTHENTICATION_TOKEN_KEYCLOAK, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            ERROR_GET_INFO_KEYCLOAK, status=status.HTTP_400_BAD_REQUEST)


class SendCodeResetPassword(generics.CreateAPIView):
    serializer_class = investigator.SendCodeResetPasswordSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post']

    @staticmethod
    def create_code_for_validation():
        return str(uuid.uuid4())

    @staticmethod
    def send_email_reset_password(email, code):
        send_mail(
            subject="Solicitud para restablecer contraseña",
            message="El siguiente código será solicitado para validar si identidad: {}".format(
                code),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email, ],
            fail_silently=False
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data.get("email")
            log, created, user = LogsConnection.create_log_of_connection(email, 'SRC')
            code = self.create_code_for_validation()
            serializer.create(code)
            self.send_email_reset_password(email, code)
            LogsConnection.update_log_of_connection(log, 202)
            return Response(
                {'detail': DETAIL_SUCCESS_SEND_EMAIL}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
