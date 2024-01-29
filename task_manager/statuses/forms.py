from task_manager.statuses.models import Status
from django.forms import ModelForm


class StatusCreationForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']


class StatusUpdateForm(ModelForm):
    class Meta:
        model = Status
        fields = ['name']
