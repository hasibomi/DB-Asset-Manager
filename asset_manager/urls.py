from django.urls import path
from .views import *

app_name = 'asset_manager'
urlpatterns = [
    path('', IndexView.as_view(), name='index')
]
