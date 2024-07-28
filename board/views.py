from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.views import View

from .models import Article


@permission_required('polls.add_choice', raise_exception=True)
@login_required
def my_view(request):
    return HttpResponse()


class MyView(LoginRequiredMixin, View):
    login_url = '/login/'
