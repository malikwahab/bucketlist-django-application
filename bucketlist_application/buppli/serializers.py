from rest_framework import serializers
from buppli.models import BucketList, BucketListItem
from django.utils.timezone import now
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings


class BucketListItemSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        if not validated_data.get("name"):
            raise serializers.ValidationError("Name cannot be empty")
        return super(BucketListItemSerializer, self).create(validated_data)

    class Meta:
        model = BucketListItem
        fields = ('id', 'name', 'done', 'date_created', 'date_modified',)


class BucketListSerializer(serializers.ModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.username')
    url = serializers.HyperlinkedIdentityField(view_name='bucketlist-detail',
                                               format='html')
    items = BucketListItemSerializer(many=True, read_only=True)

    def create(self, validated_data):
        if not validated_data.get("name"):
            raise serializers.ValidationError("Name cannot be empty")
        return super(BucketListSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.date_modified = now()
        return super(BucketListSerializer, self).update(instance,
                                                        validated_data)

    class Meta:
        model = BucketList
        fields = ('url', 'id', 'name', 'is_public', 'date_modified',
                  'date_created', 'owner', 'items')


class PublicBucketListSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='public_bucketlist'
                                               '-detail', format='html')
    items = BucketListItemSerializer(many=True, read_only=True)

    class Meta:
        model = BucketList
        fields = ('url', 'id', 'name', 'is_public', 'date_modified',
                  'date_created', 'items')


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'last_login', 'password')
