
from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _

__all__ = (
    'IsDeletedManager',
    'IsDeletedModel'
)


class IsDeletedQuerySet(QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class IsDeletedManager(models.Manager):
    def _get_query_set(self):
        return IsDeletedQuerySet(self.model, using=self._db)

    def get_queryset(self):
        return self._get_query_set().filter(is_deleted=False)

    def get_all(self):
        return self._get_query_set()

    def deleted(self):
        return self._get_query_set().filter(is_deleted=True)


class IsDeletedModel(models.Model):

    is_deleted = models.BooleanField(default=False, editable=False, verbose_name=_('Deleted'))

    objects = IsDeletedManager()

    class Meta:
        abstract = True

    def delete(self, using=None):
        self.is_deleted = True

        self.save(using=using)
