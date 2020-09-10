from django.db import models


class Connection(models.Model):
    connection_name = models.CharField(max_length=50)
    db_host = models.CharField(max_length=255, verbose_name='Database Host')
    db_port = models.PositiveIntegerField(blank=True, verbose_name='Database Port')
    db_user = models.CharField(max_length=50, verbose_name='Database User')
    db_pass = models.CharField(max_length=255, verbose_name='Database Password')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
