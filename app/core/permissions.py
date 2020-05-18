from rest_framework import permissions

class UpdateOwnProfileOnly(permissions.BasePermission):
    """Allow users to edit they own profile"""

    def has_object_permission(self, request, view, obj):
        """Check if user is trying to edit their own profile"""

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id
