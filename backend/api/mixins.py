
from rest_framework import permissions

from .permissions import IsStaffEditorPermission


class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


class UserQuerySetMixin():
    user_field = 'user'

    """
        We have kept the default value to False here and disabling staff the permission unless explicitily 
        allowed in individual classes that inherit it because we go by the principle that we should always
        keep the least amount of permissions as default and only increase them step by step as conditions pass.
    """
    allow_staff_all = False

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        user = self.request.user

        lookup_data = {}
        lookup_data[self.user_field] = user
        """
            Adding the is_staff check and sending the entire qs if true because if we don't, it will 
            contradict our logic written in permissions.py where we give full access to staff users.

            In order to still have the flexibility to disable staff users permission at times, we bring in another
            variable allow_staff_all which can be defined in individual classes that inherit this mixin. They
            can set it to true if they want to give access
        """
        if self.allow_staff_all and user.is_staff:
            return qs
        return qs.filter(**lookup_data)
