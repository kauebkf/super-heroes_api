from rest_framework import permissions

class UpdateOwnHeroOnly(permissions.BasePermission):
    """Allow users to edit they own heroes"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return False
