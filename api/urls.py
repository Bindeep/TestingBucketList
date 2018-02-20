from django.urls import path, include
from .views import ListCreateView, RetrieveUpdateDeleteView

'''
For using ViewSet
'''
# from .views import BucketListViewSet
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register(r'bucketlist', BucketListViewSet, base_name='bucket')
# urlpatterns = router.urls

app_name = 'api'

urlpatterns = [
    path(
        'bucketlist',
        ListCreateView.as_view(),
        name='create'
    ),
    path(
        'bucketlist/<int:pk>',
        RetrieveUpdateDeleteView.as_view(),
        name='detail'
    ),
    path('auth', include('rest_framework.urls', 'rest_framework'))
]
