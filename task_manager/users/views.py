from django.views import View
from django.shortcuts import render
from django.contrib.auth.models import User
# Create your views here.


class UserIndex(View):

    @staticmethod
    def get(request, *args, **kwargs):
        all_users = User.objects.all()
        return render(request, 'users/index.html', {'users': all_users})
