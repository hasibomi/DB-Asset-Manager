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
from .asset_manager import AssetBackupRestore, DatabaseBackupRestore, AssetManager


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

    def handle_form_invalid(self, request, **kwargs):
        return render(
            request,
            self.template_name,
            context={
                'connection': self.get_object(),
                **kwargs
            }
        )

    def handle_column_to_directory_compare(self, request, form):
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

    def handle_database_export_import(self, request, form):
        database_backup_restore = DatabaseBackupRestore()
        database_backup_restore.set_connection(self.get_object())
        database_backup_restore.set_form(form)
        asset_manager = AssetManager()

        try:
            asset_manager.operate(database_backup_restore)
        except Exception as e:
            if str(e) != '':
                messages.error(request, e)
                return redirect('asset_manager:connect', pk=self.kwargs['pk'])

        messages.success(request, 'Database imported')

        return redirect('asset_manager:connect', pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ColumnToDIrectoryCompareForm()
        context['form_database_export_import'] = DatabaseExportImportForm()

        return context

    def post(self, request, *args, **kwargs):
        if 'submit_asset_backup_restore' in request.POST:
            form = ColumnToDIrectoryCompareForm(request.POST)

            if not form.is_valid():
                return self.handle_form_invalid(
                    request,
                    form=form,
                    form_database_export_import=DatabaseExportImportForm()
                )

            return self.handle_column_to_directory_compare(request, form)
        elif 'submit_database_backup_restore' in request.POST:
            form = DatabaseExportImportForm(request.POST)

            if not form.is_valid():
                return self.handle_form_invalid(
                    request,
                    form=ColumnToDIrectoryCompareForm(),
                    form_database_export_import=form
                )

            return self.handle_database_export_import(
                request,
                form
            )


class DeleteAConnection(SuccessMessageMixin, DeleteView):
    model = Connection
    success_message = "%(connection_name) has been deleted"
    success_url = reverse_lazy('asset_manager:index')
