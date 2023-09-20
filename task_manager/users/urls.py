from django.urls import path
from task_manager.users.views import UserIndex

urlpatterns = [
    path('', UserIndex.as_view())
]
