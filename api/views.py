from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BucketListSerializer
from .models import BucketList

'''
For using Viewset
'''
# from rest_framework.viewsets import ModelViewSet
# class BucketListViewSet(ModelViewSet):
#     queryset = BucketList.objects.all()
#     serializer_class = BucketListSerializer


class ListCreateView(ListCreateAPIView):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
