from django.urls import path
from task_manager.users.views import UserIndex, UserCreate, UserUpdate, UserDelete

urlpatterns = [
    path('', UserIndex.as_view(), name='list_user'),
    path('create/', UserCreate.as_view(), name='create_user'),
    path('<int:pk>/update/', UserUpdate.as_view(), name='update_user'),
    path('<int:pk>/delete/', UserDelete.as_view(), name='delete_user'),
]
