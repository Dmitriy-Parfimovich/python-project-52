#!/usr/bin/env python3

from django.shortcuts import render
from django.views import View


class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'task_manager/index.html')
