from django import forms
from .models import Connection


class NewConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'


class DatabaseExportImportForm(forms.Form):
    export_db_name = forms.CharField(
        max_length=50,
        label='Database Name to Export'
    )
    export_db_tables = forms.CharField(
        max_length=255,
        label='Table names to Export',
        required=False,
        help_text='Separate table names with comma (,)'
    )
    export_directory = forms.CharField(
        max_length=255,
        required=False,
        help_text='Move the exported database to another directory'
    )
    import_db_host = forms.CharField(
        max_length=255,
        label='Import Database Host',
        required=False,
        help_text='Host of the Database to import'
    )
    import_db_port = forms.IntegerField(
        label='Import Database Port',
        required=False,
        help_text='Port of the Database to import'
    )
    import_db_user = forms.CharField(
        max_length=50,
        label='Import Database User',
        required=False,
        help_text='User of the Database to Import'
    )
    import_db_pass = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput,
        label='Import Database Password',
        required=False,
        help_text='Password of the User of the Database to Import'
    )
    download_sql = forms.BooleanField(
        label='Download SQL to PC',
        required=False,
        help_text='Unchecking this will leave the sql file in the server'
    )


class ColumnToDIrectoryCompareForm(forms.Form):
    db_name = forms.CharField(
        max_length=50,
        label='Database Name'
    )
    db_table = forms.CharField(
        max_length=50,
        label='Database Table Name to Connect'
    )
    db_column = forms.CharField(
        max_length=30,
        label='Database Column to Compare'
    )
    directory = forms.CharField(
        max_length=255,
        help_text='Directory to Check for matching files'
    )
    backup_directory = forms.CharField(
        max_length=255,
        help_text='Matched files will be backed up here'
    )
    restore_directory = forms.CharField(
        max_length=255,
        help_text='Backed up files will be restored here'
    )
    clear_restore_directory = forms.BooleanField(
        required=False,
        label='Clear restore directory before restoring files'
    )
    delete_backup_directory = forms.BooleanField(
        required=False,
        label='Delete backup directory when done'
    )
