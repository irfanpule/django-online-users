from django.http import JsonResponse
from online_users.models import OnlineUserActivity


def get_online_users(request):
    kwargs = {
        'path': request.GET.get('path', ''),
        'time_delta': int(request.GET.get('time_delta', 15)),
    }
    user_activity_objects = OnlineUserActivity.get_user_activities(**kwargs)
    number_of_active_users = user_activity_objects.count()
    data_users = []
    for obj in user_activity_objects:
        data_users.append({
            'id': obj.user.id,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email,
            'date_joined': obj.user.date_joined,
        })
    data = {
        'number_of_online_users': number_of_active_users,
        'online_users': data_users
    }
    return JsonResponse(data)


def get_current_user_online(request, username):
    kwargs = {
        'path': request.GET.get('path', ''),
        'time_delta': int(request.GET.get('time_delta', 15)),
    }
    user_activity_objects = OnlineUserActivity.get_user_activities(**kwargs)
    user_online = user_activity_objects.filter(user__username=username).first()
    if user_online:
        user = {
            'id': user_online.user.id,
            'username': user_online.user.username,
            'first_name': user_online.user.first_name,
            'last_name': user_online.user.last_name,
            'email': user_online.user.email,
            'date_joined': user_online.user.date_joined,
        }
        status = 'online'
    else:
        user = None
        status = 'offline'

    return JsonResponse({
        'status_activity': status,
        'user_data': user,
    })
