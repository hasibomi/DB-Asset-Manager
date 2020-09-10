from django.urls import path
from .views import *

app_name = 'asset_manager'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('connect/<pk>/', ConnectToAConnectionView.as_view(), name='connect'),
    path('<pk>/delete/', DeleteAConnection.as_view(), name='delete'),
]
