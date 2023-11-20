from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "superadmin"


class IsRestaurant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "restaurant"


class IsKitchenStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role =='kitchen_staff'


class IsSuperadminOrRestaurantOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "superadmin" or request.user.role == "restaurant"