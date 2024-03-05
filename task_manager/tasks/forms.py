from django import forms
from django.forms import ModelForm
from django_filters import FilterSet
from django_filters import ModelChoiceFilter

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskForm(ModelForm):
    """Create form for tasks."""
    status = forms.ModelChoiceField(queryset=Status.objects.all(),
                                    empty_label="Select status")
    performer = forms.ModelChoiceField(
        queryset=User.objects.exclude(is_superuser=True),
        empty_label="Select performer"
    )
    labels = forms.ModelChoiceField(
        queryset=Label.objects.all(),
        empty_label="Select labels",
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "performer"]


class TaskFilterForm(FilterSet):
    """Filter form for tasks."""

    status = ModelChoiceFilter(queryset=Status.objects.all())
    performer = ModelChoiceFilter(
        queryset=User.objects.exclude(is_superuser=True)
    )

    class Meta:
        model = Task
        fields = ["status", "performer"]
