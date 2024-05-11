from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone


class OnlineUserActivity(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    path = models.TextField(default='')
    last_activity = models.DateTimeField()

    @staticmethod
    def update_user_activity(user, path=""):
        """Updates the timestamp a user has for their last action. Uses UTC time."""
        OnlineUserActivity.objects.update_or_create(
            user=user, defaults={'last_activity': timezone.now(), 'path': path}
        )

    @staticmethod
    def get_user_activities(time_delta=15, path=""):
        """
        Gathers OnlineUserActivity objects from the database representing active users.

        :param time_delta: The amount of time in the past to classify a user as "active". Default is 15 minutes.
        :path: A string representing the path to a user's activity.
        :return: QuerySet of active users within the time_delta
        """
        starting_time = timezone.now() - timedelta(minutes=time_delta)
        if path:
            return OnlineUserActivity.objects.filter(last_activity__gte=starting_time, path=path).order_by(
                '-last_activity')
        else:
            return OnlineUserActivity.objects.filter(last_activity__gte=starting_time).order_by('-last_activity')

    def __str__(self):
        return str(self.user)
