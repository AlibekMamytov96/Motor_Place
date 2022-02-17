from rest_framework.permissions import IsAuthenticated


class IsSeller(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)

        if not is_authenticated:
            return False

        return request.user.isSeller


class IsBuyer(IsAuthenticated):
    def has_permission(self, request, view):
        is_authenticated = super().has_permission(request, view)

        if not is_authenticated:
            return False

        return request.user.isBuyer