from django.urls import path
from online_users.views import get_online_users, get_current_user_online


app_name = 'online_users'


urlpatterns = [
    path('get-online-users', get_online_users, name='get_online_users'),
    path('get-user-online/<str:username>/', get_current_user_online, name='get_current_user_online'),
]
