from rest_framework import permissions


class IsStaffEditorPermission(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    # def get_required_permissions(self, method, model_cls):
    #     kwargs = {
    #         'app_label': model_cls._meta.app_label,
    #         'model_name': model_cls.meta.model_name
    #     }

    #     if method not in self.perms_map:
    #         raise exceptions.MethodNotAllowed(method)

    #     return [perm % kwargs for perm in self.perms_map[method]]

    def has_permission(self, request, view):
        user = request.user
        # print('permissions: -----', user.get_all_permissions())
        # if user.is_staff:
        #     if user.has_perm("products.view_product"):
        #         return True
        #     return True
        return super().has_permission(request, view)

    # def has_object_permission(self, request, view, obj):
    #     return super().has_object_permission(request, view, obj)
