from django.urls import path

from task_manager.statuses.views import StatusCreateView
from task_manager.statuses.views import StatusDeleteView
from task_manager.statuses.views import StatusIndexView
from task_manager.statuses.views import StatusUpdateView


urlpatterns = [
    path('', StatusIndexView.as_view(), name='list_status'),
    path('create/', StatusCreateView.as_view(), name='create_status'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='update_status'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='delete_status'),
]
