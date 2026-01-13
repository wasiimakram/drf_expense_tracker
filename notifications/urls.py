from django.urls import path
from .views import NotificationView, UnreadCountAPIView, MarkAsReadAPIView

urlpatterns = [
    path('', NotificationView.as_view(), name='notifications'),
    path('unread-count/', UnreadCountAPIView.as_view(), name='unread-count'),
    path('mark-as-read/<int:id>/', MarkAsReadAPIView.as_view(), name='mark-as-read'),
]