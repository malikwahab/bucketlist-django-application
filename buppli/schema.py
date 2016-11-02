from buppli.models import BucketList, BucketListItem
from graphene import AbstractType, Field, Node
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType


class BucketListNode(DjangoObjectType):

    class Meta:
        model = BucketList
        interfaces = (Node, )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'is_public': ['exact']
        }


class BucketListItemNode(DjangoObjectType):

    class Meta:
        model = BucketListItem
        interfaces = (Node, )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
            'done': ['exact']
        }


class Query(AbstractType):
    bucketlist = Field(BucketListNode)
    all_bucketlist = DjangoFilterConnectionField(BucketListNode)

    bucketlist_item = Field(BucketListItemNode)
    all_bucketlist_item = DjangoFilterConnectionField(BucketListItemNode)
