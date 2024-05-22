from django.urls import path
from .views import *

urlpatterns = [
    path('', trigger_notification_api, name='trigger-notification'),
    # Other URL patterns for your app
]
