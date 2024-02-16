from django.urls import path

from task_manager.tasks.views import TaskCreateView
from task_manager.tasks.views import TaskDeleteView
from task_manager.tasks.views import TaskIndexView
from task_manager.tasks.views import TaskUpdateView


urlpatterns = [
    path("", TaskIndexView.as_view(), name="list_task"),
    path("create/", TaskCreateView.as_view(), name="create_task"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="update_task"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="delete_task"),
]
