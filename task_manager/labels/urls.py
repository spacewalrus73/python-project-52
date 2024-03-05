from django.urls import path

from task_manager.labels.views import LabelCreateView
from task_manager.labels.views import LabelDeleteView
from task_manager.labels.views import LabelIndexView
from task_manager.labels.views import LabelUpdateView


urlpatterns = [
    path("", LabelIndexView.as_view(), name="list_label"),
    path("create/", LabelCreateView.as_view(), name="create_label"),
    path("<int:pk>/update/", LabelUpdateView.as_view(), name="update_label"),
    path("<int:pk>/delete/", LabelDeleteView.as_view(), name="delete_label"),
]
