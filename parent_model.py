from django.db import models


class TableMetaData(models.Model):
    created_by = models.CharField(max_length=150)  # Save user id here
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.CharField(max_length=150, blank=True, null=True)  # Save user id here
    is_deleted = models.BooleanField(default=False)
    deleted_by = models.CharField(max_length=150, blank=True, null=True)  # Save user id here
    date_deleted = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
