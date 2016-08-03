from django.contrib.auth.models import User
from buppli.permissions import IsOwner, IsBucketListOwner
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from buppli.models import BucketList, BucketListItem
from rest_framework import (mixins, generics, permissions, viewsets, renderers,
                            status)
from buppli.serializers import (BucketListSerializer, UserSerializer,
                                BucketListItemSerializer,
                                PublicBucketListSerializer)
from rest_framework import filters
from buppli.filters import IsOwnerFilter


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Extends the create mixin to allow just create."""
    pass


class BucketListViewSet(viewsets.ModelViewSet):
    """The API for all bucketlist request.

    Inherits:
        rest_framework.viewsets.ModelViewSet
    """

    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer

    # ensure the bucketlist belong to the requesting authenticated owner
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    filter_backends = (filters.SearchFilter, IsOwnerFilter,)
    search_fields = ('name',)

    def perform_create(self, serializer):
        """Overwrite the parent perform_create to save bucketlist owner."""
        serializer.save(owner=self.request.user)


class BucketListItemViewSet(viewsets.ModelViewSet):
    """The API for all bucketlist item request.

    Inherits:
        rest_framework.viewsets.ModelViewSet
    """

    queryset = BucketListItem.objects.all()
    serializer_class = BucketListItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsBucketListOwner,)

    def perform_create(self, serializer):
        """Overwrite the parent perform_create to save bucketlist-item fk."""
        bucketlist = BucketList.objects.get(id=self.kwargs['bucketlist_pk'])
        serializer.save(bucketlist=bucketlist)

    def get_queryset(self):
        """Get item belonging to the requesting bucketlist."""
        return BucketListItem.objects.filter(bucketlist=self
                                             .kwargs['bucketlist_pk'])


class UserViewSet(CreateViewSet):
    """The API class for creating User.

    Inherits:
        CreateViewSet
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'token': token, 'user': serializer.data},
                        status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class PublicBucketListViewSet(viewsets.ReadOnlyModelViewSet):
    """The API viewset for BucketList avaliable public.

    Inherits:
        rest_framework.viewsets.ReadOnlyModelViewSet
    """

    queryset = BucketList.objects.all()
    serializer_class = PublicBucketListSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return BucketList.objects.filter(is_public=True)
