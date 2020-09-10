import os, shutil
from abc import ABCMeta, abstractmethod
from mysql.connector import connect


class IAssetManager(metaclass=ABCMeta):
    @abstractmethod
    def operate(self):
        raise NotImplementedError

    def remove_trailing(self, value, string):
        if value.endswith(string):
            value = value[:-1]

        return value

    def make_dir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)


class AssetBackupRestore(IAssetManager):
    connection_obj = None
    form = None

    def set_connection(self, connection):
        self.connection_obj = connection
    
    def set_form(self, form):
        self.form = form

    def connect(self):
        try:
            return connect(
                host=self.connection_obj.db_host,
                port=self.connection_obj.db_port,
                user=self.connection_obj.db_user,
                password=self.connection_obj.db_pass,
                database=self.form.cleaned_data['db_name']
            )
        except Exception as e:
            raise Exception(e)

    def query(self, connection):
        cursor = connection.cursor()

        cursor.execute(
            'SELECT {} FROM {}'.format(
                self.form.cleaned_data['db_column'],
                self.form.cleaned_data['db_table']
            )
        )

        return cursor

    def backup_files(self, **kwargs):
        for row in kwargs['result']:
            if row[0]:
                file = os.path.join(kwargs['directory'], row[0])
                dest = os.path.join(kwargs['backup_directory'], row[0].split('/')[-1])

                if os.path.exists(file):
                    shutil.copy(file, dest)

    def delete_all_files(self, directory):
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))

    def restore_files(self, directory, restore_directory):
        for file in os.listdir(directory):
            from_file = os.path.join(directory, file)
            to = os.path.join(restore_directory, file)
            shutil.copy(from_file, to)

    def operate(self):
        directory = self.remove_trailing(self.form.cleaned_data['directory'], '/')
        backup_directory = self.remove_trailing(self.form.cleaned_data['backup_directory'], '/')
        restore_directory = self.remove_trailing(self.form.cleaned_data['restore_directory'], '/')
        db_table = self.form.cleaned_data['db_table']
        db_column = self.form.cleaned_data['db_column']

        if not os.path.exists(directory):
            raise Exception('Directory does not exist')

        self.make_dir(backup_directory)
        self.make_dir(restore_directory)

        con = self.connect()
        query = self.query(connection=con)

        self.backup_files(
            result=query.fetchall(),
            directory=directory,
            backup_directory=backup_directory
        )

        if self.form.cleaned_data['clear_restore_directory']:
            self.delete_all_files(restore_directory)

        self.restore_files(backup_directory, restore_directory)

        if self.form.cleaned_data['delete_backup_directory']:
            shutil.rmtree(backup_directory)


class AssetManager():
    def operate(self, asset_manager: IAssetManager):
        asset_manager.operate()
