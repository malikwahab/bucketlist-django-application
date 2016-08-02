from rest_framework import permissions
from buppli.models import BucketList


class IsOwner(permissions.BasePermission):
    """Ensure all allowed access is of the object owner."""

    def has_object_permission(self, request, views, obj):
        return obj.owner == request.user


class IsBucketListOwner(IsOwner):
    """Ensure item's bucketlist belong to the requesting user."""

    def has_permission(self, request, view):
        bucketlist = BucketList.objects.get(id=view.kwargs['bucketlist_pk'])
        return super(IsBucketListOwner,
                     self).has_object_permission(request, view, bucketlist)

    def has_object_permission(self, request, views, obj):
        bucketlist = obj.bucketlist
        return super(IsBucketListOwner,
                     self).has_object_permission(request, views, bucketlist)
