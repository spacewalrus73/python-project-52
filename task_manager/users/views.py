from django.views import View
from django.shortcuts import render
from .forms import UserRegistrationForm
from task_manager.users.models import User
from django.views.generic.list import ListView
# Create your views here.


class UserIndex(ListView):
    model = User
    paginate_by = 60
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreate(View):

    @staticmethod
    def get(request, *args, **kwargs):
        form = UserRegistrationForm()
        return render(request, 'users/registration.html', {'form': form})
