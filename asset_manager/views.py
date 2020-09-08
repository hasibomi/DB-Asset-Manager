from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Connection
from .forms import NewConnectionForm


class IndexView(SuccessMessageMixin, CreateView):
    template_name = 'asset_manager/index.html'
    form_class = NewConnectionForm
    success_url = reverse_lazy('asset_manager:index')
    success_message = "%(connection_name) was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connections'] = Connection.objects.all()

        return context
