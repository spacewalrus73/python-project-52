import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskFilter(django_filters.FilterSet):
    """Filter queryset by status, performer, labels and own tasks."""
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    performer = django_filters.ModelChoiceFilter(
        queryset=User.objects.exclude(is_superuser=True)
    )
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all())
    own_task = django_filters.BooleanFilter(
        label=_("Only own tasks"),
        method="get_user_own_tasks",
        widget=forms.CheckboxInput
    )

    def get_user_own_tasks(self, queryset, name, value):
        if value:
            user = self.request.user
            return queryset.filter(author=user)
        return queryset

    class Meta:
        model = Task
        fields = ["status", "performer", "labels", "own_task"]
