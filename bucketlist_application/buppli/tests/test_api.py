from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from buppli.models import BucketList


class Testauthentication(APITestCase):

    def setUp(self):
        self.reg_url = "/api/auth/register/"
        self.data = {"username": "malikwahab", "password": "malik"}
        self.invalid_data = {"username": "malikwahab"}
        self.response = self.client.post(self.reg_url, self.data,
                                         format="json")

    def tearDown(self):
        User.objects.all().delete()

    def test_create_user(self):
        # assert user was created
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'malikwahab')
        self.assertIn("token", self.response.data)

        # test invalid data supplied and user already exist
        invalid_response = self.client.post(self.reg_url, self.invalid_data,
                                            format="json")
        response = self.client.post(self.reg_url, self.data, format="json")
        self.assertEqual(invalid_response.status_code,
                         response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):
        url = "/api/login/"
        wrong_data = {"username": "malikwahab", "password": "wahab"}

        # test user successful login
        response = self.client.post(url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

        # test login with wrong data and invalid_data
        wrong_response = self.client.post(url, wrong_data, format="json")
        invalid_response = self.client.post(url, self.invalid_data,
                                            format="json")
        self.assertEquals(wrong_response.status_code,
                          invalid_response.status_code,
                          status.HTTP_400_BAD_REQUEST)


class TestBucketListAPI(APITestCase):

    def setUp(self):
        self.url = "/api/bucketlists/"
        self.user = {"username": "malikwahab", "password": "malik"}
        response = self.client.post("/api/auth/register/", self.user,
                                    format="json")
        self.token = "JWT "+response.data.get("token")

    def tearDown(self):
        User.objects.all().delete()
        BucketList.objects.all().delete()

    def create_bucketlist(self):
        data = {"name": "Travel the world"}
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        return self.client.post(self.url, data, format="json")

    def test_unauthorize_access(self):
        # test unauthorize access
        response_post = self.client.post(self.url, {}, format="json")
        response_get = self.client.get(self.url)
        response_put = self.client.put(self.url, {})
        response_delete = self.client.delete(self.url)
        self.assertEquals(response_post.status_code,
                          response_get.status_code,
                          status.HTTP_403_FORBIDDEN)
        self.assertEquals(response_put.status_code,
                          response_delete.status_code,
                          status.HTTP_403_FORBIDDEN)

    def test_create_bucketlist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

        # test create bucketlist
        response = self.create_bucketlist()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # test create bucketlist with invalid data
        invalid_response = self.client.post(self.url, {"name": ''},
                                            format="json")
        self.assertEqual(invalid_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_get_bucketlist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        bucketlist = self.create_bucketlist()
        id = bucketlist.data['id']

        # test get bucketlist
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)

        # test get single bucketlist
        single_response = self.client.get(self.url+"{}/".format(id))
        self.assertEqual(single_response.status_code, status.HTTP_200_OK)
        self.assertEqual(single_response.data['name'], "Travel the world")

        # test get unavalible bucketlist
        not_found_response = self.client.get(self.url+"100/")
        self.assertEqual(not_found_response.status_code,
                         status.HTTP_404_NOT_FOUND)

    def test_edit_bucketlist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        bucketlist = self.create_bucketlist()
        id = bucketlist.data['id']

        # test edit bucketlist
        response = self.client.put(self.url+"{}/".format(id),
                                   {"is_public": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(BucketList.objects.get(pk=id).is_public)

        # test edit invalid bucketlist
        response = self.client.put(self.url+"100/",
                                            {"is_public": 1}, format="json")

    def test_delete_bucketlist(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        bucketlist = self.create_bucketlist()
        id = bucketlist.data['id']

        # test delete bucketlist
        response = self.client.delete(self.url+"{}/".format(id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # test invalid delete
        response = self.client.delete(self.url+"100/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestBucketListItemAPI(APITestCase):
    pass
