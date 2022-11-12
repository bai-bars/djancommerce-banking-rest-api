from rest_framework import permissions


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 3:
            return True
        
        return False


class IsAuthenticatedStoreOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, store_obj):
        if request.user.is_superuser:
            return True

        if store_obj.owner.id == request.user.id:
            return True

        return False