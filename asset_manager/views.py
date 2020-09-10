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
            
        # self.directory = self.remove_trailing(form.cleaned_data['directory'], '/')
        # self.backup_directory = self.remove_trailing(form.cleaned_data['backup_directory'], '/')
        # self.restore_directory = self.remove_trailing(form.cleaned_data['restore_directory'], '/')

        # db_name = form.cleaned_data['db_name']
        # db_table = form.cleaned_data['db_table']
        # db_column = form.cleaned_data['db_column']

        # if not os.path.exists(self.directory):
        #     messages.error(
        #         request,
        #         '{} does not exist'.format(self.directory)
        #     )

        #     return redirect('asset_manager:connect', id=self.kwargs['id'])

        # if not os.path.exists(self.backup_directory):
        #     os.makedirs(self.backup_directory)

        # if not os.path.exists(self.restore_directory):
        #     os.makedirs(self.restore_directory)

        # try:
        #     con = connect(
        #         host=self.get_object().db_host,
        #         port=self.get_object().db_port,
        #         user=self.get_object().db_user,
        #         password=self.get_object().db_pass,
        #         database=db_name
        #     )
        # except Exception as e:
        #     messages.error(request, e)
        #     return redirect('asset_manager:connect', pk=self.kwargs['pk'])

        # cursor = con.cursor()

        # cursor.execute(
        #     'SELECT {} FROM {}'.format(
        #         db_column,
        #         db_table
        #     )
        # )

        # self.backup_files(cursor.fetchall())

        # if form.cleaned_data['clear_restore_directory']:
        #     self.delete_all_files(self.restore_directory)

        # self.restore_files(self.backup_directory)

        # if form.cleaned_data['delete_backup_directory']:
        #     shutil.rmtree(self.backup_directory)

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
