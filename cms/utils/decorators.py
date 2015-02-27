from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def my_permission_required(perm, login_url=None, raise_exception=False):
    def my_check_perms(user):
        if user.acc_type_id == 1:
            return True
        if not isinstance(perm, (list, tuple)):
            perms = (perm, )
        else:
            perms = perm
        # First check if the user has the permission (even anon users)
        if user.has_perms(perms):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(my_check_perms, login_url=login_url)

