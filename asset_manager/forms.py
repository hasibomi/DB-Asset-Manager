from django import forms
from .models import Connection


class NewConnectionForm(forms.ModelForm):
    class Meta:
        model = Connection
        fields = '__all__'


class ColumnToDIrectoryCompareForm(forms.Form):
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
