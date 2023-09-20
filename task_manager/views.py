from django.shortcuts import render
from django.views import View


class Index(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'home.html')
