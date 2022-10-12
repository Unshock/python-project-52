from django.shortcuts import render, redirect


# Create your views here.
from django.views.generic import ListView

from task_manager.statuses.models import Status


def stab(request):
    return redirect('home')


class Statuses(ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'status'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Statuses list"
        return context

    #сюда довабить фильтр
    def get_queryset(self):
        return Status.objects.all()
