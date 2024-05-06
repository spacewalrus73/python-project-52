from django import forms
from django.forms import ModelForm

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.users.models import User


class TaskForm(ModelForm):
    """Create form for tasks."""
    status = forms.ModelChoiceField(
        queryset=Status.objects.all(),
        required=False,
    )
    performer = forms.ModelChoiceField(
        queryset=User.objects.exclude(is_superuser=True),
        required=False,
    )
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        required=False,
    )

    class Meta:
        model = Task
        fields = ["name", "description", "status", "performer", "labels"]
