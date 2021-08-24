from django.urls import path

from api.server.views import server


urlpatterns = [
    path('add/', server.CreateServerView.as_view(), name='add_server'),
    path('list/', server.ListServerView.as_view(), name='list_server'),
    path('edit/<int:server_id>/', server.UpdateServerView.as_view(), name='edit_server'),
    path('delete/<int:server_id>/', server.DeleteServerView.as_view(), name='delete_server'),
    path('get/<int:server_id>/',
         server.RetrieveServerView.as_view(), name='get_server_id'),
]
