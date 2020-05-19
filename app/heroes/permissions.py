from rest_framework import permissions
from core import models


class UpdateOwnHeroOnly(permissions.BasePermission):
    """Allow users to edit they own heroes"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """Check if the user is trying to update their own status"""

        for item in obj.user_set.all():
            if item.id == request.user.id:
                return True

        return False
