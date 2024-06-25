#!/usr/bin/env python3

from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'task_manager/index.html')


# Rollbar test
def index(request):
    a = None
    a.hello()  # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")
