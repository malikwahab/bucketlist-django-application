from django.test import TestCase
from buppli.models import BucketList, BucketListItem
from django.contrib.auth.models import User


class UserModelTestCase(TestCase):
    """Tests User model"""
    def test_user_model(self):
        user = User.objects.create(username='malikwahab', password='malik')
        self.assertEqual(str(user), 'malikwahab')


class BucketListModelTestCase(TestCase):
    """Tests for the BucketList model"""
    def setUp(self):
        user = User.objects.create(username='malikwahab', password='malik')
        BucketList.objects.create(name='Travel', owner=user)

    def test_bucketlist_model(self):
        user = User.objects.all()[0]
        bucketlist = BucketList.objects.all()[0]
        self.assertEqual(bucketlist.owner, user)
        self.assertEqual(BucketList.objects.count(), 1)


class BucketListItemModelTestCase(TestCase):
    """Tests for the BucketList Item model"""
    def setUp(self):
        user = User.objects.create(username='malikwahab', password='malik')
        bucketlist = BucketList.objects.create(name='Travel', owner=user)
        BucketListItem.objects.create(name='Visit Paris',
                                      bucketlist=bucketlist)

    def test_bucketlist_item_model(self):
        bucketlist = BucketList.objects.all()[0]
        item = BucketListItem.objects.all()[0]
        self.assertEqual(item.bucketlist, bucketlist)
        self.assertEqual(BucketListItem.objects.count(), 1)
