from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from expense_tracker.utils import CustomPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters  
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

class NotificationView(generics.ListAPIView):
    queryset = Notification.objects.all()   
    serializer_class = NotificationSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class UnreadCountAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)

class MarkAsReadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # self, request and id are parameters of the post method of request
    def post(self, request, id):
        notification = Notification.objects.filter(id=id, user=request.user)
        notification.update(is_read=True)
        return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)