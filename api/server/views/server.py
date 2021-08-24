from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.server.serializers.server_serializers import ServerSerializer
from api.server.models import Server
from api.server.constants import MESSAGE_ERROR_SERVER_SEARCH


class CreateServerView(generics.CreateAPIView):
    queryset = Server.objects.filter(is_active=True)
    serializer_class = ServerSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['post', ]


class ListServerView(generics.ListAPIView):
    queryset = Server.objects.filter(is_active=True)
    serializer_class = ServerSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]


class RetrieveServerView(generics.RetrieveAPIView):
    queryset = Server.objects.filter(is_active=True)
    serializer_class = ServerSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get', ]

    def get_object(self):
        return Server.objects.filter(pk=self.kwargs['server_id'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if len(instance) > 0:
            return Response(
                self.get_serializer(instance[0]).data, status=status.HTTP_200_OK,
            )
        return Response(
            {'detail': MESSAGE_ERROR_SERVER_SEARCH}, status=status.HTTP_400_BAD_REQUEST
        )


class UpdateServerView(generics.UpdateAPIView):
    queryset = Server.objects.filter(is_active=True)
    serializer_class = ServerSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['put', ]

    def get_object(self):
        return Server.objects.filter(pk=self.kwargs['server_id'])

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        if len(instance) > 0:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            new_instance = serializer.update(instance[0], serializer.data)
            return Response(
                self.get_serializer(new_instance).data, status=status.HTTP_202_ACCEPTED
            )
        return Response(
            {'detail': MESSAGE_ERROR_SERVER_SEARCH}, status=status.HTTP_400_BAD_REQUEST
        )


class DeleteServerView(generics.DestroyAPIView):
    queryset = Server.objects.filter(is_active=True)
    serializer_class = ServerSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['delete', ]

    def get_object(self):
        return Server.objects.filter(pk=self.kwargs['server_id'])

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()

        if len(instance) > 0:
            self.perform_destroy(instance[0])
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'detail': MESSAGE_ERROR_SERVER_SEARCH}, status=status.HTTP_400_BAD_REQUEST
        )

