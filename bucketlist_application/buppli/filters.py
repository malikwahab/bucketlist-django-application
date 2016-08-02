from rest_framework import filters


class IsOwnerFilter(filters.BaseFilterBackend):
    """Get only bucketlist belonging to the login user."""

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class IsPublicFilter(filters.BaseFilterBackend):
    """Get public bucketlist."""

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(is_public=True)
