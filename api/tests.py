from django.test import TestCase
from .models import BucketList
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
# from .views import BucketListViewSet
import json
from django.contrib.auth import get_user_model

User = get_user_model()


'''
TEST FOR MODELVIEWSET
'''
# class BucketListViewSetTest(TestCase):

#     def create_bucketlist(self, name=''):
#         return BucketList.objects.create(name='My Task')

#     def test_api_can_create_list_destroy_update_bucketlist(self):
#         '''
#         test if api can create bucketlist
#         '''
#         data = {'name': 'My Task Data'}
#         # create_request = APIRequestFactory().post('/api/bucketlist', data)
#         # create_bucketlist = BucketListViewSet.as_view({'post': 'create'})
#         # create_response = create_bucketlist(create_request)
#         # self.assertEquals(create_response.status_code, status.HTTP_201_CREATED)
#         # self.assertEquals(BucketList.objects.count(), 1)

#         create_url = reverse('api:bucket-list')
#         response = self.client.post(create_url, data)
#         self.assertEquals(response.status_code, 201)

#         '''
#         test if api can list bucketlist
#         '''
#         list_request = APIRequestFactory().get('/api/bucketlist')
#         list_bucketlist = BucketListViewSet.as_view({'get': 'list'})
#         list_response = list_bucketlist(list_request)
#         self.assertEquals(list_response.status_code, status.HTTP_200_OK)
#         # json.dumps takes objects and provide string

#         '''
#         test if api can retrieve bucketlist
#         '''
#         bucketlist_obj = BucketList.objects.first()
#         retrieve_request = APIRequestFactory().get('/api/bucketlist')
#         retrieve_bucketlist = BucketListViewSet.as_view({'get': 'retrieve'})
#         retrieve_response = retrieve_bucketlist(retrieve_request, pk=bucketlist_obj.pk)
#         self.assertEqual(retrieve_response.status_code, 200)
#         self.assertIn('My Task Data', json.dumps(list_response.data))

#         '''
#         test if api can update bucketlist
#         '''
#         update_data = {'name': 'My updated Task'}
#         update_request = APIRequestFactory().put('/api/bucketlist', update_data)
#         update_bucketlist = BucketListViewSet.as_view({'put': 'update'})
#         update_response = update_bucketlist(update_request, pk=bucketlist_obj.pk)
#         self.assertEquals(update_response.status_code, status.HTTP_200_OK)
#         self.assertIn('My updated Task', json.dumps(update_response.data))

#         '''
#         test if api can delete bucketlist
#         '''
#         delete_request = APIRequestFactory().delete('/api/bucketlist')
#         delete_bucketlist = BucketListViewSet.as_view({'delete': 'destroy'})
#         delete_response = delete_bucketlist(delete_request, pk=bucketlist_obj.pk)
#         self.assertEquals(delete_response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEquals(BucketList.objects.count(), 0)


class BucketListModelTestCase(TestCase):

    def test_model_can_create_bucket_list(self):
        user = User.objects.create(username='bindeep')
        bucketlist_obj = BucketList.objects.create(owner=user, name='test one')
        self.assertEqual(BucketList.objects.count(), 1)
        self.assertEqual(bucketlist_obj.name, 'test one')


class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='bindeep')
        self.client.force_authenticate(user=self.user)

    def create_bucketlist(self, name=''):
        return BucketList.objects.create(owner=self.user, name='my task')

    def test_api_can_create_bucket_list_with_authorised_user(self):
        data = {'owner': self.user.id, 'name': 'My Task Data'}
        create_url = reverse('api:create')
        create_response = self.client.post(create_url, data, format='json')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(BucketList.objects.count(), 1)
        self.assertIn('My Task Data', json.dumps(create_response.data))

    def test_api_can_create_with_unauthorised_user(self):
        data = {'owner': self.user.id, 'name': 'My Task Data'}
        create_url = reverse('api:create')
        new_client = APIClient()
        create_response = new_client.post(create_url, data)
        self.assertEqual(create_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEquals(BucketList.objects.count(), 1)

    def test_api_can_list_bucket_list_with_authorised_user(self):
        self.create_bucketlist()
        list_url = reverse('api:create')
        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)

    def test_api_can_list_with_unauthorised_user(self):
        self.create_bucketlist()
        list_url = reverse('api:create')
        new_client = APIClient()
        list_response = new_client.post(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_retrieve_bucket_list_with_authorised_user(self):
        retrieve_url = reverse('api:detail', kwargs={'pk': self.create_bucketlist().pk})
        retrieve_response = self.client.get(retrieve_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIn('my task', json.dumps(retrieve_response.data))

    def test_api_can_retrieve_bucket_list_with_unauthorised_user(self):
        retrieve_url = reverse('api:detail', kwargs={'pk': self.create_bucketlist().pk})
        new_client = APIClient()
        retrieve_response = new_client.get(retrieve_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_update_bucket_list_with_authorised_user(self):
        changed_data = {'name': 'My updated Task'}
        update_url = reverse('api:detail', kwargs={'pk': self.create_bucketlist().pk})
        retrieve_response = self.client.put(update_url, changed_data)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertIn('My updated Task', json.dumps(retrieve_response.data))

    def test_api_can_update_bucket_list_with_unauthorised_user(self):
        changed_data = {'name': 'My updated Task'}
        update_url = reverse('api:detail', kwargs={'pk': self.create_bucketlist().pk})
        new_client = APIClient()
        retrieve_response = new_client.put(update_url, changed_data)
        self.assertEqual(retrieve_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_delete_bucket_list_with_authorised_user(self):
        delete_url = reverse('api:detail', kwargs={'pk': self.create_bucketlist().pk})
        delete_response = self.client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(BucketList.objects.exists())

    def test_api_can_delete_bucket_list_with_unauthorised_user(self):
        delete_url = reverse('api:detail', kwargs={'pk': self.create_bucketlist().pk})
        new_client = APIClient()
        delete_response = new_client.delete(delete_url)
        self.assertEqual(delete_response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(BucketList.objects.exists())
