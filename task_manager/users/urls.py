from django.urls import path
from task_manager.users.views import UserIndex, UserCreate

urlpatterns = [
    path('', UserIndex.as_view(), name='list_user'),
    path('create/', UserCreate.as_view(), name='create_user'),
]
