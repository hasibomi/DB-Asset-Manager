from django import forms
from .models import Connection


class NewConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'


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
