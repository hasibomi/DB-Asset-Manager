import os, shutil
from django.shortcuts import (
    render,
    redirect,
    reverse,
    get_object_or_404
)
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    FormView,
    DetailView,
    DeleteView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from mysql.connector import connect
from .models import Connection
from .forms import (
    NewConnectionForm,
    DatabaseExportImportForm,
    ColumnToDIrectoryCompareForm
)
from .asset_manager import AssetBackupRestore, AssetManager


class IndexView(SuccessMessageMixin, CreateView):
    template_name = 'asset_manager/index.html'
    form_class = NewConnectionForm
    success_url = reverse_lazy('asset_manager:index')
    success_message = "%(connection_name) was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connections'] = Connection.objects.all()

        return context


class ConnectToAConnectionView(SuccessMessageMixin, DetailView):
    directory = None
    backup_directory = None
    restore_directory = None
    template_name = 'asset_manager/connect.html'
    model = Connection
    context_object_name = 'connection'

    def remove_trailing(self, value, string):
        if value.endswith(string):
            value = value[:-1]

        return value

    def backup_files(self, query_result):
        for row in query_result:
            if row[0]:
                file = self.directory + '/' + row[0]
                dest = self.backup_directory + '/' + row[0].split('/')[-1]

                if os.path.exists(file):
                    shutil.copy(file, dest)

    def delete_all_files(self, src):
        for file in os.listdir(src):
            os.remove(os.path.join(src, file))

    def restore_files(self, src):
        for file in os.listdir(src):
            from_file = os.path.join(src, file)
            to = os.path.join(self.restore_directory, file)
            shutil.copy(from_file, to)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ColumnToDIrectoryCompareForm()
        context['form_database_export_import'] = DatabaseExportImportForm()

        return context

    def post(self, request, *args, **kwargs):
        form = ColumnToDIrectoryCompareForm(request.POST)
        form_database_export_import = DatabaseExportImportForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                context={
                    'form': form,
                    'form_database_export_import': form_database_export_import,
                    'connection': self.get_object()
                }
            )

        asset_backup_restore = AssetBackupRestore()
        asset_backup_restore.set_connection(self.get_object())
        asset_backup_restore.set_form(form)
        asset_manager = AssetManager()

        try:
            asset_manager.operate(asset_backup_restore)
        except Exception as e:
            messages.error(request, e)
            return redirect('asset_manager:connect', pk=self.kwargs['pk'])

        messages.success(request, 'Files are cleared')
        return redirect('asset_manager:connect', pk=self.kwargs['pk'])


class DeleteAConnection(SuccessMessageMixin, DeleteView):
    model = Connection
    success_message = "%(connection_name) has been deleted"
    success_url = reverse_lazy('asset_manager:index')
