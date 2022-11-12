from math import prod
from rest_framework import permissions


class ReadOrIsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET' and request.user.role != 2:
            return False
        
        return True


class ReadOrIsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.user.is_authenticated and request.user.role == 3:
            return True
        
        return False


class IsAuthenticatedSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 3:
            return True
        
        return False


class IsAllowedToChangeInventory(permissions.BasePermission):
    def has_object_permission(self, request, view, product_obj):
        if request.method == 'GET':
            return True
        elif request.user.is_authenticated and product_obj.store.owner.id == request.user.id:
            return True

        return False