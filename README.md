django-online-users
===================

Tracks the time of each user's last action

Using middleware, django-online-users will keep track of each user and the timestamp of their last action in the database.

Admins can see this data in the admin portal, and the database can be queried using timedeltas.

This is meant for smaller applications as each HTTP request will result in a database entry update.

Requirements
------------

- Python: 3.6+
- Django: 2.2+


Setup
-----------

1. Add "online_users" to your ``INSTALLED_APPS``


```python
INSTALLED_APPS = [
    # other apps
    'online_users',
]
```

2. Run  `python manage.py migrate` to create the tables in the database.
3. Add the `OnlineNowMiddleware` to your `MIDDLEWARE_CLASSES` after the ``SessionMiddleware``

```python
MIDDLEWARE_CLASSES = (
    # other middlewares
    'online_users.middleware.OnlineNowMiddleware',
)
```

4. Add the `online_users.urls` to your root path

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    # other path ...
    path('online-users/', include('online_users.urls')),
]
```

Use
---
#### Query
To retrieve the current number of users online in the last 15 minutes


```python
from online_users.models import OnlineUserActivity

# basic query
user_activity_objects = OnlineUserActivity.get_user_activities() # to get all users in everywhere
number_of_active_users = user_activity_objects.count()

# with args time delta
user_activity_objects = OnlineUserActivity.get_user_activities(
    time_delta=2 # change the last active time from 15 minutes to 2 minutes
)

# with args path
user_activity_objects = OnlineUserActivity.get_user_activities(
    path='/post/slug-article/01' # to get all last active users on this path
)

# with all args
user_activity_objects = OnlineUserActivity.get_user_activities(
    path='/post/slug-article/01', # to get all last active users on this path
    time_delta=2
)
```

#### Ajax Request
```js
// basic request
$.ajax({
    url: `{% url 'online_users:get_online_users' %}`,
    type: 'GET',
    success: function (data) {
        console.log(data.online_users);
        console.log(data.number_of_online_users);
        // do something     
    },
    error: function (data) {
        alert("An error occured!");
    }
});

// with query params 
$.ajax({
    url: `{% url 'online_users:get_online_users' %}?time_delta=5&&path=${window.location.pathname}`,
    // time_delta=2 to change last active time
    // path=${window.location.pathname} to get all user with current path
    //...
});


// get current user online
$.ajax({
    url: `{% url 'online_users:get_current_user_online' username %}?time_delta=5`,
    type: 'GET',
    success: function (data) {
        console.log(data.status_activity); // status string "online" or "offline"
        console.log(data.user_data);
        // to something
    },
    error: function (data) {
        alert("An error occured!");
    }
});
```

#### Exclude specific path
You can exclude specific path use set list of exclude prefix path in `settings.py`
```python
# other setting
ONLINE_USERS_PREFIX_PATH_EXCLUDE = ['__debug__', '__reload__', 'sonar']
```


Change Log
------------
* 1.0 - Major update new features
* 0.3 - Updating to have on_delete = models.CASCADE
* 0.2 - Updating to Django 1.11. Changed from basic User model to settings.AUTH_USER_MODEL.