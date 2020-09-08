import os, shutil
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from mysql.connector import connect
from .models import Connection
from .forms import NewConnectionForm, ColumnToDIrectoryCompareForm


class IndexView(SuccessMessageMixin, CreateView):
    template_name = 'asset_manager/index.html'
    form_class = NewConnectionForm
    success_url = reverse_lazy('asset_manager:index')
    success_message = "%(connection_name) was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connections'] = Connection.objects.all()

        return context


class ConnectToAConnectionView(SuccessMessageMixin, FormView):
    directory = None
    backup_directory = None
    restore_directory = None
    template_name = 'asset_manager/connect.html'
    form_class = ColumnToDIrectoryCompareForm
    success_message = 'Files are cleared'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connection'] = get_object_or_404(Connection, id=self.kwargs['id'])

        return context

    def remove_trailing(self, value, string):
        if value.endswith(string):
            value = value[:-1]

        return value

    def form_valid(self, form):
        self.directory = self.remove_trailing(form.cleaned_data['directory'], '/')
        self.backup_directory = self.remove_trailing(form.cleaned_data['backup_directory'], '/')
        self.restore_directory = self.remove_trailing(form.cleaned_data['restore_directory'], '/')

        if not os.path.exists(self.directory):
            messages.error(
                self.request,
                '{} does not exist'.format(self.directory)
            )

            return redirect('asset_manager:connect', id=self.kwargs['id'])

        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

        if not os.path.exists(self.restore_directory):
            os.makedirs(self.restore_directory)

        connection = get_object_or_404(Connection, id=self.kwargs['id'])

        try:
            con = connect(
                host=connection.db_host,
                port=connection.db_port,
                user=connection.db_user,
                password=connection.db_pass,
                database=connection.db_name
            )
        except Exception as e:
            messages.error(self.request, e)
            return redirect('asset_manager:connect', id=self.kwargs['id'])

        cursor = con.cursor()

        cursor.execute(
            'SELECT {} FROM {}'.format(
                connection.db_column,
                connection.db_table
            )
        )

        self.backup_files(cursor.fetchall())

        if form.cleaned_data['clear_restore_directory']:
            self.delete_all_files(self.restore_directory)

        self.restore_files(self.backup_directory)

        if form.cleaned_data['delete_backup_directory']:
            shutil.rmtree(self.backup_directory)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('asset_manager:connect', kwargs={
            'id': self.kwargs['id']
        })

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


class DeleteAConnection(SuccessMessageMixin, DeleteView):
    model = Connection
    success_message = "%(connection_name) has been deleted"
    success_url = reverse_lazy('asset_manager:index')
