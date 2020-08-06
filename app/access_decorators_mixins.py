from django.core.exceptions import PermissionDenied


def admin_login_required(function):
    """ this function is a decorator used to authorize if a user is admin """

    def wrap(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_superuser:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    return wrap
