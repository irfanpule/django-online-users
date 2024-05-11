from django.utils.deprecation import MiddlewareMixin

from online_users.models import OnlineUserActivity
from django.conf import settings


class OnlineNowMiddleware(MiddlewareMixin):
    """Updates the OnlineUserActivity database whenever an authenticated user makes an HTTP request."""

    @staticmethod
    def process_request(request):
        user = request.user
        if not user.is_authenticated:
            return

        prefix_path_exclude = ['online-users', 'admin', 'media', 'static', 'assets']
        if hasattr(settings, 'ONLINE_USERS_PREFIX_PATH_EXCLUDE'):
            prefix_path_exclude += settings.ONLINE_USERS_PREFIX_PATH_EXCLUDE

        if request.path_info.split("/")[1] in prefix_path_exclude:
            return

        OnlineUserActivity.update_user_activity(user, request.path_info)
