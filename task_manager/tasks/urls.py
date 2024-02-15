from django.urls import path

from task_manager.tasks.views import TaskCreateView
from task_manager.tasks.views import TaskIndexView

urlpatterns = [
    path("", TaskIndexView.as_view(), name="list_task"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
]
